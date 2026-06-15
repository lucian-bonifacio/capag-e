# MANUAL 2 – ORIENTAÇÃO TÉCNICA PARA AUTOMAÇÃO DO CÁLCULO DO PLR E CAPAG-e PELA ECD

## 1\. OBJETIVO DO MANUAL

O presente manual tem por objetivo orientar o desenvolvimento de uma automação destinada à leitura da Escrituração Contábil Digital – ECD, identificação das contas contábeis vinculadas ao Plano de Contas Referencial da Receita Federal e cálculo automatizado do Patrimônio Líquido Realizável Econômico – PLR.

A metodologia proposta busca construir um diagnóstico econômico-financeiro prudencial aderente à lógica de análise de capacidade de pagamento utilizada pela Procuradoria-Geral da Fazenda Nacional – PGFN em procedimentos de transação tributária e análise econômico-financeira.

O objetivo principal da automação será:

1. Ler a ECD;

2. Identificar os saldos finais anuais das contas contábeis;

3. Relacionar as contas da empresa ao plano referencial da Receita Federal;

4. Aplicar regras de hierarquia para evitar duplicidade;

5. Agrupar contas conforme a metodologia do PLR;

6. Aplicar regras de realizabilidade econômica;

7. Aplicar deságios prudenciais baseados nos CPCs;

8. Apurar automaticamente o PLR;

9. Somar o FCO informado manualmente;

10. Apurar a CAPAG-e.

O sistema deverá operar com rastreabilidade completa, permitindo auditoria integral da origem de cada saldo utilizado.

---

# 2\. BASE NORMATIVA E METODOLÓGICA

## 2.1. Base da metodologia

A metodologia foi estruturada com fundamento:

• na Portaria PGFN nº 6.757/2022; • na metodologia econômico-financeira utilizada pela PGFN para análise de capacidade de pagamento; • no Manual da ECD e leiaute do SPED Contábil; • no Plano de Contas Referencial da Receita Federal; • na NBC TG 46 / CPC 46 – Mensuração do Valor Justo; • na NBC TG 01 / CPC 01 – Redução ao Valor Recuperável de Ativos; • na NBC TG 25 / CPC 25 – Provisões, Passivos Contingentes e Ativos Contingentes.

---

## 2.2. Premissa econômica da metodologia

O PLR não representa o patrimônio líquido contábil puro.

O PLR representa uma estimativa prudencial do patrimônio economicamente realizável da empresa.

Portanto:

• ativos sem liquidez efetiva poderão sofrer deságio; • ativos sem capacidade de conversão econômica poderão ser excluídos; • passivos sem exigibilidade econômica efetiva poderão ser desconsiderados; • contas meramente operacionais ou de competência poderão ser excluídas.

A lógica da metodologia é aproximar o cálculo da capacidade econômica efetiva da empresa.

---

# 3\. REGISTROS DA ECD QUE DEVEM SER UTILIZADOS

A automação deverá obrigatoriamente utilizar os registros abaixo.

## 3.1. Registro I050 – Plano de Contas da Empresa

Finalidade:

Identificar:

• código da conta da empresa; • descrição da conta; • natureza; • nível hierárquico; • estrutura da conta; • conta analítica; • conta sintética.

Campos principais utilizados:

• COD\_CTA; • COD\_NAT; • IND\_CTA; • NIVEL; • NOME\_CTA.

Função operacional:

O I050 será a base principal para identificação da estrutura hierárquica do plano de contas.

A automação deverá:

1. Ler todas as contas do I050;

2. Identificar contas analíticas;

3. Identificar contas sintéticas;

4. Montar árvore hierárquica das contas;

5. Vincular posteriormente ao I051.

---

## 3.2. Registro I051 – Plano de Contas Referencial

Finalidade:

Relacionar o plano de contas da empresa ao Plano de Contas Referencial da Receita Federal.

Campos principais:

• COD\_CTA; • COD\_CTA\_REF.

IMPORTANTE:

O registro I155 normalmente NÃO contém o código referencial.

Portanto:

A automação deverá:

1. localizar o saldo no I155;

2. localizar a conta correspondente no I050;

3. localizar o vínculo da conta no I051;

4. obter o código referencial vinculado.

Fluxo obrigatório:

I155 → COD\_CTA → I050 → I051 → COD\_CTA\_REF.

Caso a conta do I155 não possua vínculo no I051:

• marcar como “sem classificação referencial”; • não incluir automaticamente no cálculo; • gerar alerta de validação manual.

---

## 3.3. Registro I150 – Saldos Periódicos

Finalidade:

Identificar os períodos de encerramento dos saldos.

A automação deverá:

1. localizar o período encerrado em 31/12;

2. utilizar exclusivamente o encerramento anual;

3. ignorar períodos intermediários.

Regra obrigatória:

NUNCA somar:

• saldos trimestrais; • saldos mensais; • saldos intermediários.

Deve ser utilizado exclusivamente:

• o saldo final anual encerrado em 31/12.

---

## 3.4. Registro I155 – Detalhamento dos Saldos das Contas

Este é o principal registro operacional do cálculo.

Finalidade:

Capturar o saldo final das contas contábeis.

Campos principais:

• COD\_CTA; • VL\_SLD\_FIN; • IND\_DC\_FIN.

Função operacional:

A automação deverá:

1. localizar o saldo final da conta;

2. verificar se o saldo é devedor ou credor;

3. aplicar o sinal correto;

4. vincular a conta ao I050;

5. localizar o código referencial via I051.

IMPORTANTE:

O sistema não poderá utilizar:

• totalizadores do Balanço; • contas sintéticas; • agrupamentos automáticos; • registros consolidados.

O cálculo deverá ocorrer exclusivamente a partir das contas analíticas válidas.

---

## 3.5. Registro J100 – Balanço Patrimonial

O registro J100 deverá ser utilizado apenas para:

• conferência; • validação; • auditoria; • cruzamento de consistência.

O J100 NÃO poderá ser utilizado como fonte principal do cálculo.

Motivo:

O J100 apresenta demonstrativos consolidados.

A utilização direta poderá gerar:

• duplicidade; • soma de contas sintéticas; • perda da granularidade necessária.

---

# 4\. REGRA DE HIERARQUIA DAS CONTAS

## 4.1. Regra obrigatória

A automação deverá utilizar sempre o menor nível disponível com saldo.

Regra operacional:

1. Se houver conta filha com saldo, ignorar a conta pai;

2. Nunca somar conta pai com conta filha;

3. Utilizar exclusivamente contas analíticas válidas;

4. Aplicar prioridade pelo menor nível.

---

## 4.2. Exemplo operacional

Conta pai:

2.1.2.01 – Fornecedores

Contas filhas:

2.1.2.01.01 – Fornecedores Nacionais 2.1.2.01.02 – Fornecedores Estrangeiros

Se existirem saldos nas contas filhas:

A conta pai deverá ser ignorada.

---

# 5\. CONCEITO DO PLR ECONÔMICO

## 5.1. Definição

O Patrimônio Líquido Realizável Econômico – PLR representa uma estimativa prudencial da capacidade patrimonial economicamente realizável da empresa.

O cálculo NÃO representa:

• patrimônio líquido societário; • patrimônio líquido contábil puro; • valor de liquidação judicial.

O objetivo é estimar:

• capacidade econômica efetiva; • potencial patrimonial realizável; • solvência econômica prudencial.

---

# 6\. FÓRMULA DO PLR

## 6.1. Fórmula-base

PLR \= Ativos Realizáveis Ajustados – Passivos Econômicos Exigíveis

Onde:

Ativos Realizáveis Ajustados \= ativos com capacidade econômica de conversão em caixa após aplicação dos deságios prudenciais.

Passivos Econômicos Exigíveis \= passivos financeiros e obrigações economicamente exigíveis.

---

## 6.2. Fórmula da CAPAG-e

CAPAG-e \= FCO \+ PLR

Onde:

• FCO \= Fluxo de Caixa Operacional Ajustado; • PLR \= Patrimônio Líquido Realizável.

O FCO será informado manualmente pelo usuário.

---

# 7\. REGRAS DE DESÁGIO PRUDENCIAL

## 7.1. Fundamentação técnica

Os deságios deverão observar:

• CPC 46 – Valor Justo; • CPC 01 – Valor Recuperável; • prudência econômica; • realizabilidade efetiva.

A automação NÃO deverá aplicar automaticamente os percentuais.

Os percentuais deverão ser parametrizáveis.

---

## 7.2. Sugestão de deságios padrão

| Grupo | Deságio sugerido |
| :---- | :---- |
| Caixa | 0% |
| Bancos | 0% |
| Aplicações imediatas | 0% a 5% |
| Clientes | 10% a 30% |
| Adiantamentos | 20% a 50% |
| Estoques | 20% a 80% |
| Imobilizado | 40% a 80% |
| Intangível | 80% a 100% |
| Créditos judiciais | 30% a 90% |

Os percentuais deverão permanecer editáveis.

---

# 8\. REGRAS DE EXCLUSÃO AUTOMÁTICA

## 8.1. Não incluir automaticamente

A automação deverá excluir por padrão:

• tributos a recuperar; • IRPJ diferido; • CSLL diferida; • depósitos judiciais; • intangível; • goodwill; • despesas antecipadas; • prejuízo fiscal; • base negativa; • ativos sem realizabilidade econômica.

---

# 9\. REGRAS DOS PASSIVOS

## 9.1. Passivos automaticamente considerados

Devem ser incluídos automaticamente:

• empréstimos; • financiamentos; • debêntures; • fornecedores; • prestadores; • salários; • INSS; • FGTS; • parcelamentos; • contingências prováveis; • arrendamentos financeiros.

---

## 9.2. Passivos condicionais

Devem exigir validação manual:

• partes relacionadas; • mútuos com sócios; • receitas antecipadas; • provisões gerenciais; • derivativos; • multas; • passivos sem exigibilidade comprovada.

---

# 10\. TABELA DE CONTAS PARA PARAMETRIZAÇÃO

## 10.1. Estrutura da tabela

A tabela deverá possuir obrigatoriamente:

Grupo metodologia | Macrogrupo | Código Referencial | Descrição Referencial |

---

# 10.2. TABELA DE CONTAS – ATIVO CIRCULANTE

| Grupo metodologia | Macrogrupo | Código Referencial | Descrição Referencial |
| :---- | :---- | :---- | :---- |
| Ativo Circulante | Disponibilidades | 1.1.1.01.01.001 | Fundo Fixo |
| Ativo Circulante | Disponibilidades | 1.1.1.01.02.001 | Valores a Depositar |
| Ativo Circulante | Disponibilidades | 1.1.1.01.99.001 | Outros Numerários Disponíveis |
| Ativo Circulante | Direitos a Receber | 1.1.3.01.01.001 | Títulos a Receber |
| Ativo Circulante | Direitos a Receber | 1.1.3.01.06.002 | Cartão Próprio |
| Ativo Circulante | Direitos a Receber | 1.1.3.02.02.001 | Receitas de Eventos |
| Ativo Circulante | Direitos a Receber | 1.1.3.03.01.001 | Abertura por Parte Relacionada |
| Ativo Circulante | Adiantamentos | 1.1.6.01.03.001 | Adiantamentos a Fornecedores |
| Ativo Circulante | Adiantamentos | 1.1.6.01.03.002 | Valores a Recuperar de Fornecedores |
| Ativo Circulante | Outros Créditos | 1.1.6.02.01.001 | Indenizações a Receber |
| Ativo Circulante | Outros Créditos | 1.1.6.02.99.999 | Outros Valores a Receber |

---

# 10.3. TABELA DE CONTAS – ATIVO NÃO CIRCULANTE

| Grupo metodologia | Macrogrupo | Código Referencial | Descrição Referencial |
| :---- | :---- | :---- | :---- |
| Ativo Não Circulante | Realizável LP | 1.2.1.03.01.001 | Títulos a Receber de Clientes |
| Ativo Não Circulante | Realizável LP | 1.2.1.03.99.001 | Outros Créditos e Valores |
| Ativo Não Circulante | Imobilizado | 1.2.3.04.01.001 | Móveis e Utensílios |
| Ativo Não Circulante | Imobilizado | 1.2.3.04.01.002 | Máquinas e Equipamentos |
| Ativo Não Circulante | Imobilizado | 1.2.3.04.01.004 | Prédios e Benfeitorias |
| Ativo Não Circulante | Imobilizado | 1.2.3.04.01.005 | Terrenos |
| Ativo Não Circulante | Imobilizado | 1.2.3.04.01.008 | Computadores e Periféricos |
| Ativo Não Circulante | Imobilizado | 1.2.3.04.01.010 | Veículos |
| Ativo Não Circulante | Ativos Mantidos para Venda | 1.2.6.01.01.001 | Ativos Não Circulantes Mantidos para Venda |

---

# 10.4. TABELA DE CONTAS – PASSIVO CIRCULANTE

| Grupo metodologia | Macrogrupo | Código Referencial | Descrição Referencial |
| :---- | :---- | :---- | :---- |
| Passivo Circulante | Empréstimos e Financiamentos | 2.1.1.01.01.001 | Abertura por Instituição Financeira |
| Passivo Circulante | Empréstimos e Financiamentos | 2.1.1.01.05.001 | Arrendamento Mercantil Financeiro |
| Passivo Circulante | Debêntures | 2.1.1.03.01.001 | Debêntures Conversíveis em Ações |
| Passivo Circulante | CCB | 2.1.1.04.01.001 | Cédula de Crédito Bancário |
| Passivo Circulante | Fornecedores | 2.1.2.01.01.001 | Fornecedores Nacionais |
| Passivo Circulante | Fornecedores | 2.1.2.01.02.001 | Fornecedores Estrangeiros |
| Passivo Circulante | Prestadores | 2.1.2.01.04.001 | Prestadores de Serviços |
| Passivo Circulante | Trabalhistas | 2.1.2.05.01.001 | Salários a Pagar |
| Passivo Circulante | Trabalhistas | 2.1.2.05.01.002 | Férias a Pagar |
| Passivo Circulante | Trabalhistas | 2.1.2.05.01.003 | 13º Salário a Pagar |
| Passivo Circulante | Previdenciárias | 2.1.2.05.02.001 | INSS a Recolher |
| Passivo Circulante | Previdenciárias | 2.1.2.05.02.002 | FGTS a Recolher |
| Passivo Circulante | Contingências Prováveis | 2.1.2.13.01.001 | Contingências Cíveis |
| Passivo Circulante | Contingências Prováveis | 2.1.2.13.01.002 | Contingências Tributárias |
| Passivo Circulante | Contingências Prováveis | 2.1.2.13.01.003 | Contingências Trabalhistas |

---

# 10.5. TABELA DE CONTAS – PASSIVO NÃO CIRCULANTE

| Grupo metodologia | Macrogrupo | Código Referencial | Descrição Referencial |
| :---- | :---- | :---- | :---- |
| Passivo Não Circulante | Empréstimos LP | 2.2.1.01.01.001 | Abertura por Instituição Financeira |
| Passivo Não Circulante | Empréstimos LP | 2.2.1.01.05.001 | Arrendamento Mercantil Financeiro |
| Passivo Não Circulante | Debêntures LP | 2.2.1.03.01.001 | Debêntures Conversíveis em Ações |
| Passivo Não Circulante | CCB LP | 2.2.1.04.01.001 | Cédula de Crédito Bancário |
| Passivo Não Circulante | Fornecedores LP | 2.2.1.05.01.001 | Fornecedores Nacionais |
| Passivo Não Circulante | Prestadores LP | 2.2.1.05.04.001 | Prestadores de Serviços |
| Passivo Não Circulante | Contingências LP | 2.2.1.10.01.001 | Contingências Cíveis |
| Passivo Não Circulante | Contingências LP | 2.2.1.10.02.001 | Contingências Tributárias |
| Passivo Não Circulante | Contingências LP | 2.2.1.10.03.001 | Contingências Trabalhistas |

---

# 11\. FLUXO OPERACIONAL DA AUTOMAÇÃO

## 11.1. Etapa 1 – Leitura da ECD

A automação deverá:

1. importar o arquivo da ECD;

2. identificar os registros;

3. separar os registros I050, I051, I150, I155 e J100.

---

## 11.2. Etapa 2 – Estrutura hierárquica

A automação deverá:

1. montar a árvore das contas;

2. identificar contas pai;

3. identificar contas filhas;

4. identificar contas analíticas.

---

## 11.3. Etapa 3 – Captura dos saldos

A automação deverá:

1. localizar o encerramento anual no I150;

2. capturar os saldos do I155;

3. aplicar sinal correto;

4. eliminar duplicidades.

---

## 11.4. Etapa 4 – Vínculo referencial

A automação deverá:

1. localizar a conta no I050;

2. localizar o vínculo no I051;

3. identificar o código referencial.

---

## 11.5. Etapa 5 – Aplicação da metodologia

A automação deverá:

1. classificar as contas;

2. agrupar por macrogrupo;

3. aplicar deságios;

4. excluir contas vedadas;

5. apurar o PLR.

---

## 11.6. Etapa 6 – CAPAG-e

A automação deverá:

1. receber o FCO manual;

2. somar ao PLR;

3. gerar o resultado da CAPAG-e.

---

# 12\. LOG DE AUDITORIA OBRIGATÓRIO

O sistema deverá manter log completo contendo:

• código da conta da empresa; • descrição da conta; • código referencial; • descrição referencial; • saldo final; • natureza; • grupo metodológico; • regra aplicada; • deságio aplicado; • motivo de exclusão; • indicação de conta pai ignorada.

---

# 13\. REGRAS DE SEGURANÇA DO CÁLCULO

A automação NÃO poderá:

• somar contas sintéticas; • utilizar totalizadores do Balanço; • somar conta pai e filha; • utilizar J100 como fonte principal; • duplicar saldos; • utilizar contas sem vínculo validado; • incluir ativos sem realizabilidade econômica; • incluir passivos sem exigibilidade econômica.

---

# 14\. RESULTADO FINAL DA AUTOMAÇÃO

O sistema deverá gerar:

1. memória de cálculo;

2. PLR bruto;

3. PLR ajustado;

4. CAPAG-e;

5. log técnico;

6. rastreabilidade integral da origem dos saldos;

7. relatório de inconsistências;

8. relatório de contas sem vínculo referencial.

O objetivo da automação não é substituir a análise técnica.

O objetivo é estruturar uma base padronizada, auditável e economicamente coerente para suporte à análise de capacidade de pagamento.