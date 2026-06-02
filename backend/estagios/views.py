from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Aluno, Coordenador, OrganizacaoParceira, Solicitacao, Documento,
    Analise, Checklist, ItemChecklist, ModeloDocumento, Notificacao,
    AssinaturaDigital, Encaminhamento,
)
from .serializers import (
    AlunoSerializer, CoordenadorSerializer, OrganizacaoParceiraSerializer,
    SolicitacaoSerializer, DocumentoSerializer, AnaliseSerializer,
    ChecklistSerializer, ItemChecklistSerializer, ModeloDocumentoSerializer,
    NotificacaoSerializer, AssinaturaDigitalSerializer, EncaminhamentoSerializer,
)


class AlunoViewSet(viewsets.ModelViewSet):
    """CRUD de alunos."""
    queryset = Aluno.objects.select_related('usuario').all()
    serializer_class = AlunoSerializer
    filterset_fields = ['curso', 'campus']
    search_fields = ['nome', 'usuario__matricula', 'curso']
    ordering_fields = ['nome', 'data_cadastro']


class CoordenadorViewSet(viewsets.ModelViewSet):
    """CRUD de coordenadores."""
    queryset = Coordenador.objects.select_related('usuario').all()
    serializer_class = CoordenadorSerializer
    filterset_fields = ['setor']
    search_fields = ['nome', 'setor']


class OrganizacaoParceiraViewSet(viewsets.ModelViewSet):
    """CRUD de organizações parceiras."""
    queryset = OrganizacaoParceira.objects.select_related('usuario').all()
    serializer_class = OrganizacaoParceiraSerializer
    filterset_fields = ['cnpj']
    search_fields = ['razao_social', 'cnpj']


class ModeloDocumentoViewSet(viewsets.ModelViewSet):
    """CRUD de modelos/templates de documentos."""
    queryset = ModeloDocumento.objects.all()
    serializer_class = ModeloDocumentoSerializer
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_criacao']


class SolicitacaoViewSet(viewsets.ModelViewSet):
    """CRUD de solicitações de estágio com nested data."""
    serializer_class = SolicitacaoSerializer
    filterset_fields = ['status', 'curso', 'campus']
    search_fields = ['aluno__nome', 'aluno__matricula', 'curso']
    ordering_fields = ['data_criacao', 'data_atualizacao', 'status']

    def get_queryset(self):
        return (
            Solicitacao.objects
            .select_related('aluno', 'analise', 'checklist')
            .prefetch_related(
                'documentos',
                'encaminhamentos__organizacao',
                'encaminhamentos__coordenador',
                'notificacoes',
                'checklist__itens__modelo_documento',
            )
            .all()
        )


class ChecklistViewSet(viewsets.ModelViewSet):
    """CRUD de checklists."""
    serializer_class = ChecklistSerializer
    filterset_fields = ['completo']

    def get_queryset(self):
        return (
            Checklist.objects
            .select_related('solicitacao')
            .prefetch_related('itens__modelo_documento')
            .all()
        )


class ItemChecklistViewSet(viewsets.ModelViewSet):
    """CRUD de itens individuais de checklists."""
    queryset = ItemChecklist.objects.select_related(
        'checklist', 'modelo_documento'
    ).all()
    serializer_class = ItemChecklistSerializer
    filterset_fields = ['status', 'checklist']


class DocumentoViewSet(viewsets.ModelViewSet):
    """CRUD de documentos enviados."""
    queryset = Documento.objects.select_related('solicitacao').all()
    serializer_class = DocumentoSerializer
    filterset_fields = ['tipo', 'status_validacao', 'solicitacao']
    search_fields = ['nome', 'tipo']
    ordering_fields = ['data_envio', 'nome']


class AnaliseViewSet(viewsets.ModelViewSet):
    """CRUD de análises de solicitações."""
    queryset = Analise.objects.select_related(
        'solicitacao', 'coordenador'
    ).all()
    serializer_class = AnaliseSerializer
    filterset_fields = ['resultado', 'coordenador']
    ordering_fields = ['data_analise', 'resultado']


class NotificacaoViewSet(viewsets.ModelViewSet):
    """CRUD de notificações."""
    queryset = Notificacao.objects.select_related(
        'destinatario', 'solicitacao'
    ).all()
    serializer_class = NotificacaoSerializer
    filterset_fields = ['tipo_evento', 'lida', 'destinatario']
    ordering_fields = ['data_criacao']


class AssinaturaDigitalViewSet(viewsets.ModelViewSet):
    """CRUD de assinaturas digitais."""
    queryset = AssinaturaDigital.objects.select_related(
        'documento', 'assinante'
    ).all()
    serializer_class = AssinaturaDigitalSerializer
    filterset_fields = ['valida', 'assinante', 'documento']
    ordering_fields = ['data_assinatura']


class EncaminhamentoViewSet(viewsets.ModelViewSet):
    """CRUD de encaminhamentos institucionais."""
    queryset = Encaminhamento.objects.select_related(
        'solicitacao', 'organizacao', 'coordenador'
    ).all()
    serializer_class = EncaminhamentoSerializer
    filterset_fields = ['organizacao', 'coordenador', 'solicitacao']
    ordering_fields = ['data_encaminhamento']
