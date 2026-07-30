# LOG ESPECIAL - 001 - 29/07/2026 23h16min - Retomada Final Da Homologacao Da SPEC-012

## Finalidade

Este log especial consolida o ponto de parada da homologacao do grupo
`TASK-101` a `TASK-108`, referente a
`specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`.

O grupo permanece em `aguardando_homologacao`.

Este documento deve ser o primeiro artefato lido na proxima sessao. Ele nao
substitui os logs individuais nem os logs especiais anteriores; ele resume as
decisoes tomadas, ajustes executados e pendencias que ainda exigem decisao ou
acao governada.

## Padrao Proposto Para Novos Logs Especiais

Usar nomes datados e orientados a retomada:

```text
logs/LOG-ESPECIAL-NNN-DD.MM.YYYY-HHhMMmin.md
```

Exemplo:

```text
logs/LOG-ESPECIAL-001-29.07.2026-23h16min.md
```

Motivo: logs especiais nao seguem uma TASK unica; o sequencial preserva a
ordem cronologica de criacao e a data/hora explicita facilita retomadas.

## Fontes Que Devem Ser Consultadas Na Proxima Sessao

1. Este log especial.
2. `logs/LOG-ESPECIAL-homologacao-ui-balanco-spec-012.md`.
3. `logs/LOG-ESPECIAL-retomada-homologacao-spec-012.md`, se for necessario
   retomar contexto completo da execucao tecnica.
4. Logs individuais das TASKs afetadas, se houver novo ajuste:
   - `logs/LOG-101-ampliar-parser-balanco-declarado.md`;
   - `logs/LOG-102-persistir-ecd-balanco-declarado.md`;
   - `logs/LOG-103-reprocessar-importacoes-ecd-legadas.md`;
   - `logs/LOG-104-implementar-conciliacao-balanco-declarado.md`;
   - `logs/LOG-105-criar-api-balanco-declarado.md`;
   - `logs/LOG-106-criar-ui-balanco-declarado.md`;
   - `logs/LOG-107-integrar-validade-balanco-plra-capag.md`;
   - `logs/LOG-108-validar-fluxo-balanco-declarado.md`.

## Decisoes Consolidadas

### Estados Do Balanço Declarado

- `VALIDO`: fluxo normal. A importacao gera analise utilizavel e permite
  resultado anual final PLRA/CAPAG-E.
- `OBRIGATORIO_AUSENTE`: falha de importacao/preparacao. A ECD e rejeitada
  antes de criar analise utilizavel.
- `NAO_OBRIGATORIO`: falha de elegibilidade para CAPAG-E. A ECD deve cobrir
  exercicio anual encerrado e conter Bloco J.
- `ESTRUTURA_INVALIDA`: falha de importacao/preparacao. A ECD enviada ao
  CAPAG-E deve ter sido previamente transmitida/validada no ambiente oficial da
  Receita Federal/PGE do SPED.
- `DIVERGENTE`: a importacao conclui e cria analise diagnostica. A arvore
  `J100` permanece navegavel, as linhas problematicas sao destacadas e os
  componentes `I050/I052/I155` abrem sob demanda. Nao ha correcao manual na
  camada declarada e a CAPAG-E final nao deve ser emitida nesse fluxo.

### Requisito De Produto Para Importacao CAPAG-E

- A ECD importada deve corresponder ao exercicio anual encerrado.
- A ECD deve conter Bloco J quando necessario para a analise CAPAG-E.
- A ECD deve ter sido previamente transmitida/validada no ambiente oficial da
  Receita Federal/PGE do SPED.

### UI Do Balanço Declarado

- A tela deve recuperar o padrao visual anterior ao ciclo da `SPEC-012`.
- A visualizacao deve manter `Duas colunas` e `Livro-razao`.
- A organizacao visual deve usar totalizadores `J100`
  (`aggregation_code_type = T`) como base para macrogrupos e microgrupos.
- A ordem, lado, hierarquia e valores continuam vindo do backend e do `J100`.
- O frontend nao deve reconstruir a arvore a partir de `I050`.
- O frontend nao deve calcular totais, diferencas ou percentuais locais para a
  camada declarada.
- A camada declarada nao deve ter switches.
- A acao de auditoria/componentes deve abrir os componentes analiticos
  `I050/I052/I155` sob demanda.

### Reorganizacao Visual Dos Grupos

Regra atualmente implementada:

- separar primeiro por `balance_group`:
  - `A`: Ativo;
  - `P`: Passivo e Patrimonio Liquido;
- se a raiz for ampla demais, como `Ativo`, `Passivo`,
  `Patrimonio Liquido` ou `Passivo e Patrimonio Liquido`, os filhos diretos
  viram os cards principais;
- cada card representa um macrogrupo `J100`;
- dentro do card, mostrar preferencialmente os totalizadores sinteticos mais
  profundos, evitando repetir toda a cadeia sintetica;
- detalhes `J100` aparecem quando forem necessarios para apresentacao e
  auditoria;
- a regra e somente de apresentacao. Nao altera valores, nao recalcula total e
  nao muda classificacao contabil.

## Ajustes Executados Nesta Sessao

- Importacao passou a rejeitar antes da persistencia os estados:
  - `OBRIGATORIO_AUSENTE`;
  - `NAO_OBRIGATORIO`;
  - `ESTRUTURA_INVALIDA`.
- `DIVERGENTE` permanece importavel como diagnostico navegavel.
- Fixtures sinteticas antigas foram ajustadas para conter Bloco J anual valido
  quando a finalidade do teste nao era validar rejeicao.
- A UI foi ajustada em duas rodadas:
  1. primeira tentativa de restauracao visual ainda ficou diferente da tela
     anterior;
  2. segunda correcao voltou a usar `BalanceGroup`, `AccountRow` e
     `BalanceLedger`, preservando os componentes visuais anteriores e removendo
     apenas os switches na camada declarada.
- Logs individuais e log especial da UI foram atualizados.

## Validacoes Executadas Nesta Sessao

- `docker compose --profile test run --rm backend-tests`:
  - 279 testes aprovados.
- `docker compose --profile test run --rm frontend-tests`:
  - 28 testes aprovados e build de producao concluido.
- `docker compose --profile test run --rm frontend-e2e`:
  - 9 testes Playwright aprovados.
- `git diff --check`:
  - aprovado.
- busca por `parseFloat` e `float(` nos arquivos alterados:
  - nenhuma ocorrencia encontrada.

## Pendencias Para Decidir Ou Executar

### 1. Homologar Ou Reprovar O Grupo `TASK-101` A `TASK-108`

Pendencia principal:

- o usuario precisa revisar a tela novamente e decidir se homologa o grupo ou
  se ainda ha ajuste relacionado a `TASK-101` a `TASK-108`.

Se homologar:

- registrar aprovacao nos logs individuais afetados;
- atualizar `ROADMAP.md` para marcar o grupo como `concluido`;
- recalcular a proxima tarefa pelo fluxo governado.

Se reprovar ou pedir novo ajuste:

- manter o grupo em `aguardando_homologacao`;
- aplicar `scope-resolution`;
- executar apenas ajustes relacionados ao grupo, salvo gate de excecao.

### 2. Criar TASK Governada Para Ajustar Skills E Gates De Frontend

Pendencia obrigatoria registrada por decisao do usuario:

- criar uma TASK governada para revisar e ajustar as skills governadas,
  principalmente as skills de execucao de TASKs, para incluir gate forte em
  ajustes de frontend, design, UI e UX.

Problema observado:

- durante a homologacao, ajustes visuais relevantes foram feitos sem fidelidade
  suficiente ao padrao aprovado anteriormente;
- a recuperacao posterior consumiu tempo apenas para desfazer divergencias
  visuais que nao deveriam ter sido introduzidas sem autorizacao expressa.

Diretriz desejada para a futura TASK:

- quando uma TASK envolver frontend/design/UI/UX, o agente deve identificar
  explicitamente a referencia visual governada antes de implementar;
- se houver tela anterior aprovada, ela deve ser tratada como baseline visual;
- mudancas visuais relevantes devem exigir autorizacao expressa do usuario;
- se o ajuste for apenas tecnico, ele nao deve alterar layout, fonte,
  espacamento, densidade, componentes visuais ou hierarquia visual sem
  autorizacao;
- em homologacao, reprovação visual deve ser tratada como ajuste da TASK atual
  quando relacionada ao grupo em homologacao;
- a validacao deve incluir comparacao objetiva com a referencia aprovada quando
  houver baseline.

Esta pendencia ainda nao cria a TASK por si so. Na proxima sessao, deve ser
usado o fluxo governado adequado para criar a TASK, caso o usuario confirme.

### 3. Decidir Regra Futura Para CAPAG-E Com `DIVERGENTE` Auditado

Ainda nao aprovado:

- criar regra governada futura para permitir CAPAG-E mesmo com divergencia,
  desde que exista auditoria suficiente.

Observacao:

- essa regra nao pertence a camada declarada pura da `SPEC-012`;
- exige nova decisao governada, pois altera elegibilidade/metodologia do
  resultado final.

### 4. Decidir SPEC Ou TASK Para Simulacoes Manuais

Ainda precisa ser decidido:

- se sera criada nova SPEC para simulacao/revisao prudencial manual;
- se essa SPEC deve vir antes da execucao completa da camada reclassificada ou
  comportamental;
- como switches devem operar em contas sinteticas e analiticas;
- como evitar dupla exclusao entre conta sintetica e filhos;
- se cenarios serao descartaveis ou persistidos;
- como registrar justificativa, evidencia e impacto em PLRA/CAPAG-E;
- como diferenciar teste exploratorio de resultado final.

### 5. Deliberar Sobre Versionamento E Arquivos Temporarios

Pendente desde `logs/LOG-ESPECIAL-retomada-homologacao-spec-012.md`:

- decidir se `.playwright-mcp/` deve ser integralmente ignorada;
- decidir se os arquivos ja rastreados de `.playwright-mcp/` devem sair do
  indice do Git sem apagar inicialmente as copias locais;
- avaliar planilha `.xlsx` rastreada em `.playwright-mcp/`, inclusive quanto a
  dados contabeis e necessidade de preservacao;
- confirmar `.agents/` como conteudo governado e versionado;
- definir tratamento de `.codex/`;
- confirmar `.github/` como automacao versionada;
- definir rotina para separar fonte reproduzivel, evidencia governada e
  artefato temporario.

Nenhuma limpeza ou exclusao foi executada nesta sessao.

## Roteiro Para A Proxima Sessao

1. Ler integralmente este log especial.
2. Informar ao usuario que este log especial foi consultado.
3. Perguntar se a tela atual da `SPEC-012` esta homologada.
4. Se o usuario homologar:
   - registrar homologacao;
   - atualizar `ROADMAP.md`;
   - recalcular proxima tarefa.
5. Se o usuario ainda apontar ajuste visual ou funcional relacionado ao grupo:
   - aplicar `scope-resolution`;
   - manter o grupo em `aguardando_homologacao`;
   - executar somente o ajuste relacionado, respeitando gates.
6. Antes de seguir para novas execucoes, tratar a pendencia obrigatoria de criar
   TASK governada para melhorar os gates das skills de frontend/design, se o
   usuario confirmar.
