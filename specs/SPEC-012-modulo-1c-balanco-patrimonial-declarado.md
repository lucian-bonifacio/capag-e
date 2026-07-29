# SPEC-012 - Modulo 1C: Balanço Patrimonial Declarado

## 1. Objetivo Técnico

Especificar a importação, preservação, construção, apresentação e conciliação
do Balanço Patrimonial declarado na ECD, usando o `J100` como demonstração
oficial e `I050 + I052 + I155` como prova de consistência interna.

Esta SPEC refina a `SPEC-002` para a visão de Balanço Patrimonial e complementa
a `SPEC-011` sem transformar o `J100` em fonte analítica do PLRA.

## 2. Contexto E Problema

O CAPAG já importa e apresenta registros `J100`, mas a implementação atual:

- lê o saldo inicial do `J100` como valor principal;
- trata `J100.COD_AGL` como se fosse `I050.COD_CTA`;
- usa a hierarquia do `I050` para apresentar o `J100`;
- não importa `I052` nem `J005`;
- não realiza a conciliação numérica oficial;
- não preserva o arquivo ECD original completo após a importação.

O Manual da ECD demonstra que o Balanço Patrimonial é declarado no `J100` e
que sua conferência ocorre pela totalização dos saldos do `I155`, relacionados
ao código de aglutinação por meio do `I052`.

## 3. Fontes Usadas

Fontes governadas:

- `docs/product/PRD.md`;
- `docs/architecture/architecture.md`;
- `specs/SPEC-002-modulo-1-camada-declarada.md`;
- `specs/SPEC-011-modulo-1b-motor-plra.md`;
- `docs/methodology/pesquisa-oficial-balanco-patrimonial-ecd.md`.

Fonte oficial:

- Manual de Orientação do Leiaute 9 da ECD, atualização de novembro de 2024,
  Anexo ao Ato Declaratório Executivo Cofis nº 57/2023:
  `https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecd/manuais-e-documentos-tecnicos/manual_de_orientacao_da_ecd_leiaute_9_atualizacao_nov_2024.pdf/@@display-file/file`.

Fonte oficial complementar:

- Perguntas e Respostas - ReceitanetBX:
  `https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/download/receitanetbx/perguntas-e-respostas-receitanetbx`.

## 4. Escopo

Esta SPEC cobre:

- preservação imutável do arquivo ECD importado;
- leitura de registros necessários para determinar a obrigatoriedade do Bloco
  J;
- normalização completa dos campos relevantes do `J100`;
- persistência de `I010`, `I030`, `I052`, `I150`, `J005` e `J100`;
- seleção da demonstração correspondente ao encerramento analisado;
- construção da árvore do balanço pela estrutura do próprio `J100`;
- uso do saldo final do `J100`;
- conciliação das linhas de detalhe por `I050 + I052 + I155`;
- validação estrutural dos totalizadores;
- estados do balanço e das linhas de detalhe;
- API, frontend e auditoria sem recalcular regra no cliente;
- integração do estado do balanço com a elegibilidade do resultado anual
  `PLRA/CAPAG-E`;
- reprocessamento controlado de importações anteriores.

## 5. Fora De Escopo

Esta SPEC não cobre:

- decidir quais contas entram ou saem do PLRA;
- definir deságios, passivos condicionais ou metodologia CAPAG-E;
- alterar fórmula de PLRA, FCA, ROA ou CAPAG-E;
- usar `J100` como fonte analítica primária do PLRA;
- inferir `I051` ou `I052` por nome, prefixo ou semelhança;
- criar switches ou decisões humanas;
- reconstruir demonstração ausente por interpretação livre;
- implementar a DRE completa a partir do `J150`;
- criar snapshots em consultas de leitura.

## 6. Decisões Aprovadas

- O propósito da camada declarada é reproduzir e conferir objetivamente o que
  foi entregue na ECD.
- O Balanço Patrimonial apresentado ao usuário vem do `J100`.
- A hierarquia visual vem de `J100.NIVEL_AGL` e `J100.COD_AGL_SUP`.
- O valor do encerramento vem de `J100.VL_CTA_FIN` e
  `J100.IND_DC_BAL_FIN`.
- `J100.COD_AGL` não é `I050.COD_CTA`.
- A relação oficial é `I050 -> I052 -> J100`.
- Os saldos usados na conciliação vêm do `I155`.
- O `I051` não constrói o balanço; ele vincula a conta ao plano referencial.
- O arquivo ECD original deve ser preservado de forma imutável.
- Consultas ao balanço não criam snapshots.
- Balanço anual obrigatório ausente, estruturalmente inválido ou divergente
  impede resultado anual final de PLRA/CAPAG-E.
- O bloqueio não altera a fórmula prudencial: apenas impede afirmar que o
  resultado é final sobre uma base declarada inconsistente.
- Valores monetários usam `Decimal`, são quantizados em `0.01` e rejeitam
  `float`.

## 7. Decisões Pendentes

Não há decisão essencial pendente para criar TASKs desta SPEC.

## 8. Contratos

### 8.1 Preservação Da ECD Original

Cada `EcdFile` deve preservar:

- conteúdo binário original exato;
- nome original;
- hash SHA-256;
- tamanho em bytes;
- leiaute;
- período;
- data de importação;
- versão do parser usada;
- data do último reprocessamento, quando houver.

Contrato inicial:

- o conteúdo original será persistido no PostgreSQL em coluna binária;
- o conteúdo será imutável após a importação;
- o hash será calculado sobre os mesmos bytes persistidos;
- a exclusão confirmada da importação remove também o conteúdo original;
- a leitura normal da análise não expõe nem transfere o arquivo original;
- download futuro do original exige contrato próprio;
- o limite atual de upload permanece separado e pode evoluir por TASK própria.

### 8.2 Registros ECD Necessários

O parser deve preservar, no mínimo:

- `0000`: período da ECD e campos necessários à identificação;
- `I010`: `IND_ESC`;
- `I030`: data de encerramento do exercício social;
- `I050`: conta, natureza, tipo e hierarquia contábil;
- `I051`: vínculo referencial, sem participação na construção do balanço;
- `I052`: `COD_CCUS` e `COD_AGL`, vinculados ao `I050` pai;
- `I150`: período dos saldos;
- `I155`: conta, centro de custo, saldos e indicadores;
- `J005`: período, identificação e cabeçalho da demonstração;
- `J100`: todos os campos da linha do Balanço Patrimonial;
- `J150`: presença e vínculo com o `J005`, apenas para validação mínima da
  obrigatoriedade nesta SPEC.

Todos os registros normalizados devem preservar número e texto da linha
original.

### 8.3 Campos Do J100

Cada linha normalizada deve conter:

- `aggregation_code`, originado de `COD_AGL`;
- `aggregation_code_type`, originado de `IND_COD_AGL`;
- `aggregation_level`, originado de `NIVEL_AGL`;
- `parent_aggregation_code`, originado de `COD_AGL_SUP`;
- `balance_group`, originado de `IND_GRP_BAL`;
- `description`, originado de `DESCR_COD_AGL`;
- `initial_amount`, originado de `VL_CTA_INI`;
- `initial_debit_credit_indicator`, originado de `IND_DC_BAL_INI`;
- `final_amount`, originado de `VL_CTA_FIN`;
- `final_debit_credit_indicator`, originado de `IND_DC_BAL_FIN`;
- `explanatory_note_reference`, originado de `NOTA_EXP_REF`;
- vínculo com o `J005` pai;
- ordem e linha original.

É proibido nomear `COD_AGL` como código de conta contábil.

### 8.4 Obrigatoriedade Do Balanço

O sistema deve avaliar:

1. período inicial e final do `0000`;
2. data de encerramento do `I030`;
3. forma de escrituração do `I010`;
4. presença de `J005`, `J100` e `J150`.

Quando a data de encerramento estiver dentro do período da ECD e `IND_ESC` for
`G`, `R` ou `B`, devem existir `J005`, `J100` e `J150`.

Quando a data de encerramento estiver fora do período da ECD, o Bloco J não é
obrigatório. Essa ECD não é elegível como base anual final do CAPAG para aquele
encerramento.

### 8.5 Seleção Da Demonstração

Para o exercício anual do CAPAG:

- o encerramento alvo é `31/12` do exercício;
- selecionar `J005` com `DT_FIN` igual ao encerramento alvo;
- usar demonstrações da própria pessoa jurídica, `ID_DEM = 1`;
- selecionar somente os registros `J100` filhos desse `J005`;
- preservar a ordem declarada;
- mais de um `J005` aplicável com o mesmo tipo e período gera estrutura
  inválida, sem escolha silenciosa.

### 8.6 Construção Da Árvore

A árvore do balanço deve:

1. usar `COD_AGL` como identidade da linha;
2. usar `COD_AGL_SUP` como relação pai-filho;
3. usar `NIVEL_AGL` para validar o nível;
4. usar `IND_COD_AGL` para distinguir totalizador `T` e detalhe `D`;
5. usar `IND_GRP_BAL` para separar Ativo `A` e Passivo `P`;
6. usar `DESCR_COD_AGL` como descrição declarada;
7. apresentar `VL_CTA_FIN` e `IND_DC_BAL_FIN` como posição final;
8. preservar valores iniciais para comparação e auditoria.

O sistema não pode:

- inferir hierarquia por prefixo;
- usar a hierarquia do `I050` no lugar da hierarquia do `J100`;
- comparar diretamente `COD_AGL` com `COD_CTA`;
- somar totalizadores e detalhes como se fossem contas independentes.

### 8.7 Conciliação Das Linhas De Detalhe

Para cada linha `J100` com `IND_COD_AGL = D`:

1. localizar registros `I052` com o mesmo `COD_AGL`;
2. considerar somente `I052` pertencente a conta analítica do `I050`;
3. respeitar `COD_CCUS` quando informado;
4. localizar o saldo final do período aplicável no `I155` pela combinação
   conta e centro de custo;
5. normalizar débito e crédito como valor assinado em `Decimal`;
6. totalizar os saldos componentes sem somar conta sintética e analítica em
   duplicidade;
7. comparar o resultado com `J100.VL_CTA_FIN`, respeitando
   `IND_DC_BAL_FIN`;
8. registrar valor declarado, valor calculado e diferença.

A conciliação é exata em centavos:

```text
diferenca = valor_j100_assinado - valor_i155_totalizado_assinado
```

Uma linha está conciliada somente quando `diferenca = 0.00`.

### 8.8 Validação Dos Totalizadores

Linhas `J100` com `IND_COD_AGL = T` devem ser verificadas pela composição de
suas linhas filhas no próprio `J100`.

A validação deve confirmar:

- exatamente duas raízes de nível 1: uma `A` e uma `P`;
- existência de pelo menos uma linha de detalhe;
- pai existente para toda linha de nível superior a 1;
- nível do filho compatível com o pai;
- grupo do filho compatível com a raiz;
- total assinado igual à soma assinada dos filhos imediatos;
- Ativo final igual ao lado Passivo final.

O lado `P` preserva a estrutura declarada de Passivo e Patrimônio Líquido.

### 8.9 Estados

Estado único do balanço:

- `VALIDO`: obrigatório, presente, estrutura válida e todas as linhas de
  detalhe conciliadas;
- `DIVERGENTE`: estrutura legível, mas existe diferença de valor;
- `OBRIGATORIO_AUSENTE`: o Bloco J era obrigatório e o `J100` não existe;
- `ESTRUTURA_INVALIDA`: o `J100` existe, mas sua estrutura não atende ao
  contrato;
- `NAO_OBRIGATORIO`: o Bloco J não era obrigatório para o período.

Estado de cada linha de detalhe:

- `CONCILIADA`;
- `DIVERGENTE`;
- `SEM_I052`;
- `SEM_SALDO_I155`.

Esses estados:

- são calculados automaticamente;
- servem à auditoria;
- não são switches;
- não representam decisão humana;
- não alteram a ECD original.

### 8.10 Precedência Dos Estados

Aplicar a seguinte ordem:

1. `OBRIGATORIO_AUSENTE`;
2. `ESTRUTURA_INVALIDA`;
3. `DIVERGENTE`;
4. `VALIDO`;
5. `NAO_OBRIGATORIO`, somente quando a obrigação não existir.

`SEM_I052` e `SEM_SALDO_I155` tornam o balanço `DIVERGENTE`.

### 8.11 Contrato De API

O endpoint existente:

```text
GET /api/v1/analyses/{analysis_id}/exercises/{year}/declared/balance/accounts
```

deve deixar de retornar `DeclaredAccount` como representação de linha do
balanço e passar a consumir um contrato específico de Balanço Patrimonial.

Resposta mínima:

- `analysis_id`;
- `year`;
- `balance_status`;
- `is_blocking`;
- `j005_period_start`;
- `j005_period_end`;
- `assets_final_amount`;
- `liabilities_and_equity_final_amount`;
- `difference`;
- `rows`;
- `limitations`.

Cada item de `rows` deve conter:

- os campos normalizados do `J100`;
- valor inicial e final serializados como string decimal;
- estado estrutural;
- estado de conciliação para linhas de detalhe;
- valor conciliado;
- diferença;
- quantidade de contas componentes.

O detalhe de uma linha deve permitir consultar as contas `I050/I052/I155`
componentes sem alterar a resposta principal nem recalcular no frontend.

Endpoint de componentes:

```text
GET /api/v1/analyses/{analysis_id}/exercises/{year}/declared/balance/accounts/{aggregation_code}/components
```

Resposta mínima:

- `analysis_id`;
- `year`;
- `aggregation_code`;
- `rows`.

Cada componente deve conter:

- `account_code`;
- `account_name`;
- `cost_center_code`;
- `final_amount`;
- `final_debit_credit_indicator`;
- `signed_final_amount`;
- linha original do vínculo `I052`;
- linha original do saldo `I155`.

Valores monetários devem ser serializados como string decimal.

O endpoint de importação existente mantém a rota:

```text
POST /api/v1/ecd/import
```

Comportamento:

- arquivo novo: `201`, com `reprocessed = false`;
- mesmo hash de importação anterior marcada como `REIMPORTACAO_NECESSARIA`:
  `200`, com `reprocessed = true`;
- mesmo hash de importação completa e atual: `409 ECD_ALREADY_IMPORTED`.

A resposta deve informar também `parser_version` e o estado de preparação do
balanço, sem executar a conciliação no frontend.

### 8.12 Frontend

O frontend deve:

- renderizar a árvore retornada pela API;
- separar Ativo e Passivo + PL;
- distinguir visualmente totalizadores e detalhes;
- mostrar saldo final como valor principal;
- permitir consultar saldo inicial;
- mostrar o estado geral do balanço;
- mostrar a conciliação das linhas de detalhe;
- abrir as contas componentes sob demanda;
- explicar estados em linguagem simples.

O frontend não pode:

- reconstruir hierarquia;
- somar valores contábeis;
- recalcular conciliação;
- decidir obrigatoriedade;
- alterar estado recebido da API;
- criar snapshot por consulta.

### 8.13 Integração Com PLRA E CAPAG-E

O PLRA continua usando como fonte analítica:

- `I050`;
- `I051`;
- `I150`;
- `I155`;
- metodologia PLRA versionada.

O Balanço Patrimonial declarado fornece:

- contexto contábil oficial;
- prova de consistência interna;
- estado de elegibilidade da base anual;
- auditoria `I050 + I052 + I155 -> J100`.

Regras:

- o `J100` não substitui os saldos analíticos do `I155`;
- o `J100` não decide tratamento prudencial;
- `balance_status = VALIDO` permite resultado anual final;
- qualquer estado diferente de `VALIDO` impede afirmar PLRA/CAPAG-E final para
  o exercício;
- valores intermediários podem ser calculados e exibidos como diagnóstico,
  sempre acompanhados do bloqueio;
- corrigir a base exige nova importação ou reprocessamento da ECD, nunca
  alteração manual da camada declarada.

### 8.14 Reprocessamento De Importações Anteriores

Importações existentes não possuem o arquivo original, `I052`, `J005` e outros
campos agora exigidos.

Regras:

- não inferir nem fabricar os registros ausentes;
- marcar importação anterior como `REIMPORTACAO_NECESSARIA` quando não houver
  conteúdo original suficiente;
- permitir reenvio do mesmo arquivo para completar uma importação anterior
  identificada pelo mesmo hash;
- persistir o conteúdo original e os novos registros em uma única transação;
- substituir dados normalizados somente após o novo parse ser concluído com
  sucesso;
- invalidar resultados derivados da versão normalizada anterior;
- preservar identificadores da importação quando o reprocessamento ocorrer
  sobre o mesmo hash;
- registrar versão do parser e data de reprocessamento.

## 9. Fluxo Obrigatório

```text
Upload da ECD
    ↓
Preservar bytes + hash
    ↓
Parsear registros obrigatórios
    ↓
Determinar obrigação do Bloco J
    ↓
Selecionar J005 do encerramento
    ↓
Construir árvore do J100
    ↓
Conciliar I050 + I052 + I155 com J100
    ↓
Publicar balanço e estado
    ↓
Liberar ou bloquear resultado anual final
```

## 10. Critérios De Aceite

- A ECD original é preservada e reproduz o hash registrado.
- `I010`, `I030`, `I052`, `I150`, `J005` e `J100` são normalizados.
- Todos os campos relevantes do `J100` são preservados.
- O saldo final, e não o inicial, é apresentado como posição do balanço.
- A árvore usa exclusivamente a hierarquia formal do `J100`.
- `COD_AGL` não é tratado como `COD_CTA`.
- Linhas de detalhe são conciliadas por `I052 + I155`.
- Totalizadores são validados pela árvore do `J100`.
- O balanço produz um único estado geral e estados simples por linha de
  detalhe.
- A API usa contrato específico de balanço.
- O frontend não recalcula valores ou estados.
- Consultas não persistem snapshots.
- Balanço inválido não permite resultado anual final.
- Importações anteriores podem ser completadas por reenvio controlado.
- Nenhum `I051`, `I052`, código ou hierarquia é inferido.

## 11. Estratégia De Validação

Testes obrigatórios:

- preservação exata dos bytes e do hash;
- parse de todos os campos do `J100`;
- saldo inicial diferente do saldo final;
- `COD_AGL` diferente de `COD_CTA`;
- seleção do `J005` correto entre múltiplos períodos;
- rejeição de múltiplos `J005` igualmente aplicáveis;
- Bloco J obrigatório presente e ausente;
- Bloco J não obrigatório;
- linha conciliada;
- linha divergente;
- linha sem `I052`;
- linha sem saldo `I155`;
- centro de custo no `I052/I155`;
- totalizador correto e incorreto;
- Ativo igual e diferente de Passivo + PL;
- API com valores decimais como string;
- frontend sem soma ou reconstrução local;
- reprocessamento de importação anterior pelo mesmo hash;
- invalidação de resultados derivados;
- fluxo E2E com DATAPACK e INVENTCLOUD em execuções separadas;
- rejeição de `float`.

Todas as validações oficiais devem executar via Docker Compose.

## 12. Migração E Compatibilidade

- A mudança do endpoint de balanço é alteração deliberada de contrato.
- Consumidores atuais devem migrar para o novo payload na mesma entrega
  governada.
- A rota de auditoria por conta da `SPEC-002` permanece separada e continua
  baseada em `I050/I051/I155`.
- Dados antigos não serão convertidos parcialmente quando faltar a ECD
  original.
- DATAPACK e INVENTCLOUD deverão ser reimportados após a migration.

## 13. Riscos E Mitigações

- Risco: tratar código de aglutinação como conta contábil.
  Mitigação: nomes de domínio distintos e vínculo obrigatório pelo `I052`.
- Risco: apresentar saldo inicial como final.
  Mitigação: campos separados e testes com valores diferentes.
- Risco: esconder divergência para continuar a CAPAG.
  Mitigação: estado bloqueante explícito.
- Risco: perder a fonte original e impedir reprocessamento.
  Mitigação: persistência imutável dos bytes e hash.
- Risco: importação antiga parecer compatível.
  Mitigação: estado `REIMPORTACAO_NECESSARIA`.
- Risco: duplicar regra no frontend.
  Mitigação: API entrega árvore, valores e estados prontos.
- Risco: confundir consistência interna com verdade econômica.
  Mitigação: separar balanço declarado de metodologia prudencial e evidências.

## 14. Proibições

- usar `float`;
- montar balanço por nome de conta;
- inferir grupo ou hierarquia por prefixo;
- comparar diretamente `J100.COD_AGL` com `I050.COD_CTA`;
- usar `I051` no lugar de `I052`;
- usar saldo inicial como posição final;
- alterar manualmente a camada declarada;
- fabricar registros ausentes;
- persistir snapshot em consulta;
- emitir resultado anual final sobre balanço obrigatório inválido.

## 15. Suficiência

Esta SPEC está `suficiente_para_task`.

TASKs derivadas:

1. `TASK-101`: ampliar parser do balanço declarado;
2. `TASK-102`: persistir ECD e balanço declarado;
3. `TASK-103`: reprocessar importações ECD legadas;
4. `TASK-104`: implementar conciliação do balanço declarado;
5. `TASK-105`: criar API do balanço declarado;
6. `TASK-106`: criar UI do balanço declarado;
7. `TASK-107`: integrar validade do balanço ao PLRA e CAPAG-E;
8. `TASK-108`: validar fluxo do balanço declarado.
