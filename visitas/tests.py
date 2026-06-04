from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Visita


class VisitaAdminAgendaTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="secret123",
        )
        self.client.force_login(self.user)

    def test_changelist_shows_agenda_by_default(self):
        today = timezone.localdate()
        visita = Visita.objects.create(
            nombre="Juan Perez",
            dni="12345678",
            telefono="2215551234",
            cantidad_personas=2,
            fecha_evento=today + timedelta(days=20),
            fecha_visita=today,
            hora_visita="17:00",
            estado=Visita.ESTADO_CONFIRMADA,
            origen=Visita.ORIGEN_MANUAL,
        )

        response = self.client.get(reverse("admin:visitas_visita_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Agenda de visitas")
        self.assertContains(response, "Horarios del dia")
        self.assertContains(response, "Detalle de la visita")
        self.assertContains(response, visita.nombre)
        self.assertContains(response, visita.telefono)

    def test_changelist_list_mode_remains_available(self):
        today = timezone.localdate()
        visita = Visita.objects.create(
            nombre="Maria Gomez",
            dni="87654321",
            telefono="2215559876",
            cantidad_personas=1,
            fecha_evento=today + timedelta(days=10),
            fecha_visita=today,
            hora_visita="18:00",
            estado=Visita.ESTADO_CONFIRMADA,
            origen=Visita.ORIGEN_WEB,
        )

        response = self.client.get(
            reverse("admin:visitas_visita_changelist"),
            {"vista": "lista"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ver agenda")
        self.assertContains(response, "Listado completo de visitas")
        self.assertContains(response, visita.nombre)

    def test_admin_index_exposes_shortcuts(self):
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Abrir agenda")
        self.assertContains(response, reverse("admin:catalogo_traje_add"))
