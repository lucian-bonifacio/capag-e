# SPEC-002 - Modulo 1: Camada Declarada

## 1. Objetivo Tecnico

Especificar a camada declarada do CAPAG, isto e, a leitura auditavel da ECD conforme entregue, usando `I051` como classificacao referencial declarada, plano referencial oficial para descricao formal e metodologia interna versionada para tratamento por finalidade.

Esta SPEC deve impedir que codigos referenciais especificos sejam reduzidos a prefixos amplos perigosos e deve preparar a coexistencia futura com a camada reclassificada/comportamental.

## 2. Contexto E Problema

O PRD exige que o CAPAG preserve a leitura declarada da ECD como camada explicita e rastreavel. A arquitetura define que a camada declarada deve ser separada da camada comportamental, persistida como snapshot com versao metodologica e exposta por API, frontend, Excel e laudo sem recalculo fora dos motores.

O problema central desta SPEC e que a ECD pode declarar um `COD_CTA_REF` especifico no `I051`, mas a metodologia interna pode aplicar regras amplas demais por prefixo. Exemplo: `2.01.01.07.01`, referente a emprestimos/financiamentos, nao pode ser tratado como fornecedor apenas porque comeca com `2.01.01`.

## 3. Fontes Usadas

Fontes principais obrigatorias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`

Fontes de referencia autorizadas pelo usuario para fechar contratos metodologicos da camada declarada:

- `docs/reference/ajuste_modulo_principal.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/02-spec-camada-declarada.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/03-plano-referencial-oficial.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/04-metodologia-interna-plr.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/05-metodologia-interna-fco.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/06-motor-e-auditoria-declarada.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/07-api-payload-frontend-declarado.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/08-exportacao-excel-declarada.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/09-testes-camada-declarada.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/11-persistencia-camada-declarada.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/13-status-regras-e-bloqueio-prefixo-amplo.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/14-validacoes-automaticas-metodologia.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/15-algoritmo-match-metodologico.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/16-resultado-por-conta-declarada.md`
- `docs/reference/planejamento-modulos/modulo-01-camada-declarada/17-exemplo-completo-conta-1725.md`

Fontes frontend governadas consultadas porque esta SPEC envolve tela/consumo de API:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## 4. Escopo

Esta SPEC cobre:

- definicao de camada declarada;
- registros ECD necessarios para leitura declarada;
- separacao entre plano referencial oficial e metodologia interna;
- contrato do plano referencial oficial;
- contrato da tabela metodologica interna;
- status de regras metodologicas;
- algoritmo de match metodologico seguro;
- resultado por conta declarada;
- persistencia de dados e snapshots declarados;
- API da camada declarada;
- regras de frontend para exibicao sem recalculo;
- exportacao Excel declarada sem recalculo;
- validacoes automaticas e testes obrigatorios.

## 5. Fora De Escopo

Esta SPEC nao cobre:

- julgamento de substancia economica da conta;
- score, confianca ou recomendacao comportamental;
- reclassificacao automatica baseada em nome, historico, contrapartida ou comportamento;
- DFC direta completa e apuracao final de `FCA`;
- motor `ROA + PLRA`;
- geracao de laudo;
- administracao livre de metodologia pela UI;
- definicao de todas as regras metodologicas reais do projeto;
- populacao completa do plano referencial oficial.

## 6. Decisoes Ja Aprovadas

- A ECD e a fonte declaratoria.
- O `I051` contem o vinculo declaratorio entre conta societaria e `COD_CTA_REF`.
- A camada declarada responde: "qual e o resultado se a ECD for aceita conforme entregue?"
- A camada declarada nao audita se o contador classificou corretamente.
- A camada declarada deve apontar problemas de cobertura metodologica.
- Plano referencial oficial e metodologia interna sao artefatos distintos.
- Plano referencial oficial valida e enriquece o significado formal do `COD_CTA_REF` exato declarado na ECD.
- Metodologia interna define tratamento por finalidade para o codigo referencial exato: PLR/PLRA, FCO, CAPAG-E, auditoria e exportacao.
- O plano referencial oficial nao identifica codigo alternativo ao declarado na ECD.
- A metodologia interna nao usa prefixo, codigo generico ou fallback amplo para inferir tratamento.
- Ausencia de regra metodologica exata deve gerar status revisavel, nao classificacao por inferencia.
- Valores contabeis e prudenciais usam `Decimal` no backend.
- Valores financeiros trafegam na API como string decimal.
- Frontend, Excel e laudo nao recalculam regra de negocio.

## 7. Decisoes Pendentes

Nao ha decisao essencial pendente para criar TASKs da camada declarada, desde que as TASKs respeitem estes limites:

- TASKs podem estruturar plano oficial, metodologia, matcher, API, UI e Excel conforme os contratos desta SPEC.
- TASKs nao podem inventar regras prudenciais ausentes.
- TASKs devem tratar regras ainda nao aprovadas como `EM_REVISAO`, `BLOQUEADA`, `DEPRECIADA` ou `NAO_MAPEADO_METODOLOGICAMENTE`, conforme o caso.

Decisoes que permanecem para SPECs posteriores:

- criterio final de `FCA` completo;
- criterio final de `ROA`;
- contrato canonico completo de CAPAG-E;
- formato final do laudo;
- regras comportamentais de reclassificacao.

## 8. Contratos

### 8.1 Registros ECD Consumidos

A camada declarada deve consumir, no minimo:

- `I050`: plano de contas societario;
- `I051`: vinculo com plano referencial;
- `I155`: saldos por conta;
- `I200`: lancamentos;
- `I250`: partidas;
- `J100`: balanco patrimonial;
- `J150`: futuramente, quando implementado conforme arquitetura.

O parser e normalizador devem preservar dados necessarios para auditoria, incluindo linha original quando disponivel.

### 8.2 Plano Referencial Oficial

O plano referencial oficial deve representar o significado formal do `COD_CTA_REF` exato declarado na ECD, funcionando como legenda, validador e enriquecedor. Ele nao pode decidir calculo nem inferir codigo alternativo ao declarado.

Campos minimos:

- `reference_code`;
- `official_description`;
- `parent_reference_code`;
- `level`;
- `nature`;
- `valid_from`;
- `valid_to`;
- `layout`;
- `entity_type`;
- `source`;
- `status`;
- `methodology_version_id`.

Quando o `COD_CTA_REF` nao existir no plano oficial carregado:

- nao inventar descricao;
- preservar codigo declarado;
- retornar status `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`;
- indicar acao `revisar_base_oficial`.

### 8.3 Metodologia Interna

A metodologia interna deve definir tratamento por finalidade e nao redefinir a semantica oficial do codigo.

Campos minimos:

- `reference_code`;
- `purpose`;
- `methodology_description`;
- `plra_category`;
- `fco_category`;
- `capag_category`;
- `flow_nature`;
- `operational_treatment`;
- `include_in_calculation`;
- `sign`;
- `rule_status`;
- `valid_from`;
- `valid_to`;
- `methodology_version_id`;
- `observation`.

Finalidades minimas:

- `PLR` ou `PLRA` declarada, conforme nomenclatura do modulo 3;
- `FCO` declarado, sem afirmar que e `FCA` completo;
- `CAPAG_E_DECLARADA`;
- `AUDITORIA`;
- `EXPORTACAO`.

### 8.4 Status De Regras

Status permitidos:

- `ATIVA`: pode classificar.
- `BLOQUEADA`: nao pode classificar resultado final.
- `EM_REVISAO`: nao pode ser usada automaticamente em calculo novo.
- `DEPRECIADA`: nao pode ser usada em calculo novo, salvo consulta historica explicita.

### 8.5 Algoritmo De Match Metodologico

Entrada:

- `reference_code`;
- ano/exercicio;
- leiaute;
- tipo de entidade, quando aplicavel;
- finalidade.

Processo obrigatorio:

1. Buscar o codigo no plano referencial oficial.
2. Se nao existir, retornar `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
3. Buscar regra metodologica pelo mesmo `reference_code` exato, finalidade, exercicio, leiaute e tipo de entidade quando aplicavel.
4. Se existir regra exata `ATIVA` com tratamento da finalidade, retornar `MAPEADO`.
5. Se existir regra exata `BLOQUEADA`, retornar `REGRA_BLOQUEADA` e nao classificar calculo novo.
6. Se existir regra exata `EM_REVISAO`, retornar `REGRA_EM_REVISAO` e nao classificar calculo novo.
7. Se existir regra exata `DEPRECIADA`, retornar `REGRA_DEPRECIADA` e nao classificar calculo novo.
8. Se nenhuma regra metodologica exata existir, retornar `NAO_MAPEADO_METODOLOGICAMENTE`.
9. Nao avaliar prefixos, codigos genericos ou fallback amplo para inferir tratamento.

### 8.6 Resultado Por Conta Declarada

Cada conta declarada deve produzir objeto com:

- `account_code`;
- `account_name`;
- `declared_reference_code`;
- `official_description`;
- `official_reference_status`;
- `methodology_rule_applied`;
- `methodology_rule_status`;
- `purpose`;
- `plra_category`;
- `fco_category`;
- `capag_category`;
- `flow_nature`;
- `treatment`;
- `base_value`;
- `considered_value`;
- `final_status`;
- `observation`;
- `recommended_action`;
- `methodology_version_id`.

Valores monetarios devem ser `Decimal` no dominio e string decimal na API.

Status por conta:

- `MAPEADO`;
- `NAO_MAPEADO_METODOLOGICAMENTE`;
- `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`;
- `SEM_VINCULO_REFERENCIAL`;
- `REGRA_BLOQUEADA`;
- `REGRA_EM_REVISAO`;
- `REGRA_DEPRECIADA`;
- `EXCLUIDO_AUTOMATICAMENTE`;
- `INCLUIDO_AUTOMATICAMENTE`.

### 8.7 API

Endpoints alvo:

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

Erros HTTP devem distinguir validacao de request, ausencia de analise/exercicio, erro de processamento e erro de dominio. Falhas metodologicas por conta devem preferencialmente aparecer como status no payload, nao como erro HTTP global, quando a analise puder ser concluida parcialmente.

### 8.8 Frontend

Rota alvo:

```text
/analises/:analysisId/exercicios/:year/declarada
```

A tela deve:

- exibir a classificacao declarada da ECD;
- exibir descricao oficial do plano referencial;
- exibir tratamento metodologico aplicado;
- exibir status por conta;
- distinguir dado declarado, descricao oficial, metodologia interna e ajuste/revisao futura;
- usar `.tnum` para valores, codigos e percentuais;
- usar badges de status conforme tokens governados;
- permitir auditoria/detalhe sem recalcular resultado.

O frontend nao pode:

- reimplementar matcher;
- recalcular PLR/FCO/CAPAG-E;
- alterar status retornado pelo backend;
- tratar prefixo amplo como fallback local.

### 8.9 Excel

A exportacao Excel deve serializar estado calculado, sem recalculo.

Abas declaradas esperadas, quando aplicavel:

- `resumo_executivo`;
- `campos_resultado`;
- `memoria_calculo`;
- `fco_status`;
- `alertas_pendencias`;
- `log_auditoria`;
- `inconsistencias`;
- `sem_vinculo_ref`.

Colunas minimas para rastreabilidade declarada:

- conta societaria;
- nome da conta;
- `COD_CTA_REF` declarado;
- descricao oficial;
- regra metodologica aplicada;
- status da regra;
- tratamento PLR/FCO/CAPAG-E;
- valor base;
- valor considerado;
- status final;
- observacao;
- versao metodologica.

## 9. Responsabilidades Por Camada

### IO

Ler, parsear e normalizar ECD, preservando `I050`, `I051`, `I155`, `I200`, `I250`, `J100`, linha original e valores como `Decimal`.

Nao aplicar metodologia prudencial.

### Domain

Definir entidades e value objects para conta, vinculo referencial, regra metodologica, status, resultado declarado, auditoria e versionamento metodologico.

### Engine

Executar matcher seguro, aplicar metodologia por finalidade, gerar resultado por conta, auditoria e snapshots declarados.

### Application

Orquestrar `run_declared_layer`, garantir transacao, carregar metodologia versionada, persistir snapshot atomico e invalidar dependentes quando necessario.

### API

Expor endpoints, validar parametros, serializar `Decimal` como string e converter erros de dominio em contrato HTTP.

### Repositories

Persistir empresas, ECDs, exercicios, contas, vinculos `I051`, saldos, lancamentos, plano oficial, metodologia, resultados declarados e snapshots.

### Frontend

Renderizar a camada declarada e estados de UI sem regra prudencial local.

### Export

Serializar resultados declarados, auditoria, pendencias, inconsistencias e versao metodologica para Excel.

## 10. Dados De Entrada E Saida

Entradas:

- arquivo ECD importado;
- registros `I050`, `I051`, `I155`, `I200`, `I250`, `J100`;
- plano referencial oficial versionado;
- metodologia interna versionada;
- empresa, exercicio, leiaute e tipo de entidade.

Saidas:

- resultados por conta declarada;
- PLR/PLRA declarada, quando a metodologia permitir;
- FCO declarado, sem rotular como `FCA` completo;
- CAPAG-E declarada, quando contrato posterior permitir;
- auditoria declarada;
- contas sem vinculo referencial;
- codigos sem descricao oficial;
- codigos sem regra metodologica segura;
- snapshots com `methodology_version_id`;
- payloads de API;
- visualizacao frontend;
- abas Excel declaradas.

## 11. Estados E Erros Relevantes

Estados de processamento:

- `nao_executado`;
- `processando`;
- `concluido`;
- `concluido_com_pendencias`;
- `bloqueado`;
- `erro`.

Estados por conta sao os definidos no contrato de resultado por conta.

Erros e pendencias:

- ECD sem registros minimos para camada declarada;
- conta sem `I051`;
- `COD_CTA_REF` ausente no plano oficial;
- metodologia inexistente para codigo oficial;
- regra bloqueada, em revisao ou depreciada como unica candidata;
- conflito ou duplicidade de regra;
- codigo metodologico inexistente no plano oficial;
- tentativa de usar `float`;
- tentativa de recalculo em frontend/exportacao.

## 12. Criterios De Aceite

- A camada declarada preserva o `COD_CTA_REF` do `I051`.
- O plano referencial oficial e separado da metodologia interna.
- A metodologia interna possui status de regra.
- O matcher valida o codigo exato declarado na ECD contra o plano referencial oficial.
- O plano referencial oficial enriquece o codigo declarado com descricao, hierarquia, natureza, vigencia, leiaute e tipo de entidade, sem inferir codigo alternativo.
- O matcher aplica metodologia apenas quando existir regra exata para o codigo declarado e finalidade.
- Prefixos, codigos genericos e fallbacks amplos nao classificam resultado final.
- `EM_REVISAO` e `DEPRECIADA` nao sao usadas em calculo novo.
- Codigo oficial sem regra metodologica exata retorna `NAO_MAPEADO_METODOLOGICAMENTE`.
- Codigo ausente no plano oficial retorna `COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.
- Conta sem vinculo referencial retorna `SEM_VINCULO_REFERENCIAL`.
- Resultado por conta expõe codigo declarado, descricao oficial, regra aplicada, status da regra, tratamento e status final.
- API serializa valores financeiros como string decimal.
- Frontend consome payload e nao recalcula metodologia.
- Excel serializa snapshots e nao recalcula regra.
- Conta `1725` com `2.01.01.07.01` nunca e classificada como fornecedor por `2.01.01.*`, pois prefixos nao sao fonte de tratamento metodologico.

## 13. Estrategia De Validacao Esperada

Testes unitarios:

- extracao de `I051`;
- normalizacao de valores como `Decimal`;
- lookup no plano referencial oficial;
- matcher por codigo exato;
- status de regra;
- resultado por conta declarada;
- serializacao decimal para API;
- exportacao sem chamada de motor.

Testes de integracao:

- `POST /declared/run` cria snapshot declarado;
- `GET /declared` retorna resumo;
- `GET /declared/accounts` retorna contas com status corretos;
- analise com pendencias metodologicas conclui como parcial quando aplicavel.

Testes/golden cases obrigatorios:

- emprestimo nao pode virar fornecedor: `2.01.01.07.01` nao vira `pagamentos_fornecedores` por prefixo;
- fornecedor real pode virar fornecedor;
- tributo a recuperar nao pode virar cliente: `1.01.02.03.*` nao vira `recebimento_clientes` por prefixo;
- prefixo nao pode classificar: se apenas `2.01.01.*` existir como regra, resultado e `NAO_MAPEADO_METODOLOGICAMENTE`;
- regra exata vence por ser a unica forma permitida de tratamento: `2.01.01.07.01` pode classificar quando houver regra exata aprovada;
- conta `1725` preserva descricao oficial e tratamento de financiamento;
- Excel contem colunas declaradas e versao metodologica;
- frontend exibe estados de vazio, loading, sucesso, pendencia e erro sem recalculo.

Validacoes automaticas de metodologia:

- detectar qualquer regra metodologica baseada em prefixo ou padrao amplo;
- detectar regras duplicadas por codigo/finalidade/vigencia;
- detectar duplicidade ou conflito entre regras exatas por codigo/finalidade/vigencia;
- detectar codigos metodologicos ausentes no plano oficial;
- detectar codigos oficiais relevantes sem metodologia;
- detectar regras vencidas em uso;
- detectar regras bloqueadas, em revisao ou depreciadas aplicadas;
- detectar tratamentos iguais aplicados a naturezas oficiais diferentes sem justificativa;
- detectar categorias FCO incompatíveis com natureza oficial;
- detectar codigos de divida tratados como fornecedor.

## 14. Riscos E Mitigacoes

- Risco: prefixo amplo voltar a classificar conta especifica.
  Mitigacao: metodologia por codigo exato, rejeicao de prefixos como fallback e golden tests obrigatorios.

- Risco: plano oficial e metodologia interna serem misturados.
  Mitigacao: contratos separados e campos separados no resultado por conta.

- Risco: frontend recalcular resultado para facilitar exibicao.
  Mitigacao: payload completo e proibicao explicita de regra prudencial no frontend.

- Risco: Excel divergir da API.
  Mitigacao: exportacao serializa snapshot declarado e nao chama motor.

- Risco: regra metodologica incompleta virar classificacao falsa.
  Mitigacao: ausencia de regra exata retorna `NAO_MAPEADO_METODOLOGICAMENTE` com acao de revisao.

- Risco: metodologia nova alterar historico.
  Mitigacao: snapshots com `methodology_version_id`.

## 15. Bloqueios

Nao ha bloqueio para criar TASKs da camada declarada conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- criar julgamento comportamental dentro da camada declarada;
- definir `FCA` completo a partir de `FCO` declarado;
- emitir laudo final usando a camada declarada sem contrato CAPAG-E posterior;
- usar regra prudencial sem fonte normativa ou decisao aprovada;
- usar `float` para valores contabeis ou prudenciais.
