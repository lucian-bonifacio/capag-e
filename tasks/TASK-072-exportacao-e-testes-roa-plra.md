# TASK-072 - Exportacao e testes ROA + PLRA

## SPEC De Origem

- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Dependencias

- `TASK-071-criar-api-ui-roa.md`

## Objetivo

Criar exportação ROA + PLRA e consolidar testes do módulo, cobrindo blocos ROA, pressões complementares, pendências, evidências e integração CAPAG-E.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Escopo Exato

- Exportar cálculo ROA, audit rows e status.
- Incluir integração com PLRA/CAPAG-E.
- Testar blocos, sinais, pendências e evidências.

## Fora De Escopo

- Gerar laudo.
- Recalcular no Excel.
- Criar DFC.

## Passos Executaveis

1. Criar exportador ROA.
2. Criar testes obrigatórios do módulo.
3. Validar via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/export/`
- `backend/tests/`

## Criterios De Aceite

- Exportação não recalcula ROA.
- Status e pendências aparecem.
- Testes cobrem `CAPAG-E = ROA + PLRA`.

## Validacao Esperada

- Executar testes backend e frontend aplicáveis via `docker compose`.

## Riscos

- Risco: exportação omitir limitação de J150.
  Mitigação: limitações são campos obrigatórios.

## Bloqueios Pendentes

Bloqueada até API/UI ROA existirem.
