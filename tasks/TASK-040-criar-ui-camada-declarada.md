# TASK-040 - Criar UI da camada declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-029-criar-shell-frontend-minimo.md`
- `TASK-039-criar-api-camada-declarada.md`

## Objetivo

Criar tela da camada declarada para exibir contas, status metodológico, alertas e auditoria básica, consumindo API sem recalcular regra de negócio.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar rota/tela de camada declarada.
- Exibir estados de loading, vazio, erro e sucesso.
- Exibir badges de status metodológico.
- Usar `.tnum` para valores financeiros.
- Consumir contrato da API sem transformar status.

## Fora De Escopo

- Recalcular metodologia no frontend.
- Criar edição de regras.
- Criar reclassificação.
- Criar exportação.
- Alterar tokens visuais.

## Passos Executaveis

1. Ler contrato da API.
2. Criar tela conforme padrões governados.
3. Criar testes frontend mínimos.
4. Validar que a UI não recalcula nem altera status.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/`
- `frontend/src/components/`
- `frontend/src/api/`

## Criterios De Aceite

- UI exibe status e valores da API.
- UI possui estados essenciais.
- Nenhuma regra prudencial existe no frontend.
- Tokens governados são preservados.

## Validacao Esperada

- Executar testes/build frontend via `docker compose`.
- Conferir ausência de cálculo de PLRA/FCO/CAPAG-E no frontend.

## Riscos

- Risco: frontend mascarar status metodológico.
  Mitigação: renderizar status recebido da API.

## Bloqueios Pendentes

Bloqueada até shell frontend e API declarada existirem.
