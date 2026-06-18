# TASK-008 - Organizar estrutura frontend minima

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`
- `TASK-004-auditar-estrutura-frontend-governada.md`

Esta TASK so deve ser executada depois que a TASK-004 registrar lacunas ou insuficiencias na estrutura frontend atual.

## Objetivo

Organizar a estrutura minima do frontend conforme a arquitetura aprovada e os documentos visuais governados, sem criar telas funcionais, rotas definitivas, consumo de API ou componentes de negocio.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- log esperado de `logs/LOG-004-auditar-estrutura-frontend-governada.md`

## Escopo Exato

- Ler o log da TASK-004 antes de qualquer alteracao.
- Criar ou ajustar somente a estrutura minima de pastas frontend necessaria, quando a auditoria indicar lacuna.
- Organizar, quando aplicavel, pastas para:
  - `components/`;
  - `routes/`;
  - `styles/`;
  - `lib/` ou utilitarios frontend;
  - `api/` ou camada futura de cliente HTTP;
  - `types/` ou contratos frontend.
- Preservar `frontend/src/styles/globals.css` como fonte de tokens runtime.
- Criar README curto de frontend apenas se a TASK-004 indicar ausencia de orientacao local.
- Registrar no README, se criado, que o frontend nao pode recalcular motores, aplicar regra prudencial ou alterar status retornado pelo backend.

## Fora De Escopo

- Criar telas funcionais.
- Criar rotas definitivas do produto.
- Criar componentes visuais completos.
- Criar cliente de API funcional.
- Consumir endpoints.
- Alterar tokens visuais.
- Alterar `frontend/src/styles/globals.css`, salvo correcao documental explicitamente indicada pela TASK-004.
- Instalar dependencias.
- Configurar Vite, Tailwind, shadcn/ui, React Router, TanStack Query, Vitest ou Playwright.
- Definir padrao visual novo.
- Implementar regra prudencial no frontend.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `logs/LOG-004-auditar-estrutura-frontend-governada.md`.
2. Identificar apenas lacunas estruturais aprovadas para correcao nesta TASK.
3. Criar ou ajustar pastas minimas de frontend conforme lacunas registradas.
4. Criar arquivos sentinela apenas quando necessarios para versionamento.
5. Criar `frontend/README.md` somente se a auditoria indicar ausencia de orientacao local.
6. Registrar no README, se criado, as responsabilidades e proibicoes do frontend conforme SPEC-001 e arquitetura.
7. Validar que nenhuma tela, rota funcional, componente de negocio, cliente de API ou regra prudencial foi criado.

## Arquivos Ou Areas Provaveis

- `frontend/README.md`, se necessario
- `frontend/src/components/`, se necessario
- `frontend/src/routes/`, se necessario
- `frontend/src/styles/`, se necessario
- `frontend/src/lib/`, se necessario
- `frontend/src/api/`, se necessario
- `frontend/src/types/`, se necessario

## Criterios De Aceite

- A TASK-004 foi executada antes desta TASK.
- Alteracoes estruturais correspondem apenas a lacunas registradas no log da TASK-004.
- A estrutura frontend minima fica coerente com `docs/architecture.md`.
- `frontend/src/styles/globals.css` permanece como fonte de tokens runtime.
- Nenhuma tela funcional e criada.
- Nenhum componente de negocio e criado.
- Nenhuma rota definitiva e criada.
- Nenhum cliente de API funcional e criado.
- Nenhuma regra prudencial e implementada no frontend.
- Nenhum token visual novo e definido.

## Validacao Esperada

- Executar `git diff --stat` e confirmar que as alteracoes estao restritas a `frontend/`.
- Conferir manualmente que as alteracoes correspondem ao log da TASK-004.
- Conferir manualmente que nao houve criacao de tela funcional, rota definitiva, cliente de API funcional ou regra prudencial.
- Conferir manualmente que `frontend/src/styles/globals.css` nao foi alterado indevidamente.

## Riscos

- Risco: organizacao estrutural virar implementacao de UI.
  Mitigacao: limitar a TASK a pastas, arquivos sentinela e README local quando necessario.

- Risco: criar padrao visual fora dos documentos governados.
  Mitigacao: bloquear novos tokens, estilos e variantes nesta TASK.

- Risco: frontend assumir regra prudencial por conveniencia.
  Mitigacao: registrar proibicao explicita no README local, se criado, e bloquear qualquer logica funcional.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 002 e 004.

Permanece bloqueado qualquer trabalho que tente criar tela funcional, rota definitiva, componente de negocio, cliente de API funcional, token visual novo ou regra prudencial no frontend durante esta TASK.
