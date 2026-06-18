# SPEC-004 - Modulo 3: Contrato CAPAG-E, PLRA, FCA E ROA

## 1. Objetivo Tecnico

Definir o contrato canonico de resultado da `CAPAG-E`, padronizando nomes, metodos, formulas, status, bloqueios, serializacao, frontend, exportacao e validacoes.

Esta SPEC estabelece a linguagem comum para `PLRA`, `FCA`, `ROA` e `CAPAG-E`, impedindo que `FCO` seja apresentado como `FCA` completo e que resultados parciais sejam exibidos como finais.

## 2. Contexto E Problema

O PRD exige que todo resultado CAPAG-E informe metodo, formula, valor, status, limitacoes e bloqueios. A arquitetura define um motor `capag` que combina componentes calculados por outros motores, persiste snapshots e fornece contrato unico para API, frontend, Excel e laudo.

O sistema atual usa linguagem como `PLR ajustado`, `FCO` e `CAPAG-e`. Essa linguagem precisa ser compatibilizada com laudo e metodologia futura:

- `PLR ajustado` deve equivaler a `PLRA` para fins de laudo e contratos externos.
- `FCO` e apenas fluxo operacional, nao `FCA` completo.
- `FCA` pode ser final ou parcial, sempre com status.
- `ROA` e caminho alternativo para composicao de `CAPAG-E`.
- `CAPAG-E` nao pode ser final sem metodo definido e componentes suficientes.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`

Fontes de referencia autorizadas pelo usuario:

- `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/01-matriz-cobertura-spec-06.md`
- `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/02-contrato-dominio-capag-e.md`
- `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/03-status-bloqueios-metodos.md`
- `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/04-api-exportacao-ui-contrato.md`
- `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/05-testes-contrato-capag-e.md`
- `docs/reference/planejamento-modulos/modulo-03-contrato-capag-e-plra-fca-roa/06-roadmap-execucao-modulo-3.md`

Fontes frontend governadas:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## 4. Escopo

Esta SPEC cobre:

- definicoes canonicas de `PLRA`, `FCO`, `FCA`, `ROA` e `CAPAG-E`;
- mapeamento entre nomes atuais e nomes canonicos;
- entidade de dominio `CapagEAssessment`;
- metodos permitidos;
- status de componentes;
- regras de formula;
- bloqueios minimos;
- resultado parcial;
- API;
- frontend;
- exportacao Excel;
- testes de contrato.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- implementar DFC direta completa;
- implementar `FCA` final;
- implementar motor `ROA`;
- gerar laudo textual completo;
- definir evidencias, materialidade e ativos;
- administrar metodologia pela UI;
- recalcular PLRA, FCA, ROA ou CAPAG-E em frontend, Excel ou laudo.

## 6. Decisoes Ja Aprovadas

- `PLR ajustado` equivale a `PLRA` para fins de laudo e contratos externos.
- `PLR bruto` permanece tecnico e interno.
- `PLR ajustado` pode aparecer em tela tecnica, mas `PLRA` deve ser usado em contrato canonico.
- `FCO` nao e sinonimo de `FCA`.
- Enquanto so houver `FCO`, o sistema deve rotular como `FCA parcial`.
- `FCA` representa fluxo de caixa ajustado completo ou parcial, sempre com status.
- `ROA` representa resultado operacional ajustado.
- `CAPAG-E` deve sempre informar metodo.
- Todo resultado deve carregar valor, status, formula, limitacoes e bloqueios.
- Valores monetarios usam `Decimal`.
- Valores finais devem ser quantizados em `0.01`.
- Percentuais devem ser fracao `Decimal`.
- O contrato nao aceita `float`.

## 7. Decisoes Pendentes

Nao ha bloqueio para criar TASKs do contrato CAPAG-E conforme esta SPEC.

Decisoes de outros modulos:

- O Modulo 4 definira quando evidencia critica bloqueia ou gera ressalva.
- O Modulo 5 definira o calculo completo de `FCA`.
- O Modulo 6 definira o calculo de `ROA`.
- O Modulo 7 definira como o laudo consome o contrato.

Enquanto esses modulos nao existirem, o contrato deve aceitar componentes parciais, bloqueados ou nao calculados sem esconder limitacoes.

## 8. Contratos

### 8.1 Entidade `CapagEAssessment`

Campos minimos:

- `exercise_year`;
- `method`;
- `plra_value`;
- `plra_status`;
- `fca_value`;
- `fca_status`;
- `roa_value`;
- `roa_status`;
- `capag_e_value`;
- `capag_e_status`;
- `unavailable_reason`;
- `calculation_basis`;
- `methodology_formula`;
- `warnings`;
- `limitations`;
- `blocking_issues`;
- `methodology_version_id`.

### 8.2 Metodos Permitidos

- `fca_plra`;
- `roa_plra`;
- `comparativo_fca_roa`;
- `nao_definido`.

### 8.3 Status De Componente

Valores permitidos:

- `nao_calculado`;
- `calculado`;
- `parcial`;
- `bloqueado_por_pendencia`;
- `bloqueado_por_evidencia`;
- `erro_metodologico`.

### 8.4 Status De CAPAG-E

Valores permitidos:

- `nao_calculado`;
- `parcial`;
- `calculado`;
- `bloqueado`;
- `indisponivel`;
- `erro_metodologico`.

### 8.5 Regras De Formula

- `CAPAG-E` so pode ser calculada quando `PLRA` final estiver disponivel.
- `CAPAG-E = PLRA + FCA` so pode ser final com `FCA` final.
- `CAPAG-E = PLRA + ROA` so pode ser final com `ROA` final.
- Metodo `comparativo_fca_roa` deve preservar os dois caminhos e explicitar divergencias.
- Metodo `nao_definido` bloqueia resultado final.
- Se houver apenas `FCO`, o componente deve ser tratado como `FCA parcial`.
- Se houver pendencia metodologica em ativos/passivos, `PLRA` final fica bloqueada.
- Se houver evidencia critica pendente, o componente afetado fica bloqueado ou com ressalva conforme SPEC do Modulo 4.
- Valores intermediarios devem ser preservados mesmo quando resultado final estiver bloqueado.

### 8.6 Bloqueios Minimos

- Sem `PLRA`: bloqueia qualquer `CAPAG-E`.
- Sem metodo: bloqueia laudo final.
- Sem `FCA` final no metodo `fca_plra`: bloqueia resultado final.
- Sem `ROA` final no metodo `roa_plra`: bloqueia resultado final.
- Evidencia critica pendente: bloqueia ou gera ressalva conforme Modulo 4.
- Pendencia metodologica bloqueante: bloqueia componente afetado.
- Tentativa de usar `float`: erro de contrato.

### 8.7 Resultado Parcial

Resultado parcial pode ser exibido quando:

- status estiver explicito;
- limitacao estiver descrita;
- frontend nao apresentar como final;
- exportacao registrar restricao;
- laudo futuro puder consumir o status sem inferir regra.

### 8.8 API

Endpoints alvo:

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

Valores monetarios devem ser strings decimais.

### 8.9 Frontend

Rotas relacionadas:

```text
/analises/:analysisId/exercicios/:year/resultado
/analises/:analysisId/laudo
```

A UI deve:

- mostrar `PLRA` em contexto de laudo/resultado canonico;
- manter `PLR ajustado` apenas em contexto tecnico;
- indicar metodo usado;
- diferenciar `FCO`, `FCA parcial` e `FCA final`;
- exibir bloqueios, limitacoes e warnings;
- evitar linguagem como `CAPAG final` quando status for parcial, bloqueado ou indisponivel;
- usar badges e estados visuais governados;
- usar `.tnum` em valores, percentuais e formulas numericas.

Frontend nao pode recalcular `CAPAG-E`.

### 8.10 Exportacao

Criar bloco ou aba:

- `contrato_capag_e`

Campos minimos:

- exercicio;
- metodo;
- formula;
- `PLRA`;
- status do `PLRA`;
- `FCA`;
- status do `FCA`;
- `ROA`;
- status do `ROA`;
- `CAPAG-E`;
- status final;
- limitacoes metodologicas;
- warnings;
- bloqueios;
- versao metodologica.

Exportacao nao pode recalcular resultado.

## 9. Responsabilidades Por Camada

### Domain

Definir `CapagEAssessment`, metodos, status, invariantes numericas e bloqueios.

### Engine

Combinar componentes recebidos, aplicar metodo, preservar valores intermediarios e definir status final.

### Application

Orquestrar execucao do contrato, carregar snapshots de componentes, persistir assessment e invalidar dependentes quando necessario.

### API

Validar request, serializar contrato canonico e converter erros de dominio.

### Frontend

Exibir metodo, formula, valores, status, limitacoes e bloqueios sem recalculo.

### Export

Serializar `CapagEAssessment` no Excel sem recalculo.

### Report

Consumir `CapagEAssessment` futuramente, sem chamar motores.

## 10. Dados De Entrada E Saida

Entradas:

- `PLRA` final, parcial ou bloqueada;
- `FCA` final, parcial, bloqueada ou nao calculada;
- `ROA` final, parcial, bloqueado ou nao calculado;
- metodo solicitado;
- evidencias, limitacoes e bloqueios conhecidos;
- versao metodologica.

Saidas:

- `CapagEAssessment`;
- payload API canonico;
- bloco frontend de resultado;
- bloco/aba Excel `contrato_capag_e`;
- status consumivel pelo laudo futuro.

## 11. Estados E Erros Relevantes

Estados seguem os status de componente e CAPAG-E definidos nesta SPEC.

Erros:

- metodo invalido;
- status invalido;
- `CAPAG-E` final sem `PLRA`;
- `fca_plra` final sem `FCA` final;
- `roa_plra` final sem `ROA` final;
- `FCO` exibido como `FCA` final;
- valor monetario como `float`;
- frontend/exportacao/laudo tentando recalcular.

## 12. Criterios De Aceite

- Existe contrato unico `CapagEAssessment`.
- `plr_ajustado` e mapeado para `PLRA`.
- `FCO` nunca aparece como `FCA` final.
- `FCA parcial` e exibido quando so houver `FCO`.
- Metodos permitidos estao fechados.
- Status permitidos estao fechados.
- `CAPAG-E` sem `PLRA` fica bloqueada.
- Metodo `fca_plra` sem `FCA` final nao gera resultado final.
- Metodo `roa_plra` sem `ROA` final nao gera resultado final.
- Valores intermediarios aparecem mesmo quando resultado final esta bloqueado.
- API serializa valores monetarios como string decimal.
- Frontend exibe metodo e status sem recalcular.
- Excel serializa `contrato_capag_e` sem recalcular.

## 13. Estrategia De Validacao Esperada

Testes obrigatorios:

- mapear `plr_ajustado` para `PLRA`;
- bloquear `CAPAG-E` sem `PLRA`;
- bloquear `FCA + PLRA` sem `FCA`;
- bloquear `ROA + PLRA` sem `ROA`;
- identificar `FCA parcial` quando so houver `FCO`;
- serializar formula selecionada;
- garantir uso exclusivo de `Decimal`;
- validar status permitidos;
- validar metodos permitidos;
- validar payload canonico;
- validar bloco/aba `contrato_capag_e`;
- validar que exportacao nao recalcula;
- validar que frontend nao mostra parcial como final.

## 14. Riscos E Mitigacoes

- Risco: usuario interpretar `FCO` como `FCA` completo.
  Mitigacao: status `parcial`, linguagem canônica e teste obrigatório.

- Risco: modulos futuros redefinirem nomes e formulas.
  Mitigacao: contrato unico de dominio consumido por API, frontend, exportacao e laudo.

- Risco: resultado final ser exibido sem status.
  Mitigacao: status obrigatorio em payload, UI e Excel.

- Risco: evidencia futura bloquear componente sem refletir no contrato.
  Mitigacao: campos `limitations`, `warnings` e `blocking_issues`.

- Risco: divergencia por arredondamento ou tipo numerico.
  Mitigacao: `Decimal`, quantizacao final em `0.01` e proibicao de `float`.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs do contrato CAPAG-E conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- implementar DFC/FCA completo sem SPEC do Modulo 5;
- implementar ROA sem SPEC do Modulo 6;
- gerar laudo final sem SPEC do Modulo 7;
- tratar `FCO` como `FCA` final;
- apresentar `CAPAG-E` final sem metodo, status e componentes suficientes.
