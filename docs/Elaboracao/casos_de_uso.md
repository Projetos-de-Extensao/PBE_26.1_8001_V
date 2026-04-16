```plantuml
@startuml SGE_CasosDeUso

top to bottom direction
skinparam actorStyle hollow

skinparam usecase {
  BackgroundColor #F0F4FF
  BorderColor #3366CC
  FontSize 12
}

skinparam actor {
  BackgroundColor #E8F5E9
  BorderColor #2E7D32
}

skinparam note {
  BackgroundColor #FFFDE7
  BorderColor #F9A825
}

actor "Estudante"        as EST
actor "Organização"      as ORG
actor "Gestor"           as GES
actor "Plataforma"       as PLT

rectangle "Módulo do Estudante" {
  usecase "UC-E1: Registrar Conta"           as UE1
  usecase "UC-E2: Autenticar-se"             as UE2
  usecase "UC-E3: Consultar Oportunidades"   as UE3
  usecase "UC-E4: Enviar Candidatura"        as UE4
  usecase "UC-E5: Monitorar Processo"        as UE5
}

rectangle "Módulo da Organização" {
  usecase "UC-O1: Registrar Empresa"         as UO1
  usecase "UC-O2: Autenticar-se"             as UO2
  usecase "UC-O3: Publicar Vaga"             as UO3
  usecase "UC-O4: Consultar Inscritos"       as UO4
  usecase "UC-O5: Avaliar Candidatura"       as UO5
}

rectangle "Módulo do Gestor" {
  usecase "UC-G1: Autenticar-se"             as UG1
  usecase "UC-G2: Administrar Contas"        as UG2
  usecase "UC-G3: Homologar Vaga"            as UG3
  usecase "UC-G4: Emitir Relatório"          as UG4
}

EST --> UE1
EST --> UE2
EST --> UE3
EST --> UE4
EST --> UE5

ORG --> UO1
ORG --> UO2
ORG --> UO3
ORG --> UO4
ORG --> UO5

GES --> UG1
GES --> UG2
GES --> UG3
GES --> UG4

@enduml
