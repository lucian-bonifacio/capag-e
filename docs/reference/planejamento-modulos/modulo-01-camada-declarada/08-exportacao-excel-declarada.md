# 08 - Exportacao Excel da camada declarada

## Objetivo

Planejar como a camada declarada deve aparecer no workbook Excel sem recalculo dentro da exportacao.

## Ponto de decisao

Decidir quais abas e colunas precisam ser ajustadas para refletir plano oficial, metodologia e auditoria declarada.

## Arquivos correlatos

- `docs/specs/spec-05-exportacao-excel.md`
- `src/capag/export/excel.py`
- `src/capag/domain/models.py`
- `src/capag/engine/audit.py`
- `tests/unit/test_excel_export.py`
- `tests/golden/`

## Detalhamento

- Revisar abas obrigatorias atuais:
  - `resumo_executivo`;
  - `campos_resultado`;
  - `memoria_calculo`;
  - `fco_status`;
  - `alertas_pendencias`;
  - `log_auditoria`;
  - `inconsistencias`;
  - `sem_vinculo_ref`.
- Definir colunas para mostrar:
  - conta societaria;
  - `COD_CTA_REF` declarado;
  - descricao oficial;
  - regra metodologica aplicada;
  - tratamento PLR/FCO;
  - valor considerado;
  - status final.
- Garantir que exportacao apenas serialize estado ja calculado.

## Entregavel

Plano de ajuste da exportacao declarada.

## Criterios de sucesso

- O Excel permite auditar a cadeia declarada completa.
- Exportacao nao recalcula regra.

## Fora do escopo

- Gerar laudo.
- Exportar CSV.

