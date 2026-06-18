# TASK-066 - Exportacao e testes DFC/FCA

## SPEC De Origem

- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Dependencias

- `TASK-064-criar-api-dfc-fca.md`
- `TASK-065-criar-ui-dfc-fca.md`

## Objetivo

Criar exportação DFC/FCA e consolidar testes do módulo, preservando audit rows, componentes, pendências, evidências e status.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`

## Escopo Exato

- Exportar fluxos e linhas de auditoria.
- Incluir pendências e status do `FCA`.
- Testar fluxo com caixa, sem caixa, não classificado e pendente de evidência.

## Fora De Escopo

- Gerar laudo.
- Calcular ROA.
- Recalcular no Excel.

## Passos Executaveis

1. Criar exportador DFC/FCA.
2. Criar testes obrigatórios.
3. Validar via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/export/`
- `backend/tests/`

## Criterios De Aceite

- Exportação não recalcula `FCA`.
- Pendências materiais aparecem.
- Testes cobrem `FCA parcial`.

## Validacao Esperada

- Executar testes backend e build/testes frontend via `docker compose`.

## Riscos

- Risco: Excel transformar parcial em final.
  Mitigação: status e limitações obrigatórios.

## Bloqueios Pendentes

Bloqueada até API e UI DFC/FCA existirem.
