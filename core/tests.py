from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ConfiguracionSitio


class ConfiguracionSitioAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="secret123",
        )
        self.client.force_login(self.user)

    def test_changelist_redirects_to_singleton_change_form(self):
        response = self.client.get(reverse("admin:core_configuracionsitio_changelist"))

        config = ConfiguracionSitio.objects.get()
        self.assertRedirects(
            response,
            reverse("admin:core_configuracionsitio_change", args=[config.pk]),
        )

    def test_change_form_allows_saving_visit_address(self):
        config = ConfiguracionSitio.load()
        response = self.client.post(
            reverse("admin:core_configuracionsitio_change", args=[config.pk]),
            {
                "whatsapp_url": "https://wa.me/message/IXNVRCQIC6YFF1",
                "instagram_url": "https://www.instagram.com/abito.gonnet/",
                "direccion_post_reserva": "Calle 123, Gonnet",
                "mensaje_confirmacion": "Te esperamos.",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        config.refresh_from_db()
        self.assertEqual(config.direccion_post_reserva, "Calle 123, Gonnet")
