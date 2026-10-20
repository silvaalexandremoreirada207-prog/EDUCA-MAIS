from django.contrib import admin
from .models import Curso, Favorito, Matricula, Perfil


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "instrutor", "categoria", "nivel", "ativo")
    list_filter = ("categoria", "nivel", "ativo")
    search_fields = ("titulo", "instrutor", "descricao")


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo")
    list_filter = ("tipo",)
    search_fields = ("usuario__username", "usuario__email")


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "curso", "criado_em")
    search_fields = ("usuario__username", "curso__titulo")


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "curso", "progresso", "concluido", "matriculado_em")
    list_filter = ("concluido",)
    search_fields = ("aluno__username", "curso__titulo")
