from django.urls import path
from . import views

app_name = "visitas"

urlpatterns = [

    path(
        "reservar/",
        views.reservar,
        name="reservar"
    ),

    path(
        "horarios-disponibles/",
        views.horarios_disponibles,
        name="horarios_disponibles"
    ),

]