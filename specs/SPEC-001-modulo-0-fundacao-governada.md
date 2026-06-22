# SPEC-001 - Modulo 0: Fundacao Governada

## 1. Objetivo Tecnico

Definir a fundacao governada do CAPAG antes da criacao de TASKs e da implementacao funcional ampla.

Esta SPEC estabelece como o projeto deve organizar fontes de verdade, estrutura minima de repositorio, fronteiras arquiteturais, contratos iniciais de frontend/backend, criterios de validacao e regras para continuidade do fluxo `PRD -> Arquitetura -> SPEC -> TASK`.

## 2. Contexto E Problema

O CAPAG deve evoluir de uma automacao parcialmente existente para uma aplicacao interna auditavel de analise CAPAG-E. O PRD exige evolucao modular, rastreavel e verificavel. A arquitetura define stack, persistencia, camadas, contratos REST, responsabilidades e proibicoes de recalculo fora dos motores.

Sem uma fundacao governada, novas implementacoes podem misturar regra prudencial, API, frontend, exportacao, laudo e documentos metodologicos, criando desalinhamento entre produto, arquitetura, testes e resultados auditaveis.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`

Fontes frontend governadas consultadas porque esta SPEC toca organizacao visual e rotas frontend:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Materiais em `docs/reference/` nao foram usados como fonte normativa direta desta SPEC.

## 4. Escopo

Esta SPEC cobre:

- organizacao minima de pastas para `backend/`, `frontend/`, `specs/`, `tasks/` e documentos governados;
- convencao inicial para criacao de SPECs e TASKs;
- fronteiras de responsabilidade entre `api`, `application`, `domain`, `io`, `engine`, `repositories`, `export` e `report`;
- alinhamento inicial do frontend com React/Vite, rotas explicitas e documentos visuais governados;
- validacoes basicas esperadas para continuidade do projeto;
- criterio para uma SPEC ser considerada suficiente para gerar TASK.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- implementacao de parser ECD;
- implementacao de motores declarados, comportamentais, PLRA, FCA, ROA ou CAPAG-E;
- criacao de tabelas e migrations definitivas;
- criacao de endpoints funcionais completos;
- criacao de telas finais de analise;
- regras prudenciais, formulas, politicas de arredondamento ou fontes normativas;
- uso direto de `docs/reference/` como fonte normativa para tarefas de implementacao.

## 6. Decisoes Ja Aprovadas

Decisoes vindas do PRD e da arquitetura:

- Produto interno para usuario unico neste ciclo.
- Evolucao modular, pequena, verificavel e aprovavel.
- Backend em Python com FastAPI.
- Frontend em React com Vite e TypeScript para novos codigos.
- PostgreSQL 16 como banco operacional.
- SQLAlchemy 2.x e Alembic para persistencia e migrations.
- REST com OpenAPI gerado pelo FastAPI.
- `Decimal` no backend para valores contabeis e prudenciais.
- Valores financeiros serializados como string decimal em payloads.
- Excel como exportacao oficial inicial.
- Laudo e exportacao nao recalculam motores.
- Frontend nao duplica regra prudencial sensivel.
- Assets metodologicos versionados no repositorio e publicados como `MethodologyVersion`.
- Docker Compose como ambiente local alvo.
- CI deve executar validacoes backend, frontend, migrations e assets metodologicos quando existirem.

## 7. Decisoes Pendentes

Nao ha decisao essencial pendente para criar TASKs de fundacao documental e estrutural derivadas desta SPEC.

Decisoes que devem ficar para SPECs posteriores:

- modelagem detalhada por modulo funcional;
- contratos finais de cada endpoint funcional;
- politica exata de escala, quantizacao e arredondamento por calculo prudencial;
- golden cases de motores prudenciais;
- formato final do Excel e do laudo.

## 8. Contratos

### 8.1 Contrato De Estrutura

O repositorio deve convergir para esta estrutura-alvo minima, sem exigir que todos os arquivos internos existam na primeira TASK:

```text
<project-root>/
├── AGENTS.md
├── ROADMAP.md
├── docs/
│   ├── architecture/
│   │   ├── architecture.md
│   │   └── adr/
│   ├── product/PRD.md
│   └── frontend/
├── specs/
├── tasks/
├── backend/
└── frontend/
```

### 8.2 Contrato De SPEC

Toda SPEC deve declarar:

- objetivo tecnico;
- contexto e problema;
- fontes usadas;
- escopo;
- fora de escopo;
- decisoes aprovadas;
- decisoes pendentes;
- contratos;
- responsabilidades por camada;
- dados de entrada e saida;
- estados e erros relevantes;
- criterios de aceite verificaveis;
- estrategia de validacao;
- riscos e mitigacoes;
- bloqueios.

### 8.3 Contrato De TASK

Toda TASK deve nascer de SPEC suficiente e declarar:

- SPEC de origem;
- objetivo;
- escopo exato;
- fora de escopo;
- passos executaveis;
- arquivos ou areas provaveis;
- criterios de aceite;
- validacao esperada;
- riscos;
- bloqueios pendentes, se existirem.

TASK nao pode decidir arquitetura, contrato de API, regra de dominio, formula prudencial, politica de arredondamento, padrao visual ou estrategia critica de teste.

## 9. Responsabilidades Por Camada

### Frontend

Responsavel por operacao, navegacao, revisao e visualizacao. Deve consumir API e seguir os documentos governados de frontend.

Nao pode:

- parsear ECD;
- recalcular PLRA, FCA, ROA ou CAPAG-E;
- decidir classificacao comportamental;
- aplicar metodologia prudencial;
- alterar status retornado pelo backend.

### API

Responsavel por REST, validacao HTTP, autenticacao/autorizacao, OpenAPI, serializacao e conversao de erros de dominio em respostas HTTP.

### Application

Responsavel por casos de uso, transacoes logicas e orquestracao entre parse, motores, persistencia, exportacao e laudo.

### Domain

Responsavel por entidades, value objects, estados canonicos, invariantes e contratos internos.

### IO

Responsavel por leitura, parse e normalizacao de ECD, sem regra prudencial.

### Engine

Responsavel por motores de calculo, classificacao, auditoria metodologica e governanca de assets. Deve usar `Decimal` para valores contabeis e prudenciais.

### Repositories

Responsavel por persistencia via SQLAlchemy e consultas transacionais.

### Export

Responsavel por serializar snapshots e objetos calculados para Excel, sem recalcular regra de negocio.

### Report

Responsavel por montar laudo estruturado a partir de objetos calculados, evidencias, bloqueios e snapshots, sem executar motor.

## 10. Dados De Entrada E Saida

Entradas desta fundacao:

- PRD aprovado;
- arquitetura aprovada;
- documentos frontend governados;
- AGENTS.md;
- SPECs aprovadas.

Saidas esperadas:

- diretorio `specs/` com SPECs versionadas em Markdown;
- diretorio `tasks/` para TASKs derivadas de SPECs suficientes;
- `ROADMAP.md` como painel operacional vivo de proxima tarefa, status e ponteiros para TASKs e logs;
- estrutura inicial de projeto aderente a arquitetura;
- validacoes documentais e tecnicas basicas;
- rastreabilidade entre TASK, SPEC, PRD e arquitetura.

## 11. Estados E Erros Relevantes

Estados documentais:

- `rascunho`: documento ainda incompleto;
- `suficiente_para_task`: SPEC tem contratos, criterios e validacao suficientes;
- `bloqueado`: falta decisao essencial, contrato, regra ou criterio verificavel;
- `substituido`: documento superseded por versao posterior aprovada.

Erros a registrar como bloqueio:

- SPEC sem fonte principal obrigatoria;
- SPEC frontend sem documentos governados de frontend;
- TASK criada sem SPEC suficiente;
- TASK tentando decidir arquitetura, API, dominio, formula ou padrao visual;
- criterio de aceite subjetivo ou nao verificavel;
- regra prudencial inferida de codigo, teste ou referencia historica sem aprovacao.

## 12. Criterios De Aceite

- O `ROADMAP.md` deve refletir a proxima tarefa, status permitidos e ponteiros para TASKs e logs.
- Deve existir diretorio `specs/`.
- Esta SPEC deve existir em `specs/SPEC-001-modulo-0-fundacao-governada.md`.
- A SPEC deve citar explicitamente `docs/product/PRD.md` e `docs/architecture/architecture.md` como fontes principais.
- A SPEC deve citar documentos frontend governados por envolver organizacao visual e frontend.
- A SPEC deve declarar que `docs/reference/` nao foi usado como fonte normativa direta.
- A SPEC deve conter escopo, fora de escopo, decisoes aprovadas, decisoes pendentes, contratos, responsabilidades, entradas/saidas, estados/erros, criterios, validacao, riscos e bloqueios.
- Nenhuma TASK deve ser criada neste passo.
- Nenhuma implementacao funcional deve ser criada neste passo.

## 13. Estrategia De Validacao Esperada

Validacao documental:

- conferir existencia de `specs/SPEC-001-modulo-0-fundacao-governada.md`;
- conferir se o `ROADMAP.md` foi atualizado quando houver transicao operacional de TASK;
- conferir se a SPEC cita fontes obrigatorias;
- conferir se nao ha TASK criada antes de aprovacao da SPEC.

Validacao tecnica futura para TASKs derivadas:

- `pytest` para backend quando houver codigo Python;
- validacao de migrations quando Alembic existir;
- `npm run build` e Vitest quando frontend existir;
- Playwright apenas para fluxos criticos de UI;
- validacao automatizada de assets metodologicos quando assets governados forem introduzidos.

## 14. Riscos E Mitigacoes

- Risco: a fundacao virar implementacao ampla demais.
  Mitigacao: TASKs derivadas devem ser pequenas e restritas a estrutura, scaffolding e validacao.

- Risco: `docs/reference/` ser usado como fonte normativa sem aprovacao.
  Mitigacao: SPECs e TASKs devem declarar fontes usadas e bloquear inferencias historicas nao aprovadas.

- Risco: frontend assumir regra prudencial para acelerar tela.
  Mitigacao: manter regra prudencial no backend e exigir contrato de API antes de telas funcionais.

- Risco: Excel ou laudo recalcularem resultado.
  Mitigacao: exportacao e laudo devem consumir snapshots e objetos calculados.

- Risco: criterios de aceite ficarem subjetivos.
  Mitigacao: toda TASK deve herdar criterios verificaveis desta SPEC ou de SPEC funcional suficiente.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs estruturais derivadas desta SPEC.

Ha bloqueio para TASKs funcionais de dominio prudencial enquanto nao existirem SPECs especificas com contrato, fonte normativa, regra, politica de precisao/arredondamento, criterios de aceite e golden cases proporcionais ao risco.
