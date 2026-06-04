import calendar
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta

from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.formats import date_format

from .models import BloqueoAgenda, PreferenciaAmboVisita, Visita

AGENDA_SLOT_LABELS = (
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
)


def _parse_month(value):
    if not value:
        return timezone.localdate().replace(day=1)

    try:
        return datetime.strptime(value, "%Y-%m").date().replace(day=1)
    except ValueError:
        return timezone.localdate().replace(day=1)


def _parse_selected_day(value, current_month):
    if not value:
        return None

    try:
        selected_day = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

    if (
        selected_day.year != current_month.year
        or selected_day.month != current_month.month
    ):
        return None

    return selected_day


def _month_bounds(current_month):
    _, last_day = calendar.monthrange(current_month.year, current_month.month)
    return current_month, current_month.replace(day=last_day)


def _previous_month(current_month):
    return (current_month - timedelta(days=1)).replace(day=1)


def _next_month(current_month):
    return (current_month.replace(day=28) + timedelta(days=4)).replace(day=1)


def _parse_selected_visit_id(value):
    if not value:
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _empty_day_payload():
    return {
        "visits": [],
        "slots": [
            {
                "hora": slot_label,
                "label": slot_label,
                "visit_count": 0,
                "people_count": 0,
                "visits": [],
            }
            for slot_label in AGENDA_SLOT_LABELS
        ],
    }


def _build_day_payload(visits):
    slot_map = OrderedDict((slot_label, []) for slot_label in AGENDA_SLOT_LABELS)

    for visit in visits:
        slot_map.setdefault(visit["hora"], [])
        slot_map[visit["hora"]].append(visit)

    extra_slots = sorted(
        slot_label
        for slot_label in slot_map.keys()
        if slot_label not in AGENDA_SLOT_LABELS
    )
    ordered_labels = list(AGENDA_SLOT_LABELS) + extra_slots

    return {
        "visits": visits,
        "slots": [
            {
                "hora": slot_label,
                "label": slot_label,
                "visit_count": len(slot_map[slot_label]),
                "people_count": sum(
                    visit["cantidad_personas"]
                    for visit in slot_map[slot_label]
                ),
                "visits": slot_map[slot_label],
            }
            for slot_label in ordered_labels
        ],
    }


class PreferenciaAmboVisitaInline(admin.TabularInline):
    model = PreferenciaAmboVisita
    extra = 0
    can_delete = False
    readonly_fields = (
        "orden",
        "traje",
        "linea",
        "tela",
        "color",
        "talle_saco",
        "talle_pantalon",
        "creado",
    )
    fields = (
        "orden",
        "traje",
        "linea",
        "tela",
        "color",
        "talle_saco",
        "talle_pantalon",
        "creado",
    )

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    change_list_template = "admin/visitas/visita/change_list.html"
    list_display = (
        "nombre",
        "dni",
        "telefono",
        "cantidad_personas",
        "fecha_evento",
        "fecha_visita",
        "hora_visita",
        "vio_catalogo_resumen",
        "cantidad_preferencias",
        "estado",
        "origen",
        "observaciones_resumen",
        "creado",
        "actualizado",
    )
    list_filter = (
        "fecha_visita",
        "fecha_evento",
        "estado",
        "origen",
        "vio_prendas_catalogo",
    )
    search_fields = ("nombre", "telefono", "dni")
    date_hierarchy = "fecha_visita"
    list_editable = ("estado",)
    ordering = ("-fecha_visita", "-hora_visita", "-creado")
    readonly_fields = ("creado", "actualizado")
    list_per_page = 50
    save_on_top = True
    show_full_result_count = False
    show_facets = admin.ShowFacets.NEVER
    inlines = [PreferenciaAmboVisitaInline]
    fieldsets = (
        (
            "Datos del cliente",
            {
                "fields": ("nombre", "telefono", "dni"),
            },
        ),
        (
            "Reserva",
            {
                "fields": (
                    "cantidad_personas",
                    "fecha_evento",
                    "fecha_visita",
                    "hora_visita",
                    "vio_prendas_catalogo",
                    "estado",
                    "origen",
                ),
            },
        ),
        (
            "Interno",
            {
                "fields": ("observaciones_internas", "creado", "actualizado"),
            },
        ),
    )

    def get_urls(self):
        custom_urls = [
            path(
                "agenda/",
                self.admin_site.admin_view(self.agenda_view),
                name="visitas_visita_agenda",
            ),
        ]
        return custom_urls + super().get_urls()

    def changelist_view(self, request, extra_context=None):
        if request.GET.get("vista") == "lista":
            extra_context = extra_context or {}
            extra_context["agenda_url"] = reverse("admin:visitas_visita_changelist")
            request.GET = request.GET.copy()
            request.GET.pop("vista", None)
            request.META["QUERY_STRING"] = request.GET.urlencode()
            return super().changelist_view(request, extra_context=extra_context)

        return self.agenda_view(request)

    def agenda_view(self, request):
        current_month = _parse_month(request.GET.get("mes"))
        month_start, month_end = _month_bounds(current_month)
        today = timezone.localdate()
        selected_visit_id = _parse_selected_visit_id(request.GET.get("visita"))

        month_visits = list(
            Visita.objects.filter(
                fecha_visita__gte=month_start,
                fecha_visita__lte=month_end,
            )
            .prefetch_related("preferencias_ambos")
            .annotate(cantidad_preferencias_total=Count("preferencias_ambos"))
            .order_by("fecha_visita", "hora_visita", "creado")
        )

        day_summaries = {}
        day_details = defaultdict(list)

        for visit in month_visits:
            day_key = visit.fecha_visita.isoformat()
            summary = day_summaries.setdefault(
                day_key,
                {
                    "visit_count": 0,
                    "people_count": 0,
                    "time_slots": OrderedDict(),
                },
            )
            time_key = visit.hora_visita.strftime("%H:%M")

            summary["visit_count"] += 1
            summary["people_count"] += visit.cantidad_personas

            slot = summary["time_slots"].setdefault(
                time_key,
                {
                    "label": time_key,
                    "visit_count": 0,
                    "people_count": 0,
                },
            )
            slot["visit_count"] += 1
            slot["people_count"] += visit.cantidad_personas

            if visit.vio_prendas_catalogo is None:
                vio_catalogo = "-"
            else:
                vio_catalogo = "Si" if visit.vio_prendas_catalogo else "No"

            preferencias = []
            for preference in visit.preferencias_ambos.all():
                preferencias.append(
                    {
                        "orden": preference.orden,
                        "linea": preference.linea or "-",
                        "tela": preference.tela or "-",
                        "color": preference.color or "-",
                        "talle_saco": preference.talle_saco or "-",
                        "talle_pantalon": preference.talle_pantalon or "-",
                    }
                )

            day_details[day_key].append(
                {
                    "id": visit.id,
                    "hora": time_key,
                    "nombre": visit.nombre,
                    "telefono": visit.telefono,
                    "dni": visit.dni,
                    "cantidad_personas": visit.cantidad_personas,
                    "fecha_evento": visit.fecha_evento.strftime("%d/%m/%Y"),
                    "fecha_visita": visit.fecha_visita.strftime("%d/%m/%Y"),
                    "estado": visit.get_estado_display(),
                    "estado_key": visit.estado.lower(),
                    "origen": visit.get_origen_display(),
                    "vio_catalogo": vio_catalogo,
                    "cantidad_preferencias": visit.cantidad_preferencias_total,
                    "observaciones": visit.observaciones_internas.strip() or "-",
                    "creado": date_format(
                        timezone.localtime(visit.creado),
                        "j/m/Y H:i",
                    ),
                    "actualizado": date_format(
                        timezone.localtime(visit.actualizado),
                        "j/m/Y H:i",
                    ),
                    "preferencias": preferencias,
                    "admin_url": reverse(
                        "admin:visitas_visita_change",
                        args=[visit.pk],
                    ),
                }
            )

        active_days = sorted(day_summaries.keys())
        selected_day = _parse_selected_day(request.GET.get("fecha"), current_month)

        if selected_day is None:
            today_key = today.isoformat()
            if today.year == current_month.year and today.month == current_month.month:
                selected_day = today
            elif active_days:
                selected_day = datetime.strptime(active_days[0], "%Y-%m-%d").date()
            else:
                selected_day = month_start

        selected_day_key = selected_day.isoformat()
        calendar_rows = []
        month_calendar = calendar.Calendar(firstweekday=0)

        for week in month_calendar.monthdatescalendar(
            current_month.year,
            current_month.month,
        ):
            week_cells = []

            for day in week:
                day_key = day.isoformat()
                summary = day_summaries.get(day_key)
                slots = []

                if summary:
                    for slot in list(summary["time_slots"].values())[:3]:
                        slots.append(slot)

                week_cells.append(
                    {
                        "date": day,
                        "date_key": day_key,
                        "day_number": day.day,
                        "is_current_month": day.month == current_month.month,
                        "is_today": day == today,
                        "is_selected": day_key == selected_day_key,
                        "has_activity": bool(summary),
                        "visit_count": summary["visit_count"] if summary else 0,
                        "people_count": summary["people_count"] if summary else 0,
                        "time_slots": slots,
                        "extra_slot_count": (
                            len(summary["time_slots"]) - len(slots) if summary else 0
                        ),
                    }
                )

            calendar_rows.append(week_cells)

        total_people = sum(item["people_count"] for item in day_summaries.values())
        day_payloads = {
            day_key: _build_day_payload(rows)
            for day_key, rows in day_details.items()
        }
        selected_day_payload = day_payloads.get(selected_day_key, _empty_day_payload())
        selected_visit = None

        if selected_visit_id is not None:
            selected_visit = next(
                (
                    visit
                    for visit in selected_day_payload["visits"]
                    if visit["id"] == selected_visit_id
                ),
                None,
            )

        if selected_visit is None and selected_day_payload["visits"]:
            selected_visit = selected_day_payload["visits"][0]

        selected_day_label = date_format(selected_day, "l j \\d\\e F \\d\\e Y")

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "Agenda de visitas",
            "subtitle": "Calendario mensual",
            "agenda_url": reverse("admin:visitas_visita_changelist"),
            "list_url": f"{reverse('admin:visitas_visita_changelist')}?vista=lista",
            "month_value": current_month.strftime("%Y-%m"),
            "month_label": date_format(current_month, "F Y"),
            "previous_month": _previous_month(current_month).strftime("%Y-%m"),
            "next_month": _next_month(current_month).strftime("%Y-%m"),
            "selected_day_key": selected_day_key,
            "selected_day_label": selected_day_label,
            "calendar_rows": calendar_rows,
            "day_payloads": day_payloads,
            "selected_day_payload": selected_day_payload,
            "selected_visit": selected_visit,
            "selected_visit_id": selected_visit["id"] if selected_visit else "",
            "month_visit_count": len(month_visits),
            "month_people_count": total_people,
            "active_day_count": len(active_days),
        }
        return TemplateResponse(
            request,
            "admin/visitas/visita/agenda.html",
            context,
        )

    @admin.display(boolean=False, description="Vio catalogo")
    def vio_catalogo_resumen(self, obj):
        if obj.vio_prendas_catalogo is None:
            return "-"
        return "Si" if obj.vio_prendas_catalogo else "No"

    @admin.display(description="Ambos vistos")
    def cantidad_preferencias(self, obj):
        if hasattr(obj, "cantidad_preferencias_total"):
            return obj.cantidad_preferencias_total
        return obj.preferencias_ambos.count()

    @admin.display(description="Observaciones")
    def observaciones_resumen(self, obj):
        if not obj.observaciones_internas:
            return "-"

        if len(obj.observaciones_internas) <= 40:
            return obj.observaciones_internas

        return f"{obj.observaciones_internas[:37]}..."


@admin.register(BloqueoAgenda)
class BloqueoAgendaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora_inicio", "hora_fin", "motivo", "activo")
    list_filter = ("fecha", "activo")
    search_fields = ("motivo",)
    save_on_top = True
    show_full_result_count = False
    show_facets = admin.ShowFacets.NEVER
