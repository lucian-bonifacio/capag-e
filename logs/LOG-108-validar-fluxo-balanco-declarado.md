# LOG - TASK-108 - Validar fluxo do balanço declarado

## Referência

- Task: `tasks/TASK-108-validar-fluxo-balanco-declarado.md`
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `docs/methodology/pesquisa-oficial-balanco-patrimonial-ecd.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `tasks/TASK-101-ampliar-parser-balanco-declarado.md` a `tasks/TASK-107-integrar-validade-balanco-plra-capag.md`

## Execução

- Data: 2026-07-29
- Ação: consolidação, correção e validação end-to-end.
- Resumo: foram consolidadas fixtures ECD para os cinco estados gerais. A validação real revelou que o `I030` oficial completo guarda a data de encerramento no último campo; o parser foi corrigido para o leiaute completo, elevado para `2.1.0` e importações `2.0.0` foram marcadas para reimportação controlada.
- DATAPACK: reprocessado no ambiente oficial, balanço `VALIDO`, 48 linhas de detalhe `CONCILIADA` e nenhuma limitação.
- INVENTCLOUD: importado no ambiente oficial e reimportado em teste isolado, balanço `DIVERGENTE`, com 502 linhas `CONCILIADA` e 19 `SEM_SALDO_I155`.
- Data: 2026-07-29
- Ação: ajuste de homologação.
- Resumo: após decisão governada sobre `balance_status`, fixtures sintéticas antigas da camada declarada foram alinhadas ao requisito de ECD anual com Bloco J válido para importação CAPAG-E. Foi criado teste de rejeição sem persistência para ECD com balanço obrigatório ausente e teste frontend para `DIVERGENTE` diagnóstico.
- Data: 2026-07-29
- Ação: validação de ajuste visual em homologação.
- Resumo: a restauração do padrão visual anterior da tela do balanço declarado foi validada por testes unitários/build e Playwright. Os testes foram ajustados para refletir a duplicidade intencional dos status no card de indicador e no badge do painel.
- Data: 2026-07-29
- Ação: validação de correção de reprovação visual.
- Resumo: a tela foi recomposta com os componentes visuais anteriores da dashboard, mantendo apenas as restrições novas da SPEC-012. Os testes unitários e E2E foram atualizados para o padrão antigo de auditoria por ícone/botão acessível, sem switches.
- Data: 2026-07-30
- Ação: validação de ajuste visual em homologação.
- Resumo: após autorização do usuário no flow de homologação, os cards iniciais redundantes de Ativo e Passivo + PL foram removidos da tela do Balanço Patrimonial declarado. O painel de status foi compactado e os testes unitários/E2E foram ajustados para validar status único no topo, mantendo a árvore J100 e a auditoria de componentes.
- Data: 2026-07-30
- Ação: validação de ajuste de auditoria em homologação.
- Resumo: a auditoria de totalizadores `J100` passou a retornar os componentes analíticos dos detalhes descendentes. A validação cobriu API, UI unitária e E2E para garantir que totalizadores apresentados como resumo abrem contas `I050/I052/I155` sem cálculo no frontend.
- Data: 2026-07-30
- Ação: validação de ajuste visual em homologação.
- Resumo: o alinhamento do modo `Livro-razão` foi corrigido para reservar coluna própria ao botão de auditoria, evitando sobreposição com os valores. A validação cobriu testes frontend/build, E2E e verificação de whitespace.
- Data: 2026-07-30
- Ação: validação de ajuste visual em homologação.
- Resumo: a grade do modo `Livro-razão` foi unificada entre macrogrupos e microgrupos, com coluna de valor ampliada e sem quebra de linha. A validação cobriu testes frontend/build, E2E e verificação de whitespace.
- Data: 2026-07-30
- Ação: validação de ajuste de auditoria visual.
- Resumo: a tela mantém a apresentação principal nos totalizadores/microgrupos, com badge herdado quando há detalhe descendente problemático. A conta analítica problemática é destacada somente no diálogo de auditoria. A validação cobriu testes frontend/build, E2E e verificação de whitespace.

## Arquivos Alterados

- `backend/alembic/versions/0059_parser_2_1_reimport.py`
- `backend/app/io/ecd_parser.py`
- `backend/tests/fixtures/ecd/README.md`
- `backend/tests/fixtures/ecd/valid_declared.ecd`
- `backend/tests/fixtures/ecd/missing_i051.ecd`
- `backend/tests/fixtures/ecd/official_reference_missing.ecd`
- `backend/tests/fixtures/ecd/methodology_missing.ecd`
- `backend/tests/fixtures/ecd/blocked_rule.ecd`
- `backend/tests/fixtures/ecd/dangerous_prefix.ecd`
- `backend/tests/fixtures/ecd/balance_declared_divergent.ecd`
- `backend/tests/fixtures/ecd/balance_declared_invalid_structure.ecd`
- `backend/tests/fixtures/ecd/balance_declared_not_required.ecd`
- `backend/tests/fixtures/ecd/balance_declared_required_absent.ecd`
- `backend/tests/test_declared_balance_real_ecd.py`
- `backend/tests/test_declared_balance_service.py`
- `backend/tests/test_ecd_fixtures.py`
- `backend/tests/test_ecd_import_api.py`
- `backend/tests/test_ecd_parser.py`
- `backend/tests/test_ecd_reprocessing.py`
- `backend/app/api/declared.py`
- `backend/tests/test_declared_api.py`
- `frontend/e2e/declared-layer.spec.ts`
- `frontend/src/components/dashboard/AccountRow.css`
- `frontend/src/components/dashboard/BalanceGroup.css`
- `frontend/src/components/dashboard/BalanceLedger.css`
- `frontend/src/routes/BalanceDashboardPage.css`
- `frontend/src/routes/BalanceDashboardPage.tsx`
- `frontend/src/test/runner.test.tsx`
- `task-108-datapack-valid.png`
- `task-108-inventcloud-divergent.png`

## Validações

- Comando: `docker compose run --rm backend-tests`.
  - Resultado: 278 testes aprovados, incluindo reimportação real separada de DATAPACK e INVENTCLOUD.
- Comando: `docker compose run --rm frontend-tests`.
  - Resultado: 27 testes aprovados e build de produção concluído.
- Comando: `docker compose run --rm frontend-e2e`.
  - Resultado: 9 testes Playwright aprovados.
- Comando: reimportações operacionais separadas via API em containers.
  - Resultado: DATAPACK retornou `200`, `reprocessed=true`, parser `2.1.0` e balanço `VALIDO`; INVENTCLOUD retornou `201` por não existir no banco operacional atual, parser `2.1.0` e balanço `DIVERGENTE`. O caminho `200/reprocessed=true` do INVENTCLOUD passou no teste isolado.
- Inspeção: MCP Playwright em 1280x720 para DATAPACK e INVENTCLOUD.
  - Resultado: estados `Válido` e `Divergente`, árvore em duas colunas e trilha de componentes apresentadas sem recalculo ou switches. A única mensagem de console observada foi `404` do `favicon.ico`, sem impacto no fluxo.
- Comando: `alembic current`, busca por `float`/`parseFloat` e `git diff --check`.
  - Resultado: PostgreSQL em `0059_parser_2_1 (head)`, nenhuma ocorrência proibida e nenhuma inconsistência de whitespace.
- Comando: `docker compose --profile test run --rm backend-tests`.
  - Resultado: 279 testes aprovados.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 28 testes aprovados e build de produção concluído.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 9 testes Playwright aprovados.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 29 testes aprovados e build de produção concluído após destacar totalizador problemático sem inserir conta analítica na apresentação principal.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 11 testes Playwright aprovados, incluindo cenário em que a analítica com `Sem saldo I155` aparece destacada apenas no diálogo de auditoria.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 29 testes aprovados e build de produção concluído após alinhamento compartilhado entre macrogrupo e microgrupos do modo `Livro-razão`.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 10 testes Playwright aprovados após impedir quebra de linha em valores monetários no modo `Livro-razão`.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: busca por `parseFloat` e `float(` nos arquivos alterados.
  - Resultado: nenhuma ocorrência encontrada.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 29 testes aprovados e build de produção concluído após realinhamento das colunas do modo `Livro-razão`.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 10 testes Playwright aprovados após ajuste do botão de auditoria no modo `Livro-razão`.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: `docker compose --profile test run --rm backend-tests`.
  - Resultado: 280 testes aprovados, incluindo auditoria de componentes agregados de totalizador.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 29 testes aprovados e build de produção concluído, incluindo auditoria de totalizador.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 10 testes Playwright aprovados, incluindo auditoria de totalizador com componentes analíticos descendentes.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.
- Comando: busca por `parseFloat` e `float(` nos arquivos alterados.
  - Resultado: nenhuma ocorrência encontrada.
- Comando: `docker compose --profile test run --rm frontend-tests`.
  - Resultado: 28 testes aprovados e build de produção concluído após suavização do topo da tela.
- Comando: `docker compose --profile test run --rm frontend-e2e`.
  - Resultado: 9 testes Playwright aprovados após ajuste dos asserts de status único no painel compacto.
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

- INVENTCLOUD permanece objetivamente `DIVERGENTE` porque 19 linhas de detalhe não possuem saldo `I155` correspondente. O sistema mantém a auditoria e bloqueia corretamente o resultado anual final; não é falha de execução da TASK.

## Homologação

- Status: aprovado
- Data: 2026-07-30
- Decisão do usuário: grupo `TASK-101` a `TASK-108` homologado após validações e ajustes finais de UI/auditoria.
- Observação: TASK concluída por homologação consolidada do grupo.
