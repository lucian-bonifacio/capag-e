# 04 - Metodologia interna do PLR declarado

## Objetivo

Revisar a tabela metodologica do PLR para que o tratamento interno respeite especificidade do `COD_CTA_REF` e nao classifique subfamilias distintas por prefixos amplos demais.

## Ponto de decisao

Decidir quais regras PLR precisam ser especificadas, corrigidas ou testadas.

## Arquivos correlatos

- `docs/reference/ajuste_modulo_principal.md`
- `tasks/TASK-031-20260605.md`
- `src/capag/assets/methodology/tabela_metodologica_plr.csv`
- `src/capag/assets/methodology/componentes_formula_plr.csv`
- `src/capag/assets/methodology/politica_desagios_plr.json`
- `src/capag/engine/plr.py`
- `tests/unit/test_engine_plr.py`
- `tests/fixtures/ecd/`

## Detalhamento

- Revisar regras amplas como:
  - `2.01.01.*`;
  - `1.01.02.*`.
- Criar ou confirmar regras especificas para:
  - emprestimos e financiamentos;
  - tributos a recuperar;
  - passivos tributarios;
  - provisoes trabalhistas;
  - fornecedores reais;
  - clientes reais.
- Garantir que regras mais especificas prevalecam.
- Garantir que toda regra incluida automaticamente possua componente e politica de desagio quando necessario.
- Definir como registrar casos ambivalentes.

## Entregavel

Plano de ajuste da metodologia PLR declarada.

## Criterios de sucesso

- `2.01.01.07.01` nao cai como fornecedor.
- Regras amplas deixam de mascarar subfamilias importantes.
- Os testes cobrem casos claros e regressao de fornecedores/clientes reais.

## Fora do escopo

- Classificar por nome livre como regra principal.
- Implementar modulo comportamental.

