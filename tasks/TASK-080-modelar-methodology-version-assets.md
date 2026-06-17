# TASK-080 - Modelar MethodologyVersion e assets governados

## SPEC De Origem

- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Dependencias

- `TASK-079-criar-matriz-rastreabilidade-metodologica.md`

## Objetivo

Modelar `MethodologyVersion` e regras de publicação de assets governados, garantindo que resultados e laudos carreguem a versão usada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Escopo Exato

- Criar modelo de versão metodológica.
- Associar assets publicados a uma versão.
- Impedir retroação silenciosa sobre laudos emitidos.
- Registrar identificador `YYYYMMDD-sequencial`.

## Fora De Escopo

- Migrar todos os assets históricos.
- Alterar regras prudenciais.
- Criar UI.
- Atualizar documentos operacionais finais.

## Passos Executaveis

1. Modelar `MethodologyVersion`.
2. Criar persistência/migration, se necessário.
3. Integrar versão aos snapshots aplicáveis.
4. Criar testes de versionamento.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/repositories/`
- `backend/alembic/`
- `backend/tests/`

## Criterios De Aceite

- Resultados carregam versão metodológica.
- Mudança metodológica não altera laudo histórico.
- Versão tem identificador rastreável.

## Validacao Esperada

- Executar migrations e testes via `docker compose`.

## Riscos

- Risco: versão metodológica ser apenas texto solto.
  Mitigação: modelar contrato explícito.

## Bloqueios Pendentes

Bloqueada até matriz de rastreabilidade existir.
