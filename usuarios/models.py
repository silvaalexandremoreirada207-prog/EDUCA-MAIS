from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """
    Informações adicionais do usuário e seu tipo de acesso.
    O nome, e-mail e senha ficam no sistema de autenticação do Django.
    """
    class TipoUsuario(models.TextChoices):
        ALUNO = "aluno", "Aluno"
        PROFESSOR = "professor", "Professor"

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    tipo = models.CharField(
        max_length=15,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ALUNO,
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"


class Curso(models.Model):
    """Cursos exibidos na página principal do EDUCA+."""
    class Nivel(models.TextChoices):
        INICIANTE = "Iniciante", "Iniciante"
        INTERMEDIARIO = "Intermediário", "Intermediário"
        AVANCADO = "Avançado", "Avançado"

    titulo = models.CharField(max_length=200)
    instrutor = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    nivel = models.CharField(
        max_length=20,
        choices=Nivel.choices,
        default=Nivel.INICIANTE,
    )
    link = models.URLField(max_length=500)
    descricao = models.TextField()
    avaliacao = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0,
    )
    imagem = models.URLField(max_length=500, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["titulo"]
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.titulo


class Favorito(models.Model):
    """Relaciona um usuário a um curso salvo nos favoritos."""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cursos_favoritos",
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="favoritado_por",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "curso"],
                name="favorito_usuario_curso_unico",
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.curso}"


class Matricula(models.Model):
    """Registra a inscrição e o progresso de um aluno em um curso."""
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matriculas",
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="matriculas",
    )
    progresso = models.PositiveSmallIntegerField(default=0)
    concluido = models.BooleanField(default=False)
    matriculado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-matriculado_em"]
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        constraints = [
            models.UniqueConstraint(
                fields=["aluno", "curso"],
                name="matricula_aluno_curso_unica",
            )
        ]

    def __str__(self):
        return f"{self.aluno} - {self.curso} ({self.progresso}%)"
