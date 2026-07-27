# TASK-099 - Exportacao e testes PLRA

## SPEC De Origem

- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Dependencias

- `TASK-097-criar-api-integracao-plra-capag-e.md`
- `TASK-098-criar-ui-plra.md`

## Objetivo

Criar exportacao Excel PLRA e consolidar testes do modulo, incluindo fluxo E2E com ECD governada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Escopo Exato

- Exportar resumo e memoria PLRA.
- Incluir defaults, overrides, pendencias e versao.
- Consolidar testes backend, frontend e E2E.
- Validar integracao PLRA com CAPAG-E.

## Fora De Escopo

- Gerar laudo narrativo.
- Recalcular no Excel.
- Implementar FCA ou ROA.

## Passos Executaveis

1. Criar abas Excel PLRA.
2. Criar testes de exportacao.
3. Executar suites do modulo.
4. Executar Playwright via Docker Compose.
5. Validar fluxo com fixture ECD governada.

## Arquivos Ou Areas Provaveis

- `backend/app/export/`
- `backend/tests/`
- `frontend/e2e/`
- `frontend/src/test/`

## Criterios De Aceite

- Excel reconstrui o resultado sem recalculo.
- Testes cobrem defaults, hierarquia e bloqueios.
- Fluxo E2E exibe PLRA real no contrato CAPAG-E.
- Todas as validacoes rodam via Docker Compose.

## Validacao Esperada

- Executar testes backend, frontend, build e Playwright via `docker compose`.

## Riscos

- Risco: fixture nao representar cobertura real.
  Mitigacao: usar fixture governada e registrar limitacoes de cobertura.

## Bloqueios Pendentes

Bloqueada ate API e UI PLRA existirem.
