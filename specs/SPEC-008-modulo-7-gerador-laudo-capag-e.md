# SPEC-008 - Modulo 7: Gerador De Laudo CAPAG-E

## 1. Objetivo Tecnico

Especificar o gerador de laudo CAPAG-E estruturado, consumindo resultados calculados, evidencias, ajustes, bloqueios, ressalvas e versao metodologica sem recalcular motores.

## 2. Contexto E Problema

O PRD exige que o CAPAG gere laudo CAPAG-E estruturado a partir de resultados ja calculados. A arquitetura define camada `report` para montar `CapagReport` a partir de `CapagEAssessment`, evidencias, bloqueios e snapshots, sem executar motores.

O problema central e transformar analise auditavel, contrato CAPAG-E, evidencias e resultados em um artefato reprodutivel que nao esconda limitacoes, pendencias, ressalvas ou bloqueios.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture.md`

Fontes de referencia autorizadas pelo usuario:

- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/01-matriz-cobertura-spec-11.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/02-formatos-saida-exportacao.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/03-estrutura-secoes-laudo.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/04-modelo-dominio-laudo.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/05-validacoes-status-laudo.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/06-api-frontend-fluxo-laudo.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/07-testes-laudo-capag-e.md`
- `docs/reference/planejamento-modulos/modulo-07-gerador-laudo-capag-e/08-roadmap-execucao-modulo-7.md`

Fontes frontend governadas:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## 4. Escopo

Esta SPEC cobre:

- modelo `CapagReport`;
- modelo `ReportSection`;
- secoes obrigatorias do laudo;
- status do laudo;
- validacoes antes da emissao;
- preview e geracao;
- saida minima em Excel estruturado;
- API;
- frontend;
- testes.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- assinatura digital;
- protocolo no REGULARIZE/SICAR;
- geracao automatica de anexos externos;
- laudo ABNT completo;
- DOCX/PDF no MVP;
- recalculo de `PLRA`, `FCA`, `ROA` ou `CAPAG-E`.

## 6. Decisoes Ja Aprovadas

- Laudo nao recalcula `PLRA`, `FCA`, `ROA` ou `CAPAG-E`.
- Laudo consome objetos calculados e snapshots.
- Implementacao minima: Excel com abas de memoria e laudo estruturado.
- Implementacao futura desejavel: DOCX, PDF e pacote de anexos.
- Laudo deve informar metodo, formula, valores, bloqueios, ressalvas e evidencias materiais.
- Laudo pode ser preliminar quando limitacoes estiverem claras.
- Falha de validacao vira status, bloqueio ou ressalva.

## 7. Decisoes Pendentes

Nao ha bloqueio para criar TASKs do Modulo 7 conforme esta SPEC.

Decisoes futuras:

- Formato DOCX/PDF e identidade visual documental.
- Armazenamento fisico definitivo de laudos gerados.
- Politica formal de retencao.

## 8. Contratos

### 8.1 `CapagReport`

Campos minimos:

- `report_id`;
- `analysis_id`;
- `company`;
- `cnpj`;
- `created_at`;
- `responsible_name`;
- `assessment_method`;
- `capag_p_value`;
- `capag_e_value`;
- `capag_e_status`;
- `exercises`;
- `sections`;
- `warnings`;
- `blocking_issues`;
- `attachments_index`;
- `methodology_version_id`.

### 8.2 `ReportSection`

Campos minimos:

- `section_code`;
- `title`;
- `status`;
- `summary_text`;
- `tables`;
- `source_refs`;
- `warnings`.

### 8.3 Secoes Obrigatorias

1. Identificacao.
2. Contexto do pedido.
3. Metodo de calculo.
4. Base de dados.
5. `PLRA`.
6. `FCA`, quando usado.
7. `ROA`, quando usado.
8. Evidencias e justificativas.
9. Resultado `CAPAG-E`.
10. Ressalvas e limitacoes.

### 8.4 Dados Minimos

- empresa;
- CNPJ;
- exercicios;
- data de emissao;
- responsavel;
- ECDs usadas;
- metodo;
- formula;
- valores;
- bloqueios;
- ressalvas;
- evidencias materiais;
- versao metodologica.

### 8.5 Status Do Laudo

- `rascunho`;
- `preliminar`;
- `com_ressalvas`;
- `final`;
- `bloqueado`.

### 8.6 Validacoes Para Laudo Final

- Metodo de calculo definido.
- `PLRA` final disponivel.
- `FCA` ou `ROA` final disponivel conforme metodo.
- Evidencias criticas nao pendentes.
- Nenhuma conta metodologica bloqueante.
- Versao metodologica identificada.

### 8.7 Formatos De Saida

MVP:

- Excel com abas de memoria e laudo estruturado.

Abas futuras/minimas no Excel:

- `laudo_resumo`;
- `laudo_metodologia`;
- `laudo_ressalvas`;
- `laudo_evidencias`.

Futuro:

- DOCX;
- PDF;
- pacote de anexos.

### 8.8 API

Endpoints alvo:

```text
GET  /api/v1/analyses/{analysis_id}/report/preview
POST /api/v1/analyses/{analysis_id}/report/generate
GET  /api/v1/reports/{report_id}
```

Payload minimo de geracao:

- `assessment_method`;
- `capag_p_value`;
- `responsible_name`;
- `include_preliminary_sections`.

### 8.9 Frontend

Rota alvo:

```text
/analises/:analysisId/laudo
```

Fluxo de laudo:

- selecao do metodo;
- campo para `CAPAG-P`;
- responsavel pela analise;
- preview de secoes;
- lista de bloqueios;
- lista de ressalvas;
- botao de exportacao.

Frontend nao pode recalcular resultado.

## 9. Responsabilidades Por Camada

### Domain

Modelar `CapagReport`, `ReportSection`, status, validacoes e referencias de origem.

### Report

Montar laudo estruturado a partir de snapshots, contrato CAPAG-E, evidencias e bloqueios.

### Application

Orquestrar preview, geracao, persistencia, controle de status e auditoria.

### API

Expor preview, geracao e consulta de laudo.

### Frontend

Exibir preview, bloqueios, ressalvas e acionar geracao/exportacao sem recalculo.

### Export

Serializar laudo estruturado em Excel.

## 10. Dados De Entrada E Saida

Entradas:

- `CapagEAssessment`;
- `PLRA`;
- `FCA`;
- `ROA`;
- evidencias e justificativas;
- bloqueios;
- ressalvas;
- snapshots;
- versao metodologica;
- dados da empresa e responsavel.

Saidas:

- `CapagReport`;
- `ReportSection`;
- preview de laudo;
- Excel estruturado;
- status do laudo;
- auditoria de geracao.

## 11. Estados E Erros Relevantes

Erros e bloqueios:

- metodo ausente;
- `PLRA` ausente ou bloqueada;
- componente `FCA`/`ROA` final ausente conforme metodo;
- evidencia critica pendente;
- conta metodologica bloqueante;
- tentativa de recalculo no laudo;
- ausencia de versao metodologica;
- tentativa de gerar laudo final com status parcial.

## 12. Criterios De Aceite

- Laudo informa metodo, formula e valores.
- Laudo lista evidencias e justificativas relevantes.
- Laudo mostra ressalvas e bloqueios.
- Laudo nao recalcula motores.
- Laudo final exige metodo definido.
- Laudo final exige `PLRA` final.
- Laudo final exige `FCA` ou `ROA` final conforme metodo.
- Laudo preliminar pode existir com limitacao explicita.
- Excel permite reconstruir conclusao sem depender da UI.

## 13. Estrategia De Validacao Esperada

Testes obrigatorios:

- gerar laudo final com `FCA + PLRA`;
- gerar laudo final com `ROA + PLRA`;
- bloquear laudo sem metodo;
- bloquear laudo sem `PLRA`;
- gerar laudo preliminar com `FCA parcial`;
- incluir evidencias materiais;
- incluir ressalvas por evidencia pendente;
- garantir que o laudo nao chama motores;
- validar abas `laudo_resumo`, `laudo_metodologia`, `laudo_ressalvas`, `laudo_evidencias`.

## 14. Riscos E Mitigacoes

- Risco: laudo recalcular e divergir da API.
  Mitigacao: `report` consome snapshots e contrato CAPAG-E.

- Risco: laudo omitir ressalva.
  Mitigacao: secoes obrigatorias e validacoes de status.

- Risco: usuario emitir final com componente parcial.
  Mitigacao: validacoes para status final.

- Risco: metodologia mudar apos emissao.
  Mitigacao: versionamento metodologico no report.

- Risco: dados sensiveis vazarem em logs/exportacoes.
  Mitigacao: nao registrar conteudo bruto e controlar arquivos gerados.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs do Modulo 7 conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- recalcular motores no laudo;
- gerar laudo final sem metodo;
- gerar laudo final sem `PLRA` final;
- esconder evidencia critica pendente;
- tratar laudo preliminar como final;
- implementar DOCX/PDF como obrigatorio do MVP sem decisao adicional.
