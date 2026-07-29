# LOG - TASK-108 - Validar fluxo do balanço declarado

## Referência

- Task: `tasks/TASK-108-validar-fluxo-balanco-declarado.md`
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- Status: aguardando_homologacao

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

## Arquivos Alterados

- `backend/alembic/versions/0059_parser_2_1_reimport.py`
- `backend/app/io/ecd_parser.py`
- `backend/tests/fixtures/ecd/README.md`
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

## Pendências Ou Bloqueios

- INVENTCLOUD permanece objetivamente `DIVERGENTE` porque 19 linhas de detalhe não possuem saldo `I155` correspondente. O sistema mantém a auditoria e bloqueia corretamente o resultado anual final; não é falha de execução da TASK.

## Homologação

- Status: aguardando_homologacao
- Data: 2026-07-29
- Decisão do usuário: homologação adiada para a próxima sessão.
- Observação: a retomada consolidada foi transferida para `logs/LOG-ESPECIAL-retomada-homologacao-spec-012.md`.
