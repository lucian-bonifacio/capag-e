# TASK-003 - Criar estrutura backend minima

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`

Esta TASK so deve ser executada depois que a TASK-002 registrar a ausencia ou insuficiencia da estrutura `backend/`.

## Objetivo

Criar a estrutura minima de diretorios do backend conforme a arquitetura aprovada, sem implementar endpoints funcionais, regras de dominio, motores, persistencia definitiva ou contratos de API finais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`

## Escopo Exato

- Criar a pasta `backend/` caso a TASK-002 confirme que ela esta ausente.
- Criar a estrutura inicial de pacotes prevista pela arquitetura:
  - `backend/app/api/`;
  - `backend/app/application/`;
  - `backend/app/domain/`;
  - `backend/app/io/`;
  - `backend/app/engine/`;
  - `backend/app/repositories/`;
  - `backend/app/export/`;
  - `backend/app/report/`;
  - `backend/app/assets/`.
- Criar apenas arquivos sentinela ou `__init__.py` quando necessario para manter os pacotes versionaveis.
- Registrar em README curto do backend que as responsabilidades seguem `docs/architecture.md` e `SPEC-001`.

## Fora De Escopo

- Criar rotas FastAPI funcionais.
- Criar schemas Pydantic.
- Criar modelos SQLAlchemy.
- Criar migrations Alembic.
- Criar parser ECD.
- Criar motores de calculo.
- Criar exportacao Excel.
- Criar gerador de laudo.
- Definir regras prudenciais, formulas, politica de arredondamento ou golden cases.
- Alterar frontend.
- Alterar `tasks/README.md`.

## Passos Executaveis

1. Ler `tasks/reports/TASK-002-auditoria-estrutura-minima.md`.
2. Confirmar que a estrutura `backend/` esta ausente ou insuficiente.
3. Criar `backend/`.
4. Criar os subdiretorios de camada definidos no escopo.
5. Adicionar arquivos minimos para versionamento dos pacotes, sem logica funcional.
6. Criar `backend/README.md` com responsabilidades por camada e proibicoes de recalculo fora do motor.
7. Validar que nenhum endpoint, schema, modelo, migration ou regra funcional foi criado.

## Arquivos Ou Areas Provaveis

- `backend/README.md`
- `backend/app/api/`
- `backend/app/application/`
- `backend/app/domain/`
- `backend/app/io/`
- `backend/app/engine/`
- `backend/app/repositories/`
- `backend/app/export/`
- `backend/app/report/`
- `backend/app/assets/`

## Criterios De Aceite

- A TASK-002 foi executada antes desta TASK.
- `backend/` existe.
- As pastas de camada previstas no escopo existem.
- `backend/README.md` cita `docs/architecture.md` e `SPEC-001` como fontes de responsabilidade.
- Nenhum endpoint funcional e criado.
- Nenhum schema Pydantic funcional e criado.
- Nenhum modelo SQLAlchemy ou migration e criado.
- Nenhuma regra prudencial, formula ou politica de arredondamento e definida.
- Nenhum arquivo de frontend e alterado.

## Validacao Esperada

- Executar `test -d backend`.
- Executar `test -d backend/app/api`.
- Executar `test -d backend/app/application`.
- Executar `test -d backend/app/domain`.
- Executar `test -d backend/app/io`.
- Executar `test -d backend/app/engine`.
- Executar `test -d backend/app/repositories`.
- Executar `test -d backend/app/export`.
- Executar `test -d backend/app/report`.
- Executar `test -d backend/app/assets`.
- Executar `test -f backend/README.md`.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas a `backend/`.

## Riscos

- Risco: scaffolding virar implementacao funcional antecipada.
  Mitigacao: limitar a TASK a diretorios, arquivos sentinela e README de responsabilidades.

- Risco: criar contratos de API sem SPEC funcional suficiente.
  Mitigacao: bloquear rotas, schemas e endpoints nesta TASK.

- Risco: duplicar regra prudencial fora do motor.
  Mitigacao: registrar no README do backend as fronteiras de responsabilidade definidas pela arquitetura.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-002.

Permanece bloqueado qualquer trabalho que tente criar endpoint funcional, schema de API, modelo persistente, migration, parser, engine, exportacao ou regra prudencial nesta TASK.
