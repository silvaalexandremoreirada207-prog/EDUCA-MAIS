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
    Renderiza a página inicial.
    Busca apenas os cursos que estão com o status 'ativo=True'.
    """
    cursos = Curso.objects.filter(ativo=True)
    # Enviamos os cursos para o template através do dicionário 'context'
    return render(request, "usuarios/home.html", {"cursos": cursos})


@login_required
def aluno(request):
    """
    Área do aluno. Exige que o usuário esteja logado.
    Busca os favoritos e as matrículas específicas deste aluno.
    O 'select_related' é uma otimização que evita consultas lentas ao banco.
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
    Área do professor. Exige login.
    Aqui enviamos todos os cursos que ele criou para que ele possa gerenciar.
    """
    # (Opcional) Você pode filtrar apenas os cursos deste professor, se houver um campo para isso
    cursos_professor = Curso.objects.all() 
    return render(request, "usuarios/professor.html", {"cursos": cursos_professor})


# ==========================================
# 2. VIEWS DE AUTENTICAÇÃO (LOGIN/CADASTRO)
# ==========================================

def cadastrar_usuario(request):
    """
    Lida com a criação de novos usuários (Alunos e Professores).
    """
    if request.method == "POST":
        # Pega os dados enviados pelo formulário HTML (os 'name' dos inputs)
        username = request.POST.get("username")
        password = request.POST.get("password")
        tipo = request.POST.get("tipo") # 'aluno' ou 'professor'
        
        # Validação: Verifica se o nome de usuário já existe no banco
        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está em uso. Tente outro.")
            return render(request, "usuarios/cadastro.html")
            
        # Cria o usuário no sistema de autenticação do Django (a senha é criptografada automaticamente)
        user = User.objects.create_user(username=username, password=password)
        
        # Cria o perfil associado ao usuário (pois criamos o modelo Perfil)
        Perfil.objects.create(usuario=user, tipo=tipo)
        
        messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
        return redirect("login") # Redireciona para a página de login
        
    # Se a requisição for GET (apenas acessar a página), mostra o formulário
    return render(request, "usuarios/cadastro.html")


def fazer_login(request):
    """
    Autentica o usuário e redireciona para a tela correta dependendo do perfil.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Verifica se o usuário e senha existem e estão corretos
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) # Efetua o login no sistema
            
            # Verifica o tipo de usuário para mandar para a tela certa
            # O hasattr previne erro se o usuário não tiver perfil criado
            if hasattr(user, 'perfil') and user.perfil.tipo == "professor":
                return redirect("professor")
            return redirect("aluno")
        else:
            # Se a senha ou usuário estiverem errados, avisa o front-end
            messages.error(request, "Usuário ou senha inválidos.")
            
    return render(request, "usuarios/login.html")


def fazer_logout(request):
    """
    Desloga o usuário e o manda de volta para a página inicial.
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
    """
    # Busca o curso pelo ID. Se não existir, mostra erro 404.
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Tenta encontrar se esse curso já está favoritado por este usuário
    favorito = Favorito.objects.filter(usuario=request.user, curso=curso).first()
    
    if favorito:
        favorito.delete() # Se já estava favoritado, remove
        messages.success(request, "Curso removido dos favoritos.")
    else:
        Favorito.objects.create(usuario=request.user, curso=curso) # Se não, adiciona
        messages.success(request, "Curso adicionado aos favoritos!")
        
    # Redireciona o usuário de volta para a página onde ele clicou
    # HTTP_REFERER pega a URL anterior. Se não achar, vai para a home.
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def matricular_curso(request, curso_id):
    """
    Inscreve o aluno em um curso.
    """
    curso = get_object_or_404(Curso, id=curso_id)
    
    # get_or_create evita que o aluno se matricule duas vezes no mesmo curso
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
    """
    # Segurança: Verifica se é professor. Se não for, expulsa para a home.
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != "professor":
        messages.error(request, "Apenas professores podem criar cursos.")
        return redirect("home") 

    if request.method == "POST":
        # Recebendo os dados do formulário
        titulo = request.POST.get("titulo")
        instrutor = request.POST.get("instrutor")
        categoria = request.POST.get("categoria")
        link = request.POST.get("link")
        descricao = request.POST.get("descricao")
        
        # Cria o curso no banco de dados
        Curso.objects.create(
            titulo=titulo, 
            instrutor=instrutor, 
            categoria=categoria, 
            link=link, 
            descricao=descricao
        )
        messages.success(request, "Curso criado com sucesso!")
        return redirect("professor") # Volta para o painel do professor
        
    # Se for GET, mostra o formulário de criação
    return render(request, "usuarios/criar_curso.html")