---
status: DRAFT
document_type: ARCHITECTURE
created_at: 2026-06-13
updated_at: 2026-06-13
approved_at: null
version: 0
revision: 2
---

# Arquitetura Tecnica

## Escopo do Documento

Este documento define a arquitetura tecnica proposta para o `capag` a partir do PRD `DRAFT` e do planejamento do Modulo 0 em `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/`.

Este documento esta em `DRAFT` e nao autoriza implementacao.

## Fontes de Arquitetura

Fontes principais:

- `docs/product/PRD.md`
- `tmp_deu_a_louca/00-planejamento-geral.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/00-visao-geral.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/01-auditoria-documental.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/02-indice-e-status-das-specs.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/03-arquitetura-alvo-do-sistema.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/04-frontend-rotas-explicitas.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/05-organizacao-de-pastas-frontend.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/06-design-system-frontend.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/07-documentos-operacionais-e-skills.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/08-estrategia-testes-validacao.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/09-higiene-repositorio-artefatos.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/10-consolidacao-planejamento-temporario.md`
- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/11-decisao-banco-dados-persistencia.md`

Fonte auxiliar para estado atual:

- `docs/inventory/INVENTARIO.md`

O inventario tecnico informa a situacao atual do codigo, mas nao define a arquitetura-alvo.

## Objetivo Arquitetural

A arquitetura deve criar uma base clara antes de mudancas funcionais amplas.

Objetivos:

- separar fonte de verdade documental, arquitetura, design, specs, tasks e skills;
- evitar que API, frontend ou exportacao concentrem regra de negocio;
- preparar o sistema para camada declarada, camada reclassificada, contrato CAPAG-E, evidencias, DFC/FCA, ROA, laudo e governanca metodologica;
- manter motores auditaveis, testaveis e rastreaveis;
- decidir banco de dados e persistencia antes dos modulos funcionais afetados;
- manter `Decimal` no backend para valores contabeis e prudenciais;
- preservar `openpyxl` como motor de exportacao Excel;
- manter `DuckDB` e CSV oficial fora da arquitetura.

## Estado Atual Resumido

O sistema atual possui:

- backend `FastAPI` em `src/capag/api/`;
- dominio, parser, motor, exportacao e UI legada em `src/capag/`;
- frontend `React/Vite` em `web/`;
- UI legada `Streamlit`;
- estado de sessao em memoria de processo;
- parser proprio de `ECD`;
- calculos atuais de PLR, FCO e CAPAG-E;
- exportacao Excel parcial;
- testes `pytest`;
- planejamento amplo em `tmp_deu_a_louca/`.

Riscos atuais relevantes para arquitetura:

- `src/capag/api/routes.py` tende a concentrar orquestracao;
- `src/capag/domain/models.py` concentra modelos e operacoes de sessao;
- `src/capag/engine/plr.py` concentra muita regra de classificacao, calculo, simulacao e auditoria;
- frontend atual navega por estado interno, nao por rotas explicitas;
- exportacao ainda e estrutural e nao serializa a sessao completa;
- decisao de banco de dados e persistencia ainda nao foi aprovada.

## Principios Arquiteturais

- Planejamento vem antes de implementacao.
- Specs aprovadas vêm antes de tasks.
- Tasks aprovadas vêm antes de codigo.
- Regra prudencial sensivel fica no backend/motor.
- Frontend nao duplica parser, calculo ou metodologia.
- Exportacao nao recalcula regra de negocio.
- Laudo nao recalcula motores.
- Motores devem ser testaveis sem FastAPI.
- Casos de uso devem ser testaveis sem HTTP.
- Decisao de persistencia deve ser transversal, nao local a um modulo.
- Skills especializadas iniciais de governanca devem ser criadas ou alinhadas antes do design.
- Skills de implementacao e documentos operacionais finais devem ser atualizados por ultimo.

## Arquitetura-Alvo em Camadas

```text
web/
  React/Vite
  UI, navegacao, formularios, visualizacao, revisao e comandos

src/capag/api/
  FastAPI, schemas HTTP, validacao de entrada, serializacao, erros HTTP

src/capag/application/        [proposta em DRAFT]
  casos de uso, orquestracao, transacoes logicas, coordenacao entre camadas

src/capag/domain/
  entidades, estados, invariantes, alertas, contratos de resultado

src/capag/io/
  leitura, parser e normalizacao da ECD

src/capag/engine/
  motores declarados, comportamentais, PLRA, FCA, ROA, CAPAG-E, auditoria

src/capag/export/
  serializacao Excel e laudo, sem recalculo

src/capag/assets/
  assets internos versionados enquanto nao houver decisao diferente

tests/
  unit, integration, golden, fixtures, design-previews
```

## Fronteiras de Responsabilidade

### `web/`

Responsabilidades:

- experiencia de usuario;
- upload e comandos;
- navegacao;
- exibicao de resultados, status, bloqueios e auditoria;
- revisao humana;
- simulacoes;
- validacao de formulario;
- consumo de API.

Proibicoes:

- nao recalcular regra prudencial;
- nao implementar parser ECD;
- nao decidir classificacao;
- nao substituir status retornado pelo backend;
- nao reconstruir motor em JavaScript.

### `src/capag/api/`

Responsabilidades:

- receber requests;
- validar contratos HTTP com schemas;
- chamar casos de uso;
- converter excecoes em respostas HTTP;
- serializar respostas;
- manter compatibilidade de API conforme specs aprovadas.

Nao deve concentrar:

- regra de calculo;
- composicao de simulacao;
- aplicacao de decisoes em lote;
- parse manual de valores prudenciais fora de casos de uso;
- logica de exportacao.

### `src/capag/application/`

Status: proposta arquitetural em `DRAFT`.

Objetivo:

- criar uma fronteira entre FastAPI e nucleo de dominio/motor.

Responsabilidades:

- orquestrar upload, sessao, analise, simulacao, revisao, restauracao e exportacao;
- coordenar `io`, `domain`, `engine` e `export`;
- preservar logica testavel sem FastAPI;
- centralizar casos de uso sem contaminar dominio com detalhes HTTP.

Casos de uso candidatos:

- `upload_ecd_to_session`;
- `update_fco_for_exercise`;
- `simulate_macro_scenario`;
- `simulate_methodology_decisions`;
- `apply_methodology_decision`;
- `apply_group_decisions`;
- `restore_methodology_defaults`;
- `export_session_workbook`;
- `load_session`;
- `load_exercise`;
- futuros casos de camada declarada, reclassificada, evidencias, DFC/FCA, ROA e laudo.

Arquivos candidatos:

```text
src/capag/application/__init__.py
src/capag/application/session_service.py
src/capag/application/analysis_service.py
src/capag/application/simulation_service.py
src/capag/application/export_service.py
```

A criacao desta camada exige spec/task aprovada antes de implementacao.

### `src/capag/domain/`

Responsabilidades:

- modelos de dominio;
- estados;
- invariantes;
- alertas;
- contratos canonicos de resultado;
- estruturas de decisao humana;
- objetos de auditoria e evidencia.

Direcao:

- reduzir acoplamento entre modelos e motores;
- evitar importacoes internas de engine dentro de entidades quando casos de uso puderem coordenar a operacao;
- separar contratos novos por dominio: camada declarada, reclassificada, CAPAG-E, evidencias, laudo, metodologia.

### `src/capag/io/`

Responsabilidades:

- decode e leitura de arquivos;
- parsing da ECD;
- normalizacao contabil;
- preparacao de saldos, movimentos e razao por conta;
- preservar dados declarados.

Direcao:

- manter ECD como fonte declaratoria;
- preservar `I051` como dado declarado;
- expor dados suficientes para camada declarada e reclassificada;
- evoluir parser apenas mediante spec aprovada.

### `src/capag/engine/`

Responsabilidades:

- calculos e analises;
- matcher metodologico;
- camada declarada;
- camada reclassificada/comportamental;
- PLRA;
- FCO e futura DFC/FCA;
- ROA;
- CAPAG-E;
- auditoria;
- scores e salvaguardas.

Direcao:

- separar motores por finalidade;
- nao misturar motor declarado com motor comportamental;
- usar matcher seguro para regras metodologicas;
- evitar regra ampla perigosa;
- produzir status diagnostico quando nao houver regra segura;
- manter `Decimal`;
- produzir objetos auditaveis, nao apenas valores finais.

Possiveis submodulos futuros:

```text
src/capag/engine/methodology/
src/capag/engine/declarative/
src/capag/engine/reclassification/
src/capag/engine/plra/
src/capag/engine/dfc/
src/capag/engine/roa/
src/capag/engine/capag_e/
src/capag/engine/evidence/
```

Esta decomposicao e direcao arquitetural, nao autorizacao de refatoracao.

### `src/capag/export/`

Responsabilidades:

- serializar resultados calculados;
- gerar Excel;
- gerar estruturas de laudo quando aprovadas;
- incluir status, bloqueios, ressalvas, evidencias, auditoria e versao metodologica.

Proibicoes:

- nao recalcular PLRA, FCA, ROA ou CAPAG-E;
- nao reclassificar contas;
- nao aplicar regra prudencial.

### `src/capag/assets/`

Responsabilidades atuais:

- manter assets internos versionados usados por motores.

Direcao:

- continuar como fonte versionada enquanto nao houver decisao aprovada de persistencia;
- distinguir assets metodologicos de dados operacionais;
- se banco for aprovado, definir formalmente o que continua asset e o que vira dado persistido.

## Arquitetura de Persistencia

Status: decisao pendente.

O planejamento indica que a nova arquitetura pode precisar de banco de dados para:

- catalogo oficial do plano referencial;
- metodologia versionada;
- snapshots de analise declarada;
- auditoria historica;
- resultados comparativos;
- perfis comportamentais;
- scores;
- evidencias;
- revisoes humanas;
- precedentes;
- rastreabilidade por empresa, exercicio e usuario.

Nenhum banco de dados esta aprovado neste documento.

Antes de qualquer implementacao de persistencia, deve existir ADR ou documento aprovado respondendo:

- se o banco sera parte da arquitetura-alvo;
- em qual modulo passa a ser necessario;
- qual banco sera usado;
- se havera ORM ou SQL direto;
- como serao migracoes;
- o que continua asset versionado;
- o que vira dado operacional;
- como separar metodologia, resultado, auditoria e revisao humana;
- como tratar historico, multiempresa, multiusuario e dados sensiveis.

Enquanto essa decisao nao for aprovada:

- banco de dados e persistencia continuam pendencia arquitetural;
- tasks nao devem introduzir persistencia por conta propria;
- implementacoes devem explicitar se assumem memoria temporaria ou dependem de decisao futura.

## Frontend-Alvo

### Rotas

O frontend deve evoluir de navegacao por estado interno para rotas explicitas.

Rotas planejadas:

```text
/
/exercicios/:year
/exercicios/:year/espelho
/exercicios/:year/simulador
/exercicios/:year/revisao
```

Pontos pendentes:

- decidir uso de `react-router-dom`;
- definir tabela oficial de rotas;
- definir comportamento de refresh;
- definir endpoints de recuperacao de sessao ativa.

Endpoints candidatos:

```text
GET /api/session
GET /api/exercises/{year}
```

### Organizacao de Pastas

Arvore-alvo proposta:

```text
web/src/app/
web/src/routes/
web/src/pages/
web/src/features/session/
web/src/features/ecd-mirror/
web/src/features/macro-simulator/
web/src/features/analytic-review/
web/src/shared/components/
web/src/shared/formatters/
web/src/lib/api/
web/src/styles/
```

Essa reorganizacao deve ser feita apenas por task aprovada e sem alterar comportamento no mesmo passo em que mover arquivos, salvo autorizacao explicita.

### Design

Design e arquitetura tecnica devem ficar separados.

O design/frontend oficial deve ser documentado em `docs/design/DESIGN.md`, com padroes para:

- botoes;
- icon buttons;
- grids;
- filtros;
- cards;
- barras de resultado;
- drill-downs;
- inputs monetarios e percentuais;
- estados vazios;
- alertas;
- responsividade;
- previews em `tests/design-previews/`.

## Testes e Validacao

Estrategia por camada:

- `io`: reader, parser, normalizador e fixtures ECD;
- `domain`: estados, invariantes, FCO, sessoes, decisoes;
- `engine`: metodologia, camada declarada, reclassificada, PLRA, FCO/FCA, ROA, CAPAG-E, auditoria;
- `api`: contratos, rotas, serializacao, erros;
- `application`: casos de uso, quando a camada existir;
- `export`: Excel, laudo e golden tests;
- `frontend`: build, navegacao, componentes criticos e validacao visual;
- `docs`: consistencia estrutural quando aplicavel.

Comandos padrao:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m pytest <tests relevantes>
cd web && npm run build
```

Validacao visual deve ser considerada obrigatoria para mudancas em:

- layout;
- rotas React;
- grids;
- drill-downs;
- estados vazios;
- estados de erro.

Ausencia de teste deve ser justificada na task e no worklog.

## Higiene do Repositorio

Categorias de artefatos:

- fonte versionada;
- asset interno versionado;
- fixture de teste;
- golden file;
- preview de design;
- sample documental;
- build gerado;
- cache local;
- temporario de planejamento.

Politicas a definir em spec/task futura:

- `node_modules`;
- `dist`;
- `__pycache__`;
- `.pyc`;
- samples ECD grandes;
- worklogs;
- arquivos temporarios;
- destino final de `tmp_deu_a_louca/`.

Nenhuma limpeza destrutiva esta autorizada por este documento.

## Skills do Agente

Diretorios existentes:

```text
.agents/skills/
.claude/skills/
```

Skills ja existentes:

- `design-lab-capag`
- `task-creator-capag`
- `task-worker-capag`
- `testing`

Etapa arquitetural nova:

- depois da arquitetura `DRAFT`;
- antes do design/frontend `DRAFT`;
- criar ou alinhar skills especializadas iniciais para documentacao, arquitetura, specs, tasks, testes e design.

Objetivo:

- transformar o fluxo SDD em operacao repetivel do agente;
- impedir que cada documento seja produzido com regra improvisada;
- deixar claro quando parar, quando pedir aprovacao e quando criar ADR/spec/task;
- preparar o design `DRAFT` com instrucoes de frontend adequadas.

Limites:

- skills de implementacao nao autorizam codigo sem spec e task aprovadas;
- skills nao podem alterar stack, paths oficiais, arquitetura ou governanca sem ADR/documento aprovado;
- skills nao substituem `AGENTS.md`, PRD, arquitetura, specs ou tasks.

Skills previstas para esta etapa:

- `document-control`
- `technical-writer`
- `architect-spec`
- `frontend-react-spec`
- `qa-spec`
- revisao/atualizacao de `design-lab-capag`, se necessario

Skills de implementacao devem ficar para etapa posterior, apos specs e tasks aprovadas.

## Documentos Operacionais

`README.md`, `AGENTS.md`, `CLAUDE.md`, tasks e skills finais de implementacao devem ser atualizados apenas depois da aprovacao de:

- fonte de verdade;
- indice de specs;
- arquitetura-alvo;
- rotas React;
- organizacao de pastas;
- design system;
- estrategia de testes;
- higiene de repositorio;
- roadmap.

Skills devem ser consequencia da arquitetura aprovada, nao fonte de arquitetura.

## Decisoes Pendentes

Estas decisoes precisam de aprovacao antes de implementacao:

- adotar ou nao `src/capag/application/`;
- adotar ou nao banco de dados;
- escolher banco, ORM/acesso e estrategia de migracao, se banco for aprovado;
- definir modo em memoria para desenvolvimento/teste, se banco for aprovado;
- definir o que fica em `assets` e o que vira dado persistido;
- decidir uso de `react-router-dom`;
- aprovar tabela oficial de rotas;
- aprovar arvore-alvo do frontend;
- aprovar politica de higiene de artefatos;
- aprovar indice e status das specs;
- aprovar momento de atualizar README, AGENTS, CLAUDE, tasks e skills;
- definir escopo exato das skills especializadas iniciais antes do design.

## Restrições

- Nao usar `DuckDB`.
- Nao oferecer CSV como exportacao oficial.
- Nao usar `float` para valores contabeis, financeiros ou prudenciais no backend/motor.
- Nao duplicar regra de negocio no frontend.
- Nao recalcular regra dentro da exportacao.
- Nao recalcular motores dentro do laudo.
- Nao introduzir persistencia sem decisao aprovada.
- Nao usar skills para contornar arquitetura, specs, tasks ou aprovacoes.

## Caminho de Evolucao

1. Aprovar PRD.
2. Revisar e aprovar arquitetura.
3. Criar ou alinhar skills especializadas iniciais.
4. Criar design/frontend `DRAFT`.
5. Resolver decisoes arquiteturais pendentes por ADR/spec.
6. Criar specs oficiais novas ou revisar specs existentes.
7. Criar tasks pequenas e cronologicas.
8. Implementar modulo 1 antes do modulo 2.
9. Implementar contrato CAPAG-E antes de DFC/FCA, ROA e laudo.
10. Atualizar governanca, README, AGENTS, CLAUDE e skills finais por ultimo.

## Proximo Passo Governado

Pelo `AGENTS.md`, depois desta arquitetura `DRAFT`, o proximo passo deve ser criar ou alinhar skills especializadas iniciais em:

```text
.agents/skills/
.claude/skills/
```

Depois disso, o proximo documento-base deve ser:

```text
docs/design/DESIGN.md
```

O design deve refletir o planejamento de frontend/design do Modulo 0 e nao deve iniciar implementacao.
