# pyrefly: ignore [missing-import]
from rest_framework import serializers
from .models import (
    Aluno, Coordenador, OrganizacaoParceira, Solicitacao, Documento,
    Analise, Checklist, ItemChecklist, ModeloDocumento, Notificacao,
    AssinaturaDigital, Encaminhamento, Usuario,
)


class ObservacaoSerializer(serializers.Serializer):
    observacoes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Observações opcionais."
    )



class AlunoSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(
        write_only=True,
        help_text="Matrícula do usuário já cadastrado no sistema."
    )
    matricula_display = serializers.CharField(
        source='usuario.matricula', read_only=True
    )
    usuario_username = serializers.CharField(
        source='usuario.username', read_only=True
    )

    class Meta:
        model = Aluno
        fields = [
            'id', 'matricula', 'matricula_display', 'usuario_username',
            'nome', 'curso', 'campus', 'data_cadastro', 'usuario',
        ]
        read_only_fields = ['usuario', 'data_cadastro']

    def validate_matricula(self, value):
        try:
            usuario = Usuario.objects.get(matricula=value)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError(
                f"Nenhum usuário encontrado com a matrícula '{value}'. "
                "Certifique-se de que o usuário já foi cadastrado no painel Admin com essa matrícula."
            )
        return value

    def create(self, validated_data):
        matricula = validated_data.pop('matricula')
        usuario = Usuario.objects.get(matricula=matricula)
        validated_data['usuario'] = usuario
        return super().create(validated_data)

    def update(self, instance, validated_data):
        matricula = validated_data.pop('matricula', None)
        if matricula:
            usuario = Usuario.objects.get(matricula=matricula)
            validated_data['usuario'] = usuario
        return super().update(instance, validated_data)


class CoordenadorSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(
        write_only=True,
        help_text="Matrícula/Identificador do usuário já cadastrado no sistema."
    )
    matricula_display = serializers.CharField(
        source='usuario.matricula', read_only=True
    )
    usuario_username = serializers.CharField(
        source='usuario.username', read_only=True
    )

    class Meta:
        model = Coordenador
        fields = [
            'id', 'matricula', 'matricula_display', 'usuario_username',
            'nome', 'setor', 'usuario',
        ]
        read_only_fields = ['usuario']

    def validate_matricula(self, value):
        try:
            usuario = Usuario.objects.get(matricula=value)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError(
                f"Nenhum usuário encontrado com o identificador '{value}'. "
                "Certifique-se de que o usuário já foi cadastrado no painel Admin."
            )
        return value

    def create(self, validated_data):
        matricula = validated_data.pop('matricula')
        usuario = Usuario.objects.get(matricula=matricula)
        validated_data['usuario'] = usuario
        return super().create(validated_data)

    def update(self, instance, validated_data):
        matricula = validated_data.pop('matricula', None)
        if matricula:
            usuario = Usuario.objects.get(matricula=matricula)
            validated_data['usuario'] = usuario
        return super().update(instance, validated_data)


class OrganizacaoParceiraSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(
        write_only=True,
        help_text="Matrícula/CNPJ/Identificador do usuário já cadastrado no sistema."
    )
    matricula_display = serializers.CharField(
        source='usuario.matricula', read_only=True
    )
    usuario_username = serializers.CharField(
        source='usuario.username', read_only=True
    )

    class Meta:
        model = OrganizacaoParceira
        fields = [
            'id', 'matricula', 'matricula_display', 'usuario_username',
            'razao_social', 'cnpj', 'usuario',
        ]
        read_only_fields = ['usuario']

    def validate_matricula(self, value):
        try:
            usuario = Usuario.objects.get(matricula=value)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError(
                f"Nenhum usuário encontrado com o identificador '{value}'. "
                "Certifique-se de que o usuário já foi cadastrado no painel Admin."
            )
        return value

    def create(self, validated_data):
        matricula = validated_data.pop('matricula')
        usuario = Usuario.objects.get(matricula=matricula)
        validated_data['usuario'] = usuario
        return super().create(validated_data)

    def update(self, instance, validated_data):
        matricula = validated_data.pop('matricula', None)
        if matricula:
            usuario = Usuario.objects.get(matricula=matricula)
            validated_data['usuario'] = usuario
        return super().update(instance, validated_data)


class ModeloDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloDocumento
        fields = '__all__'
        read_only_fields = ['data_criacao', 'data_atualizacao']


class ItemChecklistSerializer(serializers.ModelSerializer):
    modelo_documento_nome = serializers.CharField(
        source='modelo_documento.nome', read_only=True
    )

    class Meta:
        model = ItemChecklist
        fields = '__all__'
        read_only_fields = ['checklist']


class ChecklistSerializer(serializers.ModelSerializer):
    itens = ItemChecklistSerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = '__all__'
        read_only_fields = ['data_criacao', 'data_atualizacao']


class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
        read_only_fields = ['status_validacao', 'data_envio']


class AnaliseSerializer(serializers.ModelSerializer):
    coordenador_nome = serializers.CharField(
        source='coordenador.nome', read_only=True
    )

    class Meta:
        model = Analise
        fields = '__all__'
        read_only_fields = ['data_analise']


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = '__all__'
        read_only_fields = ['data_criacao']


class AssinaturaDigitalSerializer(serializers.ModelSerializer):
    assinante_username = serializers.CharField(
        source='assinante.username', read_only=True
    )

    class Meta:
        model = AssinaturaDigital
        fields = '__all__'
        read_only_fields = ['data_assinatura', 'hash_assinatura', 'assinante']


class EncaminhamentoSerializer(serializers.ModelSerializer):
    organizacao_nome = serializers.CharField(
        source='organizacao.razao_social', read_only=True
    )
    coordenador_nome = serializers.CharField(
        source='coordenador.nome', read_only=True
    )

    class Meta:
        model = Encaminhamento
        fields = '__all__'
        read_only_fields = ['data_encaminhamento']


class SolicitacaoSerializer(serializers.ModelSerializer):
    documentos = DocumentoSerializer(many=True, read_only=True)
    analise = AnaliseSerializer(read_only=True)
    checklist = ChecklistSerializer(read_only=True)
    encaminhamentos = EncaminhamentoSerializer(many=True, read_only=True)
    notificacoes = NotificacaoSerializer(many=True, read_only=True)

    class Meta:
        model = Solicitacao
        fields = '__all__'
        read_only_fields = ['status', 'data_criacao', 'data_atualizacao']
