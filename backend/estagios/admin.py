from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    Usuario, Aluno, Coordenador, OrganizacaoParceira,
    Solicitacao, Documento, Analise,
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
                'Se nenhum marcador for selecionado, o usuário será tratado como <b>Aluno</b> '
                'e a matrícula será obrigatória.<br>'
                '"Membro da equipe" e "Empresa" não podem ser marcados ao mesmo tempo.'
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
