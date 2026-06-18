# TASK-029 - Criar shell frontend minimo

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-008-organizar-estrutura-frontend-minima.md`
- `TASK-027-configurar-dependencias-frontend-minimas.md`

## Objetivo

Criar shell frontend minimo conforme documentos visuais governados e validado via container, sem tela funcional, consumo de API, regra prudencial ou fluxo de negocio.

## Fontes Usadas

- `docs/architecture/architecture.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Escopo Exato

- Criar bootstrap minimo React/Vite se ausente.
- Aplicar `globals.css` existente.
- Criar estrutura visual minima de shell administrativo apenas se necessaria para validar layout base.
- Manter textos e estados sem funcionalidade de dominio.

## Fora De Escopo

- Criar dashboard funcional.
- Criar rotas de produto.
- Criar componentes de negocio.
- Consumir API.
- Recalcular dados ou aplicar metodologia.
- Alterar tokens visuais.

## Passos Executaveis

1. Verificar estrutura frontend e dependencias.
2. Criar bootstrap minimo.
3. Garantir uso dos tokens existentes.
4. Validar build, se configurado.
5. Confirmar ausencia de dominio e API.

## Arquivos Ou Areas Provaveis

- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- arquivos de bootstrap Vite/React necessarios

## Criterios De Aceite

- Frontend renderiza shell minimo ou bootstrap sem erro.
- Validacao oficial executa via Docker/Docker Compose.
- Nao ha rota funcional, API ou regra de negocio.
- Tokens governados sao preservados.

## Validacao Esperada

- Executar build/teste frontend definido, se disponivel.
- Executar `git diff --stat` e revisar escopo.

## Riscos

- Risco: shell minimo virar tela funcional.
  Mitigacao: bloquear dados, API e fluxos de negocio.

## Bloqueios Pendentes

Bloqueada ate a execucao das TASKs 008 e 027.
