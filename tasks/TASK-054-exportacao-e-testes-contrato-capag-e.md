# TASK-054 - Exportacao e testes do contrato CAPAG-E

## SPEC De Origem

- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Dependencias

- `TASK-052-criar-api-capag-assessment.md`
- `TASK-053-criar-ui-resultado-capag-e.md`

## Objetivo

Criar exportação Excel do contrato CAPAG-E e consolidar testes de domínio, API, UI e exportação, sem recalcular fora do backend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`

## Escopo Exato

- Exportar assessment com método, fórmula, valores, status e bloqueios.
- Testar métodos permitidos e bloqueios mínimos.
- Testar erro por `float`.
- Garantir que Excel não recalcula componentes.

## Fora De Escopo

- Gerar laudo.
- Implementar DFC/FCA ou ROA.
- Criar evidências do módulo 4.

## Passos Executaveis

1. Criar exportador do assessment.
2. Criar testes de contrato.
3. Validar backend/frontend via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/export/`
- `backend/tests/`
- frontend apenas se ação de exportação já estiver prevista

## Criterios De Aceite

- Exportação inclui status e limitações.
- Resultado parcial não é apresentado como final.
- Testes cobrem bloqueios mínimos.
- Nenhum recálculo ocorre no Excel.

## Validacao Esperada

- Executar testes backend e build/testes frontend via `docker compose`.

## Riscos

- Risco: exportação perder bloqueios.
  Mitigação: bloqueios são campos obrigatórios no exportador.

## Bloqueios Pendentes

Bloqueada até API e UI CAPAG-E existirem.
