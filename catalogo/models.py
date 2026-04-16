from django.db import models

from core.models import ConfiguracionSitio


class Traje(models.Model):
    LINEA_IMPORTADA = "IMPORTADO"
    LINEA_NACIONAL = "NACIONAL"
    LINEA_UNICO = "UNICO"

    LINEAS = [
        (LINEA_IMPORTADA, "Linea importada"),
        (LINEA_NACIONAL, "Linea nacional"),
        (LINEA_UNICO, "Talles unicos"),
    ]

    linea = models.CharField(max_length=20, choices=LINEAS)
    foto_modelo = models.ImageField(upload_to="trajes/")
    foto_colgado = models.ImageField(upload_to="trajes/")
    tela = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["linea", "-creado"]

    def __str__(self):
        return f"{self.get_linea_display()} - {self.tela}"


class TalleColorTraje(models.Model):
    traje = models.ForeignKey(
        Traje,
        on_delete=models.CASCADE,
        related_name="talles",
    )
    color = models.CharField(max_length=50)
    talle_saco = models.CharField(max_length=50)
    talle_pantalon = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.color} | Saco {self.talle_saco} | Pantalon {self.talle_pantalon}"


class Chaleco(models.Model):
    foto_modelo = models.ImageField(upload_to="chalecos/")
    foto_colgado = models.ImageField(upload_to="chalecos/")
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        if self.descripcion:
            return f"Chaleco - {self.descripcion[:40]}"
        return f"Chaleco #{self.id}"


class TalleColorChaleco(models.Model):
    chaleco = models.ForeignKey(
        Chaleco,
        on_delete=models.CASCADE,
        related_name="talles",
    )
    color = models.CharField(max_length=50)
    talle = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.color} | Talle {self.talle}"


class Cinturon(models.Model):
    foto_1 = models.ImageField(upload_to="cinturones/")
    foto_2 = models.ImageField(upload_to="cinturones/")
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        if self.descripcion:
            return f"Cinturon - {self.descripcion[:40]}"
        return f"Cinturon #{self.id}"


class Corbata(models.Model):
    foto_1 = models.ImageField(upload_to="corbatas/")
    foto_2 = models.ImageField(upload_to="corbatas/")
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        if self.descripcion:
            return f"Corbata - {self.descripcion[:40]}"
        return f"Corbata #{self.id}"


class Camisa(models.Model):
    foto_modelo = models.ImageField(upload_to="camisas/")
    foto_colgado = models.ImageField(upload_to="camisas/")
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        if self.descripcion:
            return f"Camisa - {self.descripcion[:40]}"
        return f"Camisa #{self.id}"


class TalleColorCamisa(models.Model):
    camisa = models.ForeignKey(
        Camisa,
        on_delete=models.CASCADE,
        related_name="talles",
    )
    color = models.CharField(max_length=50)
    talle = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.color} | Talle {self.talle}"


class Zapato(models.Model):
    foto_modelo = models.ImageField(upload_to="zapatos/")
    foto_colgado = models.ImageField(upload_to="zapatos/")
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        if self.descripcion:
            return f"Zapato - {self.descripcion[:40]}"
        return f"Zapato #{self.id}"


class TalleColorZapato(models.Model):
    zapato = models.ForeignKey(
        Zapato,
        on_delete=models.CASCADE,
        related_name="talles",
    )
    color = models.CharField(max_length=50)
    talle = models.CharField(max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.color} | Talle {self.talle}"


class Combo(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="combos/")
    descripcion = models.TextField(blank=True, default="")
    precio_importado = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nacional = models.DecimalField(max_digits=10, decimal_places=2)
    precio_ninos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_unico = models.DecimalField(max_digits=10, decimal_places=2)
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return self.nombre


class ConfiguracionVisitas(ConfiguracionSitio):
    class Meta:
        proxy = True
        app_label = "catalogo"
        verbose_name = "Direccion de visitas"
        verbose_name_plural = "Direccion de visitas"
