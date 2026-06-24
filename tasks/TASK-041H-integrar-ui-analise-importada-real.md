# TASK-041H - Integrar UI com analise importada real

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-041F-criar-importacao-ecd-oficial.md`
- `TASK-041G-executar-camada-declarada-ecd-importada.md`
- `TASK-040-criar-ui-camada-declarada.md`

## Objetivo

Integrar o frontend da camada declarada ao fluxo real de analise importada, substituindo dependencia de snapshot demo por analise criada a partir de ECD importada.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `tasks/TASK-040-criar-ui-camada-declarada.md`

## Escopo Exato

- Criar tela ou fluxo minimo para selecionar/importar ECD e navegar para a analise declarada real.
- Exibir status de importacao/processamento quando aplicavel.
- Permitir acionar ou acompanhar `POST /declared/run`, sem recalcular no frontend.
- Remover dependencia operacional de carga demo para homologacao manual comum.
- Preservar estados de loading, vazio, erro e sucesso.

## Fora De Escopo

- Recalcular metodologia no frontend.
- Criar editor de regras.
- Criar reclassificacao comportamental.
- Criar laudo.

## Passos Executaveis

1. Ler contratos de importacao e run declarado.
2. Integrar chamadas da API no frontend.
3. Criar navegacao para analise importada real.
4. Criar testes frontend com mocks dos contratos reais.

## Arquivos Ou Areas Provaveis

- `frontend/src/api/`
- `frontend/src/routes/`
- `frontend/src/components/`
- `frontend/src/test/`

## Criterios De Aceite

- Usuario consegue chegar na tela declarada a partir de uma analise importada real.
- UI exibe status do backend sem alterar status.
- UI nao contem regra prudencial ou matcher.

## Validacao Esperada

- Executar testes/build frontend via `docker compose`.
- Conferir ausencia de termos de calculo/matcher no frontend de producao.

## Riscos

- Risco: frontend assumir status ou simular resultado.
  Mitigacao: renderizar apenas payload da API.

## Bloqueios Pendentes

Bloqueada ate importacao oficial e `POST /declared/run` existirem.
