# 01 - Diagnostico do estado atual da camada declarada

## Objetivo

Entender como o sistema atual implementa a camada declarada antes de especificar ou corrigir qualquer coisa.

## Ponto de decisao

Decidir quais partes do sistema atual ja servem como base e quais precisam ser alteradas.

## Arquivos correlatos

- `README.md`
- `docs/reference/ajuste_modulo_principal.md`
- `docs/specs/spec-02-ingestao-validacao-normalizacao-ecd.md`
- `docs/specs/spec-04-motor-calculo-plr-capag-auditoria-pendencias.md`
- `docs/specs/spec-09-dfc-direto-completo-fca.md`
- `tasks/TASK-031-20260605.md`
- `src/capag/io/ecd_parser.py`
- `src/capag/io/ecd_normalizer.py`
- `src/capag/engine/plr.py`
- `src/capag/engine/fco.py`
- `src/capag/assets/reference/catalogo_referencial.csv`
- `src/capag/assets/methodology/tabela_metodologica_plr.csv`
- `src/capag/assets/methodology/tabela_metodologica_fco.csv`
- `tests/unit/`
- `tests/integration/`

## Detalhamento

- Mapear como o parser extrai `I051`.
- Mapear como o normalizador monta o mapa conta societaria -> `COD_CTA_REF`.
- Mapear como `engine/plr.py` faz matching metodologico.
- Mapear como `engine/fco.py` faz matching metodologico.
- Verificar se o matching por prefixo privilegia regras especificas.
- Verificar onde descricao referencial oficial aparece ou nao aparece.
- Verificar se `catalogo_referencial.csv` e suficiente ou se precisa virar outro artefato.
- Relacionar o diagnostico com o caso da `TASK-031`.

## Entregavel

Diagnostico objetivo da camada declarada atual.

## Criterios de sucesso

- Fica claro onde o sistema esta correto.
- Fica claro onde a metodologia ampla gera erro.
- Fica claro se o problema esta nos assets, no motor ou na documentacao.

## Fora do escopo

- Corrigir CSVs.
- Alterar motor.
- Alterar frontend.

