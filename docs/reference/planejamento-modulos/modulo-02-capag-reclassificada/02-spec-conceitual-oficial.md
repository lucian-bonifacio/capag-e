# 02 - Spec conceitual oficial

## Objetivo

Transformar os documentos de referencia em uma spec oficial do modulo.

## Ponto de decisao

Decidir se sera criada uma spec como `docs/specs/spec-17-capag-reclassificada-analise-comportamental.md`.

## Arquivos correlatos

- `docs/reference/nova_spec_nv_modulo.md`
- `docs/reference/novo_modulo_reclass.md`
- `docs/specs/spec-00-visao-geral-e-decisoes-arquiteturais.md`
- `docs/specs/spec-02-ingestao-validacao-normalizacao-ecd.md`
- `docs/specs/spec-04-motor-calculo-plr-capag-auditoria-pendencias.md`
- `docs/specs/spec-07-evidencias-justificativas-ajustes-laudo.md`
- `docs/specs/spec-09-dfc-direto-completo-fca.md`
- `docs/specs/spec-11-gerador-laudo-capag-e.md`

## Detalhamento

- Consolidar a decisao de duas leituras paralelas.
- Definir que a camada declarada continua sendo preservada.
- Definir que a camada reclassificada gera um cenario alternativo e auditavel.
- Definir que o nucleo decisorio e deterministico.
- Definir que IA generativa, se existir no futuro, e apenas auxiliar.
- Definir escopo MVP e escopo futuro.
- Separar a arquitetura original em memoria da nova arquitetura com banco, caso aprovada no modulo 0.

## Entregavel

Spec conceitual oficial do modulo.

## Criterios de sucesso

- Os dois documentos de referencia deixam de competir como fonte solta.
- O modulo fica especificado sem contradizer a V2.
- O MVP fica separado da visao futura.

## Fora do escopo

- Implementar codigo.
- Criar banco de dados antes da decisao arquitetural transversal.
