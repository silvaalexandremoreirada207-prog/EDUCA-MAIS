from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0003_perfil_pontos"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Atividade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pergunta", models.TextField()),
                ("alternativa_a", models.CharField(max_length=300)),
                ("alternativa_b", models.CharField(max_length=300)),
                ("alternativa_c", models.CharField(max_length=300)),
                ("alternativa_d", models.CharField(max_length=300)),
                (
                    "resposta_correta",
                    models.CharField(
                        choices=[
                            ("A", "Alternativa A"),
                            ("B", "Alternativa B"),
                            ("C", "Alternativa C"),
                            ("D", "Alternativa D"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "nivel",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Nível 1"), (2, "Nível 2"), (3, "Nível 3"), (4, "Nível 4"), (5, "Nível 5")]
                    ),
                ),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                (
                    "curso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="atividades",
                        to="usuarios.curso",
                    ),
                ),
            ],
            options={
                "verbose_name": "Atividade",
                "verbose_name_plural": "Atividades",
                "ordering": ["nivel", "criada_em", "id"],
            },
        ),
        migrations.CreateModel(
            name="RespostaAtividade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "opcao_escolhida",
                    models.CharField(
                        choices=[
                            ("A", "Alternativa A"),
                            ("B", "Alternativa B"),
                            ("C", "Alternativa C"),
                            ("D", "Alternativa D"),
                        ],
                        max_length=1,
                    ),
                ),
                ("correta", models.BooleanField()),
                ("pontos_recebidos", models.PositiveSmallIntegerField()),
                ("enviada_em", models.DateTimeField(auto_now_add=True)),
                (
                    "atividade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="respostas",
                        to="usuarios.atividade",
                    ),
                ),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="respostas_atividades",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Resposta de atividade",
                "verbose_name_plural": "Respostas de atividades",
                "ordering": ["enviada_em"],
            },
        ),
        migrations.AddConstraint(
            model_name="respostaatividade",
            constraint=models.UniqueConstraint(
                fields=("atividade", "aluno"),
                name="resposta_unica_por_aluno_atividade",
            ),
        ),
    ]
