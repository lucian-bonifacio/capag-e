# TASK-010 - Auditar ambiente local e configuracao

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`

Esta TASK so deve ser executada depois que a estrutura minima e as validacoes minimas estiverem auditadas.

## Objetivo

Auditar se o projeto possui configuracao suficiente para ambiente local governado e exclusivamente baseado em Docker Compose, considerando PostgreSQL, backend, frontend, variaveis de ambiente e comandos de desenvolvimento, sem criar ou alterar configuracoes nesta etapa.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`
- relatorio esperado de `tasks/reports/TASK-006-auditoria-validacoes.md`

## Escopo Exato

- Auditar se existem arquivos ou convencoes para ambiente local:
  - `docker-compose.yml` ou equivalente;
  - Dockerfile de backend, se aplicavel;
  - Dockerfile de frontend, se aplicavel;
  - configuracao local de PostgreSQL;
  - exemplo de variaveis de ambiente sem segredos;
  - comandos documentados para subir backend e frontend;
  - comandos documentados para testes e build.
- Auditar se os comandos oficiais usam `docker compose`.
- Auditar se ha qualquer exigencia indevida de `.venv`, `node_modules` no host, Python local, Node local, `pip` local ou package manager Node local.
- Verificar se a configuracao existente preserva a restricao de nao versionar segredos.
- Registrar lacunas em relatorio documental.
- Propor proximas TASKs pequenas para criar configuracao local quando houver lacunas.

## Fora De Escopo

- Criar `docker-compose.yml`.
- Criar Dockerfiles.
- Criar ou alterar arquivos `.env`.
- Ler arquivos `.env`.
- Criar exemplo de `.env`.
- Criar `.venv`.
- Criar `node_modules`.
- Instalar dependencias no host.
- Configurar PostgreSQL.
- Criar migrations.
- Instalar dependencias.
- Alterar scripts de package manager.
- Alterar backend, frontend, testes ou CI.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os relatorios das TASKs 002 e 006.
2. Verificar arquivos de configuracao existentes na raiz do repositorio.
3. Verificar configuracoes existentes em `backend/` e `frontend/`, se existirem.
4. Verificar se existem exemplos seguros de variaveis de ambiente, sem ler arquivos `.env`.
5. Verificar se ha comandos documentados para execucao local.
6. Criar relatorio em `tasks/reports/TASK-010-auditoria-ambiente-local.md`.
7. Registrar lacunas sem corrigi-las.
8. Classificar lacunas como documentais, estruturais, tecnicas ou bloqueadas por TASK anterior.
9. Sugerir proximas TASKs pequenas para configuracao local.
10. Validar que nenhum arquivo de configuracao, codigo, teste ou segredo foi criado ou alterado.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-010-auditoria-ambiente-local.md`
- raiz do repositorio apenas para leitura
- `backend/` apenas para leitura, se existir
- `frontend/` apenas para leitura
- `.github/` apenas para leitura, se existir

## Criterios De Aceite

- Existe relatorio em `tasks/reports/TASK-010-auditoria-ambiente-local.md`.
- O relatorio cita a SPEC de origem.
- O relatorio informa se ha configuracao local para Docker Compose, PostgreSQL, backend e frontend.
- O relatorio informa se existem comandos documentados de desenvolvimento.
- O relatorio informa se o ambiente oficial esta restrito a Docker/Docker Compose.
- O relatorio registra qualquer exigencia de `.venv`, `node_modules` no host ou instalacao local/global como lacuna.
- O relatorio registra lacunas sem corrigi-las.
- O relatorio sugere TASKs futuras pequenas quando houver lacunas.
- Nenhum arquivo `.env` e lido, criado ou alterado.
- Nenhum arquivo de configuracao, codigo, teste ou CI e criado ou alterado.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-010-auditoria-ambiente-local.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `tasks/reports/TASK-010-auditoria-ambiente-local.md`.
- Conferir manualmente que nenhum arquivo `.env` foi lido, criado ou alterado.
- Conferir manualmente que o relatorio nao cria configuracao local nem define comando novo como aprovado.

## Riscos

- Risco: auditoria virar configuracao prematura de ambiente.
  Mitigacao: registrar lacunas e propor TASKs futuras, sem criar arquivos de configuracao nesta TASK.

- Risco: expor segredo ao auditar ambiente.
  Mitigacao: nao ler arquivos `.env` e considerar apenas exemplos seguros ou documentacao sem segredos.

- Risco: criar configuracao local antes de estrutura backend/frontend suficiente.
  Mitigacao: classificar lacunas como dependentes de TASK anterior quando aplicavel.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 002 e 006.

Permanece bloqueado qualquer trabalho que tente criar Docker Compose, Dockerfile, `.env`, exemplo de ambiente, `.venv`, `node_modules`, scripts de execucao, configuracao de banco, migration, CI ou instalacao de dependencia no host durante esta TASK.
