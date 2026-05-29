from django.contrib import admin
from .models import Aluno, Coordenador, OrganizacaoParceira, Solicitacao, Documento, Analise

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'curso', 'campus', 'data_cadastro')
    search_fields = ('nome', 'matricula')

@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'setor')
    search_fields = ('nome', 'setor')

@admin.register(OrganizacaoParceira)
class OrganizacaoParceiraAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj')
    search_fields = ('razao_social', 'cnpj')

@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'curso', 'status', 'data_criacao')
    list_filter = ('status', 'curso')
    search_fields = ('aluno__nome', 'curso')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'solicitacao', 'tipo', 'status_validacao', 'data_envio')
    list_filter = ('status_validacao', 'tipo')
    search_fields = ('nome', 'solicitacao__aluno__nome')

@admin.register(Analise)
class AnaliseAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'coordenador', 'resultado', 'data_analise')
    list_filter = ('resultado',)
    search_fields = ('solicitacao__aluno__nome', 'coordenador__nome')
