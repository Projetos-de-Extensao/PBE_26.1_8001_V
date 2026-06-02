from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import (
    Aluno, Coordenador, OrganizacaoParceira, Solicitacao, Documento,
    Analise, Checklist, ModeloDocumento, Notificacao, Encaminhamento,
)


class AuthenticationTests(APITestCase):
    """Testes de autenticação — verifica que endpoints protegidos exigem login."""

    def test_acesso_sem_autenticacao_retorna_401(self):
        """Endpoints protegidos devem retornar 401 para requisições não autenticadas."""
        endpoints = [
            '/api/alunos/',
            '/api/coordenadores/',
            '/api/empresas/',
            '/api/solicitacoes/',
            '/api/documentos/',
            '/api/analises/',
            '/api/checklists/',
            '/api/modelos-documento/',
            '/api/notificacoes/',
            '/api/assinaturas/',
            '/api/encaminhamentos/',
        ]
        for url in endpoints:
            response = self.client.get(url)
            self.assertIn(
                response.status_code,
                [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
                msg=f"Endpoint {url} deveria bloquear acesso sem autenticação, "
                    f"mas retornou {response.status_code}.",
            )

    def test_obter_token_jwt(self):
        """Deve ser possível obter um par de tokens JWT com credenciais válidas."""
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_invalido_retorna_401(self):
        """Um token inválido deve ser rejeitado."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer token-invalido')
        response = self.client.get('/api/alunos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AlunoAPITests(APITestCase):
    """Testes de CRUD para o endpoint de Alunos."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='aluno01', password='senha123'
        )
        self.client.force_authenticate(user=self.user)
        self.aluno = Aluno.objects.create(
            usuario=self.user,
            nome='João Silva',
            matricula='2024001',
            curso='Ciência da Computação',
            campus='Barra da Tijuca',
        )

    def test_listar_alunos(self):
        response = self.client.get('/api/alunos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_detalhar_aluno(self):
        response = self.client.get(f'/api/alunos/{self.aluno.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['matricula'], '2024001')

    def test_filtrar_alunos_por_curso(self):
        response = self.client.get('/api/alunos/', {'curso': 'Ciência da Computação'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_buscar_alunos_por_nome(self):
        response = self.client.get('/api/alunos/', {'search': 'João'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class SolicitacaoAPITests(APITestCase):
    """Testes de CRUD para o endpoint de Solicitações."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='aluno02', password='senha123'
        )
        self.client.force_authenticate(user=self.user)
        self.aluno = Aluno.objects.create(
            usuario=self.user,
            nome='Maria Souza',
            matricula='2024002',
            curso='Engenharia de Software',
            campus='Botafogo',
        )
        self.solicitacao = Solicitacao.objects.create(
            aluno=self.aluno,
            curso='Engenharia de Software',
            campus='Botafogo',
        )

    def test_listar_solicitacoes(self):
        response = self.client.get('/api/solicitacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_detalhar_solicitacao_com_nested_data(self):
        response = self.client.get(f'/api/solicitacoes/{self.solicitacao.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que os campos nested existem na resposta
        self.assertIn('documentos', response.data)
        self.assertIn('encaminhamentos', response.data)
        self.assertIn('notificacoes', response.data)

    def test_filtrar_solicitacoes_por_status(self):
        response = self.client.get('/api/solicitacoes/', {'status': 'CRIADA'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filtrar_solicitacoes_por_curso(self):
        response = self.client.get('/api/solicitacoes/', {'curso': 'Engenharia de Software'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class CoordenadorAPITests(APITestCase):
    """Testes básicos para o endpoint de Coordenadores."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='coord01', password='senha123'
        )
        self.client.force_authenticate(user=self.user)
        self.coordenador = Coordenador.objects.create(
            usuario=self.user,
            nome='Prof. Carlos',
            setor='Computação',
        )

    def test_listar_coordenadores(self):
        response = self.client.get('/api/coordenadores/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class AnaliseAPITests(APITestCase):
    """Testes para o endpoint de Análises."""

    def setUp(self):
        self.user_aluno = User.objects.create_user(
            username='aluno03', password='senha123'
        )
        self.user_coord = User.objects.create_user(
            username='coord02', password='senha123'
        )
        self.client.force_authenticate(user=self.user_coord)

        self.aluno = Aluno.objects.create(
            usuario=self.user_aluno,
            nome='Pedro Oliveira',
            matricula='2024003',
            curso='Direito',
            campus='Centro',
        )
        self.coordenador = Coordenador.objects.create(
            usuario=self.user_coord,
            nome='Prof. Ana',
            setor='Direito',
        )
        self.solicitacao = Solicitacao.objects.create(
            aluno=self.aluno,
            curso='Direito',
            campus='Centro',
        )
        self.analise = Analise.objects.create(
            solicitacao=self.solicitacao,
            coordenador=self.coordenador,
            resultado='APROVADO',
            observacoes='Tudo em ordem.',
        )

    def test_listar_analises(self):
        response = self.client.get('/api/analises/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filtrar_analises_por_resultado(self):
        response = self.client.get('/api/analises/', {'resultado': 'APROVADO'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class NotificacaoAPITests(APITestCase):
    """Testes para o endpoint de Notificações."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='user01', password='senha123'
        )
        self.client.force_authenticate(user=self.user)
        self.notificacao = Notificacao.objects.create(
            destinatario=self.user,
            tipo_evento='SOLICITACAO_CRIADA',
            mensagem='Sua solicitação foi registrada com sucesso.',
        )

    def test_listar_notificacoes(self):
        response = self.client.get('/api/notificacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filtrar_notificacoes_nao_lidas(self):
        response = self.client.get('/api/notificacoes/', {'lida': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class ModeloDocumentoAPITests(APITestCase):
    """Testes para o endpoint de Modelos de Documentos."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='user02', password='senha123'
        )
        self.client.force_authenticate(user=self.user)
        self.modelo = ModeloDocumento.objects.create(
            nome='Termo de Compromisso',
            descricao='Modelo do termo de compromisso de estágio.',
            obrigatorio=True,
        )

    def test_listar_modelos(self):
        response = self.client.get('/api/modelos-documento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_buscar_modelo_por_nome(self):
        response = self.client.get('/api/modelos-documento/', {'search': 'Termo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class EncaminhamentoAPITests(APITestCase):
    """Testes para o endpoint de Encaminhamentos."""

    def setUp(self):
        self.user_aluno = User.objects.create_user(
            username='aluno04', password='senha123'
        )
        self.user_coord = User.objects.create_user(
            username='coord03', password='senha123'
        )
        self.user_empresa = User.objects.create_user(
            username='empresa01', password='senha123'
        )
        self.client.force_authenticate(user=self.user_coord)

        self.aluno = Aluno.objects.create(
            usuario=self.user_aluno,
            nome='Lucas Mendes',
            matricula='2024004',
            curso='Administração',
        )
        self.coordenador = Coordenador.objects.create(
            usuario=self.user_coord,
            nome='Prof. Roberto',
            setor='Administração',
        )
        self.empresa = OrganizacaoParceira.objects.create(
            usuario=self.user_empresa,
            razao_social='Tech Corp LTDA',
            cnpj='12.345.678/0001-90',
        )
        self.solicitacao = Solicitacao.objects.create(
            aluno=self.aluno,
            curso='Administração',
            campus='Barra',
        )
        self.encaminhamento = Encaminhamento.objects.create(
            solicitacao=self.solicitacao,
            organizacao=self.empresa,
            coordenador=self.coordenador,
            observacoes='Encaminhar para assinatura.',
        )

    def test_listar_encaminhamentos(self):
        response = self.client.get('/api/encaminhamentos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
