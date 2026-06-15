# 03 - Metodologia ROA e componentes

## Objetivo

Planejar assets internos para classificacao de contas de resultado.

## Assets futuros

- `src/capag/assets/methodology/tabela_metodologica_roa.csv`
- `src/capag/assets/methodology/componentes_roa.csv`

## Blocos ROA

- `receita_bruta`
- `deducoes_receita`
- `tributos_receita`
- `custos_operacionais`
- `despesas_operacionais`
- `resultado_financeiro`
- `resultado_nao_operacional`
- `pressoes_complementares_caixa`

## Tratamentos permitidos

- `incluir_automaticamente`
- `excluir_automaticamente`
- `condicional`

## Colunas minimas da tabela

- `codigo_referencial`
- `modo_correspondencia`
- `grupo_metodologico`
- `macrogrupo`
- `bloco_roa`
- `sinal_natural`
- `tratamento`
- `regra_principal`
- `componente_roa`
- `exige_revisao`
- `motivo_condicional`

## Criterio de sucesso

Toda conta de resultado elegivel deve cair em componente, pendencia ou exclusao auditavel.

