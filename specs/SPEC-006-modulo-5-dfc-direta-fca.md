# SPEC-006 - Modulo 5: DFC Direta Completa E FCA

## 1. Objetivo Tecnico

Especificar a evolucao do `FCO` atual para uma `DFC` direta completa capaz de apurar `FCA`, separando fluxos operacionais, de investimento e de financiamento, com auditoria por lancamento, pendencias, evidencias e status final ou parcial.

## 2. Contexto E Problema

O PRD exige evoluir o `FCO` atual para uma DFC direta completa e impedir que `FCO` seja confundido com `FCA`. A arquitetura define motor `dfc`, entidade de snapshots/auditoria e contrato CAPAG-E que consome `FCA` final ou parcial.

O problema central e que o `FCO` atual cobre apenas fluxo operacional. Para `CAPAG-E = PLRA + FCA`, o sistema precisa reconstruir, a partir da ECD, fluxos operacionais, de investimento e financiamento, registrar pendencias e calcular um `FCA` auditavel.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`

Fontes de referencia autorizadas pelo usuario:

- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/01-matriz-cobertura-spec-09.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/02-entrada-ecd-lancamentos-caixa.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/03-metodologia-dfc-componentes.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/04-motor-dfc-direto-fca.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/05-integracao-fco-atual.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/06-pendencias-evidencias-dfc.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/07-api-frontend-exportacao-dfc.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/08-testes-dfc-fca.md`
- `docs/reference/planejamento-modulos/modulo-05-dfc-direto-fca/09-roadmap-execucao-modulo-5.md`

Fontes frontend governadas:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## 4. Escopo

Esta SPEC cobre:

- registros ECD usados pela DFC direta;
- identificacao de contas de disponibilidades;
- classificacao de fluxos com caixa;
- atividades DFC;
- componentes DFC;
- entidade `DfcCalculation`;
- entidade `DfcAuditRow`;
- formula de `FCA`;
- compatibilidade com `FCO` atual;
- pendencias e evidencias;
- API, frontend e exportacao;
- testes obrigatorios.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- motor `ROA`;
- laudo textual completo;
- upload de DFC externa;
- classificacao por nome livre como criterio principal;
- recalculo no frontend, Excel ou laudo;
- definir contrato CAPAG-E alem do consumo da SPEC-004.

## 6. Decisoes Ja Aprovadas

- `FCO` atual vira componente operacional.
- `FCO` nao e `FCA` completo.
- Enquanto so houver operacional, status deve ser `FCA parcial`.
- DFC direta deve separar atividades operacional, investimento e financiamento.
- Entram apenas fluxos financeiros efetivos com contrapartida em disponibilidades.
- Lancamento sem caixa nao entra na DFC.
- Codigo referencial e base principal de classificacao.
- Nome livre da conta nao e criterio principal.
- Movimentos nao classificados nao entram no `FCA` final sem decisao manual.
- `FCA = operacional + investimento + financiamento + ajustes manuais validados`.
- Valores usam `Decimal`.

## 7. Decisoes Pendentes

Nao ha bloqueio para criar TASKs do Modulo 5 conforme esta SPEC.

Dependencias externas:

- Evidencias materiais seguem a SPEC-005.
- O contrato CAPAG-E segue a SPEC-004.
- Laudo final segue SPEC posterior.

## 8. Contratos

### 8.1 Entradas ECD

Registros usados:

- `I200`;
- `I250`;
- vinculo `I250 -> I050 -> I051`;
- identificacao de contas de disponibilidades.

Regras:

- Entram apenas fluxos financeiros efetivos.
- Deve existir contrapartida em disponibilidades.
- Lancamento sem caixa nao entra na DFC.
- Nome livre nao decide classificacao.
- Codigo referencial e base principal da classificacao.

### 8.2 Atividades DFC

- `operacional`;
- `investimento`;
- `financiamento`;
- `nao_classificado`.

### 8.3 Componentes Minimos

Operacional:

- recebimentos de clientes;
- pagamentos a fornecedores;
- pagamentos a empregados;
- tributos operacionais;
- outros fluxos operacionais recorrentes.

Investimento:

- compra de imobilizado;
- venda de imobilizado;
- aquisicao de participacoes;
- venda de participacoes;
- aplicacoes/resgates nao equivalentes a caixa.

Financiamento:

- captacao de emprestimos;
- amortizacao de principal;
- juros classificados como financiamento;
- aumento/reducao de capital;
- distribuicao de lucros/dividendos.

### 8.4 `DfcCalculation`

Campos minimos:

- `automatic_value`;
- `operational_flow`;
- `investment_flow`;
- `financing_flow`;
- `manual_adjustments_value`;
- `fca_value`;
- `status`;
- `component_summaries`;
- `audit_rows`;
- `alerts`;
- `methodology_version_id`.

### 8.5 `DfcAuditRow`

Campos minimos:

- `entry_number`;
- `entry_date`;
- `cash_account_code`;
- `cash_flow_direction`;
- `counterparty_account_code`;
- `counterparty_account_name`;
- `counterparty_reference_code`;
- `dfc_activity`;
- `dfc_component_code`;
- `dfc_component_label`;
- `included_value`;
- `final_status`;
- `pending_reason`;
- `history`;
- `line_number`.

### 8.6 Formula

```text
Fluxo Operacional = entradas operacionais - saidas operacionais
Fluxo de Investimento = entradas de investimento - saidas de investimento
Fluxo de Financiamento = entradas de financiamento - saidas de financiamento
FCA = Fluxo Operacional + Fluxo de Investimento + Fluxo de Financiamento + ajustes manuais validados
```

### 8.7 Status

Status de `FCA`:

- `nao_calculado`;
- `parcial`;
- `calculado`;
- `bloqueado_por_pendencia`;
- `bloqueado_por_evidencia`;
- `erro_metodologico`.

Status de linha:

- `incluido`;
- `excluido`;
- `nao_classificado`;
- `fluxo_incompativel`;
- `pendente_evidencia`;
- `decisao_manual_aplicada`.

### 8.8 Pendencias

Gerar pendencia quando:

- contrapartida nao possui codigo referencial;
- codigo referencial nao possui regra DFC;
- fluxo tem direcao incompativel;
- componente exige revisao;
- movimento e material e nao possui evidencia.

Movimentos nao classificados ficam visiveis, auditaveis e bloqueiam resultado final quando relevantes.

### 8.9 Integracao Com Evidencias

Movimento material deve criar ou exigir evidencia com:

- `scope_type = fco_movement` ou `dfc_component`;
- `method_component = FCA`;
- `adjustment_type = fluxo_excluido` ou `fluxo_incluido`;
- evidencia conforme natureza do fluxo.

### 8.10 API

Endpoints alvo:

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/dfc/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/dfc
POST /api/v1/analyses/{analysis_id}/exercises/{year}/dfc/decisions
```

Payload deve conter:

- resumo por atividade;
- componentes;
- linhas de auditoria;
- pendencias;
- valor `FCA`;
- status `FCA`;
- limitacoes.

Valores monetarios devem ser strings decimais.

### 8.11 Frontend

Rota alvo:

```text
/analises/:analysisId/exercicios/:year/dfc
```

Tela de `DFC direta` deve conter:

- resumo por atividade;
- tabela de movimentos;
- filtros por atividade;
- filtros por status;
- pendencias;
- fluxos nao classificados;
- resumo `FCA`;
- acoes de decisao manual quando permitido.

Frontend nao pode recalcular `FCA`.

### 8.12 Exportacao E Laudo

Abas de Excel:

- `dfc_resumo`;
- `dfc_auditoria`.

Laudo futuro deve informar:

- DFC reconstruida por metodo direto;
- separacao operacional, investimento e financiamento;
- movimentos nao classificados;
- status final ou parcial do `FCA`.

## 9. Responsabilidades Por Camada

### IO

Fornecer lancamentos, partidas, contas, vinculos referenciais e linhas originais.

### Domain

Modelar `DfcCalculation`, `DfcAuditRow`, atividades, componentes, pendencias e status.

### Engine

Identificar fluxos com caixa, determinar direcao, classificar contrapartidas, calcular componentes e `FCA`.

### Application

Orquestrar execucao, decisoes manuais, evidencias, snapshots e integracao com contrato CAPAG-E.

### API

Expor DFC/FCA e serializar valores sem regra de negocio.

### Frontend

Exibir DFC, pendencias e decisoes sem recalculo.

### Export

Serializar resumo e auditoria da DFC sem recalcular.

## 10. Dados De Entrada E Saida

Entradas:

- ECD normalizada;
- contas de disponibilidades;
- plano referencial;
- metodologia DFC;
- evidencias materiais;
- decisoes manuais validadas.

Saidas:

- `DfcCalculation`;
- `DfcAuditRow`;
- fluxo operacional;
- fluxo de investimento;
- fluxo de financiamento;
- `FCA`;
- status e pendencias;
- payload API;
- tela DFC;
- abas Excel.

## 11. Estados E Erros Relevantes

Erros e bloqueios:

- conta de caixa nao identificada;
- contrapartida sem codigo referencial;
- regra DFC ausente;
- fluxo incompativel com direcao esperada;
- movimento material sem evidencia;
- decisao manual sem justificativa;
- tentativa de chamar `FCO` de `FCA` final;
- tentativa de somar movimento nao classificado no `FCA` final;
- tentativa de usar `float`.

## 12. Criterios De Aceite

- DFC distingue operacional, investimento e financiamento.
- `FCO` permanece componente operacional.
- Apenas lancamentos com caixa entram na DFC.
- Lancamento sem caixa e ignorado.
- Fluxos sao classificados por codigo referencial.
- Fluxos sem regra viram `nao_classificado`.
- Fluxos nao classificados nao entram no `FCA` final sem decisao manual.
- `FCA` e soma auditavel das tres atividades mais ajustes validados.
- Status `FCA parcial` e usado quando so houver operacional.
- API expõe `FCA` e status.
- Frontend nao recalcula `FCA`.
- Excel possui `dfc_resumo` e `dfc_auditoria`.

## 13. Estrategia De Validacao Esperada

Testes obrigatorios:

- classificar fluxo operacional atual como operacional;
- classificar compra de imobilizado como investimento;
- classificar captacao/amortizacao de emprestimo como financiamento;
- ignorar lancamento sem caixa;
- registrar pendencia para regra ausente;
- registrar fluxo incompativel;
- calcular `FCA` como soma das tres atividades;
- preservar compatibilidade com `FCO`;
- impedir `FCO` como `FCA` final;
- impedir soma de fluxo nao classificado no `FCA` final;
- validar payload API;
- validar exportacao `dfc_resumo` e `dfc_auditoria`.

## 14. Riscos E Mitigacoes

- Risco: `FCO` ser apresentado como `FCA`.
  Mitigacao: status parcial obrigatorio e testes.

- Risco: movimento nao classificado contaminar `FCA`.
  Mitigacao: pendencias auditaveis e bloqueio de resultado final.

- Risco: classificacao por nome livre.
  Mitigacao: codigo referencial como base principal.

- Risco: frontend recalcular DFC.
  Mitigacao: API entrega componentes e status prontos.

- Risco: evidencias materiais ficarem fora do fluxo.
  Mitigacao: integracao obrigatoria com `AdjustmentEvidence`.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs do Modulo 5 conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- tratar `FCO` como `FCA` completo;
- incluir fluxo nao classificado no `FCA` final sem decisao manual;
- classificar DFC por nome livre como criterio principal;
- recalcular `FCA` no frontend, Excel ou laudo;
- usar `float` em valores financeiros.
