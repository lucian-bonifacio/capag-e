# TASK-047 - Criar UI de revisao reclassificada

## SPEC De Origem

- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Dependencias

- `TASK-046-criar-api-camada-reclassificada.md`

## Objetivo

Criar tela de revisão comportamental para visualizar classificação reclassificada, evidências, score, confiança e aplicar revisão humana sem recalcular no frontend.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-003-modulo-2-capag-reclassificada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar rota/tela de reclassificação.
- Exibir comparação declarado vs reclassificado.
- Exibir score, confiança e salvaguardas.
- Permitir revisão humana conforme API.
- Cobrir estados loading, vazio, erro, sucesso e bloqueado.

## Fora De Escopo

- Calcular score no frontend.
- Alterar camada declarada.
- Criar laudo.
- Alterar tokens visuais.

## Passos Executaveis

1. Ler contrato da API.
2. Criar tela conforme padrões governados.
3. Criar ações de revisão consumindo API.
4. Criar testes frontend mínimos.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/`
- `frontend/src/components/`
- `frontend/src/api/`

## Criterios De Aceite

- UI não recalcula score ou regra.
- Revisão humana usa API.
- Estados essenciais existem.
- Tokens governados são preservados.

## Validacao Esperada

- Executar testes/build frontend via `docker compose`.

## Riscos

- Risco: frontend virar motor comportamental.
  Mitigação: renderizar e enviar decisões, sem calcular regra.

## Bloqueios Pendentes

Bloqueada até API reclassificada existir.
