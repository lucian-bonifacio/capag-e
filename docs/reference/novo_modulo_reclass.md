# PLANO DE IMPLEMENTAÇÃO — RECLASSIFICADOR CONTÁBIL COM PERFIL COMPORTAMENTAL DA ECD

## 1. OBJETIVO DO SISTEMA

Construir um sistema que leia a ECD completa da empresa, ignore o I051 como verdade absoluta e reclassifique as contas contábeis com base no comportamento real observado nos lançamentos, saldos, históricos e contrapartidas.

A premissa central é:

"A conta não é aquilo que o contador disse que ela é.
A conta é aquilo que seus lançamentos mostram que ela faz."

O sistema deve produzir, para cada conta analisada:

- classificação original informada na ECD;
- classificação sugerida pelo sistema;
- família contábil identificada;
- score de confiança;
- evidências usadas;
- justificativa auditável;
- indicação de manter, reclassificar ou revisar manualmente.

---

## 2. PRINCÍPIO TÉCNICO

Não usar IA generativa como núcleo decisório.

O núcleo deve ser determinístico, baseado em:

- estrutura da ECD;
- razão contábil por conta;
- saldos;
- débitos;
- créditos;
- contrapartidas;
- históricos;
- frequência;
- recorrência;
- natureza do saldo;
- regras por família contábil;
- score por evidências.

IA pode ser usada depois, como camada auxiliar, para:

- normalizar descrições;
- identificar nomes empresariais;
- agrupar históricos parecidos;
- sugerir palavras-chave;
- ajudar em contas ambíguas;
- explicar a decisão em linguagem natural.

Mas a decisão principal deve vir do motor de regras.

---

## 3. VISÃO GERAL DO FLUXO

ECD COMPLETA
   ↓
Parser dos registros
   ↓
Extração dos dados principais
   ↓
Cadastro das contas
   ↓
Extração dos lançamentos
   ↓
Montagem do razão por conta
   ↓
Cálculo do perfil comportamental
   ↓
Aplicação das regras por família contábil
   ↓
Geração de scores
   ↓
Classificação provável
   ↓
Mapeamento para plano referencial correto
   ↓
Comparação com I051 original
   ↓
Relatório de reclassificação
   ↓
Revisão humana quando necessário
   ↓
Aprendizado supervisionado por precedentes

---

## 4. FASE 1 — INGESTÃO DA ECD

### 4.1. Objetivo

Ler o arquivo texto da ECD e transformar os registros em dados estruturados.

### 4.2. Entradas

Arquivo .txt da ECD.

### 4.3. Registros inicialmente relevantes

I050 = Plano de contas da empresa
I051 = Plano de contas referencial informado
I052 = Centro de custos, quando aplicável
I155 = Saldos periódicos das contas
I200 = Lançamentos contábeis
I250 = Partidas dos lançamentos
I355 = Saldos de contas de resultado, quando aplicável

Também podem ser usados depois:

0000 = abertura e identificação da escrituração
0007 = outras inscrições cadastrais
0020 = dados adicionais da entidade
0150 = participantes, se existirem no contexto do arquivo
J100 = balanço patrimonial
J150 = demonstração do resultado

### 4.4. Cuidados no parser

O parser precisa tratar:

- linhas quebradas dentro de descrições;
- pipes vazios;
- campos opcionais;
- datas no formato da ECD;
- valores com vírgula ou ponto, conforme padrão do arquivo;
- codificação de caracteres;
- registros com tamanhos diferentes;
- contas analíticas e sintéticas;
- contas sem I051;
- múltiplos I051 para uma mesma conta, se ocorrer;
- períodos com saldos zerados;
- históricos longos;
- históricos complementares, se existirem.

### 4.5. Saída da fase

Tabelas internas estruturadas:

Tabela: contas
- id_conta
- codigo_conta
- nome_conta
- data_inclusao_alteracao
- natureza_informada
- tipo_conta
- nivel
- codigo_conta_superior
- conta_referencial_original
- nome_conta_superior
- caminho_hierarquico

Tabela: lancamentos
- id_lancamento
- data_lancamento
- numero_lancamento
- historico_lancamento
- valor_lancamento
- origem_registro

Tabela: partidas
- id_partida
- id_lancamento
- codigo_conta
- indicador_debito_credito
- valor
- historico_partida
- codigo_historico
- centro_custo

Tabela: saldos
- codigo_conta
- periodo
- saldo_inicial
- indicador_saldo_inicial
- total_debitos
- total_creditos
- saldo_final
- indicador_saldo_final

---

## 5. FASE 2 — NORMALIZAÇÃO DOS DADOS

### 5.1. Objetivo

Padronizar os dados para permitir análise confiável.

### 5.2. Normalizações obrigatórias

Datas:
- converter para formato ISO: YYYY-MM-DD

Valores:
- converter para decimal
- preservar sinal contábil separadamente do indicador D/C

Textos:
- remover espaços duplicados
- converter para maiúsculas
- remover acentos para análise textual
- preservar texto original para auditoria
- limpar caracteres inválidos
- normalizar abreviações comuns

Exemplos:

"FORNEC." → "FORNECEDOR"
"FORN" → "FORNECEDOR"
"NF" → "NOTA FISCAL"
"N.F." → "NOTA FISCAL"
"DUPL" → "DUPLICATA"
"PGTO" → "PAGAMENTO"
"REC" → "RECEBIMENTO"
"C/C" → "CONTA CORRENTE"
"AG." → "AGENCIA"

Contas:
- padronizar código da conta
- identificar conta superior
- montar árvore hierárquica
- separar contas sintéticas e analíticas

Débito/crédito:
- converter indicador para enum:
  - DEBITO
  - CREDITO

### 5.3. Saída da fase

Dados limpos e prontos para análise.

---

## 6. FASE 3 — MONTAGEM DO RAZÃO POR CONTA

### 6.1. Objetivo

Construir, para cada conta contábil, o conjunto completo de movimentos que explica seu comportamento.

### 6.2. Processo

Para cada conta analítica:

1. Buscar todas as partidas I250 da conta.
2. Agrupar por lançamento I200.
3. Identificar as demais contas no mesmo lançamento.
4. Tratar essas demais contas como contrapartidas prováveis.
5. Separar débitos, créditos, valores e históricos.
6. Vincular saldos do I155/I355, quando disponíveis.
7. Preservar a hierarquia do I050.

### 6.3. Atenção sobre contrapartida

Em lançamentos simples, a contrapartida é direta:

Débito: Despesa
Crédito: Fornecedor

Em lançamentos compostos, a contrapartida é indireta:

Débito: Despesa A
Débito: Despesa B
Crédito: Fornecedor X

Nesse caso, o sistema deve distribuir ou marcar como lançamento composto.

Estratégias possíveis:

- se houver uma conta no lado oposto, usar como contrapartida direta;
- se houver várias contas no lado oposto, registrar todas como contrapartidas relacionadas;
- calcular percentual de participação por valor;
- evitar inferência agressiva em lançamentos muito compostos;
- reduzir score quando a contrapartida for ambígua.

### 6.4. Saída da fase

Para cada conta:

- lista de débitos;
- lista de créditos;
- saldos;
- históricos;
- contrapartidas;
- contas relacionadas;
- meses com movimento;
- lançamentos simples;
- lançamentos compostos;
- concentração por contraparte.

---

## 7. FASE 4 — CONSTRUÇÃO DO PERFIL COMPORTAMENTAL

### 7.1. Objetivo

Transformar os movimentos da conta em métricas objetivas.

### 7.2. Métricas financeiras

Para cada conta:

- total_debitos
- total_creditos
- saldo_inicial
- saldo_final
- saldo_medio
- saldo_medio_absoluto
- quantidade_lancamentos
- quantidade_debitos
- quantidade_creditos
- percentual_debitos
- percentual_creditos
- valor_medio_lancamento
- maior_lancamento
- menor_lancamento
- meses_com_movimento
- recorrencia_mensal
- volatilidade_do_saldo
- conta_zera_no_periodo
- conta_carrega_saldo
- saldo_tipico_devedor
- saldo_tipico_credor

### 7.3. Métricas de contrapartida

Para cada conta:

- principais_contrapartidas_por_valor
- principais_contrapartidas_por_quantidade
- percentual_contra_bancos
- percentual_contra_caixa
- percentual_contra_fornecedores
- percentual_contra_clientes
- percentual_contra_receitas
- percentual_contra_despesas
- percentual_contra_estoques
- percentual_contra_imobilizado
- percentual_contra_tributos
- percentual_contra_folha
- percentual_contra_partes_relacionadas
- quantidade_de_familias_contrapartes
- concentração_top_1_contrapartida
- concentração_top_5_contrapartidas

### 7.4. Métricas textuais

A partir do nome da conta e dos históricos:

- tokens_nome_conta
- tokens_historicos
- palavras_mais_frequentes
- presença_de_nome_empresarial
- presença_de_cnpj
- presença_de_banco
- presença_de_agencia
- presença_de_conta_corrente
- presença_de_nota_fiscal
- presença_de_boleto
- presença_de_pagamento
- presença_de_recebimento
- presença_de_salario
- presença_de_imposto
- presença_de_emprestimo
- presença_de_adiantamento
- presença_de_cliente
- presença_de_fornecedor
- presença_de_estoque
- presença_de_imobilizado
- presença_de_depreciacao
- presença_de_receita
- presença_de_despesa

### 7.5. Métricas hierárquicas

A partir do plano de contas:

- grupo_pai
- grupo_avo
- caminho_hierarquico
- natureza_do_grupo_superior
- conta_analitica_ou_sintetica
- nível_da_conta
- contas_irmas
- padrão_de_nomenclatura_das_contas_irmas

### 7.6. Saída da fase

Objeto PerfilComportamentalConta:

PerfilComportamentalConta:
  codigo_conta
  nome_conta
  conta_referencial_original
  caminho_hierarquico
  metricas_financeiras
  metricas_contrapartida
  metricas_textuais
  metricas_hierarquicas
  amostra_lancamentos
  evidencias_detectadas

---

## 8. FASE 5 — DEFINIÇÃO DAS FAMÍLIAS CONTÁBEIS

### 8.1. Objetivo

Criar uma taxonomia intermediária antes de mapear para a conta referencial final.

Não tentar ir direto para o código referencial.

Primeiro identificar a família econômica da conta.

### 8.2. Macroclasses

ATIVO
PASSIVO
PATRIMONIO_LIQUIDO
RECEITA
CUSTO
DESPESA
CONTA_TRANSITORIA
CONTA_COMPENSACAO
INDEFINIDA

### 8.3. Famílias iniciais sugeridas

ATIVO:
- CAIXA
- BANCO_CONTA_MOVIMENTO
- APLICACAO_FINANCEIRA
- CLIENTES
- CARTOES_A_RECEBER
- ADIANTAMENTO_A_FORNECEDORES
- TRIBUTOS_A_RECUPERAR
- ESTOQUES
- DESPESAS_ANTECIPADAS
- EMPRESTIMOS_A_RECEBER
- PARTES_RELACIONADAS_ATIVO
- IMOBILIZADO
- INTANGIVEL
- DEPRECIACAO_ACUMULADA
- AMORTIZACAO_ACUMULADA

PASSIVO:
- FORNECEDORES
- OBRIGACOES_TRABALHISTAS
- OBRIGACOES_TRIBUTARIAS
- EMPRESTIMOS_E_FINANCIAMENTOS
- ADIANTAMENTO_DE_CLIENTES
- CONTAS_A_PAGAR
- PARTES_RELACIONADAS_PASSIVO
- PROVISOES
- PARCELAMENTOS_TRIBUTARIOS
- ARRENDAMENTOS
- DIVIDENDOS_A_PAGAR

PATRIMONIO_LIQUIDO:
- CAPITAL_SOCIAL
- RESERVAS
- LUCROS_PREJUIZOS_ACUMULADOS
- AJUSTES_AVALIACAO_PATRIMONIAL

RESULTADO:
- RECEITA_BRUTA
- DEDUCOES_DA_RECEITA
- CUSTO_MERCADORIAS
- CUSTO_SERVICOS
- DESPESAS_COMERCIAIS
- DESPESAS_ADMINISTRATIVAS
- DESPESAS_FINANCEIRAS
- RECEITAS_FINANCEIRAS
- OUTRAS_RECEITAS
- OUTRAS_DESPESAS
- IRPJ_CSLL
- FOLHA_DE_PAGAMENTO

OUTRAS:
- CONTAS_TRANSITORIAS
- CONTAS_DE_ENCERRAMENTO
- CONTAS_DE_COMPENSACAO
- CONTAS_NAO_CLASSIFICADAS

---

## 9. FASE 6 — REGRAS DETERMINÍSTICAS POR FAMÍLIA

### 9.1. Modelo geral de regra

Cada família terá:

- condições positivas;
- condições negativas;
- pesos;
- penalidades;
- score mínimo;
- evidências obrigatórias;
- evidências auxiliares.

Modelo:

RegraFamilia:
  familia
  macroclasse
  evidencias_positivas
  evidencias_negativas
  pesos
  penalidades
  score_minimo_auto
  score_minimo_revisao
  justificativas

### 9.2. Exemplo — Fornecedores

Família: FORNECEDORES
Macroclasse esperada: PASSIVO

Evidências positivas:
- saldo típico credor
- créditos contra despesas
- créditos contra estoques
- créditos contra imobilizado
- débitos contra bancos
- débitos contra caixa
- históricos com pagamento, boleto, duplicata, nota fiscal
- nome da conta parece nome empresarial
- nome contém fornecedor
- conta fica no grupo de passivo
- conta zera ou reduz após pagamentos

Pontuação sugerida:
+25 saldo típico credor
+20 créditos contra despesas/estoques/ativo
+20 débitos contra banco/caixa
+15 histórico contém NF, boleto, duplicata ou pagamento
+10 nome parece fornecedor ou razão social
+10 grupo hierárquico compatível com passivo
-30 saldo típico devedor persistente
-20 contrapartida principal com receita
-20 conta no grupo de ativo com comportamento de adiantamento
-15 histórico predominante de recebimento

Classificação:
score >= 80: FORNECEDORES com alta confiança
score 60-79: FORNECEDORES com revisão recomendada
score < 60: não classificar como fornecedor

### 9.3. Exemplo — Clientes

Família: CLIENTES
Macroclasse esperada: ATIVO

Evidências positivas:
- saldo típico devedor
- débitos contra receita
- créditos contra bancos
- créditos contra caixa
- históricos com recebimento, duplicata, cliente, venda
- nome da conta parece razão social
- conta fica no grupo de contas a receber

Pontuação sugerida:
+25 saldo típico devedor
+25 débitos contra receita
+20 créditos contra bancos/caixa
+10 históricos com recebimento/venda/cliente
+10 nome parece cliente
+10 grupo hierárquico compatível com ativo
-30 saldo credor persistente
-20 créditos contra despesas/estoques
-20 histórico predominante de pagamento

### 9.4. Exemplo — Bancos

Família: BANCO_CONTA_MOVIMENTO
Macroclasse esperada: ATIVO

Evidências positivas:
- nome contém banco
- nome contém agência
- nome contém conta corrente
- alta quantidade de contrapartidas diferentes
- movimenta contra fornecedores
- movimenta contra clientes
- movimenta contra tributos
- movimenta contra folha
- movimenta contra receitas e despesas
- alto volume de lançamentos
- saldo pode variar bastante
- conta está no ativo circulante

Pontuação sugerida:
+30 nome contém banco/agência/conta corrente
+20 grande diversidade de contrapartidas
+15 alto volume de lançamentos
+15 contrapartidas com pagamentos e recebimentos
+10 saldo patrimonial no ativo
+10 hierarquia compatível
-30 conta quase não movimenta
-20 conta tem comportamento de aplicação financeira
-20 conta tem comportamento de fornecedor ou cliente

### 9.5. Exemplo — Adiantamento a fornecedores

Família: ADIANTAMENTO_A_FORNECEDORES
Macroclasse esperada: ATIVO

Evidências positivas:
- saldo típico devedor
- nome contém adiantamento
- nome contém fornecedor
- débitos contra banco/caixa
- créditos contra fornecedores, estoques, despesas ou baixa de adiantamento
- histórico contém antecipação, adiantamento, pedido, fornecedor
- conta está no ativo circulante

Pontuação sugerida:
+25 saldo típico devedor
+25 nome/histórico contém adiantamento
+15 relação com fornecedor
+15 débitos contra banco
+10 créditos contra baixa de compras/despesas/fornecedores
+10 hierarquia compatível com ativo
-30 saldo credor persistente
-20 comportamento típico de fornecedor passivo
-20 ausência total de sinal de adiantamento

### 9.6. Exemplo — Imobilizado

Família: IMOBILIZADO
Macroclasse esperada: ATIVO_NAO_CIRCULANTE

Evidências positivas:
- saldo típico devedor
- baixa rotatividade
- débitos de aquisição
- contrapartida com fornecedores ou bancos
- nome contém móveis, utensílios, máquinas, equipamentos, veículos, instalações, computadores
- conta carrega saldo ao longo do tempo
- poucas baixas
- grupo hierárquico compatível com ativo não circulante

Pontuação sugerida:
+25 saldo devedor carregado
+20 baixa rotatividade
+20 descrição compatível com bem patrimonial
+15 aquisição contra fornecedor/banco
+10 grupo hierárquico compatível
+10 pouca recorrência mensal
-30 conta zera mensalmente
-25 comportamento típico de despesa
-20 créditos/debitos recorrentes como conta operacional

### 9.7. Exemplo — Despesas operacionais

Família: DESPESAS_OPERACIONAIS
Macroclasse esperada: RESULTADO

Evidências positivas:
- conta predominantemente debitada
- lançamentos recorrentes durante o exercício
- contrapartida com fornecedores, bancos, folha ou tributos
- saldo encerrado no fim do período
- nome contém aluguel, energia, telefone, consultoria, material, manutenção, serviços
- conta fica em grupo de resultado

Pontuação sugerida:
+25 predominância de débitos
+20 recorrência mensal
+20 contrapartida com fornecedor/banco/folha/tributo
+15 nome compatível com despesa
+10 saldo encerrado no fim do exercício
+10 hierarquia compatível com resultado
-30 saldo patrimonial carregado
-20 comportamento típico de ativo
-20 comportamento típico de passivo

### 9.8. Exemplo — Receitas

Família: RECEITA_BRUTA ou OUTRAS_RECEITAS
Macroclasse esperada: RESULTADO

Evidências positivas:
- conta predominantemente creditada
- contrapartida com clientes, caixa, bancos ou contas a receber
- históricos com venda, receita, prestação de serviço, faturamento
- saldo encerrado no fim do período
- grupo hierárquico compatível com receita

Pontuação sugerida:
+30 predominância de créditos
+25 contrapartida com clientes/bancos/caixa
+15 histórico compatível com venda ou serviço
+15 hierarquia compatível
+10 encerramento no fim do exercício
-30 saldo patrimonial carregado
-20 predominância de débitos
-20 contrapartida típica de pagamento a fornecedor

---

## 10. FASE 7 — MOTOR DE SCORE

### 10.1. Objetivo

Calcular, para cada conta, a pontuação em todas as famílias possíveis.

### 10.2. Processo

Para cada conta:

1. Carregar PerfilComportamentalConta.
2. Aplicar regra da família CAIXA.
3. Aplicar regra da família BANCO.
4. Aplicar regra da família CLIENTES.
5. Aplicar regra da família FORNECEDORES.
6. Aplicar regra da família ESTOQUE.
7. Aplicar regra da família IMOBILIZADO.
8. Aplicar todas as demais regras.
9. Gerar ranking de famílias prováveis.
10. Escolher família vencedora, se passar nos critérios mínimos.

### 10.3. Resultado esperado

Exemplo:

Conta: PARS PRODUTOS DE PROCESSAMENTO DE DADOS LTDA

Scores:
- FORNECEDORES: 87
- DESPESAS_OPERACIONAIS: 42
- CLIENTES: 18
- BANCO: 5
- IMOBILIZADO: 0

Família sugerida:
FORNECEDORES

Confiança:
ALTA

Ação:
RECLASSIFICAR, se I051 original for incompatível.

### 10.4. Critérios de decisão

score >= 80:
  classificação automática

score entre 60 e 79:
  classificação sugerida com revisão humana

score entre 40 e 59:
  baixa confiança; revisão obrigatória

score < 40:
  não classificar

Diferença entre primeiro e segundo colocado:

Se diferença >= 20 pontos:
  decisão mais segura

Se diferença < 20 pontos:
  marcar como ambígua

Exemplo:

FORNECEDORES: 72
ADIANTAMENTO_A_FORNECEDORES: 68

Resultado:
REVISÃO OBRIGATÓRIA

Motivo:
Conta pode ser fornecedor passivo ou adiantamento ativo.

---

## 11. FASE 8 — CLASSIFICAÇÃO EM CAMADAS

### 11.1. Objetivo

Evitar erro por tentar acertar diretamente o código referencial final.

### 11.2. Camadas de classificação

Camada 1:
Macroclasse

Exemplo:
ATIVO
PASSIVO
RESULTADO

Camada 2:
Grupo

Exemplo:
ATIVO_CIRCULANTE
PASSIVO_CIRCULANTE
DESPESAS_OPERACIONAIS

Camada 3:
Família

Exemplo:
FORNECEDORES
CLIENTES
BANCO
IMOBILIZADO

Camada 4:
Subfamília

Exemplo:
FORNECEDORES_NACIONAIS
FORNECEDORES_ESTRANGEIROS
FORNECEDORES_PARTES_RELACIONADAS

Camada 5:
Conta referencial final

Exemplo:
2.01.01.03.01

### 11.3. Regra importante

O sistema só deve mapear para o código referencial final quando tiver confiança suficiente nas camadas anteriores.

Se a macroclasse estiver incerta, não tentar definir subgrupo.

---

## 12. FASE 9 — MAPEAMENTO PARA CONTA REFERENCIAL

### 12.1. Objetivo

Converter a família/subfamília identificada para o plano referencial correto.

### 12.2. Tabela de mapeamento

Criar uma tabela interna:

familia_detectada
subfamilia_detectada
macroclasse
codigo_referencial_sugerido
descricao_referencial_sugerida
vigencia
observacoes

Exemplo:

FORNECEDORES
FORNECEDORES_NACIONAIS
PASSIVO_CIRCULANTE
2.01.01.03.01
Fornecedores nacionais
vigência conforme plano referencial aplicável

### 12.3. Importante

Essa camada deve ser versionada.

O plano referencial pode mudar ao longo do tempo.

Portanto, o mapeamento precisa considerar:

- ano-calendário;
- leiaute da ECD;
- plano referencial aplicável;
- tipo da entidade;
- regra tributária, se relevante.

---

## 13. FASE 10 — COMPARAÇÃO COM O I051 ORIGINAL

### 13.1. Objetivo

Identificar divergências entre a classificação informada pelo contador e a classificação sugerida pelo sistema.

### 13.2. Possíveis resultados

MANTER:
- I051 original é compatível com o comportamento da conta.

RECLASSIFICAR:
- I051 original é incompatível.
- Sistema tem alta confiança.

REVISAR:
- Sistema detectou possível erro, mas há ambiguidade.

SEM_CONCLUSAO:
- Dados insuficientes.

### 13.3. Exemplo

Conta:
ADTO A FORNECEDORES NACIONAIS

I051 original:
1.01.02.01.01

Sistema:
ADIANTAMENTO_A_FORNECEDORES

Resultado:
MANTER, se o referencial original for compatível com adiantamento ativo.

Outro exemplo:

Conta:
PAGAMENTO A FORNECEDOR X

I051 original:
1.01.02.02.01

Sistema:
FORNECEDORES_NACIONAIS

Resultado:
RECLASSIFICAR

Justificativa:
- comportamento de passivo;
- saldo credor;
- créditos contra despesas;
- débitos contra banco;
- I051 original indica ativo incompatível.

---

## 14. FASE 11 — RELATÓRIO AUDITÁVEL

### 14.1. Objetivo

Gerar uma saída defensável, revisável e explicável.

### 14.2. Estrutura do relatório por conta

Conta:
- código da conta
- nome da conta
- caminho hierárquico
- conta referencial original
- conta referencial sugerida
- família sugerida
- score
- confiança
- ação recomendada

Evidências:
- saldo típico
- percentual de débitos
- percentual de créditos
- principais contrapartidas
- principais históricos
- sinais textuais encontrados
- sinais hierárquicos
- sinais negativos

Justificativa:
Texto explicando o motivo da classificação.

Exemplo:

Conta: PARS PRODUTOS DE PROCESSAMENTO DE DADOS LTDA
Classificação original: 1.01.02.02.01
Classificação sugerida: Fornecedores nacionais
Confiança: Alta
Score: 87
Ação: Reclassificar

Justificativas:
- A conta apresenta saldo típico credor.
- 78% dos créditos ocorreram contra despesas operacionais.
- 82% dos débitos ocorreram contra contas bancárias.
- Os históricos contêm termos como pagamento, NF e boleto.
- A conta possui comportamento típico de fornecedor passivo.
- A classificação original indica ativo, incompatível com o comportamento observado.

---

## 15. FASE 12 — INTERFACE DE REVISÃO HUMANA

### 15.1. Objetivo

Permitir que um especialista valide as classificações incertas.

### 15.2. Tela recomendada

Para cada conta:

Painel esquerdo:
- conta original;
- plano hierárquico;
- I051 original;
- saldos;
- movimentos resumidos.

Painel central:
- classificação sugerida;
- score;
- explicação;
- top evidências.

Painel direito:
- lista de lançamentos amostrados;
- principais contrapartidas;
- históricos mais frequentes.

Ações:
- aprovar sugestão;
- rejeitar sugestão;
- escolher outra classificação;
- marcar como exceção;
- comentar;
- salvar precedente.

### 15.3. Resultado da revisão

Toda revisão humana deve gerar um precedente:

Precedente:
- empresa
- ano
- código da conta
- nome da conta
- classificação aprovada
- regra que sugeriu
- usuário revisor
- data da revisão
- comentário
- aplicabilidade futura

---

## 16. FASE 13 — APRENDIZADO POR PRECEDENTES

### 16.1. Objetivo

Melhorar o sistema sem perder determinismo.

### 16.2. Como fazer

As revisões humanas não devem alterar automaticamente as regras universais.

Elas devem alimentar camadas separadas:

1. Precedentes da mesma empresa
2. Precedentes do mesmo grupo econômico
3. Precedentes do mesmo setor
4. Precedentes globais, depois de validação

### 16.3. Regra

Precedente da empresa tem peso alto para aquela empresa.

Precedente global só deve ser criado quando:

- houver muitas ocorrências semelhantes;
- em empresas diferentes;
- com revisão humana confirmada;
- sem conflito relevante.

### 16.4. Exemplo

Se em uma empresa a conta "PARS PRODUTOS..." foi confirmada como fornecedor, o sistema pode sugerir fornecedor em anos seguintes da mesma empresa.

Mas não deve assumir automaticamente que "PARS PRODUTOS..." será fornecedor em todas as empresas.

---

## 17. FASE 14 — CALIBRAÇÃO SEM PERDER ESCALA

### 17.1. Princípio

As regras comportamentais são gerais.
As evidências são calculadas por empresa.
A calibração deve ser mínima.

### 17.2. Camadas

Camada universal:
- regras contábeis estruturais;
- comportamento típico de famílias;
- pesos base.

Camada setorial:
- comércio;
- indústria;
- serviços;
- holding;
- incorporação;
- financeiro;
- saúde;
- tecnologia.

Camada da empresa:
- nomes específicos;
- exceções;
- contas mal nomeadas;
- precedentes aprovados.

### 17.3. Objetivo

Evitar customização eterna por empresa.

O sistema deve funcionar bem com as regras universais e melhorar com precedentes.

---

## 18. FASE 15 — BANCO DE DADOS SUGERIDO

### 18.1. Tabelas principais

empresas
- id_empresa
- cnpj
- razao_social
- setor
- regime
- grupo_economico

ecd_arquivos
- id_ecd
- id_empresa
- ano
- periodo_inicio
- periodo_fim
- leiaute
- hash_arquivo
- data_importacao

contas
- id_conta
- id_ecd
- codigo_conta
- nome_conta
- nome_normalizado
- tipo_conta
- nivel
- codigo_conta_superior
- caminho_hierarquico
- natureza_informada

contas_referenciais_originais
- id
- id_conta
- codigo_referencial_original
- fonte
- data_vinculo

lancamentos
- id_lancamento
- id_ecd
- numero_lancamento
- data_lancamento
- historico
- valor_total

partidas
- id_partida
- id_lancamento
- id_conta
- indicador_dc
- valor
- historico
- centro_custo

saldos
- id_saldo
- id_conta
- periodo
- saldo_inicial
- indicador_inicial
- total_debitos
- total_creditos
- saldo_final
- indicador_final

perfis_conta
- id_perfil
- id_conta
- metricas_json
- criado_em

scores_classificacao
- id_score
- id_conta
- familia
- score
- evidencias_json
- penalidades_json

classificacoes_sugeridas
- id_classificacao
- id_conta
- familia
- subfamilia
- codigo_referencial_sugerido
- score
- confianca
- acao
- justificativa

revisoes_humanas
- id_revisao
- id_classificacao
- usuario
- decisao
- classificacao_final
- comentario
- data_revisao

precedentes
- id_precedente
- id_empresa
- setor
- padrao_conta
- familia_confirmada
- classificacao_confirmada
- origem
- peso
- status

regras
- id_regra
- familia
- versao
- definicao_json
- ativa
- criada_em

---

## 19. FASE 16 — API INTERNA SUGERIDA

### 19.1. Endpoints

POST /ecd/importar
- recebe arquivo ECD
- processa parser
- grava estrutura

POST /ecd/{id}/normalizar
- executa limpeza e padronização

POST /ecd/{id}/montar-razao
- monta razão por conta

POST /ecd/{id}/gerar-perfis
- calcula perfil comportamental

POST /ecd/{id}/classificar
- aplica regras e gera scores

GET /ecd/{id}/contas
- lista contas analisadas

GET /contas/{id}/perfil
- retorna perfil comportamental da conta

GET /contas/{id}/classificacao
- retorna classificação sugerida

POST /classificacoes/{id}/revisar
- aprova, rejeita ou altera classificação

GET /relatorios/reclassificacao/{id_ecd}
- gera relatório consolidado

---

## 20. FASE 17 — PIPELINE TÉCNICO

Pipeline recomendado:

1. upload_ecd
2. validar_arquivo
3. parsear_registros
4. estruturar_tabelas
5. normalizar_dados
6. montar_arvore_plano_contas
7. montar_lancamentos_e_partidas
8. montar_razao_por_conta
9. calcular_saldos_e_metricas
10. gerar_perfil_comportamental
11. aplicar_regras_familias
12. calcular_scores
13. selecionar_classificacao_vencedora
14. mapear_referencial
15. comparar_com_i051
16. gerar_justificativa
17. salvar_resultado
18. enviar_para_revisao_quando_necessario
19. registrar_precedentes
20. exportar_relatorio

---

## 21. FASE 18 — ORDEM IDEAL DE IMPLEMENTAÇÃO

### Sprint 1 — Parser e estrutura básica

Objetivo:
Ler a ECD e montar as tabelas principais.

Entregáveis:
- parser de I050;
- parser de I051;
- parser de I200;
- parser de I250;
- parser de I155;
- armazenamento estruturado;
- validação básica de integridade.

Critério de sucesso:
Conseguir importar uma ECD real e listar contas, lançamentos, partidas e saldos.

---

### Sprint 2 — Razão por conta

Objetivo:
Montar a visão comportamental bruta de cada conta.

Entregáveis:
- razão por conta;
- débitos por conta;
- créditos por conta;
- contrapartidas por lançamento;
- identificação de lançamentos simples e compostos;
- amostra de históricos.

Critério de sucesso:
Dada uma conta, o sistema mostra seus movimentos e principais contrapartidas.

---

### Sprint 3 — Métricas comportamentais

Objetivo:
Transformar o razão em métricas objetivas.

Entregáveis:
- total de débitos;
- total de créditos;
- saldo típico;
- percentual D/C;
- recorrência;
- concentração de contrapartidas;
- palavras frequentes;
- sinais textuais;
- sinais hierárquicos.

Critério de sucesso:
Cada conta tem um PerfilComportamentalConta completo.

---

### Sprint 4 — Primeiras famílias contábeis

Objetivo:
Criar regras para as famílias mais importantes.

Começar com:
- BANCO_CONTA_MOVIMENTO
- FORNECEDORES
- CLIENTES
- ADIANTAMENTO_A_FORNECEDORES
- IMOBILIZADO
- DESPESAS_OPERACIONAIS
- RECEITAS

Critério de sucesso:
Classificar corretamente a maior parte das contas óbvias.

---

### Sprint 5 — Motor de score

Objetivo:
Aplicar todas as regras e gerar ranking de famílias.

Entregáveis:
- score por família;
- ranking;
- confiança;
- diferença entre primeiro e segundo colocado;
- ação recomendada.

Critério de sucesso:
Sistema diferencia classificação automática, sugestão e revisão obrigatória.

---

### Sprint 6 — Mapeamento referencial

Objetivo:
Converter família/subfamília para conta referencial.

Entregáveis:
- tabela de mapeamento;
- versionamento por ano/leiaute;
- comparação com I051 original;
- indicação de divergência.

Critério de sucesso:
Sistema aponta quais contas devem manter ou alterar o referencial.

---

### Sprint 7 — Relatório auditável

Objetivo:
Gerar relatório de reclassificação.

Entregáveis:
- relatório por conta;
- relatório consolidado;
- exportação Excel/CSV;
- justificativas;
- evidências.

Critério de sucesso:
Um contador ou auditor consegue revisar a sugestão sem olhar o código.

---

### Sprint 8 — Interface de revisão

Objetivo:
Permitir validação humana.

Entregáveis:
- tela de revisão;
- aprovação/rejeição;
- edição da classificação;
- comentário;
- registro de precedente.

Critério de sucesso:
Revisões viram dados reaproveitáveis.

---

### Sprint 9 — Precedentes e calibração

Objetivo:
Melhorar a performance por empresa e setor.

Entregáveis:
- precedentes por empresa;
- precedentes por grupo;
- precedentes setoriais;
- pesos adicionais;
- controle de conflito.

Critério de sucesso:
Sistema melhora em novas ECDs da mesma empresa sem perder controle.

---

### Sprint 10 — Expansão de famílias

Objetivo:
Cobrir a maior parte do plano de contas.

Adicionar regras para:
- tributos a recolher;
- tributos a recuperar;
- folha;
- empréstimos;
- aplicações financeiras;
- estoques;
- partes relacionadas;
- provisões;
- contas transitórias;
- patrimônio líquido;
- custos;
- despesas financeiras;
- receitas financeiras.

Critério de sucesso:
Cobertura relevante do plano inteiro, com baixa taxa de falso positivo.

---

## 22. FASE 19 — MÉTRICAS DE QUALIDADE DO SISTEMA

### 22.1. Métricas principais

Taxa de classificação automática:
- percentual de contas classificadas com score alto.

Taxa de revisão:
- percentual de contas enviadas para revisão humana.

Taxa de acerto:
- percentual de sugestões aprovadas pelo revisor.

Taxa de divergência real:
- percentual de I051 original considerado incompatível.

Taxa de falso positivo:
- sistema sugeriu reclassificação, mas revisor rejeitou.

Taxa de falso negativo:
- sistema manteve classificação, mas revisor alterou.

Cobertura por valor:
- percentual do valor movimentado coberto por classificações confiáveis.

Cobertura por quantidade:
- percentual de contas classificadas.

### 22.2. Métrica mais importante

Não medir apenas quantidade de contas.

Medir também materialidade.

Uma conta irrelevante com R$ 100 de movimento não pode ter o mesmo peso operacional de uma conta com R$ 10 milhões.

---

## 23. FASE 20 — REGRAS DE SEGURANÇA

### 23.1. O sistema não deve reclassificar automaticamente quando:

- score abaixo do mínimo;
- diferença pequena entre duas famílias;
- conta com comportamento ambíguo;
- conta com poucos lançamentos;
- conta com saldo relevante e baixa evidência;
- lançamento composto demais;
- histórico genérico demais;
- conta sintética;
- conta de encerramento;
- conta transitória;
- conta com comportamento diferente entre períodos;
- conta com classificação sensível, como tributos, partes relacionadas ou patrimônio líquido.

### 23.2. Regra de ouro

Melhor mandar para revisão do que classificar errado com confiança falsa.

---

## 24. FASE 21 — EXEMPLO DE FLUXO PARA UMA CONTA

Conta:
PARS PRODUTOS DE PROCESSAMENTO DE DADOS LTDA

1. Sistema lê I050:
   nome da conta = PARS PRODUTOS DE PROCESSAMENTO DE DADOS LTDA

2. Sistema lê I051:
   classificação original = 1.01.02.02.01

3. Sistema busca I250:
   encontra todos os lançamentos da conta.

4. Sistema monta razão:
   créditos contra despesas operacionais;
   débitos contra banco;
   saldo credor recorrente.

5. Sistema calcula perfil:
   saldo típico = credor
   percentual débitos contra banco = 82%
   percentual créditos contra despesas = 76%
   histórico contém pagamento/NF/boleto
   nome parece razão social

6. Sistema aplica regras:
   FORNECEDORES = 87
   CLIENTES = 12
   DESPESAS = 30
   BANCO = 0

7. Sistema escolhe:
   família = FORNECEDORES

8. Sistema mapeia:
   subfamília = FORNECEDORES_NACIONAIS
   referencial sugerido = passivo circulante / fornecedores nacionais

9. Sistema compara:
   I051 original parece ativo
   comportamento parece passivo

10. Resultado:
   ação = RECLASSIFICAR
   confiança = ALTA

11. Relatório:
   explicar evidências e mostrar lançamentos de suporte.

---

## 25. RISCO PRINCIPAL DO PROJETO

O maior risco não é técnico.

O maior risco é conceitual:

Tentar transformar uma classificação contábil complexa em uma simples busca por palavra-chave.

Isso precisa ser evitado.

Palavra-chave ajuda, mas não decide sozinha.

A decisão deve vir do conjunto:

nome da conta
+ hierarquia
+ saldo
+ débitos
+ créditos
+ contrapartidas
+ históricos
+ recorrência
+ materialidade
+ precedentes

---

## 26. MVP RECOMENDADO

### 26.1. Escopo do MVP

Ler uma ECD completa e classificar apenas 7 famílias:

1. Bancos
2. Clientes
3. Fornecedores
4. Adiantamento a fornecedores
5. Imobilizado
6. Despesas operacionais
7. Receitas

### 26.2. Por que começar assim

Essas famílias têm comportamento bem característico.

Elas permitem validar rapidamente se a tese funciona.

### 26.3. Saída do MVP

Para cada conta:

- família sugerida;
- score;
- classificação original;
- divergência;
- justificativa;
- revisão necessária ou não.

### 26.4. Critério de sucesso do MVP

O MVP será bem-sucedido se:

- classificar corretamente contas óbvias;
- identificar divergências claras;
- evitar classificação forçada em casos ambíguos;
- produzir justificativas compreensíveis;
- permitir revisão humana;
- gerar aprendizado para a próxima ECD.

---

## 27. CONCLUSÃO TÉCNICA

O sistema deve ser construído como um motor contábil de evidências.

A sequência correta é:

1. Não confiar no I051.
2. Ler a ECD inteira.
3. Montar o razão por conta.
4. Calcular o perfil comportamental.
5. Aplicar regras por família.
6. Gerar score.
7. Mapear para o referencial.
8. Comparar com a classificação original.
9. Explicar a divergência.
10. Submeter incertezas à revisão humana.

A frase que deve guiar a implementação é:

"Classificação contábil confiável nasce do comportamento da conta, não apenas do nome da conta."