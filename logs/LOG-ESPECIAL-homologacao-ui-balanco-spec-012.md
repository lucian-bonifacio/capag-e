# LOG ESPECIAL - Homologacao UI Do Balanco Da SPEC-012

## Nota Sobre Este Documento

Este log especial registra a interrupcao governada da homologacao consolidada
das `TASK-101` a `TASK-108`, especificamente sobre a UI/UX do Balanco
Patrimonial declarado.

O grupo permanece em `aguardando_homologacao`. Este documento nao substitui os
logs individuais nem o
`logs/LOG-ESPECIAL-retomada-homologacao-spec-012.md`; ele complementa a
retomada registrando as decisoes ja tomadas e as decisoes pendentes sobre a
tela.

## Estado Atual

- Data da interrupcao: 2026-07-29.
- Grupo: `TASK-101` a `TASK-108`.
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`.
- Status do grupo: `aguardando_homologacao`.
- Motivo: usuario concordou com ajustes de processo, backend e metodologia,
  mas nao homologou os ajustes de UI/UX da tela de Balanco Patrimonial.
- Encaminhamento: continuar a tomada de decisao antes de implementar qualquer
  ajuste na UI.

## Objetivo Acordado

Manter o contrato da `SPEC-012` e recuperar, tanto quanto possivel, a tela
anterior de Balanco Patrimonial.

A tela anterior referida pelo usuario era a tela com alternancia entre:

- `Duas colunas`;
- `Livro-razao`.

O ajuste desejado deve preservar o visual, a organizacao e a ergonomia
anteriores, sem desfazer parser, persistencia, conciliacao, API,
integracao PLRA/CAPAG-E ou validacoes da `SPEC-012`.

## Decisoes Ja Tomadas

### 1. Fonte Da Hierarquia

Decisao:

- recuperar o layout/interacao anterior;
- renderizar a arvore oficial `J100` recebida da API;
- nao reconstruir hierarquia no frontend a partir de contas `I050`.

Implicacoes:

- usar `aggregation_code` em vez de `account_code` como identidade visual da
  linha do balanco;
- usar `description` em vez de `account_name`;
- usar hierarquia, ordem, lado e tipo de linha recebidos do backend;
- preservar o visual de macrogrupo e subgrupos.

### 2. Totais E Calculos Locais

Decisao:

- preservar o contrato da `SPEC-012` sem criar calculo local;
- manter o visual anterior de totais e cabecalhos;
- exibir somente valores recebidos da API ou totalizadores `J100` ja validados
  pelo backend;
- nao calcular total de grupo, total de lado, diferenca ou percentual no
  frontend.

Observacao:

- os totalizadores sao validados no backend como prova de consistencia: soma
  assinada dos filhos imediatos no `J100`, Ativo final contra Passivo + PL,
  conciliacao de detalhes por `I050 -> I052 -> I155` e diferencas em `Decimal`.

### 3. Switches Na Visao Declarada

Decisao:

- remover switches da tela declarada da `SPEC-012`;
- recuperar o visual anterior sem transformar a tela declarada em revisao
  prudencial;
- substituir a funcao de inspeção por acao de auditoria/componentes;
- a acao de auditoria deve abrir os componentes `I050/I052/I155` da linha
  `J100` selecionada.

Decisao relacionada:

- a necessidade de switches para testes manuais de exclusao/inclusao de contas
  deve ser tratada em nova SPEC ou ajuste governado proprio, fora da
  `SPEC-012`.
- registrar como lembrete obrigatorio para essa futura SPEC: switches sao
  importantes para simulacoes manuais por conta sintetica e analitica, com
  impacto em PLRA/CAPAG-E.

Contexto:

- a camada citada para esse fluxo futuro e a camada reclassificada/
  comportamental, governada por
  `specs/SPEC-003-modulo-2-capag-reclassificada.md`;
- pode fazer sentido tratar a nova SPEC antes da execucao da UI de revisao
  reclassificada, especialmente antes de
  `tasks/TASK-047-criar-ui-revisao-reclassificada.md`.

### 4. Alternancia De Visualizacao

Decisao:

- restaurar o controle `Duas colunas` / `Livro-razao`;
- usar a mesma arvore `J100` do backend em ambos os modos;
- no modo `Duas colunas`, manter Ativo a esquerda e Passivo + PL a direita;
- no modo `Livro-razao`, mostrar a mesma estrutura em formato linear;
- nao recalcular, reordenar por regra local ou alterar estados.

### 5. Padrao Visual Resumido

Decisao:

- recuperar o padrao visual anterior com visao resumida;
- em `Duas colunas`, abrir mostrando principalmente totalizadores `J100`
  (`aggregation_code_type = T`) como macrogrupos e subgrupos;
- linhas `J100` de detalhe (`aggregation_code_type = D`) nao devem poluir a
  visao inicial;
- detalhes `J100` devem aparecer por expansao;
- acao de auditoria/componentes deve abrir os componentes analiticos
  `I050/I052/I155`;
- a estrutura, ordem, lado e tipo de linha continuam vindo do backend.

## Decisoes Pendentes

### 1. Tratamento De Cada `balance_status`

Decisao tomada em 2026-07-29:

- `VALIDO`: fluxo normal. A importacao gera analise utilizavel e permite
  resultado anual final PLRA/CAPAG-E.
- `OBRIGATORIO_AUSENTE`: falha de importacao/preparacao. Se o Bloco J era
  obrigatorio e o `J100` esta ausente, a ECD deve ser rejeitada antes de criar
  analise utilizavel. Mensagem-base: "ECD rejeitada: Balanco Patrimonial
  obrigatorio ausente. Envie uma ECD corrigida ou substituta."
- `NAO_OBRIGATORIO`: falha de elegibilidade da importacao. Para CAPAG-E, a ECD
  deve cobrir o exercicio anual encerrado e conter Bloco J. Mensagem-base:
  "ECD rejeitada: o arquivo nao cobre o encerramento anual necessario para
  analise CAPAG-E. Envie a ECD do exercicio encerrado contendo o Bloco J."
- `ESTRUTURA_INVALIDA`: falha de importacao/preparacao. A ECD enviada ao CAPAG
  deve ter sido previamente transmitida/validada no ambiente oficial da Receita
  Federal/PGE do SPED. Estrutura `J100` invalida nao deve gerar analise
  navegavel. Mensagem-base: "ECD rejeitada: o Balanco Patrimonial declarado no
  J100 nao possui estrutura valida para analise CAPAG-E. Envie a ECD anual
  transmitida/validada no PGE do SPED ou uma ECD substituta valida."
- `DIVERGENTE`: a importacao conclui e cria analise diagnostica. A arvore
  `J100` permanece navegavel, linhas problematicas devem ser destacadas, e os
  componentes `I050/I052/I155` devem abrir sob demanda. Nao ha correcao manual
  na camada declarada e a CAPAG-E final nao deve ser emitida nesse fluxo.

Requisito de produto consolidado:

- para analise CAPAG-E, a ECD importada deve corresponder ao exercicio anual
  encerrado e ter sido previamente transmitida/validada no ambiente oficial da
  Receita Federal/PGE do SPED.

Ponto sensivel:

- o usuario nao gosta da ideia de "calculos bloqueados";
- foi esclarecido que, pela `SPEC-012`, o bloqueio impede afirmar resultado
  anual final PLRA/CAPAG-E quando a base declarada nao e valida, mas nao deve
  esconder valores diagnosticos nem impedir auditoria.

Proposta em discussao, ainda nao aprovada:

- criar regra governada futura para permitir CAPAG-E com divergencia auditada,
  se aplicavel. Essa regra nao pertence a camada declarada pura e exige decisao
  propria, pois altera elegibilidade/metodologia do resultado final.

### 2. Especificacao Futura Para Simulacoes Manuais

Ainda precisa ser decidido, em fluxo governado proprio:

- se sera criada nova SPEC para simulacao/revisao prudencial manual;
- se essa SPEC deve ser priorizada antes da execucao completa da camada
  reclassificada/comportamental;
- como switches devem operar em contas sinteticas e analiticas;
- como evitar dupla exclusao entre conta sintetica e seus filhos;
- se cenarios serao descartaveis ou persistidos;
- como registrar justificativa, evidencia e impacto em PLRA/CAPAG-E;
- como diferenciar teste exploratorio de resultado final.

## Roteiro Para A Proxima Sessao

1. Ler integralmente este log especial.
2. Ler, se necessario, o
   `logs/LOG-ESPECIAL-retomada-homologacao-spec-012.md`.
3. Informar ao usuario que os logs especiais foram consultados.
4. Retomar a discussao a partir do tratamento de cada `balance_status`.
5. Nao implementar ajuste de UI antes de concluir as decisoes pendentes ou
   receber autorizacao expressa do usuario para um recorte especifico.
6. Apos decisao, enquadrar o ajuste como ajuste da homologacao do grupo
   `TASK-101` a `TASK-108`, afetando principalmente a `TASK-106`.

## Rodada De Ajuste Visual - 2026-07-29

Decisao do usuario:

- a tela ajustada nao ficou parecida com a tela anterior;
- foi autorizada a recuperacao do padrao visual anterior.

Ajuste executado:

- restaurado o padrao de tela com indicadores superiores, busca, alternancia
  `Duas colunas`/`Livro-razao`, cards de grupo e arvore expansivel;
- preservado o contrato da camada declarada: sem switches, sem calculo local e
  com componentes `I050/I052/I155` abertos sob demanda;
- mantido `DIVERGENTE` como diagnostico navegavel, com resultado anual
  indisponivel nesse fluxo.

Validacoes:

- `docker compose --profile test run --rm frontend-tests`: 28 testes aprovados
  e build de producao concluido;
- `docker compose --profile test run --rm frontend-e2e`: 9 testes Playwright
  aprovados;
- `git diff --check`: aprovado;
- busca por `parseFloat` e `float(` nos arquivos alterados: nenhuma ocorrencia
  encontrada.

## Rodada De Correcao De Fidelidade Visual - 2026-07-29

Nova reprovação do usuario:

- a visualizacao `Duas colunas` ainda estava diferente da tela anterior;
- os cards dos microgrupos estavam ruins;
- a fonte, espacamentos e composicao visual divergiam do padrao anterior;
- grupos sinteticos apareciam repetidos, por exemplo `Ativo Circulante`.

Ajuste executado:

- a rota voltou a usar os componentes visuais anteriores `BalanceGroup`,
  `AccountRow` e `BalanceLedger`;
- `AccountRow` recebeu suporte opcional para ocultar o switch somente na camada
  declarada, preservando o comportamento padrao das demais telas;
- a apresentacao dos grupos foi reorganizada para usar macrogrupos como cards
  e mostrar os sinteticos mais profundos como linhas, evitando repeticao
  artificial da cadeia sintetica;
- o contrato novo foi preservado: valores vindos da API, sem recalculo local e
  componentes `I050/I052/I155` sob demanda.

Validacoes:

- `docker compose --profile test run --rm frontend-tests`: 28 testes aprovados
  e build de producao concluido;
- `docker compose --profile test run --rm frontend-e2e`: 9 testes Playwright
  aprovados;
- `git diff --check`: aprovado;
- busca por `parseFloat` e `float(` nos arquivos alterados: nenhuma ocorrencia
  encontrada.
