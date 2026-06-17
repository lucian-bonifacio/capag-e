# TASK-068 - Implementar motor ROA

## SPEC De Origem

- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Dependencias

- `TASK-067-estruturar-assets-roa.md`

## Objetivo

Implementar motor ROA com blocos, componentes, regras de sinal e `RoaAuditRow`, sem recalcular `PLRA`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Escopo Exato

- Consumir contas de resultado e referencial.
- Calcular blocos ROA.
- Aplicar regras de sinal.
- Gerar audit rows e pendências.
- Registrar limitação de conferência `J150` quando ausente.

## Fora De Escopo

- Recalcular `PLRA`.
- Calcular DFC/FCA.
- Criar API, UI ou exportação.

## Passos Executaveis

1. Ler assets ROA.
2. Implementar `RoaCalculation` e `RoaAuditRow`.
3. Criar testes de blocos, sinais e pendências.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/app/domain/`
- `backend/tests/`

## Criterios De Aceite

- ROA não recalcula PLRA.
- Ausência de `J150` vira limitação/pendência.
- Valores usam `Decimal`.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: duplicar cálculo patrimonial.
  Mitigação: motor ROA recebe PLRA de fora.

## Bloqueios Pendentes

Bloqueada até assets ROA existirem.
