from django.contrib import admin

from .models import BloqueoAgenda, Visita


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "telefono",
        "cantidad_personas",
        "fecha_evento",
        "fecha_visita",
        "hora_visita",
        "estado",
        "origen",
    )
    list_filter = ("fecha_visita", "estado", "origen")
    search_fields = ("nombre", "telefono", "dni")
    date_hierarchy = "fecha_visita"
    list_editable = ("estado",)
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
                    "estado",
                    "origen",
                ),
            },
        ),
        (
            "Interno",
            {
                "fields": ("observaciones_internas",),
            },
        ),
    )


@admin.register(BloqueoAgenda)
class BloqueoAgendaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora_inicio", "hora_fin", "motivo", "activo")
    list_filter = ("fecha", "activo")
    search_fields = ("motivo",)
