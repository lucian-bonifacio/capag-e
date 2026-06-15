# 08 - Regras deterministicas por familia

## Objetivo

Definir o modelo das regras de classificacao por familia contabil.

## Ponto de decisao

Decidir onde as regras ficarao versionadas: codigo Python, CSV/JSON em assets ou combinacao dos dois.

## Arquivos correlatos

- futuro `src/capag/engine/behavioral_rules.py`
- futuro `src/capag/assets/behavioral/`
- `tests/unit/`

## Modelo de regra

Cada regra deve ter:

- familia;
- macroclasse esperada;
- evidencias positivas;
- evidencias negativas;
- pesos;
- penalidades;
- score minimo automatico;
- score minimo revisao;
- justificativas.

## Familias MVP com exemplos de evidencias

- Fornecedores:
  - saldo tipico credor;
  - creditos contra despesas/estoques/ativo;
  - debitos contra banco/caixa;
  - historicos com pagamento, boleto, duplicata, nota fiscal.
- Clientes:
  - saldo tipico devedor;
  - debitos contra receita;
  - creditos contra bancos/caixa;
  - historicos de recebimento/venda.
- Bancos:
  - nome com banco/agencia/conta corrente;
  - grande diversidade de contrapartidas;
  - alto volume de lancamentos.
- Adiantamento a fornecedores:
  - saldo devedor;
  - sinais de adiantamento;
  - relacao com fornecedores.
- Imobilizado:
  - saldo devedor carregado;
  - baixa rotatividade;
  - descricao de bem patrimonial.
- Despesas operacionais:
  - predominancia de debitos;
  - recorrencia mensal;
  - contrapartida com fornecedor/banco/folha/tributo.
- Receitas:
  - predominancia de creditos;
  - contrapartida com clientes/bancos/caixa;
  - sinais de venda/servico.

## Entregavel

Contrato das regras deterministicas.

## Criterios de sucesso

- Regras sao auditaveis.
- Pesos e penalidades sao explicaveis.
- Texto ajuda, mas nao decide sozinho.

## Fora do escopo

- Usar IA como decisor.
- Criar interface para editar regras.

