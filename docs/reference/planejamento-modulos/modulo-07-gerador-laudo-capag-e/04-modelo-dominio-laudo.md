# 04 - Modelo de dominio do laudo

## Objetivo

Definir estruturas de dominio para representar o laudo.

## Entidade `CapagReport`

Campos minimos:

- `report_id`
- `session_id`
- `company`
- `cnpj`
- `created_at`
- `assessment_method`
- `capag_p_value`
- `capag_e_value`
- `capag_e_status`
- `exercises`
- `sections`
- `warnings`
- `blocking_issues`
- `attachments_index`

## Entidade `ReportSection`

Campos minimos:

- `section_code`
- `title`
- `status`
- `summary_text`
- `tables`
- `source_refs`
- `warnings`

## Ponto de decisao

Definir se o laudo sera parte de:

- `src/capag/export/`, por ser saida; ou
- modulo proprio futuro `src/capag/report/`, por ter estrutura e validacoes proprias.

Preferencia tecnica:

- criar dominio/engine de laudo separado da exportacao;
- deixar `export` apenas serializar.

