# 17 - Exemplo completo da conta 1725

## Objetivo

Manter um exemplo completo do problema original para guiar implementacao, testes e validacao.

## Ponto de decisao

Decidir se este exemplo vira fixture minima e teste de regressao obrigatorio.

## Entrada da ECD

Conta societaria:

- `1725`

Nome:

- `EMPRESTIMO - SICOOB CREDICITRUS - C`

`I050` esperado:

- conta analitica;
- nivel 5;
- pai relacionado a emprestimos e financiamentos no plano societario.

`I051`:

- `2.01.01.07.01`

## Consulta a tabela oficial

Codigo:

- `2.01.01.07.01`

Descricao oficial esperada:

- emprestimos e financiamentos, ou descricao oficial equivalente conforme plano referencial aplicavel.

## Consulta a metodologia

Busca esperada:

1. `2.01.01.07.01`
2. `2.01.01.07.*`
3. `2.01.01.*`

Resultado esperado:

- aplicar regra especifica `2.01.01.07.*`, se nao houver regra exata;
- nao aplicar `2.01.01.*` se ela for ampla/perigosa/bloqueada;
- nunca classificar como fornecedor apenas por comecar com `2.01.01`.

## Resultado esperado por finalidade

PLR:

- passivo financeiro ou grupo metodologico equivalente.

FCO:

- nao classificar como pagamento operacional a fornecedor;
- tratar como fluxo financeiro ou excluir do FCO operacional, conforme metodologia aprovada.

CAPAG-e:

- divida financeira/financiamento ou categoria equivalente.

Natureza do fluxo:

- financiamento.

Status:

- `MAPEADO`, se regra especifica existir;
- `NAO_MAPEADO_METODOLOGICAMENTE`, se a unica regra disponivel for ampla perigosa/bloqueada.

## Teste de regressao

O teste deve falhar se:

- `2.01.01.07.01` cair em fornecedores;
- `2.01.01.07.01` cair em pagamentos a fornecedores no FCO;
- `2.01.01.*` bloqueado for usado como classificacao final;
- a descricao oficial for inventada quando o codigo nao existir na tabela oficial.

## Criterios de sucesso

- A conta `1725` demonstra que o problema foi corrigido.
- O exemplo protege contra regressao futura.
- O fluxo evidencia a separacao entre tabela oficial e metodologia interna.

