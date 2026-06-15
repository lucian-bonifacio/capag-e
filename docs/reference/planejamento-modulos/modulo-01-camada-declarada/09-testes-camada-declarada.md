# 09 - Testes da camada declarada

## Objetivo

Planejar a cobertura de testes necessaria para garantir que a camada declarada funcione corretamente.

## Ponto de decisao

Decidir quais testes entram antes de alterar assets e motor.

## Arquivos correlatos

- `tests/unit/test_ecd_parser.py`
- `tests/unit/test_ecd_normalizer.py`
- `tests/unit/test_engine_plr.py`
- `tests/unit/test_excel_export.py`
- `tests/integration/test_api_routes.py`
- `tests/integration/test_session_flow.py`
- `tests/fixtures/ecd/`
- `src/capag/assets/methodology/`
- `src/capag/assets/reference/`

## Detalhamento

- Testar extracao do `I051`.
- Testar enriquecimento por plano referencial oficial, se implementado.
- Testar matching PLR por especificidade.
- Testar que emprestimos nao caem como fornecedores.
- Testar que tributos a recuperar nao caem como clientes.
- Testar FCO operacional vs financeiro/tributario.
- Testar payload da API com campos declarados.
- Testar exportacao das colunas declaradas.
- Criar fixture minima quando o sample real for grande demais.
- Cobrir explicitamente os cinco testes obrigatorios de `docs/reference/ajuste_modulo_principal.md`:
  - emprestimo nao pode virar fornecedor;
  - fornecedor pode virar fornecedor;
  - tributo a recuperar nao pode virar cliente;
  - prefixo bloqueado nao pode classificar;
  - regra mais especifica vence.

## Entregavel

Plano de testes da camada declarada.

## Criterios de sucesso

- A correcao do modulo 1 fica protegida contra regressao.
- Casos da `TASK-031` ficam cobertos.

## Fora do escopo

- Testar modulo comportamental.
- Testar rotas React.
