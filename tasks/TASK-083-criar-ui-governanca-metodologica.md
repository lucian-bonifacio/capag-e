# TASK-083 - Criar UI de governanca metodologica

## SPEC De Origem

- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Dependencias

- `TASK-079-criar-matriz-rastreabilidade-metodologica.md`
- `TASK-081-validacoes-cobertura-metodologica.md`

## Objetivo

Criar UI de governança metodológica para visualizar versões, cobertura, status de assets e documentos, sem permitir edição livre de regras.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar rota `/governanca/metodologia`.
- Exibir matriz, versões, cobertura e status.
- Exibir relatório de validações.
- Bloquear edição livre de regras.

## Fora De Escopo

- Administrar metodologia pela UI.
- Editar assets.
- Alterar regras de cálculo.
- Criar aprovações multiusuário.

## Passos Executaveis

1. Criar API de leitura se necessária.
2. Criar tela conforme padrões governados.
3. Criar testes frontend mínimos.

## Arquivos Ou Areas Provaveis

- `backend/app/api/`
- `frontend/src/routes/`
- `frontend/src/components/`

## Criterios De Aceite

- UI é somente leitura para regras.
- Status de cobertura fica visível.
- Tokens governados são preservados.

## Validacao Esperada

- Executar testes/build via `docker compose`.

## Riscos

- Risco: UI virar editor livre de metodologia.
  Mitigação: somente leitura nesta TASK.

## Bloqueios Pendentes

Bloqueada até matriz e validações de cobertura existirem.
