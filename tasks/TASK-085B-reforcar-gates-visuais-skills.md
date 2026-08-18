# TASK-085B - Reforcar gates visuais em skills

## SPEC De Origem

- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Dependencias

- `TASK-085A-ajustar-governanca-homologacao.md`
- `logs/LOG-ESPECIAL-002-30.07.2026-16h50min.md`

## Objetivo

Revisar e ajustar as skills operacionais governadas para criar gate forte em
ajustes de frontend, design, UI e UX, impedindo alteracoes visuais relevantes
sem referencia governada, baseline aprovado quando existir e autorizacao
expressa do usuario.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `AGENTS.md`
- `tasks/README.md`
- `.agents/skills/execution-log/SKILL.md`
- `.agents/skills/roadmap-manager/SKILL.md`
- `.agents/skills/scope-resolution/SKILL.md`
- `.agents/skills/task-planner/SKILL.md`
- `logs/LOG-ESPECIAL-002-30.07.2026-16h50min.md`

## Escopo Exato

- Revisar as skills operacionais governadas em `.agents/skills/` que orientam
  execucao de TASKs, log, roadmap, escopo e planejamento.
- Identificar onde ajustes de frontend, design, UI e UX devem ser bloqueados,
  classificados ou condicionados a autorizacao expressa.
- Exigir que TASKs ou ajustes com escopo visual identifiquem explicitamente a
  referencia visual governada antes de implementar.
- Exigir que tela anterior aprovada seja tratada como baseline visual quando
  existir.
- Exigir autorizacao expressa do usuario para mudancas visuais relevantes em
  layout, fonte, espacamento, densidade, componentes visuais, cores ou
  hierarquia visual.
- Definir que ajuste tecnico nao pode alterar padrao visual governado por
  conveniencia.
- Alinhar o fluxo de homologacao para tratar reprovacao visual relacionada ao
  grupo executado como ajuste da TASK atual ou do grupo em homologacao, sem
  criar nova TASK por padrao.
- Definir criterio para registrar comparacao objetiva com baseline aprovado
  quando houver referencia visual aplicavel.
- Atualizar `AGENTS.md` apenas se necessario para manter coerencia com as
  skills ajustadas.
- Registrar log da execucao ao final e atualizar `ROADMAP.md` conforme o fluxo.

## Fora De Escopo

- Alterar tokens, componentes, telas, CSS ou qualquer implementacao de frontend.
- Criar novo padrao visual, alterar design system ou mudar baseline aprovado.
- Alterar PRD, arquitetura, SPECs de produto, contratos de API, regra de
  dominio, formula prudencial, fonte normativa ou politica de arredondamento.
- Remover a obrigatoriedade geral de homologacao de TASKs.
- Criar nova SPEC de governanca de homologacao ou de autonomia operacional.
- Executar qualquer TASK funcional pendente.

## Passos Executaveis

1. Ler `AGENTS.md`, esta TASK, `SPEC-009`, PRD, arquitetura, docs frontend
   governados e skills operacionais aplicaveis.
2. Mapear as regras atuais das skills para execucao, log, roadmap, resolucao de
   escopo e planejamento de TASKs.
3. Identificar lacunas relacionadas a mudancas visuais relevantes,
   baseline visual, referencia aprovada e autorizacao expressa.
4. Ajustar as skills operacionais com regras objetivas de gate visual.
5. Ajustar `AGENTS.md` somente se houver regra operacional que precise ficar na
   fonte principal.
6. Validar textual e documentalmente a coerencia entre `AGENTS.md`, skills,
   docs frontend governados e `SPEC-009`.
7. Registrar log da TASK em `logs/LOG-085B-reforcar-gates-visuais-skills.md`.
8. Mover a TASK para `aguardando_homologacao` no `ROADMAP.md`.

## Arquivos Ou Areas Provaveis

- `AGENTS.md`
- `.agents/skills/execution-log/SKILL.md`
- `.agents/skills/roadmap-manager/SKILL.md`
- `.agents/skills/scope-resolution/SKILL.md`
- `.agents/skills/task-planner/SKILL.md`
- `logs/LOG-085B-reforcar-gates-visuais-skills.md`
- `ROADMAP.md`

## Criterios De Aceite

- As skills operacionais exigem referencia visual governada antes de qualquer
  implementacao ou ajuste visual.
- As skills tratam tela anterior aprovada como baseline visual quando existir.
- Mudancas visuais relevantes exigem autorizacao expressa do usuario.
- Ajustes tecnicos nao podem alterar layout, fonte, espacamento, densidade,
  componentes, cores ou hierarquia visual por conveniencia.
- Reprovacao visual relacionada a TASK ou grupo em homologacao e tratada como
  ajuste da TASK atual ou do grupo, respeitando gates.
- A necessidade de comparacao objetiva com baseline aprovado fica registrada
  quando houver referencia aplicavel.
- `AGENTS.md` e skills permanecem coerentes entre si.
- Nenhum arquivo de frontend, token visual, componente, CSS ou tela e alterado.

## Validacao Esperada

- Validacao documental por leitura de `AGENTS.md` e skills alteradas.
- Busca textual por termos relacionados a frontend, design, UI, UX, baseline,
  referencia visual, autorizacao expressa, homologacao e gate.
- Revisao de diff para confirmar que nenhum arquivo de frontend ou documento de
  design system foi alterado.
- Nao ha teste automatizado esperado, pois a TASK altera governanca documental
  e operacional.

## Riscos

- Risco: gate visual ficar subjetivo demais.
  Mitigacao: explicitar exemplos concretos de mudanca visual relevante.

- Risco: ajuste tecnico necessario ser bloqueado indevidamente.
  Mitigacao: permitir ajustes sem impacto visual relevante e exigir registro
  objetivo quando houver impacto.

- Risco: skills e `AGENTS.md` divergirem.
  Mitigacao: validar coerencia textual entre as fontes alteradas.

## Bloqueios Pendentes

- Nenhum.
