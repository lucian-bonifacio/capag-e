# TASK-013 - Criar configuracao Docker Compose minima

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-003-criar-estrutura-backend-minima.md`
- `TASK-008-organizar-estrutura-frontend-minima.md`
- `TASK-010-auditar-ambiente-local-e-configuracao.md`

Esta TASK so deve ser executada depois que a auditoria de ambiente local indicar lacunas de configuracao e as estruturas minimas de backend e frontend estiverem prontas ou explicitamente dispensadas.

## Objetivo

Criar uma configuracao minima de Docker Compose como unico ambiente oficial do CAPAG, contemplando PostgreSQL e pontos de extensao para backend/frontend, sem implementar servicos funcionais alem do necessario para a fundacao estrutural.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-010-auditoria-ambiente-local.md`

## Escopo Exato

- Criar `docker-compose.yml` minimo quando a TASK-010 indicar ausencia ou insuficiencia.
- Incluir servico PostgreSQL 16 conforme arquitetura.
- Preparar a base para backend, frontend, testes, build, migrations e validacoes executarem via `docker compose`.
- Definir volumes locais nomeados para dados do PostgreSQL.
- Definir variaveis de ambiente apenas por nomes e valores locais nao sensiveis ou placeholders seguros.
- Documentar como o backend e o frontend serao acoplados em TASKs futuras, se ainda nao houver Dockerfiles.
- Garantir que arquivos `.env` reais nao sejam lidos, criados ou alterados.

## Fora De Escopo

- Criar Dockerfile de backend.
- Criar Dockerfile de frontend.
- Criar arquivo `.env`.
- Ler arquivo `.env`.
- Criar `.venv`.
- Criar `node_modules` no host.
- Instalar Python, Node ou dependencias no host.
- Configurar secrets reais.
- Criar migrations.
- Criar banco, tabelas ou modelos SQLAlchemy.
- Criar endpoints.
- Instalar dependencias.
- Alterar backend ou frontend.
- Configurar CI.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `tasks/reports/TASK-010-auditoria-ambiente-local.md`.
2. Confirmar que a lacuna de Docker Compose foi registrada.
3. Criar `docker-compose.yml` minimo.
4. Incluir PostgreSQL 16 com volume nomeado.
5. Usar somente variaveis locais nao sensiveis ou placeholders seguros.
6. Registrar comentarios ou README curto apenas se necessario para explicar acoplamento futuro de backend/frontend.
7. Validar que nenhum `.env`, Dockerfile, backend, frontend, migration ou CI foi criado ou alterado.

## Arquivos Ou Areas Provaveis

- `docker-compose.yml`
- `README.md` apenas se a TASK-010 indicar necessidade documental local especifica

## Criterios De Aceite

- A TASK-010 foi executada antes desta TASK.
- `docker-compose.yml` existe.
- O Compose inclui PostgreSQL 16.
- O Compose e tratado como unico ambiente oficial do projeto.
- O Compose usa volume nomeado para dados do PostgreSQL.
- Nenhuma dependencia e instalada ou exigida no host.
- Nao ha secrets reais no arquivo criado.
- Nenhum arquivo `.env` e lido, criado ou alterado.
- Nenhum Dockerfile e criado nesta TASK.
- Nenhum codigo backend ou frontend e alterado.
- Nenhuma migration, modelo ou endpoint e criado.

## Validacao Esperada

- Executar `test -f docker-compose.yml`.
- Executar `docker compose config`, se Docker estiver disponivel no ambiente.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas ao arquivo de configuracao permitido.
- Conferir manualmente que nao ha segredo real e que nenhum `.env` foi lido, criado ou alterado.

## Riscos

- Risco: configurar ambiente antes de backend/frontend estarem prontos.
  Mitigacao: manter Compose minimo e registrar pontos de extensao futuros.

- Risco: vazar segredo em configuracao versionada.
  Mitigacao: usar apenas placeholders seguros e nao ler arquivos `.env`.

- Risco: transformar Compose em implementacao de infraestrutura completa.
  Mitigacao: limitar a TASK ao ambiente local minimo definido pela arquitetura.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 003, 008 e 010, ou ate decisao explicita dispensar uma dessas dependencias.

Permanece bloqueado qualquer trabalho que tente criar Dockerfiles, secrets, `.env`, `.venv`, `node_modules` no host, instalacao local/global, migrations, banco definitivo, endpoints, backend funcional, frontend funcional ou CI durante esta TASK.
