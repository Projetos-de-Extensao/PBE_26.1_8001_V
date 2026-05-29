from rest_framework import viewsets
from .models import Aluno, Coordenador, OrganizacaoParceira, Solicitacao, Documento, Analise
from .serializers import (
    AlunoSerializer, CoordenadorSerializer, OrganizacaoParceiraSerializer,
    SolicitacaoSerializer, DocumentoSerializer, AnaliseSerializer
)

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class CoordenadorViewSet(viewsets.ModelViewSet):
    queryset = Coordenador.objects.all()
    serializer_class = CoordenadorSerializer

class OrganizacaoParceiraViewSet(viewsets.ModelViewSet):
    queryset = OrganizacaoParceira.objects.all()
    serializer_class = OrganizacaoParceiraSerializer

class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class AnaliseViewSet(viewsets.ModelViewSet):
    queryset = Analise.objects.all()
    serializer_class = AnaliseSerializer
