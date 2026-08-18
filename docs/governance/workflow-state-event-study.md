# Estudo De Workflow Simples E Deterministico

## 1. Controle Do Estudo

- TASK: `TASK-085D-estudar-workflow-simples-deterministico.md`
- Status do estudo: `em_construcao`
- Inicio: 2026-08-18
- Ultima consulta das fontes externas: 2026-08-18
- Regra de decisao: nenhuma hipotese deste documento altera o workflow vigente
  sem conclusao do estudo, decisao do usuario e autorizacao especifica.

## 2. Problema Investigado

O fluxo atual distribui condicionais entre `AGENTS.md`, TASKs, `ROADMAP.md`,
logs e skills. O estudo avalia se essa operacao pode ser reduzida a uma regra
canonica:

```text
estado atual + evento normalizado + guardas aplicaveis
        -> acoes deterministicas + proximo estado
```

A linguagem natural permanece na entrada. O objetivo nao e afirmar que a
classificacao de toda mensagem sera deterministica, mas tornar deterministico
o comportamento posterior a uma classificacao explicita, auditavel e com
fallback seguro.

## 3. Fronteiras Do Estudo

- Este documento e analitico e ainda nao define o workflow futuro aprovado.
- `AGENTS.md`, skills, templates e status vigentes nao sao alterados nesta
  TASK.
- Conceitos profissionais sao usados como referencia, nao como obrigacao de
  adotar produtos ou toda a sua complexidade.
- A maquina proposta e operacional, para interacao usuario-agente. Ela nao e
  o motor de estados do produto CAPAG-E.

## 4. Tabela Comparativa Inicial Preservada

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

## 5. Classificacao Das Referencias

| Referencia | Classe | O que ela oferece | O que ela nao decide para o CAPAG |
| --- | --- | --- | --- |
| Maquina de estados finita | Fundamento formal | Estados finitos, eventos e transicoes explicitas | Persistencia, retries, aprovacao humana ou estrutura de arquivos |
| Statecharts de David Harel | Fundamento formal ampliado | Hierarquia, ortogonalidade, historia e comunicacao | Necessidade de usar estados compostos ou paralelos |
| BPMN | Padrao de modelagem | Notacao legivel para eventos, tarefas, gateways e processos | Engine, politica de homologacao ou catalogo de eventos |
| SCXML | Recomendacao W3C executavel | Representacao XML de maquinas orientadas a eventos | Necessidade de adotar XML ou um interpretador |
| Arquitetura orientada a eventos | Estilo arquitetural | Produtores, consumidores, canais, desacoplamento e streams | Que toda mensagem precise de broker ou processamento assincrono |
| Agregado DDD | Padrao de modelagem de dominio | Fronteira de consistencia e invariantes | Que a TASK seja automaticamente um agregado de software |
| Step Functions, Temporal, Cadence, Durable Functions e Conductor | Produtos e plataformas | Execucao duravel, historico, retries e orquestracao | Que o CAPAG precise de infraestrutura distribuida |
| XState | Biblioteca e ferramenta de modelagem | Statecharts executaveis, guardas, acoes e snapshots | Persistencia duravel completa ou governanca documental |
| GitHub Actions | Produto e analogia familiar | Evento -> workflow YAML -> jobs -> steps | Workflow humano geral ou maquina de estados canonica |
| Modelo futuro do CAPAG | Adaptacao especifica | Contrato operacional minimo para usuario e agente | Permanece aberto ate as decisoes conjuntas deste estudo |

## 6. Fundamentos Profissionais

### 6.1 Maquinas De Estados Finitas E Statecharts

Uma maquina de estados torna explicitos o conjunto de estados, os eventos e
as transicoes. Ela ajuda a identificar estados impossiveis, eventos invalidos
e transicoes ausentes. O formalismo, isoladamente, nao prescreve persistencia,
logs, retries ou aprovacao humana.

O artigo de David Harel de 1987, `Statecharts: a visual formalism for complex
systems`, ampliou maquinas tradicionais para sistemas complexos. Statecharts
acrescentam principalmente hierarquia, concorrencia/ortogonalidade e historia.
Esses recursos reduzem explosao combinatoria em fluxos complexos, mas podem
ser excesso para o primeiro modelo CAPAG. A hipotese inicial e comecar com uma
maquina plana e somente promover para statechart diante de estados compostos
ou paralelos inevitaveis.

### 6.2 BPMN

A OMG define BPMN como notacao de processos compreensivel por stakeholders e
precisa o suficiente para traducao em componentes de software. BPMN e forte
para representar tarefas humanas, eventos, gateways, subprocessos e fluxos
organizacionais. Para o CAPAG, ele pode ser uma visualizacao secundaria. Usa-lo
como contrato canonico desde o inicio adicionaria vocabulario e semantica
maiores que o problema atual.

### 6.3 SCXML

A recomendacao W3C define SCXML como linguagem geral de maquinas de estados
orientadas a eventos que combina conceitos de CCXML e State Tables de Harel.
Ela especifica estados, estados paralelos, transicoes, historico, eventos,
selecao de transicoes, conteudo executavel e comunicacao externa.

SCXML demonstra que uma maquina pode ter representacao executavel padronizada.
Entretanto, XML, conformidade e semantica completa de interpretacao nao trazem
beneficio proporcional ao estudo documental inicial do CAPAG.

### 6.4 Arquitetura Orientada A Eventos

Na descricao do Azure Architecture Center, produtores geram eventos,
consumidores os processam e canais transferem os eventos. Pub/sub e event
streaming resolvem desacoplamento, alto volume e reprocessamento. Entregas
repetidas e concorrencia exigem consumidores idempotentes e coordenacao.

No CAPAG, `evento` significa o resultado operacional normalizado da
interpretacao de uma interacao ou resultado interno. Nao implica broker,
stream, assincronia ou multiplos consumidores. A analogia util e separar a
ocorrencia do evento de seu handler; a infraestrutura distribuida e inaplicavel
sem necessidade futura concreta.

### 6.5 Agregado Em Domain-Driven Design

O guia de DDD da Microsoft define agregado como fronteira de consistencia em
torno de uma ou mais entidades, com uma raiz, usada para modelar invariantes
transacionais. A analogia com a TASK governada e util porque TASK, estado,
contexto duravel e historico precisam permanecer coerentes.

A analogia tem limite: arquivos Markdown nao formam automaticamente um
agregado DDD, e o CAPAG ainda nao possui repositorio transacional ou raiz de
agregado executavel para esse workflow. O termo mais preciso durante o estudo
e `unidade governada de trabalho`, deixando `agregado` como comparacao.

## 7. Comparacao Estrutural Das Abordagens

| Abordagem | Unidade central | Estado | Eventos, transicoes e guardas | Orquestrador e executores | Persistencia e historico | Representacao | Aplicabilidade CAPAG |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Maquina de estados finita | Instancia da maquina | Um estado finito ativo | Evento seleciona transicao; condicoes podem restringi-la | Nao prescrito | Nao prescrito | Tabela, grafo ou codigo | Base canonica minima |
| Statecharts | Configuracao de estados | Simples, composto, paralelo e historico | Eventos, guardas e acoes em hierarquia | Interpretador da maquina | Nao necessariamente duravel | Diagrama e modelo executavel | Adiar ate haver complexidade real |
| BPMN | Instancia de processo | Tokens e estado das atividades/processo | Eventos, gateways e fluxos de sequencia | Engine BPMN e workers, quando executavel | Dependente da engine | Diagrama padronizado e XML | Boa visualizacao, contrato inicial pesado |
| SCXML | Sessao de interpretacao | Configuracao legal de estados | Eventos, condicoes, transicoes e conteudo executavel | Processador SCXML e invocacoes | Datamodel e historia; durabilidade externa | XML normativo | Sem beneficio proporcional agora |
| Arquitetura orientada a eventos | Evento e consumidor | Estado distribuido por consumidores | Publicacao e consumo; guardas ficam nos consumidores | Broker/canal e handlers | Log duravel apenas no modelo de stream | Schemas de eventos e codigo | Util apenas como disciplina conceitual |
| Agregado DDD | Agregado e raiz | Dados sob invariantes | Comandos/eventos de dominio; transacoes na fronteira | Application service e dominio | Repositorio transacional | Modelo de dominio e codigo | Analogia forte, nao implementacao literal |

## 8. Comparacao Dos Produtos E Ferramentas

### 8.1 Estrutura E Execucao

| Produto | Unidade central | Modelo | Orquestrador e executores | Estado, persistencia e historico | Intervencao humana | Complexidade para o CAPAG |
| --- | --- | --- | --- | --- | --- | --- |
| AWS Step Functions | Execucao de state machine | Amazon States Language, estados e tasks | Servico AWS + integracoes/workers | Standard mantem historico visual e execucao auditavel | Callback com task token pode aguardar aprovacao | Alta e dependente de AWS |
| Temporal | Workflow Execution | Workflow em linguagem de programacao | Temporal Service + Workers + Activities | Event History append-only, replay e recuperacao duravel | Signals/Updates podem entregar decisoes externas | Muito alta para fluxo documental |
| Cadence | Workflow Execution | Funcao duravel deterministica | Cadence Service + workers + activities | Event sourcing e recuperacao por replay | Signals alteram workflow em execucao | Muito alta; precursor conceitual do Temporal |
| Durable Functions | Instancia de orquestracao | Orchestrator, activity e entity functions | Runtime Azure Functions + workers | Checkpoints, event sourcing, replay, retries e recovery | Eventos externos permitem pausas longas | Alta e dependente de Azure |
| Netflix Conductor | Execucao de workflow | Grafo de tasks em JSON ou codigo | Servidor Conductor + workers desacoplados | Estado de workflow/task persistido e UI de execucao | HUMAN task para aprovacao externa | Alta; repositorio Netflix esta arquivado |
| XState | Actor/machine | Statechart em codigo ou modelo visual | Biblioteca no processo hospedeiro | Snapshot pode ser persistido/restaurado pelo host | Evento comum pode representar decisao humana | Baixa a media, mas ainda prematuro implementar |
| GitHub Actions | Workflow run | YAML com eventos, jobs e steps | GitHub + runners + actions | Historico de runs, logs e artefatos | Environments podem exigir reviewers | Boa analogia; semantica restrita a automacao CI/CD |

### 8.2 Confiabilidade, Replay E Evolucao

| Produto | Determinismo e replay | Idempotencia e repeticao | Erros, retries, timeouts e compensacao | Auditoria | Versionamento |
| --- | --- | --- | --- | --- | --- |
| AWS Step Functions | Definicao declarativa; Standard declara execucao exactly-once | Express pode ser at-least-once; tasks ainda precisam considerar efeitos externos | `Retry`, `Catch`, backoff, timeouts e workflows de compensacao modelados | Historico e depuracao visual em Standard | Versoes sao snapshots imutaveis; aliases roteiam entre versoes |
| Temporal | Workflow code deve repetir os mesmos comandos sobre o mesmo historico | Activities com efeitos externos devem ser idempotentes | Retries/timeouts nativos; compensacao e modelada pelo workflow | Event History append-only funciona como recuperacao e auditoria | Worker Versioning e patching protegem execucoes longas |
| Cadence | Workflow deterministico recuperado por event sourcing | Activities externas devem tolerar retries | Politicas de retry, backoff e timeouts; compensacao em workflow | Historico e queries/signals de execucao | Mudancas devem preservar determinismo de execucoes ativas |
| Durable Functions | Orchestrator reexecuta por replay e deve ser deterministico | Activities precisam considerar repeticao | Runtime gerencia checkpoints, retries e recovery; timers duraveis | Historico da instancia e estado persistido | Mudanca de codigo pode quebrar replay; exige estrategia explicita |
| Netflix Conductor | Grafo dirigido pelo servidor, nao replay deterministico de codigo | Workers devem tratar repeticao conforme politica de tasks | Retries, timeouts, restart, failure workflow e tasks de compensacao | UI exibe diagrama, timeline, inputs, outputs e JSON | Multiplas versoes inteiras podem coexistir |
| XState | Transicao e deterministica para estado, evento e guardas definidos | Repeticao segue as transicoes modeladas; efeitos dependem do host | Sem runtime duravel completo; erros/retries precisam ser modelados | Snapshots sao persistiveis, mas log/auditoria dependem do host | Evolucao de maquina e snapshots precisa de politica externa |
| GitHub Actions | YAML e condicoes sao reproduziveis, mas steps externos podem variar | Re-run pode repetir efeitos; actions precisam ser seguras | Timeouts, `continue-on-error`, concorrencia e tentativas modeladas por workflow/action | Runs e logs sao persistidos pelo GitHub | Workflow versionado no Git; run usa a revisao correspondente |

## 9. Achados Preliminares Para O CAPAG

### 9.1 Determinismo Tem Uma Fronteira

O limite inevitavel esta na interpretacao da linguagem natural. A mesma frase
pode carregar duvida, autorizacao, ajuste e comentario. O modelo nao deve
ocultar esse julgamento.

Depois da normalizacao, a transicao pode e deve ser deterministica:

```text
mensagem bruta
  -> classificacao explicita ou nao_classificado
  -> uma ou mais ocorrencias de evento com os dados necessarios
  -> leitura do estado persistente e das guardas
  -> uma transicao valida ou uma rejeicao segura
```

`nao_classificado` e resultado seguro da fronteira linguistica. Ele impede as
mutacoes derivadas da interacao e pede um esclarecimento curto. O estado so
muda para `aguardando_usuario` se a falta de classificacao tambem impedir toda
continuacao segura.

### 9.2 Estado Nao Deve Ser Confundido Com Acao

`executar`, `validar`, `registrar log` e `pedir esclarecimento` descrevem
acoes. Elas so devem virar estados persistentes se houver necessidade real de
retomada, exclusao mutua e regra operacional enquanto duram.

Decisao do usuario em 2026-08-18: estado representa a condicao operacional
presente da TASK no momento em que ela e lida, consultada ou planejada. Ele nao
representa primariamente o passado nem a proxima acao. O historico registra o
que aconteceu; eventos, guardas e transicoes determinam o que pode acontecer a
seguir.

Decisao do usuario em 2026-08-18: `em_execucao` representa um ciclo de execucao
autorizado, ainda nao encerrado e sem gate estrito que impeça toda continuacao
segura. Acoes do agente e interacoes humanas comuns permanecem no mesmo estado.
Somente uma mudanca duravel da condicao operacional justifica transicao.

Uma pergunta pode gerar transicao interna ou permanencia no mesmo estado. O
fato de uma mensagem exigir resposta nao obriga a criar um novo estado.

### 9.3 Evento Nao E Apenas Um Tipo Em Um Catalogo

O catalogo define tipos estaveis, por exemplo `autorizacao_de_execucao`. Cada
mensagem produz uma ou mais ocorrencias simples, ligadas a mesma origem. Essa
distincao permite detectar repeticao e tratar multiplas intencoes sem inventar
tipo composto ou novo tipo por mensagem.

### 9.4 Snapshot E Log Tem Papeis Diferentes

- `ROADMAP.md` responde qual e o estado corrente persistente.
- O log registra ocorrencias, acoes, validacoes e decisoes relevantes.
- A TASK registra contrato e escopo.
- SPEC, PRD, arquitetura e docs governados registram contexto duravel.
- A conversa e entrada temporaria; decisoes duraveis migram para o artefato
  apropriado.

O CAPAG nao precisa reconstruir todo estado exclusivamente por replay do log.
Um modelo `snapshot atual + log auditavel` e mais simples. Replay pode ser uma
validacao futura da coerencia, nao a unica forma de retomada.

### 9.5 Homologacao Ainda E Hipotese Aberta

As plataformas pesquisadas tratam aprovacao humana normalmente como evento
externo que libera uma atividade, callback ou gate. Isso mostra que
`aguardando_homologacao` nao precisa necessariamente ser estado persistente.
Tambem nao prova que deva ser removido: enquanto a TASK aguarda uma decisao,
esse fato pode restringir legitimamente as proximas acoes permitidas.

A comparacao entre estado, evento, gate e politica sera decidida depois da
definicao semantica de `estado` pelo usuario.

Decisoes do usuario em 2026-08-18: toda espera por acao humana usa um unico
estado, `aguardando_usuario`, acompanhado de contexto estruturado que informa
o motivo e a acao necessaria. `aguardando_homologacao` nao permanece como
estado distinto. Tambem nao existe aprovacao final obrigatoria ou politica
`aprovacao_final`: toda TASK conclui automaticamente depois de cumprir seu
contrato e passar nas validacoes.

Homologacao deixa de ser estado e de ser gate final universal. A conferencia
do usuario passa a ser feedback posterior a conclusao. Esse feedback pode nao
alterar a TASK, reabri-la quando seu contrato nao foi cumprido ou originar novo
escopo conforme classificacao governada.

Decisao do usuario em 2026-08-18: `concluida` pode retornar a `em_execucao`
somente quando feedback posterior demonstrar descumprimento do contrato
original ou de seus criterios. Nova necessidade nao reabre a TASK; segue o
fluxo de novo escopo. O log preserva conclusao, feedback, classificacao e
reabertura.

### 9.6 Modelo Minimo Antes De Ferramenta

A recomendacao preliminar e manter o primeiro modelo documental e tabular. Uma
representacao YAML/JSON, XState, SCXML ou engine so deve ser avaliada depois
que o vocabulario e a matriz estiverem estaveis e uma validacao automatizada
trouxer beneficio verificavel.

### 9.7 Mandato De Execucao Duravel

Decisao do usuario em 2026-08-18: o modelo candidato possui um mandato de
execucao duravel, limitado e revogavel. O mandato e uma autorizacao operacional
acima das TASKs individuais. Quando ativo e aplicavel, ele permite iniciar
automaticamente as TASKs cobertas, na ordem determinada pelo roadmap, sem nova
autorizacao a cada TASK.

O mandato nao substitui TASK, SPEC, PRD, arquitetura ou gates. Ele nao amplia
escopo e nao autoriza decisoes reservadas ao usuario. Deve parar diante de gate
bloqueante, falha sem correcao segura, fim do escopo ou revogacao.

Decisao do usuario em 2026-08-18: o escopo do mandato e sempre fechado. O
usuario identifica explicitamente as TASKs cobertas. TASK criada depois nao e
incluida automaticamente; ampliar a lista exige nova manifestacao do usuario e
registro de alteracao do mandato.

Para sobreviver a interrupcoes e retomadas, o mandato precisa de representacao
persistente. Decisao do usuario em 2026-08-18: o `ROADMAP.md` mantem o snapshot
do mandato vigente e aponta para um log proprio, responsavel pela evidencia
historica de concessao, alteracao, pausa e revogacao. O schema e a convencao de
nomes permanecem para o plano de propagacao, sem implementacao nesta TASK.

### 9.8 TASK Governada Como Unidade Central

Decisao do usuario em 2026-08-18: a TASK governada e a unidade central duravel
do modelo-alvo. A maquina de estados e o mecanismo operacional aplicado a essa
unidade. A sessao e apenas uma executora temporaria.

```text
TASK governada
|- TASK: contrato, escopo e validacoes
|- ROADMAP: estado presente
|- LOG: historico, evidencias e checkpoint
|- SPEC, PRD, arquitetura e docs: contexto duravel referenciado
`- conversa atual: mensagem e contexto temporario
```

O mandato fica acima das TASKs individuais: autoriza uma lista fechada e o
roadmap determina sua ordem. Na retomada, o agente carrega mandato, TASK,
estado, log e fontes antes de processar a mensagem atual. Decisoes da conversa
que precisem sobreviver sao persistidas no artefato governado apropriado.

### 9.9 Normalizacao De Mensagens Em Eventos

Decisao do usuario em 2026-08-18: toda mensagem e preservada como entrada
bruta, mas somente eventos operacionais normalizados entram na maquina de
estados.

```text
mensagem bruta
  -> classificacao explicita
  -> um ou mais eventos operacionais normalizados ou nao_classificado
  -> estado + evento + guardas
  -> acoes + proximo estado
```

O evento preserva referencia a sua origem. Tipo, alvo, identidade e dados
adicionais sao elementos candidatos; o contrato minimo exato continua pendente
e nao deve duplicar a conversa sem necessidade. A classificacao de linguagem
natural continua sendo fronteira de julgamento. Depois dela, a matriz deve
produzir resultado deterministico. `nao_classificado` e o fallback seguro e nao
cria autorizacao ou decisao por inferencia.

Definicao aprovada pelo usuario em 2026-08-18: evento operacional e o resultado
normalizado da interpretacao de uma interacao do usuario ou de um resultado
interno relevante para o workflow. Para interacao, a mensagem bruta e a origem;
para atividade interna, o resultado bruto e a origem. O evento traduz o
significado para o vocabulario estavel da maquina.

Decisao do usuario em 2026-08-18: toda mensagem gera uma ou mais ocorrencias
semanticas simples para processamento, mas nem toda ocorrencia e persistida em
arquivo. Perguntas e interacoes sem mutacao podem permanecer transitorias na
conversa. Mudancas de estado, mandato, decisoes governadas, gates, validacoes,
conclusoes, reaberturas e falhas relevantes produzem evidencia duravel. O
modelo usa `snapshot atual + log auditavel`, nao event sourcing integral.

Decisao do usuario em 2026-08-18: mensagem com multiplas intencoes e decomposta
em eventos simples vinculados a mesma origem. Eventos compostos nao sao criados
para combinacoes ocasionais de intencoes.

Decisao do usuario em 2026-08-18: eventos compativeis da mesma mensagem sao
processados na ordem indicada pela interacao, depois de verificacao previa do
conjunto. Intencoes materialmente contraditorias nao produzem mutacao parcial;
  a interpretacao resulta em `nao_classificado` e o agente pede esclarecimento.

## 10. Vocabulario De Trabalho Nao Aprovado

| Termo | Definicao provisoria |
| --- | --- |
| Estado persistente | Situacao exclusiva e observavel que restringe eventos ou proximas acoes |
| Contexto do estado | Dados estruturados que qualificam a condicao sem criar outro estado |
| Mensagem bruta | Texto atual enviado pelo usuario |
| Evento operacional | Resultado normalizado da interpretacao de uma interacao do usuario ou de resultado interno relevante |
| Ocorrencia de evento | Instancia do evento com origem, data, payload e identidade |
| Guarda | Condicao objetiva consultada antes de aceitar uma transicao |
| Transicao | Regra que liga estado, evento e guardas a acoes e proximo estado |
| Acao | Efeito a executar sem ser, por isso, estado persistente |
| Handler/activity | Skill ou procedimento especializado responsavel por uma acao |
| Evento invalido | Evento conhecido que nao possui transicao valida no estado atual |
| Nao classificado | Fallback seguro quando a intencao da mensagem nao esta clara |
| Mandato de execucao | Autorizacao duravel, limitada e revogavel para executar um escopo de TASKs sem nova permissao individual |

## 11. Criterios Provisorios Para Estados

Um candidato a estado deve ser:

- uma descricao da condicao operacional presente da TASK;
- mutuamente exclusivo em relacao aos demais estados da mesma maquina;
- observavel a partir de artefato persistente;
- relevante para autorizar ou proibir eventos e acoes;
- necessario para retomada depois de interrupcao de sessao;
- dotado de significado operacional unico;
- mais duravel que uma acao instantanea ou uma pergunta transitoria.

Regra adicional aprovada: uma TASK so deixa `em_execucao` por espera quando um
gate estrito impede toda continuacao segura. Se ainda houver trabalho seguro e
independente, ela permanece `em_execucao`.

## 11.1 Inventario Minimo De Estados Aprovado Ate Aqui

| Estado | Condicao presente | Invariante principal |
| --- | --- | --- |
| `planejada` | A TASK existe no roadmap, mas nao esta em execucao nem possui decisao humana concretamente pendente | Contrato existente; ciclo de execucao ainda nao aberto |
| `aguardando_usuario` | Nenhuma continuacao segura esta disponivel ao agente e o proximo evento necessario deve vir do usuario | Contexto informa acao necessaria, origem, motivo e eventos aceitos |
| `em_execucao` | A execucao esta autorizada, aberta e ainda nao concluiu o contrato | Nenhum gate estrito impede toda continuacao segura |
| `concluida` | O contrato foi cumprido e as validacoes aplicaveis passaram | Conclusao automatica; so reabre por descumprimento demonstrado do contrato original |

`em_execucao` comporta diversas ocorrencias sem multiplicar estados: duvidas,
questionamentos, atualizacoes, acoes do agente, testes, validacoes, correcoes
seguras e interacoes humanas nao bloqueantes. Cada ocorrencia e evento, acao ou
contexto. Ela produz permanencia no mesmo estado quando a invariante continua
verdadeira. Somente gate estrito que impeça toda continuacao segura leva a
`aguardando_usuario`.

## 12. Hipoteses Abertas

- Quais situacoes atendem aos criterios de estado persistente?
- Execucao precisa ser persistida ou pode ser acao com marcadores de inicio e
  fim no log?
- A conclusao automatica e global; falta definir o tratamento exato do feedback
  posterior e da eventual reabertura.
- Reflexao de governanca pertence a maquina da TASK ativa ou e contexto de
  sessao sem mutacao dessa TASK?
- Grupos podem ser somente fila de TASKs individuais?
- O catalogo de eventos pode ser unico para TASK individual, grupo e
  governanca?
- A classificacao de mensagens deve ficar no `AGENTS.md` ou em handler
  roteador?
- A matriz canonica deve viver neste documento, em outro documento ou em
  formato validavel futuro?

## 13. Registro De Decisoes Da Conversa

### 2026-08-18 - Prioridade Do Estudo

- O usuario considera o tema muito importante e autorizou dedicar atencao
  substancial ao estudo por envolver um modelo avancado de trabalho.
- Consequencia: profundidade e rigor sao prioritarios, sem abandonar a regra
  de uma decisao por vez nem ampliar o escopo para implementacao prematura.
- Estado da decisao: registrado.

### 2026-08-18 - Significado De Estado

- Decisao: o estado de uma TASK representa sua condicao operacional presente,
  no momento em que ela e lida, consultada ou planejada.
- Nao representa primariamente: o historico do que ja aconteceu nem a proxima
  acao permitida.
- Consequencia: o historico pertence ao log; as proximas acoes sao derivadas do
  estado presente, do evento e das guardas.
- Consequencia: um nome de estado deve permitir completar a frase `a TASK esta
  ... agora` com significado observavel e unico.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Execucao, Autonomia E Gates

- Decisao: `em_execucao` e uma condicao persistente da TASK, nao a indicacao de
  que o agente esta processando uma instrucao exatamente naquele segundo.
- Invariante: a execucao foi autorizada, ainda nao terminou e nenhum gate
  estrito impede toda continuacao segura.
- Decisao: acoes do agente e interacoes humanas nao bloqueantes nao alteram o
  estado.
- Decisao: a TASK so entra em espera quando um gate estrito impede toda
  continuacao segura.
- Decisao: dentro do mandato autorizado, autonomia e o padrao. Existirem duas
  ou mais alternativas tecnicas validas nao cria gate por si so; o agente usa
  as fontes governadas e julgamento tecnico.
- Limite: o catalogo e as guardas objetivas dos gates ainda serao definidos.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Estado Unico De Espera

- Decisao: autorizacao inicial, gate durante a execucao e aprovacao final usam
  um unico estado, inicialmente chamado `aguardando_decisao` e depois renomeado
  para `aguardando_usuario`.
- Decisao: o motivo da espera pertence ao contexto estruturado, com campos como
  tipo da acao, origem, solicitacao pendente e eventos aceitos.
- Consequencia: `aguardando_homologacao` nao e preservado como estado distinto
  no modelo candidato.
- Limite registrado nesta etapa: a politica de aprovacao final ainda nao havia
  sido decidida; ela foi resolvida na decisao seguinte.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Conclusao Automatica Sem Homologacao Universal

- Decisao: toda TASK conclui automaticamente quando executa seu contrato e
  passa nas validacoes aplicaveis.
- Decisao: nao existe aprovacao final obrigatoria para todas as TASKs nem campo
  contratual `aprovacao_final` por TASK.
- Decisao: `aguardando_homologacao` e removido do modelo candidato.
- Decisao: intervencao humana obrigatoria ocorre somente em gates estritos
  durante a execucao.
- Decisao: a conferencia do usuario ocorre sobre o resultado final e funciona
  como feedback posterior, nao como pre-condicao para concluir.
- Consequencia: feedback pode manter a conclusao, reabrir a TASK por contrato
  nao cumprido ou originar nova TASK/SPEC conforme classificacao futura.
- Garantias compensatorias: validacoes reproduziveis, evidencia, log,
  rastreabilidade e possibilidade de correcao ou reversao.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Mandato De Execucao

- Decisao: o modelo candidato tera mandato de execucao duravel, limitado e
  revogavel.
- Efeito: mandato ativo e aplicavel autoriza iniciar automaticamente as TASKs
  cobertas, seguindo a selecao e a ordem do roadmap.
- Sem mandato aplicavel: iniciar uma TASK continua dependendo de decisao
  humana, representada pelo estado unico de espera e pelo motivo correspondente.
- Limites: o mandato nao supera escopo, fontes governadas, gates ou decisoes
  reservadas ao usuario.
- Condicoes de parada minimas: gate bloqueante, falha sem correcao segura, fim
  do escopo e revogacao.
- Persistencia: necessaria, mas o artefato e o formato ainda nao foram
  escolhidos.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Persistencia Do Mandato

- Decisao: o snapshot do mandato vigente fica no `ROADMAP.md`.
- Decisao: o roadmap aponta para log proprio do mandato.
- Responsabilidade do roadmap: mostrar de forma curta a autorizacao operacional
  atualmente vigente junto da fila e dos estados das TASKs.
- Responsabilidade do log: registrar concessao, alteracao, pausa, revogacao e
  demais eventos relevantes do mandato.
- Consequencia: nao existe arquivo adicional de configuracao concorrendo com o
  roadmap como fonte do estado atual.
- Limite: schema, nome do log e validacao automatizada serao definidos no plano
  de propagacao, nao implementados nesta TASK.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Escopo Fechado Do Mandato

- Decisao: todo mandato possui escopo fechado.
- Decisao: o usuario identifica explicitamente as TASKs cobertas, seja uma
  TASK individual ou uma lista.
- Decisao: TASK criada depois da concessao nao entra automaticamente no
  mandato.
- Alteracao: incluir outra TASK exige nova manifestacao do usuario, atualizacao
  do snapshot no roadmap e evento no log do mandato.
- Consequencia: nao existe mandato dinamico por criterio nem expansao silenciosa
  do escopo.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Inventario Minimo De Estados

- Decisao: adotar os nomes `planejada`, `aguardando_usuario`, `em_execucao` e
  `concluida` para as quatro condicoes ja identificadas.
- Decisao: `planejada` separa backlog existente de uma decisao humana
  concretamente solicitada.
- Decisao: `em_execucao` permanece durante duvidas, questionamentos, acoes,
  testes e interacoes diversas que nao bloqueiem toda continuacao segura.
- Limite registrado nesta etapa: ainda seria avaliado se falha ou impedimento
  nao humano exigiria outro estado persistente; a decisao seguinte resolveu o
  ponto sem novo estado.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Gates E Espera Por Acao Do Usuario

- Decisao: substituir o nome `aguardando_decisao` por
  `aguardando_usuario`.
- Invariante: nenhuma continuacao segura esta disponivel ao agente e o proximo
  evento necessario deve vir do usuario.
- Abrangencia: decisao, autorizacao, informacao, arquivo, acao manual, correcao
  externa ou orientacao para aguardar, cancelar ou mudar o caminho.
- Gates: a decisao anterior e preservada. Enquanto houver correcao, retry,
  espera autorizada ou trabalho independente seguro, a TASK permanece
  `em_execucao`.
- Transicao: somente depois de esgotada a autonomia segura, o gate bloqueante
  leva de `em_execucao` para `aguardando_usuario`.
- Consequencia: nao e necessario um estado separado `bloqueada`.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Feedback E Reabertura

- Decisao: `concluida` pode retornar a `em_execucao` somente quando feedback
  posterior demonstrar descumprimento do contrato original ou de seus criterios
  de aceite/validacao.
- Decisao: nova necessidade, melhoria ou ampliacao nao reabre a TASK concluida;
  segue o fluxo governado de novo escopo.
- Evidencia: o log preserva a conclusao anterior, o feedback, sua classificacao
  e a reabertura, sem apagar historico.
- Consequencia: conferencia posterior do usuario continua eficaz sem virar gate
  universal de homologacao.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Unidade Central Do Workflow

- Decisao: a TASK governada e a unidade central duravel do modelo-alvo.
- Composicao: contrato na TASK, estado presente no roadmap, historico e
  checkpoint no log, contexto duravel nas fontes referenciadas e contexto
  temporario na conversa atual.
- Decisao: a maquina de estados e o mecanismo aplicado a essa unidade.
- Decisao: a sessao e executora temporaria e nao fonte duravel isolada.
- Decisao: o mandato fechado fica acima das TASKs e autoriza sua fila; o
  roadmap determina a ordem.
- Limite conceitual: `agregado DDD` permanece analogia de consistencia, nao
  equivalencia formal de implementacao.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Eventos Semanticos Normalizados

- Decisao: preservar toda mensagem como entrada bruta.
- Decisao: somente eventos operacionais normalizados entram na maquina de
  estados.
- Elementos candidatos ainda nao aprovados: tipo estavel, alvo, identidade,
  dados adicionais e referencia a origem. O contrato minimo continua pendente.
- Limite: a classificacao de linguagem natural ainda envolve julgamento.
- Fallback: `nao_classificado` pede esclarecimento e nao inventa autorizacao,
  decisao ou transicao.
- Consequencia: catalogo de eventos e matriz de transicoes serao artefatos
  complementares, sem criar tipo novo para cada mensagem.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Processamento E Persistencia De Eventos

- Decisao: toda mensagem e normalizada em uma ou mais ocorrencias semanticas
  simples para serem processadas pela maquina.
- Decisao: somente eventos operacionalmente relevantes sao persistidos no log.
- Persistencia obrigatoria candidata: mudanca de estado ou mandato, decisao
  governada, gate, validacao, conclusao, reabertura e falha relevante.
- Processamento transitorio: perguntas e interacoes sem mutacao, salvo quando
  forem necessarias para checkpoint.
- Consequencia: o CAPAG nao adota event sourcing integral; mantem snapshot atual
  e log auditavel seletivo.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Significado De Evento Operacional

- Decisao: evento operacional e o resultado normalizado da interpretacao de
  uma interacao do usuario ou de um resultado interno relevante.
- Origem externa: mensagem bruta do usuario.
- Origem interna: resultado bruto de atividade, validacao, gate ou outro
  processamento relevante.
- Funcao: traduzir a origem para vocabulario semantico estavel consumido pela
  matriz de transicoes.
- Distincao: evento descreve como a entrada ou o resultado foi interpretado;
  acao descreve o que o agente fara em resposta.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Multiplas Intencoes Na Mesma Mensagem

- Decisao: uma mensagem pode produzir um ou mais eventos operacionais simples.
- Decisao: todos os eventos derivados mantem referencia a mesma mensagem de
  origem.
- Decisao: nao criar tipos compostos para combinacoes ocasionais, como
  aprovacao mais pergunta.
- Consequencia: cada evento simples usa o catalogo estavel e e processado pela
  mesma matriz de transicoes.
- Limite registrado nesta etapa: ordem e conflito ainda estavam pendentes; a
  decisao seguinte resolveu o ponto.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Ordem E Conflito Entre Eventos

- Decisao: verificar o conjunto de eventos antes de executar mutacoes.
- Decisao: eventos compativeis seguem a ordem indicada pela interacao.
- Decisao: intencoes materialmente contraditorias nao produzem mutacao parcial.
- Fallback: produzir `nao_classificado` e pedir esclarecimento.
- Limite registrado nesta etapa: o efeito sobre o estado ainda estava pendente;
  a decisao seguinte resolveu o ponto.
- Estado da decisao: aprovada pelo usuario.

### 2026-08-18 - Fallback Nao Classificado E Gates

- Decisao: manter `nao_classificado` como nome canonico do fallback para
  interacao ambigua, insuficiente ou materialmente contraditoria.
- Decisao: `nao_classificado` sempre impede mutacoes derivadas da interacao.
- Guarda: `impede_toda_continuacao_segura?` determina o efeito no estado.
- Resultado `nao`: pedir esclarecimento e manter o estado atual enquanto houver
  trabalho seguro.
- Resultado `sim`: registrar gate, pedir esclarecimento e transicionar para
  `aguardando_usuario`.
- Distincao: `nao_classificado` descreve o resultado da interpretacao;
  `identificacao_de_gate` descreve que a autonomia segura foi esgotada.
- Estado da decisao: aprovada pelo usuario.

## 14. Decisoes Sobre Estados

### 14.1 Primeira Decisao Concluida

Pergunta canonica definida pela TASK:

```text
Quando voce pensa no estado de uma TASK, ele deve representar principalmente
o que ja aconteceu, o que esta aguardando uma decisao ou qual e a proxima acao
permitida?
```

Resposta consolidada: o estado representa a condicao operacional presente da
TASK. Algo que aconteceu pertence ao historico. Uma decisao aguardada pode
caracterizar um estado presente, mas apenas quando descrever realmente a
condicao atual. A proxima acao permitida e consequencia do estado, nao sua
definicao.

### 14.2 Segunda Decisao Concluida

Uma execucao autorizada e ainda nao encerrada constitui a condicao persistente
`em_execucao`. A TASK permanece nesse estado durante acoes e interacoes comuns.
Ela so entra em espera quando um gate estrito impede toda continuacao segura.

### 14.3 Terceira Decisao Concluida

Todas as esperas por decisao humana usam um unico estado, provisoriamente
chamado `aguardando_decisao` nesta etapa e depois renomeado para
`aguardando_usuario`, com o motivo registrado em contexto estruturado.

### 14.4 Quarta Decisao Concluida

Toda TASK conclui automaticamente depois de cumprir seu contrato e passar nas
validacoes. Nao existe homologacao final universal nem politica variavel de
aprovacao por TASK. A conferencia do usuario e feedback posterior.

### 14.5 Quinta Decisao Concluida

Um mandato duravel, limitado e revogavel pode autorizar o inicio automatico das
TASKs cobertas. Sem mandato aplicavel, a autorizacao humana continua
necessaria.

### 14.6 Sexta Decisao Concluida

O `ROADMAP.md` persiste o snapshot do mandato vigente e aponta para um log
proprio que registra concessao, alteracao, pausa e revogacao.

### 14.7 Setima Decisao Concluida

Todo mandato possui escopo fechado e lista explicitamente as TASKs cobertas.
TASKs futuras exigem ampliacao expressa do mandato.

### 14.8 Oitava Decisao Concluida

Adotar `planejada` para TASK existente no roadmap que ainda nao possui execucao
aberta nem decisao humana concretamente pendente. O inventario minimo passa a
conter `planejada`, `aguardando_usuario`, `em_execucao` e `concluida`.

### 14.9 Nona Decisao Concluida

Falha ou impedimento permanece em `em_execucao` enquanto houver recuperacao ou
trabalho seguro. Depois de esgotada essa autonomia, o gate bloqueante leva a
TASK para `aguardando_usuario`, pois o proximo evento necessario deve vir do
usuario. Nao existe estado separado `bloqueada`.

### 14.10 Decima Decisao Concluida

`concluida` retorna a `em_execucao` somente quando feedback posterior demonstra
descumprimento do contrato original. Nova necessidade segue novo escopo.

### 14.11 Decima Primeira Decisao Concluida

Confirmada a TASK governada como unidade central, composta por contrato, estado,
historico, fontes duraveis referenciadas e contexto temporario da conversa. A
maquina de estados e o mecanismo aplicado a ela.

### 14.12 Decima Segunda Decisao Concluida

Toda mensagem e preservada como entrada bruta, mas somente eventos operacionais
normalizados entram na maquina de estados. `nao_classificado` e o fallback
seguro.

### 14.13 Decima Terceira Decisao Pendente

Definir o contrato comum das ocorrencias, o catalogo minimo de tipos de evento
e sua relacao com a matriz de transicoes. Ja foi decidido que evento e o
resultado normalizado da interpretacao e que multiplas intencoes viram eventos
simples separados. Eventos compativeis seguem a ordem indicada e conflitos nao
geram mutacao parcial. `nao_classificado` bloqueia mutacoes da interacao e so
leva a `aguardando_usuario` quando impedir toda continuacao segura. O contrato
final das ocorrencias e o catalogo minimo ainda estao pendentes.

## 15. Fontes Oficiais E Primarias

Fontes consultadas em 2026-08-18:

1. David Harel, `Statecharts: a visual formalism for complex systems`, Science
   of Computer Programming, 1987:
   <https://doi.org/10.1016/0167-6423(87)90035-9>
2. Object Management Group, BPMN 2.0.2:
   <https://www.omg.org/spec/BPMN/2.0.2/About-BPMN>
3. W3C Recommendation, SCXML 1.0:
   <https://www.w3.org/TR/scxml/>
4. Microsoft Azure Architecture Center, Event-Driven Architecture Style:
   <https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven>
5. Microsoft Azure Architecture Center, Tactical DDD:
   <https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design>
6. AWS Step Functions Developer Guide:
   <https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html>
7. AWS Step Functions, error handling:
   <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html>
8. AWS Step Functions, callback with task token:
   <https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html>
9. AWS Step Functions, versions and aliases:
   <https://docs.aws.amazon.com/step-functions/latest/dg/concepts-cd-aliasing-versioning.html>
10. Temporal, Workflow Definition:
    <https://docs.temporal.io/workflow-definition>
11. Temporal, Workflow Execution:
    <https://docs.temporal.io/workflow-execution>
12. Temporal, Events and Event History:
    <https://docs.temporal.io/workflow-execution/event>
13. Temporal, Activities:
    <https://docs.temporal.io/activities>
14. Cadence, Workflows:
    <https://cadenceworkflow.io/docs/concepts/workflows>
15. Cadence, Activities:
    <https://cadenceworkflow.io/docs/concepts/activities>
16. Microsoft, Durable Functions overview:
    <https://learn.microsoft.com/en-us/azure/durable-task/durable-functions/durable-functions-overview>
17. Microsoft, Durable orchestrator code constraints:
    <https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-code-constraints>
18. Netflix Conductor, archived official repository:
    <https://github.com/Netflix/conductor>
19. Netflix Conductor, workflow definition:
    <https://github.com/Netflix/conductor/blob/main/docs/docs/configuration/workflowdef.md>
20. Netflix Conductor, HUMAN task:
    <https://github.com/Netflix/conductor/blob/main/docs/docs/reference-docs/human-task.md>
21. Netflix Conductor, workflow versioning:
    <https://github.com/Netflix/conductor/blob/main/docs/docs/how-tos/Workflows/versioning-workflows.md>
22. Stately/XState, State machines and statecharts:
    <https://stately.ai/docs/state-machines-and-statecharts>
23. Stately/XState, Events and transitions:
    <https://stately.ai/docs/transitions>
24. Stately/XState, Persistence:
    <https://stately.ai/docs/persistence>
25. GitHub Actions, events that trigger workflows:
    <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows>
26. GitHub Actions, workflow syntax:
    <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
27. GitHub Actions, deployments and environments:
    <https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments>

## 16. Limites Das Fontes

- A especificacao BPMN e normativa para a notacao, mas a operacao concreta
  depende da engine escolhida.
- As documentacoes de produtos descrevem garantias dentro de seus proprios
  runtimes; elas nao se transferem automaticamente para Markdown e conversa.
- O repositorio oficial Netflix Conductor esta arquivado. Ele e usado como
  referencia historica e arquitetural, nao como recomendacao de adocao.
- DDD fornece uma analogia de consistencia. Nao ha afirmacao de equivalencia
  formal entre TASK governada e agregado implementado.
- Determinismo da classificacao de linguagem natural continua limitado; o
  fallback seguro e parte necessaria do modelo.

## 17. Checkpoint De Encerramento - 2026-08-18

### 17.1 Estado Da TASK E Da Sessao

- `TASK-085D`: `pendente`, estudo em construcao e nao enviado para homologacao.
- Pesquisa comparativa: concluida para as referencias obrigatorias.
- Entrevista do modelo-alvo: em andamento.
- Workflow vigente: inalterado.
- Arquivos executaveis de governanca: inalterados.
- Artefatos desta execucao:
  - `docs/governance/workflow-state-event-study.md`;
  - `logs/LOG-085D-estudar-workflow-simples-deterministico.md`.

### 17.2 Decisoes Aprovadas Nesta Sessao

1. Estado representa a condicao operacional presente da TASK.
2. O inventario minimo possui `planejada`, `em_execucao`,
   `aguardando_usuario` e `concluida`.
3. `em_execucao` permanece durante acoes, duvidas, perguntas, testes,
   validacoes, correcoes e interacoes nao bloqueantes.
4. Gate bloqueante so existe depois de esgotada toda continuacao segura e
   quando o proximo evento necessario deve vir do usuario.
5. Nao existe estado separado `bloqueada`; o estado unico de espera e
   `aguardando_usuario`.
6. `aguardando_homologacao` e homologacao final universal sao removidos do
   modelo candidato.
7. Toda TASK conclui automaticamente depois de cumprir o contrato e passar nas
   validacoes aplicaveis.
8. Feedback posterior reabre a mesma TASK somente por descumprimento demonstrado
   do contrato original; nova necessidade segue novo escopo.
9. O mandato de execucao e duravel, limitado, revogavel e sempre fechado, com
   lista explicita de TASKs autorizadas.
10. O snapshot do mandato vigente fica no `ROADMAP.md`; seu historico fica em
    log proprio.
11. A TASK governada e a unidade central duravel; a maquina de estados e o
    mecanismo e a sessao e executora temporaria.
12. Toda mensagem bruta e preservada como origem e normalizada para um ou mais
    eventos operacionais simples.
13. Evento operacional e o resultado normalizado da interpretacao de interacao
    do usuario ou de resultado interno relevante.
14. Somente eventos operacionalmente relevantes sao persistidos; o modelo usa
    snapshot atual e log auditavel, nao event sourcing integral.
15. Multiplas intencoes compativeis viram eventos simples e seguem a ordem
    indicada; conflito material nao produz mutacao parcial.
16. `nao_classificado` e o fallback canonico. Ele bloqueia mutacoes da
    interacao e so muda a TASK para `aguardando_usuario` quando tambem impedir
    toda continuacao segura.

### 17.3 Estrutura Minima Ja Compreendida

O modelo operacional tera:

```text
catalogo de estados
+ catalogo de eventos
+ matriz esparsa de transicoes
+ tabela de cenarios para validacao
```

A matriz usa somente transicoes validas e uma regra global para evento invalido.
Guardas sao perguntas objetivas de `sim` ou `nao`. Acoes sao verbos que indicam
o que o handler executa. Guardas e acoes nao formam novos eixos de produto
cartesiano.

### 17.4 Pendencias Para A Proxima Sessao

1. Finalizar o contrato minimo de ocorrencia de evento sem burocracia ou
   duplicacao desnecessaria da conversa.
2. Definir o catalogo minimo e estavel de eventos externos e internos.
3. Definir guardas objetivas, gates estritos e vocabulario reutilizavel de
   acoes/handlers.
4. Construir a matriz esparsa de transicoes para os quatro estados.
5. Definir idempotencia, mensagem repetida, evento invalido e falha de handler.
6. Completar contrato e ciclo de vida do mandato fechado.
7. Modelar grupos como fila de TASKs individuais submetidas a mesma maquina.
8. Definir papeis finais de `AGENTS.md`, skills e roteamento/classificacao.
9. Simular todos os cenarios exigidos pela TASK.
10. Validar ambiguidade, destinos inexistentes, transicoes ausentes e limites de
    determinismo.
11. Consolidar modelo-alvo, comparacao antes/depois e plano de propagacao sem
    executar a propagacao.

### 17.5 Retomada Exata

Na proxima sessao:

1. reler a `TASK-085D`, sua SPEC, este checkpoint e o log;
2. confirmar que as fontes nao mudaram e reutilizar a pesquisa quando permitido
   pelo `AGENTS.md`;
3. informar que a TASK permanece `pendente` e pedir a autorizacao exigida pelo
   workflow vigente;
4. retomar sem rediscutir decisoes aprovadas, salvo pedido do usuario;
5. apresentar um primeiro candidato pequeno de catalogo de eventos, separando
   interpretacoes de interacoes do usuario e resultados internos;
6. continuar com uma unica pergunta por vez.

Primeira pergunta conceitual planejada para a retomada:

```text
Quais tipos minimos de interpretacao precisamos reconhecer nas interacoes do
usuario sem criar um evento diferente para cada frase?
```
