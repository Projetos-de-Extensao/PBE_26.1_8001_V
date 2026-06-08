# Reanálise do App Django REST — Sistema de Gestão de Estágios (Grupo I)

**Data:** 05/06/2026  
**Versão:** 3.0 — Reanálise completa com foco em lógica de processo  
**Escopo:** `backend/estagios/` — models, serializers, views, urls, settings, tests  
**Referência de requisitos:** `docs/Elaboracao/Requisitos.md`, `docs/Elaboracao/casos_de_uso.md`, `docs/Elaboracao/diagrama_de_classes.md`  
**Modelo de avaliação:** `analise/analisereferencia.md`

---

## Evolução Comparativa (vs. segunda_analise.md — 28/05/2026)

A tabela abaixo registra o que foi corrigido e o que permanece pendente desde a análise anterior.

| Não-conformidade anterior | Status atual |
|:---|:---:|
| `SECRET_KEY` hardcoded | ✅ Resolvido — usa `python-decouple` |
| `DEBUG` e `ALLOWED_HOSTS` hardcoded | ✅ Resolvido — via variável de ambiente |
| `DEFAULT_PERMISSION_CLASSES` ausente | ✅ Resolvido — `IsAuthenticated` global |
| Paginação ausente | ✅ Resolvido — `PAGE_SIZE: 20` |
| Filtros ausentes | ✅ Resolvido — `DjangoFilterBackend` em todas as views |
| `Notificacao` não implementada | ✅ Resolvido — model + serializer + viewset completos |
| `select_related`/`prefetch_related` ausentes | ✅ Resolvido — aplicados nos querysets críticos |
| Swagger/OpenAPI ausente | ✅ Resolvido — `drf-spectacular` configurado |
| Admin não customizado | ✅ Resolvido — `admin.py` detalhado por entidade |
| `tests.py` vazio | ⚠️ Parcial — testes escritos, mas com bugs que impedem execução |
| Ações de aprovação/rejeição sem endpoint | ❌ Persiste — ausência de `@action` |
| Rotas duplicadas | ✅ Resolvido — prefixo único `/api/` |

> **Balanço:** 10 de 12 não-conformidades críticas da segunda análise foram endereçadas. A versão atual representa um salto significativo de qualidade estrutural. Os problemas que permanecem concentram-se na **lógica de processo** — o fluxo de estágio ponta a ponta ainda não está operacionalizado na API.

---

## Análise do Fluxo do Processo de Estágio (Foco Principal)

O sistema deve suportar um fluxo de 8 etapas conforme a documentação. A tabela abaixo avalia cada etapa com base no que o código atual entrega.

| # | Etapa do Processo | Ator | Esperado pela doc | Implementado | Status |
|:-:|:---|:---|:---|:---|:---:|
| 1 | Criar solicitação | Aluno | `Solicitacao` criada com `status=CRIADA` | `SolicitacaoViewSet` cria normalmente | ✅ |
| 2 | Gerar Checklist automático | Sistema | Ao criar Solicitação, o sistema associa um `Checklist` com os `ModeloDocumento` obrigatórios | Nenhum `perform_create` ou signal faz isso | ❌ |
| 3 | Consultar checklist (UC3) | Aluno | Listar documentos exigidos para a solicitação | `ChecklistViewSet` existe e filtra; mas depende de criação manual | ⚠️ |
| 4 | Download de modelos (UC4/RF06) | Aluno | `ModeloDocumento` com `arquivo_template` disponível | `ModeloDocumentoViewSet` + campo `arquivo_template` implementados | ✅ |
| 5 | Enviar documento (UC5/RF01) | Aluno | Upload de arquivo + status→`EM_VALIDACAO` automaticamente | `DocumentoViewSet` faz upload; status não muda automaticamente | ⚠️ |
| 6 | Analisar documentos (UC9/RF04) | Coordenador | Criar `Analise` com resultado; `Solicitacao.status` atualiza | Criar `Analise` via POST não altera o status da `Solicitacao` | ❌ |
| 7 | Aprovar / Reprovar / Solicitar correção (UC10/RF04) | Coordenador | Endpoint dedicado para transição de status | `status` é `read_only` no serializer; não há `@action` | ❌ |
| 8 | Notificar eventos (UC7/RF07) | Sistema | Notificação criada automaticamente em cada evento | Criação apenas manual via POST em `/api/notificacoes/` | ❌ |
| 9 | Assinatura digital (UC11/RF05) | Aluno / Coord / Empresa | Hash gerado pelo sistema, múltiplos signatários por fluxo | `hash_assinatura` é campo gravável pelo cliente | ⚠️ |
| 10 | Encaminhar institucionalmente (UC12/RF04) | Coordenador | Criar `Encaminhamento` → status→`ENCAMINHADA` | `EncaminhamentoViewSet` existe; não atualiza status | ❌ |
| 11 | Aceitar proposta de estágio (UC13) | Organização Parceira | Endpoint de aceite/recusa da empresa | Sem `@action` ou campo de aceite no `Encaminhamento` | ❌ |
| 12 | Acompanhar status (UC6) | Aluno | Consultar `Solicitacao` com status atual e histórico | `SolicitacaoViewSet` com nested data completo | ✅ |

> **Resumo do fluxo:** Das 12 etapas mapeadas, **3 estão plenamente implementadas**, **2 são parciais** e **7 estão ausentes ou quebradas**. O sistema atual é um CRUD genérico sem orquestração do processo de negócio de estágio.

---

## 1. Especificação

### 1.1 Cobertura dos Requisitos Funcionais

| Código | Descrição | Status | Evidência |
|:---|:---|:---:|:---|
| RF01 | Upload de documentos de estágio | ⚠️ Parcial | `DocumentoViewSet` + campo `arquivo` presentes; sem transição de status ao enviar |
| RF02 | Verificação de documentos obrigatórios via Checklist | ⚠️ Parcial | Modelos `Checklist`/`ItemChecklist` existem; checklist não é criado automaticamente ao abrir solicitação |
| RF03 | Visão geral de solicitações com filtragem para coordenação | ✅ Implementado | Filtros por `status`, `curso`, `campus` em `SolicitacaoViewSet` |
| RF04 | Coordenação aprova, rejeita ou solicita ajuste | ❌ Não implementado | `status` é `read_only`; nenhum `@action` para transição; `AnaliseViewSet` desconectado do status |
| RF05 | Assinatura digital | ⚠️ Parcial | `AssinaturaDigital` model + endpoint presentes; `hash_assinatura` gravável pelo cliente |
| RF06 | Modelos de documentos para download | ✅ Implementado | `ModeloDocumentoViewSet` com `arquivo_template` e CRUD completo |
| RF07 | Notificações de status e prazos | ⚠️ Parcial | Model + endpoint presentes; sem disparo automático por eventos |

### 1.2 Cobertura dos Requisitos Não Funcionais

| RNF | Status | Detalhe |
|:---|:---:|:---|
| Segurança / autenticação restrita | ✅ | `IsAuthenticated` global + JWT |
| Performance / queries otimizadas | ✅ | `select_related` e `prefetch_related` implementados |
| Usabilidade / interface responsiva | N/A | Escopo de frontend |
| Confiabilidade / rastreabilidade | ⚠️ | `auto_now_add` presente; histórico de transições de status não registrado |
| Disponibilidade / escalabilidade | ⚠️ | SQLite em uso |

### 1.3 Aderência ao Diagrama de Classes

| Elemento | Status | Observação |
|:---|:---:|:---|
| `Usuario` como `AbstractUser` customizado | ✅ | `is_empresa`, `matricula` implementados |
| `Aluno.criarSolicitacao()` | ⚠️ | Solicitação criada via API, mas sem lógica automática de checklist |
| `Aluno.enviarDocumentos()` | ⚠️ | Upload via API; transição de status ausente |
| `Coordenador.analisarDocumentos()` | ⚠️ | `Analise` criada via API; sem vínculo com status |
| `Coordenador.revisar()` — aprovar/reprovar | ❌ | Sem `@action` dedicado |
| `Notificacao` | ✅ | Implementada com 7 tipos de eventos |
| `AssinaturaDigital` | ⚠️ | Campos presentes; sem geração/verificação de hash pelo sistema |
| `Encaminhamento` | ⚠️ | Criação possível; sem atualização de status na `Solicitacao` |
| `Checklist` automático ao criar `Solicitacao` | ❌ | Nenhum signal ou `perform_create` faz essa ligação |

### 1.4 Pontuação — Especificação

| Critério | Pontuação (1–5) |
|:---|:---:|
| Cobertura de requisitos funcionais | 3 |
| Aderência ao diagrama de classes | 3 |
| Documentação de API (OpenAPI/Swagger) | 4 |
| **Média Especificação** | **3,3** |

---

## 2. Codificação

### 2.1 Pontuação por Critério

| Critério | Pontuação (1–5) | Observação |
|:---|:---:|:---|
| Estrutura e organização do projeto | 4 | Separação clara de concerns; models, serializers, views, urls, admin bem organizados |
| Uso de ViewSets e Routers | 3 | `ModelViewSet` + `DefaultRouter` corretos; sem `@action` para nenhuma regra de negócio |
| Permissões e Autenticação | 3 | JWT + `IsAuthenticated` global; sem permissões por papel (aluno ≠ coordenador ≠ empresa) |
| Serializers e Validação | 3 | Validação de `matricula` robusta; `status` corretamente `read_only`; `hash_assinatura` sem validação |
| Qualidade e Limpeza do Código | 4 | Código limpo, legível, com docstrings nas views; constantes via `choices` |
| Otimização de Queries | 4 | `select_related`/`prefetch_related` aplicados em todos os viewsets críticos |
| Testes | 2 | 9 classes de teste escritas, porém com bugs críticos que impedem execução |
| Paginação e Filtering | 4 | `PAGE_SIZE=20`, `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter` configurados |
| **Média Codificação** | **3,4** | |

### 2.2 Bugs e Problemas Técnicos

#### BUG-01 — [ALTO] Importação incorreta de modelo de usuário nos testes

**Arquivo:** `backend/estagios/tests.py`, linha 3  
**Problema:** `from django.contrib.auth.models import User` — o projeto usa `AUTH_USER_MODEL = 'estagios.Usuario'`. Usar `User` do Django padrão cria uma instância diferente e os relacionamentos de ForeignKey falham silenciosamente ou com erros de integridade.  
**Correção:**
```python
# Errado
from django.contrib.auth.models import User

# Correto
from django.contrib.auth import get_user_model
User = get_user_model()
```

#### BUG-02 — [ALTO] Campo `matricula` inexistente no model `Aluno`

**Arquivo:** `backend/estagios/tests.py` — classes `AlunoAPITests` e `SolicitacaoAPITests`  
**Problema:** `Aluno.objects.create(..., matricula='2024001', ...)` — o campo `matricula` pertence ao model `Usuario`, não a `Aluno`. O `create()` falha com `TypeError`.  
**Correção:** Criar o `Usuario` primeiro com `matricula`, depois criar o `Aluno` sem esse campo:
```python
usuario = get_user_model().objects.create_user(
    username='aluno01', password='senha123', matricula='2024001'
)
aluno = Aluno.objects.create(usuario=usuario, nome='João Silva', ...)
```

#### BUG-03 — [MÉDIO] `BLACKLIST_AFTER_ROTATION=True` sem `token_blacklist` em `INSTALLED_APPS`

**Arquivo:** `backend/core/settings.py`  
**Problema:** `SIMPLE_JWT` define `BLACKLIST_AFTER_ROTATION: True`, mas `rest_framework_simplejwt.token_blacklist` não está em `INSTALLED_APPS`. Tokens expirados não são invalidados e a rotação falha com erro na primeira tentativa de uso real em produção.  
**Correção:** Adicionar `'rest_framework_simplejwt.token_blacklist'` em `INSTALLED_APPS` e executar `python manage.py migrate`.

#### BUG-04 — [MÉDIO] `MEDIA_ROOT` e `MEDIA_URL` ausentes em `settings.py`

**Arquivo:** `backend/core/settings.py`  
**Problema:** Os models `Documento` e `ModeloDocumento` usam `FileField` e `upload_to`, mas `MEDIA_ROOT` e `MEDIA_URL` não estão configurados. Arquivos enviados não são servidos e o Django não sabe onde gravá-los de forma determinística.  
**Correção:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### BUG-05 — [ALTO] `status` da `Solicitacao` é `read_only` sem rota alternativa de escrita

**Arquivo:** `backend/estagios/serializers.py` — `SolicitacaoSerializer`  
**Problema:** `read_only_fields = ['status', 'data_criacao', 'data_atualizacao']` é correto para evitar escrita direta, mas não há nenhum `@action` nas views que permita ao coordenador mudar o status. O campo está travado sem saída.

#### BUG-06 — [MÉDIO] `hash_assinatura` gravável pelo cliente sem validação

**Arquivo:** `backend/estagios/serializers.py` — `AssinaturaDigitalSerializer`  
**Problema:** O cliente pode enviar qualquer string como `hash_assinatura`. O sistema não gera nem verifica o hash. Isso invalida completamente a proposta de assinatura digital.

### 2.3 Ausência de Orquestração de Processo (Problemas Arquiteturais)

Os problemas abaixo não são bugs pontuais — são lacunas arquiteturais que impedem o processo de estágio de funcionar como sistema integrado.

| Lacuna | Impacto | Solução recomendada |
|:---|:---|:---|
| Sem `perform_create` em `SolicitacaoViewSet` | Checklist não é criado automaticamente | Sobrescrever `perform_create` para criar `Checklist` e popular `ItemChecklist` com todos os `ModeloDocumento` obrigatórios |
| Sem `perform_create` em `DocumentoViewSet` | Status não vai para `EM_VALIDACAO` | Sobrescrever `perform_create` para atualizar `solicitacao.status` |
| Sem `perform_create` em `AnaliseViewSet` | Resultado da análise não propaga para `Solicitacao` | Sobrescrever `perform_create` para sincronizar `Analise.resultado` → `Solicitacao.status` |
| Sem `perform_create` em `EncaminhamentoViewSet` | Status não vai para `ENCAMINHADA` | Sobrescrever `perform_create` para atualizar `solicitacao.status = 'ENCAMINHADA'` |
| Sem Django signals ou hooks de notificação | Notificações nunca são disparadas automaticamente | Usar `post_save` signal ou chamar helper de notificação nos `perform_create`/`perform_update` |

### 2.4 Pontos Positivos

- Model `Usuario` estende corretamente `AbstractUser` com validação `clean()` para impedir conflito de perfis.
- Serializers de `Aluno`, `Coordenador` e `OrganizacaoParceira` fazem lookup por `matricula` com mensagem de erro clara ao usuário.
- `SolicitacaoSerializer` com dados nested completos (`documentos`, `analise`, `checklist`, `encaminhamentos`, `notificacoes`) — excelente legibilidade da resposta.
- `Admin` customizado com formulários de criação específicos e descrições de campo orientadas ao operador.
- `ROTATE_REFRESH_TOKENS=True` — boa prática de segurança (exceto pelo BUG-03).
- Filtros por `status`, `curso`, `campus` em `SolicitacaoViewSet` — atende RF03 diretamente.

---

## 3. Conformidade

### 3.1 Segurança

| Item | Status | Detalhe |
|:---|:---:|:---|
| `SECRET_KEY` via variável de ambiente | ✅ | `config('SECRET_KEY')` via `python-decouple` |
| `DEBUG` via variável de ambiente | ✅ | `config('DEBUG', default=False, cast=bool)` |
| `ALLOWED_HOSTS` via variável de ambiente | ✅ | `config('ALLOWED_HOSTS', default='localhost', cast=Csv())` |
| `DEFAULT_PERMISSION_CLASSES: IsAuthenticated` | ✅ | Todos os endpoints exigem autenticação |
| JWT com rotação de refresh token | ⚠️ | `ROTATE_REFRESH_TOKENS=True` correto; `token_blacklist` não instalado (BUG-03) |
| Sem permissões por papel | ❌ | Qualquer usuário autenticado cria `Analise`, `Encaminhamento`, `Notificacao` de qualquer aluno |
| `hash_assinatura` gravável | ❌ | Permite forja de assinatura digital |
| `MEDIA_ROOT` ausente | ❌ | Uploads de documentos não são servidos corretamente (BUG-04) |
| CORS restrito via variável de ambiente | ✅ | `CORS_ALLOWED_ORIGINS` configurável |
| `SecurityMiddleware` e `CsrfViewMiddleware` ativos | ✅ | Presentes no `MIDDLEWARE` |
| Sem `SECURE_SSL_REDIRECT` | ⚠️ | Não configurado — necessário para produção |

### 3.2 Padrões REST

| Item | Status |
|:---|:---|
| Verbos HTTP corretos via `ModelViewSet` | ✅ |
| Códigos de status HTTP (DRF padrão) | ✅ |
| Paginação em respostas de lista | ✅ |
| `@action` para transições de estado (aprovar, reprovar, encaminhar) | ❌ |
| Recursos aninhados legíveis via nested serializers | ✅ |
| Documentação OpenAPI gerada automaticamente | ✅ |

### 3.3 LGPD / Privacidade

| Item | Status | Detalhe |
|:---|:---|:---|
| Acesso a dados pessoais exige autenticação | ✅ | `IsAuthenticated` global |
| Controle de acesso por perfil (aluno vê só seus dados) | ❌ | Qualquer usuário autenticado lista dados de qualquer aluno |
| Arquivos sensíveis protegidos por autenticação | ❌ | `MEDIA_ROOT` ausente; arquivos servidos sem controle de acesso |
| `matricula` e `cnpj` como dados pessoais sensíveis | ⚠️ | Expostos na API sem restrição de perfil |

### 3.4 Deploy e Ambiente

| Item | Status |
|:---|:---|
| Variáveis de ambiente via `python-decouple` | ✅ |
| Migrations controladas e versionadas | ✅ |
| `requirements.txt` presente com versões pinadas | ✅ |
| `MEDIA_ROOT`/`MEDIA_URL` configurados | ❌ |
| `token_blacklist` em `INSTALLED_APPS` | ❌ |
| Banco de dados para produção (PostgreSQL) | ❌ — SQLite em uso |

### 3.5 Pontuação — Conformidade

| Critério | Pontuação (1–5) |
|:---|:---:|
| Segurança (configuração de ambiente) | 4 |
| Segurança (controle de acesso por papel) | 2 |
| Padrões REST | 3 |
| LGPD / Privacidade | 2 |
| Deploy / Ambiente | 3 |
| **Média Conformidade** | **2,8** |

---

## 4. Tabela Consolidada de Pontuação

| Dimensão | Critério | Pontuação (1–5) |
|:---|:---|:---:|
| **Especificação** | Cobertura de requisitos funcionais | 3 |
| **Especificação** | Aderência ao diagrama de classes | 3 |
| **Especificação** | Documentação de API (OpenAPI/Swagger) | 4 |
| | **Média Especificação** | **3,3** |
| **Codificação** | Estrutura e organização | 4 |
| **Codificação** | ViewSets e Routers | 3 |
| **Codificação** | Permissões e Autenticação | 3 |
| **Codificação** | Serializers e Validação | 3 |
| **Codificação** | Qualidade e Limpeza | 4 |
| **Codificação** | Otimização de Queries | 4 |
| **Codificação** | Testes | 2 |
| **Codificação** | Paginação e Filtering | 4 |
| | **Média Codificação** | **3,4** |
| **Conformidade** | Segurança — configuração de ambiente | 4 |
| **Conformidade** | Segurança — controle de acesso por papel | 2 |
| **Conformidade** | Padrões REST | 3 |
| **Conformidade** | LGPD / Privacidade | 2 |
| **Conformidade** | Deploy / Ambiente | 3 |
| | **Média Conformidade** | **2,8** |
| | **Média Geral** | **3,2** |

---

## 5. Lista de Não Conformidades

| # | Severidade | Descrição |
|:-:|:---|:---|
| 1 | 🔴 CRÍTICO | `@action` ausente — RF04/UC10 completamente inoperante: nenhuma rota permite aprovar, reprovar ou solicitar correção |
| 2 | 🔴 CRÍTICO | Sem permissões por papel: qualquer usuário autenticado acessa e manipula dados de qualquer outro usuário |
| 3 | 🟠 ALTO | `perform_create` em `SolicitacaoViewSet` não cria `Checklist` automaticamente — RF02/UC3 quebrado no fluxo |
| 4 | 🟠 ALTO | `perform_create` em `DocumentoViewSet` não muda status da `Solicitacao` para `EM_VALIDACAO` — UC5 incompleto |
| 5 | 🟠 ALTO | `perform_create` em `AnaliseViewSet` não propaga resultado para `Solicitacao.status` — UC9/UC10 desconectados |
| 6 | 🟠 ALTO | `perform_create` em `EncaminhamentoViewSet` não muda status para `ENCAMINHADA` — UC12 incompleto |
| 7 | 🟠 ALTO | `tests.py` usa `from django.contrib.auth.models import User` em vez de `get_user_model()` — testes falham em execução |
| 8 | 🟠 ALTO | `AlunoAPITests`/`SolicitacaoAPITests` referenciam campo `matricula` inexistente em `Aluno` — `TypeError` na execução |
| 9 | 🟡 MÉDIO | `BLACKLIST_AFTER_ROTATION=True` sem `rest_framework_simplejwt.token_blacklist` em `INSTALLED_APPS` |
| 10 | 🟡 MÉDIO | Notificações não disparadas automaticamente — ausência de Django signals ou chamadas em `perform_create` |
| 11 | 🟡 MÉDIO | `hash_assinatura` gravável pelo cliente sem geração/verificação pelo sistema |
| 12 | 🟡 MÉDIO | UC13 (Aceitar Proposta de Estágio pela Empresa) sem implementação — nenhum campo ou endpoint de aceite/recusa |
| 13 | 🟡 MÉDIO | `MEDIA_ROOT`/`MEDIA_URL` ausentes em `settings.py` — uploads de `Documento` e `ModeloDocumento` não são servidos |
| 14 | 🟢 BAIXO | Endpoints de `Analise` e `ModeloDocumento` sem restrição `IsAdminUser` ou `IsCoordenador` |
| 15 | 🟢 BAIXO | SQLite inadequado para produção com múltiplos usuários simultâneos |

---

## 6. Recomendações Práticas

### 6.1 Prioridade Máxima — Lógica de Processo (Sprint imediato)

**1. Criar `@action` de transição de status em `SolicitacaoViewSet`:**
```python
@action(detail=True, methods=['post'], url_path='aprovar')
def aprovar(self, request, pk=None):
    solicitacao = self.get_object()
    solicitacao.status = 'APROVADA'
    solicitacao.save()
    return Response({'status': 'APROVADA'})

@action(detail=True, methods=['post'], url_path='reprovar')
def reprovar(self, request, pk=None):
    solicitacao = self.get_object()
    solicitacao.status = 'REPROVADA'
    solicitacao.save()
    return Response({'status': 'REPROVADA'})

@action(detail=True, methods=['post'], url_path='solicitar-correcao')
def solicitar_correcao(self, request, pk=None):
    solicitacao = self.get_object()
    solicitacao.status = 'CORRECAO_NECESSARIA'
    solicitacao.save()
    return Response({'status': 'CORRECAO_NECESSARIA'})
```

**2. Sobrescrever `perform_create` nos viewsets críticos:**
```python
# SolicitacaoViewSet
def perform_create(self, serializer):
    solicitacao = serializer.save()
    checklist = Checklist.objects.create(solicitacao=solicitacao)
    for modelo in ModeloDocumento.objects.filter(obrigatorio=True):
        ItemChecklist.objects.create(checklist=checklist, modelo_documento=modelo)

# DocumentoViewSet
def perform_create(self, serializer):
    documento = serializer.save()
    documento.solicitacao.status = 'EM_VALIDACAO'
    documento.solicitacao.save(update_fields=['status'])

# AnaliseViewSet
def perform_create(self, serializer):
    analise = serializer.save()
    mapa_status = {
        'APROVADO': 'APROVADA',
        'REPROVADO': 'REPROVADA',
        'CORRECAO_NECESSARIA': 'CORRECAO_NECESSARIA',
    }
    novo_status = mapa_status.get(analise.resultado)
    if novo_status:
        analise.solicitacao.status = novo_status
        analise.solicitacao.save(update_fields=['status'])

# EncaminhamentoViewSet
def perform_create(self, serializer):
    encaminhamento = serializer.save()
    encaminhamento.solicitacao.status = 'ENCAMINHADA'
    encaminhamento.solicitacao.save(update_fields=['status'])
```

### 6.2 Prioridade Alta — Segurança e Testes

**3. Corrigir importação nos testes:**
```python
# tests.py — substituir linha 3
from django.contrib.auth import get_user_model
User = get_user_model()
```

**4. Corrigir criação de Aluno nos testes:**
```python
def setUp(self):
    self.user = User.objects.create_user(
        username='aluno01', password='senha123', matricula='2024001'
    )
    self.client.force_authenticate(user=self.user)
    self.aluno = Aluno.objects.create(
        usuario=self.user,
        nome='João Silva',
        curso='Ciência da Computação',
        campus='Barra da Tijuca',
    )
```

**5. Adicionar `token_blacklist` e `MEDIA_ROOT` em `settings.py`:**
```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt.token_blacklist',  # adicionar
    ...
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**6. Implementar permissões por papel:**
```python
# permissions.py (novo arquivo)
from rest_framework.permissions import BasePermission

class IsCoordenador(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'coordenador')

class IsAluno(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'aluno')
```

### 6.3 Prioridade Média — Notificações e UC13

**7. Criar helper de notificação e chamar nos `perform_create`:**
```python
def criar_notificacao(destinatario, tipo_evento, mensagem, solicitacao=None):
    Notificacao.objects.create(
        destinatario=destinatario,
        tipo_evento=tipo_evento,
        mensagem=mensagem,
        solicitacao=solicitacao,
    )
```

**8. Implementar UC13 — aceite da empresa via `@action` em `EncaminhamentoViewSet`:**
```python
@action(detail=True, methods=['post'], url_path='aceitar')
def aceitar(self, request, pk=None):
    encaminhamento = self.get_object()
    # lógica de aceite da organização parceira
    return Response({'aceito': True})
```

**9. Gerar `hash_assinatura` no servidor:**
```python
# AssinaturaDigitalViewSet
def perform_create(self, serializer):
    import hashlib, uuid
    hash_val = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    serializer.save(hash_assinatura=hash_val)
```

### 6.4 Prioridade Baixa

- Migrar para PostgreSQL para ambiente de produção.
- Adicionar `SECURE_SSL_REDIRECT = True` e `SESSION_COOKIE_SECURE = True` para produção.
- Escrever testes de integração para cada `@action` de transição de status.
- Implementar histórico de transições de status com model de log (ex: `HistoricoStatus`).

---

## 7. Arquivos Analisados

| Arquivo | Papel |
|:---|:---|
| [backend/estagios/models.py](../backend/estagios/models.py) | Definição das 14 entidades do domínio |
| [backend/estagios/serializers.py](../backend/estagios/serializers.py) | Serializers com validações customizadas |
| [backend/estagios/views.py](../backend/estagios/views.py) | 12 ViewSets com filtros e query optimization |
| [backend/estagios/urls.py](../backend/estagios/urls.py) | Roteamento via DefaultRouter |
| [backend/estagios/admin.py](../backend/estagios/admin.py) | Admin customizado por entidade |
| [backend/estagios/tests.py](../backend/estagios/tests.py) | 9 classes de teste (com bugs de importação) |
| [backend/estagios/migrations/0001_initial.py](../backend/estagios/migrations/0001_initial.py) | Migração inicial completa |
| [backend/core/settings.py](../backend/core/settings.py) | Configuração de ambiente e DRF |
| [backend/core/urls.py](../backend/core/urls.py) | URLs principais com JWT e Swagger |
| [requirements.txt](../requirements.txt) | Dependências com versões pinadas |
| [docs/Elaboracao/Requisitos.md](../docs/Elaboracao/Requisitos.md) | RF01-RF07 e RNFs de referência |
| [docs/Elaboracao/casos_de_uso.md](../docs/Elaboracao/casos_de_uso.md) | UC1-UC13 — fluxo esperado do processo |
| [docs/Elaboracao/diagrama_de_classes.md](../docs/Elaboracao/diagrama_de_classes.md) | Diagrama de classes de referência |

---


