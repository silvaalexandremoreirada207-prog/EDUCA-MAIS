from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("cursos/", views.home, name="home"), # <--- ADICIONE ESTA LINHA
    path("login/", views.fazer_login, name="login"),
    path("cadastro/", views.cadastrar_usuario, name="cadastro"),
    path("logout/", views.fazer_logout, name="logout"),
    path("aluno/", views.aluno, name="aluno"),
    path("professor/", views.professor, name="professor"),
    # ações
    path("favoritar/<int:curso_id>/", views.favoritar_curso, name="favoritar_curso"),
    path("matricular/<int:curso_id>/", views.matricular_curso, name="matricular_curso"),
    path("continuar/<int:curso_id>/", views.continuar_curso, name="continuar_curso"),
    path("criar-curso/", views.criar_curso, name="criar_curso"),
]