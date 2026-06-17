# TASK-006 - Auditar validacoes minimas do projeto

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`
- `TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`

Esta TASK so deve ser executada depois que a estrutura minima e o estado das SPECs estiverem auditados.

## Objetivo

Auditar quais validacoes documentais e tecnicas minimas existem ou faltam no projeto, preparando TASKs futuras para testes, build, migrations, assets metodologicos e CI sem configurar ferramentas nesta etapa.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`
- relatorio esperado de `tasks/reports/TASK-005-auditoria-specs.md`

## Escopo Exato

- Auditar se existem comandos ou configuracoes para:
  - testes backend com `pytest`;
  - validacao de migrations com Alembic;
  - build frontend;
  - testes frontend com Vitest;
  - fluxos criticos com Playwright;
  - validacao de assets metodologicos;
  - CI com GitHub Actions.
- Auditar se comandos existentes executam via Docker/Docker Compose.
- Auditar se ha qualquer validacao que exija `.venv`, `node_modules` no host, Python local, Node local ou instalacao global/local fora de container.
- Registrar o que existe, o que falta e o que depende de scaffolding futuro.
- Separar validacoes documentais de validacoes tecnicas.
- Propor proximas TASKs pequenas para configurar validacoes ausentes.

## Fora De Escopo

- Criar ou alterar testes.
- Instalar dependencias.
- Criar configuracao de `pytest`, Alembic, Vitest, Playwright ou GitHub Actions.
- Criar workflow de CI.
- Criar assets metodologicos.
- Implementar backend ou frontend.
- Definir golden cases prudenciais.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os relatorios das TASKs 002 e 005.
2. Verificar arquivos de configuracao existentes na raiz, `backend/`, `frontend/` e `.github/`, se existirem.
3. Verificar se ha comandos documentados para testes, build, migrations e validacao de assets.
4. Criar relatorio em `tasks/reports/TASK-006-auditoria-validacoes.md`.
5. Classificar cada validacao como:
   - existente;
   - ausente;
   - dependente de scaffolding;
   - bloqueada por SPEC posterior.
6. Sugerir proximas TASKs pequenas para validacoes ausentes ou dependentes.
7. Validar que nenhum arquivo de configuracao ou codigo foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-006-auditoria-validacoes.md`
- raiz do repositorio apenas para leitura
- `backend/` apenas para leitura, se existir
- `frontend/` apenas para leitura
- `.github/` apenas para leitura, se existir

## Criterios De Aceite

- Existe relatorio em `tasks/reports/TASK-006-auditoria-validacoes.md`.
- O relatorio cobre todas as validacoes listadas no escopo.
- O relatorio identifica se as validacoes existentes respeitam ambiente oficial Docker-only.
- O relatorio registra exigencia de `.venv`, `node_modules` no host ou instalacao fora de container como lacuna.
- Cada validacao possui status objetivo.
- O relatorio separa lacunas documentais de lacunas tecnicas.
- O relatorio sugere TASKs futuras pequenas e independentes.
- Nenhum teste, workflow, config, backend, frontend ou asset e criado ou alterado.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-006-auditoria-validacoes.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `tasks/reports/TASK-006-auditoria-validacoes.md`.
- Conferir manualmente que o relatorio nao cria configuracao, teste, CI, asset ou regra prudencial.

## Riscos

- Risco: auditoria virar configuracao prematura de ferramentas.
  Mitigacao: registrar lacunas e propor TASKs futuras, sem configurar nada nesta TASK.

- Risco: exigir testes antes de existir scaffolding minimo.
  Mitigacao: classificar como `dependente de scaffolding` quando aplicavel.

- Risco: criar golden cases sem SPEC funcional suficiente.
  Mitigacao: bloquear golden cases prudenciais ate SPEC funcional correspondente.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 002 e 005.

Permanece bloqueado qualquer trabalho que tente criar testes, configurar CI, instalar dependencias, criar assets metodologicos ou definir golden cases prudenciais durante esta TASK.
