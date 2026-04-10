from django.shortcuts import render
from catalogo.models import (
    Traje,
    Chaleco,
    Cinturon,
    Corbata,
    Camisa,
    Zapato,
    Combo,
)


def home(request):
    traje_importado = (
        Traje.objects
        .filter(linea=Traje.LINEA_IMPORTADA, activo=True)
        .prefetch_related("talles")
        .order_by("-creado")
        .first()
    )

    traje_nacional = (
        Traje.objects
        .filter(linea=Traje.LINEA_NACIONAL, activo=True)
        .prefetch_related("talles")
        .order_by("-creado")
        .first()
    )

    chalecos = (
        Chaleco.objects
        .filter(activo=True)
        .prefetch_related("talles")
        .order_by("-creado")
    )

    cinturones = (
        Cinturon.objects
        .filter(activo=True)
        .order_by("-creado")
    )

    corbatas = (
        Corbata.objects
        .filter(activo=True)
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
        "traje_importado": traje_importado,
        "traje_nacional": traje_nacional,
        "chalecos": chalecos,
        "cinturones": cinturones,
        "corbatas": corbatas,
        "camisas": camisas,
        "zapatos": zapatos,
        "combos": combos,
    })