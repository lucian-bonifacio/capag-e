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
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- log esperado de `logs/LOG-002-auditar-estrutura-minima-repositorio.md`

## Escopo Exato

- Auditar se `frontend/` existe e se possui estrutura minima compatível com React/Vite e TypeScript.
- Auditar se `frontend/src/styles/globals.css` existe e expõe tokens governados.
- Auditar se a estrutura atual separa, quando existente, areas como:
  - rotas;
  - componentes;
  - estilos;
  - consumo de API;
  - tipos ou contratos frontend.
- Registrar lacunas em log operacional.
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

1. Ler `logs/LOG-002-auditar-estrutura-minima-repositorio.md`.
2. Conferir a existencia e organizacao de `frontend/`.
3. Conferir a existencia de `frontend/src/styles/globals.css`.
4. Comparar a estrutura encontrada com `docs/architecture/architecture.md` e documentos governados de frontend.
5. Criar log em `logs/LOG-004-auditar-estrutura-frontend-governada.md`.
6. Registrar achados por area auditada.
7. Registrar lacunas sem corrigi-las.
8. Sugerir proximas TASKs pequenas para lacunas encontradas.
9. Validar que nenhum arquivo de frontend foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `logs/LOG-004-auditar-estrutura-frontend-governada.md`
- `frontend/` apenas para leitura
- `docs/frontend/` apenas para leitura
- `specs/SPEC-001-modulo-0-fundacao-governada.md` apenas para leitura

## Criterios De Aceite

- Existe log em `logs/LOG-004-auditar-estrutura-frontend-governada.md`.
- O log cita a SPEC de origem e os documentos governados de frontend.
- O log informa se `frontend/` existe e qual estrutura foi encontrada.
- O log informa se `frontend/src/styles/globals.css` existe.
- O log registra lacunas sem corrigi-las.
- O log sugere proximas TASKs pequenas e independentes quando houver lacunas.
- Nenhum arquivo em `frontend/` e alterado.
- Nenhum padrao visual novo e definido.
- Nenhuma regra prudencial e movida para o frontend.

## Validacao Esperada

- Executar `test -f logs/LOG-004-auditar-estrutura-frontend-governada.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `logs/LOG-004-auditar-estrutura-frontend-governada.md`.
- Conferir manualmente que o log nao implementa UI, nao define regra visual nova e nao cria regra de dominio no frontend.

## Riscos

- Risco: auditoria virar refatoracao de frontend.
  Mitigacao: registrar lacunas em log e criar TASKs futuras, sem alterar `frontend/`.

- Risco: frontend assumir responsabilidade de regra prudencial.
  Mitigacao: reforcar no log as proibicoes da SPEC-001 e da arquitetura.

- Risco: criar tarefa seguinte ampla demais.
  Mitigacao: sugerir apenas TASKs pequenas, independentes e verificaveis.

## Bloqueios Pendentes

Bloqueada ate a execucao da TASK-002.

Permanece bloqueado qualquer trabalho que tente criar tela, componente, rota, cliente de API, novo token visual, regra prudencial ou recalculo no frontend durante esta TASK.
