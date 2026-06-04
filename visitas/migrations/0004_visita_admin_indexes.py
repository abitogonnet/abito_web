from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visitas", "0003_visita_vio_prendas_catalogo_preferenciaambovisita"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="visita",
            index=models.Index(
                fields=["fecha_visita", "hora_visita"],
                name="visitas_fecha_hora_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="visita",
            index=models.Index(
                fields=["fecha_visita", "estado"],
                name="visitas_fecha_estado_idx",
            ),
        ),
    ]
