import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from estagios.models import Usuario, Aluno, Coordenador, OrganizacaoParceira, ModeloDocumento

def seed():
    print("Iniciando semeadura do banco de dados...")

    # 1. Criar ou atualizar Superuser Admin
    admin_user, created = Usuario.objects.get_or_create(username='admin', defaults={'matricula': 'ADMIN01', 'is_staff': True, 'is_superuser': True})
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print(f"Superusuário 'admin' {'criado' if created else 'atualizado'} (senha: admin123).")

    # 2. Criar Aluno (usuario + perfil)
    aluno_user, created = Usuario.objects.get_or_create(username='aluno01', defaults={'matricula': '2026001'})
    aluno_user.set_password('senha123')
    aluno_user.save()
    aluno, al_created = Aluno.objects.get_or_create(usuario=aluno_user, defaults={
        'nome': 'João Aluno',
        'curso': 'Ciência da Computação',
        'campus': 'Barra da Tijuca'
    })
    print(f"Aluno 'aluno01' {'criado' if al_created else 'atualizado'} (senha: senha123).")

    # 3. Criar Coordenador (usuario + perfil)
    coord_user, created = Usuario.objects.get_or_create(username='coordenador01', defaults={'matricula': 'COORD001'})
    coord_user.set_password('senha123')
    coord_user.save()
    coord, co_created = Coordenador.objects.get_or_create(usuario=coord_user, defaults={
        'nome': 'Prof. Carlos Coordenador',
        'setor': 'Computação'
    })
    print(f"Coordenador 'coordenador01' {'criado' if co_created else 'atualizado'} (senha: senha123).")

    # 4. Criar Empresa Parceira (usuario + perfil)
    empresa_user, created = Usuario.objects.get_or_create(username='empresa01', defaults={'matricula': 'CNPJ001', 'is_empresa': True})
    empresa_user.set_password('senha123')
    empresa_user.save()
    empresa, emp_created = OrganizacaoParceira.objects.get_or_create(usuario=empresa_user, defaults={
        'razao_social': 'Empresa Parceira S/A',
        'cnpj': '12.345.678/0001-90'
    })
    print(f"Empresa 'empresa01' {'criado' if emp_created else 'atualizado'} (senha: senha123).")

    # 5. Criar Modelos de Documento
    tce, created = ModeloDocumento.objects.get_or_create(nome='Termo de Compromisso de Estágio - TCE', defaults={
        'descricao': 'Documento formalizador do estágio.',
        'obrigatorio': True
    })
    pae, created = ModeloDocumento.objects.get_or_create(nome='Plano de Atividades de Estágio - PAE', defaults={
        'descricao': 'Plano detalhado de atividades.',
        'obrigatorio': True
    })
    ficha, created = ModeloDocumento.objects.get_or_create(nome='Ficha de Avaliação de Estágio', defaults={
        'descricao': 'Ficha final de avaliação preenchida pelo supervisor.',
        'obrigatorio': False
    })
    print("Modelos de documentos criados/verificados.")
    print("Semeadura concluída com sucesso!")

if __name__ == '__main__':
    seed()
