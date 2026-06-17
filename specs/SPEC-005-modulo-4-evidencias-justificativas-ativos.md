# SPEC-005 - Modulo 4: Evidencias, Justificativas E Avaliacao De Ativos

## 1. Objetivo Tecnico

Especificar a camada de evidencias, justificativas, materialidade, bloqueios, ressalvas e avaliacao de ativos do CAPAG.

Esta SPEC transforma ajustes metodologicos, revisoes humanas e avaliacao patrimonial em trilha documental defensavel para `PLRA`, `FCA`, `ROA`, `CAPAG-E`, Excel e laudo futuro.

## 2. Contexto E Problema

O PRD exige que toda conta material ajustada ou reclassificada possua justificativa, evidencia, status e trilha auditavel. A arquitetura define entidades para `AdjustmentEvidence` e `AssetValuationAssessment`, alem de bloqueios que alimentam o contrato CAPAG-E e o laudo.

Sem essa camada, ajustes materiais podem alterar `PLRA` ou `CAPAG-E` sem suporte documental, e ativos relevantes podem ser tratados por desagio padrao sem diferenciar valor contabil, valor prudencial default, valor avaliado e liquidacao forcada.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture.md`

Fontes de referencia autorizadas pelo usuario:

- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/01-matriz-cobertura-spec-07-08.md`
- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/02-modelo-evidencias-materialidade.md`
- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/03-avaliacao-ativos-liquidacao-forcada.md`
- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/04-integracao-plra-bloqueios.md`
- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/05-api-frontend-exportacao.md`
- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/06-testes-evidencias-ativos.md`
- `docs/reference/planejamento-modulos/modulo-04-evidencias-avaliacao-ativos/07-roadmap-execucao-modulo-4.md`

Fontes frontend governadas:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Decisao aprovada pelo usuario nesta SPEC:

- Materialidade default sera politica hibrida calculada automaticamente por impacto percentual no componente afetado, com override manual justificado e regras conservadoras.

## 4. Escopo

Esta SPEC cobre:

- entidade `AdjustmentEvidence`;
- escopos de evidencia;
- tipos de status de evidencia;
- politica default de materialidade;
- override manual de materialidade;
- bloqueios e ressalvas;
- avaliacao de ativos relevantes;
- entidade `AssetValuationAssessment`;
- classificacao de realizabilidade;
- base de avaliacao;
- integracao com `PLRA`;
- API, frontend, exportacao e consumo futuro pelo laudo;
- testes de evidencias e ativos.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- upload persistente de anexos;
- assinatura digital;
- integracao com GED;
- laudo ABNT completo;
- avaliacao imobiliaria real;
- recalcular motores no frontend, Excel ou laudo;
- definir DFC/FCA, ROA ou laudo final;
- administracao livre de regras criticas pela UI.

## 6. Decisoes Ja Aprovadas

- Evidencia nao altera valor calculado por si so.
- Evidencia explica, sustenta, bloqueia ou ressalva.
- Ajuste material deve ter justificativa.
- Ajuste critico sem evidencia validada deve bloquear resultado/laudo final ou gerar ressalva explicita conforme regra.
- Ajuste de baixa materialidade pode ser agrupado, mas nao deve sumir da auditoria.
- Materialidade default sera calculada pelo backend.
- Analista pode revisar materialidade de forma controlada com justificativa.
- Evidencias criticas pendentes bloqueiam resultado final ou geram ressalva conforme regra.
- Valor base de ativo vem da ECD.
- Politica de desagio atual continua como default.
- Valor de liquidacao forcada validado prevalece sobre desagio default.
- Valor manual exige justificativa e evidencia.
- Ativo sem realizabilidade vai a valor economico zero.
- Ativo essencial nao deve ser automaticamente excluido.

## 7. Decisoes Pendentes

Nao ha bloqueio para criar TASKs do Modulo 4 conforme esta SPEC.

Decisoes de modulos posteriores:

- O Modulo 7 definira exatamente como bloqueio e ressalva aparecem no laudo narrativo.
- O Modulo 8 governara alteracoes futuras dos limiares de materialidade e politicas de desagio.

## 8. Contratos

### 8.1 `AdjustmentEvidence`

Campos minimos:

- `evidence_id`;
- `exercise_year`;
- `scope_type`;
- `scope_key`;
- `adjustment_type`;
- `method_component`;
- `amount_impact`;
- `impact_base_value`;
- `impact_percent`;
- `materiality_level`;
- `materiality_source`;
- `required_evidence_type`;
- `evidence_status`;
- `analyst_justification`;
- `review_notes`;
- `blocks_final_report`;
- `created_at`;
- `updated_at`;
- `methodology_version_id`.

### 8.2 Escopos Permitidos

- `account`;
- `methodology_group`;
- `macrogroup`;
- `fco_movement`;
- `dfc_component`;
- `roa_component`;
- `asset_valuation`;
- `manual_override`;
- `capag_assessment`.

### 8.3 Componentes Metodologicos

- `PLRA`;
- `FCA`;
- `ROA`;
- `CAPAG-E`.

### 8.4 Status De Evidencia

- `nao_exigida`;
- `pendente`;
- `informada`;
- `validada`;
- `dispensada_com_justificativa`;
- `rejeitada`.

### 8.5 Materialidade

Niveis permitidos:

- `baixa`;
- `media`;
- `alta`;
- `critica`.

Politica default inicial:

- `baixa`: impacto absoluto menor que `1%` do componente afetado;
- `media`: impacto absoluto maior ou igual a `1%` e menor que `5%`;
- `alta`: impacto absoluto maior ou igual a `5%` e menor que `10%`;
- `critica`: impacto absoluto maior ou igual a `10%`.

Base do percentual:

- para ajuste de `PLRA`, usar valor-base do `PLRA` antes do ajuste, quando disponivel;
- para ajuste de `FCA`, usar valor-base do `FCA` ou componente de fluxo afetado, quando disponivel;
- para ajuste de `ROA`, usar valor-base do `ROA` ou componente de resultado afetado, quando disponivel;
- para ajuste de `CAPAG-E`, usar valor-base da `CAPAG-E` antes do ajuste, quando disponivel.

Regras conservadoras:

- se a base percentual for zero, negativa, ausente ou instavel, materialidade minima `media` e revisao humana obrigatoria;
- se o ajuste puder mudar status final da `CAPAG-E`, materialidade minima `alta`;
- se o ajuste puder inverter sinal de componente prudencial, materialidade minima `alta`;
- se houver evidencia critica pendente em item `alta` ou `critica`, bloquear resultado final ou laudo final ate validacao, dispensa justificada ou ressalva explicita;
- override manual de materialidade exige justificativa e registro antes/depois.

### 8.6 `AssetValuationAssessment`

Campos minimos:

- `assessment_id`;
- `exercise_year`;
- `account_code`;
- `account_name`;
- `reference_code`;
- `macrogroup`;
- `book_value`;
- `default_desagio_percent`;
- `default_economic_value`;
- `valuation_required`;
- `valuation_basis`;
- `forced_liquidation_value`;
- `analyst_adjusted_value`;
- `final_economic_value`;
- `essentiality_status`;
- `evidence_id`;
- `valuation_status`;
- `blocks_plra`;
- `methodology_version_id`.

### 8.7 Ativos Alvo

- imoveis;
- terrenos;
- maquinas e equipamentos;
- veiculos;
- moveis e utensilios relevantes;
- ativos mantidos para venda;
- investimentos e participacoes;
- intangiveis materiais;
- direitos creditorios relevantes;
- creditos judiciais.

### 8.8 Classificacao De Realizabilidade

- `liquidez_imediata`;
- `realizavel_curto_prazo`;
- `realizavel_longo_prazo`;
- `liquidacao_forcada_exige_laudo`;
- `ativo_operacional_essencial`;
- `ativo_sem_realizabilidade`;
- `ativo_condicional`.

### 8.9 Base De Avaliacao

- `politica_interna`;
- `laudo_abnt_nbr_14653`;
- `documento_suporte`;
- `estimativa_analista`;
- `nao_aplicavel`.

### 8.10 Regras De Ativos

- Valor base vem da ECD.
- Desagio default vem da politica metodologica versionada.
- Valor de liquidacao forcada validado prevalece sobre desagio default.
- Valor manual exige justificativa e evidencia.
- Ativo sem realizabilidade vai a valor economico zero.
- Ativo essencial nao deve ser automaticamente excluido.
- Ativo material sem suporte documental deve bloquear ou ressalvar conforme materialidade.
- Auditoria deve mostrar valor contabil, desagio default, valor de liquidacao e valor final.

### 8.11 Bloqueios E Ressalvas

Bloquear ou ressalvar `PLRA`/resultado/laudo quando:

- ativo material exige laudo e esta pendente;
- ativo material tem valor manual sem justificativa;
- ativo essencial foi excluido sem justificativa operacional;
- ativo com liquidacao forcada nao tem base documental;
- evidencia critica esta pendente;
- evidencia foi rejeitada;
- justificativa obrigatoria esta vazia;
- ajuste material nao tem tipo de evidencia definido.

### 8.12 API

Endpoints alvo:

```text
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/evidences
POST /api/v1/analyses/{analysis_id}/exercises/{year}/evidences
PUT  /api/v1/evidences/{evidence_id}
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/assets/valuations
PUT  /api/v1/assets/valuations/{assessment_id}
```

Valores monetarios e percentuais devem ser serializados como strings decimais.

### 8.13 Frontend

Rotas alvo:

```text
/analises/:analysisId/exercicios/:year/evidencias
```

A tela deve conter:

- evidencias por exercicio;
- filtros por componente;
- filtros por status;
- edicao de justificativa;
- selecao de tipo de evidencia;
- resumo de impacto monetario;
- painel de ativos relevantes;
- valor contabil, default e avaliado;
- status de laudo/avaliacao.

Frontend nao pode recalcular materialidade, `PLRA` ou bloqueios. Pode solicitar override justificado ao backend.

### 8.14 Exportacao E Laudo

Abas de Excel:

- `evidencias_justificativas`;
- `avaliacao_ativos`.

O laudo futuro deve consumir:

- ajustes materiais;
- justificativas;
- tipo de evidencia exigida;
- status da evidencia;
- ressalvas;
- ativos relevantes ajustados;
- base de avaliacao;
- ausencia ou presenca de laudo externo.

## 9. Responsabilidades Por Camada

### Domain

Modelar evidencias, materialidade, avaliacao de ativos, status, bloqueios e invariantes.

### Engine

Calcular materialidade default, aplicar regras de bloqueio/ressalva e entregar avaliacoes ao motor afetado.

### Application

Orquestrar criacao/atualizacao de evidencias, override de materialidade, avaliacao de ativos e invalidacao de snapshots dependentes.

### API

Validar payloads, serializar `Decimal` e expor evidencias/ativos sem regra prudencial na rota.

### Frontend

Permitir revisao operacional e justificativas sem recalcular regra.

### Export

Serializar evidencias, justificativas e avaliacao de ativos.

### Report

Consumir evidencias e bloqueios no laudo futuro, sem recalcular.

## 10. Dados De Entrada E Saida

Entradas:

- resultados de PLRA/FCA/ROA/CAPAG-E;
- ajustes metodologicos;
- revisoes humanas;
- avaliacoes de ativos;
- politicas de desagio;
- justificativas do analista;
- status de evidencias.

Saidas:

- `AdjustmentEvidence`;
- `AssetValuationAssessment`;
- materialidade default;
- overrides justificados;
- bloqueios e ressalvas;
- dados para contrato CAPAG-E;
- abas Excel;
- dados para laudo futuro.

## 11. Estados E Erros Relevantes

Estados principais:

- evidencia `pendente`, `informada`, `validada`, `dispensada_com_justificativa`, `rejeitada`;
- avaliacao `nao_exigida`, `pendente`, `validada`, `rejeitada`, `bloqueante`;
- materialidade `baixa`, `media`, `alta`, `critica`.

Erros e bloqueios:

- override de materialidade sem justificativa;
- valor manual sem evidencia;
- evidencia critica pendente;
- evidencia rejeitada;
- ativo material sem laudo/base documental;
- ativo essencial excluido sem justificativa;
- tentativa de usar `float`;
- tentativa de alterar valor calculado diretamente pela evidencia;
- tentativa de recalcular no frontend/exportacao.

## 12. Criterios De Aceite

- Ajuste material possui justificativa.
- Materialidade default e calculada pelo backend.
- Faixas percentuais default estao versionadas.
- Override de materialidade exige justificativa e registra antes/depois.
- Evidencia critica pendente bloqueia ou ressalva resultado final.
- Evidencia nao altera valor calculado por si so.
- Ativo com laudo validado substitui desagio default.
- Ativo material sem laudo gera bloqueio ou ressalva.
- Ativo essencial excluido sem justificativa bloqueia.
- Valor manual exige evidencia.
- Auditoria exibe valor contabil, default e final.
- API serializa evidencias e ativos.
- Frontend nao recalcula materialidade.
- Excel inclui `evidencias_justificativas` e `avaliacao_ativos`.

## 13. Estrategia De Validacao Esperada

Testes obrigatorios:

- criar evidencia por decisao metodologica manual;
- calcular materialidade a partir do impacto;
- aplicar faixas `1%`, `5%` e `10%`;
- elevar materialidade quando ajuste puder mudar status da `CAPAG-E`;
- exigir revisao quando base percentual for zero, negativa ou ausente;
- bloquear laudo final quando evidencia critica estiver pendente;
- permitir evidencia dispensada com justificativa;
- rejeitar override de materialidade sem justificativa;
- serializar evidencias na API;
- exportar evidencias na aba correta;
- garantir que evidencia nao altera valor calculado por si so;
- validar ativo com laudo substituindo desagio default;
- validar ativo material sem laudo gerando bloqueio ou ressalva;
- validar ativo essencial excluido sem justificativa;
- validar valor manual exigindo evidencia;
- validar auditoria de valor contabil, default e final.

## 14. Riscos E Mitigacoes

- Risco: materialidade virar julgamento subjetivo.
  Mitigacao: politica default calculada, versionada e override justificado.

- Risco: evidencia ser tratada como motor de calculo.
  Mitigacao: evidencia sustenta/bloqueia/ressalva, mas nao altera valor sozinha.

- Risco: ativo material passar por desagio default sem suporte.
  Mitigacao: bloqueios por materialidade e avaliacao obrigatoria.

- Risco: frontend mascarar pendencia documental.
  Mitigacao: status e bloqueios vindos do backend.

- Risco: laudo futuro omitir ressalva.
  Mitigacao: contrato explicito de evidencias e `blocks_final_report`.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs do Modulo 4 conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- emitir resultado/laudo final ignorando evidencia critica pendente;
- ajustar materialidade sem justificativa;
- aplicar valor manual de ativo sem evidencia;
- usar desagio default como avaliacao real;
- recalcular regra prudencial no frontend, Excel ou laudo.
