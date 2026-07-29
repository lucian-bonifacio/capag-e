# TASK-108 - Validar fluxo do balanço declarado

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-101-ampliar-parser-balanco-declarado.md`
- `TASK-102-persistir-ecd-balanco-declarado.md`
- `TASK-103-reprocessar-importacoes-ecd-legadas.md`
- `TASK-104-implementar-conciliacao-balanco-declarado.md`
- `TASK-105-criar-api-balanco-declarado.md`
- `TASK-106-criar-ui-balanco-declarado.md`
- `TASK-107-integrar-validade-balanco-plra-capag.md`

## Objetivo

Consolidar os testes automatizados, a validação end-to-end e as evidências de
homologação do fluxo completo do Balanço Patrimonial declarado.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `docs/methodology/pesquisa-oficial-balanco-patrimonial-ecd.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `tasks/TASK-101-ampliar-parser-balanco-declarado.md`
- `tasks/TASK-102-persistir-ecd-balanco-declarado.md`
- `tasks/TASK-103-reprocessar-importacoes-ecd-legadas.md`
- `tasks/TASK-104-implementar-conciliacao-balanco-declarado.md`
- `tasks/TASK-105-criar-api-balanco-declarado.md`
- `tasks/TASK-106-criar-ui-balanco-declarado.md`
- `tasks/TASK-107-integrar-validade-balanco-plra-capag.md`

## Escopo Exato

- Consolidar fixtures sintéticas para todos os estados previstos na SPEC.
- Testar preservação do arquivo, parser, persistência e reprocessamento.
- Testar obrigatoriedade, seleção do `J005`, árvore, totalizadores e
  conciliação.
- Testar contratos da API e ausência de escrita em consultas.
- Testar apresentação da árvore e auditoria de componentes no frontend.
- Testar bloqueio do resultado anual final por estado inválido.
- Executar fluxo E2E via Docker Compose.
- Reimportar e validar DATAPACK e INVENTCLOUD em execuções separadas.
- Registrar resultados, limitações e evidências visuais no log da TASK.
- Confirmar ausência de `float` em valores contábeis.

## Fora De Escopo

- Criar nova regra prudencial.
- Ajustar percentuais, inclusões, exclusões ou switches.
- Aceitar divergência conhecida como balanço válido.
- Validar verdade econômica externa à ECD.
- Executar testes oficiais fora de Docker/Docker Compose.
- Homologar automaticamente a entrega.

## Passos Executaveis

1. Revisar a matriz de casos obrigatórios da `SPEC-012`.
2. Completar fixtures e testes ausentes.
3. Executar testes backend e migrations.
4. Executar testes frontend e build.
5. Executar Playwright E2E via Docker Compose.
6. Reimportar DATAPACK e INVENTCLOUD separadamente.
7. Inspecionar visualmente os fluxos principais.
8. Registrar evidências objetivas e limitações no log.

## Arquivos Ou Areas Provaveis

- `backend/tests/`
- `backend/tests/fixtures/`
- `frontend/src/test/`
- `frontend/e2e/`
- `logs/LOG-108-validar-fluxo-balanco-declarado.md`

## Criterios De Aceite

- Todos os estados gerais e por linha possuem cobertura automatizada.
- Arquivo original, hash e reprocessamento estão cobertos.
- Casos de `COD_AGL != COD_CTA` e saldo inicial diferente do final passam.
- API e frontend não recalculam nem persistem em consultas.
- Balanço inválido bloqueia resultado anual final.
- DATAPACK e INVENTCLOUD são reimportados e avaliados separadamente.
- Testes e builds aplicáveis passam via Docker Compose.
- Evidências e limitações ficam registradas no log.
- Nenhum valor contábil ou prudencial usa `float`.

## Validacao Esperada

- `docker compose` para migrations e testes backend.
- `docker compose` para testes frontend e build.
- `docker compose` para Playwright E2E.
- MCP Playwright para inspeção visual complementar, quando usado.
- Busca focada por `float` e `parseFloat`.
- Validação manual separada de DATAPACK e INVENTCLOUD.

## Riscos

- Risco: testes unitários passarem sem validar a jornada real.
  Mitigação: manter E2E e reimportações governadas.
- Risco: uma ECD de exemplo mascarar comportamento da outra.
  Mitigação: executar e registrar cada arquivo separadamente.
- Risco: omitir limitação por indisponibilidade do ambiente.
  Mitigação: registrar objetivamente qualquer validação bloqueada.

## Bloqueios Pendentes

Bloqueada até a conclusão das `TASK-101` a `TASK-107`.

