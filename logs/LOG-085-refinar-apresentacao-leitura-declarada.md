# LOG - TASK-085 - Refinar apresentacao da leitura declarada

## Referência

- Task: `tasks/TASK-085-refinar-apresentacao-leitura-declarada.md`
- SPEC: `specs/SPEC-002-modulo-1-camada-declarada.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Execução

- Data: 2026-07-08
- Ação: refinamento da tela de leitura declarada.
- Resumo: a tela passou a exibir resumo acionavel, filtros por status, pendencias por materialidade, labels legiveis, agrupamento hierarquico recolhivel e detalhe por conta separando declaracao ECD de cobertura metodologica.
- Data: 2026-07-08
- Ação: ajuste solicitado em homologacao.
- Resumo: a lista principal foi reorganizada para seguir o padrao visual de `BalanceLedger`/`BalanceGroup` indicado em `docs/frontend/references/balanço.png`, com conta, nome e codigo referencial na esquerda e colunas declaradas/metodologicas compactas a direita.
- Data: 2026-07-08
- Ação: segundo ajuste solicitado em homologacao.
- Resumo: removidos agrupamentos artificiais como `Grupo X`; a leitura declarada passou a renderizar a propria hierarquia de contas, com indentacao por codigo contábil, no formato visual de balanco patrimonial.
- Data: 2026-07-08
- Ação: ajuste de contrato autorizado pelo usuario.
- Resumo: a API de contas declaradas passou a expor metadados hierarquicos do `I050` (`account_type`, `account_level`, `parent_account_code`, `account_order`) e a UI passou a usar esses campos, sem inferir hierarquia por prefixo.
- Data: 2026-07-08
- Ação: ajuste solicitado em homologacao.
- Resumo: o dashboard de balanco passou a montar grupos a partir da arvore formal declarada na ECD (`parent_account_code`, nivel e ordem), deixando de separar macrogrupos por prefixo de codigo. Contas sinteticas como `Ativo Circulante` agora aparecem como grupo uma unica vez, sem repeticao como microgrupo interno.
- Data: 2026-07-08
- Ação: ajuste solicitado em homologacao.
- Resumo: o dashboard passou a exibir apenas uma visao resumida das contas sinteticas declaradas no `I050`, usando o saldo declarado da propria conta/grupo. Contas analiticas deixaram de aparecer na tela principal e permanecem acessiveis pela auditoria, evitando soma local no frontend e classificacao visual por nome ou prefixo.
- Data: 2026-07-08
- Ação: reversao solicitada em homologacao.
- Resumo: revertida a ultima alteracao de layout do dashboard. A tela voltou ao layout anterior com indicadores, alternancia entre duas colunas e livro-razao, preservando o ajuste anterior de evitar repeticao de conta sintetica como microgrupo.
- Data: 2026-07-08
- Ação: ajuste solicitado em homologacao.
- Resumo: mantido o layout anterior do dashboard; a selecao das linhas internas do balanco passou a priorizar as contas sinteticas mais especificas declaradas no `I050` como resumo inteligente. Quando nao houver subgrupo sintetico dentro do macrogrupo, a tela preserva as contas analiticas como fallback para nao ocultar dados declarados.
- Data: 2026-07-08
- Ação: ajuste solicitado em homologacao.
- Resumo: corrigidos valores zerados em linhas sinteticas do resumo. Quando a conta sintetica declarada no `I050` nao possui saldo proprio, o valor apresentado passa a ser a soma das contas analiticas descendentes, preservando o saldo proprio quando ele vier preenchido.
- Data: 2026-07-21
- Ação: ajuste solicitado em homologacao.
- Resumo: o dashboard de balanco patrimonial passou a classificar contas pela natureza declarada no `I050`, expondo `account_nature` pela API. Contas de resultado (`04`) foram excluidas do balanco, os nomes visuais passaram de aplicacoes/origens para Ativo e Passivo + PL, e a tela passou a alertar quando Ativo divergir de Passivo + Patrimonio Liquido.
- Data: 2026-07-21
- Ação: ajuste solicitado em homologacao.
- Resumo: o dashboard de balanco patrimonial passou a consumir valores do ultimo bloco `J100` do exercicio, mantendo a estrutura, natureza, tipo, nivel, conta superior e ordem a partir do `I050`. A rota de auditoria continua usando os snapshots declarados da camada declarada.
- Data: 2026-07-21
- Ação: ajuste solicitado em homologacao.
- Resumo: adicionados apontamentos explicitos de consistencia entre `J100` e `I050` no endpoint e na tela de balanco, cobrindo linhas do `J100` sem conta correspondente no `I050` e contas patrimoniais do `I050` ausentes do ultimo bloco `J100`.

## Arquivos Alterados

- `frontend/src/routes/DeclaredLayerPage.tsx`
- `frontend/src/App.css`
- `frontend/src/test/runner.test.tsx`
- `frontend/e2e/declared-layer.spec.ts`
- `frontend/src/routes/BalanceDashboardPage.tsx`
- `frontend/src/routes/BalanceDashboardPage.css`
- `frontend/src/api/declared.ts`
- `frontend/src/App.tsx`
- `frontend/src/components/dashboard/AccountRow.tsx`
- `frontend/src/components/dashboard/AccountRow.css`
- `frontend/src/components/dashboard/BalanceGroup.tsx`
- `frontend/src/lib/formatters.ts`
- `backend/app/api/declared.py`
- `backend/app/application/declared_service.py`
- `backend/app/schemas/declared.py`
- `backend/tests/test_app_bootstrap.py`
- `backend/tests/test_declared_api.py`
- `backend/tests/test_declared_excel_export.py`
- `backend/tests/test_declared_end_to_end.py`
- `backend/tests/test_declared_run_service.py`

## Validações

- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests`
  - Resultado: 6 testes passaram; build frontend concluido.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 4 testes E2E passaram.
- Comando: `rg -n "\bfloat\b" frontend/src/routes/DeclaredLayerPage.tsx frontend/src/App.css frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests && COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 6 testes frontend passaram, build concluido e 4 testes E2E passaram apos ajuste de homologacao.
- Comando: `rg -n "\bfloat\b" frontend/src/routes/DeclaredLayerPage.tsx frontend/src/App.css frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia apos ajuste.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests`
  - Resultado: 6 testes frontend passaram; build concluido apos remocao dos grupos artificiais.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 4 testes E2E passaram apos remocao dos grupos artificiais.
- Comando: `rg -n "\bfloat\b" frontend/src/routes/DeclaredLayerPage.tsx frontend/src/App.css frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia apos segundo ajuste.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm backend-tests`
  - Resultado: 64 testes backend passaram com o contrato hierarquico do `I050`.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests && COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 6 testes frontend passaram, build concluido e 4 testes E2E passaram.
- Validacao manual: `docs/reference/ecd-example/ECD 2024 DATAPACK.txt`
  - Resultado: API retornou metadados `I050` e tela renderizou hierarquia formal de contas.
- Validacao manual: `docs/reference/ecd-example/ECD 2024 INVENTCLOUD.txt`
  - Resultado: tela renderizou hierarquia formal de contas usando os campos expostos pela API.
- Comando: `rg -n "\bfloat\b" ...`
  - Resultado: ocorrencias apenas em textos governados que proíbem `float`; nenhum uso em codigo alterado.
- Validacao manual: `docs/reference/ecd-example/ECD 2024 DATAPACK.txt`
  - Resultado: tela abriu `analysis-bc7478b47f261603`, 191 contas, com filtros e resumo da leitura declarada.
- Validacao manual: `docs/reference/ecd-example/ECD 2024 INVENTCLOUD.txt`
  - Resultado: tela abriu `analysis-23cd543e13f5b4c7`, 952 contas, com filtros e resumo da leitura declarada.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests`
  - Resultado: 7 testes frontend passaram; build frontend concluido.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 5 testes E2E passaram, incluindo validacao de que `Ativo Circulante` nao se repete como microgrupo quando vem como conta sintetica do `I050`.
- Comando: `rg -n "\bfloat\b|parseFloat" frontend/src/routes/BalanceDashboardPage.tsx frontend/src/components/dashboard/AccountRow.tsx frontend/src/components/dashboard/BalanceGroup.tsx frontend/src/lib/formatters.ts frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests`
  - Resultado: 7 testes frontend passaram; build frontend concluido apos correcao de valores agregados em contas sinteticas.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 5 testes E2E passaram, incluindo validacao de conta sintetica zerada exibindo soma das analiticas descendentes.
- Comando: `rg -n "\bfloat\b|parseFloat" frontend/src/routes/BalanceDashboardPage.tsx frontend/src/components/dashboard/AccountRow.tsx frontend/src/components/dashboard/BalanceGroup.tsx frontend/src/lib/formatters.ts frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests`
  - Resultado: 7 testes frontend passaram; build frontend concluido apos resumo inteligente por contas sinteticas do `I050`.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 5 testes E2E passaram, incluindo validacao de que conta analitica coberta por subgrupo sintetico nao aparece no dashboard principal.
- Comando: `rg -n "\bfloat\b|parseFloat" frontend/src/routes/BalanceDashboardPage.tsx frontend/src/components/dashboard/AccountRow.tsx frontend/src/components/dashboard/BalanceGroup.tsx frontend/src/lib/formatters.ts frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests`
  - Resultado: 7 testes frontend passaram; build frontend concluido apos ajuste para resumo por contas sinteticas.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 5 testes E2E passaram apos ajuste para resumo por contas sinteticas.
- Comando: `rg -n "\bfloat\b|parseFloat|startsWith\(|normalizeText|assetGroups|originGroups|totalAplicacoes|totalOrigens|sumRows|groupTotal|percentageOf|Indicadores Calculados|Liquidez|Endividamento|Poupança" frontend/src/routes/BalanceDashboardPage.tsx frontend/src/components/dashboard/AccountRow.tsx frontend/src/components/dashboard/BalanceGroup.tsx frontend/src/lib/formatters.ts frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia de `float`, `parseFloat`, soma local de grupos, heuristica ativo/passivo ou indicadores mockados no dashboard. A unica ocorrencia de `startsWith` fica no parser decimal de sinal negativo em `frontend/src/lib/formatters.ts`.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests`
  - Resultado: 7 testes frontend passaram; build frontend concluido apos reversao da ultima alteracao de layout.
- Comando: `COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-e2e`
  - Resultado: 5 testes E2E passaram apos reversao da ultima alteracao de layout.
- Comando: `rg -n "\bfloat\b|parseFloat" frontend/src/routes/BalanceDashboardPage.tsx frontend/src/components/dashboard/AccountRow.tsx frontend/src/components/dashboard/BalanceGroup.tsx frontend/src/lib/formatters.ts frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Comando: `docker compose --profile test run --rm backend-tests`
  - Resultado: 64 testes backend passaram apos exposicao de `account_nature` no contrato declarado.
- Comando: `docker compose --profile test run --rm frontend-tests`
  - Resultado: 8 testes frontend passaram; build frontend concluido.
- Comando: `docker compose --profile test run --rm frontend-e2e`
  - Resultado: 6 testes E2E passaram, incluindo exclusao de contas de resultado do balanco e alerta para Ativo diferente de Passivo + PL.
- Comando: `rg -n "\bfloat\b|parseFloat" backend/app/application/declared_service.py backend/app/schemas/declared.py backend/tests/test_declared_api.py backend/tests/test_declared_excel_export.py backend/tests/test_declared_end_to_end.py backend/tests/test_declared_run_service.py frontend/src/api/declared.ts frontend/src/routes/BalanceDashboardPage.tsx frontend/src/routes/BalanceDashboardPage.css frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Comando: `docker compose --profile test run --rm backend-tests`
  - Resultado: 66 testes backend passaram, incluindo contrato do endpoint de balanco por `J100` com metadados/hierarquia do `I050` e selecao do ultimo bloco `J100`.
- Comando: `docker compose --profile test run --rm frontend-tests`
  - Resultado: 8 testes frontend passaram; build frontend concluido consumindo `/declared/balance/accounts` no dashboard.
- Comando: `docker compose --profile test run --rm frontend-e2e`
  - Resultado: 6 testes E2E passaram.
- Validacao manual: `docs/reference/ecd-example/ECD 2024 DATAPACK.txt`
  - Resultado: leitor de balanco retornou 95 linhas do ultimo bloco `J100`; raiz Ativo `5089953.51`, raiz Passivo `5089953.51`, diferenca `0.00`.
- Comando: `rg -n "\bfloat\b|parseFloat" backend/app/application/declared_service.py backend/app/api/declared.py backend/tests/test_app_bootstrap.py backend/tests/test_declared_api.py backend/tests/test_declared_end_to_end.py backend/tests/test_declared_run_service.py frontend/src/App.tsx frontend/src/api/declared.ts frontend/src/routes/BalanceDashboardPage.tsx frontend/src/routes/BalanceDashboardPage.css frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Comando: `docker compose --profile test run --rm backend-tests`
  - Resultado: 66 testes backend passaram apos inclusao dos apontamentos `J100 x I050`.
- Comando: `docker compose --profile test run --rm frontend-tests`
  - Resultado: 9 testes frontend passaram; build frontend concluido com painel de consistencia.
- Comando: `docker compose --profile test run --rm frontend-e2e`
  - Resultado: 7 testes E2E passaram, incluindo exibicao de apontamentos de consistencia `J100 x I050`.
- Validacao manual: `docs/reference/ecd-example/ECD 2024 DATAPACK.txt`
  - Resultado: leitor de balanco reportou 109 apontamentos: 48 `J100_SEM_I050` e 61 `I050_PATRIMONIAL_SEM_J100`.
- Comando: `rg -n "\bfloat\b|parseFloat" backend/app/application/declared_service.py backend/app/schemas/declared.py backend/app/api/declared.py backend/tests/test_declared_api.py backend/tests/test_declared_run_service.py frontend/src/App.tsx frontend/src/api/declared.ts frontend/src/routes/BalanceDashboardPage.tsx frontend/src/routes/BalanceDashboardPage.css frontend/src/test/runner.test.tsx frontend/e2e/declared-layer.spec.ts || true`
  - Resultado: nenhuma ocorrencia.
- Evidencias visuais:
  - `homologacao-task-085-datapack.png`
  - `homologacao-task-085-inventcloud.png`
  - `homologacao-task-085-datapack-ajuste-ledger-final-v2.png`
  - `homologacao-task-085-datapack-hierarquia-contas.png`
  - `homologacao-task-085-inventcloud-hierarquia-contas.png`
  - `homologacao-task-085-datapack-i050-api.png`
  - `homologacao-task-085-inventcloud-i050-api.png`

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aprovada
- Data: 2026-07-21
- Decisao do usuario: aprovacao em grupo das TASKs executadas e homologadas nesta data.
- Observação: reenviada para homologação com valores do balanco patrimonial vindos do ultimo bloco `J100`, hierarquia/metadados do `I050`, exclusao de contas de resultado, alerta apenas quando a composicao do BP nao fechar e painel de apontamentos `J100 x I050`.
