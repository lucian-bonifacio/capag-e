# TASK-087 - Tratar contas sem vinculo referencial

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041D-implementar-parser-ecd-declarado.md`
- `TASK-041E-persistir-ecd-normalizada.md`
- `TASK-041G-executar-camada-declarada-ecd-importada.md`
- `TASK-085-refinar-apresentacao-leitura-declarada.md`
- `TASK-086-tabela-oficial-referencial-obrigatoria.md`

## Objetivo

Tratar contas sem vinculo referencial de forma util para analise, separando contas estruturais de contas analiticas/materialmente relevantes e deixando claro quando a pendencia vem do arquivo ECD.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `tasks/TASK-085-refinar-apresentacao-leitura-declarada.md`

## Escopo Exato

- Identificar contas sem `I051` que recebem status `SEM_VINCULO_REFERENCIAL`.
- Diferenciar contas estruturais/sinteticas de contas analiticas com saldo ou movimento.
- Tratar contas estruturais sem vinculo como contexto de hierarquia, sem poluir a lista principal de pendencias.
- Destacar contas analiticas sem vinculo com valor base ou movimento relevante.
- Criar resumo especifico de `SEM_VINCULO_REFERENCIAL`, separando total estrutural e total acionavel.
- Ajustar UI para comunicar que ausencia de vinculo referencial e pendencia do arquivo ECD, nao falha da tabela oficial.
- Criar detalhe por conta sem vinculo com dados disponiveis: `I050`, saldo `I155`, movimentos quando disponiveis e ausencia de `I051`.
- Manter comportamento conservador: nao inferir codigo referencial por nome, prefixo, hierarquia ou saldo.
- Criar testes para conta sintetica sem vinculo, conta analitica sem vinculo e conta com vinculo normal.

## Fora De Escopo

- Corrigir automaticamente ECD sem `I051`.
- Criar vinculo referencial manual ou editor de vinculos.
- Inferir `COD_CTA_REF` por nome, prefixo, grupo ou comportamento.
- Alterar regra prudencial, metodologia interna ou matcher.
- Criar camada reclassificada/comportamental.
- Alterar tabela oficial do plano referencial.

## Passos Executaveis

1. Ler parser, persistencia e resultado da camada declarada para contas sem `I051`.
2. Definir criterio operacional para conta estrutural/sintetica versus analitica usando dados ja persistidos.
3. Ajustar backend ou frontend para expor/apresentar a separacao sem recalcular regra prudencial.
4. Ajustar resumo e filtros da tela declarada para `SEM_VINCULO_REFERENCIAL`.
5. Criar detalhe por conta sem vinculo referencial.
6. Criar testes backend/frontend conforme o ponto de implementacao escolhido.
7. Validar que nenhuma conta sem vinculo recebe codigo inferido.
8. Validar manualmente com `DATAPACK` e `INVENTCLOUD` em execucoes separadas.

## Arquivos Ou Areas Provaveis

- `backend/app/application/declared_run_service.py`
- `backend/app/schemas/declared.py`
- `backend/app/api/declared.py`
- `backend/tests/`
- `frontend/src/routes/DeclaredLayerPage.tsx`
- `frontend/src/api/declared.ts`
- `frontend/src/App.css`
- `frontend/src/test/runner.test.tsx`
- `frontend/e2e/declared-layer.spec.ts`

## Criterios De Aceite

- Contas sem vinculo referencial deixam de aparecer como massa indistinta na tabela principal.
- A tela separa contas estruturais sem vinculo de contas analiticas acionaveis.
- O usuario consegue entender se a pendencia vem da ECD e nao da tabela oficial.
- Contas analiticas sem vinculo e materialidade ficam destacadas como pendencia de revisao.
- Nenhum `COD_CTA_REF` e inferido automaticamente.
- Frontend nao recalcula regra prudencial nem altera status retornado pelo backend.
- DATAPACK e INVENTCLOUD continuam abrindo e exibindo leitura declarada.

## Validacao Esperada

- Executar testes backend via `docker compose`, se houver alteracao de API/backend.
- Executar testes frontend via `docker compose`.
- Executar E2E Playwright via Docker Compose.
- Validar manualmente `docs/reference/ecd-example/ECD 2024 DATAPACK.txt`.
- Validar manualmente `docs/reference/ecd-example/ECD 2024 INVENTCLOUD.txt`.
- Conferir ausencia de `float` em arquivos alterados.

## Riscos

- Risco: esconder conta sem vinculo que deveria ser revisada.
  Mitigacao: manter modo de pendencias acionaveis e contadores separados.

- Risco: usuario interpretar ausencia de vinculo como erro do sistema.
  Mitigacao: texto e detalhe devem indicar que o vinculo `I051` vem da ECD.

- Risco: solucao tentar inferir codigo referencial.
  Mitigacao: criterio de aceite proibe inferencia automatica.

## Bloqueios Pendentes

Nenhum.
