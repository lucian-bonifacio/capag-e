# TASK-060 - Exportacao e testes de evidencias e ativos

## SPEC De Origem

- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Dependencias

- `TASK-058-criar-api-evidencias-ativos.md`
- `TASK-059-criar-ui-evidencias-ativos.md`

## Objetivo

Incluir evidências, materialidade, avaliações de ativos, bloqueios e ressalvas na exportação, consolidando testes obrigatórios do módulo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Escopo Exato

- Exportar evidências e avaliações sem recalcular motores.
- Incluir status e justificativas.
- Testar materialidade, override, bloqueios e avaliação de ativos.

## Fora De Escopo

- Gerar laudo narrativo.
- Upload de anexos.
- Alterar regra de DFC/ROA.

## Passos Executaveis

1. Criar exportação de evidências e ativos.
2. Criar testes backend e frontend aplicáveis.
3. Validar via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/app/export/`
- `backend/tests/`
- frontend apenas se ação de exportação já existir

## Criterios De Aceite

- Exportação mostra evidências críticas pendentes.
- Avaliações de ativos preservam status.
- Testes cobrem bases zero/ausentes e override justificado.

## Validacao Esperada

- Executar testes backend e build/testes frontend via `docker compose`.

## Riscos

- Risco: exportação omitir ressalva.
  Mitigação: status e bloqueios obrigatórios.

## Bloqueios Pendentes

Bloqueada até API e UI de evidências existirem.
