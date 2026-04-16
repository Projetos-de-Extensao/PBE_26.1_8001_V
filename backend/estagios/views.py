from django.shortcuts import render
from django.http import HttpResponse
from .models import Aluno

def home(request):
    alunos = Aluno.objects.all()
    lista_alunos = "<br>".join([str(a) for a in alunos])
    return HttpResponse(f"<h1>Sistema de Estágios - Ibmec</h1><p>Alunos cadastrados:</p>{lista_alunos or 'Nenhum aluno cadastrado.'}")
