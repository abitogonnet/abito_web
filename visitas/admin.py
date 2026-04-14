from django.contrib import admin

from .models import BloqueoAgenda, Visita


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
        "estado",
        "origen",
        "observaciones_resumen",
        "creado",
        "actualizado",
    )
    list_filter = ("fecha_visita", "fecha_evento", "estado", "origen")
    search_fields = ("nombre", "telefono", "dni")
    date_hierarchy = "fecha_visita"
    list_editable = ("estado",)
    ordering = ("-fecha_visita", "-hora_visita", "-creado")
    readonly_fields = ("creado", "actualizado")
    list_per_page = 50
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
                "fields": ("observaciones_internas", "creado", "actualizado"),
            },
        ),
    )

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
