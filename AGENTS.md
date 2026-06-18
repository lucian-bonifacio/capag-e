# Instruções Para Agentes

## 1. Objetivo

Este arquivo é a regra operacional principal para agentes de IA, assistentes de código e ferramentas automatizadas que atuem no projeto CAPAG.

O projeto deve evoluir por execução governada de TASKs, com rastreabilidade entre PRD, arquitetura, SPECs, TASKs, logs, validações e homologação do usuário.

## 2. Ao Iniciar A Sessão

Ao iniciar trabalho neste repositório pela primeira vez na sessão:

1. Leia este `AGENTS.md` inteiro.
2. Leia o `ROADMAP.md`.
3. Identifique a `## Próxima Tarefa`.
4. Leia `tasks/README.md`.
5. Leia a TASK indicada.
6. Leia a SPEC de origem indicada pela TASK.
7. Leia PRD, arquitetura e documentos governados aplicáveis.
8. Quando o escopo envolver UI, telas, componentes, UX ou visual, leia também:
   - `docs/frontend/DESIGN_TOKENS.md`
   - `docs/frontend/UI_COMPONENT_RULES.md`
   - `docs/frontend/SCREEN_PATTERNS.md`
   - `frontend/src/styles/globals.css`
9. Informe ao usuário a TASK identificada, seu status e que as fontes aplicáveis foram consultadas.
10. Peça autorização simples para executar.

Materiais históricos em `docs/reference/` e outros diretórios de referência não são fonte normativa direta para implementação. Use esses materiais somente com autorização explícita do usuário ou quando forem citados pela SPEC/TASK governada.

## 3. Documentos Operacionais

- `ROADMAP.md`: documento vivo de execução, próxima tarefa e status.
- `tasks/`: detalhamento governado das TASKs.
- `logs/`: evidência operacional objetiva de execução.
- `specs/`: contratos técnicos por módulo.

## 4. Skills Operacionais

Use as skills operacionais do projeto quando o fluxo exigir:

- `execution-log`: criar ou atualizar logs em `logs/`.
- `roadmap-manager`: criar ou atualizar `ROADMAP.md`.
- `scope-resolution`: classificar dúvidas, sugestões, ajustes, reprovações e mudanças de escopo.
- `task-planner`: criar nova TASK governada após confirmação explícita.


Após a resposta do usuário ao pedido de autorização da seção `## 2. Ao Iniciar A Sessão`:

- Se o usuário autorizar claramente, execute a TASK.
- Se a resposta não for autorização clara, use `scope-resolution`.
- Se houver TASK em `aguardando_homologacao`, solicite ao usuário uma conclusão de homologação antes de qualquer nova execução. Não execute a próxima TASK, salvo pedido expresso do usuário.

Durante a execução:

1. Execute apenas o escopo da TASK.
2. Execute as validações esperadas pela TASK.
3. Ao final da implementação, use `execution-log` para registrar a evidência operacional.
4. Use `roadmap-manager` para mover a TASK para `aguardando_homologacao`.
5. Informe o usuário e aguarde homologação.

Após homologação:

- se o usuário aprovar, use `execution-log` para registrar aprovação e `roadmap-manager` para marcar `concluido` e recalcular a próxima tarefa;
- se o usuário pedir ajuste, use `scope-resolution`;
- não marque TASK como `concluido` sem homologação do usuário.

Quando não houver homologação, ajuste, bloqueio ou decisão governada pendente, retome o fluxo normal:

1. Informe ao usuário a `## Próxima Tarefa` indicada no `ROADMAP.md`, seu status e que as fontes aplicáveis foram consultadas.
2. Peça autorização simples para executar.
3. Após a resposta do usuário, aplique novamente as regras desta seção `## 5. Fluxo De Trabalho`.

Se `scope-resolution` classificar uma solicitação como nova TASK, peça confirmação explícita. Após aprovação, use `task-planner`. Não implemente a nova TASK no mesmo passo.

## 6. Gates De Exceção

Pare e peça decisão expressa do usuário quando a execução exigir:

- descumprir PRD;
- descumprir arquitetura;
- descumprir SPEC;
- descumprir TASK;
- alterar contrato de API;
- alterar regra prudencial, fórmula, fonte normativa ou arredondamento;
- alterar padrão visual governado;
- usar `float` em valor contábil, fiscal, financeiro ou prudencial;
- executar fora do ambiente Docker/Docker Compose;
- ler ou alterar segredo;
- executar comando destrutivo;
- ampliar escopo de forma relevante.

Não contorne bloqueios por conveniência.

## 7. Ambiente Oficial

O ambiente oficial do projeto é exclusivamente Docker/Docker Compose.

Regras:

- comandos oficiais devem executar via `docker compose`;
- dependências Python devem ser instaladas apenas dentro de imagem/container;
- dependências Node devem ser instaladas apenas dentro de imagem/container;
- PostgreSQL deve rodar em container;
- testes, builds, migrations e validações devem rodar via container;
- o host deve exigir apenas Git, Docker e Docker Compose.

Proibições:

- não criar ou exigir `.venv` local;
- não criar ou exigir `node_modules` no host;
- não usar `pip install` global;
- não usar `npm install -g`, `pnpm add -g`, `yarn global` ou equivalente;
- não exigir Python, Node, npm, pnpm, yarn ou pip instalados no host para operar o projeto.
