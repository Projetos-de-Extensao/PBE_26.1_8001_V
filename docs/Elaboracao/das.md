---
id: documento_de_arquitetura
title: Documento de Arquitetura de Software
---

# Documento de Arquitetura de Software (DAS)

# Sistema de Gestão e Validação de Estágios

## Introdução

### Proposta

<p align="justify">
Este documento apresenta uma visão geral da arquitetura do Sistema de Gestão e Validação de Estágios do Ibmec, utilizando diferentes visões arquiteturais para destacar aspectos relevantes da solução. Ele captura as decisões arquiteturais significativas que guiaram o desenvolvimento do sistema.
</p>

### Escopo

<p align="justify">
A aplicação tem como objetivo fornecer uma API RESTful para centralizar e automatizar o fluxo de validação de documentos de estágio, desde a criação de solicitações pelo aluno até o encaminhamento institucional pela coordenação. O sistema busca reduzir o retrabalho manual, aumentar a rastreabilidade e garantir segurança no tratamento dos dados dos alunos.
</p>

### Definições, Acrônimos e Abreviações

| Sigla | Significado |
|---|---|
| MVT | Model-View-Template — padrão arquitetural do Django |
| DRF | Django REST Framework — toolkit para APIs REST em Django |
| JWT | JSON Web Token — padrão de autenticação stateless |
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| LGPD | Lei Geral de Proteção de Dados |
| REST | Representational State Transfer |

### Visão Geral

<p align="justify">
O DAS trata-se de uma visão geral de toda a arquitetura do sistema. Neste documento são abordadas as seguintes visões:
</p>

- Caso de Uso
- Lógica
- Implementação
- Dados

---

## Representação Arquitetural

### Arquitetura Cliente-Servidor (REST API)

<p align="justify">
O sistema segue a arquitetura Cliente-Servidor, onde o backend expõe uma API RESTful que pode ser consumida por qualquer cliente (frontend web, aplicativo móvel ou ferramenta como Postman/Swagger).
</p>

**Servidor (Backend — Django + DRF):**

- **Model (Django ORM):** Responsável pela definição das entidades de domínio e persistência no banco de dados. Inclui 12 models que representam o fluxo completo de estágio.
- **Serializer (DRF):** Camada de validação e transformação de dados entre formato JSON e objetos Python. Realiza validações customizadas (ex: lookup por matrícula).
- **ViewSet (DRF):** Controladores que recebem as requisições HTTP, aplicam permissões, delegam para os serializers e executam lógica de negócio via `perform_create` e `@action`.
- **Router (DRF):** Gera automaticamente as URLs RESTful a partir dos ViewSets registrados.

```kroki-plantuml
@startuml
skinparam componentStyle rectangle

package "Cliente" {
  [Frontend / Swagger UI / Postman]
}

package "Backend (Django + DRF)" {
  [URLs / Router] --> [ViewSets]
  [ViewSets] --> [Serializers]
  [ViewSets] --> [Permissions]
  [Serializers] --> [Models]
  [Models] --> [SQLite DB]
}

[Frontend / Swagger UI / Postman] --> [URLs / Router] : HTTP/JSON
@enduml
```

---

## Objetivos de Arquitetura e Restrições

### Objetivos

- **Segurança:** Autenticação via JWT com rotação de refresh tokens. Variáveis sensíveis (`SECRET_KEY`, `DEBUG`) gerenciadas via `python-decouple`. Permissões por perfil de usuário (Aluno, Coordenador, Empresa).
- **Persistência:** Banco de dados SQLite (desenvolvimento) com Django ORM. Migrations controladas e versionadas.
- **Privacidade:** Controle de acesso baseado em perfil — aluno vê apenas suas solicitações, coordenador vê solicitações do seu setor.
- **Desempenho:** Uso de `select_related` e `prefetch_related` para otimização de queries. Paginação com `PAGE_SIZE=20`.
- **Rastreabilidade:** Campos `auto_now_add` e `auto_now` em todas as entidades. Sistema de notificações automáticas para cada evento do fluxo.

### Restrições

- **Banco de dados:** SQLite em ambiente de desenvolvimento; recomenda-se PostgreSQL para produção.
- **Assinatura digital:** Implementação interna para rastreabilidade, sem integração com provedores externos (gov.br, ICP-Brasil) nesta versão.
- **Acesso a internet:** Necessário para autenticação e consumo da API.

### Ferramentas Utilizadas

| Ferramenta | Finalidade |
|---|---|
| Python 3.x | Linguagem de programação principal |
| Django 4.2 | Framework web com ORM integrado |
| Django REST Framework 3.16 | Toolkit para construção de APIs REST |
| SimpleJWT 5.3 | Autenticação JWT |
| drf-spectacular 0.29 | Geração automática de documentação OpenAPI/Swagger |
| django-filter 24.3 | Filtros de queryset para endpoints de listagem |
| django-cors-headers 4.3 | Controle de CORS para consumo por frontends separados |
| python-decouple 3.8 | Gestão de variáveis de ambiente |
| SQLite | Banco de dados (desenvolvimento) |
| MkDocs + Material | Documentação do projeto |

---

## Visão de Caso de Uso

<p align="justify">
Os casos de uso do sistema estão documentados em detalhes no documento <a href="casos_de_uso.md">Casos de Uso</a>. O sistema suporta 13 casos de uso (FUNC1–FUNC13) distribuídos entre 3 atores: Aluno, Coordenador e Organização Parceira.
</p>

O diagrama de casos de uso pode ser consultado em [Casos de Uso](casos_de_uso.md).

---

## Visão Lógica

A estrutura lógica do sistema segue a arquitetura em camadas do Django REST Framework:

```kroki-plantuml
@startuml
skinparam packageStyle rectangle

package "Camada de Apresentação" {
  [Swagger UI / ReDoc]
  [Django Admin]
}

package "Camada de Roteamento" {
  [DefaultRouter]
  [URLs (core/urls.py)]
}

package "Camada de Controle" {
  [ViewSets (12)]
  [@actions (aprovar, reprovar, etc.)]
  [Permissions (IsAluno, IsCoordenador)]
}

package "Camada de Serialização" {
  [Serializers (12)]
  [Validações customizadas]
}

package "Camada de Domínio" {
  [Models (12 entidades)]
  [Helpers (notificações)]
}

package "Camada de Persistência" {
  [Django ORM]
  [SQLite / PostgreSQL]
}

[Swagger UI / ReDoc] --> [URLs (core/urls.py)]
[Django Admin] --> [Models (12 entidades)]
[URLs (core/urls.py)] --> [DefaultRouter]
[DefaultRouter] --> [ViewSets (12)]
[ViewSets (12)] --> [Serializers (12)]
[ViewSets (12)] --> [Permissions (IsAluno, IsCoordenador)]
[@actions (aprovar, reprovar, etc.)] --> [Helpers (notificações)]
[Serializers (12)] --> [Models (12 entidades)]
[Models (12 entidades)] --> [Django ORM]
[Django ORM] --> [SQLite / PostgreSQL]
@enduml
```

---

## Visão de Implementação

### Estrutura de Diretórios

```
backend/
├── core/                  # Configuração do projeto Django
│   ├── settings.py        # Configurações (DRF, JWT, CORS, DB)
│   ├── urls.py            # URLs principais (admin, api, swagger, JWT)
│   ├── wsgi.py
│   └── asgi.py
├── estagios/              # App principal
│   ├── models.py          # 12 entidades do domínio
│   ├── serializers.py     # Serializers com validações
│   ├── views.py           # ViewSets + @actions + perform_create
│   ├── urls.py            # Router com 12 endpoints
│   ├── permissions.py     # Permissões por perfil
│   ├── helpers.py         # Helper de notificação
│   ├── admin.py           # Admin customizado
│   ├── tests.py           # Testes unitários e de integração
│   └── migrations/
├── manage.py
├── .env                   # Variáveis de ambiente (não versionado)
└── .env.example           # Template de variáveis
```

---

## Visão de Dados

### Modelo Entidade-Relacionamento (MER)

#### Entidades e Relacionamentos

| Entidade | Relacionamentos |
|---|---|
| `Usuario` | Base para Aluno, Coordenador e OrganizacaoParceira (1:1) |
| `Aluno` | Cria Solicitações (1:N) |
| `Coordenador` | Realiza Análises (1:N), Encaminhamentos (1:N) |
| `OrganizacaoParceira` | Recebe Encaminhamentos (1:N) |
| `Solicitacao` | Possui Checklist (1:1), Documentos (1:N), Análise (1:1), Encaminhamentos (1:N), Notificações (1:N) |
| `Checklist` | Contém Itens (1:N) via ItemChecklist |
| `ItemChecklist` | Referencia ModeloDocumento (N:1) |
| `Documento` | Recebe Assinaturas (1:N) |
| `Notificacao` | Destinada a um Usuario (N:1) |

O diagrama de classes completo está disponível em [Diagrama de Classes](diagrama_de_classes.md).

---

## Qualidade

<p align="justify">
O sistema adota práticas de qualidade que incluem: testes automatizados com <code>APITestCase</code> do DRF, cobertura de fluxos de negócio (criação de solicitação, aprovação, encaminhamento), documentação automática da API via OpenAPI/Swagger, e código organizado em camadas com separação clara de responsabilidades.
</p>

---

## Referências Bibliográficas

> Django REST Framework. Disponível em https://www.django-rest-framework.org/

> Django Documentation. Disponível em https://docs.djangoproject.com/en/4.2/

> drf-spectacular Documentation. Disponível em https://drf-spectacular.readthedocs.io/

> Simple JWT Documentation. Disponível em https://django-rest-framework-simplejwt.readthedocs.io/

---

## Histórico de Versão

| Data       | Versão | Descrição | Autor(es) |
|---|---|---|---|
| 07/06/2026 | 1.0 | Preenchimento completo do DAS com arquitetura real do projeto | Equipe PBE |
