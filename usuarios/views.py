from django.shortcuts import render


def home(request):
    return render(request, "usuarios/home.html")


def aluno(request):
    return render(request, "usuarios/aluno.html")


def professor(request):
    return render(request, "usuarios/professor.html")
