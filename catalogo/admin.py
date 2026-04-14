from django.contrib import admin

from .models import (
    Camisa,
    Chaleco,
    Cinturon,
    Combo,
    Corbata,
    TalleColorCamisa,
    TalleColorChaleco,
    TalleColorTraje,
    TalleColorZapato,
    Traje,
    Zapato,
)


class TalleColorTrajeInline(admin.TabularInline):
    model = TalleColorTraje
    extra = 1


class TalleColorChalecoInline(admin.TabularInline):
    model = TalleColorChaleco
    extra = 1


class TalleColorCamisaInline(admin.TabularInline):
    model = TalleColorCamisa
    extra = 1


class TalleColorZapatoInline(admin.TabularInline):
    model = TalleColorZapato
    extra = 1


@admin.register(Traje)
class TrajeAdmin(admin.ModelAdmin):
    list_display = ("id", "linea", "tela", "precio", "activo", "creado")
    list_filter = ("linea", "activo")
    search_fields = ("tela", "descripcion")
    inlines = [TalleColorTrajeInline]
    fieldsets = (
        (
            "Datos principales",
            {
                "fields": ("linea", "tela", "descripcion", "precio", "activo"),
            },
        ),
        (
            "Fotos",
            {
                "fields": ("foto_modelo", "foto_colgado"),
            },
        ),
    )


@admin.register(Chaleco)
class ChalecoAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("descripcion",)
    inlines = [TalleColorChalecoInline]
    fields = ("descripcion", "precio", "activo", "foto_modelo", "foto_colgado")


@admin.register(Cinturon)
class CinturonAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("descripcion",)
    fields = ("descripcion", "precio", "activo", "foto_1", "foto_2")


@admin.register(Corbata)
class CorbataAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("descripcion",)
    fields = ("descripcion", "precio", "activo", "foto_1", "foto_2")


@admin.register(Camisa)
class CamisaAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("descripcion",)
    inlines = [TalleColorCamisaInline]
    fields = ("descripcion", "precio", "activo", "foto_modelo", "foto_colgado")


@admin.register(Zapato)
class ZapatoAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    search_fields = ("descripcion",)
    inlines = [TalleColorZapatoInline]
    fields = ("descripcion", "precio", "activo", "foto_modelo", "foto_colgado")


@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orden",
        "nombre",
        "precio_importado",
        "precio_nacional",
        "precio_ninos",
        "precio_unico",
        "activo",
    )
    list_filter = ("activo",)
    search_fields = ("nombre", "descripcion")
    ordering = ("orden", "id")
