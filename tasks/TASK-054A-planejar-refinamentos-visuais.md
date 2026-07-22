# TASK-054A - Planejar refinamentos visuais governados

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-085-refinar-apresentacao-leitura-declarada.md`
- `TASK-086-tabela-oficial-referencial-obrigatoria.md`
- `TASK-087-tratar-contas-sem-vinculo-referencial.md`
- `TASK-054-exportacao-e-testes-contrato-capag-e.md`

## Objetivo

Conduzir uma conversa governada com o usuario para levantar problemas visuais, UX e eventuais apontamentos funcionais nas telas da camada declarada e do resultado CAPAG-E, classificando cada item e preparando TASKs especificas para execucao posterior.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- `tasks/README.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Abrir uma sessao dedicada de levantamento com o usuario.
- Registrar os problemas visuais, UX e eventuais problemas funcionais apontados pelo usuario.
- Revisar os apontamentos contra PRD, arquitetura, SPECs aplicaveis e documentos frontend governados.
- Classificar cada apontamento como ajuste visual/UX, bug funcional, nova TASK de SPEC existente, necessidade de ajuste de SPEC ou item fora de escopo.
- Separar itens relacionados a camada declarada, resultado CAPAG-E e navegacao geral.
- Preparar proposta objetiva de TASKs derivadas, com agrupamento, prioridade sugerida, SPEC de origem provavel e validacao esperada.
- Solicitar confirmacao explicita antes de criar qualquer TASK derivada.
- Atualizar o ROADMAP somente com TASKs derivadas confirmadas pelo usuario.

## Fora De Escopo

- Implementar ajustes visuais, UX ou funcionais.
- Alterar padroes visuais governados, tokens, componentes ou arquitetura de frontend.
- Alterar contrato de API.
- Alterar regra prudencial, formula, fonte normativa, arredondamento ou classificacao metodologica.
- Criar TASK derivada sem confirmacao explicita do usuario.
- Homologar TASKs anteriores.

## Passos Executaveis

1. Ler fontes obrigatorias e confirmar o escopo da sessao de levantamento.
2. Pedir ao usuario os apontamentos visuais, UX e funcionais observados.
3. Para cada apontamento, identificar tela, fluxo, severidade, impacto e fonte governada afetada.
4. Classificar o apontamento conforme `scope-resolution`.
5. Agrupar apontamentos em propostas de TASK pequenas e verificaveis.
6. Apresentar a proposta de TASKs ao usuario para confirmacao.
7. Criar somente as TASKs confirmadas, usando `task-planner`.
8. Atualizar `ROADMAP.md` com as TASKs confirmadas, usando `roadmap-manager`.
9. Registrar log objetivo da execucao da TASK de planejamento.

## Arquivos Ou Areas Provaveis

- `tasks/`
- `logs/`
- `ROADMAP.md`
- `docs/frontend/`
- `frontend/src/routes/`
- `frontend/src/components/`

## Criterios De Aceite

- A conversa de levantamento foi conduzida e os apontamentos do usuario foram classificados.
- Itens visuais/UX e funcionais foram separados.
- Nenhum ajuste de produto foi implementado durante esta TASK.
- Toda TASK derivada proposta tem escopo pequeno, fonte governada provavel e validacao esperada.
- Nenhuma TASK derivada foi criada sem confirmacao explicita do usuario.
- O ROADMAP foi atualizado apenas com TASKs confirmadas.
- O log da TASK registra o resultado do planejamento e eventuais itens bloqueados.

## Validacao Esperada

- Validar documentalmente que a TASK segue o template obrigatorio.
- Se TASKs derivadas forem criadas, validar existencia dos arquivos em `tasks/` e entradas correspondentes em `ROADMAP.md`.
- Nao ha teste automatizado esperado, pois esta TASK e de planejamento governado e nao altera codigo de produto.

## Riscos

- Risco: misturar preferencia visual com erro funcional.
  Mitigacao: classificar cada apontamento antes de propor TASK.

- Risco: criar uma TASK ampla demais.
  Mitigacao: fatiar por tela, fluxo ou comportamento verificavel.

- Risco: propor ajuste visual que conflite com documento frontend governado.
  Mitigacao: marcar como necessidade de ajuste de SPEC/documento governado antes de implementar.

## Bloqueios Pendentes

- A parte de CAPAG-E depende da execucao das TASKs `TASK-049` a `TASK-054`.
- A criacao de TASKs derivadas depende de confirmacao explicita do usuario durante a execucao desta TASK.
