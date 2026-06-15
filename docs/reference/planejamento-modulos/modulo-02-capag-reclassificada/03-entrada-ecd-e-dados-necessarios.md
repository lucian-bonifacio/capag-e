# 03 - Entrada ECD e dados necessarios

## Objetivo

Definir quais dados da ECD sao necessarios para o modulo reclassificado.

## Ponto de decisao

Decidir se o parser/normalizador atual ja captura tudo que o MVP precisa ou se precisa ser expandido.

## Arquivos correlatos

- `src/capag/io/ecd_parser.py`
- `src/capag/io/ecd_normalizer.py`
- `src/capag/domain/models.py`
- `tests/fixtures/ecd/`
- `docs/specs/spec-02-ingestao-validacao-normalizacao-ecd.md`

## Registros principais

- `I050`: plano de contas, hierarquia, tipo e natureza da conta;
- `I051`: classificacao referencial original declarada;
- `I155`: saldos;
- `I200`: lancamentos;
- `I250`: partidas;
- historicos dos lancamentos e partidas;
- `J100`: referencia patrimonial ja usada pela camada declarada.

## Registros futuros possiveis

- `I052`: centro de custos;
- `I355`: saldos de contas de resultado;
- `J150`: demonstracao do resultado;
- `0150`: participantes, se disponivel e relevante.

## Detalhamento

- Mapear o que o parser ja extrai hoje.
- Mapear o que falta para razao por conta.
- Preservar linha bruta e numero de linha quando necessario para auditoria.
- Tratar historicos longos e campos opcionais.
- Manter `Decimal` para valores.
- Definir quais estruturas da ECD podem ser mantidas em memoria e quais podem virar tabelas persistidas se banco for aprovado.

## Entregavel

Contrato de entrada de dados para o modulo reclassificado.

## Criterios de sucesso

- Fica claro quais dados alimentam a analise comportamental.
- A expansao do parser fica planejada, nao acidental.

## Fora do escopo

- Implementar novo parser.
- Criar banco de dados antes da decisao arquitetural transversal.
