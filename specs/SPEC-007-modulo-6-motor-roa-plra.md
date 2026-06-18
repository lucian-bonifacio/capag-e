# SPEC-007 - Modulo 6: Motor ROA + PLRA

## 1. Objetivo Tecnico

Especificar o motor `ROA + PLRA`, caminho alternativo para calcular `CAPAG-E` a partir de resultado operacional ajustado (`ROA`) combinado com `PLRA`.

## 2. Contexto E Problema

O PRD exige implementar o caminho alternativo `CAPAG-E = ROA + PLRA`. A arquitetura define motor `roa`, contrato CAPAG-E com metodo `roa_plra` e integração com evidências quando despesas ou pressões materiais exigirem justificativa.

O problema central e calcular um `ROA` auditavel por conta referencial, separando receita, deducoes, tributos, custos, despesas, resultado financeiro, resultado nao operacional e pressoes complementares de caixa sem duplicar calculo patrimonial de `PLRA`.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`

Fontes de referencia autorizadas pelo usuario:

- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/01-matriz-cobertura-spec-10.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/02-entrada-contas-resultado-ecd.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/03-metodologia-roa-componentes.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/04-motor-roa-calculo.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/05-pressoes-complementares-caixa.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/06-pendencias-evidencias-roa.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/07-integracao-plra-capag-e.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/08-api-frontend-exportacao-roa.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/09-testes-roa-plra.md`
- `docs/reference/planejamento-modulos/modulo-06-motor-roa-plra/10-roadmap-execucao-modulo-6.md`

Fontes frontend governadas:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## 4. Escopo

Esta SPEC cobre:

- entradas ECD para contas de resultado;
- suporte incremental a `J150`;
- assets e componentes ROA;
- entidade `RoaCalculation`;
- entidade `RoaAuditRow`;
- formula do ROA;
- regras de sinal;
- pressoes complementares de caixa;
- pendencias e evidencias;
- integracao `ROA + PLRA`;
- API, frontend, exportacao e testes.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- DFC direta completa;
- laudo textual;
- persistencia documental final alem dos snapshots definidos pela arquitetura;
- recalculo de `PLRA`;
- recalculo em frontend, Excel ou laudo;
- classificacao por nome livre como criterio principal.

## 6. Decisoes Ja Aprovadas

- O metodo CAPAG-E deste modulo e `roa_plra`.
- Quando houver FCA tambem, o contrato pode usar `comparativo_fca_roa`.
- O motor ROA nao recalcula `PLRA`.
- O motor recebe `PLRA` final do contrato/camada patrimonial.
- Implementacao inicial pode calcular a partir de `I155 + referencial`.
- Ausencia de conferencia `J150` deve ser registrada como limitacao/pendencia de conferencia.
- Codigo referencial e metodologia versionada sao bases principais.
- Nome livre nao deve decidir classificação.
- Valores usam `Decimal`.

## 7. Decisoes Pendentes

Nao ha bloqueio para criar TASKs do Modulo 6 conforme esta SPEC.

Decisoes futuras:

- `J150` pode virar requisito para status final mais rigoroso se decisao metodologica futura aprovar.
- Laudo narrativo segue SPEC posterior.

## 8. Contratos

### 8.1 Entradas

Registros e fontes:

- `I050`;
- `I051`;
- `I150`;
- `I155`;
- contas referenciais de resultado;
- `J150`, quando parser suportar conferencia de DRE.

### 8.2 Assets ROA

Assets alvo:

- `tabela_metodologica_roa.csv`;
- `componentes_roa.csv`.

Colunas minimas da tabela metodologica:

- `codigo_referencial`;
- `modo_correspondencia`;
- `grupo_metodologico`;
- `macrogrupo`;
- `bloco_roa`;
- `sinal_natural`;
- `tratamento`;
- `regra_principal`;
- `componente_roa`;
- `exige_revisao`;
- `motivo_condicional`;
- `methodology_version_id`.

Tratamentos permitidos:

- `incluir_automaticamente`;
- `excluir_automaticamente`;
- `condicional`.

### 8.3 Blocos ROA

- `receita_bruta`;
- `deducoes_receita`;
- `tributos_receita`;
- `custos_operacionais`;
- `despesas_operacionais`;
- `resultado_financeiro`;
- `resultado_nao_operacional`;
- `pressoes_complementares_caixa`.

### 8.4 `RoaCalculation`

Campos minimos:

- `gross_revenue`;
- `deductions`;
- `revenue_taxes`;
- `net_operating_revenue`;
- `operating_costs`;
- `operating_expenses`;
- `financial_result`;
- `non_operating_result`;
- `cash_pressure_adjustments`;
- `roa_preliminary`;
- `roa_final`;
- `status`;
- `component_summaries`;
- `audit_rows`;
- `pending_groups`;
- `alerts`;
- `methodology_version_id`.

### 8.5 `RoaAuditRow`

Campos minimos:

- `account_code`;
- `account_name`;
- `reference_code`;
- `reference_description`;
- `roa_block`;
- `component_roa`;
- `base_value`;
- `signed_value`;
- `treatment`;
- `final_status`;
- `pending_reason`;
- `evidence_id`;
- `line_reference`.

### 8.6 Formula

```text
ROL = Receita Bruta - Deducoes - Tributos sobre Receita

ROA = ROL
    - Custos Operacionais
    - Despesas Operacionais
    +/- Resultado Financeiro
    +/- Resultado Nao Operacional

ROA Final = ROA - Pressoes Complementares de Caixa

CAPAG-E = ROA Final + PLRA
```

### 8.7 Regras De Sinal

- Receitas aumentam resultado.
- Deducoes reduzem resultado.
- Tributos sobre receita reduzem resultado.
- Custos reduzem resultado.
- Despesas reduzem resultado.
- Resultado financeiro depende da natureza e sinal.
- Resultado nao operacional depende da natureza e sinal.
- Pressoes complementares reduzem `ROA Final`.

### 8.8 Pressoes Complementares De Caixa

Itens minimos:

- fornecedores vencidos;
- parcelamentos;
- contingencias;
- divida fiscal;
- divida trabalhista;
- mutuos;
- intercompany.

Regras:

- Podem vir de contas patrimoniais.
- Devem ser segregadas do resultado operacional puro.
- Devem ter rastreabilidade.
- Quando materiais, devem exigir evidencia.
- Devem reduzir `ROA Final`.

### 8.9 Pendencias E Evidencias

Gerar pendencia quando:

- conta de resultado elegivel nao tiver regra ROA;
- conta condicional exigir revisao;
- despesa material precisar justificativa de pertinencia operacional;
- resultado financeiro ou nao operacional exigir reclassificacao;
- pressao complementar depender de evidencia.

Evidencias materiais:

- `method_component = ROA`;
- `adjustment_type = despesa_operacional_justificada` ou tipo coerente;
- `required_evidence_type` conforme macrogrupo.

O sistema nao deve permitir `ROA final` quando despesas ou pressoes materiais estiverem sem tratamento.

### 8.10 Integracao Com PLRA E CAPAG-E

Regras:

- Motor ROA nao recalcula `PLRA`.
- Motor recebe `PLRA` final.
- `CAPAG-E = ROA Final + PLRA`.
- Se `ROA` estiver final e `PLRA` bloqueado, `CAPAG-E` fica bloqueada por `PLRA`.
- Se `PLRA` estiver final e `ROA` bloqueado, `CAPAG-E` fica bloqueada por `ROA`.
- Metodo do contrato CAPAG-E: `roa_plra`.

### 8.11 API

Endpoints alvo:

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/roa/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/roa
POST /api/v1/analyses/{analysis_id}/exercises/{year}/roa/decisions
```

Payload deve incluir:

- resumo do ROA;
- componentes;
- auditoria;
- pendencias;
- status;
- valor de `CAPAG-E` por metodo `roa_plra`, quando disponivel.

Valores devem ser strings decimais.

### 8.12 Frontend

Rota alvo:

```text
/analises/:analysisId/exercicios/:year/roa
```

Tela de `ROA` deve conter:

- resumo por bloco;
- tabela de contas de resultado;
- pendencias de despesas/receitas condicionais;
- comparativo com `FCA`, quando existir;
- status de evidencias.

Frontend nao pode recalcular `ROA`, `PLRA` ou `CAPAG-E`.

### 8.13 Exportacao E Laudo

Abas de Excel:

- `roa_resumo`;
- `roa_auditoria`;
- `roa_pressoes_caixa`.

Laudo futuro deve apresentar:

- formula do `ROA`;
- blocos de receita/custo/despesa;
- pressoes complementares;
- justificativas de despesas materiais;
- valor final de `ROA`;
- combinacao com `PLRA`.

## 9. Responsabilidades Por Camada

### IO

Fornecer contas, saldos, vinculos referenciais e dados de conferencia `J150` quando disponiveis.

### Domain

Modelar `RoaCalculation`, `RoaAuditRow`, blocos, componentes, status e pendencias.

### Engine

Classificar contas, aplicar sinais, calcular ROA, aplicar pressoes e gerar auditoria.

### Application

Orquestrar execucao, evidencias, decisoes manuais, snapshots e integracao com contrato CAPAG-E.

### API

Expor ROA e serializar valores sem regra de negocio.

### Frontend

Exibir ROA, pendencias e evidencias sem recalculo.

### Export

Serializar ROA e auditoria sem recalcular.

## 10. Dados De Entrada E Saida

Entradas:

- ECD normalizada;
- contas referenciais;
- metodologia ROA;
- PLRA final;
- evidencias e decisoes manuais;
- dados `J150`, quando disponiveis.

Saidas:

- `RoaCalculation`;
- `RoaAuditRow`;
- `ROA Final`;
- status e pendencias;
- `CAPAG-E` por metodo `roa_plra`, quando possivel;
- payload API;
- tela ROA;
- abas Excel.

## 11. Estados E Erros Relevantes

Erros e bloqueios:

- conta elegivel sem regra ROA;
- conta condicional sem decisao;
- despesa material sem evidencia;
- pressao complementar sem evidencia;
- ausencia de `PLRA` final;
- ausencia de conferencia `J150`, como limitacao quando aplicavel;
- tentativa de recalcular no frontend/exportacao;
- uso de `float`.

## 12. Criterios De Aceite

- `ROA` calcula `ROL`.
- `ROA` calcula custos e despesas.
- Resultado financeiro aplica sinal correto.
- Resultado nao operacional aplica sinal correto.
- Pressoes complementares reduzem `ROA Final`.
- Conta elegivel sem regra bloqueia ou gera pendencia.
- Despesa condicional material gera pendencia.
- `ROA + PLRA` integra com contrato CAPAG-E.
- `CAPAG-E` nao e calculada sem `PLRA`.
- `ROA` e auditavel por conta referencial.
- Frontend e Excel nao recalculam.

## 13. Estrategia De Validacao Esperada

Testes obrigatorios:

- calcular ROL com receita, deducoes e tributos;
- calcular ROA com custos e despesas;
- aplicar resultado financeiro com sinal correto;
- aplicar resultado nao operacional com sinal correto;
- aplicar pressoes complementares;
- bloquear ROA por conta sem regra;
- gerar pendencia para despesa condicional material;
- combinar `ROA + PLRA`;
- impedir `CAPAG-E` sem `PLRA`;
- registrar ausencia de `J150` como limitacao;
- validar API e exportacao.

## 14. Riscos E Mitigacoes

- Risco: misturar pressoes patrimoniais com despesa operacional.
  Mitigacao: bloco separado de pressoes complementares.

- Risco: sinal contabil inverter resultado.
  Mitigacao: regras de sinal e testes por componente.

- Risco: calcular CAPAG-E sem PLRA final.
  Mitigacao: bloqueio pelo contrato CAPAG-E.

- Risco: ausencia de J150 ocultar limitacao.
  Mitigacao: registrar limitacao/pendencia de conferencia.

- Risco: frontend recalcular ROA.
  Mitigacao: API retorna valores, status e auditoria prontos.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs do Modulo 6 conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- recalcular `PLRA` dentro do motor ROA;
- calcular `CAPAG-E` sem `PLRA`;
- misturar pressoes complementares com despesa operacional sem rastreabilidade;
- tratar conta sem regra como incluída automaticamente;
- usar `float`.
