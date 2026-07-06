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

### Reuso De Fontes Na Mesma Sessão

Dentro da mesma sessão, uma fonte obrigatória já consultada pode ser considerada consultada novamente sem releitura integral quando todas as condições abaixo forem verdadeiras:

- o conteúdo relevante da fonte permanece disponível no contexto da conversa;
- não houve alteração no arquivo desde a consulta anterior;
- não houve compactação, perda de contexto ou troca de sessão que comprometa a compreensão do conteúdo;
- a nova TASK não exige uma leitura mais específica ou diferente daquela fonte.

Mesmo nesses casos, o agente deve reler a TASK em execução e a SPEC de origem indicada pela TASK, pois esses documentos são o contrato direto da execução.

Se houver dúvida sobre atualidade, completude ou aplicabilidade do conteúdo já consultado, releia a fonte antes de executar.

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

## 5. Fluxo De Trabalho

Após a resposta do usuário ao pedido de autorização da seção `## 2. Ao Iniciar A Sessão`:

- Se o usuário autorizar claramente, execute a TASK.
- Se a resposta não for autorização clara, use `scope-resolution`.
- Se houver TASK em `aguardando_homologacao`, solicite ao usuário uma conclusão de homologação antes de qualquer nova execução, salvo quando a autorização vigente definir explicitamente um grupo de execução ou quando o usuário pedir expressamente para continuar.

### Execução Individual

Uma TASK individual é o padrão de execução.

Durante a execução:

1. Execute apenas o escopo da TASK.
2. Execute as validações esperadas pela TASK.
3. Quando a TASK envolver UI, fluxo interativo ou jornada end-to-end, aplique também as regras da subseção `### Validação De UI E Playwright`.
4. Ao final da implementação, use `execution-log` para registrar a evidência operacional.
5. Use `roadmap-manager` para mover a TASK para `aguardando_homologacao`.
6. Informe o usuário e aguarde homologação, exceto quando a TASK fizer parte de um grupo de execução autorizado.

Se uma validação esperada ainda não existir, estiver bloqueada pela maturidade do projeto ou não puder ser executada sem violar o ambiente oficial, registre objetivamente a limitação no log da TASK.

Quando não houver teste automatizado adequado para o escopo alterado, crie teste automatizado focado se isso couber na TASK e não violar SPEC, TASK, arquitetura ou gates de exceção. Se criar teste não couber sem ampliar escopo ou violar gate, registre a limitação no log e peça decisão governada ou proponha nova TASK conforme o fluxo de escopo.

### Execução Por Grupo

Um grupo de execução pode ser autorizado pelo usuário como:

- sequência contínua de TASKs a partir da `## Próxima Tarefa`;
- lista explícita de TASKs;
- conjunto definido pelo usuário por critério objetivo.

Mesmo dentro de um grupo:

1. Cada TASK continua sendo executada individualmente.
2. Cada TASK exige leitura das fontes aplicáveis, escopo próprio, validações próprias, log próprio e atualização própria do `ROADMAP.md`.
3. Testes e validações previstas são obrigatórios ao final de cada TASK.
4. Gates de exceção continuam valendo para cada TASK.
5. Uma TASK concluída dentro do grupo deve ser movida para `aguardando_homologacao`.

Quando houver grupo autorizado, o agente não deve parar para homologação individual entre TASKs do grupo. Ao final do grupo, ou ao encontrar bloqueio que impeça continuidade governada, informe o resultado consolidado e solicite homologação do conjunto.

Se uma TASK do grupo falhar, bloquear ou exigir decisão expressa do usuário:

- pare o grupo no ponto afetado;
- registre a evidência no log da TASK;
- mantenha concluídas em `aguardando_homologacao` as TASKs já executadas;
- solicite decisão governada antes de continuar.

### Validação De UI E Playwright

- Testes E2E governados devem ser executáveis pelo ambiente oficial Docker/Docker Compose.
- MCP Playwright pode ser usado pelo agente para navegar, inspecionar, capturar evidência visual e diagnosticar problemas durante execução ou homologação assistida.
- MCP Playwright não substitui testes automatizados reproduzíveis quando a TASK exigir validação E2E governada.
- Ao concluir TASK com UI ou fluxo interativo, registre no log quais validações foram executadas: testes unitários/frontend, build, Playwright via Docker Compose quando existir, e inspeção MCP Playwright quando usada.
- Se Playwright ainda não estiver configurado para o fluxo da TASK, registre a limitação no log em vez de omitir validação visual.

Após homologação:

- se o usuário aprovar uma TASK individual, use `execution-log` para registrar aprovação e `roadmap-manager` para marcar `concluido` e recalcular a próxima tarefa;
- se o usuário aprovar um grupo, use `execution-log` para registrar aprovação das TASKs aprovadas e `roadmap-manager` para marcar essas TASKs como `concluido` e recalcular a próxima tarefa;
- se o usuário reprovar parcialmente um grupo ou pedir ajuste em uma TASK do grupo, use `scope-resolution` para classificar o ajuste, mantenha como `concluido` apenas as TASKs explicitamente aprovadas e mantenha a TASK afetada em estado governado compatível com a decisão;
- se o usuário pedir ajuste em TASK individual, use `scope-resolution`;
- não marque TASK como `concluido` sem homologação do usuário.

Quando não houver homologação, ajuste, bloqueio ou decisão governada pendente, retome o fluxo normal:

1. Informe ao usuário a `## Próxima Tarefa` indicada no `ROADMAP.md`, seu status e que as fontes aplicáveis foram consultadas.
2. Peça autorização simples para executar.
3. Após a resposta do usuário, aplique novamente as regras desta seção `## 5. Fluxo De Trabalho`.

Nota: se desejar, o usuário pode autorizar um grupo de TASKs em vez de apenas a próxima TASK, desde que informe uma sequência, lista ou critério objetivo.

Se `scope-resolution` classificar uma solicitação como nova TASK, peça confirmação explícita. Após aprovação, use `task-planner`. Não implemente a nova TASK no mesmo passo.

Criar uma TASK não autoriza sua execução no mesmo passo. Após criar ou planejar uma TASK, aguarde confirmação explícita do usuário para executá-la dentro do fluxo governado.

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
