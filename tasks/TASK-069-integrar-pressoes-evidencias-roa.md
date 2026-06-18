# TASK-069 - Integrar pressoes e evidencias ROA

## SPEC De Origem

- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Dependencias

- `TASK-057-persistir-e-integrar-bloqueios-evidencias.md`
- `TASK-068-implementar-motor-roa.md`

## Objetivo

Integrar pressões complementares de caixa, pendências e evidências ao cálculo de `ROA Final`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Escopo Exato

- Tratar fornecedores vencidos, parcelamentos, contingências, dívida fiscal, trabalhista, mútuos e intercompany.
- Gerar pendências para despesas condicionais materiais.
- Integrar evidências sem recalcular fora do motor.

## Fora De Escopo

- Criar laudo.
- Criar UI.
- Calcular FCA.
- Recalcular PLRA.

## Passos Executaveis

1. Implementar pressões complementares.
2. Integrar evidências por componente.
3. Criar testes de pendências e bloqueios.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Pressões reduzem ROA Final conforme regra.
- Pendências materiais ficam explícitas.
- Evidências afetam status.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: pressão complementar duplicar PLRA.
  Mitigação: testes de separação ROA/PLRA.

## Bloqueios Pendentes

Bloqueada até motor ROA e evidências existirem.
