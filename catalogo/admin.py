from django.contrib import admin
from .models import (
    Traje,
    TalleColorTraje,
    Chaleco,
    TalleColorChaleco,
    Cinturon,
    Corbata,
    Camisa,
    TalleColorCamisa,
    Zapato,
    TalleColorZapato,
    Combo,
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
    search_fields = ("tela",)
    inlines = [TalleColorTrajeInline]


@admin.register(Chaleco)
class ChalecoAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    inlines = [TalleColorChalecoInline]


@admin.register(Cinturon)
class CinturonAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)


@admin.register(Corbata)
class CorbataAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)


@admin.register(Camisa)
class CamisaAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    inlines = [TalleColorCamisaInline]


@admin.register(Zapato)
class ZapatoAdmin(admin.ModelAdmin):
    list_display = ("id", "precio", "activo", "creado")
    list_filter = ("activo",)
    inlines = [TalleColorZapatoInline]


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