from django.core.exceptions import ValidationError
from django.db import models


class Visita(models.Model):
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_REALIZADA = "REALIZADA"
    ESTADO_NO_ASISTIO = "NO_ASISTIO"

    ESTADOS = [
        (ESTADO_CONFIRMADA, "Confirmada"),
        (ESTADO_CANCELADA, "Cancelada"),
        (ESTADO_REALIZADA, "Realizada"),
        (ESTADO_NO_ASISTIO, "No asistio"),
    ]

    ORIGEN_WEB = "WEB"
    ORIGEN_MANUAL = "MANUAL"

    ORIGENES = [
        (ORIGEN_WEB, "Web"),
        (ORIGEN_MANUAL, "Manual"),
    ]

    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    telefono = models.CharField(max_length=30)
    cantidad_personas = models.PositiveIntegerField()
    fecha_evento = models.DateField()
    fecha_visita = models.DateField()
    hora_visita = models.TimeField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_CONFIRMADA,
    )
    origen = models.CharField(
        max_length=20,
        choices=ORIGENES,
        default=ORIGEN_WEB,
    )
    observaciones_internas = models.TextField(blank=True, default="")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_visita", "-hora_visita", "-creado"]

    def __str__(self):
        return f"{self.nombre} - {self.fecha_visita} {self.hora_visita}"


class BloqueoAgenda(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    motivo = models.CharField(max_length=200, blank=True, default="")
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora_inicio", "id"]
        verbose_name = "Bloqueo de agenda"
        verbose_name_plural = "Bloqueos de agenda"

    def clean(self):
        if bool(self.hora_inicio) != bool(self.hora_fin):
            raise ValidationError(
                "Si indicas un horario de inicio, tambien debes indicar el de fin."
            )

        if self.hora_inicio and self.hora_fin and self.hora_inicio >= self.hora_fin:
            raise ValidationError(
                "La hora de fin debe ser posterior a la hora de inicio."
            )

    def __str__(self):
        if self.hora_inicio and self.hora_fin:
            return f"{self.fecha} {self.hora_inicio}-{self.hora_fin}"
        return f"{self.fecha} bloqueada"
