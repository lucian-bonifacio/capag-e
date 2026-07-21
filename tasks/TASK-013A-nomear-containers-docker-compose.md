# TASK-013A - Nomear containers Docker Compose

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-013-criar-configuracao-docker-compose-minima.md`

## Objetivo

Ajustar a configuracao Docker Compose oficial para que os containers principais aparecam com nomes previsiveis em comandos operacionais como `docker ps`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/TASK-013-criar-configuracao-docker-compose-minima.md`

## Escopo Exato

- Definir nomes explicitos para os containers dos servicos `backend`, `frontend` e `postgres`.
- Preservar os nomes dos servicos Compose existentes.
- Preservar imagens, comandos, portas, volumes, variaveis locais nao sensiveis, profiles e healthchecks existentes.
- Validar que `docker compose config` permanece valido.
- Validar que `docker ps` mostra nomes previsiveis para backend, frontend e banco de dados quando os servicos estiverem em execucao.

## Fora De Escopo

- Alterar imagem, versao de runtime ou banco de dados.
- Alterar porta publicada.
- Alterar credenciais locais nao sensiveis ja existentes.
- Criar ou alterar `.env`.
- Ler arquivos `.env`.
- Criar Dockerfile.
- Criar scripts novos.
- Alterar backend, frontend, migrations, testes ou CI.
- Instalar dependencias no host.
- Alterar qualquer regra de dominio, API ou comportamento funcional do produto.

## Passos Executaveis

1. Ler `docker-compose.yml` atual.
2. Definir `container_name` para `backend`, `frontend` e `postgres` usando nomes claros do projeto.
3. Executar `docker compose config` via ambiente oficial.
4. Subir os servicos principais via `docker compose`.
5. Conferir `docker ps` e registrar os nomes observados.
6. Confirmar que a alteracao ficou restrita ao `docker-compose.yml`, log e roadmap.

## Arquivos Ou Areas Provaveis

- `docker-compose.yml`
- `logs/LOG-013A-nomear-containers-docker-compose.md`
- `ROADMAP.md`

## Criterios De Aceite

- `backend`, `frontend` e `postgres` possuem nomes de container explicitos.
- `docker compose config` executa sem erro.
- `docker ps` exibe nomes previsiveis para backend, frontend e banco de dados.
- Nenhum arquivo `.env` e lido, criado ou alterado.
- Nenhuma dependencia e instalada ou exigida no host.
- Nenhum codigo backend, frontend, teste, migration ou CI e alterado.

## Validacao Esperada

- Executar `COMPOSE_DISABLE_ENV_FILE=1 docker compose config`.
- Executar `COMPOSE_DISABLE_ENV_FILE=1 docker compose up -d postgres backend frontend`.
- Executar `docker ps --format '{{.Names}}'` e conferir os nomes dos containers principais.
- Executar `git diff --stat` e confirmar escopo restrito.

## Riscos

- Risco: nomes fixos de container conflitarem com containers existentes.
  Mitigacao: usar nomes claros e especificos do projeto CAPAG e registrar qualquer conflito como bloqueio.

- Risco: alterar Compose alem da identificacao operacional.
  Mitigacao: limitar a TASK a `container_name` nos servicos principais.

## Bloqueios Pendentes

Nenhum.
