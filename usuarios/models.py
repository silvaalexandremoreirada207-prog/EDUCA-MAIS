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
    # Pontuação acumulada do aluno (XP), armazenada no PostgreSQL.
    pontos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"


class Curso(models.Model):
    """Cursos exibidos na página principal do EDUCA+."""
    class Nivel(models.TextChoices):
        INICIANTE = "Iniciante", "Iniciante"
        INTERMEDIARIO = "Intermediário", "Intermediário"
        AVANCADO = "Avançado", "Avançado"

    # NOVA LINHA: Vincula o curso ao professor que o criou
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cursos_criados",
        null=True,
        blank=True,
        verbose_name="Criado por",
    )
    
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


class Atividade(models.Model):
    """Questão de múltipla escolha criada pelo professor para um curso."""
    class Opcao(models.TextChoices):
        A = "A", "Alternativa A"
        B = "B", "Alternativa B"
        C = "C", "Alternativa C"
        D = "D", "Alternativa D"

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="atividades",
    )
    pergunta = models.TextField()
    alternativa_a = models.CharField(max_length=300)
    alternativa_b = models.CharField(max_length=300)
    alternativa_c = models.CharField(max_length=300)
    alternativa_d = models.CharField(max_length=300)
    resposta_correta = models.CharField(max_length=1, choices=Opcao.choices)
    nivel = models.PositiveSmallIntegerField(
        choices=[(nivel, f"Nível {nivel}") for nivel in range(1, 6)],
    )
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nivel", "criada_em", "id"]
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

    def __str__(self):
        return f"Nível {self.nivel} — {self.curso.titulo}: {self.pergunta[:60]}"

    @property
    def alternativas(self):
        return [
            ("A", self.alternativa_a),
            ("B", self.alternativa_b),
            ("C", self.alternativa_c),
            ("D", self.alternativa_d),
        ]


class RespostaAtividade(models.Model):
    """Resposta única de um aluno a uma atividade, com XP concedido."""
    atividade = models.ForeignKey(
        Atividade,
        on_delete=models.CASCADE,
        related_name="respostas",
    )
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="respostas_atividades",
    )
    opcao_escolhida = models.CharField(max_length=1, choices=Atividade.Opcao.choices)
    correta = models.BooleanField()
    pontos_recebidos = models.PositiveSmallIntegerField()
    enviada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["enviada_em"]
        verbose_name = "Resposta de atividade"
        verbose_name_plural = "Respostas de atividades"
        constraints = [
            models.UniqueConstraint(
                fields=["atividade", "aluno"],
                name="resposta_unica_por_aluno_atividade",
            )
        ]

    def __str__(self):
        return f"{self.aluno} — {self.atividade} ({self.pontos_recebidos} XP)"
