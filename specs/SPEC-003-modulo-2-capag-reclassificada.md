# SPEC-003 - Modulo 2: CAPAG Reclassificada

## 1. Objetivo Tecnico

Especificar a camada reclassificada/comportamental do CAPAG, criando uma segunda leitura paralela da ECD baseada em comportamento contábil, evidências estruturadas, score, confiança, salvaguardas e revisão humana.

Esta SPEC define um cenário completo reclassificado, capaz de recalcular impactos em PLR/PLRA e CAPAG-E quando os contratos necessários estiverem disponíveis, preservando sempre a camada declarada original.

## 2. Contexto E Problema

O PRD exige que o CAPAG preserve a leitura declarada da ECD e crie uma segunda leitura reclassificada/comportamental sem substituição silenciosa. A arquitetura define motor comportamental determinístico, auditável e conservador, com perfis, famílias, score, confiança, comparação com a camada declarada, revisão humana e persistência.

O problema central é que a classificação declarada no `I051` pode divergir do comportamento observado da conta. A camada reclassificada deve responder: "o que os movimentos, saldos, históricos, contrapartidas, recorrência, materialidade e precedentes permitidos mostram que esta conta realmente parece ser?"

## 3. Fontes Usadas

Fontes principais obrigatórias:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`

Fontes de referência autorizadas pelo usuário:

- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/00-visao-geral.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/02-spec-conceitual-oficial.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/03-entrada-ecd-e-dados-necessarios.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/04-normalizacao-comportamental.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/05-razao-por-conta-e-contrapartidas.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/06-perfil-comportamental-conta.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/07-taxonomia-familias-contabeis.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/08-regras-deterministicas-familias.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/09-motor-score-confianca-seguranca.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/10-classificacao-em-camadas-mapeamento-referencial.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/11-comparacao-com-camada-declarada.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/12-cenario-capag-reclassificada.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/13-relatorio-auditavel-e-evidencias.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/14-revisao-humana-precedentes.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/15-banco-dados-evolucao-futura.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/16-api-contratos-backend.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/17-frontend-revisao-comportamental.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/18-exportacao-laudo-comparativo.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/19-metricas-qualidade-calibracao.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/20-testes-validacao-mvp.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/21-roadmap-execucao-modulo-2.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/23-exemplo-fluxo-conta.md`
- `docs/reference/planejamento-modulos/modulo-02-capag-reclassificada/24-riscos-conceituais-e-salvaguardas.md`

Fontes frontend governadas:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Decisão adicional do usuário nesta SPEC:

- O MVP deve mirar cenário completo reclassificado.
- A auditoria deve permitir ajuste manual analítico ou por subgrupo inteiro.

## 4. Escopo

Esta SPEC cobre:

- segunda leitura comportamental paralela à camada declarada;
- dados ECD necessários para comportamento;
- normalização comportamental sem perda do dado original;
- razão por conta e contrapartidas;
- perfil comportamental por conta;
- taxonomia MVP de famílias contábeis;
- regras determinísticas por família;
- score, confiança, diferença entre famílias e salvaguardas;
- mapeamento família -> código referencial sugerido;
- comparação declarado vs reclassificado;
- cenário completo reclassificado;
- revisão humana e ajustes manuais;
- ajuste manual analítico e por subgrupo via auditoria;
- persistência de perfis, classificações, revisões e snapshots;
- API, frontend, exportação comparativa e testes.

## 5. Fora De Escopo

Esta SPEC não cobre:

- alterar a camada declarada original;
- classificar por palavra-chave isolada;
- usar IA generativa como núcleo decisório;
- administrar regras livremente pela UI;
- precedentes globais persistidos sem governança;
- recalcular Excel internamente;
- gerar laudo narrativo final;
- definir fórmula final de FCA, ROA ou contrato CAPAG-E além do consumo dos contratos posteriores;
- criar avaliação de evidências e ativos do Módulo 4.

## 6. Decisões Já Aprovadas

- A camada declarada permanece preservada.
- A camada reclassificada é paralela, determinística, auditável e conservadora.
- O `I051` é preservado como dado declarado, mas não é verdade decisória principal da segunda leitura.
- A decisão comportamental deve considerar conjunto de sinais, não palavra-chave isolada.
- Falso positivo é mais grave do que mandar para revisão.
- Casos ambíguos, materiais ou sensíveis devem ir para revisão humana.
- O MVP deve gerar cenário completo reclassificado.
- Ajustes manuais podem ocorrer pela auditoria em nível analítico ou de subgrupo.
- Ajustes manuais afetam o cenário revisado/reclassificado, nunca sobrescrevem a camada declarada.
- Regra prudencial sensível permanece no backend.
- Frontend não recalcula score, regra, PLR/PLRA ou CAPAG-E.
- Exportação serializa resultados calculados e revisados, sem recalcular.
- Valores contábeis e prudenciais usam `Decimal` no backend e string decimal na API.

## 7. Decisões Pendentes

Não há bloqueio para criar TASKs do Módulo 2 conforme esta SPEC.

Dependências de SPECs posteriores:

- O recálculo completo do cenário reclassificado deve consumir o contrato CAPAG-E da SPEC do Módulo 3 quando disponível.
- Evidências formais, materialidade de bloqueio e ativos seguem a SPEC do Módulo 4.
- DFC/FCA completo segue a SPEC do Módulo 5.
- ROA + PLRA segue a SPEC do Módulo 6.
- Laudo final segue a SPEC do Módulo 7.

Até esses contratos existirem, TASKs podem gerar cenário reclassificado parcial ou bloqueado, desde que exibam status, limitações e impactos calculáveis.

## 8. Contratos

### 8.1 Entradas ECD

Registros mínimos:

- `I050`: plano de contas, hierarquia, tipo e natureza;
- `I051`: classificação referencial declarada;
- `I155`: saldos;
- `I200`: lançamentos;
- `I250`: partidas;
- históricos de lançamentos e partidas;
- `J100`: referência patrimonial.

Registros futuros possíveis:

- `I052`: centro de custos;
- `I355`: saldos de contas de resultado;
- `J150`: demonstração do resultado;
- `0150`: participantes, se disponível e relevante.

### 8.2 Normalização Comportamental

O sistema deve preservar texto original e criar texto normalizado para análise.

Normalizações permitidas:

- datas ISO;
- valores como `Decimal`;
- indicador débito/crédito preservado;
- remoção de acentos para métricas;
- espaços duplicados;
- abreviações comuns, como `FORNEC.`, `FORN`, `NF`, `DUPL`, `PGTO`, `REC`, `C/C`.

Normalização textual não pode virar classificação por palavra-chave.

### 8.3 Razão Por Conta E Contrapartidas

Para cada conta analítica:

- agrupar partidas `I250`;
- vincular cada partida ao lançamento `I200`;
- identificar contas do lado oposto;
- em lançamentos simples, usar contrapartida direta;
- em lançamentos compostos, registrar todas as contrapartidas relacionadas;
- calcular participação por valor quando possível;
- marcar ambiguidade;
- reduzir score quando contrapartida for incerta.

Métricas mínimas:

- débitos;
- créditos;
- saldos;
- históricos;
- meses com movimento;
- lançamentos simples;
- lançamentos compostos;
- concentração por contraparte.

### 8.4 Perfil Comportamental

Cada conta deve gerar um `BehavioralAccountProfile` com:

- métricas financeiras;
- métricas de contrapartida;
- métricas textuais;
- métricas hierárquicas;
- evidências positivas;
- evidências negativas;
- versão metodológica.

Métricas financeiras incluem totais de débitos/créditos, saldos, quantidade de lançamentos, recorrência, volatilidade, saldo típico e carrega/zera saldo.

Métricas de contrapartida incluem principais contrapartidas por valor/quantidade, percentuais por família e concentração.

Métricas textuais incluem tokens do nome, históricos e sinais recorrentes.

Métricas hierárquicas incluem grupo pai, caminho hierárquico, natureza superior, nível e contas irmãs.

### 8.5 Taxonomia MVP

Famílias MVP:

- `bancos_disponibilidades`;
- `clientes`;
- `fornecedores`;
- `adiantamento_fornecedores`;
- `imobilizado`;
- `despesas_operacionais`;
- `receitas`.

Famílias sensíveis ou futuras devem ser tratadas com conservadorismo até haver regra aprovada.

### 8.6 Regras Determinísticas

Cada regra deve ter:

- família;
- macroclasse esperada;
- evidências positivas;
- evidências negativas;
- pesos;
- penalidades;
- score mínimo automático;
- score mínimo de revisão;
- justificativas.

Texto ajuda, mas não decide sozinho. A decisão deve combinar nome, hierarquia, saldo, débitos, créditos, contrapartidas, históricos, recorrência, materialidade, regras, score e diferença entre famílias.

### 8.7 Score, Confiança E Salvaguardas

Limiar inicial do MVP:

- `score >= 80`: classificação automática no cenário comportamental, salvo salvaguarda;
- `score entre 60 e 79`: sugestão com revisão recomendada;
- `score entre 40 e 59`: baixa confiança e revisão obrigatória;
- `score < 40`: sem classificação.

Diferença entre primeiro e segundo colocado:

- `score_gap >= 20`: decisão mais segura;
- `score_gap < 20`: ambígua.

Salvaguardas obrigatórias que impedem reclassificação automática:

- score baixo;
- diferença pequena entre famílias;
- poucos lançamentos;
- lançamentos compostos demais;
- histórico genérico;
- conta sintética;
- conta de encerramento;
- conta transitória;
- comportamento instável entre períodos;
- materialidade elevada;
- tributos;
- partes relacionadas;
- patrimônio líquido;
- classificações sensíveis.

### 8.8 Mapeamento Família Para Referencial

Camadas:

1. Macroclasse.
2. Grupo.
3. Família.
4. Subfamília.
5. Código referencial final.

O sistema só pode sugerir código referencial final quando houver confiança suficiente nas camadas anteriores e mapeamento versionado.

Campos mínimos do mapeamento:

- `detected_family`;
- `detected_subfamily`;
- `macroclass`;
- `suggested_reference_code`;
- `suggested_reference_description`;
- `validity`;
- `calendar_year`;
- `layout`;
- `entity_type`;
- `observations`;
- `methodology_version_id`.

### 8.9 Comparação Com Camada Declarada

Estados oficiais:

- `manter`;
- `reclassificar`;
- `revisar`;
- `sem_conclusao`.

A comparação deve registrar:

- código referencial original;
- família declarada;
- família comportamental;
- código referencial sugerido;
- motivo da divergência;
- impacto potencial;
- status de revisão.

### 8.10 Cenário Completo Reclassificado

O cenário completo reclassificado deve distinguir:

- resultado declarado;
- resultado reclassificado automático;
- resultado revisado pelo humano;
- simulações.

Regras:

- O cenário reclassificado usa classificações comportamentais automáticas apenas quando score, confiança e salvaguardas permitirem.
- Contas com revisão humana usam a decisão humana aprovada.
- Contas sem conclusão mantêm leitura declarada ou são excluídas do cenário conforme contrato posterior do componente impactado, sempre com status explícito.
- PLR/PLRA e CAPAG-E reclassificados só podem ser finais quando os contratos posteriores permitirem.
- Enquanto contratos posteriores não existirem, o cenário pode ser `parcial` ou `bloqueado`, mas deve expor impactos por conta calculáveis.

### 8.11 Revisão Humana E Ajuste Manual

A revisão humana deve permitir:

- aprovar sugestão;
- rejeitar sugestão;
- escolher outra classificação;
- marcar exceção;
- comentar;
- registrar precedente, se fase aprovada;
- aplicar ajuste manual analítico;
- aplicar ajuste manual por subgrupo inteiro.

Tipos de ajuste manual:

- `analytic_account_adjustment`: ajuste em uma conta específica;
- `entry_line_adjustment`: ajuste em lançamento/partida específica, quando suportado;
- `subgroup_adjustment`: ajuste aplicado a um subgrupo de contas;
- `manual_override`: classificação escolhida pelo usuário com justificativa obrigatória.

Todo ajuste manual deve registrar:

- escopo;
- valor ou classificação antes;
- valor ou classificação depois;
- justificativa;
- usuário;
- timestamp;
- impacto estimado;
- versão metodológica;
- origem `auditoria`;
- se cria precedente.

Ajuste por subgrupo deve listar as contas afetadas e permitir exclusões explícitas antes de confirmar.

### 8.12 API

Endpoints alvo:

```text
POST /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/accounts/{account_code}
POST /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/reviews
POST /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/manual-adjustments
POST /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/reclassified-scenario/run
GET  /api/v1/analyses/{analysis_id}/exercises/{year}/behavioral/reclassified-scenario
```

Contrato resumido de classificação:

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
  "positive_evidence": ["saldo tipico credor", "debitos contra banco"],
  "negative_evidence": [],
  "impact": {
    "plra": "-125000.00",
    "capag_e": "-125000.00"
  },
  "review_status": "pendente"
}
```

### 8.13 Frontend

Rota alvo:

```text
/analises/:analysisId/exercicios/:year/reclassificada
```

A tela deve exibir:

- painel com conta original, hierarquia, `I051`, saldos e movimentos;
- painel com classificação sugerida, score, confiança e explicação;
- painel de auditoria com lançamentos, contrapartidas e históricos;
- comparação declarado vs reclassificado;
- cenário reclassificado automático e revisado;
- ações de revisão humana;
- botão/ação `Auditoria` com ajuste manual analítico e por subgrupo.

Regras visuais:

- seguir shell administrativo;
- usar badges para status;
- usar `.tnum` em valores, percentuais, códigos e scores;
- não usar hero ou tela promocional;
- não recalcular score ou impacto no frontend.

### 8.14 Exportação Comparativa

Excel deve serializar:

- resumo dos cenários;
- comparativo declarado vs reclassificado;
- contas reclassificadas;
- contas mantidas;
- contas em revisão;
- contas sem conclusão;
- evidências por conta;
- justificativas;
- ajustes manuais;
- impacto por conta;
- impacto consolidado;
- versão metodológica.

Exportação não pode recalcular.

## 9. Responsabilidades Por Camada

### IO

Fornecer dados normalizados e originais necessários ao perfil comportamental.

### Domain

Modelar perfil, classificação, score, evidência, revisão, ajuste manual, cenário reclassificado, estados e invariantes.

### Engine

Montar razão, calcular perfil, aplicar regras, calcular score, aplicar salvaguardas, sugerir família/referencial e gerar cenário reclassificado.

### Application

Orquestrar execução, persistência, revisão humana, ajustes manuais, invalidação de snapshots dependentes e recálculo do cenário revisado.

### API

Expor contratos sem regra de negócio e serializar `Decimal` como string.

### Frontend

Exibir evidências, revisão e auditoria; enviar decisões humanas; não recalcular regra.

### Export

Serializar cenários e revisões para Excel sem recalcular.

## 10. Dados De Entrada E Saida

Entradas:

- ECD normalizada;
- camada declarada;
- plano oficial;
- metodologia comportamental versionada;
- mapeamento família -> referencial;
- decisões humanas;
- ajustes manuais.

Saídas:

- perfis comportamentais;
- classificações sugeridas;
- score e confiança;
- evidências positivas/negativas;
- ações recomendadas;
- revisões humanas;
- ajustes manuais;
- cenário reclassificado automático;
- cenário reclassificado revisado;
- impactos em PLR/PLRA e CAPAG-E quando calculáveis;
- relatório auditável;
- exportação comparativa.

## 11. Estados E Erros Relevantes

Estados de classificação:

- `manter`;
- `reclassificar`;
- `revisar`;
- `sem_conclusao`;
- `bloqueado_por_salvaguarda`;
- `ajustado_manualmente`;
- `aprovado`;
- `rejeitado`.

Estados do cenário:

- `nao_executado`;
- `parcial`;
- `calculado`;
- `revisado`;
- `bloqueado`;
- `erro`.

Erros e bloqueios:

- dados ECD insuficientes;
- ausência de camada declarada;
- mapeamento família -> referencial ausente;
- score baixo;
- salvaguarda ativa;
- ajuste manual sem justificativa;
- ajuste por subgrupo sem lista de contas afetadas;
- tentativa de alterar camada declarada;
- tentativa de usar `float`;
- tentativa de recalcular no frontend ou Excel.

## 12. Critérios De Aceite

- A camada declarada permanece intacta.
- O sistema monta razão por conta e contrapartidas.
- Lançamentos compostos reduzem confiança ou geram revisão.
- Cada conta possui perfil comportamental e evidências estruturadas.
- O score não depende apenas de palavra-chave.
- Famílias MVP estão explicitadas.
- Score, confiança e `score_gap` são retornados.
- Salvaguardas impedem reclassificação automática.
- Estados `manter`, `reclassificar`, `revisar` e `sem_conclusao` são suportados.
- Cenário completo reclassificado é produzido quando contratos dependentes permitirem.
- Cenário parcial/bloqueado explicita limitações.
- Revisão humana permite aprovar, rejeitar, escolher outra classificação, exceção e comentário.
- Auditoria permite ajuste manual analítico e por subgrupo.
- Ajuste manual exige justificativa e é auditável.
- Ajuste por subgrupo lista contas afetadas.
- API serializa valores como string decimal.
- Frontend não recalcula score, regra, PLR/PLRA ou CAPAG-E.
- Excel serializa cenários e ajustes sem recalcular.

## 13. Estratégia De Validação Esperada

Testes unitários:

- razão por conta;
- contrapartidas simples;
- lançamentos compostos;
- métricas financeiras;
- métricas textuais;
- métricas hierárquicas;
- regras das 7 famílias MVP;
- score e limiares;
- `score_gap`;
- salvaguardas;
- mapeamento família -> referencial;
- ajuste manual analítico;
- ajuste manual por subgrupo.

Testes de integração:

- execução de `behavioral/run`;
- consulta de conta comportamental;
- revisão humana;
- ajuste manual pela auditoria;
- recálculo do cenário revisado;
- exportação comparativa.

Golden/casos obrigatórios:

- conta com comportamento claro de fornecedor e `I051` de ativo deve recomendar `reclassificar`;
- caso ambíguo deve ir para `revisar`;
- score baixo deve gerar `sem_conclusao`;
- materialidade elevada com evidência insuficiente deve bloquear automático;
- ajuste manual deve aparecer no cenário revisado e na exportação;
- camada declarada não pode mudar após revisão comportamental.

## 14. Riscos E Mitigações

- Risco: reclassificação virar busca por palavra-chave.
  Mitigação: exigir conjunto de sinais, score, gap e evidências.

- Risco: falso positivo contaminar cenário, Excel e laudo futuro.
  Mitigação: salvaguardas, revisão humana e status parcial/bloqueado.

- Risco: ajuste manual virar alteração invisível.
  Mitigação: auditoria obrigatória, justificativa e antes/depois.

- Risco: ajuste por subgrupo afetar contas indevidas.
  Mitigação: listar contas afetadas e permitir exclusões explícitas.

- Risco: frontend recalcular impacto.
  Mitigação: API retorna valores prontos e frontend só renderiza.

- Risco: cenário reclassificado depender de contratos ainda não criados.
  Mitigação: permitir cenário parcial/bloqueado até SPECs posteriores.

## 15. Bloqueios

Não há bloqueio para criar TASKs do Módulo 2 conforme esta SPEC.

Permanece bloqueado qualquer trabalho que tente:

- substituir a camada declarada;
- aplicar reclassificação automática em caso protegido por salvaguarda;
- criar precedente global sem governança;
- emitir laudo final sem SPEC do laudo;
- apresentar CAPAG-E reclassificada como final sem contrato CAPAG-E suficiente;
- usar `float` em valores contábeis ou prudenciais.
