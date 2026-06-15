# 02 - Entrada ECD e lancamentos de caixa

## Objetivo

Definir quais registros da ECD alimentam o motor DFC direto.

## Registros usados

- `I200`
- `I250`
- vinculo `I250 -> I050 -> I051`
- identificacao de contas de disponibilidades

## Regras

1. Entram apenas fluxos financeiros efetivos.
2. Deve existir contrapartida em disponibilidades.
3. Lancamento sem caixa nao entra na DFC.
4. Nome livre da conta nao e criterio principal.
5. Codigo referencial e a base principal de classificacao.

## Dados minimos por linha de auditoria

- numero do lancamento;
- data;
- conta caixa;
- direcao do fluxo;
- conta contraparte;
- codigo referencial da contraparte;
- historico;
- linha original quando disponivel.

## Criterio de sucesso

O motor DFC deve ser rastreavel ate o lancamento original da ECD.

