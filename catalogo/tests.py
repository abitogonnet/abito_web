from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import ConfiguracionSitio


class ConfiguracionVisitasAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="secret123",
        )
        self.client.force_login(self.user)

    def test_catalog_changelist_redirects_to_visit_settings(self):
        response = self.client.get(reverse("admin:catalogo_configuracionvisitas_changelist"))

        config = ConfiguracionSitio.objects.get()
        self.assertRedirects(
            response,
            reverse("admin:catalogo_configuracionvisitas_change", args=[config.pk]),
        )

    def test_catalog_admin_saves_visit_address(self):
        config = ConfiguracionSitio.load()
        response = self.client.post(
            reverse("admin:catalogo_configuracionvisitas_change", args=[config.pk]),
            {
                "direccion_post_reserva": "Calle 123, Gonnet",
                "mensaje_confirmacion": "Te esperamos.",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        config.refresh_from_db()
        self.assertEqual(config.direccion_post_reserva, "Calle 123, Gonnet")
