# CodeSpace — Ambiente de Desenvolvimento

> Instruções para configuração do ambiente de desenvolvimento do projeto.

## Pré-requisitos

| Ferramenta | Versão Mínima |
|---|---|
| Python | 3.10+ |
| pip | 22.0+ |
| Git | 2.30+ |
| Editor | VS Code (recomendado) |

## Setup do Ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/Projetos-de-Extensao/PBE_26.1_8001_V.git
cd PBE_26.1_8001_V
```

### 2. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
# Copiar template
cp backend/.env.example backend/.env    # Linux/macOS
copy backend\.env.example backend\.env  # Windows

# Editar .env com valores desejados
```

### 5. Executar migrations

```bash
cd backend
python manage.py migrate
```

### 6. Criar superusuário

```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acessar:
- **API Root:** http://localhost:8000/api/
- **Swagger:** http://localhost:8000/api/docs/swagger/
- **ReDoc:** http://localhost:8000/api/docs/redoc/
- **Admin:** http://localhost:8000/admin/

## Executar Testes

```bash
cd backend
python manage.py test estagios -v 2
```

## Estrutura do Projeto

```
PBE_26.1_8001_V/
├── backend/                 # Código-fonte Django
│   ├── core/                # Configurações do projeto
│   │   ├── settings.py      # DRF, JWT, CORS, DB
│   │   ├── urls.py          # URLs (admin, api, swagger, JWT)
│   │   └── ...
│   ├── estagios/            # App principal
│   │   ├── models.py        # 12 entidades do domínio
│   │   ├── serializers.py   # Serializers com validações
│   │   ├── views.py         # ViewSets + @actions
│   │   ├── permissions.py   # Permissões por perfil
│   │   ├── helpers.py       # Helper de notificação
│   │   ├── admin.py         # Admin customizado
│   │   ├── tests.py         # Testes automatizados
│   │   └── urls.py          # Router com 12 endpoints
│   ├── .env                 # Variáveis de ambiente (não versionado)
│   ├── .env.example         # Template de variáveis
│   └── manage.py
├── docs/                    # Documentação MkDocs
├── mkdocs.yml               # Configuração do MkDocs
├── requirements.txt         # Dependências Python
└── README.md
```

## GitHub Codespaces

O projeto pode ser desenvolvido diretamente no GitHub Codespaces, que oferece um ambiente de desenvolvimento completo no navegador. Para utilizar:

1. Acessar o repositório no GitHub
2. Clicar no botão "Code" → "Codespaces" → "Create codespace on main"
3. Aguardar o provisionamento do ambiente
4. Seguir os passos de setup acima no terminal integrado
