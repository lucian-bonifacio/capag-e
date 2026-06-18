# TASK-077 - Criar UI de laudo CAPAG-E

## SPEC De Origem

- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Dependencias

- `TASK-076-criar-api-laudo-capag-e.md`

## Objetivo

Criar tela de laudo CAPAG-E com método, `CAPAG-P`, responsável, preview de seções, bloqueios, ressalvas e ação de exportação, sem recalcular resultados.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar rota `/analises/:analysisId/laudo`.
- Consumir preview da API.
- Exibir status do laudo, bloqueios e ressalvas.
- Enviar payload de geração conforme contrato.

## Fora De Escopo

- Recalcular PLRA/FCA/ROA/CAPAG-E.
- Editar regras metodológicas.
- Criar DOCX/PDF.
- Alterar tokens.

## Passos Executaveis

1. Ler contrato da API.
2. Criar tela conforme padrões governados.
3. Criar testes frontend de estados essenciais.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/`
- `frontend/src/components/`
- `frontend/src/api/`

## Criterios De Aceite

- UI mostra bloqueios e ressalvas.
- UI não recalcula resultado.
- Exportação usa API.
- Estados essenciais existem.

## Validacao Esperada

- Executar testes/build frontend via `docker compose`.

## Riscos

- Risco: UI permitir laudo final bloqueado.
  Mitigação: ação respeita status vindo da API.

## Bloqueios Pendentes

Bloqueada até API de laudo existir.
