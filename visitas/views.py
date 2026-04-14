from datetime import datetime, time

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VisitaForm
from .models import BloqueoAgenda, Visita


HORARIOS_BASE = [
    time(17, 0),
    time(17, 30),
    time(18, 0),
    time(18, 30),
    time(19, 0),
    time(19, 30),
]

HORARIOS_INDEX = {hora: idx for idx, hora in enumerate(HORARIOS_BASE)}


def _fmt_hora(hora):
    return hora.strftime("%H:%M")


def _bloqueos_para_fecha(fecha_visita):
    return list(
        BloqueoAgenda.objects
        .filter(fecha=fecha_visita, activo=True)
        .order_by("hora_inicio", "id")
    )


def _hora_bloqueada(hora, bloqueos):
    for bloqueo in bloqueos:
        if bloqueo.hora_inicio is None or bloqueo.hora_fin is None:
            return True

        if bloqueo.hora_inicio <= hora < bloqueo.hora_fin:
            return True

    return False


def _capacidad_por_horario(fecha_visita, visitas_dia=None, bloqueos=None):
    if visitas_dia is None:
        visitas_dia = (
            Visita.objects
            .filter(
                fecha_visita=fecha_visita,
                estado=Visita.ESTADO_CONFIRMADA,
            )
            .order_by("hora_visita", "creado")
        )

    if bloqueos is None:
        bloqueos = _bloqueos_para_fecha(fecha_visita)

    capacidad = {
        hora: 0 if _hora_bloqueada(hora, bloqueos) else 2
        for hora in HORARIOS_BASE
    }

    for visita in visitas_dia:
        hora = visita.hora_visita
        personas = visita.cantidad_personas

        if hora not in capacidad:
            continue

        if personas == 1:
            capacidad[hora] = max(capacidad[hora] - 1, 0)

        elif personas == 2:
            capacidad[hora] = max(capacidad[hora] - 2, 0)

        elif personas == 3:
            capacidad[hora] = max(capacidad[hora] - 2, 0)

            idx = HORARIOS_INDEX[hora]
            if idx + 1 < len(HORARIOS_BASE):
                siguiente = HORARIOS_BASE[idx + 1]
                capacidad[siguiente] = max(capacidad[siguiente] - 1, 0)

    return capacidad


def _horario_admite_reserva(capacidad, hora, cantidad_personas):
    if hora not in capacidad:
        return False

    idx = HORARIOS_INDEX[hora]
    libres_en_bloque = capacidad[hora]

    if cantidad_personas == 1:
        return libres_en_bloque >= 1

    if cantidad_personas == 2:
        return libres_en_bloque >= 2

    if cantidad_personas == 3:
        if idx + 1 >= len(HORARIOS_BASE):
            return False

        siguiente = HORARIOS_BASE[idx + 1]
        libres_siguiente = capacidad[siguiente]

        return libres_en_bloque >= 2 and libres_siguiente >= 1

    return False


def _horarios_disponibles_para_fecha(fecha_visita, cantidad_personas):
    bloqueos = _bloqueos_para_fecha(fecha_visita)
    capacidad = _capacidad_por_horario(
        fecha_visita,
        bloqueos=bloqueos,
    )
    horarios_disponibles = []

    for hora in HORARIOS_BASE:
        if _horario_admite_reserva(capacidad, hora, cantidad_personas):
            horarios_disponibles.append(hora)

    return horarios_disponibles


def _paso_inicial(form):
    if not form.errors:
        return 1

    if any(campo in form.errors for campo in ["nombre", "telefono", "dni"]):
        return 4

    if "hora_visita" in form.errors:
        return 3

    if "fecha_visita" in form.errors:
        return 2

    return 1


def reservar(request):
    if request.method == "POST":
        form = VisitaForm(request.POST)

        if form.is_valid():
            fecha_visita = form.cleaned_data["fecha_visita"]
            hora_visita = form.cleaned_data["hora_visita"]
            cantidad_personas = form.cleaned_data["cantidad_personas"]

            with transaction.atomic():
                visitas_dia = list(
                    Visita.objects
                    .select_for_update()
                    .filter(
                        fecha_visita=fecha_visita,
                        estado=Visita.ESTADO_CONFIRMADA,
                    )
                    .order_by("hora_visita", "creado")
                )
                bloqueos = _bloqueos_para_fecha(fecha_visita)
                capacidad = _capacidad_por_horario(
                    fecha_visita,
                    visitas_dia=visitas_dia,
                    bloqueos=bloqueos,
                )

                if not _horario_admite_reserva(capacidad, hora_visita, cantidad_personas):
                    form.add_error(
                        "hora_visita",
                        "Ese horario esta lleno, bloqueado o no tiene cupo suficiente. Elegi otro.",
                    )
                else:
                    visita = form.save(commit=False)
                    visita.estado = Visita.ESTADO_CONFIRMADA
                    visita.origen = Visita.ORIGEN_WEB
                    visita.save()
                    request.session["ultima_visita_id"] = visita.id
                    return redirect("visitas:confirmada")
    else:
        form = VisitaForm()

    return render(
        request,
        "visitas/reservar.html",
        {
            "form": form,
            "initial_step": _paso_inicial(form),
        },
    )


def confirmada(request):
    visita_id = request.session.get("ultima_visita_id")

    if not visita_id:
        return redirect("visitas:reservar")

    visita = get_object_or_404(Visita, pk=visita_id)

    return render(
        request,
        "visitas/confirmada.html",
        {
            "visita": visita,
        },
    )


def horarios_disponibles(request):
    fecha_str = request.GET.get("fecha")
    personas_str = request.GET.get("personas")

    if not fecha_str or not personas_str:
        return JsonResponse({"horarios": []})

    try:
        fecha_visita = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        cantidad_personas = int(personas_str)
    except (ValueError, TypeError):
        return JsonResponse({"horarios": []})

    if cantidad_personas not in [1, 2, 3]:
        return JsonResponse({"horarios": []})

    if fecha_visita.weekday() > 4:
        return JsonResponse({"horarios": []})

    horarios = _horarios_disponibles_para_fecha(
        fecha_visita,
        cantidad_personas,
    )

    return JsonResponse({
        "horarios": [_fmt_hora(h) for h in horarios],
    })
