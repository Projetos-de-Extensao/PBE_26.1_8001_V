---
id: diagrama_de_sequencia
title: Diagramas de Sequência
---

# Diagramas de Sequência

## Introdução

<p align="justify">
Os diagramas de sequência representam a interação temporal entre os atores e os componentes do sistema, detalhando o fluxo de mensagens para os principais cenários de uso da API de Gestão e Validação de Estágios.
</p>

---

## 1. Autenticação JWT (FUNC1)

```kroki-plantuml
@startuml
title Autenticação via JWT

actor "Usuário" as User
participant "POST /api/token/" as Auth
participant "SimpleJWT" as JWT
database "Banco de Dados" as DB

User -> Auth : POST {username, password}
Auth -> DB : Consultar credenciais
alt Credenciais válidas
  DB --> Auth : Usuario encontrado
  Auth -> JWT : Gerar par de tokens
  JWT --> Auth : {access, refresh}
  Auth --> User : 200 OK {access, refresh}
else Credenciais inválidas
  DB --> Auth : Não encontrado
  Auth --> User : 401 Unauthorized
end

note right of User
  O token "access" deve ser enviado
  no header Authorization: Bearer <token>
  em todas as requisições seguintes.
end note
@enduml
```

---

## 2. Criação de Solicitação com Checklist Automático (FUNC2/FUNC3)

```kroki-plantuml
@startuml
title Criar Solicitação + Geração de Checklist

actor "Aluno" as Aluno
participant "SolicitacaoViewSet" as SV
participant "perform_create()" as PC
participant "Checklist" as CK
participant "ModeloDocumento" as MD
participant "Notificacao" as NT
database "Banco de Dados" as DB

Aluno -> SV : POST /api/solicitacoes/ {aluno, curso, campus}
SV -> SV : Validar serializer
SV -> PC : perform_create(serializer)
PC -> DB : Criar Solicitacao (status=CRIADA)
DB --> PC : Solicitação #N criada

PC -> CK : Criar Checklist para Solicitação #N
PC -> MD : Consultar ModeloDocumento (obrigatorio=True)
MD --> PC : [TCE, Relatório, ...]
loop Para cada modelo obrigatório
  PC -> DB : Criar ItemChecklist (status=PENDENTE)
end

PC -> NT : criar_notificacao(aluno, SOLICITACAO_CRIADA)
NT -> DB : Salvar notificação

SV --> Aluno : 201 Created {id, status: CRIADA, checklist: {...}}
@enduml
```

---

## 3. Envio de Documento com Transição de Status (FUNC5/RF01)

```kroki-plantuml
@startuml
title Envio de Documento + Atualização de Status

actor "Aluno" as Aluno
participant "DocumentoViewSet" as DV
participant "perform_create()" as PC
participant "Notificacao" as NT
database "Banco de Dados" as DB

Aluno -> DV : POST /api/documentos/ {solicitacao, nome, tipo, arquivo}
DV -> DV : Validar serializer + upload de arquivo
DV -> PC : perform_create(serializer)
PC -> DB : Salvar Documento
DB --> PC : Documento criado

PC -> DB : Atualizar Solicitacao.status = EM_VALIDACAO
PC -> NT : criar_notificacao(aluno, DOCUMENTO_ENVIADO)
NT -> DB : Salvar notificação

DV --> Aluno : 201 Created {id, nome, status_validacao: Pendente}
@enduml
```

---

## 4. Análise e Aprovação pelo Coordenador (FUNC9/FUNC10/RF04)

```kroki-plantuml
@startuml
title Fluxo de Análise e Aprovação

actor "Coordenador" as Coord
participant "SolicitacaoViewSet" as SV
participant "@action aprovar" as AP
participant "Notificacao" as NT
database "Banco de Dados" as DB

== Opção A: Via @action (recomendado) ==

Coord -> SV : POST /api/solicitacoes/{id}/aprovar/ {observacoes}
SV -> SV : Verificar permissão IsCoordenador
SV -> AP : aprovar(request, pk)
AP -> DB : Atualizar Solicitacao.status = APROVADA
AP -> NT : criar_notificacao(aluno, SOLICITACAO_APROVADA)
NT -> DB : Salvar notificação
AP --> Coord : 200 OK {status: APROVADA}

== Opção B: Reprovar ==

Coord -> SV : POST /api/solicitacoes/{id}/reprovar/ {observacoes}
SV -> AP : reprovar(request, pk)
AP -> DB : Atualizar Solicitacao.status = REPROVADA
AP -> NT : criar_notificacao(aluno, SOLICITACAO_REPROVADA)
AP --> Coord : 200 OK {status: REPROVADA}

== Opção C: Solicitar correção ==

Coord -> SV : POST /api/solicitacoes/{id}/solicitar-correcao/ {observacoes}
SV -> AP : solicitar_correcao(request, pk)
AP -> DB : Atualizar Solicitacao.status = CORRECAO_NECESSARIA
AP -> NT : criar_notificacao(aluno, CORRECAO_SOLICITADA)
AP --> Coord : 200 OK {status: CORRECAO_NECESSARIA}

@enduml
```

---

## 5. Encaminhamento Institucional e Aceite da Empresa (FUNC12/FUNC13)

```kroki-plantuml
@startuml
title Encaminhamento e Aceite da Empresa

actor "Coordenador" as Coord
actor "Empresa" as Emp
participant "EncaminhamentoViewSet" as EV
participant "perform_create()" as PC
participant "@action aceitar" as AC
participant "Notificacao" as NT
database "Banco de Dados" as DB

== Encaminhamento pelo Coordenador ==

Coord -> EV : POST /api/encaminhamentos/ {solicitacao, organizacao, coordenador}
EV -> PC : perform_create(serializer)
PC -> DB : Criar Encaminhamento
PC -> DB : Atualizar Solicitacao.status = ENCAMINHADA
PC -> NT : criar_notificacao(aluno, ENCAMINHAMENTO_REALIZADO)
EV --> Coord : 201 Created

== Aceite pela Empresa ==

Emp -> EV : POST /api/encaminhamentos/{id}/aceitar/
EV -> AC : aceitar(request, pk)
AC -> NT : criar_notificacao(aluno, SOLICITACAO_APROVADA)
AC --> Emp : 200 OK {aceito: true}

@enduml
```

---

## Conclusão

<p align="justify">
Os diagramas de sequência apresentados cobrem os fluxos principais do sistema: autenticação, criação de solicitação com checklist automático, envio de documentos com transição de status, análise/aprovação pelo coordenador, e encaminhamento institucional com aceite da empresa. Cada fluxo demonstra como os componentes da API interagem para orquestrar o processo completo de validação de estágio.
</p>

---

## Autor(es)

| Data       | Versão | Descrição                            | Autor(es)         |
|---|---|---|---|
| 07/06/2026 | 1.0    | Criação dos diagramas de sequência reais do sistema | Equipe PBE |
