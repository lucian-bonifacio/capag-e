# 18 - Exportacao e laudo comparativo

## Objetivo

Planejar como a exportacao demonstrara as duas leituras: declarada e reclassificada.

## Ponto de decisao

Decidir quais abas entram no Excel do MVP.

## Abas ou secoes possiveis

- resumo dos cenarios;
- comparativo declarado vs reclassificado;
- contas reclassificadas;
- contas mantidas;
- contas em revisao;
- contas sem conclusao;
- evidencias por conta;
- justificativas;
- impacto por conta no PLR;
- impacto consolidado na CAPAG-e.

## Arquivos correlatos

- `src/capag/export/excel.py`
- `docs/specs/spec-05-exportacao-excel.md`
- `docs/specs/spec-11-gerador-laudo-capag-e.md`
- `tests/golden/`
- `tests/unit/test_excel_export.py`

## Entregavel

Spec de exportacao comparativa.

## Criterios de sucesso

- Exportacao serializa resultado calculado.
- Nao ha recalculo dentro do Excel.
- As duas leituras ficam defensaveis.

## Fora do escopo

- CSV.
- Laudo narrativo completo no MVP, salvo decisao futura.

