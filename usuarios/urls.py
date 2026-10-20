from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("index.html", views.home, name="index_html"),
    path("aluno/", views.aluno, name="aluno"),
    path("aluno.html", views.aluno, name="aluno_html"),
    path("professor/", views.professor, name="professor"),
    path("professor.html", views.professor, name="professor_html"),
]
