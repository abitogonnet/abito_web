from django.contrib import admin

from .models import BloqueoAgenda, PreferenciaAmboVisita, Visita


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

    @admin.display(boolean=False, description="Vio catalogo")
    def vio_catalogo_resumen(self, obj):
        if obj.vio_prendas_catalogo is None:
            return "-"
        return "Si" if obj.vio_prendas_catalogo else "No"

    @admin.display(description="Ambos vistos")
    def cantidad_preferencias(self, obj):
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
