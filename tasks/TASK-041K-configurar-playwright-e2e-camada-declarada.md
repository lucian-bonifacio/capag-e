# TASK-041K - Configurar Playwright E2E da camada declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-040-criar-ui-camada-declarada.md`
- `TASK-041-exportacao-e-testes-camada-declarada.md`
- `TASK-041L-ajustar-fluxo-homologacao-por-grupo.md`

## Objetivo

Configurar Playwright como ferramenta governada de testes end-to-end da camada declarada, executavel via Docker Compose, com possibilidade de apoio manual por MCP Playwright durante desenvolvimento e homologacao.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Adicionar dependencias e configuracao do Playwright no frontend.
- Criar `frontend/playwright.config.ts`.
- Criar servico Docker Compose para executar testes E2E sem `node_modules` no host.
- Criar teste inicial da rota declarada cobrindo carregamento, sucesso e erro, usando ambiente Docker.
- Documentar uso do MCP Playwright como apoio de inspecao manual/visual, sem substituir validacao reprodutivel por Docker Compose.
- Garantir que Playwright nao execute regra de negocio nem substitua testes backend/frontend existentes.

## Fora De Escopo

- Implementar upload real de ECD.
- Implementar parser ECD.
- Criar fluxo E2E completo de importacao real.
- Criar testes de camada reclassificada.
- Usar Playwright fora do ambiente Docker como requisito oficial.

## Passos Executaveis

1. Ler configuracao atual de frontend e Docker Compose.
2. Adicionar Playwright e scripts de teste E2E no frontend.
3. Criar configuracao e teste minimo governado.
4. Criar servico Docker Compose para E2E.
5. Validar via Docker Compose.
6. Registrar no log o resultado dos testes e qualquer limitacao temporaria.

## Arquivos Ou Areas Provaveis

- `frontend/package.json`
- `frontend/playwright.config.ts`
- `frontend/e2e/`
- `docker-compose.yml`
- `docs/` ou `AGENTS.md`, se necessario para instrucoes operacionais.

## Criterios De Aceite

- Playwright pode ser executado via Docker Compose.
- Teste E2E inicial valida rota declarada sem depender de `node_modules` no host.
- MCP Playwright fica documentado como apoio de inspecao manual/visual.
- Validacoes automatizadas existentes continuam executando.
- Nenhum dado real sensivel e usado em teste E2E.

## Validacao Esperada

- Executar testes frontend via `docker compose`.
- Executar testes E2E Playwright via `docker compose`.
- Conferir ausencia de `node_modules` no host.

## Riscos

- Risco: teste E2E ficar dependente de estado local instavel.
  Mitigacao: usar fixtures/carga controlada e ambiente Docker.

## Bloqueios Pendentes

Nenhum.
