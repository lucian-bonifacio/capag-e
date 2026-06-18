# TASK-075 - Gerar Excel de laudo estruturado

## SPEC De Origem

- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Dependencias

- `TASK-074-validar-status-laudo.md`

## Objetivo

Gerar saída MVP do laudo em Excel estruturado com abas de memória e seções do laudo, sem recalcular motores.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Escopo Exato

- Criar abas `laudo_resumo`, `laudo_metodologia`, `laudo_ressalvas` e `laudo_evidencias`.
- Consumir `CapagReport` e objetos calculados.
- Incluir método, fórmula, valores, bloqueios e versão metodológica.

## Fora De Escopo

- DOCX/PDF.
- Assinatura digital.
- Anexos externos.
- Recalcular PLRA, FCA, ROA ou CAPAG-E.

## Passos Executaveis

1. Criar exportador Excel do laudo.
2. Criar testes de abas e conteúdo mínimo.
3. Validar ausência de chamadas a motores.

## Arquivos Ou Areas Provaveis

- `backend/app/report/`
- `backend/app/export/`
- `backend/tests/`

## Criterios De Aceite

- Excel contém abas mínimas.
- Bloqueios e ressalvas aparecem.
- Versão metodológica aparece.
- Nenhum recálculo ocorre.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: Excel do laudo ocultar limitação.
  Mitigação: abas de ressalvas e bloqueios obrigatórias.

## Bloqueios Pendentes

Bloqueada até validação de status do laudo existir.
