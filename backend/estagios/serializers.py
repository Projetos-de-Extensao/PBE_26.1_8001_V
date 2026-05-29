from rest_framework import serializers
from .models import Aluno, Coordenador, OrganizacaoParceira, Solicitacao, Documento, Analise

class AlunoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Aluno
        fields = '__all__'

class CoordenadorSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Coordenador
        fields = '__all__'

class OrganizacaoParceiraSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrganizacaoParceira
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
        read_only_fields = ['status_validacao', 'data_envio']

class AnaliseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analise
        fields = '__all__'
        read_only_fields = ['data_analise']

class SolicitacaoSerializer(serializers.ModelSerializer):
    documentos = DocumentoSerializer(many=True, read_only=True)
    analise = AnaliseSerializer(read_only=True)

    class Meta:
        model = Solicitacao
        fields = '__all__'
        read_only_fields = ['status', 'data_criacao', 'data_atualizacao']
