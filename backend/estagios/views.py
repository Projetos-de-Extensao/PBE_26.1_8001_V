import hashlib
import uuid

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

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
    ObservacaoSerializer,
)
from .helpers import criar_notificacao
from .permissions import IsAluno, IsCoordenador, IsEmpresa, IsCoordenadorOrReadOnly, IsOwnerOrCoordenador


class AlunoViewSet(viewsets.ModelViewSet):
    """CRUD de alunos."""
    queryset = Aluno.objects.select_related('usuario').all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordenadorOrReadOnly]
    filterset_fields = ['curso', 'campus']
    search_fields = ['nome', 'usuario__matricula', 'curso']
    ordering_fields = ['nome', 'data_cadastro']


class CoordenadorViewSet(viewsets.ModelViewSet):
    """CRUD de coordenadores."""
    queryset = Coordenador.objects.select_related('usuario').all()
    serializer_class = CoordenadorSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordenadorOrReadOnly]
    filterset_fields = ['setor']
    search_fields = ['nome', 'setor']


class OrganizacaoParceiraViewSet(viewsets.ModelViewSet):
    """CRUD de organizações parceiras."""
    queryset = OrganizacaoParceira.objects.select_related('usuario').all()
    serializer_class = OrganizacaoParceiraSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordenadorOrReadOnly]
    filterset_fields = ['cnpj']
    search_fields = ['razao_social', 'cnpj']


class ModeloDocumentoViewSet(viewsets.ModelViewSet):
    """CRUD de modelos/templates de documentos."""
    queryset = ModeloDocumento.objects.all()
    serializer_class = ModeloDocumentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordenadorOrReadOnly]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_criacao']


class SolicitacaoViewSet(viewsets.ModelViewSet):
    """CRUD de solicitações de estágio com nested data."""
    serializer_class = SolicitacaoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCoordenador]
    filterset_fields = ['status', 'curso', 'campus']
    search_fields = ['aluno__nome', 'aluno__matricula', 'curso']
    ordering_fields = ['data_criacao', 'data_atualizacao', 'status']

    def get_queryset(self):
        qs = (
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
        user = self.request.user
        if hasattr(user, 'aluno'):
            return qs.filter(aluno=user.aluno)
        return qs

    def perform_create(self, serializer):
        """NC#3: Ao criar Solicitação, gera Checklist + Itens + Notificação."""
        solicitacao = serializer.save()

        checklist = Checklist.objects.create(solicitacao=solicitacao)
        modelos_obrigatorios = ModeloDocumento.objects.filter(obrigatorio=True)
        for modelo in modelos_obrigatorios:
            ItemChecklist.objects.create(
                checklist=checklist, modelo_documento=modelo
            )

        criar_notificacao(
            destinatario=solicitacao.aluno.usuario,
            tipo_evento='SOLICITACAO_CRIADA',
            mensagem=f'Sua solicitação #{solicitacao.id} foi criada com sucesso. Verifique o checklist.',
            solicitacao=solicitacao,
        )

    @extend_schema(request=ObservacaoSerializer)
    @action(detail=True, methods=['post'], url_path='aprovar', permission_classes=[permissions.IsAuthenticated, IsCoordenador])
    def aprovar(self, request, pk=None):
        solicitacao = self.get_object()
        observacoes = request.data.get('observacoes', '')
        solicitacao.status = 'APROVADA'
        solicitacao.save(update_fields=['status'])
        criar_notificacao(
            destinatario=solicitacao.aluno.usuario,
            tipo_evento='SOLICITACAO_APROVADA',
            mensagem=f'Sua solicitação #{solicitacao.id} foi APROVADA. {observacoes}',
            solicitacao=solicitacao,
        )
        return Response({'status': 'APROVADA', 'mensagem': f'Solicitação #{solicitacao.id} aprovada com sucesso.'})

    @extend_schema(request=ObservacaoSerializer)
    @action(detail=True, methods=['post'], url_path='reprovar', permission_classes=[permissions.IsAuthenticated, IsCoordenador])
    def reprovar(self, request, pk=None):
        solicitacao = self.get_object()
        observacoes = request.data.get('observacoes', '')
        solicitacao.status = 'REPROVADA'
        solicitacao.save(update_fields=['status'])
        criar_notificacao(
            destinatario=solicitacao.aluno.usuario,
            tipo_evento='SOLICITACAO_REPROVADA',
            mensagem=f'Sua solicitação #{solicitacao.id} foi REPROVADA. {observacoes}',
            solicitacao=solicitacao,
        )
        return Response({'status': 'REPROVADA', 'mensagem': f'Solicitação #{solicitacao.id} reprovada.'})

    @extend_schema(request=ObservacaoSerializer)
    @action(detail=True, methods=['post'], url_path='solicitar-correcao', permission_classes=[permissions.IsAuthenticated, IsCoordenador])
    def solicitar_correcao(self, request, pk=None):
        solicitacao = self.get_object()
        observacoes = request.data.get('observacoes', '')
        solicitacao.status = 'CORRECAO_NECESSARIA'
        solicitacao.save(update_fields=['status'])
        criar_notificacao(
            destinatario=solicitacao.aluno.usuario,
            tipo_evento='CORRECAO_SOLICITADA',
            mensagem=f'Correção necessária na solicitação #{solicitacao.id}. {observacoes}',
            solicitacao=solicitacao,
        )
        return Response({'status': 'CORRECAO_NECESSARIA', 'mensagem': f'Correção solicitada.'})


class ChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCoordenador]
    filterset_fields = ['completo']

    def get_queryset(self):
        qs = Checklist.objects.select_related('solicitacao').prefetch_related('itens__modelo_documento').all()
        user = self.request.user
        if hasattr(user, 'aluno'):
            return qs.filter(solicitacao__aluno=user.aluno)
        return qs


class ItemChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ItemChecklistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCoordenador]
    filterset_fields = ['status', 'checklist']

    def get_queryset(self):
        qs = ItemChecklist.objects.select_related('checklist', 'modelo_documento').all()
        user = self.request.user
        if hasattr(user, 'aluno'):
            return qs.filter(checklist__solicitacao__aluno=user.aluno)
        return qs


class DocumentoViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCoordenador]
    parser_classes = (MultiPartParser, FormParser) # Added this to fix swagger file upload
    filterset_fields = ['tipo', 'status_validacao', 'solicitacao']
    search_fields = ['nome', 'tipo']
    ordering_fields = ['data_envio', 'nome']

    def get_queryset(self):
        qs = Documento.objects.select_related('solicitacao').all()
        user = self.request.user
        if hasattr(user, 'aluno'):
            return qs.filter(solicitacao__aluno=user.aluno)
        return qs

    def perform_create(self, serializer):
        documento = serializer.save()
        solicitacao = documento.solicitacao

        if solicitacao.status == 'CRIADA':
            solicitacao.status = 'EM_VALIDACAO'
            solicitacao.save(update_fields=['status'])

        criar_notificacao(
            destinatario=solicitacao.aluno.usuario,
            tipo_evento='DOCUMENTO_ENVIADO',
            mensagem=f'Documento "{documento.nome}" enviado para a solicitação #{solicitacao.id}.',
            solicitacao=solicitacao,
        )


class AnaliseViewSet(viewsets.ModelViewSet):
    serializer_class = AnaliseSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordenadorOrReadOnly]
    filterset_fields = ['resultado', 'coordenador']
    ordering_fields = ['data_analise', 'resultado']

    def get_queryset(self):
        qs = Analise.objects.select_related('solicitacao', 'coordenador').all()
        user = self.request.user
        if hasattr(user, 'aluno'):
            return qs.filter(solicitacao__aluno=user.aluno)
        return qs

    def perform_create(self, serializer):
        analise = serializer.save()

        mapa_status = {
            'APROVADO': 'APROVADA',
            'REPROVADO': 'REPROVADA',
            'CORRECAO_NECESSARIA': 'CORRECAO_NECESSARIA',
        }
        novo_status = mapa_status.get(analise.resultado)
        if novo_status:
            analise.solicitacao.status = novo_status
            analise.solicitacao.save(update_fields=['status'])

        criar_notificacao(
            destinatario=analise.solicitacao.aluno.usuario,
            tipo_evento='ANALISE_CONCLUIDA',
            mensagem=f'Análise da solicitação #{analise.solicitacao.id}: {analise.get_resultado_display()}.',
            solicitacao=analise.solicitacao,
        )


class NotificacaoViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacaoSerializer
    filterset_fields = ['tipo_evento', 'lida']
    ordering_fields = ['data_criacao']

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Notificacao.objects.none()
        return Notificacao.objects.select_related('destinatario', 'solicitacao').filter(destinatario=self.request.user)


class AssinaturaDigitalViewSet(viewsets.ModelViewSet):
    serializer_class = AssinaturaDigitalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCoordenador]
    filterset_fields = ['valida', 'assinante', 'documento']
    ordering_fields = ['data_assinatura']

    def get_queryset(self):
        qs = AssinaturaDigital.objects.select_related('documento', 'assinante').all()
        user = self.request.user
        if hasattr(user, 'aluno'):
            return qs.filter(documento__solicitacao__aluno=user.aluno)
        return qs

    def perform_create(self, serializer):
        hash_val = hashlib.sha256(f'{uuid.uuid4()}-{self.request.user.id}'.encode()).hexdigest()
        serializer.save(hash_assinatura=hash_val, assinante=self.request.user)


class EncaminhamentoViewSet(viewsets.ModelViewSet):
    serializer_class = EncaminhamentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoordenadorOrReadOnly]
    filterset_fields = ['organizacao', 'coordenador', 'solicitacao']
    ordering_fields = ['data_encaminhamento']

    def get_queryset(self):
        qs = Encaminhamento.objects.select_related('solicitacao', 'organizacao', 'coordenador').all()
        user = self.request.user
        if hasattr(user, 'aluno'):
            return qs.filter(solicitacao__aluno=user.aluno)
        if hasattr(user, 'organizacaoparceira'):
            return qs.filter(organizacao=user.organizacaoparceira)
        return qs

    def perform_create(self, serializer):
        encaminhamento = serializer.save()
        solicitacao = encaminhamento.solicitacao

        solicitacao.status = 'ENCAMINHADA'
        solicitacao.save(update_fields=['status'])

        criar_notificacao(
            destinatario=solicitacao.aluno.usuario,
            tipo_evento='ENCAMINHAMENTO_REALIZADO',
            mensagem=f'Solicitação #{solicitacao.id} encaminhada para {encaminhamento.organizacao.razao_social}.',
            solicitacao=solicitacao,
        )

    @extend_schema(request=None)
    @action(detail=True, methods=['post'], url_path='aceitar', permission_classes=[permissions.IsAuthenticated, IsEmpresa])
    def aceitar(self, request, pk=None):
        encaminhamento = self.get_object()
        criar_notificacao(
            destinatario=encaminhamento.solicitacao.aluno.usuario,
            tipo_evento='SOLICITACAO_APROVADA',
            mensagem=f'A empresa {encaminhamento.organizacao.razao_social} aceitou a proposta.',
            solicitacao=encaminhamento.solicitacao,
        )
        return Response({'aceito': True, 'mensagem': 'Proposta de estágio aceita.'})

    @extend_schema(request=ObservacaoSerializer)
    @action(detail=True, methods=['post'], url_path='recusar', permission_classes=[permissions.IsAuthenticated, IsEmpresa])
    def recusar(self, request, pk=None):
        encaminhamento = self.get_object()
        observacoes = request.data.get('observacoes', '')
        criar_notificacao(
            destinatario=encaminhamento.solicitacao.aluno.usuario,
            tipo_evento='SOLICITACAO_REPROVADA',
            mensagem=f'A empresa {encaminhamento.organizacao.razao_social} recusou a proposta. {observacoes}',
            solicitacao=encaminhamento.solicitacao,
        )
        return Response({'aceito': False, 'mensagem': 'Proposta recusada.'})
