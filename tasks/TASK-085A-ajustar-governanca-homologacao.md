# TASK-085A - Ajustar governanca de homologacao

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-041L-ajustar-fluxo-homologacao-por-grupo.md`
- `TASK-085-refinar-apresentacao-leitura-declarada.md`

## Objetivo

Refinar as regras operacionais de homologacao do projeto para deixar explicito como encerrar TASKs individuais e grupos de TASKs quando, durante a validacao, surgirem ajustes relacionados, problemas nao relacionados ou necessidade de criar nova TASK.

## Fontes Usadas

- `AGENTS.md`
- `.agents/skills/execution-log/SKILL.md`
- `.agents/skills/roadmap-manager/SKILL.md`
- `.agents/skills/scope-resolution/SKILL.md`
- `.agents/skills/task-planner/SKILL.md`
- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `tasks/README.md`

## Escopo Exato

- Revisar o fluxo atual de homologacao individual em `AGENTS.md`.
- Revisar o fluxo atual de homologacao por grupo em `AGENTS.md`.
- Definir regra explicita para quando um problema identificado na homologacao esta relacionado a TASK atual.
- Definir regra explicita para quando um problema identificado na homologacao nao esta relacionado a TASK atual e deve virar backlog ou nova TASK.
- Definir se, ao criar uma nova TASK durante a homologacao, a TASK validada deve ser homologada por consequencia natural quando o novo problema nao bloquear seu escopo.
- Definir o equivalente para grupos de TASKs: aprovacao integral, aprovacao parcial, ajuste de TASK afetada e criacao de backlog para problema nao relacionado.
- Ajustar `AGENTS.md` com o fluxo aprovado.
- Avaliar e ajustar as skills operacionais somente se houver desalinhamento com o novo fluxo.
- Registrar no log da TASK a regra final adotada e os arquivos alterados.
- Atualizar o ROADMAP ao final da execucao conforme o fluxo governado.

## Fora De Escopo

- Alterar regras de produto, dominio, API, metodologia prudencial, formulas ou arredondamentos.
- Implementar qualquer ajuste funcional ou visual identificado durante uma homologacao.
- Criar TASKs de produto a partir de problemas hipoteticos.
- Homologar TASKs pendentes durante a execucao desta TASK, salvo se o usuario pedir expressamente dentro do fluxo governado.
- Reescrever a governanca completa do projeto fora do tema homologacao, backlog e grupos.

## Passos Executaveis

1. Ler `AGENTS.md`, ROADMAP, esta TASK, SPEC-001, PRD, arquitetura e skills operacionais aplicaveis.
2. Mapear as regras atuais de homologacao individual e por grupo.
3. Comparar as regras atuais com a reflexao do usuario:
   - problema relacionado a TASK atual corrige antes de homologar;
   - problema nao relacionado registra no backlog ou nova TASK;
   - a TASK atual pode ser homologada normalmente quando seu escopo foi validado;
   - nova TASK entra no fluxo principal apenas quando chegar sua vez.
4. Propor redacao objetiva para `AGENTS.md`.
5. Ajustar `AGENTS.md`.
6. Ajustar skills operacionais apenas se necessario para manter coerencia.
7. Validar documentalmente que nao ha contradicao entre `AGENTS.md`, skills e ROADMAP.
8. Registrar log da execucao.
9. Mover a TASK para `aguardando_homologacao` e recalcular a proxima tarefa conforme permitido.

## Arquivos Ou Areas Provaveis

- `AGENTS.md`
- `.agents/skills/execution-log/SKILL.md`
- `.agents/skills/roadmap-manager/SKILL.md`
- `.agents/skills/scope-resolution/SKILL.md`
- `.agents/skills/task-planner/SKILL.md`
- `logs/LOG-085A-ajustar-governanca-homologacao.md`
- `ROADMAP.md`

## Criterios De Aceite

- `AGENTS.md` diferencia problema relacionado ao escopo da TASK de problema nao relacionado.
- `AGENTS.md` define como homologar TASK individual quando uma nova TASK e criada durante a homologacao.
- `AGENTS.md` define como homologar grupo de TASKs em aprovacao integral, aprovacao parcial e problema nao relacionado.
- Skills operacionais permanecem coerentes com o fluxo documentado ou sao ajustadas.
- O fluxo preserva que nenhuma TASK e marcada como `concluido` sem homologacao do usuario.
- O fluxo preserva que criar uma TASK nao autoriza sua execucao imediata.
- O ROADMAP aponta corretamente para a proxima tarefa apos a execucao.

## Validacao Esperada

- Validacao documental por leitura de `AGENTS.md` e skills alteradas.
- Busca textual por termos de status para verificar coerencia entre `pendente`, `aguardando_homologacao` e `concluido`.
- Nao ha teste automatizado esperado, pois a TASK altera governanca documental e operacional.

## Riscos

- Risco: homologar automaticamente uma TASK sem decisao do usuario.
  Mitigacao: manter exigencia explicita de homologacao do usuario para status `concluido`.

- Risco: problema relacionado ser tratado como backlog e encerrar TASK incorretamente.
  Mitigacao: exigir classificacao por `scope-resolution` antes de decidir homologacao, ajuste ou nova TASK.

- Risco: grupo de TASKs ficar ambiguo em caso de reprovacao parcial.
  Mitigacao: documentar aprovacao parcial e status da TASK afetada.

## Bloqueios Pendentes

- Nenhum.
