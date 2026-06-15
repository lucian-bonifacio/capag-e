# 20 - Testes e validacao do MVP

## Objetivo

Planejar testes para o modulo reclassificado.

## Arquivos correlatos

- `tests/unit/`
- `tests/integration/`
- `tests/fixtures/ecd/`
- `tests/golden/`
- futuro `tests/unit/test_behavioral_*.py`
- futuro `tests/integration/test_behavioral_flow.py`

## Testes necessarios

- montagem do razao por conta;
- identificacao de contrapartidas simples;
- tratamento conservador de lancamentos compostos;
- metricas financeiras;
- metricas textuais;
- metricas hierarquicas;
- regras de fornecedores;
- regras de clientes;
- regras de bancos;
- regras de adiantamento a fornecedores;
- regras de imobilizado;
- regras de despesas;
- regras de receitas;
- score e limiares;
- diferenca entre primeiro e segundo colocado;
- estados manter/reclassificar/revisar/sem conclusao;
- payload da API;
- exportacao comparativa;
- regressao para nao alterar camada declarada.

## Criterios de sucesso

- O MVP classifica contas obvias.
- Casos ambiguos vao para revisao.
- O resultado declarado permanece intacto.

## Fora do escopo

- Testar banco de dados antes de uma arquitetura de persistencia aprovada.
- Testar precedentes persistidos antes da decisao de persistencia.
