# TASK-106 - Criar UI do balanço declarado

## SPEC De Origem

- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`

## Dependencias

- `TASK-085-refinar-apresentacao-leitura-declarada.md`
- `TASK-105-criar-api-balanco-declarado.md`

## Objetivo

Atualizar a tela de Balanço Patrimonial para reproduzir a árvore oficial do
`J100`, mostrar o estado da base declarada e permitir auditoria das contas
componentes sem recalcular valores ou incluir decisões prudenciais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `tasks/TASK-085-refinar-apresentacao-leitura-declarada.md`
- `tasks/TASK-105-criar-api-balanco-declarado.md`

## Escopo Exato

- Consumir exclusivamente o novo payload da API do balanço.
- Renderizar a árvore pela ordem e hierarquia recebidas.
- Separar Ativo e Passivo + Patrimônio Líquido.
- Distinguir totalizadores e linhas de detalhe.
- Mostrar saldo final como valor principal e saldo inicial como informação
  secundária.
- Exibir estado geral e diferença do balanço em linguagem simples.
- Exibir estados de conciliação somente nas linhas de detalhe.
- Abrir componentes `I050/I052/I155` sob demanda em Dialog ou tela secundária.
- Usar valores tabulares e componentes/tokens governados.
- Manter a tela declarada sem switches ou decisões de inclusão/exclusão.
- Diferenciar no padrão de tela o balanço declarado da futura revisão
  prudencial com switches.
- Ajustar os documentos frontend governados somente onde essa distinção for
  necessária.
- Criar testes frontend e inspeção visual proporcional ao escopo.

## Fora De Escopo

- Somar valores no frontend.
- Reconstruir hierarquia ou estados.
- Alterar a ECD ou a camada declarada.
- Criar switches, dicas ou tratamento prudencial.
- Calcular PLRA, FCA, ROA ou CAPAG-E.
- Criar novo padrão visual fora do design system.
- Exibir tabela analítica como bloco central do balanço.

## Passos Executaveis

1. Atualizar tipos e cliente da API.
2. Ajustar o padrão governado para distinguir visão declarada e prudencial.
3. Migrar o dashboard para a árvore do `J100`.
4. Implementar estados gerais e por linha.
5. Implementar detalhe de componentes sob demanda.
6. Remover dependências visuais da hierarquia `I050` na tela do balanço.
7. Criar ou ajustar testes frontend.
8. Executar build, E2E aplicável e inspeção visual.

## Arquivos Ou Areas Provaveis

- `frontend/src/api/declared.ts`
- `frontend/src/routes/BalanceDashboardPage.tsx`
- `frontend/src/routes/BalanceDashboardPage.css`
- `frontend/src/components/dashboard/`
- `frontend/src/test/runner.test.tsx`
- `frontend/e2e/declared-layer.spec.ts`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`

## Criterios De Aceite

- Tela reproduz a ordem e a árvore do `J100`.
- Saldo final é o valor principal.
- Ativo e Passivo + PL são apresentados separadamente.
- Totalizadores e detalhes são visualmente distintos.
- Estado geral e diferenças são compreensíveis.
- Componentes podem ser auditados sem poluir o balanço principal.
- Tela declarada não contém switches.
- Nenhuma soma, conciliação ou decisão ocorre no frontend.
- Valores financeiros usam `.tnum`.
- UI respeita tokens e padrões governados.
- Estados de carregamento, vazio e erro são objetivos.

## Validacao Esperada

- Executar testes frontend via `docker compose`.
- Executar build frontend via `docker compose`.
- Executar Playwright E2E via Docker Compose quando aplicável.
- Usar MCP Playwright para inspeção visual durante execução ou homologação
  assistida, registrando seu uso no log.
- Conferir ausência de `float` e `parseFloat` nos arquivos alterados.

## Riscos

- Risco: reintroduzir cálculo no frontend.
  Mitigação: renderizar somente dados e estados fornecidos pela API.
- Risco: usuário confundir conciliação com decisão prudencial.
  Mitigação: tela declarada sem switches e com linguagem de consistência.
- Risco: alterar o padrão visual por conveniência.
  Mitigação: reutilizar componentes e atualizar documentos governados quando
  necessário.

## Bloqueios Pendentes

Bloqueada até a conclusão da `TASK-105`.

