# TASK-078 - Testes do laudo CAPAG-E

## SPEC De Origem

- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Dependencias

- `TASK-076-criar-api-laudo-capag-e.md`
- `TASK-077-criar-ui-laudo-capag-e.md`

## Objetivo

Consolidar testes do gerador de laudo CAPAG-E, cobrindo status, seções, bloqueios, ressalvas, exportação Excel e ausência de recálculo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Escopo Exato

- Testar laudo final, preliminar, com ressalvas e bloqueado.
- Testar seções obrigatórias.
- Testar Excel estruturado.
- Testar API e UI.
- Testar que laudo não chama motores.

## Fora De Escopo

- Criar DOCX/PDF.
- Criar assinatura digital.
- Alterar regra de cálculo.

## Passos Executaveis

1. Criar testes backend do report.
2. Criar testes de contrato API.
3. Criar testes frontend de fluxo crítico.
4. Validar via Docker Compose.

## Arquivos Ou Areas Provaveis

- `backend/tests/`
- `frontend/src/**/*.test.*`

## Criterios De Aceite

- Laudo bloqueado não é emitido como final.
- Ressalvas aparecem.
- Excel contém abas mínimas.
- Nenhum recálculo é executado.

## Validacao Esperada

- Executar testes backend e frontend via `docker compose`.

## Riscos

- Risco: teste não detectar recálculo indevido.
  Mitigação: usar mocks/guards de motores quando aplicável.

## Bloqueios Pendentes

Bloqueada até API e UI do laudo existirem.
