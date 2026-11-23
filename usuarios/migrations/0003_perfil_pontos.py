from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0002_curso_criador"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfil",
            name="pontos",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
