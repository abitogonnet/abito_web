from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from catalogo.image_utils import normalize_uploaded_image
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


class CatalogoImageNormalizationTests(TestCase):
    def test_normalize_uploaded_image_returns_jpeg_with_standard_extension(self):
        normalized = normalize_uploaded_image(
            self._build_uploaded_image("foto-modelo", "PNG"),
            fallback_name="traje-foto-modelo",
        )

        self.assertTrue(normalized.name.endswith(".jpg"))

        with Image.open(BytesIO(normalized.read())) as saved_image:
            self.assertEqual(saved_image.format, "JPEG")

    def _build_uploaded_image(self, file_name, image_format):
        buffer = BytesIO()
        Image.new("RGBA", (30, 30), (255, 0, 0, 160)).save(buffer, format=image_format)
        return SimpleUploadedFile(
            file_name,
            buffer.getvalue(),
            content_type=f"image/{image_format.lower()}",
        )
