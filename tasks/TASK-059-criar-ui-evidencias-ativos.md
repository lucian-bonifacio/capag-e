# TASK-059 - Criar UI de evidencias e ativos

## SPEC De Origem

- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Dependencias

- `TASK-058-criar-api-evidencias-ativos.md`

## Objetivo

Criar tela de evidências, justificativas, materialidade e avaliação de ativos, consumindo API sem recalcular materialidade, bloqueios, `PLRA` ou `CAPAG-E`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Exibir evidências por escopo e componente.
- Permitir justificativa e override controlado via API.
- Exibir avaliações de ativos e bloqueios.
- Cobrir estados essenciais de UI.

## Fora De Escopo

- Recalcular materialidade no frontend.
- Upload persistente de anexos.
- Criar laudo.
- Alterar tokens visuais.

## Passos Executaveis

1. Ler contrato da API.
2. Criar tela conforme padrões governados.
3. Criar formulários de justificativa quando permitido.
4. Criar testes frontend mínimos.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/`
- `frontend/src/components/`
- `frontend/src/api/`

## Criterios De Aceite

- UI não recalcula materialidade.
- Bloqueios e pendências são visíveis.
- Override exige justificativa.
- Tokens governados são preservados.

## Validacao Esperada

- Executar testes/build frontend via `docker compose`.

## Riscos

- Risco: UI esconder pendência documental.
  Mitigação: badges/status vindos da API.

## Bloqueios Pendentes

Bloqueada até API de evidências e ativos existir.
