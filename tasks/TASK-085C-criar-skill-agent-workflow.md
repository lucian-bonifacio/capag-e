# TASK-085C - Criar skill agent workflow

## SPEC De Origem

- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Dependencias

- `TASK-085A-ajustar-governanca-homologacao.md`
- `TASK-085B-reforcar-gates-visuais-skills.md`

## Objetivo

Criar a skill governada `agent-workflow` para reflexao e evolucao da
governanca operacional usuario-agente, capaz de criar ou atualizar o artefato
mestre `docs/governance/workflow.md` e, quando autorizado, criar TASKs derivadas
para ajustar arquivos governados do fluxo de desenvolvimento.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `AGENTS.md`
- `tasks/README.md`
- `.agents/skills/execution-log/SKILL.md`
- `.agents/skills/roadmap-manager/SKILL.md`
- `.agents/skills/scope-resolution/SKILL.md`
- `.agents/skills/task-planner/SKILL.md`
- `ROADMAP.md`

## Escopo Exato

- Criar o artefato mestre `docs/governance/workflow.md`.
- Definir nesse artefato o fluxo operacional completo entre usuario, agente,
  `AGENTS.md`, skills, TASKs, ROADMAP, logs, autorizacao, execucao,
  homologacao, reflexao e encerramento de sessao.
- Criar a skill `.agents/skills/agent-workflow/SKILL.md`.
- Fazer a skill abrir uma sessao de reflexao sobre mudancas de governanca
  operacional e instrucao operacional.
- Fazer a skill classificar ideias como observacao, descarte, amadurecimento,
  ajuste pequeno autorizavel, nova TASK, nova SPEC ou conflito governado.
- Fazer a skill criar ou atualizar `docs/governance/workflow.md` somente
  com autorizacao explicita do usuario.
- Fazer a skill usar `task-planner` para criar TASKs derivadas quando a reflexao
  concluir que `AGENTS.md`, skills, ROADMAP ou outros arquivos governados
  precisam ser ajustados.
- Registrar regras para conter alteracoes impulsivas por perfeccionismo,
  privilegiando observacao e evidencia de recorrencia antes de mudar o fluxo.
- Registrar log da execucao e atualizar `ROADMAP.md` conforme o fluxo
  governado.

## Fora De Escopo

- Alterar imediatamente `AGENTS.md`, skills existentes ou `ROADMAP.md` para
  aplicar novas regras do modelo operacional, salvo a propria inclusao da TASK
  e o log desta execucao.
- Remover ou flexibilizar homologacao de TASKs.
- Alterar regras prudenciais, metodologia, contratos de API, padrao visual,
  arquitetura ou produto.
- Implementar qualquer funcionalidade backend ou frontend.
- Criar TASKs derivadas durante esta TASK sem conclusao explicita da reflexao e
  autorizacao do usuario.

## Passos Executaveis

1. Ler `AGENTS.md`, esta TASK, `SPEC-009`, PRD, arquitetura, `tasks/README.md`
   e skills operacionais aplicaveis.
2. Definir a estrutura inicial de `docs/governance/workflow.md`.
3. Criar `docs/governance/workflow.md` com o fluxo ponta a ponta:
   inicio de sessao, classificacao de interacoes, autorizacao, execucao,
   validacao, logs, roadmap, homologacao, reflexao de governanca e finalizacao.
4. Criar `.agents/skills/agent-workflow/SKILL.md` com gatilhos,
   entradas, classificacoes, saidas permitidas e proibicoes.
5. Incluir na skill a regra de que ela nao altera arquivos governados
   executaveis diretamente sem reflexao, decisao e autorizacao.
6. Incluir na skill o encaminhamento para criar TASKs derivadas via
   `task-planner` quando necessario.
7. Validar documentalmente coerencia com `AGENTS.md`, `scope-resolution` e
   `task-planner`.
8. Registrar log da TASK em `logs/LOG-085C-criar-skill-agent-workflow.md`.
9. Mover a TASK para `aguardando_homologacao` no `ROADMAP.md`.

## Arquivos Ou Areas Provaveis

- `docs/governance/workflow.md`
- `.agents/skills/agent-workflow/SKILL.md`
- `logs/LOG-085C-criar-skill-agent-workflow.md`
- `ROADMAP.md`

## Criterios De Aceite

- Existe `docs/governance/workflow.md` como artefato mestre do fluxo
  operacional usuario-agente.
- O artefato descreve o fluxo completo desde inicio ate finalizacao de sessao.
- Existe `.agents/skills/agent-workflow/SKILL.md`.
- A skill define quando deve ser acionada para mudancas de governanca
  operacional e instrucao operacional.
- A skill diferencia reflexao, decisao, autorizacao, criacao de TASK e
  execucao.
- A skill pode criar ou atualizar o artefato mestre quando autorizada.
- A skill encaminha criacao de TASKs derivadas via `task-planner` quando
  ajustes em arquivos governados forem necessarios.
- A skill contem regra explicita para evitar alteracoes imediatas motivadas por
  perfeccionismo sem evidencia de recorrencia ou decisao consciente.
- `AGENTS.md` e skills existentes nao sao alterados para aplicar novas regras
  fora do escopo desta TASK.

## Validacao Esperada

- Validacao documental por leitura do artefato mestre e da skill criada.
- Busca textual por termos relacionados a reflexao, autorizacao, TASK,
  `workflow.md`, governanca operacional, instrucao operacional,
  homologacao, inicio de sessao e finalizacao.
- Revisao de diff para confirmar que apenas arquivos previstos foram alterados.
- Nao ha teste automatizado esperado, pois a TASK cria governanca documental e
  skill operacional.

## Riscos

- Risco: a skill virar burocracia adicional e desacelerar decisoes simples.
  Mitigacao: definir fluxo leve, com classificacoes objetivas e saidas claras.

- Risco: o artefato mestre conflitar com `AGENTS.md`.
  Mitigacao: tratar o artefato como modelo conceitual e criar TASKs derivadas
  para propagar mudancas ao `AGENTS.md` quando autorizado.

- Risco: perfeccionismo gerar alteracoes excessivas no proprio artefato.
  Mitigacao: exigir classificacao da ideia, evidencia de recorrencia e decisao
  explicita antes de atualizar o modelo operacional.

## Bloqueios Pendentes

- Nenhum.
