from django.urls import path, include
# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet, CoordenadorViewSet, OrganizacaoParceiraViewSet,
    SolicitacaoViewSet, DocumentoViewSet, AnaliseViewSet,
    ChecklistViewSet, ItemChecklistViewSet, ModeloDocumentoViewSet,
    NotificacaoViewSet, AssinaturaDigitalViewSet, EncaminhamentoViewSet,
)

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'coordenadores', CoordenadorViewSet, basename='coordenador')
router.register(r'empresas', OrganizacaoParceiraViewSet, basename='empresa')
router.register(r'solicitacoes', SolicitacaoViewSet, basename='solicitacao')
router.register(r'documentos', DocumentoViewSet, basename='documento')
router.register(r'analises', AnaliseViewSet, basename='analise')
router.register(r'checklists', ChecklistViewSet, basename='checklist')
router.register(r'itens-checklist', ItemChecklistViewSet, basename='item-checklist')
router.register(r'modelos-documento', ModeloDocumentoViewSet, basename='modelo-documento')
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')
router.register(r'assinaturas', AssinaturaDigitalViewSet, basename='assinatura')
router.register(r'encaminhamentos', EncaminhamentoViewSet, basename='encaminhamento')

urlpatterns = [
    path('', include(router.urls)),
]
