# TASK-055 - Modelar evidencias e materialidade

## SPEC De Origem

- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Dependencias

- `TASK-054-exportacao-e-testes-contrato-capag-e.md`

## Objetivo

Modelar `AdjustmentEvidence`, status de evidência, política default de materialidade e override manual justificado.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Escopo Exato

- Criar contratos internos de evidência.
- Calcular materialidade default no backend.
- Registrar override antes/depois com justificativa.
- Definir bloqueio/ressalva a partir de status e materialidade.

## Fora De Escopo

- Upload persistente de anexos.
- GED ou assinatura digital.
- Avaliação de ativos.
- UI, API e exportação.

## Passos Executaveis

1. Modelar `AdjustmentEvidence`.
2. Implementar cálculo de materialidade.
3. Implementar override justificado.
4. Criar testes de materialidade e bloqueio.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Materialidade default segue limiares da SPEC-005.
- Override exige justificativa.
- Evidência não altera valor por si só.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: evidência virar motor de cálculo.
  Mitigação: evidência sustenta, bloqueia ou ressalva, mas não recalcula.

## Bloqueios Pendentes

Bloqueada até contrato CAPAG-E estar disponível.
