# 04 - Normalizacao comportamental

## Objetivo

Definir normalizacoes especificas para analise comportamental, sem alterar a camada declarada.

## Ponto de decisao

Decidir quais normalizacoes entram no MVP.

## Arquivos correlatos

- `src/capag/io/ecd_normalizer.py`
- futuro `src/capag/engine/behavioral.py`
- futuro `src/capag/assets/behavioral/`
- `tests/unit/`

## Normalizacoes previstas

- datas em formato ISO;
- valores em `Decimal`;
- indicador debito/credito preservado;
- texto original preservado;
- texto normalizado para analise;
- remocao de acentos para metricas textuais;
- espacos duplicados;
- abreviacoes comuns:
  - `FORNEC.` -> `FORNECEDOR`;
  - `FORN` -> `FORNECEDOR`;
  - `NF` -> `NOTA FISCAL`;
  - `DUPL` -> `DUPLICATA`;
  - `PGTO` -> `PAGAMENTO`;
  - `REC` -> `RECEBIMENTO`;
  - `C/C` -> `CONTA CORRENTE`.

## Detalhamento

- Definir o que e normalizacao para analise e o que e dado original.
- Garantir que normalizacao textual nao destrua evidencia auditavel.
- Definir se abreviacoes ficam em codigo ou asset versionado.

## Entregavel

Contrato de normalizacao comportamental.

## Criterios de sucesso

- O sistema pode calcular sinais textuais sem perder o texto original.
- Normalizacao nao vira classificacao por palavra-chave.

## Fora do escopo

- Usar IA generativa para normalizar texto.
- Persistir dados normalizados em banco antes da decisao arquitetural transversal.
