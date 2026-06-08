# Sistema de Gestão e Validação de Estágios

**Código da Disciplina**: IBM8936  
**Curso**: Projeto Back-End — Ibmec

## Sobre o Projeto

Sistema back-end (API REST) voltado para o gerenciamento e validação de documentos de estágio. Permite que estudantes realizem o envio de documentos, acompanhem o andamento das solicitações e que a coordenação analise, valide e aprove os processos de forma organizada.

### Participantes

Daniel Studart, Davi Jacob, João Paulo Dopcke, Felipe Ultramar, Gustavo Rezende

## Stack Tecnológica

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.x | Linguagem principal |
| Django | 4.2 | Framework web |
| Django REST Framework | 3.16 | API REST |
| SimpleJWT | 5.3 | Autenticação JWT |
| drf-spectacular | 0.29 | Documentação OpenAPI/Swagger |
| django-filter | 24.3 | Filtros de queryset |
| django-cors-headers | 4.3 | Controle de CORS |
| python-decouple | 3.8 | Variáveis de ambiente |
| SQLite | — | Banco de dados (desenvolvimento) |

## Pré-requisitos

- Python 3.10+
- pip

## Instalação e Setup

### 1. Clonar o repositório

```bash
git clone https://github.com/Projetos-de-Extensao/PBE_26.1_8001_V.git
cd PBE_26.1_8001_V
```

### 2. Criar e ativar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
# Copiar o template e editar
cp backend/.env.example backend/.env

# No Windows:
copy backend\.env.example backend\.env
```

Edite o arquivo `backend/.env` com uma SECRET_KEY segura para produção.

### 5. Executar migrations

```bash
cd backend
python manage.py migrate
```

### 6. Criar superusuário (para acesso ao Admin)

```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000/`.

## Endpoints Principais

| URL | Descrição |
|---|---|
| `/admin/` | Painel administrativo Django |
| `/api/docs/swagger/` | Documentação interativa Swagger UI |
| `/api/docs/redoc/` | Documentação ReDoc |
| `/api/schema/` | Schema OpenAPI (JSON) |
| `/api/token/` | Obter token JWT (POST) |
| `/api/token/refresh/` | Renovar token JWT (POST) |
| `/api/alunos/` | CRUD de alunos |
| `/api/coordenadores/` | CRUD de coordenadores |
| `/api/empresas/` | CRUD de organizações parceiras |
| `/api/solicitacoes/` | CRUD + ações de solicitações |
| `/api/documentos/` | CRUD de documentos |
| `/api/analises/` | CRUD de análises |
| `/api/checklists/` | CRUD de checklists |
| `/api/modelos-documento/` | CRUD de modelos de documento |
| `/api/notificacoes/` | Notificações do usuário |
| `/api/assinaturas/` | Assinaturas digitais |
| `/api/encaminhamentos/` | Encaminhamentos institucionais |

### Ações Especiais (Actions)

| URL | Método | Descrição |
|---|---|---|
| `/api/solicitacoes/{id}/aprovar/` | POST | Coordenador aprova solicitação |
| `/api/solicitacoes/{id}/reprovar/` | POST | Coordenador reprova solicitação |
| `/api/solicitacoes/{id}/solicitar-correcao/` | POST | Coordenador solicita correção |
| `/api/encaminhamentos/{id}/aceitar/` | POST | Empresa aceita proposta |
| `/api/encaminhamentos/{id}/recusar/` | POST | Empresa recusa proposta |

## Executar Testes

```bash
cd backend
python manage.py test estagios -v 2
```

## Documentação do Projeto

A documentação completa está disponível via MkDocs:

```bash
pip install -r requirements.txt
mkdocs serve
```

Acesse `http://localhost:8000/` para ver a documentação.

## Licença

Este projeto é desenvolvido como trabalho acadêmico para a disciplina de Projeto Back-End do Ibmec.
