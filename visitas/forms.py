from datetime import date, timedelta, time
from django import forms
from .models import Visita


HORARIOS_VALIDOS = [
    time(17, 0),
    time(17, 30),
    time(18, 0),
    time(18, 30),
    time(19, 0),
    time(19, 30),
]


class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = [
            "cantidad_personas",
            "fecha_evento",
            "fecha_visita",
            "hora_visita",
            "nombre",
            "telefono",
            "dni",
        ]

        widgets = {
            "cantidad_personas": forms.Select(
                attrs={"class": "reserve-input"},
                choices=[
                    (1, "1 persona"),
                    (2, "2 personas"),
                    (3, "3 personas"),
                ],
            ),
            "fecha_evento": forms.DateInput(
                attrs={"type": "date", "class": "reserve-input"}
            ),
            "fecha_visita": forms.DateInput(
                attrs={"type": "date", "class": "reserve-input"}
            ),
            "hora_visita": forms.HiddenInput(),
            "nombre": forms.TextInput(attrs={"class": "reserve-input"}),
            "telefono": forms.TextInput(attrs={"class": "reserve-input"}),
            "dni": forms.TextInput(attrs={"class": "reserve-input"}),
        }

        labels = {
            "cantidad_personas": "Cantidad de personas",
            "fecha_evento": "Fecha del evento",
            "fecha_visita": "Día para la visita",
            "hora_visita": "Horario",
            "nombre": "Nombre",
            "telefono": "Celular",
            "dni": "DNI",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hoy = date.today().isoformat()
        self.fields["fecha_evento"].widget.attrs["min"] = hoy
        self.fields["fecha_visita"].widget.attrs["min"] = hoy

    def clean(self):
        cleaned_data = super().clean()

        cantidad_personas = cleaned_data.get("cantidad_personas")
        fecha_evento = cleaned_data.get("fecha_evento")
        fecha_visita = cleaned_data.get("fecha_visita")
        hora_visita = cleaned_data.get("hora_visita")

        hoy = date.today()

        if cantidad_personas not in [1, 2, 3]:
            self.add_error(
                "cantidad_personas",
                "La cantidad de personas debe ser 1, 2 o 3."
            )

        if fecha_evento and fecha_evento < hoy:
            self.add_error(
                "fecha_evento",
                "La fecha del evento no puede ser anterior a hoy."
            )

        if fecha_evento and fecha_visita:
            if fecha_visita < hoy:
                self.add_error(
                    "fecha_visita",
                    "La fecha de la visita no puede ser anterior a hoy."
                )

            if fecha_visita > fecha_evento:
                self.add_error(
                    "fecha_visita",
                    "La visita no puede ser posterior a la fecha del evento."
                )

            primer_dia_habil = max(hoy, fecha_evento - timedelta(days=30))

            if fecha_visita < primer_dia_habil:
                self.add_error(
                    "fecha_visita",
                    "La visita solo puede reservarse dentro de los 30 días previos al evento."
                )

            if fecha_visita.weekday() > 4:
                self.add_error(
                    "fecha_visita",
                    "Las visitas solo se reservan de lunes a viernes."
                )

        if hora_visita and hora_visita not in HORARIOS_VALIDOS:
            self.add_error(
                "hora_visita",
                "El horario elegido no es válido."
            )

        return cleaned_data