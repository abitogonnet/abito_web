from django.db import models


class Visita(models.Model):

    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    telefono = models.CharField(max_length=30)

    cantidad_personas = models.PositiveIntegerField()

    fecha_evento = models.DateField()

    fecha_visita = models.DateField()
    hora_visita = models.TimeField()

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.fecha_visita} {self.hora_visita}"