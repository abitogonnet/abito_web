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


class VisitaPublicReservationTests(TestCase):
    def _next_weekday(self):
        day = timezone.localdate()
        while day.weekday() > 4:
            day += timedelta(days=1)
        return day

    def test_reservar_renderiza_nueva_experiencia_y_campos_compatibles(self):
        response = self.client.get(reverse("visitas:reservar"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "reserve-experience")
        self.assertContains(response, "Reserva activa")
        self.assertContains(response, 'name="cantidad_personas"', html=False)
        self.assertContains(response, 'name="fecha_evento"', html=False)
        self.assertContains(response, 'name="fecha_visita"', html=False)
        self.assertContains(response, 'name="hora_visita"', html=False)
        self.assertContains(response, 'name="vio_prendas_catalogo"', html=False)

    def test_reservar_crea_visita_web_compatible_con_panel(self):
        fecha_visita = self._next_weekday()
        fecha_evento = fecha_visita + timedelta(days=10)

        response = self.client.post(reverse("visitas:reservar"), {
            "cantidad_personas": "1",
            "fecha_evento": fecha_evento.isoformat(),
            "fecha_visita": fecha_visita.isoformat(),
            "hora_visita": "17:00",
            "vio_prendas_catalogo": "no",
            "nombre": "Juan Perez",
            "telefono": "2215551234",
            "dni": "12345678",
        })

        self.assertRedirects(response, reverse("visitas:confirmada"))

        visita = Visita.objects.get()
        self.assertEqual(visita.nombre, "Juan Perez")
        self.assertEqual(visita.telefono, "2215551234")
        self.assertEqual(visita.dni, "12345678")
        self.assertEqual(visita.cantidad_personas, 1)
        self.assertEqual(visita.fecha_evento, fecha_evento)
        self.assertEqual(visita.fecha_visita, fecha_visita)
        self.assertEqual(visita.hora_visita.strftime("%H:%M"), "17:00")
        self.assertEqual(visita.estado, Visita.ESTADO_CONFIRMADA)
        self.assertEqual(visita.origen, Visita.ORIGEN_WEB)
        self.assertFalse(visita.vio_prendas_catalogo)
