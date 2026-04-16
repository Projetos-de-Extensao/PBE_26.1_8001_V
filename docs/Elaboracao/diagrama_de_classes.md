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

```plantuml
@startuml
title Diagrama de Classes - Sistema de Validação de Estágio

skinparam classAttributeIconSize 0

abstract class Usuario {
  - id: int
  - nome: String
  - email: String
  - senha: String
  + autenticar(email: String, senha: String): boolean
  + logout(): void
}

class Aluno {
  - matricula: String
  - curso: String
  - campus: String
  + criarSolicitacao(curso: String, campus: String): Solicitacao
  + consultarChecklist(solicitacaoId: int): Checklist
  + baixarModelo(nomeDocumento: String): ModeloDocumento
  + enviarDocumentos(documentos: List<Documento>): void
  + acompanharStatus(solicitacaoId: int): String
}

class Coordenador {
  - setor: String
  + listarSolicitacoes(): List<Solicitacao>
  + analisarDocumentos(solicitacao: Solicitacao): Analise
  + revisarSolicitacao(solicitacao: Solicitacao, decisao: String): void
  + assinarDocumento(documento: Documento): AssinaturaDigital
  + encaminharParaReitoria(solicitacao: Solicitacao): Encaminhamento
}

class Solicitacao {
  - id: int
  - dataCriacao: Date
  - curso: String
  - campus: String
  - status: StatusSolicitacao
  + registrar(): void
  + atualizarStatus(novoStatus: StatusSolicitacao): void
  + consultarStatus(): StatusSolicitacao
}

class Checklist {
  - id: int
  - itensObrigatorios: String[]
  + exibirChecklist(): void
  + validarPendencias(): boolean
}

class Documento {
  - id: int
  - nome: String
  - tipo: String
  - arquivo: String
  - statusValidacao: String
  + anexarArquivo(): void
  + validarDocumento(): boolean
  + atualizarStatus(status: String): void
}

class ModeloDocumento {
  - id: int
  - nome: String
  - descricao: String
  - arquivoModelo: String
  + disponibilizarDownload(): void
}

class Analise {
  - id: int
  - dataAnalise: Date
  - resultado: ResultadoAnalise
  - observacoes: String
  + registrarAnalise(): void
  + emitirParecer(): String
}

class Notificacao {
  - id: int
  - mensagem: String
  - dataEnvio: Date
  - tipoEvento: String
  + enviar(usuario: Usuario): void
}

class AssinaturaDigital {
  - id: int
  - dataAssinatura: Date
  - status: String
  + assinar(): void
  + validarAssinatura(): boolean
}

class Encaminhamento {
  - id: int
  - destino: String
  - dataEnvio: Date
  - status: String
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

Aluno "1" -- "0..*" Solicitacao : cria >
Solicitacao "1" -- "1" Checklist : possui >
Solicitacao "1" -- "0..*" Documento : contém >
Solicitacao "1" -- "0..1" Analise : gera >
Solicitacao "1" -- "0..1" Encaminhamento : gera >

Aluno "1" -- "0..*" Notificacao : recebe >
Coordenador "1" -- "0..*" Notificacao : recebe >

Coordenador "1" -- "0..*" Analise : realiza >
Coordenador "1" -- "0..*" AssinaturaDigital : executa >

Documento "1" -- "0..1" AssinaturaDigital : recebe >
Aluno "1" -- "0..*" ModeloDocumento : acessa >

Analise --> ResultadoAnalise
Solicitacao --> StatusSolicitacao

@enduml
