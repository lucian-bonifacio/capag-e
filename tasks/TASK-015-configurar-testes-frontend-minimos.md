# TASK-015 - Configurar testes frontend minimos

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-004-auditar-estrutura-frontend-governada.md`
- `TASK-006-auditar-validacoes-minimas-do-projeto.md`
- `TASK-008-organizar-estrutura-frontend-minima.md`

Esta TASK so deve ser executada depois que a estrutura frontend minima existir e a auditoria de validacoes indicar a lacuna ou insuficiencia de testes frontend.

## Objetivo

Configurar a base minima de testes frontend com Vitest e React Testing Library executando via Docker Compose, sem criar testes de tela funcional, consumo de API, regra prudencial, fluxo de negocio ou validacao visual abrangente.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- relatorio esperado de `tasks/reports/TASK-006-auditoria-validacoes.md`

## Escopo Exato

- Criar configuracao minima de Vitest, se ainda nao existir.
- Criar configuracao minima de React Testing Library, se necessaria.
- Criar teste sentinela nao funcional para validar que o runner executa.
- Documentar comando esperado para execucao dos testes frontend via `docker compose`.
- Garantir que nenhum teste de tela funcional, rota, API, regra prudencial ou fluxo de negocio seja criado nesta TASK.
- Garantir que `node_modules` no host nao seja criado ou exigido.

## Fora De Escopo

- Criar testes de componentes de negocio.
- Criar testes de rotas reais.
- Criar testes de consumo de API.
- Criar testes Playwright.
- Criar testes visuais.
- Criar componentes React.
- Criar telas.
- Criar cliente de API.
- Alterar tokens visuais ou `globals.css`.
- Instalar dependencias no host.
- Criar ou exigir `node_modules` no host.
- Configurar CI.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler `tasks/reports/TASK-006-auditoria-validacoes.md`.
2. Confirmar que a lacuna de testes frontend foi registrada.
3. Verificar a estrutura frontend organizada pela TASK-008.
4. Criar ou ajustar configuracao minima de Vitest.
5. Criar setup minimo de React Testing Library, se necessario.
6. Criar teste sentinela que nao exerca tela, rota, API ou regra de negocio.
7. Documentar comando de execucao em local apropriado, se a auditoria indicar ausencia documental.
8. Validar que nenhum componente, tela, rota, cliente de API, teste funcional ou regra prudencial foi criado.

## Arquivos Ou Areas Provaveis

- `frontend/vitest.config.*`, se necessario
- `frontend/src/test/` ou estrutura equivalente, se necessario
- `frontend/src/**/*.test.*` apenas para teste sentinela nao funcional
- `frontend/README.md`, somente se a auditoria indicar necessidade de documentar comando

## Criterios De Aceite

- A TASK-006 foi executada antes desta TASK.
- Existe configuracao minima para testes frontend.
- Vitest consegue descobrir e executar o teste sentinela.
- O teste sentinela nao valida tela, rota, API ou regra de negocio.
- Nenhum componente, tela, rota, cliente de API ou regra prudencial e criado.
- `frontend/src/styles/globals.css` nao e alterado indevidamente.
- Playwright e CI nao sao configurados nesta TASK.

## Validacao Esperada

- Executar o comando frontend de teste definido pela TASK via `docker compose`.
- Executar `git diff --stat` e confirmar que as alteracoes estao restritas a configuracao/testes frontend minimos permitidos.
- Conferir manualmente que o teste criado e apenas sentinela e nao define comportamento funcional.
- Conferir manualmente que nenhuma dependencia foi instalada no host e que `node_modules` no host nao foi criado.

## Riscos

- Risco: teste sentinela virar contrato de UI indevido.
  Mitigacao: limitar o teste a verificacao do runner, sem testar componente de negocio.

- Risco: introduzir padrao visual fora dos documentos governados.
  Mitigacao: nao criar componentes nem alterar tokens nesta TASK.

- Risco: antecipar consumo de API sem contrato funcional suficiente.
  Mitigacao: bloquear cliente de API e testes de API nesta TASK.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 004, 006 e 008.

Permanece bloqueado qualquer trabalho que tente criar componente, tela, rota, cliente de API, teste funcional, teste visual, Playwright, CI, regra prudencial, `node_modules` no host ou instalacao de dependencia no host durante esta TASK.
