---
id: prototipo_alta_fidelidade
title: Protótipo de Alta Fidelidade
---

# Protótipo de Alta Fidelidade

## Introdução

<p align="justify">
Por se tratar de um projeto exclusivamente back-end (API REST), o protótipo de alta fidelidade é representado pelas interfaces reais da API que os consumidores utilizam: a documentação interativa Swagger UI, o painel administrativo Django Admin e os exemplos de requisições/respostas JSON. Essas interfaces constituem a "tela" do sistema para seus usuários diretos.
</p>

---

## 1. Swagger UI — Documentação Interativa da API

A documentação Swagger UI é gerada automaticamente pelo `drf-spectacular` e está acessível em `/api/docs/swagger/`.

### Características:

- **Listagem completa dos 12 endpoints** com documentação de cada campo
- **Autenticação JWT integrada** — botão "Authorize" para inserir o token
- **Teste interativo** — permite executar requisições diretamente da interface
- **Schema OpenAPI** — contrato formal da API disponível em `/api/schema/`

### Endpoints documentados:

| Grupo | Endpoints | Ações Especiais |
|---|---|---|
| Alunos | GET, POST, PUT, PATCH, DELETE `/api/alunos/` | Filtro por curso, campus; busca por nome |
| Coordenadores | GET, POST, PUT, PATCH, DELETE `/api/coordenadores/` | Filtro por setor |
| Empresas | GET, POST, PUT, PATCH, DELETE `/api/empresas/` | Filtro por CNPJ |
| Solicitações | GET, POST, PUT, PATCH, DELETE `/api/solicitacoes/` | `aprovar/`, `reprovar/`, `solicitar-correcao/` |
| Documentos | GET, POST, PUT, PATCH, DELETE `/api/documentos/` | Upload de arquivo |
| Análises | GET, POST, PUT, PATCH, DELETE `/api/analises/` | Filtro por resultado |
| Checklists | GET, POST, PUT, PATCH, DELETE `/api/checklists/` | Filtro por completo |
| Modelos | GET, POST, PUT, PATCH, DELETE `/api/modelos-documento/` | Download de template |
| Notificações | GET, POST `/api/notificacoes/` | Filtro por tipo, lida |
| Assinaturas | GET, POST `/api/assinaturas/` | Hash gerado pelo servidor |
| Encaminhamentos | GET, POST `/api/encaminhamentos/` | `aceitar/`, `recusar/` |

---

## 2. Django Admin — Painel de Administração

O Django Admin é acessível em `/admin/` e permite a gestão direta das entidades do sistema.

### Models registrados:

| Model | Campos exibidos | Filtros |
|---|---|---|
| Usuário | username, email, is_staff, is_empresa, matricula | — |
| Aluno | nome, matrícula, curso, campus, data_cadastro | — |
| Coordenador | nome, setor | — |
| Organização Parceira | razão social, CNPJ | — |
| Solicitação | id, aluno, curso, status, data_criação | status, curso |
| Documento | nome, solicitação, tipo, status, data_envio | status, tipo |
| Análise | solicitação, coordenador, resultado, data | resultado |
| Checklist | solicitação, completo, datas | completo |
| Item Checklist | checklist, modelo, status, observação | status |
| Modelo de Documento | nome, obrigatório, datas | obrigatório |
| Notificação | destinatário, tipo_evento, lida, data | tipo, lida |
| Assinatura Digital | documento, assinante, válida, data | válida |
| Encaminhamento | solicitação, organização, coordenador, data | — |

---

## 3. Exemplos de Requisição/Resposta JSON

### 3.1 Autenticação — Obter Token JWT

**Request:**
```http
POST /api/token/
Content-Type: application/json

{
    "username": "aluno01",
    "password": "senha123"
}
```

**Response (200 OK):**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3.2 Criar Solicitação (com Checklist automático)

**Request:**
```http
POST /api/solicitacoes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "aluno": 1,
    "curso": "Ciência da Computação",
    "campus": "Barra da Tijuca"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "aluno": 1,
    "curso": "Ciência da Computação",
    "campus": "Barra da Tijuca",
    "status": "CRIADA",
    "data_criacao": "2026-06-07T18:30:00-03:00",
    "data_atualizacao": "2026-06-07T18:30:00-03:00",
    "documentos": [],
    "analise": null,
    "checklist": {
        "id": 1,
        "completo": false,
        "itens": [
            {"id": 1, "modelo_documento_nome": "TCE", "status": "PENDENTE"},
            {"id": 2, "modelo_documento_nome": "Relatório Parcial", "status": "PENDENTE"}
        ]
    },
    "encaminhamentos": [],
    "notificacoes": [
        {
            "id": 1,
            "tipo_evento": "SOLICITACAO_CRIADA",
            "mensagem": "Sua solicitação #1 foi criada com sucesso.",
            "lida": false
        }
    ]
}
```

### 3.3 Aprovar Solicitação (Coordenador)

**Request:**
```http
POST /api/solicitacoes/1/aprovar/
Authorization: Bearer <coord_access_token>
Content-Type: application/json

{
    "observacoes": "Todos os documentos conferem. Aprovado."
}
```

**Response (200 OK):**
```json
{
    "status": "APROVADA",
    "mensagem": "Solicitação #1 aprovada com sucesso."
}
```

### 3.4 Listar Solicitações com Filtros

**Request:**
```http
GET /api/solicitacoes/?status=CRIADA&curso=Engenharia
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {"id": 3, "status": "CRIADA", "curso": "Engenharia de Software", "...": "..."},
        {"id": 5, "status": "CRIADA", "curso": "Engenharia Civil", "...": "..."}
    ]
}
```

---

## Conclusão

<p align="justify">
O protótipo de alta fidelidade do sistema é composto pelas interfaces reais e operacionais da API: Swagger UI para documentação interativa e testes, Django Admin para gestão administrativa, e os contratos JSON para integração. Essas interfaces permitem que desenvolvedores, coordenadores e operadores interajam com o sistema de forma completa e funcional.
</p>

---

## Autor(es)

| Data       | Versão | Descrição                            | Autor(es)         |
|---|---|---|---|
| 07/06/2026 | 1.0    | Protótipo de alta fidelidade baseado nas interfaces reais da API | Equipe PBE |
