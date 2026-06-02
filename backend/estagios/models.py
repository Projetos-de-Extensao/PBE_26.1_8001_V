from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError


class Usuario(AbstractUser):
    is_empresa = models.BooleanField(default=False, verbose_name="Empresa")
    matricula = models.CharField(max_length=20, blank=True, null=True, verbose_name="Matrícula")

    def clean(self):
        super().clean()
        if self.is_staff and self.is_empresa:
            raise ValidationError("Um usuário não pode ser simultaneamente membro da equipe e empresa.")
        
        # Considera aluno se não for staff, não for empresa e não for superuser
        if not self.is_staff and not self.is_empresa and not self.is_superuser:
            if not self.matricula:
                raise ValidationError({"matricula": "A matrícula é obrigatória para contas de alunos."})

    def __str__(self):
        return self.username


class Aluno(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    curso = models.CharField(max_length=100)
    campus = models.CharField(max_length=100, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        matricula = self.usuario.matricula if self.usuario and self.usuario.matricula else "Sem Matrícula"
        return f"{self.nome} ({matricula})"


class Coordenador(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    setor = models.CharField(max_length=100)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class OrganizacaoParceira(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    razao_social = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['razao_social']

    def __str__(self):
        return self.razao_social


class ModeloDocumento(models.Model):
    """Modelo/template para documentos exigidos no processo de estágio."""
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    arquivo_template = models.FileField(upload_to='modelos_documento/', blank=True, null=True)
    obrigatorio = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Solicitacao(models.Model):
    STATUS_CHOICES = [
        ('CRIADA', 'Criada'),
        ('EM_VALIDACAO', 'Em Validação'),
        ('CORRECAO_NECESSARIA', 'Correção Necessária'),
        ('APROVADA', 'Aprovada'),
        ('REPROVADA', 'Reprovada'),
        ('ENCAMINHADA', 'Encaminhada'),
    ]
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='solicitacoes')
    curso = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CRIADA')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Solicitação #{self.id} - {self.aluno.nome}"


class Checklist(models.Model):
    """Lista de verificação associada a uma solicitação de estágio."""
    solicitacao = models.OneToOneField(
        Solicitacao, on_delete=models.CASCADE, related_name='checklist'
    )
    modelo_documento = models.ManyToManyField(
        ModeloDocumento, through='ItemChecklist', related_name='checklists'
    )
    completo = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checklist - Solicitação #{self.solicitacao.id}"


class ItemChecklist(models.Model):
    """Item individual do checklist — liga um ModeloDocumento a um Checklist."""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ENVIADO', 'Enviado'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='itens')
    modelo_documento = models.ForeignKey(
        ModeloDocumento, on_delete=models.CASCADE, related_name='itens_checklist'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('checklist', 'modelo_documento')

    def __str__(self):
        return f"{self.modelo_documento.nome} - {self.get_status_display()}"


class Documento(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name='documentos')
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)
    arquivo = models.FileField(upload_to='documentos_estagio/')
    status_validacao = models.CharField(max_length=50, default='Pendente')
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_envio']

    def __str__(self):
        return self.nome


class Analise(models.Model):
    RESULTADO_CHOICES = [
        ('APROVADO', 'Aprovado'),
        ('REPROVADO', 'Reprovado'),
        ('CORRECAO_NECESSARIA', 'Correção Necessária'),
    ]
    solicitacao = models.OneToOneField(Solicitacao, on_delete=models.CASCADE, related_name='analise')
    coordenador = models.ForeignKey(Coordenador, on_delete=models.SET_NULL, null=True, related_name='analises')
    data_analise = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data_analise']

    def __str__(self):
        return f"Análise Solicitação #{self.solicitacao.id} - {self.get_resultado_display()}"


class Notificacao(models.Model):
    """Notificação do sistema para os usuários sobre eventos relevantes."""
    TIPO_EVENTO_CHOICES = [
        ('SOLICITACAO_CRIADA', 'Solicitação Criada'),
        ('DOCUMENTO_ENVIADO', 'Documento Enviado'),
        ('ANALISE_CONCLUIDA', 'Análise Concluída'),
        ('CORRECAO_SOLICITADA', 'Correção Solicitada'),
        ('SOLICITACAO_APROVADA', 'Solicitação Aprovada'),
        ('SOLICITACAO_REPROVADA', 'Solicitação Reprovada'),
        ('ENCAMINHAMENTO_REALIZADO', 'Encaminhamento Realizado'),
    ]
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes')
    tipo_evento = models.CharField(max_length=30, choices=TIPO_EVENTO_CHOICES)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    solicitacao = models.ForeignKey(
        Solicitacao, on_delete=models.CASCADE, related_name='notificacoes',
        blank=True, null=True
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Notificação para {self.destinatario.username} - {self.get_tipo_evento_display()}"


class AssinaturaDigital(models.Model):
    """Registro de assinatura digital associada a um documento."""
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='assinaturas')
    assinante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assinaturas')
    hash_assinatura = models.CharField(max_length=256)
    data_assinatura = models.DateTimeField(auto_now_add=True)
    valida = models.BooleanField(default=True)

    class Meta:
        ordering = ['-data_assinatura']

    def __str__(self):
        return f"Assinatura de {self.assinante.username} em {self.documento.nome}"


class Encaminhamento(models.Model):
    """Registro de encaminhamento de uma solicitação para uma organização parceira."""
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name='encaminhamentos')
    organizacao = models.ForeignKey(
        OrganizacaoParceira, on_delete=models.CASCADE, related_name='encaminhamentos'
    )
    coordenador = models.ForeignKey(
        Coordenador, on_delete=models.SET_NULL, null=True, related_name='encaminhamentos'
    )
    observacoes = models.TextField(blank=True, null=True)
    data_encaminhamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_encaminhamento']

    def __str__(self):
        return f"Encaminhamento #{self.id} - Solicitação #{self.solicitacao.id} → {self.organizacao.razao_social}"
