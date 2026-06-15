# 04 - Motor DFC direto e FCA

## Objetivo

Definir o comportamento do motor que calcula `FCA`.

## Entidade principal

Planejar estrutura equivalente a `DfcCalculation`.

Campos minimos:

- `automatic_value`
- `operational_flow`
- `investment_flow`
- `financing_flow`
- `fca_value`
- `status`
- `component_summaries`
- `audit_rows`
- `alerts`

## Auditoria

Planejar `DfcAuditRow` com:

- `entry_number`
- `entry_date`
- `cash_account_code`
- `cash_flow_direction`
- `counterparty_account_code`
- `counterparty_account_name`
- `counterparty_reference_code`
- `dfc_activity`
- `dfc_component_code`
- `dfc_component_label`
- `included_value`
- `final_status`
- `pending_reason`
- `history`
- `line_number`

## Formula

```text
Fluxo Operacional = entradas operacionais - saidas operacionais
Fluxo de Investimento = entradas de investimento - saidas de investimento
Fluxo de Financiamento = entradas de financiamento - saidas de financiamento
FCA = Fluxo Operacional + Fluxo de Investimento + Fluxo de Financiamento + ajustes manuais validados
```

## Regras

1. Identificar lancamentos com caixa.
2. Determinar direcao pelo sinal das linhas de caixa.
3. Classificar contrapartidas por codigo referencial.
4. Registrar `nao_classificado` quando regra faltar.
5. Registrar `fluxo_incompativel` quando direcao divergir.
6. Movimentos nao classificados nao entram no `FCA` final sem decisao manual.

## Criterio de sucesso

O `FCA` deve ser soma auditavel das tres atividades.

