# TASK-041C - Criar fixtures ECD governadas

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041A-modelar-importacao-ecd-status-analise.md`

## Objetivo

Criar fixtures ECD sinteticas e governadas para validar importacao, parser, camada declarada e casos obrigatorios sem versionar dados reais sensiveis.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Escopo Exato

- Criar fixture ECD valida com `I050`, `I051`, `I155`, `I200`, `I250` e `J100`.
- Criar fixture sem `I051`.
- Criar fixture com codigo referencial ausente no plano oficial.
- Criar fixture com regra metodologica ausente.
- Criar fixture com regra bloqueada.
- Criar fixture com prefixo perigoso, incluindo caso `2.01.01.07.01` que nao pode virar fornecedor por `2.01.01.*`.
- Documentar que as fixtures sao sinteticas e nao contem ECD real.

## Fora De Escopo

- Implementar parser.
- Popular plano oficial completo.
- Criar regra prudencial real.
- Usar ECD real do usuario.

## Passos Executaveis

1. Definir diretorio governado para fixtures sinteticas.
2. Criar arquivos ECD minimos com registros relevantes.
3. Criar README das fixtures e finalidade de cada caso.
4. Criar teste de presenca/estrutura basica das fixtures.

## Arquivos Ou Areas Provaveis

- `backend/tests/fixtures/`
- `backend/tests/`

## Criterios De Aceite

- Fixtures sinteticas cobrem os casos obrigatorios de validacao da SPEC-002.
- Nenhuma fixture contem dado real sensivel.
- Fixtures estao documentadas e rastreaveis aos cenarios esperados.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Conferir que fixtures nao contem segredos ou dados reais.

## Riscos

- Risco: fixture sintetica nao representar minimamente o leiaute esperado.
  Mitigacao: manter registros pequenos, explicitos e testaveis.

## Bloqueios Pendentes

Nenhum.
