# Workflow

## 1. Arquivos Governados

| Grupo | Arquivos atuais | Funcao no fluxo |
| --- | --- | --- |
| Workflow | `docs/governance/workflow.md` | Mapa vigente da operacao usuario-agente. |
| Orquestracao | `AGENTS.md` | Instrucoes executaveis da sessao e dos gates. |
| Skills | `.agents/skills/*/SKILL.md` | Comportamentos especializados acionados pelo fluxo. |
| Produto | `docs/product/PRD.md` | Requisitos e limites do produto. |
| Arquitetura | `docs/architecture/architecture.md`, `docs/architecture/layer-boundaries.md` | Estrutura tecnica e fronteiras de camadas. |
| Especificacoes | `specs/README.md`, `specs/SPEC-*.md` | Contratos tecnicos que sustentam TASKs. |
| Frontend | `docs/frontend/DESIGN_TOKENS.md`, `docs/frontend/UI_COMPONENT_RULES.md`, `docs/frontend/SCREEN_PATTERNS.md`, `frontend/src/styles/globals.css` | Contrato visual e de interface. |
| Metodologia | `docs/methodology/*.md`, `backend/app/assets/reference/*`, `backend/app/assets/methodology/*` | Fontes, contratos e assets metodologicos. |
| Manuais normativos | `docs/reference/manual-plr-capag-ecd-pgfn-v2.md`, `docs/reference/manual-motor-operacional-universal-ebitda.md` | Referencias metodologicas governadas. |
| Planejamento | `tasks/README.md`, `tasks/TASK-*.md` | Escopo executavel e criterios de aceite. |
| Controle | `ROADMAP.md` | Proxima TASK e status da execucao. |
| Evidencia | `logs/LOG-*.md` | Registro objetivo de execucao, validacao e homologacao. |
| Orientacao | `README.md`, `backend/README.md`, `frontend/README.md`, `backend/app/assets/README.md` | Entrada e orientacao operacional do repositorio. |

## 2. Fluxo Operacional Atual

```mermaid
flowchart TD
    START([Inicio da sessao])
    AG[Ler AGENTS.md]
    RM[Ler ROADMAP.md]
    WAITING{Existe TASK aguardando homologacao?}
    READ_REVIEW[Ler TASK e LOG de homologacao]
    SELECT[Identificar TASK]
    SOURCES[Ler TASK, SPEC e fontes aplicaveis]
    REPORT[Informar TASK, status e fontes consultadas]
    AUTH{Usuario autorizou?}
    SCOPE[scope-resolution]
    EXEC[Executar somente o escopo autorizado]
    GATE{Gate de excecao?}
    DECISION[Solicitar decisao expressa]
    GATE_AUTH{Excecao autorizada?}
    VALIDATE[Executar validacoes da TASK]
    LOG[execution-log]
    TO_REVIEW[roadmap-manager: aguardando_homologacao]
    GROUP{TASK pertence a grupo autorizado?}
    MORE{Restam TASKs no grupo?}
    REVIEW[Solicitar homologacao]
    REVIEW_GROUP[Solicitar homologacao do grupo]
    REVIEW_RESULT{Resposta do usuario}
    APPROVE[execution-log: registrar aprovacao]
    COMPLETE[roadmap-manager: concluir TASK ou grupo]
    STOP{Encerrar sessao?}
    END([Finalizar sessao com estado e pendencias])

    START --> AG --> RM --> WAITING
    WAITING -- nao --> SELECT --> SOURCES --> REPORT --> AUTH
    WAITING -- sim --> READ_REVIEW --> REVIEW
    AUTH -- nao, duvida ou sugestao --> SCOPE
    AUTH -- sim --> EXEC --> GATE
    GATE -- sim --> DECISION --> GATE_AUTH
    GATE_AUTH -- sim --> EXEC
    GATE_AUTH -- nao --> END
    GATE -- nao --> VALIDATE --> LOG --> TO_REVIEW --> GROUP
    GROUP -- nao --> REVIEW
    GROUP -- sim --> MORE
    MORE -- sim --> SELECT
    MORE -- nao --> REVIEW_GROUP
    REVIEW --> REVIEW_RESULT
    REVIEW_GROUP --> REVIEW_RESULT
    REVIEW_RESULT -- aprovada --> APPROVE --> COMPLETE --> STOP
    REVIEW_RESULT -- ajuste, duvida ou novo ponto --> SCOPE
    STOP -- nao --> RM
    STOP -- sim --> END
```

## 3. Escopo E Homologacao

```mermaid
flowchart TD
    INPUT[Interacao sem autorizacao clara ou retorno de homologacao]
    SR[scope-resolution]
    CLASS{Classificacao}
    EXPLAIN[Responder e retomar autorizacao]
    ADJUST[Confirmar ajuste]
    GROUP_CONTEXT{Ajuste em homologacao de grupo?}
    PENDING[roadmap-manager: pendente]
    EXECUTE[Executar ou reexecutar a TASK atual]
    KEEP_REVIEW[Manter grupo aguardando_homologacao]
    ADJUST_GROUP[Executar ajuste, validar e atualizar logs]
    REVIEW_GROUP[Retomar homologacao do grupo]
    NEW_TASK[Confirmar criacao de nova TASK]
    INDIVIDUAL{Origem e homologacao individual?}
    APPROVE_CURRENT[Registrar aprovacao e concluir TASK atual]
    PLANNER[task-planner]
    ROADMAP[roadmap-manager: inserir TASK pendente]
    WAIT[Esperar nova autorizacao de execucao]
    NEW_SPEC[Bloquear implementacao e orientar SPEC]
    CONFLICT[Apresentar conflito e solicitar decisao expressa]

    INPUT --> SR --> CLASS
    CLASS -- esclarecimento_sem_mudanca --> EXPLAIN
    CLASS -- ajuste_da_task_atual --> ADJUST --> GROUP_CONTEXT
    GROUP_CONTEXT -- nao --> PENDING --> EXECUTE
    GROUP_CONTEXT -- sim --> KEEP_REVIEW --> ADJUST_GROUP --> REVIEW_GROUP
    CLASS -- nova_task --> NEW_TASK --> INDIVIDUAL
    INDIVIDUAL -- sim --> APPROVE_CURRENT --> PLANNER
    INDIVIDUAL -- nao --> PLANNER
    PLANNER --> ROADMAP --> WAIT
    CLASS -- nova_spec --> NEW_SPEC
    CLASS -- conflito_governado --> CONFLICT
```

## 4. Evolucao Do Workflow

```mermaid
flowchart TD
    IDEA[Ideia ou experiencia sobre o fluxo]
    AW[agent-workflow: abrir reflexao]
    CLASS{Classificacao}
    NO_CHANGE[Encerrar sem alterar arquivos]
    MATURE[Observar ou amadurecer]
    AUTH_WORKFLOW{Atualizacao do workflow autorizada?}
    UPDATE[Atualizar docs/governance/workflow.md]
    PROPAGATE{Muda arquivo executavel governado?}
    SR[scope-resolution: nova_task]
    AUTH_TASK{Criacao da TASK autorizada?}
    TP[task-planner]
    PENDING[TASK pendente no ROADMAP]
    SPEC[Orientar nova SPEC]
    CONFLICT[Solicitar decisao sobre conflito]
    DONE([Reflexao encerrada])

    IDEA --> AW --> CLASS
    CLASS -- observacao ou descarte --> NO_CHANGE --> DONE
    CLASS -- amadurecimento --> MATURE --> DONE
    CLASS -- ajuste_pequeno_autorizavel --> AUTH_WORKFLOW
    AUTH_WORKFLOW -- nao --> DONE
    AUTH_WORKFLOW -- sim --> UPDATE --> PROPAGATE
    CLASS -- nova_task --> SR
    PROPAGATE -- nao --> DONE
    PROPAGATE -- sim --> SR
    SR --> AUTH_TASK
    AUTH_TASK -- nao --> DONE
    AUTH_TASK -- sim --> TP --> PENDING --> DONE
    CLASS -- nova_spec --> SPEC --> DONE
    CLASS -- conflito_governado --> CONFLICT --> DONE
```
