from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Favorito, Matricula, Perfil


# ==========================================
# 1. VIEWS DE NAVEGAÇÃO (PÁGINAS PRINCIPAIS)
# ==========================================

def home(request):
    """
    Renderiza a página inicial com a lista de cursos ativos.

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
    Área do aluno. Exige que o usuário esteja logado.
    Busca os favoritos e as matrículas específicas deste aluno.

    **Contexto:**
    ``favoritos``
        Lista de objetos :model:`usuarios.Favorito` do aluno logado.
    ``matriculas``
        Lista de objetos :model:`usuarios.Matricula` do aluno logado.

    **Template:**
    :template:`usuarios/aluno.html`
    """
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('curso')
    matriculas = Matricula.objects.filter(aluno=request.user).select_related('curso')
    
    context = {
        "favoritos": favoritos,
        "matriculas": matriculas
    }
    return render(request, "usuarios/aluno.html", context)


@login_required
def professor(request):
    """
    Área do professor. Exige login. Envia todos os cursos para gerenciamento.

    **Contexto:**
    ``cursos``
        Lista de todos os objetos :model:`usuarios.Curso`.

    **Template:**
    :template:`usuarios/professor.html`
    """
    cursos_professor = Curso.objects.all() 
    return render(request, "usuarios/professor.html", {"cursos": cursos_professor})


# ==========================================
# 2. VIEWS DE AUTENTICAÇÃO (LOGIN/CADASTRO)
# ==========================================

def cadastrar_usuario(request):
    """
    Lida com a criação de novos usuários (Alunos e Professores).
    Se o método for POST, cria o :model:`auth.User` e o :model:`usuarios.Perfil`.
    Se for GET, apenas exibe o formulário.

    **Template:**
    :template:`usuarios/cadastro.html`
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        tipo = request.POST.get("tipo")
        
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
    Autentica o usuário e redireciona para a tela correta dependendo do perfil.
    Se o usuário for professor, redireciona para a view 'professor'. Se for aluno, para 'aluno'.

    **Template:**
    :template:`usuarios/login.html`
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if hasattr(user, 'perfil') and user.perfil.tipo == "professor":
                return redirect("professor")
            return redirect("aluno")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            
    return render(request, "usuarios/login.html")


def fazer_logout(request):
    """
    Desloga o usuário e o redireciona para a página inicial ('home').
    """
    logout(request)
    return redirect("home")


# ==========================================
# 3. VIEWS DE AÇÕES DO ALUNO (FAVORITOS/MATRÍCULAS)
# ==========================================

@login_required
def favoritar_curso(request, curso_id):
    """
    Adiciona ou remove um curso dos favoritos (sistema de Toggle).
    Utiliza o modelo :model:`usuarios.Favorito`.

    **Parâmetro:**
    ``curso_id``
        O ID do objeto :model:`usuarios.Curso` a ser favoritado/desfavoritado.
    """
    curso = get_object_or_404(Curso, id=curso_id)
    favorito = Favorito.objects.filter(usuario=request.user, curso=curso).first()
    
    if favorito:
        favorito.delete() 
        messages.success(request, "Curso removido dos favoritos.")
    else:
        Favorito.objects.create(usuario=request.user, curso=curso)
        messages.success(request, "Curso adicionado aos favoritos!")
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def matricular_curso(request, curso_id):
    """
    Inscreve o aluno em um curso, criando um registro em :model:`usuarios.Matricula`.

    **Parâmetro:**
    ``curso_id``
        O ID do objeto :model:`usuarios.Curso` a ser matriculado.
    """
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
    Permite que o professor crie um novo curso, salvando um objeto :model:`usuarios.Curso`.
    Apenas usuários com Perfil do tipo 'professor' têm acesso.

    **Template:**
    :template:`usuarios/criar_curso.html`
    """
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != "professor":
        messages.error(request, "Apenas professores podem criar cursos.")
        return redirect("home") 

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        instrutor = request.POST.get("instrutor")
        categoria = request.POST.get("categoria")
        link = request.POST.get("link")
        descricao = request.POST.get("descricao")
        
        Curso.objects.create(
            titulo=titulo, 
            instrutor=instrutor, 
            categoria=categoria, 
            link=link, 
            descricao=descricao
        )
        messages.success(request, "Curso criado com sucesso!")
        return redirect("professor") 
        
    return render(request, "usuarios/criar_curso.html")