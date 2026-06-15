# 06 - Pendencias e evidencias da DFC

## Objetivo

Definir pendencias e evidencias necessarias para fluxos de caixa.

## Pendencias

Gerar pendencia quando:

- contrapartida nao possui codigo referencial;
- codigo referencial nao possui regra DFC;
- fluxo tem direcao incompativel;
- componente exige revisao;
- movimento e material e nao possui evidencia.

## Integracao com Modulo 04

Movimento material deve criar ou exigir evidencia com:

- `scope_type = fco_movement` ou `dfc_component`;
- `method_component = FCA`;
- `adjustment_type = fluxo_excluido` ou `fluxo_incluido`;
- evidencia conforme natureza do fluxo.

## Criterio de sucesso

Movimentos nao classificados ficam visiveis, auditaveis e bloqueiam o resultado final quando necessario.

