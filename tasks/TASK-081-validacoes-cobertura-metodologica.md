# TASK-081 - Validacoes e cobertura metodologica

## SPEC De Origem

- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Dependencias

- `TASK-080-modelar-methodology-version-assets.md`

## Objetivo

Criar validações automatizadas de assets governados e relatório de cobertura metodológica.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Escopo Exato

- Validar colunas obrigatórias.
- Validar tratamentos permitidos.
- Detectar componentes ausentes.
- Listar sobreposição de prefixos.
- Listar regras sem teste associado.
- Gerar relatório de cobertura.

## Fora De Escopo

- Corrigir assets.
- Alterar metodologia.
- Criar regra prudencial.
- Atualizar UI.

## Passos Executaveis

1. Implementar validadores.
2. Gerar relatório de cobertura.
3. Integrar comando via Docker Compose.
4. Criar testes dos validadores.

## Arquivos Ou Areas Provaveis

- `backend/app/assets/`
- `backend/tests/`
- `docs/methodology/`

## Criterios De Aceite

- Relatório lista regras PLRA, DFC e ROA.
- Regras sem teste são identificadas.
- Validador não altera assets.

## Validacao Esperada

- Executar validação via `docker compose`.

## Riscos

- Risco: validador modificar asset.
  Mitigação: execução somente leitura.

## Bloqueios Pendentes

Bloqueada até `MethodologyVersion` existir.
