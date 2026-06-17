# TASK-014 - Configurar testes backend minimos

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-003-criar-estrutura-backend-minima.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`

Esta TASK so deve ser executada depois que a estrutura backend minima existir e a auditoria de validacoes indicar a lacuna ou insuficiencia de testes backend.

## Objetivo

Configurar a base minima de testes backend com `pytest` executando via Docker Compose, sem criar testes funcionais de dominio prudencial, endpoints reais, banco definitivo, migrations ou golden cases.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-006-auditoria-validacoes.md`

## Escopo Exato

- Criar estrutura minima de testes backend, quando a TASK-006 indicar lacuna.
- Criar configuracao minima de `pytest`, se ainda nao existir.
- Criar um teste sentinela nao funcional para validar que o runner executa.
- Documentar comando esperado para execucao dos testes backend via `docker compose`.
- Garantir que nenhum teste prudencial, de parser ECD, engine, API funcional, banco ou exportacao seja criado nesta TASK.
- Garantir que `.venv` local nao seja criado ou exigido.

## Fora De Escopo

- Criar testes de dominio prudencial.
- Criar golden cases.
- Criar fixtures contabeis.
- Criar testes de parser ECD.
- Criar testes de API funcional.
- Criar testes de banco, repositories ou migrations.
- Criar modelos, schemas, endpoints ou engines.
- Instalar dependencias no host.
- Criar ou exigir `.venv`.
- Alterar frontend.
- Configurar CI.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `tasks/reports/TASK-006-auditoria-validacoes.md`.
2. Confirmar que a lacuna de testes backend foi registrada.
3. Verificar a estrutura backend criada pela TASK-003.
4. Criar diretorio de testes backend minimo.
5. Criar configuracao minima de `pytest`, se necessaria.
6. Criar teste sentinela que nao exerca regra funcional.
7. Documentar comando de execucao em local apropriado, se a auditoria indicar ausencia documental.
8. Validar que nenhum teste funcional, prudencial, de API, banco, parser, engine, exportacao ou laudo foi criado.

## Arquivos Ou Areas Provaveis

- `backend/tests/`
- `backend/pytest.ini` ou configuracao equivalente, se necessaria
- `backend/README.md`, somente se a auditoria indicar necessidade de documentar comando

## Criterios De Aceite

- A TASK-006 foi executada antes desta TASK.
- Existe estrutura minima para testes backend.
- `pytest` consegue descobrir e executar o teste sentinela.
- O teste sentinela nao valida regra de negocio.
- Nenhum teste prudencial, fixture contabil, golden case, endpoint, parser, engine, banco, exportacao ou laudo e criado.
- Nenhum arquivo de frontend e alterado.
- CI nao e configurado nesta TASK.

## Validacao Esperada

- Executar o comando backend de `pytest` definido pela TASK via `docker compose`.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas a configuracao/testes backend minimos permitidos.
- Conferir manualmente que o teste criado e apenas sentinela e nao define comportamento funcional.
- Conferir manualmente que nenhuma dependencia foi instalada no host e que `.venv` nao foi criado.

## Riscos

- Risco: teste sentinela virar contrato funcional indevido.
  Mitigacao: limitar o teste a verificacao do runner, sem importar regra de dominio.

- Risco: criar golden cases antes de SPEC funcional suficiente.
  Mitigacao: bloquear golden cases nesta TASK.

- Risco: acoplar testes backend a banco ou API antes do scaffolding adequado.
  Mitigacao: nao criar testes de banco, API ou repositories nesta TASK.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 003 e 006.

Permanece bloqueado qualquer trabalho que tente criar testes funcionais, prudenciais, golden cases, fixtures contabeis, endpoints, schemas, models, migrations, parser, engine, exportacao, laudo, `.venv` ou instalacao de dependencia no host durante esta TASK.
