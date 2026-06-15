# 03 - Avaliacao de ativos e liquidacao forcada

## Objetivo

Definir o tratamento especifico para ativos que exigem avaliacao, liquidacao forcada ou justificativa operacional.

## Ativos alvo

- imoveis;
- terrenos;
- maquinas e equipamentos;
- veiculos;
- moveis e utensilios relevantes;
- ativos mantidos para venda;
- investimentos e participacoes;
- intangiveis materiais;
- direitos creditorios relevantes;
- creditos judiciais.

## Entidade principal

Planejar estrutura equivalente a `AssetValuationAssessment`.

Campos minimos:

- `assessment_id`
- `exercise_year`
- `account_code`
- `account_name`
- `reference_code`
- `macrogroup`
- `book_value`
- `default_desagio_percent`
- `default_economic_value`
- `valuation_required`
- `valuation_basis`
- `forced_liquidation_value`
- `analyst_adjusted_value`
- `final_economic_value`
- `essentiality_status`
- `evidence_id`
- `valuation_status`
- `blocks_plra`

## Classificacao de realizabilidade

- `liquidez_imediata`
- `realizavel_curto_prazo`
- `realizavel_longo_prazo`
- `liquidacao_forcada_exige_laudo`
- `ativo_operacional_essencial`
- `ativo_sem_realizabilidade`
- `ativo_condicional`

## Base de avaliacao

- `politica_interna`
- `laudo_abnt_nbr_14653`
- `documento_suporte`
- `estimativa_analista`
- `nao_aplicavel`

## Regras de calculo

1. Valor base vem da ECD.
2. Politica de desagio atual continua como default.
3. Valor de liquidacao forcada validado prevalece sobre desagio default.
4. Valor manual exige justificativa e evidencia.
5. Ativo sem realizabilidade vai a valor economico zero.
6. Ativo essencial nao deve ser automaticamente excluido.

## Criterios de sucesso

- O `PLRA` sabe diferenciar valor contabil, valor prudencial default e valor avaliado.
- A auditoria mostra a origem do valor final.
- Ativos materiais sem suporte documental nao passam silenciosamente.

