from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from catalogo.models import (
    Camisa,
    Combo,
    Traje,
    Zapato,
)


def home(request):
    trajes_importados = (
        Traje.objects
        .filter(linea=Traje.LINEA_IMPORTADA, activo=True)
        .prefetch_related("talles")
        .order_by("-creado")
    )

    trajes_nacionales = (
        Traje.objects
        .filter(linea=Traje.LINEA_NACIONAL, activo=True)
        .prefetch_related("talles")
        .order_by("-creado")
    )

    camisas = (
        Camisa.objects
        .filter(activo=True)
        .prefetch_related("talles")
        .order_by("-creado")
    )

    zapatos = (
        Zapato.objects
        .filter(activo=True)
        .prefetch_related("talles")
        .order_by("-creado")
    )

    combos = (
        Combo.objects
        .filter(activo=True)
        .order_by("orden", "id")
    )

    return render(request, "core/home.html", {
        "trajes_importados": trajes_importados,
        "trajes_nacionales": trajes_nacionales,
        "camisas": camisas,
        "zapatos": zapatos,
        "combos": combos,
    })


@staff_member_required(login_url="/admin/login/")
def panel_privado(request):
    return render(request, "core/panel_privado.html")
