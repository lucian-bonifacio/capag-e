# TASK-036 - Implementar matcher metodologico declarado

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-035-estruturar-assets-camada-declarada.md`

## Objetivo

Implementar o matcher metodológico seguro da camada declarada, respeitando o `COD_CTA_REF` exato declarado na ECD, a validação/enriquecimento pelo plano referencial oficial e os status metodológicos definidos pela SPEC-002.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Implementar algoritmo de match exato para `reference_code`, exercício, leiaute, entidade e finalidade.
- Validar/enriquecer o `reference_code` contra o plano referencial oficial, sem inferir codigo alternativo.
- Retornar status previstos pela SPEC-002.
- Impedir uso de regras `BLOQUEADA`, `EM_REVISAO` e `DEPRECIADA` em cálculo novo.
- Retornar `NAO_MAPEADO_METODOLOGICAMENTE` quando nao houver regra metodologica exata para o codigo e finalidade.
- Usar `Decimal` quando valor financeiro participar de resultado.

## Fora De Escopo

- Criar regras metodológicas reais.
- Implementar parser ECD.
- Criar API, frontend, Excel ou laudo.
- Implementar camada reclassificada.

## Passos Executaveis

1. Ler assets estruturados da TASK-035.
2. Implementar matcher no backend.
3. Criar testes unitários para codigo oficial existente, codigo oficial ausente, regra exata ativa, regra ausente, regra bloqueada, regra em revisao e regra depreciada.
4. Validar que prefixos ou padroes amplos não classificam resultado final.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Regra exata ativa classifica o codigo declarado.
- Ausencia de regra exata retorna `NAO_MAPEADO_METODOLOGICAMENTE`.
- Prefixo ou padrao amplo não classifica cálculo novo.
- Código inexistente retorna status adequado.
- Testes cobrem exemplo de `2.01.01.07.01` nao classificado por `2.01.01.*`.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Conferir que não houve uso de `float`.

## Riscos

- Risco: regra ampla classificar indevidamente conta específica.
  Mitigação: matcher deve aceitar apenas regra metodologica exata e testes obrigatórios devem rejeitar prefixos.

## Bloqueios Pendentes

Bloqueada até assets mínimos da camada declarada existirem.
