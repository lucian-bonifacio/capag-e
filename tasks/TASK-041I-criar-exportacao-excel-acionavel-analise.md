# TASK-041I - Criar exportacao Excel acionavel por analise

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041G-executar-camada-declarada-ecd-importada.md`
- `TASK-041-exportacao-e-testes-camada-declarada.md`

## Objetivo

Expor a exportacao Excel da camada declarada como acao oficial por analise/exercicio, consumindo snapshots gerados pela execucao real da ECD importada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-041-exportacao-e-testes-camada-declarada.md`

## Escopo Exato

- Criar endpoint de download Excel da camada declarada por analise/exercicio.
- Integrar exportador existente aos snapshots persistidos.
- Opcionalmente criar botao/acao na UI se o contrato frontend ja estiver disponivel.
- Garantir nome de arquivo e content-type adequados.
- Garantir que Excel nao recalcula regra nem contem formulas de negocio.

## Fora De Escopo

- Exportar camada reclassificada.
- Gerar laudo narrativo.
- Recalcular resultados no exportador.
- Criar CSV.

## Passos Executaveis

1. Ler exportador Excel existente.
2. Criar endpoint de download por analise/exercicio.
3. Criar testes de resposta HTTP e workbook.
4. Integrar acao no frontend se aplicavel e sem ampliar escopo visual.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `backend/app/export/`
- `backend/tests/`
- `frontend/src/`, se houver acao UI minima.

## Criterios De Aceite

- Usuario consegue baixar Excel da camada declarada para analise real.
- Workbook reflete snapshots persistidos.
- Valores financeiros permanecem serializados sem `float`.
- Exportacao nao executa motor.

## Validacao Esperada

- Executar testes backend via `docker compose`.
- Executar build frontend se houver alteracao de UI.
- Conferir workbook gerado por teste.

## Riscos

- Risco: endpoint chamar motor novamente durante exportacao.
  Mitigacao: exportar somente snapshots ja persistidos.

## Bloqueios Pendentes

Bloqueada ate `POST /declared/run` gerar snapshots reais.
