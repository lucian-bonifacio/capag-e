---
name: agent-workflow
description: Conduzir reflexoes sobre governanca operacional e instrucao operacional do CAPAG, criar ou atualizar docs/governance/workflow.md com autorizacao explicita e encaminhar TASKs derivadas quando arquivos governados precisarem mudar.
---

# Agent Workflow

Use esta skill para refletir deliberadamente sobre como usuario e agente
trabalham e para manter o mapa operacional vigente em
`docs/governance/workflow.md`.

A skill separa reflexao, decisao, autorizacao, planejamento e execucao. Ela nao
transforma toda ideia em mudanca de governanca.

## Quando Usar

Acione esta skill quando o usuario:

- quiser rever o fluxo de trabalho entre usuario e agente;
- propuser mudanca de governanca operacional;
- propuser mudanca de instrucao operacional do agente;
- quiser alterar inicio de sessao, autorizacao, execucao, validacao,
  homologacao ou encerramento;
- questionar o funcionamento, gatilho ou limite de uma skill;
- relatar friccao recorrente ou perda de tempo causada pelo proprio processo;
- pedir criacao ou atualizacao de `docs/governance/workflow.md`.

Nao use esta skill para decidir requisito de produto, arquitetura, contrato de
API, regra prudencial, padrao visual ou implementacao tecnica. Esses assuntos
seguem suas fontes e skills especializadas.

## Fontes Obrigatorias

Antes de conduzir a reflexao, leia:

- `AGENTS.md`;
- `docs/governance/workflow.md`, se existir;
- `ROADMAP.md` quando a ideia puder originar TASK ou afetar o fluxo vigente;
- `tasks/README.md` quando houver possibilidade de nova TASK;
- as skills operacionais diretamente afetadas pela ideia.

Leia PRD, arquitetura e SPEC aplicavel somente quando a proposta tocar seus
contratos ou quando for necessario verificar se existe base suficiente para
uma TASK.

## Contrato De Entrada

Comece identificando:

- a ideia em uma frase;
- o problema ou experiencia que a motivou;
- o resultado desejado;
- o modo solicitado: apenas refletir, atualizar o workflow ou avaliar trabalho
  derivado.

Se faltar informacao que altere materialmente a classificacao, faca uma
pergunta curta por vez. Nao prolongue a entrevista quando ja houver base para
uma recomendacao segura.

## Fluxo

1. Declare que a sessao esta em `reflexao_governanca`.
2. Capture a ideia sem editar arquivos.
3. Separe fatos, recorrencia, risco, preferencia e hipotese.
4. Compare a proposta com o workflow e as regras executaveis vigentes.
5. Avalie impacto, evidencia, custo, reversibilidade e conflitos.
6. Classifique a ideia em uma unica categoria principal.
7. Recomende uma unica proxima acao e explique o criterio decisivo.
8. Solicite autorizacao explicita para a mutacao recomendada.
9. Execute apenas o ato autorizado.
10. Informe o resultado e se ainda existe propagacao pendente.

## Classificacoes

- `observacao`: ha aprendizado relevante, mas nenhuma acao e necessaria agora.
- `descarte`: o ganho nao justifica a mudanca ou a ideia conflita com o objetivo
  da governanca.
- `amadurecimento`: faltam recorrencia, exemplos ou evidencia para tornar a
  ideia uma regra duravel.
- `ajuste_pequeno_autorizavel`: cabe alterar apenas
  `docs/governance/workflow.md`, sem mudar diretamente o comportamento
  executavel vigente.
- `nova_task`: a decisao esta madura e ha fonte normativa suficiente para
  alterar arquivos governados executaveis.
- `nova_spec`: falta decisao normativa suficiente para planejar implementacao.
- `conflito_governado`: a proposta contraria fonte vigente, gate ou instrucao
  obrigatoria.

## Protecao Contra Perfeccionismo

Nao recomende mudanca duravel apenas porque uma redacao alternativa parece mais
completa, elegante ou simetrica.

Antes de editar, confirme pelo menos um destes fundamentos:

- problema recorrente observado;
- risco concreto relevante;
- ambiguidade que ja causou erro ou retrabalho;
- simplificacao com beneficio operacional verificavel;
- evento unico de impacto alto que justifique prevencao imediata.

Diante de evidencia fraca, prefira `observacao` ou `amadurecimento`. Encerre a
reflexao quando a decisao estiver suficientemente clara e novas rodadas
produzirem apenas refinamento marginal.

## Autorizacoes Separadas

Trate como autorizacoes independentes:

1. conversar e refletir;
2. criar ou atualizar `docs/governance/workflow.md`;
3. criar uma TASK derivada;
4. executar uma TASK criada.

Uma autorizacao nao implica a seguinte. Comentario, hipotese, pergunta, elogio
ou silencio nao autorizam mutacao.

## Atualizacao Do Workflow

Quando a classificacao for `ajuste_pequeno_autorizavel` e o usuario autorizar:

1. edite somente `docs/governance/workflow.md`;
2. mantenha apenas o mapa dos arquivos governados e o desenho do fluxo atual;
3. remova explicacoes, principios, tutoriais e historico da conversa;
4. incorpore somente decisoes aprovadas pelo usuario;
5. se a decisao exigir mudanca em `AGENTS.md`, skills ou outro arquivo
   executavel governado, identifique a propagacao pendente e encaminhe uma
   TASK derivada;
6. informe quais propagacoes, se houver, dependem de TASK futura.

Nao altere no mesmo ato `AGENTS.md`, skills existentes, templates, codigo ou
outros arquivos governados executaveis.

## Criacao De TASK Derivada

Quando a classificacao for `nova_task`:

1. use `scope-resolution` para formalizar o enquadramento conforme o fluxo
   vigente e pedir uma unica confirmacao explicita;
2. confirme que existe SPEC suficiente;
3. apresente ao usuario o alvo governado e o efeito esperado;
4. apos a autorizacao, use `task-planner`;
5. deixe `task-planner` inserir a TASK no `ROADMAP.md` por
   `roadmap-manager`;
6. nao execute a TASK criada sem nova autorizacao.

Se faltar base normativa, classifique como `nova_spec`. Se houver conflito,
pare e apresente a fonte afetada e a decisao necessaria.

## Saidas Permitidas

- recomendacao sem alteracao;
- atualizacao autorizada de `docs/governance/workflow.md`;
- encaminhamento autorizado para criacao de TASK;
- recomendacao de SPEC;
- pausa por conflito governado.

## Proibicoes

- Nao usar o workflow como backlog de ideias ou diario de conversa.
- Nao editar arquivo governado executavel diretamente por conveniencia.
- Nao usar a reflexao para contornar TASK, SPEC, gate ou homologacao pendente.
- Nao criar TASK sem classificacao e autorizacao explicita.
- Nao executar TASK no mesmo ato em que ela for criada.
- Nao continuar refinando quando o ganho marginal nao justificar o tempo.

## Resposta De Encerramento

Ao encerrar a reflexao, informe de forma curta:

- ideia avaliada;
- classificacao;
- decisao tomada;
- arquivo atualizado ou proximo passo autorizado;
- propagacoes ainda pendentes.
