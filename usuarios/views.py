from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Favorito, Matricula, Perfil


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
    return render(request, "usuarios/home.html", {"cursos": cursos})


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

    return render(request, "usuarios/aluno.html", {
        "favoritos": favoritos,
        "matriculas": matriculas,
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
        Perfil.objects.create(usuario=user, tipo=tipo)

        messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
        return redirect("login")

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
            return redirect("aluno" if tipo_escolhido == "aluno" else "professor")

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
            return render(request, "usuarios/criar_curso.html")

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