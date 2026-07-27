# SPEC-011 - Modulo 1B: Motor PLRA

## 1. Objetivo Tecnico

Especificar o motor auditavel de Patrimonio Liquido Realizavel Ajustado (`PLRA`), transformando saldos patrimoniais declarados na ECD em `PLR bruto` e `PLRA`, com metodologia versionada, desagios prudenciais, pendencias, memoria por conta e integracao com evidencias e com o contrato `CAPAG-E`.

## 2. Contexto E Problema

O PRD exige que o sistema consolide `PLRA` antes de calcular `CAPAG-E`. A arquitetura reserva um motor `plra`, mas a SPEC-002 e as TASKs da camada declarada implementaram apenas classificacao e resultado por conta. Nao existe hoje um contrato governado que consolide esses resultados em um componente patrimonial final.

O manual interno aprovado pelo usuario em 24/07/2026 define a formula, as fontes ECD, os grupos prudenciais e faixas de desagio. O usuario aprovou o uso automatico do limite superior dessas faixas como politica default conservadora, sem bloquear o calculo apenas pela ausencia de avaliacao individual. Avaliacao validada ou valor de liquidacao forcada pode substituir o default conforme SPEC-005.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`

Fonte metodologica interna autorizada e aprovada pelo usuario:

- `docs/reference/manual-plr-capag-ecd-pgfn-v2.md`

Fontes publicas oficiais consultadas:

- Portaria PGFN n. 6.757/2022, texto consolidado:
  `https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/125274`
- Orientacao oficial para revisao da capacidade de pagamento:
  `https://www.gov.br/pgfn/pt-br/servicos/orientacoes-contribuintes/pedir-revisao-de-capacidade-de-pagamento-para-fins-de-negociacao-perante-a-fazenda-nacional`

As fontes oficiais sustentam o uso de informacoes patrimoniais, metodologia documentada e valor de liquidacao forcada, mas nao definem percentuais fixos de desagio. Os percentuais desta SPEC sao politica metodologica interna do CAPAG, nao formula oficial publicada pela PGFN.

## 4. Escopo

Esta SPEC cobre:

- formula de `PLR bruto` e `PLRA`;
- selecao de saldos patrimoniais anuais da ECD;
- hierarquia e eliminacao de dupla contagem;
- metodologia exata por `COD_CTA_REF`;
- grupos de ativos e passivos;
- politica default versionada de desagios;
- exclusoes automaticas aprovadas;
- contas condicionais e revisao humana;
- memoria de calculo e auditoria por conta;
- estados, limitacoes, pendencias e bloqueios;
- persistencia de snapshots;
- API, frontend e Excel sem recalculo fora do backend;
- integracao com avaliacao de ativos, evidencias e contrato `CAPAG-E`.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- calcular `FCA` ou `ROA`;
- substituir avaliacao profissional de bens;
- produzir laudo ABNT NBR 14.653;
- inferir `COD_CTA_REF` ausente;
- classificar por nome livre como criterio decisorio;
- administrar livremente metodologia critica pela UI;
- recalcular `PLRA` no frontend, Excel ou laudo;
- criar formula oficial da PGFN ou atribuir esse status a politica interna;
- implementar upload persistente de documentos.

## 6. Decisoes Ja Aprovadas

- `PLR ajustado` equivale a `PLRA` no contrato canonico.
- `PLR bruto` permanece resultado tecnico intermediario.
- Formula-base: `PLR = Ativos Realizaveis - Passivos Economicos Exigiveis`.
- Formula final: `PLRA = Ativos Realizaveis Ajustados - Passivos Economicos Exigiveis`.
- O motor usa saldos finais anuais do `I155`, vinculados a `I050` e `I051`.
- O `J100` serve somente para conferencia, consistencia e auditoria.
- O motor nao soma simultaneamente conta pai e conta filha.
- Apenas codigo referencial exato e regra metodologica ativa podem classificar automaticamente.
- Conta sem `I051` permanece fora do calculo automatico e na auditoria, sem inferencia.
- A existencia de conta sem `I051`, isoladamente, nao cria novo bloqueio automatico.
- Regra metodologica ausente, bloqueada ou insegura nao pode ser substituida por prefixo amplo.
- Desagio default e aplicado automaticamente e nao bloqueia `PLRA` apenas por ser default.
- O limite superior da faixa aprovada e o default inicial conservador.
- Valor de liquidacao forcada validado prevalece sobre o default.
- Valor manual exige justificativa e evidencia conforme SPEC-005.
- Passivo condicional exige decisao humana antes de compor resultado final.
- Valores monetarios usam `Decimal`, rejeitam `float` e sao quantizados em `0.01`.
- Percentuais usam fracao `Decimal`, entre `0` e `1`.
- Toda execucao preserva `methodology_version_id`.

## 7. Decisoes Pendentes

Nao ha decisao essencial pendente para criar TASKs desta SPEC.

A cobertura completa de codigos depende do plano referencial oficial e da metodologia interna versionada. Codigo nao coberto deve permanecer auditavel e nao pode ser inferido.

## 8. Contratos

### 8.1 Entradas ECD

Entradas obrigatorias:

- `I050`: conta, tipo, nivel e hierarquia;
- `I051`: vinculo declaratorio exato com `COD_CTA_REF`;
- `I150`: periodo anual encerrado;
- `I155`: saldo final e indicador de natureza;
- `J100`: conferencia, sem uso como fonte primaria.

O exercicio deve usar o periodo anual encerrado em `31/12`. Periodos mensais, trimestrais ou intermediarios nao podem ser somados.

### 8.2 Elegibilidade E Hierarquia

- Contas analiticas validas tem prioridade.
- Conta sintetica nao entra quando conta descendente com saldo representar sua composicao.
- Conta pai e filha nunca sao somadas conjuntamente.
- Saldo e sinal devem ser obtidos dos campos normalizados da ECD.
- Conta sem vinculo referencial exato nao entra automaticamente.
- Conta de resultado nao deve ser convertida em conta patrimonial pelo motor.

### 8.3 Politica Default De Desagios

| Grupo | Desagio default | Origem aprovada |
| --- | ---: | --- |
| `caixa` | `0.00` | faixa `0%` |
| `bancos` | `0.00` | faixa `0%` |
| `aplicacoes_imediatas` | `0.05` | limite superior de `0% a 5%` |
| `clientes` | `0.30` | limite superior de `10% a 30%` |
| `adiantamentos` | `0.50` | limite superior de `20% a 50%` |
| `estoques` | `0.80` | limite superior de `20% a 80%` |
| `imobilizado` | `0.80` | limite superior de `40% a 80%` |
| `intangivel` | `1.00` | limite superior de `80% a 100%` |
| `creditos_judiciais` | `0.90` | limite superior de `30% a 90%` |

Formula do valor economico default:

```text
valor_economico_default = valor_contabil * (1 - desagio_default)
```

Regras:

- Percentual deve estar versionado.
- Default aplicado deve aparecer na auditoria.
- Alteracao do default cria nova versao metodologica e nao retroage snapshots.
- Avaliacao validada substitui o default apenas para o escopo avaliado.
- Override manual nao validado nao substitui o default.

### 8.4 Exclusoes Automaticas

Categorias excluidas por default:

- tributos a recuperar;
- IRPJ diferido;
- CSLL diferida;
- depositos judiciais;
- intangivel e goodwill;
- despesas antecipadas;
- prejuizo fiscal e base negativa;
- ativo classificado como sem realizabilidade economica.

A exclusao deve produzir audit row com valor contabil, regra, motivo e valor economico zero. Exclusao metodologica explicita nao e, por si so, pendencia.

### 8.5 Passivos

Categorias incluidas automaticamente como passivos economicos exigiveis:

- emprestimos;
- financiamentos;
- debentures;
- fornecedores;
- prestadores;
- salarios;
- INSS;
- FGTS;
- parcelamentos;
- contingencias provaveis;
- arrendamentos financeiros.

Categorias condicionais:

- partes relacionadas;
- mutuos com socios;
- receitas antecipadas;
- provisoes gerenciais;
- derivativos;
- multas;
- passivos sem exigibilidade comprovada.

Categoria condicional sem decisao valida permanece na auditoria e impede `PLRA` final quando tiver saldo nao zero.

### 8.6 `PlraAccountAuditRow`

Campos minimos:

- `account_code`;
- `account_name`;
- `account_type`;
- `account_level`;
- `parent_account_code`;
- `declared_reference_code`;
- `official_description`;
- `methodology_rule_id`;
- `methodology_group`;
- `macrogroup`;
- `base_value`;
- `sign`;
- `inclusion_status`;
- `default_discount_percent`;
- `default_economic_value`;
- `valuation_source`;
- `validated_valuation_value`;
- `final_economic_value`;
- `decision_status`;
- `evidence_status`;
- `reason`;
- `limitations`;
- `methodology_version_id`.

### 8.7 `PlraCalculation`

Campos minimos:

- `analysis_id`;
- `exercise_year`;
- `gross_assets_value`;
- `gross_economic_liabilities_value`;
- `adjusted_assets_value`;
- `plr_gross_value`;
- `plra_value`;
- `plra_status`;
- `calculation_formula`;
- `account_rows`;
- `pending_accounts`;
- `warnings`;
- `limitations`;
- `blocking_issues`;
- `j100_reconciliation_status`;
- `methodology_version_id`;
- `calculated_at`.

Formulas:

```text
PLR bruto = ativos incluidos antes dos desagios - passivos economicos exigiveis
PLRA = ativos com valor economico final - passivos economicos exigiveis
```

### 8.8 Estados

Usar os estados canonicos de componente:

- `nao_calculado`;
- `calculado`;
- `parcial`;
- `bloqueado_por_pendencia`;
- `bloqueado_por_evidencia`;
- `erro_metodologico`.

Regras:

- Default aprovado permite status `calculado`.
- Conta condicional nao resolvida com saldo nao zero bloqueia por pendencia.
- Evidencia critica pendente ou rejeitada bloqueia por evidencia conforme SPEC-005.
- Cobertura incompleta conhecida deve produzir `parcial`, limitacao ou bloqueio conforme impacto metodologico identificado, sem inferencia.
- Erro de asset, duplicidade de regra ou uso de `float` gera erro metodologico.
- Valores intermediarios permanecem disponiveis mesmo quando o status nao for final.

### 8.9 Algoritmo

1. Carregar ECD normalizada, exercicio e versao metodologica.
2. Selecionar o saldo final anual aplicavel.
3. Resolver hierarquia sem somar pai e filha.
4. Vincular conta a `COD_CTA_REF` exato declarado.
5. Validar codigo no plano referencial oficial.
6. Aplicar regra PLRA exata, ativa e versionada.
7. Registrar exclusoes e pendencias sem inferencia.
8. Calcular `PLR bruto`.
9. Aplicar desagio default aos ativos incluidos.
10. Substituir default por avaliacao validada quando existir.
11. Consolidar passivos economicos exigiveis.
12. Calcular `PLRA`.
13. Aplicar bloqueios de pendencia/evidencia.
14. Reconciliar com `J100` apenas como controle.
15. Persistir snapshot atomico e auditoria.
16. Invalidar `CapagEAssessment` dependente quando o snapshot mudar.

### 8.10 Integracao Com Evidencias E Avaliacao

- SPEC-005 governa materialidade, justificativas, evidencias e avaliacao de ativos.
- `AssetValuationAssessment.final_economic_value` validado prevalece sobre default.
- Ativo essencial nao e excluido automaticamente sem justificativa.
- Evidencia explica, sustenta, bloqueia ou ressalva; nao recalcula por si so.
- Alteracao validada invalida snapshot PLRA e assessment CAPAG-E dependentes.

### 8.11 Integracao Com CAPAG-E

- O contrato CAPAG-E recebe `plra_value`, `plra_status`, limitacoes e bloqueios do snapshot PLRA.
- API ou frontend nao pode informar `plra_status=calculado` sem snapshot calculado.
- `CAPAG-E` permanece bloqueada quando `PLRA` nao estiver final.
- `PLRA` nao calcula `FCA`, `ROA` ou `CAPAG-E`.

### 8.12 API

Endpoints alvo:

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/plra/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/plra
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/plra/audit
```

Valores monetarios e percentuais devem ser strings decimais. A resposta deve incluir resultado, status, formula, versao metodologica, pendencias, limitacoes e bloqueios.

### 8.13 Frontend

Rota alvo:

```text
/analises/:analysisId/exercicios/:year/plra
```

A tela deve:

- exibir `PLR bruto`, ativos ajustados, passivos exigiveis e `PLRA`;
- mostrar status e versao metodologica;
- mostrar politica default aplicada;
- listar pendencias e bloqueios;
- permitir abrir auditoria por conta;
- encaminhar avaliacao/justificativa para o fluxo da SPEC-005;
- cobrir loading, vazio, erro e sucesso;
- usar `.tnum` para valores e percentuais;
- nao recalcular valores localmente.

### 8.14 Persistencia

Persistir:

- snapshot `plra_calculations`;
- audit rows `plra_audit_rows`;
- politica/versao metodologica usada;
- pendencias e bloqueios;
- vinculo com analise e exercicio.

Snapshots devem ser imutaveis para fins historicos. Reprocessamento cria nova versao/snapshot e invalida dependentes sem alterar resultados emitidos retroativamente.

### 8.15 Exportacao

O Excel deve incluir:

- aba `plra_resumo`;
- aba `plra_memoria`;
- formula, status e versao;
- valor contabil, desagio, valor default, avaliacao validada e valor final;
- exclusoes, pendencias, limitacoes e bloqueios;
- conciliacao informativa com `J100`.

Excel apenas serializa o snapshot.

## 9. Responsabilidades Por Camada

### Domain

Modelar politica, calculo, audit rows, estados e invariantes.

### Engine

Executar hierarquia, classificacao exata, desagios, consolidacao e bloqueios.

### Application

Orquestrar calculo, persistencia, invalidacao e integracoes.

### API

Validar requests, serializar decimais e expor snapshots sem regra prudencial na rota.

### Frontend

Exibir resultado e auditoria, acionando comandos permitidos sem recalculo.

### Repositories

Persistir snapshots, audit rows e versao metodologica.

### Export

Serializar memoria e resultado sem recalculo.

## 10. Criterios De Aceite

- Formula de `PLR bruto` e `PLRA` e aplicada no backend.
- Conta pai e filha nao sao somadas conjuntamente.
- `I051` ausente nao gera codigo inferido.
- `J100` nao e fonte primaria.
- Defaults aprovados sao aplicados automaticamente.
- Default aplicado nao bloqueia sozinho o componente.
- Avaliacao validada prevalece sobre default.
- Exclusao produz auditoria e valor economico zero.
- Passivo condicional nao resolvido impede resultado final.
- Snapshot preserva versao metodologica.
- Contrato CAPAG-E recebe PLRA calculado e status real.
- API e Excel serializam `Decimal` como string.
- Frontend nao recalcula.

## 11. Estrategia De Validacao Esperada

Testes obrigatorios:

- calculo de `PLR bruto` e `PLRA`;
- defaults de todos os grupos;
- conta pai/filha sem duplicidade;
- conta sem `I051` auditada e nao inferida;
- codigo sem regra exata nao classificado;
- exclusoes automaticas;
- passivos automaticos e condicionais;
- avaliacao validada substituindo default;
- bloqueio por evidencia critica;
- reconciliacao informativa com `J100`;
- persistencia e recuperacao de snapshot;
- invalidacao de assessment dependente;
- contratos API;
- UI sem recalculo;
- exportacao Excel;
- fluxo E2E com fixture ECD governada;
- rejeicao de `float`.

Validacoes oficiais devem executar via Docker Compose.

## 12. Riscos E Mitigacoes

- Risco: apresentar politica interna como formula oficial da PGFN.
  Mitigacao: identificar origem interna em API, UI, Excel e laudo.
- Risco: desagio default excessivamente conservador.
  Mitigacao: permitir avaliacao validada e preservar memoria do default.
- Risco: dupla contagem patrimonial.
  Mitigacao: algoritmo de hierarquia e testes pai/filha.
- Risco: cobertura incompleta do plano referencial.
  Mitigacao: dependencia do plano oficial completo e auditoria sem inferencia.
- Risco: alteracao metodologica retroativa.
  Mitigacao: versoes e snapshots imutaveis.
- Risco: resultado final com conta condicional relevante.
  Mitigacao: pendencia explicita e bloqueio do componente.

## 13. Proibicoes

- inferir codigo referencial;
- classificar por prefixo amplo inseguro;
- somar conta pai e filha;
- usar `J100` como base primaria;
- usar `float`;
- recalcular em frontend, Excel ou laudo;
- ocultar default, override, pendencia ou bloqueio;
- alterar snapshot historico por nova politica;
- tratar percentual interno como percentual oficial da PGFN.
