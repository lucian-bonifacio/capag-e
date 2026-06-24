# TASK-041E - Persistir ECD normalizada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041B-criar-migrations-ecd-normalizada.md`
- `TASK-041D-implementar-parser-ecd-declarado.md`

## Objetivo

Persistir a saida normalizada do parser ECD nas tabelas operacionais da camada declarada, mantendo rastreabilidade entre arquivo, analise, exercicio e registros originais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041B-criar-migrations-ecd-normalizada.md`
- `tasks/TASK-041D-implementar-parser-ecd-declarado.md`

## Escopo Exato

- Criar repositories/casos de uso para persistir ECD normalizada.
- Persistir contas `I050`, vinculos `I051`, saldos `I155`, lancamentos `I200`, partidas `I250` e `J100`.
- Garantir transacao por arquivo/importacao.
- Preservar status de importacao e erros estruturados.
- Criar testes de persistencia com fixtures sinteticas.

## Fora De Escopo

- Criar endpoint de upload.
- Executar matcher declarado.
- Gerar snapshots declarados.
- Criar UI.

## Passos Executaveis

1. Criar caso de uso de persistencia da ECD normalizada.
2. Integrar saida do parser aos repositories.
3. Criar tratamento transacional para importacao.
4. Testar persistencia e rollback em erro.

## Arquivos Ou Areas Provaveis

- `backend/app/application/`
- `backend/app/repositories/`
- `backend/tests/`

## Criterios De Aceite

- Uma fixture ECD valida e persistida por analise/exercicio.
- Registros minimos podem ser consultados por conta e exercicio.
- Erro de importacao nao deixa persistencia parcial inconsistente.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Executar migration em PostgreSQL Docker.

## Riscos

- Risco: persistencia parcial em importacao com erro.
  Mitigacao: usar transacao por arquivo/importacao.

## Bloqueios Pendentes

Bloqueada ate migrations e parser existirem.
