from django.contrib import admin
from .models import ConfiguracionSitio


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Canales publicos",
            {
                "fields": ("whatsapp_url", "instagram_url"),
            },
        ),
        (
            "Reserva y confirmacion",
            {
                "fields": ("direccion_post_reserva", "mensaje_confirmacion"),
            },
        ),
    )

    def has_add_permission(self, request):
        if ConfiguracionSitio.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "ABITO Administracion"
admin.site.site_title = "ABITO Admin"
admin.site.index_title = "Gestion interna"
