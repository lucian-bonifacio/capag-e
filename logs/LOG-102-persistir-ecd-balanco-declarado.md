# LOG - TASK-102 - Persistir ECD e balanço declarado

## Referência

- Task: `tasks/TASK-102-persistir-ecd-balanco-declarado.md`
- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- Status: aguardando_homologacao

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Execução

- Data: 2026-07-29
- Ação: persistência e migration implementadas.
- Resumo: bytes originais, hash, tamanho, versão do parser e registros `I010/I030/I052/I150/J005/J100/J150` passaram a ser persistidos atomicamente com relacionamentos formais.
- Ajuste: a primeira aplicação da migration excedeu o limite do identificador Alembic; o identificador foi reduzido e a migration reaplicada com sucesso.
- Data: 2026-07-29
- Ação: ajuste de homologação.
- Resumo: a importação passou a executar pré-validação do balanço antes da persistência. Estados `OBRIGATORIO_AUSENTE`, `NAO_OBRIGATORIO` e `ESTRUTURA_INVALIDA` rejeitam a ECD sem criar análise ou ECD operacional; `DIVERGENTE` continua persistindo para diagnóstico.

## Arquivos Alterados

- `backend/alembic/versions/0056_balance_declared_persistence.py`
- `backend/app/repositories/ecd_imports.py`
- `backend/app/application/ecd_import_service.py`
- `backend/app/api/imports.py`
- `backend/app/domain/imports.py`
- `backend/app/schemas/imports.py`
- `backend/tests/`
- `backend/app/application/ecd_balance_preflight.py`

## Validações

- Comando: testes focados de modelos, persistência e API via `docker compose`.
  - Resultado: 9 testes aprovados.
- Comando: migration e `alembic current` via `docker compose`.
  - Resultado: PostgreSQL em `0056_balance_declared (head)`.
- Comando: `docker compose --profile test run --rm backend-tests`.
  - Resultado: 246 testes aprovados.
- Validação: hash recalculado dos bytes persistidos, busca por `float` e `git diff --check`.
  - Resultado: conteúdo idêntico e nenhuma inconsistência.
- Comando: `docker compose --profile test run --rm backend-tests`.
  - Resultado: 279 testes aprovados.
- Comando: `git diff --check`.
  - Resultado: aprovado, sem inconsistência de whitespace.

## Pendências Ou Bloqueios

- Nenhum.

## Homologação

- Status: aguardando_homologacao
- Data: 2026-07-29
- Decisão do usuário: execução em grupo autorizada para `TASK-101` a `TASK-108`.
- Observação: continuidade automática para a `TASK-103`.
