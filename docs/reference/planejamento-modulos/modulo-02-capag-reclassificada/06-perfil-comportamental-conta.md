# 06 - Perfil comportamental por conta

## Objetivo

Definir o objeto `PerfilComportamentalConta` e suas metricas.

## Ponto de decisao

Decidir quais metricas entram no MVP e quais ficam para expansao.

## Arquivos correlatos

- `src/capag/domain/models.py`
- futuro `src/capag/domain/behavioral.py`
- futuro `src/capag/engine/behavioral_profile.py`
- `tests/unit/`

## Metricas financeiras

- total de debitos;
- total de creditos;
- saldo inicial;
- saldo final;
- saldo medio;
- saldo medio absoluto;
- quantidade de lancamentos;
- quantidade de debitos;
- quantidade de creditos;
- percentual de debitos;
- percentual de creditos;
- valor medio;
- maior lancamento;
- menor lancamento;
- meses com movimento;
- recorrencia mensal;
- volatilidade do saldo;
- conta zera no periodo;
- conta carrega saldo;
- saldo tipico devedor;
- saldo tipico credor.

## Metricas de contrapartida

- principais contrapartidas por valor;
- principais contrapartidas por quantidade;
- percentuais contra bancos, caixa, fornecedores, clientes, receitas, despesas, estoques, imobilizado, tributos, folha e partes relacionadas;
- quantidade de familias de contrapartes;
- concentracao top 1;
- concentracao top 5.

## Metricas textuais

- tokens do nome da conta;
- tokens dos historicos;
- palavras frequentes;
- sinais de banco, agencia, conta corrente, nota fiscal, boleto, pagamento, recebimento, salario, imposto, emprestimo, adiantamento, cliente, fornecedor, estoque, imobilizado, depreciacao, receita e despesa.

## Metricas hierarquicas

- grupo pai;
- grupo avo;
- caminho hierarquico;
- natureza do grupo superior;
- conta analitica ou sintetica;
- nivel da conta;
- contas irmas;
- padrao de nomenclatura das contas irmas.

## Entregavel

Modelo do perfil comportamental.

## Criterios de sucesso

- Cada conta analisada tem evidencias estruturadas.
- O score nao depende apenas de palavras-chave.

## Fora do escopo

- Definir pesos finais.
- Mapear codigo referencial final.

