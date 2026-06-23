# CAPAG

Aplicacao interna para analise CAPAG-E auditavel a partir de ECD, com evolucao governada por PRD, arquitetura, SPECs, TASKs, logs, validacoes e homologacao.

Este README e um mapa de entrada do projeto. Ele nao substitui `AGENTS.md`, PRD, arquitetura, SPECs, TASKs ou logs.

## Fontes Governadas

- `AGENTS.md`: regras operacionais para agentes, fluxo de autorizacao, homologacao e gates de excecao.
- `ROADMAP.md`: painel operacional vivo com proxima tarefa, status, TASKs e logs.
- `docs/product/PRD.md`: visao de produto, objetivos, escopo e restricoes.
- `docs/architecture/architecture.md`: arquitetura alvo, stack, camadas e responsabilidades.
- `specs/`: contratos tecnicos por modulo.
- `specs/README.md`: indice oficial de SPECs e rastreabilidade.
- `tasks/`: TASKs executaveis derivadas de SPEC suficiente.
- `tasks/README.md`: convencao, template e bloqueios para TASKs.
- `logs/`: evidencia operacional objetiva de execucao, validacao e homologacao.

Materiais em `docs/reference/` nao sao fonte normativa direta para implementacao, salvo autorizacao explicita ou incorporacao previa em documento governado.

## Ordem De Leitura Recomendada

1. `AGENTS.md`
2. `ROADMAP.md`
3. `tasks/README.md`
4. TASK indicada em `## Proxima Tarefa`
5. SPEC de origem indicada pela TASK
6. `docs/product/PRD.md`
7. `docs/architecture/architecture.md`
8. Documentos governados adicionais citados pela TASK ou SPEC

Quando a TASK envolver UI, telas, componentes, UX ou visual, consulte tambem:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Fluxo De Trabalho

O fluxo obrigatorio e:

```text
PRD -> Arquitetura -> SPEC -> TASK -> execucao -> log -> homologacao
```

Uma TASK deve nascer de SPEC suficiente. Criar uma TASK nao autoriza sua execucao no mesmo passo.

Durante a execucao, o escopo fica limitado a TASK autorizada. Ao final, o agente registra evidencia em `logs/`, move a TASK para `aguardando_homologacao` no `ROADMAP.md` e aguarda homologacao do usuario. A TASK so vira `concluido` apos aprovacao.

## Ambiente Oficial

O ambiente oficial exige no host apenas:

- Git
- Docker
- Docker Compose

Comandos oficiais devem usar `docker compose`. O fluxo oficial nao usa `.venv` local, `node_modules` no host, `pip install` global, instalacoes globais de Node ou package managers no host.

Arquivos `.env` reais nao devem ser lidos, criados ou alterados por conveniencia. Use os contratos governados e o Compose existente.

## Comandos Disponiveis

Validar a configuracao Docker Compose:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test config
```

Subir o PostgreSQL local em container:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose up -d postgres
```

Executar testes backend minimos:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm backend-tests
```

Executar testes frontend minimos:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm frontend-tests
```

Validar a estrutura minima do Alembic:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose --profile test run --rm backend-tests sh -c "python -m pip install --disable-pip-version-check --root-user-action=ignore alembic && alembic -c alembic.ini heads"
```

Estes comandos sao validacoes de fundacao. Eles nao implementam parser ECD, motores prudenciais, endpoints funcionais, migrations de dominio, telas finais, exportacao Excel ou laudo.

## Estrutura Principal

- `backend/`: estrutura minima do backend Python/FastAPI conforme arquitetura.
- `frontend/`: estrutura minima do frontend React/Vite e tokens runtime.
- `docs/`: PRD, arquitetura, documentos frontend e referencias historicas.
- `specs/`: SPECs oficiais suficientes para gerar TASKs.
- `tasks/`: TASKs governadas.
- `logs/`: registros de execucao, validacao e homologacao.
- `.github/workflows/ci.yml`: CI minimo com validacoes via Docker Compose.

## Regras De Escopo

- Regra prudencial sensivel fica no backend, conforme arquitetura e SPECs.
- Frontend, Excel e laudo nao recalculam motores prudenciais.
- Valores contabeis, fiscais, financeiros ou prudenciais nao devem usar `float`.
- Contratos de API, formulas, arredondamento, fontes normativas e padroes visuais exigem SPEC/TASK suficiente.
- Mudancas fora da TASK autorizada exigem classificacao de escopo e decisao do usuario.
