# TASK-085D - Estudar workflow simples e deterministico

## SPEC De Origem

- `specs/SPEC-009-modulo-8-governanca-metodologia.md`

## Dependencias

- `TASK-085C-criar-skill-agent-workflow.md`

## Objetivo

Estudar e propor um modelo operacional usuario-agente mais simples e
deterministico, centrado na TASK governada, orientado por estados, eventos e
transicoes explicitas, sem assumir a permanencia dos estados atuais e sem
alterar arquivos executaveis de governanca antes de conclusao, decisao e
autorizacao do usuario.

## Contexto Preservado Para Retomada

- O fluxo atual foi percebido como procedural, distribuido e complexo, com
  condicionais espalhadas entre `AGENTS.md`, TASKs, ROADMAP, logs e skills.
- O objetivo orientador e: **simples + deterministico**.
- A hipotese principal e trocar condicionais narrativas e distribuidas por uma
  maquina de estados com a forma:

```text
estado atual + evento + guardas aplicaveis
        -> acao deterministica + proximo estado
```

- A unidade central proposta nao e apenas o arquivo da TASK, mas a TASK
  governada como conjunto:

```text
TASK governada
|- TASK: contrato e escopo
|- ROADMAP: estado persistente
|- LOG: historico e evidencias
|- SPEC, PRD, arquitetura e docs: contexto duravel referenciado
`- conversa: contexto temporario da sessao
```

- A sessao deve ser uma executora temporaria: identifica a TASK, carrega o
  contexto duravel, interpreta a mensagem atual e aplica a transicao prevista.
- Decisoes da conversa que precisem sobreviver devem ser registradas no
  artefato governado apropriado.
- `AGENTS.md` deve continuar sendo considerado o orquestrador. A proposta a
  estudar e torna-lo menor e mais deterministico: inicializar a sessao,
  carregar a TASK e o contexto, identificar o evento, aplicar a transicao,
  acionar a skill e garantir persistencia e evidencia.
- Skills operacionais devem ser avaliadas como handlers/activities acionados
  pelo orquestrador. Skills globais nao devem necessariamente ser repetidas em
  todas as TASKs; uma TASK registraria skill apenas quando ela fosse requisito
  especifico de seu contrato.
- A lista de eventos deve ser pequena e estavel. Cada mensagem gera uma
  ocorrencia de evento; nao se cria um novo tipo de evento a cada interacao.
- Mensagem ambigua deve produzir um evento seguro como `nao_classificado`,
  cuja acao e pedir um esclarecimento curto sem alterar o estado.
- Perguntas podem gerar transicoes que mantem o mesmo estado.
- Uma duvida pode revelar pedido de ajuste em mensagem posterior. Cada mensagem
  deve ser classificada separadamente; a TASK so muda quando a intencao estiver
  clara e a autorizacao exigida tiver ocorrido.
- Grupos devem ser estudados como fila de TASKs individuais usando a mesma
  maquina, e nao como fluxo paralelo, salvo evidencia contraria.
- O usuario deseja redefinir os estados. `aguardando_homologacao` nao deve ser
  preservado por premissa: sua remocao, substituicao ou transformacao em evento,
  gate ou politica deve ser estudada.
- A reflexao deve continuar com uma pergunta por vez, em linguagem calma e
  didatica.

## Tabela Comparativa Inicial Obrigatoria

Esta tabela deve ser preservada, validada e aprofundada no estudo:

| Proposta CAPAG | Conceito profissional relacionado |
| --- | --- |
| Estado + evento -> acao + proximo estado | Maquina de estados finita |
| Eventos documentados e handlers acionados | Arquitetura orientada a eventos |
| Fluxos e estados desenhados | Statecharts e BPMN |
| `AGENTS.md` como orquestrador | Workflow orchestration |
| Skills executando acoes especializadas | Handlers ou activities |
| TASK + estado + contexto + historico | Agregado, em Domain-Driven Design |
| Log persistente e retomada | Event log ou durable execution |
| Transicoes reproduziveis a partir do historico | Determinismo e replay de workflows |

Referencias e familias profissionais que devem integrar o estudo comparativo:

- maquinas de estados finitas;
- statecharts, incluindo o trabalho de David Harel;
- BPMN e materiais da Object Management Group;
- SCXML e materiais do W3C, se aplicavel;
- arquitetura orientada a eventos;
- agregados de Domain-Driven Design;
- AWS Step Functions;
- Temporal;
- Cadence, originado na Uber;
- Microsoft Durable Functions;
- Netflix Conductor;
- XState;
- GitHub Actions como referencia familiar de evento -> workflow -> acao.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `AGENTS.md`
- `docs/governance/workflow.md`
- `.agents/skills/agent-workflow/SKILL.md`
- `.agents/skills/scope-resolution/SKILL.md`
- `.agents/skills/task-planner/SKILL.md`
- `.agents/skills/roadmap-manager/SKILL.md`
- `.agents/skills/execution-log/SKILL.md`
- `tasks/README.md`
- `tasks/TASK-085C-criar-skill-agent-workflow.md`
- `logs/LOG-085C-criar-skill-agent-workflow.md`
- `ROADMAP.md`
- Fontes oficiais dos conceitos, padroes e produtos listados na tabela
  comparativa, autorizadas pelo usuario para esta pesquisa.

## Escopo Exato

- Produzir estudo comparativo entre o fluxo CAPAG atual, a hipotese orientada a
  estados/eventos e as abordagens profissionais listadas nesta TASK.
- Diferenciar claramente conceito consolidado, pratica de mercado, produto de
  referencia e adaptacao especifica do CAPAG.
- Redefinir os estados a partir de seus significados e invariantes, sem herdar
  automaticamente `pendente`, `aguardando_homologacao` ou `concluido`.
- Estudar especificamente se homologacao deve ser estado, evento, gate,
  politica opcional ou combinacao desses elementos.
- Definir o que e estado persistente e o que e acao ou condicao transitoria.
- Definir a TASK governada como unidade central e explicitar como seu contexto
  duravel e temporario e carregado.
- Propor catalogo minimo e estavel de eventos, incluindo evento seguro para
  intencao ambigua ou nao classificada.
- Propor matriz de transicoes na forma estado + evento + guarda -> acao +
  proximo estado.
- Definir comportamento para evento invalido no estado atual.
- Avaliar guardas, gates de excecao, autorizacao, idempotencia, repeticao de
  mensagem, interrupcao e retomada de sessao.
- Modelar duvidas, ajustes, autorizacoes, aprovacoes e reflexoes sem criar
  fluxos paralelos desnecessarios.
- Definir o papel proposto de `AGENTS.md` como orquestrador.
- Definir o papel proposto das skills como handlers/activities e quando uma
  skill precisa ou nao constar explicitamente em uma TASK.
- Avaliar grupos como filas de TASKs individuais submetidas a mesma maquina de
  estados.
- Testar a proposta contra cenarios reais ja vividos no projeto.
- Recomendar um modelo-alvo minimo, com trade-offs, lacunas e limites de
  determinismo claramente declarados.
- Produzir um plano de propagacao futura, sem executa-lo: workflow, `AGENTS.md`,
  skills, TASK template, ROADMAP, logs e validacoes automatizadas.

## Dimensoes Do Estudo Comparativo

Cada abordagem profissional deve ser comparada, quando aplicavel, por:

- unidade central de execucao;
- representacao de estado;
- modelo de eventos;
- transicoes e guardas;
- orquestrador e executores;
- persistencia e historico;
- determinismo e replay;
- idempotencia e eventos repetidos;
- erros, retries, timeouts e compensacao;
- intervencao e aprovacao humana;
- auditoria e rastreabilidade;
- versionamento e evolucao do workflow;
- representacao humana e representacao machine-readable;
- complexidade operacional;
- aplicabilidade a interacao usuario-agente do CAPAG.

## Hipoteses Que Devem Permanecer Abertas

- A TASK governada e realmente a melhor unidade central?
- Quantos estados persistentes sao indispensaveis?
- `aguardando_homologacao` deve ser removido, renomeado ou reclassificado?
- Homologacao deve existir para toda TASK, apenas por risco, ou ser substituida
  por outro mecanismo?
- Execucao e estado persistente ou apenas acao transitoria?
- Reflexao de governanca altera o estado da TASK ativa ou ocorre em paralelo
  sem mutacao?
- Um unico catalogo de eventos cobre TASK individual, grupo e governanca?
- Quem classifica a mensagem: `AGENTS.md`, uma skill roteadora ou outro
  contrato?
- Onde a matriz canonica deve viver e como evitar duplicacao com `AGENTS.md`?
- O primeiro modelo deve permanecer documental ou ganhar representacao YAML ou
  JSON validavel?

## Fora De Escopo

- Alterar `AGENTS.md` durante esta TASK de estudo.
- Alterar imediatamente skills operacionais existentes para adotar o modelo.
- Remover, renomear ou flexibilizar homologacao antes da decisao final do
  estudo e de autorizacao especifica.
- Modificar os status permitidos no `ROADMAP.md` durante o estudo.
- Atualizar `docs/governance/workflow.md` com um modelo-alvo ainda nao aprovado.
- Implementar engine, parser, schema YAML/JSON ou automacao de transicoes.
- Alterar produto, arquitetura da aplicacao, backend, frontend, API, metodologia
  prudencial ou padrao visual.
- Criar TASKs de propagacao antes da conclusao do estudo e da autorizacao do
  usuario.

## Passos Executaveis

1. Retomar a sessao lendo esta TASK, `TASK-085C`, seu log,
   `docs/governance/workflow.md`, `AGENTS.md` e as skills operacionais citadas.
2. Informar ao usuario que o checkpoint foi recuperado e que a conversa
   continuara com uma pergunta por vez.
3. Pesquisar fontes oficiais e primarias para os conceitos, padroes e produtos
   listados na tabela comparativa.
4. Criar `docs/governance/workflow-state-event-study.md` com a tabela inicial
   preservada e a comparacao por todas as dimensoes previstas.
5. Separar o que e fundamento profissional consolidado do que e adaptacao
   proposta especificamente para o CAPAG.
6. Explicar ao usuario os resultados da pesquisa de forma didatica, uma decisao
   por vez, antes de consolidar o modelo-alvo.
7. Comecar a redefinicao dos estados sem assumir os status atuais. A primeira
   pergunta da retomada conceitual deve ser:

```text
Quando voce pensa no estado de uma TASK, ele deve representar principalmente
o que ja aconteceu, o que esta aguardando uma decisao ou qual e a proxima acao
permitida?
```

8. Definir criterios para estados: poucos, mutuamente exclusivos, observaveis,
   persistentes quando necessario e com significado operacional unico.
9. Avaliar `aguardando_homologacao` separadamente como estado, evento, gate ou
   politica e registrar trade-offs de cada opcao.
10. Definir a unidade central e o carregamento de contexto duravel e temporario.
11. Definir o catalogo minimo de eventos, distinguindo definicao de evento de
    ocorrencia de evento em cada mensagem.
12. Definir tratamento deterministico para mensagem ambigua, multiplas
    intencoes na mesma mensagem e evento invalido no estado atual.
13. Construir a matriz de transicoes com acoes, proximos estados, guardas e
    handlers responsaveis.
14. Definir o papel de `AGENTS.md` e das skills no modelo, sem edita-los.
15. Avaliar se skills operacionais globais devem ficar apenas no roteamento do
    orquestrador e quais skills especificas precisam constar nas TASKs.
16. Modelar grupo como fila da maquina individual e comparar com um fluxo de
    grupo dedicado.
17. Testar a matriz contra, no minimo: inicio de sessao, autorizacao simples,
    pergunta sem mudanca, duvida que revela ajuste, autorizacao de ajuste,
    aprovacao, nova TASK, nova SPEC, gate de excecao, grupo, interrupcao,
    retomada e reflexao de governanca.
18. Verificar se a mesma combinacao de estado, evento e guarda sempre produz a
    mesma acao e o mesmo proximo estado.
19. Identificar onde julgamento humano continua inevitavel, especialmente na
    classificacao de linguagem natural, e definir fallback seguro.
20. Apresentar modelo-alvo minimo ao usuario, com comparacao antes/depois e
    trade-offs.
21. Somente apos aprovacao, atualizar o estudo com a decisao final e propor as
    TASKs de propagacao necessarias.

## Roteiro Da Proxima Sessao

1. Recuperar o checkpoint pelos arquivos desta TASK.
2. Nao alterar arquivos executaveis de governanca.
3. Executar primeiro a pesquisa comparativa e consolidar suas fontes.
4. Apresentar os achados em blocos curtos, sem despejar toda a pesquisa de uma
   vez.
5. Retomar a entrevista pela pergunta registrada no passo 7.
6. Fazer uma unica pergunta por vez e aguardar a resposta antes de avancar.
7. Nao assumir que `aguardando_homologacao` continuara existindo.
8. Registrar decisoes amadurecidas no estudo; manter hipoteses ainda abertas
   explicitamente abertas.
9. Nao transformar refinamento de redacao em mudanca estrutural.
10. Encerrar cada bloco recapitulando apenas a decisao tomada e a proxima
    pergunta.

## Arquivos Ou Areas Provaveis

- `docs/governance/workflow-state-event-study.md`
- `logs/LOG-085D-estudar-workflow-simples-deterministico.md`
- `ROADMAP.md`

## Criterios De Aceite

- Existe estudo comparativo baseado prioritariamente em fontes oficiais.
- A tabela comparativa inicial desta TASK foi preservada, validada e ampliada.
- Todas as referencias profissionais listadas foram avaliadas ou tiveram
  inaplicabilidade justificada.
- O estudo distingue fundamentos profissionais de adaptacoes do CAPAG.
- A unidade central e o carregamento de contexto estao definidos.
- Os estados foram redefinidos sem presumir os status atuais.
- `aguardando_homologacao` recebeu comparacao explicita entre remocao,
  substituicao e reclassificacao.
- Existe catalogo minimo de eventos com fallback para intencao ambigua.
- Existe matriz de transicoes com estados, eventos, guardas, acoes, handlers e
  proximos estados.
- O papel de `AGENTS.md` como orquestrador esta definido.
- O papel das skills e sua relacao com TASKs estao definidos.
- Grupos foram comparados como fila e como fluxo dedicado.
- Os cenarios reais minimos foram simulados contra a proposta.
- Limites de determinismo diante de linguagem natural estao explicitos.
- O modelo-alvo e menor e mais simples que o fluxo atual ou a impossibilidade
  foi demonstrada objetivamente.
- Nenhum arquivo executavel de governanca foi alterado para adotar o modelo.
- A conversa de decisao foi conduzida com uma pergunta por vez.

## Validacao Esperada

- Revisao de fontes, links, autoria, escopo e data de consulta.
- Matriz comparativa completa por dimensao aplicavel.
- Revisao textual de estados, eventos, guardas, transicoes e handlers.
- Simulacao tabular dos cenarios reais previstos.
- Busca por estados ou eventos sem transicao, transicoes ambiguas e destinos
  inexistentes.
- Revisao de diff para confirmar que `AGENTS.md`, skills existentes e status
  operacionais nao foram alterados para adotar prematuramente o modelo.
- Nao ha teste de produto esperado; a TASK e de pesquisa e desenho operacional.

## Riscos

- Risco: transformar simplificacao em uma nova camada de burocracia.
  Mitigacao: exigir reducao mensuravel de estados, bifurcacoes e regras
  narrativas.

- Risco: confundir documentacao deterministica com execucao realmente
  deterministica.
  Mitigacao: declarar limites da linguagem natural e testar a matriz com
  cenarios ambiguos e repetidos.

- Risco: copiar ferramentas profissionais complexas alem da necessidade do
  CAPAG.
  Mitigacao: extrair principios, nao reproduzir plataformas inteiras.

- Risco: decidir estados antes do estudo comparativo.
  Mitigacao: manter todas as hipoteses abertas, principalmente homologacao.

- Risco: a pesquisa crescer indefinidamente por perfeccionismo.
  Mitigacao: usar as dimensoes e criterios de aceite desta TASK como limite do
  estudo.

- Risco: perder garantias atuais de autorizacao, rastreabilidade ou gates.
  Mitigacao: simular os cenarios existentes e exigir fallback seguro antes de
  recomendar propagacao.

## Bloqueios Pendentes

- Nenhum bloqueio para iniciar o estudo na proxima sessao.
- Qualquer propagacao para `AGENTS.md`, skills, ROADMAP ou templates permanece
  bloqueada ate conclusao do estudo, aprovacao do modelo e nova autorizacao.
