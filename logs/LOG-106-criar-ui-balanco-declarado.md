# LOG - TASK-106 - Criar UI do balanço declarado

## Referência

- Task: `tasks/TASK-106-criar-ui-balanco-declarado.md`
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- Status: aguardando_homologacao

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `tasks/TASK-085-refinar-apresentacao-leitura-declarada.md`
- `tasks/TASK-105-criar-api-balanco-declarado.md`

## Execução

- Data: 2026-07-29
- Ação: implementação e validação.
- Resumo: a tela passou a renderizar diretamente a árvore J100 recebida, separar Ativo e Passivo + PL, destacar saldo final, estado geral e conciliação, e carregar componentes I050/I052/I155 sob demanda em diálogo. Switches, somas e reconstrução de hierarquia foram removidos da visão declarada.
- Data: 2026-07-29
- Ação: ajuste de homologação.
- Resumo: após decisão governada sobre `balance_status`, a UI passou a tratar `DIVERGENTE` como conciliação pendente navegável, com contador de divergências, resultado anual indisponível, árvore J100 preservada, ação de componentes também em linhas problemáticas sem componentes e resumo J100/I155/diferença/status no diálogo.
- Data: 2026-07-29
- Ação: ajuste de homologação visual.
- Resumo: após reprovação do visual pelo usuário, a tela do balanço declarado recuperou o padrão anterior com indicadores no topo, busca, alternância `Duas colunas`/`Livro-razão`, cards de grupo e árvore expansível. O contrato declarado foi preservado: sem switches, sem cálculo local e com auditoria de componentes sob demanda.
- Data: 2026-07-29
- Ação: correção de reprovação visual.
- Resumo: após nova reprovação do usuário, a tela deixou de usar os cards/linhas novos e voltou a compor a visualização com os componentes anteriores `BalanceGroup`, `AccountRow` e `BalanceLedger`. A organização dos grupos foi ajustada para apresentar macrogrupos e os sintéticos mais profundos, evitando repetição artificial de cadeias sintéticas como `Ativo Circulante`. A camada declarada segue sem switches e sem cálculo local de valores.

## Arquivos Alterados

- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/e2e/declared-layer.spec.ts`
- `frontend/src/components/dashboard/AccountRow.css`
- `frontend/src/components/dashboard/AccountRow.tsx`
- `frontend/src/App.tsx`
- `frontend/src/api/declared.ts`
- `frontend/src/routes/BalanceDashboardPage.css`
- `frontend/src/routes/BalanceDashboardPage.tsx`
- `frontend/src/test/runner.test.tsx`

## Validações

- Comando: `docker compose run --rm frontend-tests`.
  - Resultado: 27 testes aprovados e build de produção concluído.
- Comando: `docker compose run --rm frontend-e2e`.
  - Resultado: 9 testes Playwright aprovados, incluindo 4 cenários do balanço declarado.
- Inspeção: MCP Playwright em 1280x720, tela e diálogo de componentes.
  - Resultado: duas colunas alinhadas, zero switches, sem overflow horizontal; diálogo centralizado, sem overflow e com trilha I052/I155 legível.
- Comando: busca por `float`, `parseFloat`, cálculos removidos e `git diff --check`.
  - Resultado: nenhuma ocorrência proibida ou inconsistência de whitespace.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 28 testes aprovados e build de produção concluído.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 9 testes Playwright aprovados.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: busca por `parseFloat` e `float(` nos arquivos alterados.
  - Resultado: nenhuma ocorrência encontrada.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 28 testes aprovados e build de produção concluído após correção de fidelidade visual.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 9 testes Playwright aprovados após correção de fidelidade visual.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: busca por `parseFloat` e `float(` nos arquivos alterados.
  - Resultado: nenhuma ocorrência encontrada.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 28 testes aprovados e build de produção concluído após restauração visual.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 9 testes Playwright aprovados após restauração visual.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: busca por `parseFloat` e `float(` nos arquivos alterados.
  - Resultado: nenhuma ocorrência encontrada.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aguardando_homologacao
- Data: 2026-07-29
- Decisão do usuário: grupo TASK-101 a TASK-108 autorizado para execução contínua.
- Observação: homologação consolidada será solicitada ao final do grupo.
