# TASK-013B - Ajustar Docker Compose dev e politica de env

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-013-criar-configuracao-docker-compose-minima.md`
- `TASK-013A-nomear-containers-docker-compose.md`

## Objetivo

Simplificar o ambiente oficial de desenvolvimento via Docker Compose para que `backend` e `frontend` leiam o codigo montado do host em tempo real, sem copias para `/tmp`, e ajustar a politica operacional de `.env` para permitir uso normal do Docker Compose sem exigir `COMPOSE_DISABLE_ENV_FILE=1`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/TASK-013-criar-configuracao-docker-compose-minima.md`
- `tasks/TASK-013A-nomear-containers-docker-compose.md`
- `tasks/README.md`
- `AGENTS.md`
- `README.md`

## Escopo Exato

- Ajustar o servico `frontend` existente para rodar Vite diretamente sobre o diretorio montado do projeto, sem copiar arquivos para `/tmp`.
- Ajustar o servico `backend` existente para rodar FastAPI/Uvicorn em modo desenvolvimento com reload, lendo o codigo montado do projeto, sem copiar arquivos para `/tmp`.
- Manter os mesmos nomes de servicos Compose: `postgres`, `backend`, `frontend`, `backend-tests`, `frontend-tests` e `frontend-e2e`.
- Nao criar servicos `*-dev` adicionais.
- Usar volumes nomeados ou estrategia equivalente para evitar `node_modules`, caches ou artefatos de dependencia no host.
- Preservar execucao de testes, build, migrations e E2E via Docker Compose.
- Atualizar documentos operacionais para permitir comandos oficiais `docker compose` sem `COMPOSE_DISABLE_ENV_FILE=1`.
- Manter `.env` local fora do Git e proibicao de versionar segredos reais.
- Ajustar a regra dos agentes para nao ler nem copiar conteudo de `.env` por conveniencia, sem bloquear o uso normal do Docker Compose.

## Fora De Escopo

- Criar `.env`.
- Criar `.env.example`, salvo se uma decisao governada posterior solicitar.
- Ler conteudo de `.env`.
- Versionar segredo real.
- Alterar credenciais locais nao sensiveis ja existentes no Compose sem necessidade direta.
- Criar Dockerfile.
- Criar novos servicos Compose.
- Alterar contrato de API.
- Alterar regra de dominio, regra prudencial, formula, fonte normativa ou arredondamento.
- Alterar UI, fluxo funcional, migrations de dominio ou comportamento de produto.
- Instalar dependencias Python ou Node no host.

## Passos Executaveis

1. Ler `docker-compose.yml`, `AGENTS.md`, `README.md` e documentos operacionais aplicaveis.
2. Ajustar `docker-compose.yml` para remover copias de `backend` e `frontend` para `/tmp` nos servicos de desenvolvimento.
3. Configurar `backend` com reload de desenvolvimento via Uvicorn, preservando migrations via Compose.
4. Configurar `frontend` com Vite dev server lendo diretamente o volume montado.
5. Garantir que dependencias e caches de desenvolvimento nao sejam criados no host.
6. Atualizar comandos documentados para uso direto de `docker compose`.
7. Atualizar politica operacional de `.env` sem autorizar leitura ou versionamento de segredos.
8. Validar Compose, backend e frontend via ambiente oficial.
9. Confirmar que a alteracao ficou restrita a Compose, documentos operacionais, log e roadmap.

## Arquivos Ou Areas Provaveis

- `docker-compose.yml`
- `AGENTS.md`
- `README.md`
- `tasks/TASK-013A-nomear-containers-docker-compose.md`, apenas se necessario para alinhar validacao pendente.
- `logs/LOG-013B-ajustar-docker-compose-dev-env.md`
- `ROADMAP.md`

## Criterios De Aceite

- `docker compose config` executa sem erro.
- `docker compose up -d postgres backend frontend` sobe o ambiente principal sem exigir `COMPOSE_DISABLE_ENV_FILE=1`.
- Alteracoes em arquivos frontend passam a ser refletidas pelo Vite sem rebuild de imagem e sem copia manual para `/tmp`.
- Alteracoes em arquivos backend passam a acionar reload do Uvicorn sem rebuild de imagem e sem copia manual para `/tmp`.
- Nenhum servico Compose novo e criado.
- Nenhum arquivo `.env` e criado, lido ou versionado durante a execucao da TASK.
- Segredos reais continuam proibidos no repositorio.
- Nenhuma dependencia e instalada ou exigida no host.
- Testes/backend, testes frontend e E2E continuam executaveis via Docker Compose.

## Validacao Esperada

- Executar `docker compose config`.
- Executar `docker compose up -d postgres backend frontend`.
- Executar `docker compose ps`.
- Alterar temporariamente um texto ou marcador nao funcional no frontend, confirmar atualizacao via Vite, e reverter a alteracao antes de concluir.
- Alterar temporariamente um marcador nao funcional no backend, confirmar reload do Uvicorn, e reverter a alteracao antes de concluir.
- Executar `docker compose --profile test run --rm backend-tests`.
- Executar `docker compose --profile test run --rm frontend-tests`.
- Executar `docker compose --profile test run --rm frontend-e2e`, se o ambiente estiver apto.
- Executar `git diff --stat` e confirmar escopo restrito.

## Riscos

- Risco: instalar dependencias no volume do host por engano.
  Mitigacao: usar volume nomeado para `node_modules` e evitar qualquer instalacao fora do container.

- Risco: reload do backend reiniciar durante migrations ou inicializacao.
  Mitigacao: manter ordem explicita de instalacao, migration e startup no comando do servico.

- Risco: politica de `.env` ser interpretada como permissao para versionar segredo.
  Mitigacao: documentar que `.env` local e permitido operacionalmente, mas leitura por agentes, copia de valores e versionamento de segredos continuam proibidos.

- Risco: alterar servicos de teste junto com servicos de desenvolvimento e quebrar validacoes reprodutiveis.
  Mitigacao: manter escopo de teste apenas no necessario para preservar comandos existentes.

## Bloqueios Pendentes

Nenhum bloqueio essencial identificado para criar a TASK.

Execucao depende de autorizacao explicita futura no fluxo governado.
