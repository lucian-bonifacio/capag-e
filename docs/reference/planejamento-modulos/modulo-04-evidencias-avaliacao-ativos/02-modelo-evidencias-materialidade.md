# 02 - Modelo de evidencias e materialidade

## Objetivo

Definir a entidade de evidencia e as regras de materialidade.

## Entidade principal

Planejar estrutura equivalente a `AdjustmentEvidence`.

Campos minimos:

- `evidence_id`
- `exercise_year`
- `scope_type`
- `scope_key`
- `adjustment_type`
- `method_component`
- `amount_impact`
- `materiality_level`
- `required_evidence_type`
- `evidence_status`
- `analyst_justification`
- `review_notes`
- `blocks_final_report`
- `created_at`
- `updated_at`

## Escopos permitidos

- `account`
- `methodology_group`
- `macrogroup`
- `fco_movement`
- `dfc_component`
- `roa_component`
- `asset_valuation`
- `manual_override`
- `capag_assessment`

## Componentes metodologicos

- `PLRA`
- `FCA`
- `ROA`
- `CAPAG-E`

## Status de evidencia

- `nao_exigida`
- `pendente`
- `informada`
- `validada`
- `dispensada_com_justificativa`
- `rejeitada`

## Materialidade

Valores permitidos:

- `baixa`
- `media`
- `alta`
- `critica`

## Regras

1. Ajuste material deve ter justificativa.
2. Ajuste critico sem evidencia validada deve bloquear laudo final ou gerar ressalva explicita.
3. Ajuste de baixa materialidade pode ser agrupado, mas nao deve sumir da auditoria.
4. Evidencia nao altera valor calculado por si so.
5. Evidencia explica, sustenta, bloqueia ou ressalva.

## Ponto de decisao

Definir se a materialidade sera:

- calculada automaticamente;
- informada pelo analista;
- combinacao das duas.

Preferencia tecnica:

- calcular materialidade default;
- permitir revisao controlada;
- registrar justificativa quando houver override.

