from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet, CoordenadorViewSet, OrganizacaoParceiraViewSet,
    SolicitacaoViewSet, DocumentoViewSet, AnaliseViewSet
)

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'coordenadores', CoordenadorViewSet, basename='coordenador')
router.register(r'empresas', OrganizacaoParceiraViewSet, basename='empresa')
router.register(r'solicitacoes', SolicitacaoViewSet, basename='solicitacao')
router.register(r'documentos', DocumentoViewSet, basename='documento')
router.register(r'analises', AnaliseViewSet, basename='analise')

urlpatterns = [
    path('', include(router.urls)),
]
