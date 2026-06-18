# TASK-036 - Implementar matcher metodologico declarado

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-035-estruturar-assets-camada-declarada.md`

## Objetivo

Implementar o matcher metodológico seguro da camada declarada, respeitando regra mais específica, bloqueio de prefixo amplo perigoso e status metodológicos definidos pela SPEC-002.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Implementar algoritmo de match para `reference_code`, exercício, leiaute, entidade e finalidade.
- Retornar status previstos pela SPEC-002.
- Impedir uso de regras `BLOQUEADA`, `GENERICA_PERIGOSA`, `EM_REVISAO` e `DEPRECIADA` em cálculo novo.
- Usar `Decimal` quando valor financeiro participar de resultado.

## Fora De Escopo

- Criar regras metodológicas reais.
- Implementar parser ECD.
- Criar API, frontend, Excel ou laudo.
- Implementar camada reclassificada.

## Passos Executaveis

1. Ler assets estruturados da TASK-035.
2. Implementar matcher no backend.
3. Criar testes unitários para casos seguros, genéricos e bloqueados.
4. Validar que prefixo amplo perigoso não classifica resultado final.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Regra exata ativa vence regra ampla.
- Regra genérica perigosa não classifica cálculo novo.
- Código inexistente retorna status adequado.
- Testes cobrem exemplo de prefixo amplo perigoso.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Conferir que não houve uso de `float`.

## Riscos

- Risco: regra ampla classificar indevidamente conta específica.
  Mitigação: testes obrigatórios para prefixos perigosos.

## Bloqueios Pendentes

Bloqueada até assets mínimos da camada declarada existirem.
