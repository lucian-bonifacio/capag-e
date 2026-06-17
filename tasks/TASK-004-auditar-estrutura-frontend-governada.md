# TASK-004 - Auditar estrutura frontend governada

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`

Esta TASK so deve ser executada depois que a TASK-002 registrar o estado geral da estrutura minima do repositorio.

## Objetivo

Auditar a estrutura atual do frontend contra a arquitetura aprovada e os documentos visuais governados, identificando lacunas de organizacao, tokens, rotas e responsabilidades antes de qualquer implementacao de tela funcional.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`

## Escopo Exato

- Auditar se `frontend/` existe e se possui estrutura minima compatível com React/Vite e TypeScript.
- Auditar se `frontend/src/styles/globals.css` existe e expõe tokens governados.
- Auditar se a estrutura atual separa, quando existente, areas como:
  - rotas;
  - componentes;
  - estilos;
  - consumo de API;
  - tipos ou contratos frontend.
- Registrar lacunas em relatorio documental.
- Propor TASKs pequenas para organizar frontend quando houver lacunas.
- Confirmar que frontend nao deve duplicar regra prudencial, recalcular motores ou alterar status retornado pelo backend.

## Fora De Escopo

- Criar ou alterar componentes React.
- Criar rotas.
- Criar telas.
- Alterar `globals.css`.
- Instalar dependencias.
- Configurar Vite, Tailwind, shadcn/ui, React Router ou TanStack Query.
- Criar cliente de API.
- Implementar consumo de endpoint.
- Definir padrao visual novo.
- Alterar `tasks/README.md`.

## Passos Executaveis

1. Ler `tasks/reports/TASK-002-auditoria-estrutura-minima.md`.
2. Conferir a existencia e organizacao de `frontend/`.
3. Conferir a existencia de `frontend/src/styles/globals.css`.
4. Comparar a estrutura encontrada com `docs/architecture.md` e documentos governados de frontend.
5. Criar relatorio em `tasks/reports/TASK-004-auditoria-frontend-governada.md`.
6. Registrar achados por area auditada.
7. Registrar lacunas sem corrigi-las.
8. Sugerir proximas TASKs pequenas para lacunas encontradas.
9. Validar que nenhum arquivo de frontend foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-004-auditoria-frontend-governada.md`
- `frontend/` apenas para leitura
- `docs/frontend/` apenas para leitura
- `specs/SPEC-001-modulo-0-fundacao-governada.md` apenas para leitura

## Criterios De Aceite

- Existe relatorio em `tasks/reports/TASK-004-auditoria-frontend-governada.md`.
- O relatorio cita a SPEC de origem e os documentos governados de frontend.
- O relatorio informa se `frontend/` existe e qual estrutura foi encontrada.
- O relatorio informa se `frontend/src/styles/globals.css` existe.
- O relatorio registra lacunas sem corrigi-las.
- O relatorio sugere proximas TASKs pequenas e independentes quando houver lacunas.
- Nenhum arquivo em `frontend/` e alterado.
- Nenhum padrao visual novo e definido.
- Nenhuma regra prudencial e movida para o frontend.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-004-auditoria-frontend-governada.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `tasks/reports/TASK-004-auditoria-frontend-governada.md`.
- Conferir manualmente que o relatorio nao implementa UI, nao define regra visual nova e nao cria regra de dominio no frontend.

## Riscos

- Risco: auditoria virar refatoracao de frontend.
  Mitigacao: registrar lacunas em relatorio e criar TASKs futuras, sem alterar `frontend/`.

- Risco: frontend assumir responsabilidade de regra prudencial.
  Mitigacao: reforcar no relatorio as proibicoes da SPEC-001 e da arquitetura.

- Risco: criar tarefa seguinte ampla demais.
  Mitigacao: sugerir apenas TASKs pequenas, independentes e verificaveis.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-002.

Permanece bloqueado qualquer trabalho que tente criar tela, componente, rota, cliente de API, novo token visual, regra prudencial ou recalculo no frontend durante esta TASK.
