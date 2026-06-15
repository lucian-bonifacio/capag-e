# 05 - Metodologia interna do FCO declarado

## Objetivo

Revisar a tabela metodologica do FCO direto para evitar que fluxos financeiros, tributarios ou nao operacionais sejam tratados como fornecedores/clientes por prefixo amplo.

## Ponto de decisao

Decidir como o FCO declarado tratara codigos fora do fluxo operacional direto.

## Arquivos correlatos

- `docs/reference/ajuste_modulo_principal.md`
- `tasks/TASK-031-20260605.md`
- `src/capag/assets/methodology/tabela_metodologica_fco.csv`
- `src/capag/assets/methodology/componentes_fco_direto.csv`
- `src/capag/engine/fco.py`
- `src/capag/domain/models.py`
- `tests/unit/`
- `tests/integration/`
- `tests/fixtures/ecd/`

## Detalhamento

- Revisar regras amplas que tratam:
  - `2.01.01.*` como pagamentos a fornecedores;
  - `1.01.02.*` como recebimentos de clientes.
- Definir se o FCO tera `tratamento = excluir_automaticamente`.
- Definir status de auditoria para exclusoes automaticas de FCO.
- Garantir que emprestimos/financiamentos nao entrem como pagamentos operacionais.
- Garantir que tributos a recuperar nao entrem como recebimentos de clientes.
- Garantir que fornecedor real continue entrando como pagamento operacional.
- Garantir que cliente real continue entrando como recebimento operacional.

## Entregavel

Plano de ajuste da metodologia FCO declarada.

## Criterios de sucesso

- O FCO direto passa a diferenciar fluxo operacional de fluxo financeiro/tributario.
- O resultado continua auditavel por lancamento.
- O motor permanece deterministico.

## Fora do escopo

- Implementar DFC completo.
- Criar banco de dados antes da decisao arquitetural transversal.
- Corrigir classificacao no frontend.
