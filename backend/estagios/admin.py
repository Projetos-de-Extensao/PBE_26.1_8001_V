from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    Usuario, Aluno, Coordenador, OrganizacaoParceira,
    Solicitacao, Documento, Analise,
    Checklist, ItemChecklist, ModeloDocumento,
    Notificacao, AssinaturaDigital, Encaminhamento,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'is_staff', 'is_empresa', 'matricula')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = '__all__'


@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Tela de CRIAÇÃO: define os blocos de campos desde o zero
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Tipo de Conta', {
            'fields': ('is_staff', 'is_empresa', 'matricula'),
            'description': (
                '<b>Atenção:</b> O campo Matrícula / CNPJ / Identificador é <b>obrigatório</b> para todos os usuários.<br>'
                'Ele será usado como chave para vincular este usuário via API.'
            ),
        }),
    )

    # Tela de EDIÇÃO: adiciona a seção "Informações Adicionais"
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('is_empresa', 'matricula')}),
    )

    list_display = ['username', 'email', 'is_staff', 'is_empresa', 'matricula']
    search_fields = ['username', 'email', 'matricula']


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_matricula', 'curso', 'campus', 'data_cadastro')
    search_fields = ('nome', 'usuario__matricula')

    def get_matricula(self, obj):
        return obj.usuario.matricula if obj.usuario else None
    get_matricula.short_description = 'Matrícula'
    get_matricula.admin_order_field = 'usuario__matricula'


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


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'completo', 'data_criacao', 'data_atualizacao')
    list_filter = ('completo',)
    search_fields = ('solicitacao__aluno__nome',)


@admin.register(ItemChecklist)
class ItemChecklistAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'modelo_documento', 'status', 'observacao')
    list_filter = ('status',)
    search_fields = ('modelo_documento__nome',)


@admin.register(ModeloDocumento)
class ModeloDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'obrigatorio', 'data_criacao', 'data_atualizacao')
    list_filter = ('obrigatorio',)
    search_fields = ('nome', 'descricao')


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('destinatario', 'tipo_evento', 'lida', 'data_criacao')
    list_filter = ('tipo_evento', 'lida')
    search_fields = ('destinatario__username', 'mensagem')


@admin.register(AssinaturaDigital)
class AssinaturaDigitalAdmin(admin.ModelAdmin):
    list_display = ('documento', 'assinante', 'valida', 'data_assinatura')
    list_filter = ('valida',)
    search_fields = ('assinante__username', 'documento__nome')


@admin.register(Encaminhamento)
class EncaminhamentoAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'organizacao', 'coordenador', 'data_encaminhamento')
    search_fields = ('solicitacao__aluno__nome', 'organizacao__razao_social')
