# 02 - Spec oficial da camada declarada

## Objetivo

Criar uma especificacao oficial da camada declarada.

## Ponto de decisao

Decidir se a camada declarada sera documentada em uma spec propria ou dentro da spec do plano referencial/metodologia.

## Arquivos correlatos

- `docs/reference/ajuste_modulo_principal.md`
- `docs/specs/spec-00-visao-geral-e-decisoes-arquiteturais.md`
- `docs/specs/spec-02-ingestao-validacao-normalizacao-ecd.md`
- `docs/specs/spec-04-motor-calculo-plr-capag-auditoria-pendencias.md`
- `docs/specs/spec-05-exportacao-excel.md`
- `docs/specs/spec-09-dfc-direto-completo-fca.md`

## Detalhamento

- Definir o termo "camada declarada".
- Definir que `I051` e a classificacao referencial declarada.
- Definir que a camada declarada responde:
  - "qual e o resultado se a ECD for aceita conforme entregue?"
- Definir que a camada declarada nao audita se o contador classificou certo.
- Definir que a camada declarada pode apontar problemas de cobertura metodologica.
- Definir saidas esperadas:
  - PLR declarado;
  - FCO declarado;
  - CAPAG-e declarada;
  - auditoria declarada;
  - contas sem vinculo referencial;
  - codigos sem regra metodologica;
  - codigos com regra ampla demais, se detectavel.

## Entregavel

Spec oficial da camada declarada.

## Criterios de sucesso

- O modulo declarado fica separado do modulo comportamental.
- O papel do `I051` fica claro.
- O escopo funcional fica testavel.

## Fora do escopo

- Implementar mudancas.
- Definir score comportamental.

