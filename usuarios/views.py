from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from .models import Atividade, Curso, Favorito, Matricula, Perfil, RespostaAtividade


# ==========================================
# 1. VIEWS DE NAVEGAÇÃO (PÁGINAS PRINCIPAIS)
# ==========================================

def landing(request):
    """
    Tela inicial com escolha entre Aluno e Professor.
    Se o usuário já está logado, redireciona direto pro painel dele.

    **Template:**
    :template:`usuarios/landing.html`
    """
    if request.user.is_authenticated and hasattr(request.user, "perfil"):
        if request.user.perfil.tipo == "professor":
            return redirect("professor")
        return redirect("aluno")
    return render(request, "usuarios/landing.html")


def home(request):
    """
    Lista pública de cursos ativos (pode ser usada como catálogo).
    Acessível sem login.

    **Contexto:**
    ``cursos``
        Lista de objetos :model:`usuarios.Curso` filtrados por ativo=True.

    **Template:**
    :template:`usuarios/home.html`
    """
    cursos = Curso.objects.filter(ativo=True)
    favoritos_ids = set()
    matriculas_ids = set()
    concluidos_ids = set()
    if request.user.is_authenticated and hasattr(request.user, "perfil") and request.user.perfil.tipo == "aluno":
        favoritos_ids = set(
            Favorito.objects.filter(usuario=request.user).values_list("curso_id", flat=True)
        )
        matriculas = Matricula.objects.filter(aluno=request.user)
        matriculas_ids = set(matriculas.values_list("curso_id", flat=True))
        concluidos_ids = set(
            matriculas.filter(concluido=True).values_list("curso_id", flat=True)
        )
    return render(request, "usuarios/home.html", {
        "cursos": cursos,
        "favoritos_ids": favoritos_ids,
        "matriculas_ids": matriculas_ids,
        "concluidos_ids": concluidos_ids,
    })


@login_required
def aluno(request):
    """
    Área do aluno. Exige login E perfil do tipo 'aluno'.

    **Contexto:**
    ``favoritos``
        Favoritos do aluno logado.
    ``matriculas``
        Matrículas do aluno logado.

    **Template:**
    :template:`usuarios/aluno.html`
    """
    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "aluno":
        messages.error(request, "Acesso restrito a alunos.")
        return redirect("landing")

    favoritos = Favorito.objects.filter(usuario=request.user).select_related("curso")
    matriculas = Matricula.objects.filter(aluno=request.user).select_related("curso")
    activity_folders = Curso.objects.filter(
        matriculas__aluno=request.user,
        atividades__isnull=False,
    ).annotate(
        atividades_count=Count("atividades", distinct=True),
    ).distinct()

    # Pontuação e nível do aluno conectado (200 XP por nível).
    pontos = request.user.perfil.pontos
    nivel_aluno = (pontos // 200) + 1

    return render(request, "usuarios/aluno.html", {
        "favoritos": favoritos,
        "matriculas": matriculas,
        "activity_folders": activity_folders,
        "pontos": pontos,
        "nivel_aluno": nivel_aluno,
    })


@login_required
def professor(request):
    """
    Área do professor. Exige login E perfil do tipo 'professor'.
    Mostra APENAS os cursos criados por este professor logado.

    **Contexto:**
    ``cursos``
        Lista de cursos do professor logado.

    **Template:**
    :template:`usuarios/professor.html`
    """
    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "professor":
        messages.error(request, "Acesso restrito a professores.")
        return redirect("landing")

    # Alteração de segurança: Só mostra os cursos que o próprio professor criou
    cursos = Curso.objects.filter(criador=request.user)
    return render(request, "usuarios/professor.html", {"cursos": cursos})


# ==========================================
# 2. VIEWS DE AUTENTICAÇÃO (LOGIN/CADASTRO)
# ==========================================

def cadastrar_usuario(request):
    """
    Cria novos usuários (Aluno ou Professor) + Perfil associado.
    GET: exibe o formulário.
    POST: cria User + Perfil.

    **Template:**
    :template:`usuarios/cadastro.html`
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        tipo = request.POST.get("tipo")

        # Validações básicas
        if not username or not password or tipo not in ("aluno", "professor"):
            messages.error(request, "Preencha todos os campos corretamente.")
            return render(request, "usuarios/cadastro.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está em uso. Tente outro.")
            return render(request, "usuarios/cadastro.html")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        Perfil.objects.create(usuario=user, tipo=tipo)

        messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
        return redirect("home")

    return render(request, "usuarios/cadastro.html")


def fazer_login(request):
    """
    Login único. O usuário escolhe se é Aluno ou Professor.
    Se o tipo escolhido não bater com o Perfil, bloqueia.

    **Template:**
    :template:`usuarios/login.html`
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        tipo_escolhido = request.POST.get("tipo")  # "aluno" ou "professor"

        if tipo_escolhido not in ("aluno", "professor"):
            messages.error(request, "Selecione se você é Aluno ou Professor.")
            return render(request, "usuarios/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verifica se o Perfil existe
            if not hasattr(user, "perfil"):
                messages.error(request, "Usuário sem perfil cadastrado. Contate o suporte.")
                return render(request, "usuarios/login.html")

            # Verifica se o tipo bate
            if user.perfil.tipo != tipo_escolhido:
                messages.error(
                    request,
                    f"Esta conta não é de {tipo_escolhido}. "
                    f"Ela está registrada como {user.perfil.get_tipo_display()}."
                )
                return render(request, "usuarios/login.html")

            login(request, user)
            return redirect("home" if tipo_escolhido == "aluno" else "professor")

        messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "usuarios/login.html")


def fazer_logout(request):
    """
    Desloga o usuário e redireciona para a landing.
    """
    logout(request)
    return redirect("landing")


# ==========================================
# 3. VIEWS DE AÇÕES DO ALUNO (FAVORITOS/MATRÍCULAS)
# ==========================================

@login_required
def favoritar_curso(request, curso_id):
    """
    Adiciona ou remove um curso dos favoritos (toggle).
    Só permite se o usuário for aluno.
    """
    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "aluno":
        messages.error(request, "Apenas alunos podem favoritar cursos.")
        return redirect("landing")

    curso = get_object_or_404(Curso, id=curso_id)
    favorito = Favorito.objects.filter(usuario=request.user, curso=curso).first()

    if favorito:
        favorito.delete()
        messages.success(request, "Curso removido dos favoritos.")
    else:
        Favorito.objects.create(usuario=request.user, curso=curso)
        messages.success(request, "Curso adicionado aos favoritos!")

    return redirect(request.META.get("HTTP_REFERER", "landing"))


@login_required
def matricular_curso(request, curso_id):
    """
    Inscreve o aluno em um curso (cria Matricula).
    Só permite se o usuário for aluno.
    """
    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "aluno":
        messages.error(request, "Apenas alunos podem se matricular.")
        return redirect("landing")

    curso = get_object_or_404(Curso, id=curso_id)
    matricula, created = Matricula.objects.get_or_create(aluno=request.user, curso=curso)

    if created:
        messages.success(request, f"Você se matriculou no curso: {curso.titulo}!")
    else:
        messages.warning(request, "Você já está matriculado neste curso.")

    return redirect("aluno")


@login_required
def continuar_curso(request, curso_id):
    """Registra uma etapa de estudo e depois abre a playlist do curso.

    Cada clique válido acrescenta 10% e 10 XP, até 100%. A conclusão
    concede um bônus único de 100 XP.
    """
    if request.method != "POST":
        return redirect("aluno")

    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "aluno":
        messages.error(request, "Apenas alunos podem registrar progresso.")
        return redirect("landing")

    curso = get_object_or_404(Curso, id=curso_id)
    with transaction.atomic():
        matricula = get_object_or_404(
            Matricula.objects.select_for_update(), aluno=request.user, curso=curso
        )
        perfil = Perfil.objects.select_for_update().get(usuario=request.user)

        if not matricula.concluido:
            novo_progresso = min(100, matricula.progresso + 10)
            ganho = novo_progresso - matricula.progresso
            matricula.progresso = novo_progresso
            matricula.concluido = novo_progresso >= 100
            matricula.save(update_fields=["progresso", "concluido", "atualizado_em"])
            perfil.pontos += ganho
            if matricula.concluido:
                perfil.pontos += 100
            perfil.save(update_fields=["pontos"])

    return redirect(curso.link)


# ==========================================
# 4. VIEWS DO PROFESSOR (CRUD)
# ==========================================

@login_required
def criar_curso(request):
    """
    Permite que o professor crie um novo curso.
    Apenas usuários com Perfil tipo 'professor' têm acesso.

    **Template:**
    :template:`usuarios/criar_curso.html`
    """
    if not hasattr(request.user, "perfil") or request.user.perfil.tipo != "professor":
        messages.error(request, "Apenas professores podem criar cursos.")
        return redirect("landing")

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        instrutor = request.POST.get("instrutor")
        categoria = request.POST.get("categoria")
        link = request.POST.get("link")
        descricao = request.POST.get("descricao")
        imagem = request.POST.get("imagem", "")
        nivel = request.POST.get("nivel", Curso.Nivel.INICIANTE)

        if not all([titulo, instrutor, categoria, link, descricao]):
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return render(request, "usuarios/professor.html", {
                "cursos": Curso.objects.filter(criador=request.user),
                "abrir_modal": True,
            })

        Curso.objects.create(
            titulo=titulo,
            instrutor=instrutor,
            categoria=categoria,
            link=link,
            descricao=descricao,
            imagem=imagem,
            nivel=nivel,
            criador=request.user, # Salva quem criou o curso
        )
        messages.success(request, "Curso criado com sucesso!")
        return redirect("professor")

    return render(request, "usuarios/criar_curso.html")


def _niveis_disponiveis_para_criacao(curso):
    niveis_existentes = set(
        Atividade.objects.filter(curso=curso).values_list("nivel", flat=True).distinct()
    )
    ultimo_nivel_sequencial = 0
    for nivel in range(1, 6):
        if nivel not in niveis_existentes:
            break
        ultimo_nivel_sequencial = nivel
    return list(range(1, min(5, ultimo_nivel_sequencial + 1) + 1))


def _contexto_atividades(curso, usuario, eh_professor):
    atividades = list(curso.atividades.all())
    niveis = {nivel: [] for nivel in range(1, 6)}
    nivel_liberado = {nivel: True for nivel in range(1, 6)}

    if eh_professor:
        for atividade in atividades:
            niveis[atividade.nivel].append({
                "atividade": atividade,
                "alternativas": atividade.alternativas,
            })
    else:
        respostas = {
            resposta.atividade_id: resposta
            for resposta in RespostaAtividade.objects.filter(
                aluno=usuario,
                atividade__curso=curso,
            )
        }
        totais_por_nivel = {nivel: 0 for nivel in range(1, 6)}
        respondidas_por_nivel = {nivel: 0 for nivel in range(1, 6)}
        for atividade in atividades:
            totais_por_nivel[atividade.nivel] += 1
            if atividade.id in respostas:
                respondidas_por_nivel[atividade.nivel] += 1

        for nivel_atual in range(1, 6):
            nivel_liberado[nivel_atual] = nivel_atual == 1 or all(
                respondidas_por_nivel[nivel_anterior] == totais_por_nivel[nivel_anterior]
                for nivel_anterior in range(1, nivel_atual)
            )

        for atividade in atividades:
            liberada = nivel_liberado[atividade.nivel]
            niveis[atividade.nivel].append({
                "atividade": atividade,
                "alternativas": atividade.alternativas,
                "resposta": respostas.get(atividade.id),
                "liberada": liberada,
            })

    return [
        {
            "nivel": nivel,
            "atividades": niveis[nivel],
            "liberada": nivel_liberado[nivel],
        }
        for nivel in range(1, 6)
    ]


@login_required
def atividades_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    perfil = getattr(request.user, "perfil", None)
    eh_professor = bool(
        perfil
        and perfil.tipo == "professor"
        and curso.criador_id == request.user.id
    )
    eh_aluno_matriculado = bool(
        perfil
        and perfil.tipo == "aluno"
        and Matricula.objects.filter(aluno=request.user, curso=curso).exists()
    )

    if not eh_professor and not eh_aluno_matriculado:
        messages.error(request, "Você não tem acesso às atividades deste curso.")
        return redirect("professor" if perfil and perfil.tipo == "professor" else "aluno")

    niveis_disponiveis = _niveis_disponiveis_para_criacao(curso) if eh_professor else []
    niveis_visiveis = [
        {
            "numero": nivel,
            "disponivel": nivel in niveis_disponiveis,
            "cadastrado": Atividade.objects.filter(curso=curso, nivel=nivel).exists(),
        }
        for nivel in range(1, 6)
    ] if eh_professor else []
    form_data = {}

    if request.method == "POST" and eh_professor:
        pergunta = request.POST.get("pergunta", "").strip()
        alternativas = {
            letra: request.POST.get(f"alternativa_{letra.lower()}", "").strip()
            for letra in "ABCD"
        }
        resposta_correta = request.POST.get("resposta_correta", "").upper()
        try:
            nivel = int(request.POST.get("nivel", ""))
        except (TypeError, ValueError):
            nivel = 0

        form_data = {
            "pergunta": pergunta,
            "alternativa_a": alternativas["A"],
            "alternativa_b": alternativas["B"],
            "alternativa_c": alternativas["C"],
            "alternativa_d": alternativas["D"],
            "nivel": nivel,
            "resposta_correta": resposta_correta,
        }

        if not pergunta or any(not texto for texto in alternativas.values()):
            messages.error(request, "Preencha a pergunta e as quatro alternativas.")
        elif any(len(texto) > 300 for texto in alternativas.values()):
            messages.error(request, "Cada alternativa deve ter no máximo 300 caracteres.")
        elif resposta_correta not in alternativas:
            messages.error(request, "Marque qual das quatro alternativas está correta.")
        elif nivel not in niveis_disponiveis:
            messages.error(request, "Esse nível ainda não pode ser criado. Complete a sequência dos níveis anteriores.")
        else:
            Atividade.objects.create(
                curso=curso,
                pergunta=pergunta,
                alternativa_a=alternativas["A"],
                alternativa_b=alternativas["B"],
                alternativa_c=alternativas["C"],
                alternativa_d=alternativas["D"],
                resposta_correta=resposta_correta,
                nivel=nivel,
            )
            messages.success(request, f"Atividade criada no nível {nivel}.")
            return redirect("atividades_curso", curso_id=curso.id)

    return render(request, "usuarios/atividades_curso.html", {
        "curso": curso,
        "eh_professor": eh_professor,
        "activity_groups": _contexto_atividades(curso, request.user, eh_professor),
        "has_activities": Atividade.objects.filter(curso=curso).exists(),
        "niveis_disponiveis": niveis_disponiveis,
        "niveis_visiveis": niveis_visiveis,
        "form_data": form_data,
    })


@login_required
def enviar_resposta_atividade(request, atividade_id):
    if request.method != "POST":
        return redirect("aluno")

    perfil = getattr(request.user, "perfil", None)
    if not perfil or perfil.tipo != "aluno":
        messages.error(request, "Somente alunos matriculados podem responder atividades.")
        return redirect("landing")

    atividade = get_object_or_404(Atividade.objects.select_related("curso"), id=atividade_id)
    opcao = request.POST.get("opcao", "").upper()
    if opcao not in {"A", "B", "C", "D"}:
        messages.error(request, "Selecione uma das quatro alternativas.")
        return redirect("atividades_curso", curso_id=atividade.curso_id)

    with transaction.atomic():
        matricula = get_object_or_404(
            Matricula.objects.select_for_update(),
            aluno=request.user,
            curso=atividade.curso,
        )
        if RespostaAtividade.objects.filter(atividade=atividade, aluno=request.user).exists():
            messages.warning(request, "Você já enviou sua resposta para esta atividade.")
            return redirect("atividades_curso", curso_id=atividade.curso_id)

        atividades_anteriores_pendentes = Atividade.objects.filter(
            curso=atividade.curso,
            nivel__lt=atividade.nivel,
        ).exclude(respostas__aluno=request.user)
        if atividades_anteriores_pendentes.exists():
            messages.error(request, "Envie todas as atividades dos níveis anteriores para liberar esta atividade.")
            return redirect("atividades_curso", curso_id=atividade.curso_id)

        correta = opcao == atividade.resposta_correta
        pontos_recebidos = 10 if correta else 5
        RespostaAtividade.objects.create(
            atividade=atividade,
            aluno=request.user,
            opcao_escolhida=opcao,
            correta=correta,
            pontos_recebidos=pontos_recebidos,
        )
        perfil = Perfil.objects.select_for_update().get(usuario=request.user)
        perfil.pontos += pontos_recebidos
        perfil.save(update_fields=["pontos"])

    if correta:
        messages.success(request, f"Resposta correta! Você recebeu {pontos_recebidos} XP.")
    else:
        messages.error(request, f"Resposta incorreta. Você recebeu {pontos_recebidos} XP.")
    return redirect("atividades_curso", curso_id=atividade.curso_id)
