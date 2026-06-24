# TASK-041B - Criar migrations da ECD normalizada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041A-modelar-importacao-ecd-status-analise.md`

## Objetivo

Criar as tabelas relacionais para persistir arquivo ECD, analise, exercicio e dados normalizados minimos consumidos pela camada declarada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041A-modelar-importacao-ecd-status-analise.md`

## Escopo Exato

- Criar models e migration para empresas, arquivos ECD, analises e exercicios.
- Criar models e migration para contas `I050`, vinculos `I051`, saldos `I155`, lancamentos `I200`, partidas `I250` e demonstracao `J100`.
- Preservar linha original e numero de linha quando aplicavel.
- Usar `Numeric`/`Decimal` para valores contabeis.
- Criar indices por analise, exercicio, conta e codigo referencial quando necessario.

## Fora De Escopo

- Implementar parser ECD.
- Popular dados reais.
- Implementar upload.
- Rodar motor declarado.

## Passos Executaveis

1. Ler contratos de dados da SPEC-002 e arquitetura.
2. Criar models SQLAlchemy para entidades operacionais.
3. Criar migration Alembic.
4. Criar testes de persistencia minima.

## Arquivos Ou Areas Provaveis

- `backend/app/repositories/`
- `backend/alembic/versions/`
- `backend/tests/`

## Criterios De Aceite

- Tabelas da ECD normalizada existem via migration.
- Valores monetarios usam precisao decimal.
- Dados de origem preservam rastreabilidade suficiente para auditoria.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Executar migration em banco Docker.
- Conferir ausencia de `float` em models e testes.

## Riscos

- Risco: migration ficar grande demais.
  Mitigacao: limitar ao minimo exigido pela camada declarada e arquitetura.

## Bloqueios Pendentes

Nenhum.
