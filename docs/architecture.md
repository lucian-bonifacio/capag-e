# Documento de Arquitetura - CAPAG

## 1. Resumo Executivo

O CAPAG sera estruturado como uma aplicacao interna para analise CAPAG-E auditavel, usada por um unico usuario, capaz de importar ECD, preservar a leitura declarada, gerar uma leitura reclassificada/comportamental paralela, calcular componentes prudenciais, produzir exportacao Excel e emitir laudo estruturado sem recalcular motores.

A arquitetura-alvo adota:

- backend em Python com FastAPI;
- frontend em React com Vite;
- PostgreSQL como banco relacional;
- REST com OpenAPI gerado pelo FastAPI;
- SQLAlchemy 2.x com Alembic;
- Pydantic para contratos;
- React Router, TanStack Query, React Hook Form, Zod e Tailwind CSS no frontend;
- Docker Compose para ambiente local;
- GitHub Actions para CI;
- logs estruturados em JSON, healthcheck e metricas basicas.

A principal decisao arquitetural e transformar o CAPAG de uma automacao orientada a sessao em memoria para um sistema com persistencia governada. Essa persistencia e necessaria para metodologia versionada, snapshots de analise, auditoria, evidencias, revisoes humanas, precedentes, exportacoes e laudos reproduziveis. Assets metodologicos versionados continuam existindo no repositorio, mas resultados emitidos devem carregar a versao efetivamente usada para impedir alteracao retroativa silenciosa.

## 2. Contexto e Objetivos

O produto atual e uma ferramenta interna de analise prudencial baseada em ECD. O PRD direciona a evolucao para tres entregas conectadas:

- analise interna auditavel;
- planilha Excel final com resultados e trilhas relevantes;
- laudo CAPAG-E estruturado, sem recalcular motores.

Objetivos arquiteturais:

- separar claramente ECD declarada, metodologia interna, leitura comportamental, resultado prudencial, evidencia, exportacao e laudo;
- manter regra prudencial sensivel no backend;
- impedir duplicacao de regra no frontend, Excel ou laudo;
- preservar `I051` como dado declaratorio da ECD;
- criar camada reclassificada que nao substitui silenciosamente a declarada;
- usar `Decimal` no backend para valores contabeis e prudenciais;
- manter Excel como exportacao oficial;
- manter historico e rastreabilidade por empresa, exercicio, arquivo ECD, versao metodologica e laudo;
- evoluir por modulos sequenciais, pequenos e verificaveis.

## 3. Insumos Utilizados

Insumo principal:

- `docs/product/PRD.md`

Referencias tecnicas consideradas:

- `docs/reference/ARCHITECTURE.md`
- `docs/reference/ajuste_modulo_principal.md`
- `docs/reference/ideia-de-automacao.md`
- `docs/reference/implementation_plan.md`
- `docs/reference/manual-plr-capag-ecd-pgfn-v2.md`
- `docs/reference/manual-motor-operacional-universal-ebitda.md`
- `docs/reference/nova_spec_nv_modulo.md`
- `docs/reference/novo_modulo_reclass.md`
- `docs/reference/planejamento-modulos/00-planejamento-geral.md`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-00-organizacao-arquitetura-design/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-01-camada-declarada/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/`
- todos os arquivos de `docs/reference/planejamento-modulos/modulo-08-governanca-metodologia/`

O PRD registra que nao ha referencias externas adicionais informadas. A solicitacao desta arquitetura adicionou explicitamente todo `docs/reference` como referencia complementar.

## 4. Premissas e Restrições

Premissas:

- O produto e interno e usado por um unico usuario.
- A ECD e a fonte declaratoria da analise.
- A camada declarada e a camada reclassificada coexistem.
- A camada reclassificada e deterministica, auditavel e conservadora.
- IA generativa nao e nucleo decisorio.
- Excel e a exportacao oficial inicial.
- O laudo consome resultados calculados e nao executa motor.
- Todo resultado final deve carregar metodo, formula, status, limitacoes, bloqueios e versao metodologica.
- Valores monetarios usam `Decimal` no backend e sao serializados de forma controlada para API, frontend, Excel e laudo.

Restricoes:

- Nao criar SaaS, multiusuario amplo ou administracao livre de regras metodologicas neste ciclo.
- Nao usar DuckDB como banco operacional.
- Nao oferecer CSV como exportacao oficial.
- Nao classificar automaticamente por palavra-chave isolada.
- Nao usar prefixo metodologico amplo perigoso como classificacao final.
- Nao permitir que frontend, Excel ou laudo recalculem PLRA, FCA, ROA ou CAPAG-E.
- Nao retroagir mudanca metodologica sobre laudos ja emitidos.

## 5. Drivers Arquiteturais

Drivers funcionais criticos:

- importar ECD e estruturar registros `I050`, `I051`, `I155`, `I200`, `I250`, `J100` e, quando implementado, `J150`;
- preservar `COD_CTA_REF` declarado no `I051`;
- separar plano referencial oficial de metodologia interna;
- calcular camada declarada com status, auditoria e resultado por conta;
- bloquear regras metodologicas amplas perigosas;
- montar razao por conta, contrapartidas e perfil comportamental;
- calcular score, confianca, evidencias e recomendacao da camada reclassificada;
- comparar declarado, reclassificado e revisado pelo usuario;
- formalizar contrato `PLRA`, `FCA`, `ROA` e `CAPAG-E`;
- estruturar evidencias, materialidade, justificativas, bloqueios e ressalvas;
- calcular DFC direta completa para `FCA`;
- calcular caminho alternativo `ROA + PLRA`;
- gerar Excel e laudo a partir dos objetos calculados.

Drivers nao funcionais:

- auditabilidade integral por conta, lancamento, regra aplicada, evidencia e versao metodologica;
- reprodutibilidade de resultados historicos;
- seguranca operacional para dados contabeis sensiveis;
- evolucao modular, testavel e governada;
- rastreabilidade entre PRD, specs, assets, codigo, testes, exportacao e laudo;
- conservadorismo em classificacoes ambiguas ou materiais;
- operacao local simples via Docker Compose e deploy previsivel em staging/producao.

Volume e disponibilidade:

- O sistema deve suportar ECDs com milhares ou centenas de milhares de linhas.
- A disponibilidade esperada e de ferramenta interna, nao plataforma 24x7.
- O processamento pode ser sincrono no MVP quando couber no tempo de request configurado; processamentos longos devem evoluir para fila de jobs com PostgreSQL como fonte de estado e worker Python dedicado.

Privacidade e seguranca:

- ECDs, CNPJs, dados contabeis, evidencias, laudos e exportacoes sao dados sensiveis.
- Mesmo com usuario unico, a arquitetura deve autenticar acesso, registrar acoes relevantes e controlar segredos fora do repositorio.

## 6. Stack Tecnológica

Backend:

- Python 3.12.
- FastAPI para API REST e OpenAPI.
- Pydantic para validacao e serializacao de contratos.
- SQLAlchemy 2.x para ORM.
- Alembic para migracoes.
- PostgreSQL 16 para persistencia relacional.
- `Decimal` para valores monetarios e prudenciais.
- `openpyxl` para exportacao Excel.
- `pytest` para testes unitarios, integracao e golden tests.

Frontend:

- React com Vite.
- TypeScript como padrao para novos codigos frontend.
- React Router para rotas explicitas.
- TanStack Query para cache e sincronizacao com API.
- React Hook Form com Zod para formularios.
- Tailwind CSS para UI base.
- Vitest com React Testing Library.
- Playwright para fluxos criticos de upload, revisao, exportacao e laudo.

Infraestrutura e operacao:

- Docker e Docker Compose para desenvolvimento local.
- GitHub Actions para lint, testes, build e validacoes metodologicas.
- Logs estruturados em JSON.
- Healthcheck em `/health`.
- Metricas basicas em endpoint protegido ou integracao Prometheus quando ambiente permitir.
- Backups automatizados do PostgreSQL em staging/producao.

Autenticacao e autorizacao:

- JWT com access token e refresh token.
- Refresh token persistido com hash no backend.
- RBAC simples por papeis, mesmo que inicialmente exista apenas `analyst_admin`.

## 7. Visão Geral da Arquitetura

A arquitetura sera modular, com backend responsavel por regra de negocio e frontend responsavel por operacao, revisao e visualizacao.

Visao em camadas:

```text
frontend/
  React/Vite
  Rotas, telas, formularios, revisao humana, visualizacao e comandos

backend/app/api/
  FastAPI, rotas REST, dependencies, validacao HTTP e serializacao

backend/app/application/
  Casos de uso, orquestracao, transacoes logicas e coordenacao de modulos

backend/app/domain/
  Entidades, value objects, estados, contratos canonicos, invariantes e eventos internos

backend/app/io/
  Leitura, parse e normalizacao da ECD

backend/app/engine/
  Motores declarados, comportamentais, PLRA, DFC/FCA, ROA, CAPAG-E e auditoria

backend/app/repositories/
  Persistencia via SQLAlchemy e consultas transacionais

backend/app/export/
  Serializacao Excel e artefatos de laudo, sem recalculo de regra

backend/app/report/
  Montagem de laudo estruturado a partir de objetos calculados

backend/app/assets/
  Leitura de assets metodologicos versionados do repositorio

postgresql
  Empresas, arquivos ECD, exercicios, snapshots, metodologia, auditoria, evidencias, revisoes, exportacoes e laudos
```

Principio de dependencia:

- `api` depende de `application`;
- `application` depende de `domain`, `io`, `engine`, `repositories`, `export` e `report`;
- `engine` depende de `domain` e assets/metodologia carregados por interfaces claras;
- `domain` nao depende de FastAPI, SQLAlchemy, React ou openpyxl;
- `export` e `report` nao chamam motores de calculo;
- frontend consome contratos da API e nunca reimplementa metodologia prudencial.

## 8. Componentes e Responsabilidades

### Frontend

Responsabilidades:

- upload de ECD;
- navegacao por rotas explicitas;
- exibicao de camada declarada, reclassificada, evidencias, DFC, ROA, contrato CAPAG-E e laudo;
- revisao humana de classificacoes, evidencias e bloqueios;
- acionamento de exportacao Excel;
- preview de laudo.

Proibicoes:

- nao parsear ECD;
- nao recalcular PLRA, FCA, ROA ou CAPAG-E;
- nao decidir classificacao comportamental;
- nao aplicar metodologia por conta propria;
- nao alterar status retornado pelo backend.

Rotas-alvo:

- `/`
- `/analises`
- `/analises/:analysisId`
- `/analises/:analysisId/exercicios/:year/declarada`
- `/analises/:analysisId/exercicios/:year/reclassificada`
- `/analises/:analysisId/exercicios/:year/evidencias`
- `/analises/:analysisId/exercicios/:year/dfc`
- `/analises/:analysisId/exercicios/:year/roa`
- `/analises/:analysisId/exercicios/:year/resultado`
- `/analises/:analysisId/laudo`
- `/governanca/metodologia`

### API

Responsabilidades:

- expor REST com OpenAPI;
- validar requests com Pydantic;
- autenticar e autorizar requests;
- converter erros de dominio em respostas HTTP;
- serializar `Decimal` como string decimal em payloads financeiros;
- manter contratos estaveis para frontend, exportacao e testes.

### Application

Responsabilidades:

- orquestrar casos de uso;
- abrir transacoes;
- coordenar parse, calculo, persistencia e exportacao;
- garantir que resultados persistidos carreguem `methodology_version`;
- impedir que rotas acumulem logica de negocio.

Casos de uso principais:

- `create_analysis_from_ecd`;
- `run_declared_layer`;
- `run_behavioral_layer`;
- `review_behavioral_classification`;
- `calculate_capag_contract`;
- `upsert_adjustment_evidence`;
- `calculate_dfc_fca`;
- `calculate_roa_plra`;
- `generate_excel_export`;
- `generate_capag_report`;
- `publish_methodology_version`.

### Domain

Responsabilidades:

- entidades e contratos canonicos;
- estados de resultado;
- invariantes numericas;
- status de regra, evidencia, componente e laudo;
- objetos de auditoria e rastreabilidade.

Entidades e objetos centrais:

- `Company`;
- `EcdFile`;
- `Analysis`;
- `Exercise`;
- `DeclaredAccountResult`;
- `MethodologyRule`;
- `BehavioralAccountProfile`;
- `BehavioralClassification`;
- `HumanReview`;
- `CapagEAssessment`;
- `AdjustmentEvidence`;
- `AssetValuationAssessment`;
- `DfcCalculation`;
- `DfcAuditRow`;
- `RoaCalculation`;
- `RoaAuditRow`;
- `CapagReport`;
- `ReportSection`;
- `MethodologyVersion`.

### IO

Responsabilidades:

- detectar encoding e ler ECD;
- parsear registros `I050`, `I051`, `I155`, `I200`, `I250`, `J100` e futuramente `J150`;
- preservar texto original, linha original e numero de linha quando disponivel;
- normalizar valores para `Decimal`;
- construir estruturas intermediarias sem aplicar metodologia prudencial.

### Engine

Responsabilidades:

- aplicar metodologia declarada;
- executar matcher metodologico seguro;
- calcular PLRA;
- montar razao, perfis e score comportamental;
- calcular cenarios declarado, reclassificado e revisado;
- calcular DFC direta e FCA;
- calcular ROA;
- combinar componentes no contrato CAPAG-E;
- produzir auditoria estruturada.

Motores separados:

- `declared`: leitura `ECD + I051 + plano oficial + metodologia`;
- `methodology_matcher`: match exato/prefixo seguro por finalidade;
- `behavioral`: perfil, familias, score, confianca e comparacao;
- `plra`: patrimonio liquido realizavel ajustado;
- `dfc`: fluxo operacional, investimento, financiamento e FCA;
- `roa`: resultado operacional ajustado;
- `capag`: contrato canonico CAPAG-E;
- `evidence`: materialidade, bloqueios e ressalvas;
- `governance`: validacao de assets e cobertura metodologica.

### Repositories

Responsabilidades:

- persistir entidades operacionais;
- consultar snapshots;
- recuperar versao metodologica usada;
- controlar transacoes;
- evitar SQL ad hoc fora da camada de persistencia.

### Export

Responsabilidades:

- gerar workbook Excel oficial com `openpyxl`;
- serializar resultados calculados, auditoria, evidencias, bloqueios e metodologia;
- gerar abas por modulo;
- nao executar regra prudencial.

### Report

Responsabilidades:

- montar `CapagReport` a partir de `CapagEAssessment`, evidencias, bloqueios e snapshots;
- validar status do laudo;
- produzir secoes estruturadas;
- entregar estrutura para exportacao Excel e futura geracao DOCX/PDF.

## 9. Fluxos Principais

### Fluxo 1 - Preparacao Governada

1. O responsavel aprova PRD, arquitetura, specs e modulos.
2. A governanca cria matriz de rastreabilidade entre manual, spec, asset, codigo e teste.
3. A versao metodologica e publicada com changelog.
4. O sistema valida assets no CI e no startup da API.

### Fluxo 2 - Importacao da ECD

1. Usuario envia arquivo ECD.
2. API autentica, valida tamanho e tipo.
3. `application` cria `Analysis` e `EcdFile`.
4. `io` le e parseia registros relevantes.
5. Dados normalizados sao persistidos por empresa, arquivo, exercicio, contas, saldos, lancamentos e partidas.
6. A analise fica com status `importada`.

### Fluxo 3 - Camada Declarada

1. Usuario solicita analise declarada.
2. Motor carrega contas, saldos e `COD_CTA_REF` declarado no `I051`.
3. Motor consulta plano referencial oficial versionado.
4. Matcher busca regra metodologica por codigo exato e prefixo mais especifico seguro.
5. Regras `BLOQUEADA`, `GENERICA_PERIGOSA`, `EM_REVISAO` e `DEPRECIADA` nao classificam calculo novo.
6. Resultado por conta registra descricao oficial, regra aplicada, status, finalidade, valor e acao recomendada.
7. Snapshots de PLRA/FCO atual/CAPAG-E declarada sao persistidos com versao metodologica.

### Fluxo 4 - Camada Reclassificada

1. Motor monta razao por conta usando `I200` e `I250`.
2. Calcula metricas financeiras, textuais, hierarquicas e de contrapartidas.
3. Aplica regras deterministicas das familias MVP.
4. Calcula score, confianca e diferenca entre primeira e segunda familia.
5. Aplica salvaguardas: materialidade alta, poucos lancamentos, ambiguidade, tributos, partes relacionadas e patrimonio liquido exigem revisao.
6. Compara classificacao sugerida com `I051`.
7. Gera acao `manter`, `reclassificar`, `revisar` ou `sem_conclusao`.
8. Usuario revisa casos materiais ou ambiguos.
9. Sistema persiste decisao humana, justificativa e precedente quando aprovado.

### Fluxo 5 - Contrato CAPAG-E

1. Sistema recebe `PLRA` final ou parcial.
2. Sistema recebe `FCA` final/parcial ou `ROA` final/parcial.
3. Motor `capag` aplica metodo `fca_plra`, `roa_plra`, `comparativo_fca_roa` ou `nao_definido`.
4. `CAPAG-E` so fica `final` quando metodo, componentes, evidencias e bloqueios permitirem.
5. Valores intermediarios permanecem visiveis mesmo quando resultado final estiver bloqueado.

### Fluxo 6 - Evidencias e Avaliacao de Ativos

1. Ajuste material gera ou exige `AdjustmentEvidence`.
2. Materialidade default e calculada pelo backend.
3. Usuario pode revisar materialidade de forma controlada com justificativa.
4. Evidencias criticas pendentes bloqueiam resultado final ou geram ressalva conforme regra.
5. Ativos relevantes usam `AssetValuationAssessment` para valor contabil, desagio default, valor de liquidacao e valor final.

### Fluxo 7 - DFC Direta e FCA

1. Motor identifica lancamentos com caixa/disponibilidades.
2. Classifica contrapartida em operacional, investimento ou financiamento por codigo referencial.
3. Registra pendencias quando regra faltar, direcao divergir ou movimento material exigir evidencia.
4. Calcula `FCA = operacional + investimento + financiamento + ajustes validados`.
5. Enquanto houver apenas FCO operacional, status e `FCA parcial`.

### Fluxo 8 - ROA + PLRA

1. Motor identifica contas de resultado por ECD e referencial.
2. Calcula receita liquida, custos, despesas, resultado financeiro e nao operacional.
3. Aplica pressoes complementares de caixa com evidencia quando materiais.
4. Combina `ROA Final + PLRA` pelo metodo `roa_plra`.

### Fluxo 9 - Excel e Laudo

1. Usuario revisa status, bloqueios, evidencias e metodo.
2. Sistema gera Excel serializando objetos calculados.
3. Sistema gera laudo estruturado como `rascunho`, `preliminar`, `com_ressalvas`, `final` ou `bloqueado`.
4. Laudo informa empresa, exercicios, metodo, formula, PLRA, FCA/ROA, CAPAG-E, evidencias, ressalvas, bloqueios e versao metodologica.

## 10. Arquitetura de Dados

PostgreSQL sera o banco operacional da arquitetura-alvo.

### Principios de dados

- Dados brutos relevantes da ECD devem ser preservados para auditoria.
- Dados normalizados devem ser persistidos para reprocessamento e consulta.
- Resultados calculados devem ser persistidos como snapshots com versao metodologica.
- Assets metodologicos continuam versionados no repositorio e sao publicados como `MethodologyVersion`.
- Laudos e exportacoes devem apontar para snapshots e versao metodologica.
- Mudanca metodologica nao altera resultados historicos emitidos.

### Entidades principais

`companies`

- empresa analisada;
- campos minimos: `id`, `name`, `cnpj`, `created_at`, `updated_at`.

`ecd_files`

- arquivo ECD importado;
- campos minimos: `id`, `company_id`, `original_filename`, `content_hash`, `uploaded_at`, `layout_version`, `period_start`, `period_end`, `status`.

`analyses`

- analise operacional;
- campos minimos: `id`, `company_id`, `ecd_file_id`, `status`, `methodology_version_id`, `created_by`, `created_at`, `updated_at`.

`exercises`

- recorte por exercicio;
- campos minimos: `id`, `analysis_id`, `year`, `status`.

`accounts`

- contas do `I050`;
- campos minimos: `id`, `exercise_id`, `account_code`, `account_name`, `account_type`, `level`, `parent_account_code`, `is_analytical`, `nature`.

`account_references`

- vinculos `I051`;
- campos minimos: `id`, `account_id`, `reference_code`, `source_line`, `declared_at`.

`account_balances`

- saldos `I155`;
- campos minimos: `id`, `account_id`, `period`, `initial_balance`, `initial_dc`, `debits`, `credits`, `final_balance`, `final_dc`.

`entries` e `entry_lines`

- lancamentos `I200` e partidas `I250`;
- preservam numero, data, historico, conta, indicador D/C, valor, linha original e centro de custo quando existir.

`official_reference_accounts`

- plano referencial oficial;
- campos minimos: `id`, `reference_code`, `official_description`, `parent_reference_code`, `level`, `nature`, `valid_from`, `valid_to`, `layout`, `entity_type`, `source`, `status`, `methodology_version_id`.

`methodology_rules`

- regras internas por finalidade;
- campos minimos: `id`, `pattern`, `match_type`, `purpose`, `methodology_description`, `plra_category`, `fco_category`, `dfc_component`, `roa_component`, `capag_category`, `flow_nature`, `operational_treatment`, `include_in_calculation`, `sign`, `specificity_level`, `priority`, `rule_status`, `valid_from`, `valid_to`, `methodology_version_id`.

`declared_account_results`

- resultado por conta declarada;
- campos minimos: `id`, `exercise_id`, `account_id`, `declared_reference_code`, `official_description`, `methodology_rule_id`, `rule_status`, `purpose`, `treatment`, `base_value`, `considered_value`, `final_status`, `recommended_action`, `snapshot_json`.

`behavioral_profiles`

- perfil comportamental por conta;
- campos minimos: `id`, `exercise_id`, `account_id`, `metrics_json`, `created_at`, `methodology_version_id`.

`behavioral_classifications`

- classificacao sugerida;
- campos minimos: `id`, `profile_id`, `suggested_family`, `suggested_reference_code`, `score`, `confidence`, `runner_up_family`, `score_gap`, `recommended_action`, `safeguards_json`, `evidence_json`, `impact_json`, `status`.

`human_reviews`

- decisao do usuario;
- campos minimos: `id`, `classification_id`, `decision`, `chosen_reference_code`, `justification`, `comment`, `creates_precedent`, `created_by`, `created_at`.

`adjustment_evidences`

- evidencias e justificativas;
- campos minimos: `id`, `exercise_id`, `scope_type`, `scope_key`, `adjustment_type`, `method_component`, `amount_impact`, `materiality_level`, `required_evidence_type`, `evidence_status`, `analyst_justification`, `review_notes`, `blocks_final_report`, `created_at`, `updated_at`.

`asset_valuation_assessments`

- avaliacao de ativos;
- campos minimos: `id`, `exercise_id`, `account_id`, `book_value`, `default_discount_percent`, `default_economic_value`, `valuation_required`, `valuation_basis`, `forced_liquidation_value`, `analyst_adjusted_value`, `final_economic_value`, `essentiality_status`, `evidence_id`, `valuation_status`, `blocks_plra`.

`capag_assessments`

- contrato CAPAG-E;
- campos minimos: `id`, `exercise_id`, `method`, `plra_value`, `plra_status`, `fca_value`, `fca_status`, `roa_value`, `roa_status`, `capag_e_value`, `capag_e_status`, `calculation_basis`, `limitations_json`, `warnings_json`, `blocking_issues_json`, `methodology_version_id`.

`dfc_calculations`, `dfc_audit_rows`, `roa_calculations`, `roa_audit_rows`

- snapshots e auditorias de FCA e ROA.

`exports`

- exportacoes geradas;
- campos minimos: `id`, `analysis_id`, `export_type`, `status`, `file_path_or_object_key`, `content_hash`, `created_at`, `methodology_version_id`.

`capag_reports` e `report_sections`

- laudo estruturado;
- campos minimos: `id`, `analysis_id`, `status`, `assessment_method`, `capag_p_value`, `capag_e_value`, `capag_e_status`, `warnings_json`, `blocking_issues_json`, `created_at`, `methodology_version_id`.

`methodology_versions`

- versao metodologica publicada;
- campos minimos: `id`, `version_code`, `description`, `assets_manifest_json`, `coverage_status`, `changelog`, `published_at`, `published_by`.

### Consistencia e transacoes

- Importacao da ECD deve ser transacional por arquivo.
- Calculos por exercicio devem gravar snapshot atomico.
- Revisao humana deve registrar antes/depois e invalidar snapshots dependentes quando necessario.
- Geracao de laudo final deve bloquear alteracao silenciosa dos snapshots usados.

### Retencao

- ECD, snapshots, exportacoes e laudos devem ser mantidos enquanto forem necessarios para auditoria interna.
- Exclusao fisica de dados sensiveis deve ser uma rotina administrativa explicita, nao acao casual da UI.

## 11. APIs, Contratos e Integrações

A API sera REST, versionada sob `/api/v1`, com OpenAPI gerado pelo FastAPI.

### Autenticacao

```text
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

Refresh tokens sao persistidos com hash e rotacionados.

### Analises e ECD

```text
POST /api/v1/analyses
GET  /api/v1/analyses
GET  /api/v1/analyses/{analysis_id}
GET  /api/v1/analyses/{analysis_id}/exercises/{year}
```

Payload resumido de criacao:

```json
{
  "company_name": "Empresa Exemplo Ltda",
  "company_cnpj": "00000000000100",
  "ecd_file": "multipart/form-data"
}
```

### Camada Declarada

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/declared/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/declared
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/declared/accounts
```

Contrato por conta:

```json
{
  "account_code": "1725",
  "account_name": "EMPRESTIMO - SICOOB CREDICITRUS - C",
  "declared_reference_code": "2.01.01.07.01",
  "official_description": "Emprestimos e financiamentos",
  "methodology_rule_applied": "2.01.01.07.*",
  "methodology_rule_status": "ATIVA",
  "purpose": "FCO",
  "treatment": "excluir_operacional_ou_financiamento",
  "base_value": "100000.00",
  "considered_value": "0.00",
  "final_status": "MAPEADO",
  "recommended_action": null
}
```

### Camada Reclassificada

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/accounts/{account_code}
POST /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/reviews
```

Contrato de classificacao:

```json
{
  "account_code": "1234",
  "declared_reference_code": "1.01.02.02.01",
  "suggested_family": "fornecedores",
  "suggested_reference_code": "2.01.01.01.01",
  "score": 87,
  "confidence": "alta",
  "score_gap": 24,
  "recommended_action": "reclassificar",
  "safeguards": [],
  "positive_evidence": ["saldo tipico credor", "debitos contra banco", "historicos com pagamento"],
  "negative_evidence": [],
  "impact": {
    "plra": "-125000.00",
    "capag_e": "-125000.00"
  }
}
```

### Evidencias e Ativos

```text
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/evidences
POST /api/v1/analyses/{analysis_id}/exercises/{year}/evidences
PUT  /api/v1/evidences/{evidence_id}
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/assets/valuations
PUT  /api/v1/assets/valuations/{assessment_id}
```

### DFC/FCA

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/dfc/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/dfc
POST /api/v1/analyses/{analysis_id}/exercises/{year}/dfc/decisions
```

### ROA

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/roa/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/roa
POST /api/v1/analyses/{analysis_id}/exercises/{year}/roa/decisions
```

### Contrato CAPAG-E

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/capag-assessment/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/capag-assessment
```

Payload minimo:

```json
{
  "method": "fca_plra",
  "plra_value": "500000.00",
  "plra_status": "calculado",
  "fca_value": "120000.00",
  "fca_status": "calculado",
  "roa_value": null,
  "roa_status": "nao_calculado",
  "capag_e_value": "620000.00",
  "capag_e_status": "calculado",
  "methodology_formula": "CAPAG-E = PLRA + FCA",
  "limitations": [],
  "warnings": []
}
```

### Exportacao e Laudo

```text
POST /api/v1/analyses/{analysis_id}/exports/excel
GET  /api/v1/exports/{export_id}/download
GET  /api/v1/analyses/{analysis_id}/report/preview
POST /api/v1/analyses/{analysis_id}/report/generate
GET  /api/v1/reports/{report_id}
```

Integracoes externas:

- Nao ha integracao externa obrigatoria no ciclo atual.
- Upload persistente de anexos, assinatura digital, GED e protocolo externo ficam fora do escopo.

## 12. Segurança e Controle de Acesso

Autenticacao:

- JWT com access token curto.
- Refresh token rotacionado e persistido com hash.
- Logout invalida refresh token no backend.

Autorizacao:

- RBAC simples com papeis:
  - `analyst_admin`: acesso completo;
  - `analyst_readonly`: leitura e download, sem revisao ou geracao final;
  - `system`: execucao de jobs internos.

Mesmo com usuario unico no MVP, RBAC evita acoplamento da regra de seguranca ao pressuposto de uso individual.

Dados sensiveis:

- Nao versionar ECDs reais, exportacoes reais, laudos reais ou evidencias sensiveis.
- Guardar segredos em variaveis de ambiente, fora do repositorio.
- Mascarar CNPJ e nomes em logs quando o dado completo nao for necessario.
- Registrar `content_hash` do arquivo ECD para rastreabilidade sem depender apenas do nome.

Auditoria:

- Registrar importacao, execucao de motores, revisao humana, alteracao de evidencia, geracao de exportacao e emissao de laudo.
- Auditoria deve incluir usuario, timestamp, entidade afetada, acao, status anterior e status novo quando aplicavel.

Ameacas relevantes:

- vazamento de ECD ou laudo;
- alteracao metodologica sem teste;
- reprocessamento historico com metodologia nova sem aviso;
- classificacao automatica indevida por regra ampla;
- exportacao ou laudo recalculando resultado diferente do snapshot;
- frontend exibindo valor parcial como final.

Mitigacoes:

- snapshots com `methodology_version_id`;
- validacoes automatizadas de assets;
- bloqueios de status no contrato CAPAG-E;
- logs estruturados;
- testes de regressao metodologica;
- controle de acesso nos endpoints de exportacao e laudo.

## 13. Infraestrutura, Deploy e Operação

Ambiente local:

- Docker Compose com `backend`, `frontend`, `postgres` e opcional `worker`;
- volume local para PostgreSQL;
- pasta local ignorada pelo Git para exportacoes geradas;
- comando unico para subir ambiente.

Ambientes:

- `local`: desenvolvimento;
- `staging`: validacao de migrations, importacao, calculos e exportacao;
- `production`: uso interno controlado.

Deploy:

- Backend empacotado como container Python.
- Frontend gerado por Vite e servido por Nginx ou pelo provedor de frontend escolhido.
- PostgreSQL gerenciado ou containerizado conforme ambiente interno disponivel.
- Migrations Alembic executadas antes da nova versao do backend aceitar trafego.

CI/CD:

- instalar dependencias backend;
- rodar lint/format quando configurado;
- rodar `pytest`;
- validar migrations;
- validar assets metodologicos;
- instalar dependencias frontend;
- rodar `npm run build`;
- rodar Vitest;
- rodar Playwright para fluxos criticos quando houver mudanca em UI/rotas;
- publicar imagem em registry interno quando todos os checks passarem.

Backup e restore:

- backup diario do PostgreSQL em staging/producao;
- retencao minima de 30 dias para staging e 90 dias para producao, ajustavel por politica interna;
- teste de restore mensal em ambiente isolado.

Rollback:

- manter imagem anterior do backend e frontend;
- migrations destrutivas exigem plano especifico e backup;
- resultados historicos devem permanecer legiveis por versao metodologica.

Escalabilidade:

- MVP pode executar processamento sincrono.
- Se ECDs grandes causarem timeout, introduzir worker Python com tabela `jobs` no PostgreSQL.
- Nao introduzir Redis/RabbitMQ no MVP; o trade-off e menor complexidade operacional. A fila dedicada pode ser ADR futura se jobs concorrentes ou longos justificarem.

## 14. Observabilidade

Logs:

- JSON estruturado no backend;
- campos minimos: `timestamp`, `level`, `request_id`, `user_id`, `analysis_id`, `exercise_year`, `operation`, `duration_ms`, `status`;
- nao registrar conteudo bruto de ECD, historicos sensiveis ou laudos completos.

Healthcheck:

```text
GET /health
```

Deve verificar:

- processo backend ativo;
- conexao PostgreSQL;
- versao da aplicacao;
- ultima migration aplicada.

Metricas basicas:

- tempo de importacao da ECD;
- tempo de calculo da camada declarada;
- tempo de calculo comportamental;
- tempo de DFC/FCA;
- tempo de ROA;
- tempo de exportacao Excel;
- quantidade de contas analisadas;
- quantidade de regras bloqueadas/perigosas;
- quantidade de evidencias pendentes;
- quantidade de laudos bloqueados;
- erros por endpoint.

Alertas iniciais:

- API indisponivel;
- PostgreSQL indisponivel;
- migration pendente em producao;
- falha repetida na importacao de ECD;
- erro na geracao de exportacao/laudo;
- assets metodologicos invalidos no startup.

## 15. Decisões Arquiteturais

### Decisao 1 - PostgreSQL como banco operacional

Decisao:

- Usar PostgreSQL 16 como banco relacional da arquitetura-alvo.

Justificativa:

- Os modulos exigem historico, snapshots, revisoes humanas, evidencias, precedentes, versao metodologica e laudos reproduziveis.

Alternativas descartadas:

- Apenas memoria de processo: insuficiente para auditoria e laudo.
- DuckDB: fora das restricoes do PRD e inadequado como banco operacional multi-entidade.
- Arquivos JSON/CSV: fracos para transacao, consulta, auditoria e migrations.

Impacto:

- Aumenta complexidade inicial, mas remove ambiguidade sobre persistencia.

Risco:

- Modelagem excessiva cedo demais. Mitigacao: criar tabelas por modulo e migracoes pequenas.

### Decisao 2 - API REST com OpenAPI

Decisao:

- Usar REST com OpenAPI gerado pelo FastAPI.

Justificativa:

- O produto tem fluxos claros de comando/consulta e nao exige GraphQL.

Trade-off:

- Alguns payloads serao grandes; mitigacao com endpoints paginados para contas, auditorias e lancamentos.

### Decisao 3 - Camada Application obrigatoria

Decisao:

- Criar `backend/app/application/` para casos de uso.

Justificativa:

- Evita que rotas FastAPI concentrem parse, simulacao, calculo, revisao e exportacao.

Impacto:

- Testes podem validar casos de uso sem HTTP.

### Decisao 4 - Motores separados por dominio

Decisao:

- Separar motores declarada, comportamental, PLRA, DFC/FCA, ROA, CAPAG-E, evidencias e governanca.

Justificativa:

- Os modulos planejados tem fronteiras conceituais fortes e riscos diferentes.

Trade-off:

- Mais arquivos e contratos internos; mitigacao com modelos de dominio compartilhados e testes por modulo.

### Decisao 5 - Matcher metodologico seguro e compartilhado

Decisao:

- Implementar matcher unico por finalidade, com prioridade: codigo exato ativo, prefixo mais especifico ativo, prefixos menos especificos ativos, regra generica apenas se explicitamente segura.

Justificativa:

- Evita regressao como `2.01.01.07.01` cair em fornecedor por `2.01.01.*`.

Impacto:

- Assets precisam de `status_regra`, finalidade e validacoes.

### Decisao 6 - Camada reclassificada deterministica e conservadora

Decisao:

- A camada comportamental usa regras, scores e evidencias estruturadas; IA generativa nao decide.

Justificativa:

- Falso positivo em reclassificacao pode contaminar PLRA, CAPAG-E, Excel, laudo e precedentes.

Trade-off:

- Mais casos vao para revisao humana; aceitavel pelo perfil de usuario unico e pelo requisito de auditabilidade.

### Decisao 7 - Excel e laudo nao recalculam

Decisao:

- `export` e `report` apenas serializam snapshots e objetos calculados.

Justificativa:

- Garante reprodutibilidade e evita divergencia entre API, frontend, Excel e laudo.

### Decisao 8 - Assets versionados mais publicacao metodologica

Decisao:

- Manter assets no repositorio e publicar cada conjunto como `MethodologyVersion` no banco.

Justificativa:

- Preserva governanca por Git e permite snapshots historicos consultaveis.

Trade-off:

- Necessita rotina de carga/publicacao de metodologia.

### Decisao 9 - Sem fila externa no MVP

Decisao:

- Usar processamento sincrono inicialmente e evoluir para worker com tabela `jobs` no PostgreSQL quando necessario.

Justificativa:

- Produto interno, usuario unico e menor custo operacional inicial.

Risco:

- ECD grande pode estourar timeout. Mitigacao: instrumentar tempos e isolar caso de uso para futura execucao assincrona.

## 16. Estrutura de Pastas Recomendada

```text
<project-root>/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── analyses.py
│   │   │   │   ├── declared.py
│   │   │   │   ├── behavioral.py
│   │   │   │   ├── evidences.py
│   │   │   │   ├── dfc.py
│   │   │   │   ├── roa.py
│   │   │   │   ├── capag.py
│   │   │   │   ├── exports.py
│   │   │   │   ├── reports.py
│   │   │   │   └── governance.py
│   │   │   ├── dependencies.py
│   │   │   └── errors.py
│   │   ├── application/
│   │   │   ├── analyses_service.py
│   │   │   ├── declared_service.py
│   │   │   ├── behavioral_service.py
│   │   │   ├── evidence_service.py
│   │   │   ├── dfc_service.py
│   │   │   ├── roa_service.py
│   │   │   ├── capag_service.py
│   │   │   ├── export_service.py
│   │   │   ├── report_service.py
│   │   │   └── governance_service.py
│   │   ├── assets/
│   │   │   ├── reference/
│   │   │   ├── methodology/
│   │   │   └── behavioral/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── decimal.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── migrations/
│   │   ├── domain/
│   │   │   ├── analysis.py
│   │   │   ├── ecd.py
│   │   │   ├── declared.py
│   │   │   ├── behavioral.py
│   │   │   ├── evidence.py
│   │   │   ├── dfc.py
│   │   │   ├── roa.py
│   │   │   ├── capag.py
│   │   │   ├── report.py
│   │   │   ├── methodology.py
│   │   │   └── states.py
│   │   ├── engine/
│   │   │   ├── declared/
│   │   │   ├── methodology_matcher/
│   │   │   ├── behavioral/
│   │   │   ├── plra/
│   │   │   ├── dfc/
│   │   │   ├── roa/
│   │   │   ├── capag/
│   │   │   ├── evidence/
│   │   │   └── governance/
│   │   ├── export/
│   │   │   ├── excel.py
│   │   │   └── workbook_sections/
│   │   ├── io/
│   │   │   ├── ecd_reader.py
│   │   │   ├── ecd_parser.py
│   │   │   └── ecd_normalizer.py
│   │   ├── models/
│   │   │   ├── analysis.py
│   │   │   ├── ecd.py
│   │   │   ├── methodology.py
│   │   │   ├── results.py
│   │   │   ├── evidence.py
│   │   │   └── report.py
│   │   ├── repositories/
│   │   │   ├── analyses.py
│   │   │   ├── ecd.py
│   │   │   ├── methodology.py
│   │   │   ├── results.py
│   │   │   ├── evidence.py
│   │   │   └── reports.py
│   │   ├── report/
│   │   │   ├── builder.py
│   │   │   └── validators.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── analyses.py
│   │   │   ├── declared.py
│   │   │   ├── behavioral.py
│   │   │   ├── evidence.py
│   │   │   ├── dfc.py
│   │   │   ├── roa.py
│   │   │   ├── capag.py
│   │   │   ├── exports.py
│   │   │   └── reports.py
│   │   └── main.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── golden/
│   │   └── fixtures/
│   ├── pyproject.toml
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── router.tsx
│   │   │   ├── query-client.ts
│   │   │   └── layout.tsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── AnalysisPage.tsx
│   │   │   ├── DeclaredLayerPage.tsx
│   │   │   ├── BehavioralReviewPage.tsx
│   │   │   ├── EvidencesPage.tsx
│   │   │   ├── DfcPage.tsx
│   │   │   ├── RoaPage.tsx
│   │   │   ├── ResultPage.tsx
│   │   │   ├── ReportPage.tsx
│   │   │   └── MethodologyGovernancePage.tsx
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── analyses/
│   │   │   ├── ecd-upload/
│   │   │   ├── declared-layer/
│   │   │   ├── behavioral-review/
│   │   │   ├── evidences/
│   │   │   ├── asset-valuation/
│   │   │   ├── dfc/
│   │   │   ├── roa/
│   │   │   ├── capag-assessment/
│   │   │   ├── exports/
│   │   │   ├── report/
│   │   │   └── methodology-governance/
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   ├── formatters/
│   │   │   ├── hooks/
│   │   │   └── validation/
│   │   ├── lib/
│   │   │   ├── api/
│   │   │   └── auth/
│   │   ├── styles/
│   │   └── main.tsx
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
├── infra/
│   ├── docker/
│   │   ├── backend.Dockerfile
│   │   ├── frontend.Dockerfile
│   │   └── nginx.conf
│   └── compose.yaml
├── docs/
│   ├── architecture.md
│   ├── adr/
│   ├── product/
│   ├── reference/
│   ├── specs/
│   └── methodology/
├── scripts/
│   ├── validate_methodology.py
│   ├── publish_methodology.py
│   └── export_openapi.py
└── README.md
```

Responsabilidades:

- `backend/app/api`: superficie HTTP, sem regra prudencial.
- `backend/app/application`: casos de uso e transacoes.
- `backend/app/domain`: contratos e invariantes livres de framework.
- `backend/app/engine`: calculos, regras, scores e auditoria.
- `backend/app/io`: ECD bruta e normalizada.
- `backend/app/repositories`: persistencia SQLAlchemy.
- `backend/app/export`: Excel e serializacao de saida.
- `backend/app/report`: laudo estruturado e validacoes de emissao.
- `frontend/src/features`: UI por modulo do PRD.
- `docs/adr`: decisoes arquiteturais futuras.
- `docs/methodology`: matriz de rastreabilidade e changelog metodologico.
- `scripts`: validacoes e rotinas operacionais automatizaveis.

## 17. Plano Técnico de Implementação

### Fase 0 - Fundacao do repositorio

1. Criar `backend/`, `frontend/`, `infra/`, `docs/adr/`, `docs/methodology/` e `scripts/`.
2. Configurar FastAPI, Pydantic, SQLAlchemy, Alembic e PostgreSQL.
3. Configurar React/Vite/TypeScript, React Router, TanStack Query, React Hook Form, Zod e Tailwind.
4. Configurar Docker Compose.
5. Configurar GitHub Actions com backend tests, frontend build e validacao de assets.

Entregavel:

- aplicacao inicial sobe localmente com backend, frontend e PostgreSQL.

### Fase 1 - Persistencia e metodologia versionada

1. Criar migrations para empresas, ECDs, analises, exercicios e versao metodologica.
2. Implementar carga/publicacao de assets metodologicos.
3. Criar validacoes de colunas, status, componentes e prefixos perigosos.
4. Registrar `methodology_version` em toda analise.

Entregavel:

- metodologia versionada carregada e validada no banco.

### Fase 2 - Importacao ECD

1. Implementar reader/parser/normalizer.
2. Persistir contas, vinculos `I051`, saldos, lancamentos e partidas.
3. Criar endpoints de analise e upload.
4. Testar fixtures ECD e casos de encoding/valores.

Entregavel:

- ECD importada e consultavel por empresa/exercicio.

### Fase 3 - Modulo 1 Camada Declarada

1. Implementar plano referencial oficial.
2. Implementar matcher metodologico seguro.
3. Implementar resultados por conta declarada.
4. Ajustar PLRA/FCO declarado.
5. Expor API e tela de camada declarada.
6. Gerar abas Excel declaradas.
7. Testar conta `1725`, bloqueio de prefixo amplo e regra mais especifica.

Entregavel:

- leitura declarada auditavel e protegida contra prefixos perigosos.

### Fase 4 - Modulo 3 Contrato CAPAG-E

1. Implementar `CapagEAssessment`.
2. Implementar metodos e status.
3. Mapear `PLR ajustado` para `PLRA`.
4. Diferenciar `FCO`, `FCA parcial` e `FCA final`.
5. Expor API, UI e bloco Excel `contrato_capag_e`.

Entregavel:

- contrato canonico consumido por frontend, exportacao e laudo futuro.

### Fase 5 - Modulo 4 Evidencias e Ativos

1. Implementar `AdjustmentEvidence`.
2. Implementar materialidade default e revisao controlada.
3. Implementar `AssetValuationAssessment`.
4. Integrar bloqueios de `PLRA` e laudo.
5. Criar APIs e telas de evidencias/ativos.
6. Criar abas Excel `evidencias_justificativas` e `avaliacao_ativos`.

Entregavel:

- ajustes materiais possuem justificativa, evidencia, bloqueio ou ressalva.

### Fase 6 - Modulo 2 CAPAG Reclassificada

1. Implementar razao por conta e contrapartidas.
2. Implementar perfil comportamental.
3. Implementar familias MVP.
4. Implementar score, confianca e salvaguardas.
5. Implementar mapeamento familia -> referencial.
6. Implementar comparativo declarado vs reclassificado.
7. Implementar revisao humana.
8. Criar tela de revisao comportamental.
9. Criar exportacao comparativa.

Entregavel:

- cenario comportamental auditavel, conservador e revisavel.

### Fase 7 - Modulo 5 DFC/FCA

1. Implementar assets DFC.
2. Implementar identificacao de fluxos com caixa.
3. Implementar classificacao operacional, investimento e financiamento.
4. Implementar pendencias e evidencias materiais.
5. Calcular `FCA`.
6. Expor API, tela e abas Excel.

Entregavel:

- `FCA` auditavel por lancamento e distinguido de `FCO`.

### Fase 8 - Modulo 6 ROA + PLRA

1. Implementar assets ROA.
2. Implementar classificacao de contas de resultado.
3. Implementar formula ROA.
4. Implementar pressoes complementares de caixa.
5. Integrar evidencias.
6. Integrar `ROA + PLRA` ao contrato CAPAG-E.

Entregavel:

- caminho alternativo `CAPAG-E = ROA + PLRA`.

### Fase 9 - Modulo 7 Laudo CAPAG-E

1. Implementar `CapagReport` e `ReportSection`.
2. Implementar validacoes de status do laudo.
3. Implementar preview e geracao.
4. Implementar abas de laudo no Excel.
5. Garantir que laudo nao chama motores.

Entregavel:

- laudo estruturado final, preliminar, com ressalvas ou bloqueado.

### Fase 10 - Modulo 8 Governanca

1. Criar matriz de rastreabilidade metodologica.
2. Criar changelog metodologico.
3. Ampliar validacoes automatizadas.
4. Expor UI opcional de versao/cobertura.
5. Atualizar README, AGENTS, CLAUDE e skills por ultimo.

Entregavel:

- governanca entre docs, specs, assets, codigo, testes, Excel e laudo.

## 18. Riscos, Trade-offs e Mitigações

Risco: modelagem de banco grande demais no inicio.

- Mitigacao: migracoes por modulo, snapshots JSON apenas onde o contrato ainda estiver evoluindo e normalizacao gradual dos campos de consulta frequente.

Risco: regra metodologica ampla distorcer resultado declarado.

- Mitigacao: `status_regra`, matcher seguro, validacao de prefixos, testes obrigatorios da conta `1725`.

Risco: reclassificacao comportamental virar busca por palavra-chave.

- Mitigacao: exigir conjunto de evidencias, score, diferenca entre familias, salvaguardas e revisao humana para materialidade alta.

Risco: frontend recalcular valor prudencial.

- Mitigacao: contratos de API com valores prontos, testes de UI e revisao de componentes para impedir logica prudencial local.

Risco: Excel ou laudo divergirem do backend.

- Mitigacao: export/report apenas serializam snapshots; golden tests para workbooks e testes de laudo sem chamada de motor.

Risco: metodologia mudar e alterar laudos historicos.

- Mitigacao: `MethodologyVersion`, snapshots, manifest de assets e bloqueio de retroatividade silenciosa.

Risco: ECD grande causar timeout.

- Mitigacao: medir tempos por etapa, paginar consultas, introduzir worker com tabela `jobs` se necessario.

Risco: dados sensiveis vazarem em logs ou repositorio.

- Mitigacao: politica de artefatos, `.gitignore`, mascaramento em logs e proibicao de versionar ECD/laudo real.

Risco: excesso de status confundir usuario.

- Mitigacao: glossario canonico, UI consistente, status permitidos por componente e mensagens objetivas de bloqueio/ressalva.

## 19. Perguntas Abertas

- Qual sera o ambiente de producao interno: servidor unico, container platform, VM ou PaaS?
- Onde exportacoes Excel e laudos gerados ficarao armazenados: filesystem local controlado ou object storage interno?
- Qual politica de retencao formal deve ser aplicada a ECDs, exportacoes, evidencias e laudos?
- O MVP deve ter apenas `analyst_admin` ou tambem `analyst_readonly` desde a primeira versao?
- O suporte a `J150` entra junto com ROA ou como etapa preparatoria anterior?
- Precedentes da camada reclassificada entram no MVP ou ficam para fase posterior apos calibracao?
- Laudo futuro deve permanecer apenas em Excel estruturado ou deve ganhar DOCX/PDF em fase posterior?
- Qual criterio quantitativo de materialidade default sera aprovado para evidencias e revisoes?
- Quais assets metodologicos atuais serao migrados primeiro para `MethodologyVersion`?
- A organizacao deseja manter compatibilidade nominal com pastas antigas `src/capag` e `web` ou migrar diretamente para `backend/` e `frontend/`?
