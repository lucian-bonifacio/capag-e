# TASK-070 - Integrar ROA + PLRA ao CAPAG-E

## SPEC De Origem

- `specs/SPEC-007-modulo-6-motor-roa-plra.md`

## Dependencias

- `TASK-050-implementar-motor-contrato-capag-e.md`
- `TASK-069-integrar-pressoes-evidencias-roa.md`

## Objetivo

Integrar `ROA Final` ao contrato CAPAG-E no método `roa_plra`, preservando `PLRA` recebido de camada externa e status de bloqueio.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Escopo Exato

- Enviar `ROA` final/parcial/bloqueado ao contrato CAPAG-E.
- Calcular `CAPAG-E = ROA Final + PLRA` somente quando componentes permitirem.
- Preservar status comparativo quando `FCA` também existir.

## Fora De Escopo

- Recalcular PLRA.
- Calcular DFC/FCA.
- Criar laudo.
- Criar UI.

## Passos Executaveis

1. Integrar saída ROA ao assessment.
2. Criar testes de `roa_plra`.
3. Criar testes de bloqueio por PLRA ou ROA.

## Arquivos Ou Areas Provaveis

- `backend/app/application/`
- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- ROA bloqueado bloqueia CAPAG-E por ROA.
- PLRA bloqueado bloqueia CAPAG-E por PLRA.
- Valores intermediários são preservados.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: método `roa_plra` ignorar status de componente.
  Mitigação: testes de status cruzados.

## Bloqueios Pendentes

Bloqueada até contrato CAPAG-E e motor ROA existirem.
