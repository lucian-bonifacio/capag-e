**MANUAL DE ORIENTAÇÃO PARA DESENVOLVIMENTO — MOTOR DE FLUXO OPERACIONAL UNIVERSAL (ECD)**

**1\. OBJETIVO DA AUTOMAÇÃO**

Este motor tem por objetivo construir automaticamente um **diagnóstico econômico-operacional padronizado**, utilizando informações extraídas da **ECD**.

O cálculo deverá ser **independente da atividade econômica da empresa**, funcionando para:

* indústria; 

* comércio; 

* serviços; 

* construção civil; 

* transportadoras; 

* tecnologia; 

* locação; 

* holdings; 

* marketing; 

* Zona Franca de Manaus; 

* demais segmentos. 

O sistema deverá eliminar dependência de nomes livres do plano societário da empresa.

Toda classificação deverá ocorrer através do **Plano de Contas Referencial da Receita Federal**.

---

**2\. DOCUMENTOS-FONTE UTILIZADOS**

O motor utilizará exclusivamente informações oriundas da **ECD**.

Registros obrigatórios:

| Registro ECD | Finalidade |
| :---- | :---- |
| **I050** | identificar plano contábil da empresa, código da conta, natureza, descrição, nível hierárquico |
| **I051** | identificar vínculo entre conta societária e conta referencial |
| **I150** | localizar o período do saldo |
| **I155** | capturar saldo final das contas |
| **J150** | conferência da DRE consolidada |

---

**3\. REGRA TEMPORAL OBRIGATÓRIA**

A automação deverá utilizar:

**EXCLUSIVAMENTE saldo anual encerrado em 31/12**

Critérios obrigatórios:

✔ utilizar saldo final anual.

Não utilizar:

❌ saldos trimestrais;

❌ saldos mensais;

❌ acumulados intermediários;

❌ somatórios de períodos.

---

**Exemplo:**

Se o arquivo possuir:

* 31/03; 

* 30/06; 

* 30/09; 

* 31/12. 

O motor deverá capturar somente:

**31/12.**

---

**4\. REGRA DE HIERARQUIA — PREVENÇÃO DE DUPLICIDADE**

A ECD pode apresentar contas pai e contas filhas simultaneamente.

Para evitar duplicidade, o motor deverá seguir obrigatoriamente a seguinte regra:

**REGRA PRINCIPAL**

**Sempre utilizar o menor nível disponível com saldo.**

---

**REGRA OPERACIONAL**

**Passo 1**

Verificar existência de contas filhas vinculadas ao mesmo macrogrupo.

**Passo 2**

Se houver contas filhas com saldo:

→ utilizar as filhas.

→ ignorar a conta pai.

**Passo 3**

Se não houver contas filhas:

→ utilizar a conta pai.

---

**Exemplo**

Situação:

| Conta | Saldo |
| :---- | :---- |
| 3.01.01.07 | 100.000 |
| 3.01.01.07.01.02 | 70.000 |
| 3.01.01.07.01.05 | 30.000 |

Resultado correto:

Capturar:

✔ 3.01.01.07.01.02

✔ 3.01.01.07.01.05

Ignorar:

❌ 3.01.01.07

---

O sistema nunca poderá somar simultaneamente conta pai e filha.

---

**5\. LÓGICA DE EXTRAÇÃO DOS DADOS**

Fluxo obrigatório:

**Etapa 1 — Ler I050**

Capturar:

* código conta empresa; 

* descrição conta; 

* natureza; 

* nível hierárquico. 

---

**Etapa 2 — Ler I051**

Mapear:

**Conta societária → Conta referencial Receita Federal**

---

**Etapa 3 — Ler I150**

Identificar:

**encerramento anual 31/12.**

---

**Etapa 4 — Ler I155**

Capturar:

**saldo final da conta no exercício.**

---

**Etapa 5 — Aplicar regra hierárquica.**

---

**Etapa 6 — Agrupar por:**

* Grupo metodologia; 

* Macrogrupo. 

---

**6\. METODOLOGIA DO MOTOR DE FLUXO OPERACIONAL**

O motor deverá transformar a DRE em um **modelo universal de geração operacional de caixa**.

---

**BLOCO 1 — RECEITA OPERACIONAL**

**(+) Receita Bruta Operacional**

Inclui:

* venda de produtos; 

* venda de mercadorias; 

* prestação de serviços; 

* locação; 

* construção; 

* receitas operacionais. 

---

**(-) Deduções da Receita**

Inclui:

* devoluções; 

* cancelamentos; 

* descontos; 

* abatimentos; 

* glosas. 

---

**(-) Tributos sobre Receita**

Inclui:

* ICMS; 

* ISS; 

* IPI sobre vendas; 

* PIS; 

* COFINS; 

* demais tributos incidentes sobre faturamento. 

---

**Fórmula:**

**Receita Operacional Líquida \=**

Receita Bruta

− Deduções

− Tributos.

---

**BLOCO 2 — CUSTOS OPERACIONAIS**

Inclui:

* CPV; 

* CMV; 

* CSP; 

* custos industriais; 

* custos de prestação; 

* custos de produção; 

* materiais; 

* insumos; 

* logística; 

* fretes; 

* tecnologia operacional; 

* serviços operacionais. 

---

**BLOCO 3 — DESPESAS OPERACIONAIS**

**Pessoal**

Inclui:

* salários; 

* encargos; 

* benefícios; 

* pró-labore; 

* bônus. 

---

**Administrativas**

Inclui:

* aluguel; 

* condomínio; 

* escritório; 

* jurídico; 

* contabilidade; 

* consultorias; 

* utilities. 

---

**Comerciais**

Inclui:

* publicidade; 

* propaganda; 

* marketing; 

* vendas; 

* comissões. 

---

**Tecnologia**

Inclui:

* software; 

* ERP; 

* licenças; 

* telecom; 

* cloud; 

* internet. 

---

**Outras despesas operacionais**

Inclui:

* provisões operacionais; 

* perdas operacionais; 

* demais despesas de operação. 

---

**BLOCO 4 — RESULTADO FINANCEIRO**

**Receitas Financeiras**

Inclui:

* juros ativos; 

* aplicações; 

* rendimentos; 

* ganhos financeiros. 

---

**Despesas Financeiras**

Inclui:

* juros passivos; 

* IOF; 

* tarifas; 

* despesas bancárias; 

* variações cambiais passivas; 

* encargos financeiros. 

---

**BLOCO 5 — RESULTADO NÃO OPERACIONAL**

Inclui:

* ganhos extraordinários; 

* perdas extraordinárias; 

* receitas não recorrentes; 

* despesas não recorrentes. 

---

**7\. FÓRMULA DO CÁLCULO**

**Receita Operacional Líquida**

ROL \= Receita Bruta  
− Deduções  
− Tributos sobre Receita

---

**Resultado Operacional Ajustado**

Resultado Operacional Ajustado \=  
ROL  
− Custos Operacionais  
− Despesas Operacionais  
\+/− Resultado Financeiro  
\+/− Resultado Não Operacional

---

**Fluxo Operacional Ajustado Final**

Fluxo Operacional Ajustado Final \=  
Resultado Operacional Ajustado  
− Pressões Complementares de Caixa

---

**8\. PRESSÕES COMPLEMENTARES DE CAIXA**

Este bloco utiliza contas híbridas da DRE e BP.

Inclui:

* fornecedores vencidos; 

* parcelamentos; 

* contingências; 

* dívida fiscal; 

* dívida trabalhista; 

* mútuos; 

* intercompany. 

Objetivo:

avaliar fatores de drenagem de caixa não capturados integralmente pela DRE tradicional.

---

**9\. TABELA DE PARAMETRIZAÇÃO**

O sistema deverá utilizar a tabela fornecida no manual:

**Grupo metodologia | Macrogrupo | Código Referencial | Descrição Referencial**

Cada conta referencial deverá ser automaticamente agrupada em seu respectivo macrogrupo.

---

**10\. LOG OBRIGATÓRIO DA AUTOMAÇÃO**

O sistema deverá gerar trilha de auditoria completa contendo:

* código conta empresa; 

* descrição conta empresa; 

* código referencial; 

* descrição referencial; 

* saldo 31/12; 

* grupo metodologia; 

* macrogrupo; 

* regra aplicada. 

---

**Regra registrada obrigatória:**

Exemplo:

Conta empresa: 5.01.02.003

Conta referencial: 3.01.01.07.01.18

Macrogrupo: Aluguéis

Saldo: 80.000

Regra aplicada:  
"Conta filha utilizada; conta pai ignorada."

---

**11\. RESULTADO ESPERADO DA AUTOMAÇÃO**

Saída final do motor:

| Grupo metodologia | Macrogrupo | Valor |
| :---- | :---- | :---- |
| Receita Operacional | Receita Bruta Operacional | 12.500.000 |
| Receita Operacional | Tributos sobre Receita | (1.900.000) |
| Custos Operacionais | CPV/CMV/CSP | (6.300.000) |
| Despesas Operacionais | Pessoal | (2.100.000) |
| Resultado Financeiro | Despesas Financeiras | (280.000) |

E posterior cálculo automático do:

**Fluxo Operacional Ajustado Final.**

| Grupo metodologia | Macrogrupo | Código Referencial | Descrição Referencial |
| :---- | :---- | :---- | :---- |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.01 | Receita de Exportação Direta de Mercadorias e Produtos |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.02 | Receita de Vendas de Mercadorias e Produtos a Comercial Exportadora com Fim Específico de Exportação |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.03 | Receita de Exportação de Serviços |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.04 | Receita da Venda de Produtos de Fabricação Própria no Mercado Interno |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.05 | Receita da Revenda de Mercadorias no Mercado Interno |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.06 | Receita da Prestação de Serviços no Mercado Interno |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.07 | Receita da Venda de Unidades Imobiliárias |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.08 | Receita da Locação de Bens Móveis e Imóveis |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.20 | Receita de Contrato de Construção |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.25 | Receita de Direito de Exploração Serviço Público |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.30 | Receita de Securitização de Créditos |
| Receita Operacional | Receita Bruta Operacional | 3.01.01.01.01.98 | Outras Receitas da Atividade Geral |
| Receita Operacional | Deduções da Receita | 3.01.01.01.02.01 | Vendas Canceladas e Devoluções de Vendas |
| Receita Operacional | Deduções da Receita | 3.01.01.01.02.02 | Descontos Incondicionais e Abatimentos |
| Receita Operacional | Tributos sobre Receita | 3.01.01.01.02.03 | ICMS |
| Receita Operacional | Tributos sobre Receita | 3.01.01.01.02.04 | COFINS sobre Receita Bruta |
| Receita Operacional | Tributos sobre Receita | 3.01.01.01.02.05 | PIS/PASEP sobre Receita Bruta |
| Receita Operacional | Tributos sobre Receita | 3.01.01.01.02.06 | ISS |
| Receita Operacional | Tributos sobre Receita | 3.01.01.01.02.09 | Demais Impostos e Contribuições Incidentes sobre Vendas e Serviços |
| Receita Operacional | Ajustes Redutores da Receita | 3.01.01.01.02.10 | Ajuste a Valor Presente sobre Receita Bruta |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.60 | CPC 47 \- Modificações Contratuais |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.62 | CPC 47 \- Reconhecimento de Passivos de Contrato \- Garantias |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.64 | CPC 47 \- Reconhecimento de Passivos de Contrato \- Direitos não Exercidos |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.66 | CPC 47 \- Reconhecimento de Passivos de Contrato \- Serviços de Custódia \- Vendas para Entrega Futura |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.68 | CPC 47 \- Preço de Transação \- Contraprestações Variáveis |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.70 | CPC 47 \- Preço de Transação \- Reavaliações de Contraprestação Variável |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.72 | CPC 47 \- Preço de Transação \- Contraprestações Pagas ou a Pagar |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.74 | CPC 47 \- Preço de Transação \- Obrigações de Desempenho |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.76 | CPC 47 \- Critérios Divergentes da Legislação Tributária \- Não Recebimento de Contraprestação |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.78 | CPC 47 \- Critérios Divergentes da Legislação Tributária \- Passivos de Contrato \- Direito à Devolução |
| Receita Operacional | Ajustes CPC 47 | 3.01.01.01.02.80 | CPC 47 \- Critérios Divergentes da Legislação Tributária \- Passivos de Contrato \- Direito de Aquisição Opcional |
| Custos Operacionais | Custo dos Produtos Vendidos | 3.01.01.03.01.01 | Custo dos Produtos de Fabricação Própria Vendidos |
| Custos Operacionais | Custo das Mercadorias Revendidas | 3.01.01.03.01.02 | Custo das Mercadorias Revendidas |
| Custos Operacionais | Custo dos Serviços Prestados | 3.01.01.03.01.03 | Custo dos Serviços Prestados |
| Custos Operacionais | Custo Imobiliário | 3.01.01.03.01.04 | Custo das Unidades Imobiliárias Vendidas |
| Custos Operacionais | Custo de Locação / Arrendamento | 3.01.01.03.01.10 | Custo dos Bens Arrendados |
| Custos Operacionais | Custo de Construção | 3.01.01.03.01.20 | Custo de Construção |
| Custos Operacionais | Custo de Securitização | 3.01.01.03.01.30 | Custo de Operação de Securitização |
| Outras Receitas Operacionais | Receitas Financeiras / Cambiais | 3.01.01.05.01.01 | Variações Cambiais Ativas |
| Outras Receitas Operacionais | Ganhos Financeiros | 3.01.01.05.01.02 | Ganhos Auferidos no Mercado de Renda Variável, exceto Day-Trade |
| Outras Receitas Operacionais | Ganhos Financeiros | 3.01.01.05.01.03 | Ganhos em Operações Day-Trade |
| Outras Receitas Operacionais | Receitas Financeiras | 3.01.01.05.01.04 | Receitas de Juros sobre o Capital Próprio |
| Outras Receitas Operacionais | Receitas Financeiras | 3.01.01.05.01.05 | Outras Receitas Financeiras |
| Outras Receitas Operacionais | Participações Societárias | 3.01.01.05.01.06 | Resultados Positivos em Participações Societárias Avaliadas pelo Método de Equivalência Patrimonial |
| Outras Receitas Operacionais | Participações Societárias | 3.01.01.05.01.07 | Resultados Positivos em SCP Avaliadas pelo Método de Equivalência Patrimonial |
| Outras Receitas Operacionais | Exterior / Ganhos de Capital | 3.01.01.05.01.08 | Rendimentos e Ganhos de Capital Auferidos no Exterior |
| Outras Receitas Operacionais | Reversões | 3.01.01.05.01.09 | Reversão das Perdas Estimadas Decorrentes de Teste de Recuperabilidade |
| Outras Receitas Operacionais | Reversões | 3.01.01.05.01.10 | Reversão dos Saldos das Provisões |
| Outras Receitas Operacionais | Prêmios / Subvenções | 3.01.01.05.01.11 | Prêmios Recebidos na Emissão de Debêntures |
| Outras Receitas Operacionais | Subvenções | 3.01.01.05.01.12 | Doações e Subvenções para Custeio ou Operações |
| Outras Receitas Operacionais | Subvenções | 3.01.01.05.01.13 | Doações e Subvenções para Investimentos |
| Outras Receitas Operacionais | Ajustes Patrimoniais | 3.01.01.05.01.14 | Receitas de Reclassificação de Ajustes de Avaliação Patrimonial |
| Outras Receitas Operacionais | Ajustes Patrimoniais | 3.01.01.05.01.15 | Receitas de Reclassificação de Ajustes de Avaliação Patrimonial \- Reflexo |
| Outras Receitas Operacionais | Receitas Financeiras AVP | 3.01.01.05.01.16 | Receitas Financeiras Decorrentes de Ajustes ao Valor Presente |
| Outras Receitas Operacionais | Ganhos Societários | 3.01.01.05.01.17 | Ganho por Compra Vantajosa em Investimentos |
| Outras Receitas Operacionais | Ganhos Societários | 3.01.01.05.01.18 | Amortização de Menos-Valia |
| Outras Receitas Operacionais | Receitas de Aluguel | 3.01.01.05.01.19 | Receita de Aluguel de Bens Imóveis \- Atividade Não Principal |
| Outras Receitas Operacionais | Receitas de Aluguel | 3.01.01.05.01.20 | Receita de Aluguel de Bens Móveis \- Atividade Não Principal |
| Outras Receitas Operacionais | Créditos Fiscais | 3.01.01.05.01.21 | Créditos Presumidos de IPI |
| Outras Receitas Operacionais | Créditos Fiscais | 3.01.01.05.01.22 | Créditos Presumidos de PIS/COFINS |
| Outras Receitas Operacionais | Créditos Fiscais | 3.01.01.05.01.23 | Outros Créditos Fiscais Presumidos |
| Outras Receitas Operacionais | Indenizações / Multas Recebidas | 3.01.01.05.01.24 | Multas e Outras Vantagens Recebidas |
| Outras Receitas Operacionais | Dividendos / Participações | 3.01.01.05.01.25 | Lucros e Dividendos Derivados de Participações Societárias Avaliadas pelo Custo de Aquisição |
| Outras Receitas Operacionais | Receitas Financeiras | 3.01.01.05.01.26 | Receitas com Empréstimos de Valores Mobiliários |
| Outras Receitas Operacionais | Receitas Financeiras / Mútuos | 3.01.01.05.01.27 | Rendimentos Auferidos em Operações de Mútuo – Partes Relacionadas |
| Outras Receitas Operacionais | Receitas Financeiras / Mútuos | 3.01.01.05.01.28 | Rendimentos Auferidos em Operações de Mútuo – Partes Não Relacionadas |
| Outras Receitas Operacionais | Receitas Financeiras / Debêntures | 3.01.01.05.01.29 | Rendimentos Auferidos com Debêntures \- Emitente Partes Relacionadas |
| Outras Receitas Operacionais | Receitas Financeiras / Debêntures | 3.01.01.05.01.30 | Rendimentos Auferidos com Debêntures \- Emitente Partes Não Relacionadas |
| Outras Receitas Operacionais | Receitas Financeiras | 3.01.01.05.01.31 | Rendimentos Auferidos com Títulos Públicos |
| Outras Receitas Operacionais | Receitas Financeiras | 3.01.01.05.01.32 | Juros Auferidos com Outros Ativos Financeiros Mensurados pelo Custo Amortizado |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.33 | Ganho de Ajustes a Valor Justo \- Instrumentos Financeiros para Negociação |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.34 | Ganho de Ajustes a Valor Justo \- Instrumentos Financeiros Disponíveis para Venda |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.35 | Ganho de Ajustes a Valor Justo \- Instrumentos Financeiros de Hedge de Valor Justo |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.36 | Ganho de Ajustes a Valor Justo \- Instrumentos Financeiros de Hedge \- Reclassificação |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.37 | Ganho de Ajustes a Valor Justo \- Item Objeto de Hedge de Valor Justo |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.38 | Ganho de Ajustes a Valor Justo \- Propriedade para Investimento |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.39 | Ganho de Ajustes a Valor Justo \- Ativo Biológico Consumível |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.40 | Ganho de Ajustes a Valor Justo \- Ativo Biológico de Produção |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.41 | Ganho de Ajustes a Valor Justo \- Ativos Não Circulantes Mantidos para Venda |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.42 | Ganho de Ajustes a Valor Justo \- Subscrição de Capital com demais Bens |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.43 | Ganho de Ajustes a Valor Justo \- Subscrição de Capital com Participação Societária |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.44 | Ganho de Ajustes a Valor Justo \- Aquisição de Participação Societária em Estágios |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.45 | Ganho de Ajustes a Valor Justo \- Decorrente de Permuta de Ativos ou Passivos |
| Outras Receitas Operacionais | Ganhos a Valor Justo | 3.01.01.05.01.46 | Ganho de Ajustes a Valor Justo \- Outras Operações |
| Outras Receitas Operacionais | Outras Receitas Operacionais | 3.01.01.05.01.99 | Outras Receitas Operacionais |
| Despesas Operacionais | Pessoal / Administração | 3.01.01.07.01.01 | Remuneração a Dirigentes e a Conselho de Administração |
| Despesas Operacionais | Pessoal | 3.01.01.07.01.02 | Ordenados, Salários, Gratificações e Outras Remunerações a Empregados |
| Despesas Operacionais | Pessoal | 3.01.01.07.01.03 | Outros Gastos com Pessoal |
| Despesas Operacionais | Serviços de Terceiros | 3.01.01.07.01.04 | Outros Serviços Prestados por Pessoa Física ou Jurídica |
| Despesas Operacionais | Encargos Sociais | 3.01.01.07.01.05 | Encargos Sociais \- Previdência Social |
| Despesas Operacionais | Encargos Sociais | 3.01.01.07.01.06 | Encargos Sociais \- FGTS |
| Despesas Operacionais | Encargos Sociais | 3.01.01.07.01.07 | Encargos Sociais – Outros |
| Despesas Operacionais | Doações / Patrocínios | 3.01.01.07.01.08 | Doações e Patrocínios de Caráter Cultural e Artístico |
| Despesas Operacionais | Benefícios | 3.01.01.07.01.09 | Operações de Aquisição de Vale Cultura |
| Despesas Operacionais | Doações / Patrocínios | 3.01.01.07.01.10 | Doações a Instituições de Ensino e Pesquisa |
| Despesas Operacionais | Doações / Patrocínios | 3.01.01.07.01.11 | Doações a Entidades Civis |
| Despesas Operacionais | Doações / Patrocínios | 3.01.01.07.01.12 | Outras Contribuições, Doações e Patrocínios |
| Despesas Operacionais | Benefícios | 3.01.01.07.01.13 | Alimentação do Trabalhador |
| Despesas Operacionais | Tributos sobre Outras Receitas | 3.01.01.07.01.14 | PIS/PASEP |
| Despesas Operacionais | Tributos sobre Outras Receitas | 3.01.01.07.01.15 | COFINS |
| Despesas Operacionais | Tributos / Taxas | 3.01.01.07.01.16 | Demais Impostos, Taxas e Contribuições, exceto IR e CSLL |
| Despesas Operacionais | Arrendamento / Ocupação | 3.01.01.07.01.17 | Arrendamento Mercantil |
| Despesas Operacionais | Ocupação / Aluguéis | 3.01.01.07.01.18 | Aluguéis |
| Despesas Operacionais | Veículos / Conservação | 3.01.01.07.01.19 | Despesas com Veículos e de Conservação de Bens e Instalações |
| Despesas Operacionais | Comercial / Marketing | 3.01.01.07.01.20 | Propaganda, Publicidade e Patrocínio |
| Despesas Operacionais | Comercial / Marketing | 3.01.01.07.01.21 | Propaganda, Publicidade e Patrocínio de Associações Desportivas |
| Despesas Operacionais | Multas | 3.01.01.07.01.22 | Multas |
| Despesas Operacionais | Depreciação | 3.01.01.07.01.23 | Encargos de Depreciação |
| Despesas Operacionais | Amortização | 3.01.01.07.01.24 | Encargos de Amortização |
| Despesas Operacionais | Perdas Operacionais | 3.01.01.07.01.25 | Perdas em Operações de Crédito |
| Despesas Operacionais | Provisões Trabalhistas | 3.01.01.07.01.26 | Provisões para Férias |
| Despesas Operacionais | Provisões Trabalhistas | 3.01.01.07.01.27 | Provisões para 13º Salário de Empregados |
| Despesas Operacionais | Provisões | 3.01.01.07.01.28 | Provisão para Perda de Estoque de Livros |
| Despesas Operacionais | Provisões | 3.01.01.07.01.29 | Demais Provisões |
| Despesas Operacionais | Administração | 3.01.01.07.01.30 | Gratificações a Administradores |
| Despesas Operacionais | Royalties / Tecnologia | 3.01.01.07.01.31 | Royalties e Assistência Técnica \- no País |
| Despesas Operacionais | Royalties / Tecnologia | 3.01.01.07.01.32 | Royalties e Assistência Técnica \- no Exterior |
| Despesas Operacionais | Benefícios | 3.01.01.07.01.33 | Assistência Médica, Odontológica e Farmacêutica a Empregados |
| Despesas Operacionais | Tecnologia / Pesquisa | 3.01.01.07.01.34 | Pesquisas Científicas e Tecnológicas |
| Despesas Operacionais | Bens de Pequeno Valor | 3.01.01.07.01.35 | Bens de Pequeno Valor Unitário ou de Vida Útil de até um Ano Deduzidos como Despesa |
| Despesas Operacionais | Utilities | 3.01.01.07.01.36 | Despesas com Energia Elétrica |
| Despesas Operacionais | Utilities | 3.01.01.07.01.37 | Despesas com Água e Esgoto |
| Despesas Operacionais | Tecnologia / Telecom | 3.01.01.07.01.38 | Despesas com Telefone e Internet |
| Despesas Operacionais | Administrativas | 3.01.01.07.01.39 | Despesas com Correios e Malotes |
| Despesas Operacionais | Seguros | 3.01.01.07.01.40 | Despesas com Seguros |
| Despesas Operacionais | Benefícios | 3.01.01.07.01.41 | Benefícios Previdenciários a Empregados |
| Despesas Operacionais | Benefícios | 3.01.01.07.01.42 | Fundo de Aposentadoria Individual \- FAPI |
| Despesas Operacionais | Benefícios | 3.01.01.07.01.43 | Planos de Poupança e Investimento \- PAIT |
| Despesas Operacionais | Tecnologia / Pesquisa | 3.01.01.07.01.44 | Pesquisa e Desenvolvimento Abrangidas no Programa Rota 2030 |
| Outras Despesas Operacionais | Despesas Financeiras / Cambiais | 3.01.01.09.01.01 | Variações Cambiais Passivas |
| Outras Despesas Operacionais | Perdas Financeiras | 3.01.01.09.01.02 | Perdas Incorridas no Mercado de Renda Variável, exceto Day-Trade |
| Outras Despesas Operacionais | Perdas Financeiras | 3.01.01.09.01.03 | Perdas em Operações Day-Trade |
| Outras Despesas Operacionais | Despesas Financeiras | 3.01.01.09.01.04 | Despesas de Juros sobre o Capital Próprio |
| Outras Despesas Operacionais | Despesas Financeiras / Debêntures | 3.01.01.09.01.05 | Despesas de Remuneração de Debêntures |
| Outras Despesas Operacionais | Despesas Financeiras / Empréstimos | 3.01.01.09.01.06 | Juros com Empréstimos de Pessoas Vinculadas ou Situadas em País com Tributação Favorecida |
| Outras Despesas Operacionais | Despesas Financeiras / Arrendamento | 3.01.01.09.01.07 | Despesas Financeiras Relativas a Arrendamento Mercantil Financeiro |
| Outras Despesas Operacionais | Despesas Financeiras | 3.01.01.09.01.08 | Outras Despesas Financeiras |
| Outras Despesas Operacionais | Participações Societárias | 3.01.01.09.01.09 | Resultados Negativos em Participações Societárias Avaliadas pelo Método de Equivalência Patrimonial |
| Outras Despesas Operacionais | Participações Societárias | 3.01.01.09.01.10 | Resultados Negativos em SCP Avaliadas pelo Método de Equivalência Patrimonial |
| Outras Despesas Operacionais | Exterior / Perdas | 3.01.01.09.01.11 | Perdas em Operações Realizadas no Exterior |
| Outras Despesas Operacionais | Impairment | 3.01.01.09.01.12 | Perdas Estimadas Decorrentes de Teste de Recuperabilidade |
| Outras Despesas Operacionais | Ajustes Patrimoniais | 3.01.01.09.01.13 | Despesas de Reclassificação de Ajustes de Avaliação Patrimonial |
| Outras Despesas Operacionais | Ajustes Patrimoniais | 3.01.01.09.01.14 | Despesas de Reclassificação de Ajustes de Avaliação Patrimonial \- Reflexo |
| Outras Despesas Operacionais | Despesas Financeiras AVP | 3.01.01.09.01.15 | Despesas Financeiras Decorrentes dos Ajustes ao Valor Presente |
| Outras Despesas Operacionais | Depreciação Leasing | 3.01.01.09.01.16 | Encargos de Depreciação de Bens Objeto de Leasing Financeiro |
| Outras Despesas Operacionais | Amortização | 3.01.01.09.01.17 | Encargos de Amortização de Mais-Valia |
| Outras Despesas Operacionais | Aluguéis | 3.01.01.09.01.18 | Aluguéis de Bens Imóveis \- Locador Parte Relacionada |
| Outras Despesas Operacionais | Aluguéis | 3.01.01.09.01.19 | Aluguéis de Bens Imóveis \- Locador Parte Não Relacionada |
| Outras Despesas Operacionais | Despesas Financeiras / Títulos | 3.01.01.09.01.20 | Despesas com Empréstimos de Valores Mobiliários |

