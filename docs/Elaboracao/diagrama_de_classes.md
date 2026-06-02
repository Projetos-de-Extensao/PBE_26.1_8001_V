---
id: diagrama_de_classes
title: Diagrama de Classes
---

# Diagrama de Classes

## Introdução

O diagrama de classes representa a estrutura do sistema de validação automatizada de documentos de estágio, descrevendo as principais entidades, seus atributos, métodos e relacionamentos.

Com base nos casos de uso definidos, o sistema foi modelado considerando dois perfis principais de usuários: **Aluno** e **Coordenador**, além das entidades responsáveis pelo gerenciamento das solicitações, documentos, análises e notificações.

---

## Diagrama em PlantUML

```kroki-plantuml
@startuml
title Diagrama de Classes - Sistema de Validação de Estágio

skinparam classAttributeIconSize 0

abstract class Usuario {
  - id: int
  - username: String
  - email: String
  - is_empresa: boolean
  - matricula: String
  + autenticar(username: String, senha: String): boolean
  + logout(): void
}

class Aluno {
  - nome: String
  - curso: String
  - campus: String
  - data_cadastro: Date
  + criarSolicitacao(curso: String, campus: String): Solicitacao
  + consultarChecklist(solicitacaoId: int): Checklist
  + baixarModelo(nomeDocumento: String): ModeloDocumento
  + enviarDocumentos(documentos: List<Documento>): void
  + acompanharStatus(solicitacaoId: int): String
}

class Coordenador {
  - nome: String
  - setor: String
  + listarSolicitacoes(): List<Solicitacao>
  + analisarDocumentos(solicitacao: Solicitacao): Analise
  + revisarSolicitacao(solicitacao: Solicitacao, decisao: String): void
  + assinarDocumento(documento: Documento): AssinaturaDigital
  + encaminharParaReitoria(solicitacao: Solicitacao): Encaminhamento
}

class OrganizacaoParceira {
  - cnpj: String
  - razao_social: String
  + validarProposta(solicitacao: Solicitacao): void
}

class Solicitacao {
  - id: int
  - curso: String
  - campus: String
  - status: StatusSolicitacao
  - data_criacao: Date
  - data_atualizacao: Date
  + registrar(): void
  + atualizarStatus(novoStatus: StatusSolicitacao): void
  + consultarStatus(): StatusSolicitacao
}

class Checklist {
  - id: int
  - completo: boolean
  - data_criacao: Date
  - data_atualizacao: Date
  + exibirChecklist(): void
  + validarPendencias(): boolean
}

class ItemChecklist {
  - id: int
  - status: String
  - observacao: String
}

class Documento {
  - id: int
  - nome: String
  - tipo: String
  - arquivo: String
  - status_validacao: String
  - data_envio: Date
  + anexarArquivo(): void
  + validarDocumento(): boolean
  + atualizarStatus(status: String): void
}

class ModeloDocumento {
  - id: int
  - nome: String
  - descricao: String
  - arquivo_template: String
  - obrigatorio: boolean
  - data_criacao: Date
  - data_atualizacao: Date
  + disponibilizarDownload(): void
}

class Analise {
  - id: int
  - resultado: ResultadoAnalise
  - observacoes: String
  - data_analise: Date
  + registrarAnalise(): void
  + emitirParecer(): String
}

class Notificacao {
  - id: int
  - mensagem: String
  - tipo_evento: String
  - lida: boolean
  - data_criacao: Date
  + enviar(usuario: Usuario): void
}

class AssinaturaDigital {
  - id: int
  - hash_assinatura: String
  - valida: boolean
  - data_assinatura: Date
  + assinar(): void
  + validarAssinatura(): boolean
}

class Encaminhamento {
  - id: int
  - observacoes: String
  - data_encaminhamento: Date
  + encaminhar(): void
  + atualizarStatus(): void
}

enum StatusSolicitacao {
  CRIADA
  EM_VALIDACAO
  CORRECAO_NECESSARIA
  APROVADA
  REPROVADA
  ENCAMINHADA
}

enum ResultadoAnalise {
  APROVADO
  REPROVADO
  CORRECAO_NECESSARIA
}

Usuario <|-- Aluno
Usuario <|-- Coordenador
Usuario <|-- OrganizacaoParceira

Aluno "1" -- "0..*" Solicitacao : cria >
Solicitacao "1" -- "1" Checklist : possui >
Checklist "1" -- "0..*" ItemChecklist : contém >
ItemChecklist "0..*" -- "1" ModeloDocumento : refere-se a >
Solicitacao "1" -- "0..*" Documento : contém >
Solicitacao "1" -- "0..1" Analise : gera >
Solicitacao "1" -- "0..*" Encaminhamento : gera >

Usuario "1" -- "0..*" Notificacao : recebe >

Coordenador "1" -- "0..*" Analise : realiza >
Usuario "1" -- "0..*" AssinaturaDigital : executa >
OrganizacaoParceira "1" -- "0..*" Solicitacao : valida >

Documento "1" -- "0..*" AssinaturaDigital : recebe >
Aluno "1" -- "0..*" ModeloDocumento : acessa >
Encaminhamento "0..*" -- "1" OrganizacaoParceira : direcionado a >
Encaminhamento "0..*" -- "1" Coordenador : realizado por >

Analise --> ResultadoAnalise
Solicitacao --> StatusSolicitacao

@enduml
```
