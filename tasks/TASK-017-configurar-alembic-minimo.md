# TASK-017 - Configurar Alembic minimo

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-003-criar-estrutura-backend-minima.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`
- `TASK-010-auditar-ambiente-local-e-configuracao.md`
- `TASK-013-criar-configuracao-docker-compose-minima.md`

Esta TASK so deve ser executada depois que a estrutura backend minima existir, o ambiente local estiver definido e a auditoria de validacoes indicar a lacuna ou insuficiencia de migrations.

## Objetivo

Configurar a base minima do Alembic para migrations futuras executando via container backend, sem criar modelos de dominio, tabelas definitivas, migrations funcionais ou contratos persistentes de modulos prudenciais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- log esperado de `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`
- log esperado de `logs/LOG-010-auditar-ambiente-local-e-configuracao.md`

## Escopo Exato

- Criar estrutura minima do Alembic quando a auditoria indicar lacuna.
- Configurar apenas o necessario para o Alembic reconhecer o projeto backend.
- Documentar comando minimo para validar configuracao de migrations via `docker compose`.
- Garantir que nenhuma migration funcional seja criada nesta TASK.
- Garantir que nenhum modelo SQLAlchemy definitivo seja criado nesta TASK.
- Garantir que `.venv` local nao seja criado ou exigido.

## Fora De Escopo

- Criar tabelas.
- Criar modelos SQLAlchemy de dominio.
- Criar migration inicial funcional.
- Criar entidades de empresa, ECD, metodologia, auditoria, evidencias, exportacao ou laudo.
- Criar repositories.
- Criar conexao transacional de aplicacao.
- Criar endpoints.
- Criar testes de banco.
- Definir contratos persistentes de modulos funcionais.
- Definir regra prudencial, formula, arredondamento ou golden cases.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os logs das TASKs 006 e 010.
2. Confirmar que a lacuna de Alembic/migrations foi registrada.
3. Verificar a estrutura backend criada pela TASK-003.
4. Verificar a configuracao local criada pela TASK-013.
5. Criar estrutura minima do Alembic.
6. Configurar o Alembic para apontar para o backend sem criar modelos funcionais.
7. Documentar comando minimo de validacao, se a auditoria indicar ausencia documental.
8. Validar que nenhuma migration funcional, modelo, tabela, repository ou endpoint foi criado.

## Arquivos Ou Areas Provaveis

- `backend/alembic.ini` ou equivalente
- `backend/alembic/`
- `backend/README.md`, somente se a auditoria indicar necessidade de documentar comando

## Criterios De Aceite

- As TASKs 003, 006, 010 e 013 foram executadas antes desta TASK.
- Estrutura minima do Alembic existe.
- Comando minimo de validacao de migrations esta documentado quando necessario.
- Nenhuma migration funcional e criada.
- Nenhum modelo SQLAlchemy definitivo e criado.
- Nenhuma tabela, repository, endpoint, engine ou regra de dominio e criado.
- Nenhum arquivo de frontend e alterado.

## Validacao Esperada

- Executar comando minimo de Alembic definido pela TASK, sem aplicar migrations funcionais.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas a configuracao minima do Alembic permitida.
- Conferir manualmente que nao ha migration funcional, modelo SQLAlchemy definitivo, tabela, repository ou endpoint.
- Conferir manualmente que o comando oficial usa `docker compose` e nao `.venv`.

## Riscos

- Risco: configuracao de migration virar modelagem prematura de banco.
  Mitigacao: bloquear modelos, tabelas e migrations funcionais nesta TASK.

- Risco: criar contrato persistente antes das SPECs funcionais.
  Mitigacao: manter Alembic apenas como infraestrutura minima.

- Risco: acoplar configuracao a segredo local.
  Mitigacao: nao ler nem criar `.env` e usar apenas placeholders seguros ja definidos em TASK anterior.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 003, 006, 010 e 013.

Permanece bloqueado qualquer trabalho que tente criar migration funcional, modelo SQLAlchemy definitivo, tabela, repository, endpoint, teste de banco, contrato persistente funcional, regra prudencial, `.venv` ou instalacao de dependencia no host durante esta TASK.
