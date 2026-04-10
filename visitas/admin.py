from django.contrib import admin
from .models import Visita


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "telefono",
        "cantidad_personas",
        "fecha_evento",
        "fecha_visita",
        "hora_visita",
    )

    list_filter = ("fecha_visita",)

    search_fields = ("nombre", "telefono", "dni")