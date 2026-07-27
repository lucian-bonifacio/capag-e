# TASK-098 - Criar UI PLRA

## SPEC De Origem

- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Dependencias

- `TASK-097-criar-api-integracao-plra-capag-e.md`

## Objetivo

Criar tela tecnica do PLRA para executar, consultar e auditar o calculo, sem recalcular metodologia no frontend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar rota e tela PLRA.
- Exibir resumo, formula, status e versao.
- Exibir defaults, pendencias e bloqueios.
- Abrir auditoria por conta.
- Cobrir loading, vazio, erro e sucesso.

## Fora De Escopo

- Recalcular PLRA no frontend.
- Administrar metodologia livremente.
- Alterar tokens ou padrao visual.
- Implementar fluxo de evidencias da SPEC-005.

## Passos Executaveis

1. Criar cliente de API e rota.
2. Criar resumo e tabela de memoria.
3. Criar estados e auditoria.
4. Criar testes frontend.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/`
- `frontend/src/api/`
- `frontend/src/components/`
- `frontend/src/test/`

## Criterios De Aceite

- UI mostra origem interna dos defaults.
- Valores e percentuais usam `.tnum`.
- Bloqueios e pendencias permanecem visiveis.
- Nenhuma formula prudencial existe no frontend.

## Validacao Esperada

- Executar testes e build frontend via `docker compose`.
- Inspecionar a jornada com Playwright.

## Riscos

- Risco: default parecer avaliacao definitiva.
  Mitigacao: exibir fonte, status e eventual avaliacao substituta.

## Bloqueios Pendentes

Bloqueada ate API PLRA existir.
