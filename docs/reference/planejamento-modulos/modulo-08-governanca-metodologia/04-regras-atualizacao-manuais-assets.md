# 04 - Regras de atualizacao de manuais e assets

## Regras para manuais

1. Manual nao deve afirmar como implementado algo que ainda e planejado.
2. Manual pode ter secoes `Estado atual` e `Evolucao planejada`.
3. Mudanca em asset metodologico deve referenciar spec.
4. Mudanca em formula deve atualizar manual, spec e testes.
5. Mudanca em nomenclatura deve atualizar API/exportacao quando aplicavel.

## Regras para assets

Toda alteracao em metodologia deve ter:

- justificativa metodologica;
- referencia a spec/manual;
- teste de carregamento;
- teste de regra afetada.

## Assets atuais e futuros

- `tabela_metodologica_plr.csv`
- `politica_desagios_plr.json`
- `tabela_metodologica_fco.csv`
- `componentes_fco_direto.csv`
- `tabela_metodologica_dfc.csv`
- `componentes_dfc_direto.csv`
- `tabela_metodologica_roa.csv`
- `componentes_roa.csv`

## Criterio de sucesso

Mudanca metodologica nao deve acontecer sem rastro documental e teste.

