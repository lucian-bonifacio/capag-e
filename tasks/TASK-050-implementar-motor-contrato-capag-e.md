# TASK-050 - Implementar motor do contrato CAPAG-E

## SPEC De Origem

- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Dependencias

- `TASK-049-modelar-contrato-dominio-capag-e.md`

## Objetivo

Implementar o motor agregador que combina `PLRA`, `FCA` e `ROA` conforme método definido, preservando valores intermediários, status, limitações e bloqueios.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Escopo Exato

- Implementar regras de fórmula da SPEC-004.
- Bloquear resultado final sem `PLRA`.
- Tratar `FCO` como `FCA parcial`.
- Preservar componentes parciais, bloqueados ou indisponíveis.
- Registrar método, fórmula e limitações.

## Fora De Escopo

- Calcular `PLRA`, `FCA` ou `ROA` internamente.
- Implementar DFC ou ROA.
- Criar frontend, Excel ou laudo.

## Passos Executaveis

1. Ler domínio CAPAG-E.
2. Implementar agregador.
3. Criar testes para métodos e bloqueios.
4. Validar ausência de `float`.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- `CAPAG-E = PLRA + FCA` exige `FCA` final para status final.
- `CAPAG-E = PLRA + ROA` exige `ROA` final para status final.
- Método não definido bloqueia resultado final.
- Componentes parciais ficam visíveis.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: resultado parcial aparecer como final.
  Mitigação: testes obrigatórios de status parcial/bloqueado.

## Bloqueios Pendentes

Bloqueada até contrato de domínio CAPAG-E existir.
