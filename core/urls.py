from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('panel/', views.panel_privado, name='panel_privado'),
]
