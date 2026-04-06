## Tema
Validação automática do relatório final de estágio na aplicação web de gestão de estágio.

## Contexto
A ideia deste projeto é ajudar no processo de análise dos relatórios finais de estágio dentro de uma aplicação web de gestão de estágio.  
Hoje, essa validação pode acabar sendo muito manual, o que gera demora e também faz com que erros simples passem ou precisem ser corrigidos só depois.

## Problema que queremos resolver
Alguns pontos que esse projeto tenta melhorar:

- a revisão manual pode levar tempo;
- relatórios podem ser enviados com campos faltando;
- pode haver erros de estrutura ou formatação;
- nem sempre existe um padrão claro entre os relatórios enviados;
- o coordenador ou responsável pode acabar gastando tempo com conferências básicas.

## Objetivo do brainstorm
Este brainstorm tem como objetivo levantar ideias iniciais para o projeto, pensando principalmente em:

- funcionalidades possíveis;
- regras de validação;
- fluxo de uso do sistema;
- dificuldades que podem aparecer no desenvolvimento;
- definição de um MVP simples e viável.

## Ideias de funcionalidades
Algumas ideias iniciais para o sistema:

- verificar se os campos obrigatórios foram preenchidos;
- validar se o arquivo enviado está em um formato aceito, como PDF ou DOCX;
- checar se o relatório possui seções básicas, como introdução, atividades desenvolvidas e conclusão;
- identificar relatórios com conteúdo muito curto;
- mostrar mensagens de erro ou aviso para ajudar o aluno a corrigir;
- permitir o reenvio do relatório após ajustes;
- exibir o status do relatório no sistema;
- gerar um resumo simples com os problemas encontrados;
- encaminhar o relatório para revisão final de um coordenador após a validação automática.

## Ideias técnicas
Pensando de forma inicial, o projeto poderia seguir algo assim:

- leitura do arquivo enviado pelo usuário;
- extração do texto do relatório;
- aplicação de regras simples de validação;
- retorno de mensagens com os erros ou avisos encontrados;
- armazenamento do resultado da validação para consulta posterior.

Também pode ser interessante separar as validações por etapas, por exemplo:

1. validação do arquivo;
2. validação dos campos obrigatórios;
3. validação da estrutura do relatório;
4. exibição do resultado para o usuário.

## Fluxo sugerido do usuário
Um fluxo simples de uso poderia ser:

1. o estagiário envia o relatório final na plataforma;
2. o sistema realiza a validação automática;
3. caso existam erros, o sistema informa o que precisa ser corrigido;
4. o estagiário ajusta o arquivo e envia novamente;
5. se estiver tudo certo, o relatório segue para revisão final.

## Critérios iniciais de validação
Exemplos de validações que podem existir no começo do projeto:

- nome do aluno preenchido;
- matrícula preenchida;
- empresa informada;
- período de estágio informado;
- arquivo em formato permitido;
- presença de seções principais no relatório;
- quantidade mínima de conteúdo.

## Riscos e desafios
Alguns desafios que podem aparecer:

- dificuldade para ler corretamente certos arquivos;
- relatórios com estruturas diferentes entre cursos;
- regras muito rígidas que acabem marcando erro sem necessidade;
- regras muito simples que deixem passar problemas importantes;
- dificuldade em definir até onde a validação automática deve ir.

## Perguntas em aberto
Durante o desenvolvimento, algumas dúvidas ainda precisam ser melhor definidas:

- quais validações devem bloquear o envio?
- quais validações devem aparecer apenas como aviso?
- o coordenador poderá aprovar um relatório mesmo com alertas?
- haverá um modelo padrão de relatório para todos os cursos?
- quais formatos serão aceitos no MVP?
- a empresa contratante afeta a estrutura do documento? Ex. Associações de estágio (NUBE, entre outros), mudam algo no arquivo?


## MVP proposto
Para uma primeira versão, queremos algo mais simples:

- validação de campos obrigatórios;
- verificação do formato do arquivo;
- checagem básica das seções do relatório;
- exibição de feedback simples para o usuário.

## Métricas de sucesso
Algumas formas de avaliar se a ideia está funcionando:

- redução do tempo de análise inicial;
- diminuição da quantidade de relatórios com erro básico;
- tempo médio entre envio e retorno do sistema;
- quantidade de relatórios reenviados para correção.

## Próximos passos
Como próximos passos, seria interessante:

1. definir quais validações são prioritárias;
2. entender como o sistema atual funciona;
3. escolher uma forma de ler e analisar os arquivos;
4. montar um protótipo simples da validação;
5. testar com exemplos de relatórios.

## Observação final
Este brainstorm representa ideias iniciais do projeto.  
Alguns pontos ainda podem mudar conforme o entendimento do problema ficar mais claro e conforme forem aparecendo limitações técnicas ou novas necessidades.
