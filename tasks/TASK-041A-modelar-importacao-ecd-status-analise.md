# TASK-041A - Modelar importacao ECD e status da analise

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041-exportacao-e-testes-camada-declarada.md`

## Objetivo

Modelar os contratos de dominio e persistencia logica para arquivo ECD, analise, exercicio e status de processamento necessarios ao fluxo real da camada declarada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041-exportacao-e-testes-camada-declarada.md`

## Escopo Exato

- Definir modelos/contratos para `Company`, `EcdFile`, `Analysis` e `Exercise`, conforme arquitetura.
- Definir status de processamento: `nao_executado`, `processando`, `concluido`, `concluido_com_pendencias`, `bloqueado`, `erro`.
- Definir campos minimos de hash, nome original, leiaute, periodo, metodologia e rastreabilidade.
- Criar testes unitarios de transicao/serializacao dos status, quando aplicavel.

## Fora De Escopo

- Criar migrations fisicas.
- Implementar upload.
- Implementar parser ECD.
- Persistir registros normalizados.
- Executar camada declarada.

## Passos Executaveis

1. Ler contratos de entidades da arquitetura e estados da SPEC-002.
2. Criar contratos de dominio ou schemas internos para importacao e analise.
3. Garantir que status parciais e de erro sejam representaveis.
4. Criar testes focados nos contratos criados.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/application/`
- `backend/tests/`

## Criterios De Aceite

- Os contratos representam arquivo ECD, analise, exercicio e status.
- Os status previstos pela SPEC-002 existem e podem ser persistidos futuramente.
- Nenhum parser, upload ou motor e implementado nesta TASK.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Conferir ausencia de `float` em caminhos alterados.

## Riscos

- Risco: modelar campos insuficientes para rastreabilidade.
  Mitigacao: seguir campos minimos da arquitetura e SPEC-002.

## Bloqueios Pendentes

Nenhum.
