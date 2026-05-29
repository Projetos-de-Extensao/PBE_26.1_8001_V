from django.db import models
from django.contrib.auth.models import User

class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20, unique=True)
    curso = models.CharField(max_length=100)
    campus = models.CharField(max_length=100, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

class Coordenador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    setor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class OrganizacaoParceira(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    razao_social = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.razao_social

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

    def __str__(self):
        return f"Solicitação #{self.id} - {self.aluno.nome}"

class Documento(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name='documentos')
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)
    arquivo = models.FileField(upload_to='documentos_estagio/')
    status_validacao = models.CharField(max_length=50, default='Pendente')
    data_envio = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"Análise Solicitação #{self.solicitacao.id} - {self.get_resultado_display()}"
