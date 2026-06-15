# FLUXO DECIDIDO — INTERPRETAÇÃO DO COD_CTA_REF DA ECD COM TABELA OFICIAL + TABELA METODOLÓGICA

## 1. PREMISSA CENTRAL

Neste fluxo, o sistema deve partir da seguinte premissa:

A ECD é a fonte declaratória confiável.

Ou seja, quando a ECD informa um vínculo entre a conta societária da empresa e um código do plano referencial da Receita Federal, o sistema deve aceitar esse vínculo como a classificação contábil declarada pelo contador.

O objetivo aqui não é auditar se o contador classificou certo.

O objetivo é garantir que o sistema interprete corretamente o código referencial que já veio informado na ECD.

---

## 2. PROBLEMA ATUAL

O sistema está recebendo da ECD um código referencial específico, por exemplo:

2.01.01.07.01

Mas a tabela metodológica interna está usando regras genéricas demais, como:

2.01.01.* → fornecedores

Isso causa erro porque o prefixo 2.01.01.* pode conter naturezas econômicas diferentes, como:

- fornecedores;
- empréstimos e financiamentos;
- obrigações tributárias;
- parcelamentos;
- provisões;
- outras obrigações.

Assim, uma conta que a ECD declarou como empréstimo pode ser interpretada pelo sistema como fornecedor.

O erro não está necessariamente na ECD.

O erro está na camada interna de interpretação metodológica.

---

## 3. PRINCÍPIO CORRETO

O sistema não deve tentar “adivinhar” o significado do COD_CTA_REF apenas pelo prefixo.

O sistema deve seguir duas camadas distintas:

1. Tabela oficial do plano referencial da Receita
2. Tabela metodológica interna do sistema

A separação é essencial.

---

## 4. CAMADA 1 — TABELA OFICIAL DO PLANO REFERENCIAL

### 4.1. Finalidade

A tabela oficial serve para traduzir o código referencial informado na ECD para sua descrição formal.

Exemplo:

COD_CTA_REF:
2.01.01.07.01

Consulta na tabela oficial:

2.01.01.07.01 → Empréstimos / financiamentos / obrigação financeira equivalente

A ECD traz o código.

A tabela oficial traz a semântica formal do código.

---

### 4.2. O que essa tabela responde

A tabela oficial responde:

“O que esse código referencial significa segundo a Receita Federal?”

Ela não responde necessariamente:

“Como esse código deve ser tratado no PLR?”
“Como esse código deve ser tratado no FCO?”
“Como esse código deve ser tratado na CAPAG-e?”

Essas respostas pertencem à tabela metodológica interna.

---

### 4.3. Estrutura mínima da tabela oficial

Tabela: plano_referencial_oficial

Campos sugeridos:

- id
- cod_cta_ref
- descricao_oficial
- cod_cta_ref_pai
- nivel
- natureza
- vigencia_inicio
- vigencia_fim
- leiaute
- tipo_entidade
- fonte
- status

Exemplo:

cod_cta_ref: 2.01.01.07.01
descricao_oficial: Empréstimos e financiamentos
cod_cta_ref_pai: 2.01.01.07
nivel: 5
vigencia_inicio: 2024-01-01
vigencia_fim: null
leiaute: ECD/ECF aplicável
status: ativo

---

## 5. CAMADA 2 — TABELA METODOLÓGICA INTERNA

### 5.1. Finalidade

A tabela metodológica interna não deve redefinir o que o código é.

Ela deve definir como o código será tratado nos cálculos e relatórios do sistema.

Ou seja:

COD_CTA_REF oficial
   ↓
tratamento metodológico interno

Exemplo:

2.01.01.07.01
   ↓
PLR: passivo financeiro
FCO: não classificar como pagamento operacional a fornecedor
CAPAG-e: dívida / financiamento

---

### 5.2. O que essa tabela responde

A tabela metodológica responde:

“Dado que a Receita classifica esse código dessa forma, como meu sistema deve tratar esse código em cada finalidade?”

Finalidades possíveis:

- PLR;
- FCO;
- CAPAG-e;
- análise patrimonial;
- agrupamento gerencial;
- memória de cálculo;
- indicadores internos;
- relatórios de auditoria.

---

### 5.3. Estrutura mínima da tabela metodológica

Tabela: metodologia_cod_cta_ref

Campos sugeridos:

- id
- cod_cta_ref_padrao
- tipo_match
- descricao_metodologica
- categoria_plr
- categoria_fco
- categoria_capag
- natureza_fluxo
- tratamento_operacional
- incluir_no_calculo
- sinal
- nivel_especificidade
- prioridade
- status_regra
- observacao
- vigencia_inicio
- vigencia_fim

Exemplo:

cod_cta_ref_padrao: 2.01.01.07.*
tipo_match: PREFIXO
descricao_metodologica: Empréstimos e financiamentos de curto prazo
categoria_plr: passivo_financeiro
categoria_fco: excluir_fluxo_operacional
categoria_capag: divida_financeira
natureza_fluxo: financiamento
tratamento_operacional: nao_fornecedor
incluir_no_calculo: sim
nivel_especificidade: 4
prioridade: 100
status_regra: ativa

---

## 6. FLUXO GERAL DO PROCESSAMENTO

ECD COMPLETA
   ↓
Parser da ECD
   ↓
Extração dos registros I050/I051
   ↓
Conta societária da empresa
   ↓
COD_CTA_REF informado na ECD
   ↓
Consulta à tabela oficial do plano referencial
   ↓
Descrição oficial do código
   ↓
Consulta à tabela metodológica interna
   ↓
Tratamento por finalidade:
   - PLR
   - FCO
   - CAPAG-e
   ↓
Classificação interna correta
   ↓
Memória de cálculo
   ↓
Relatório final

---

## 7. FLUXO DETALHADO

### 7.1. Etapa 1 — Ler a ECD

Entrada:

Arquivo ECD em texto.

Registros principais:

I050 = conta contábil da empresa
I051 = vínculo com o plano referencial

Exemplo:

I050:
Conta societária: 1725
Nome: EMPRESTIMO - SICOOB CREDICITRUS - C

I051:
COD_CTA_REF: 2.01.01.07.01

Resultado da etapa:

Conta 1725 vinculada ao código referencial 2.01.01.07.01.

---

### 7.2. Etapa 2 — Consultar a tabela oficial

O sistema consulta:

plano_referencial_oficial.cod_cta_ref = 2.01.01.07.01

Resultado esperado:

cod_cta_ref: 2.01.01.07.01
descricao_oficial: Empréstimos e financiamentos
grupo_oficial: Passivo / Obrigações / Empréstimos e financiamentos

Resultado da etapa:

O sistema passa a saber formalmente que aquele código representa empréstimo/financiamento segundo o plano referencial.

---

### 7.3. Etapa 3 — Consultar a tabela metodológica

O sistema procura na tabela metodológica a regra aplicável ao código:

2.01.01.07.01

A busca deve obedecer à regra de especificidade:

1. primeiro tenta código exato;
2. depois tenta prefixo mais específico;
3. depois tenta prefixos menos específicos;
4. nunca usa prefixo bloqueado;
5. nunca usa prefixo amplo que contenha naturezas diferentes, salvo se explicitamente permitido.

Exemplo de busca:

Tentativa 1:
2.01.01.07.01

Tentativa 2:
2.01.01.07.*

Tentativa 3:
2.01.01.*

Se existir regra para 2.01.01.07.*, ela vence a regra 2.01.01.*.

---

## 8. REGRA DE ESPECIFICIDADE

A regra mais específica sempre vence.

Ordem de prioridade:

1. código exato;
2. prefixo de maior profundidade;
3. prefixo de menor profundidade;
4. regra genérica, apenas se for segura.

Exemplo:

2.01.01.07.01 vence 2.01.01.07.*
2.01.01.07.* vence 2.01.01.*
2.01.01.* só pode ser usado se for metodologicamente seguro.

---

## 9. REGRA DE BLOQUEIO DE PREFIXO AMPLO

Um prefixo amplo não deve ser usado como regra final quando seus filhos tiverem tratamentos econômicos diferentes.

Exemplo de regra ruim:

2.01.01.* → fornecedores

Por que é ruim?

Porque dentro de 2.01.01.* podem existir:

2.01.01.01.* → fornecedores
2.01.01.07.* → empréstimos e financiamentos
2.01.01.09.* → obrigações tributárias
2.01.01.15.* → provisões

Portanto:

2.01.01.* deve ser bloqueado para classificação final.

Exemplo correto:

2.01.01.01.* → fornecedores
2.01.01.07.* → empréstimos e financiamentos
2.01.01.09.* → obrigações tributárias
2.01.01.15.* → provisões
2.01.01.*    → BLOQUEADO

---

## 10. STATUS DAS REGRAS METODOLÓGICAS

Cada regra metodológica deve ter um status.

Status sugeridos:

ATIVA:
Regra válida para classificação.

BLOQUEADA:
Regra não pode ser usada para classificação final.

EM_REVISAO:
Regra ainda não validada metodologicamente.

DEPRECIADA:
Regra antiga, mantida apenas para histórico.

GENERICA_SEGURA:
Regra ampla permitida porque todos os filhos relevantes possuem o mesmo tratamento econômico.

GENERICA_PERIGOSA:
Regra ampla identificada como potencialmente incorreta.

---

## 11. EXEMPLO DE TABELA METODOLÓGICA CORRIGIDA

### Exemplo ruim

cod_cta_ref_padrao: 2.01.01.*
categoria_fco: pagamentos_fornecedores
status_regra: ativa

Problema:

Essa regra transforma empréstimos, tributos e provisões em fornecedores.

---

### Exemplo correto

cod_cta_ref_padrao: 2.01.01.01.*
tipo_match: PREFIXO
categoria_plr: fornecedores
categoria_fco: pagamentos_fornecedores
categoria_capag: fornecedores
natureza_fluxo: operacional
status_regra: ativa

cod_cta_ref_padrao: 2.01.01.07.*
tipo_match: PREFIXO
categoria_plr: emprestimos_financiamentos
categoria_fco: excluir_fluxo_operacional
categoria_capag: divida_financeira
natureza_fluxo: financiamento
status_regra: ativa

cod_cta_ref_padrao: 2.01.01.09.*
tipo_match: PREFIXO
categoria_plr: obrigacoes_tributarias
categoria_fco: tributos_pagos_ou_a_pagar
categoria_capag: obrigacoes_fiscais
natureza_fluxo: tributario
status_regra: ativa

cod_cta_ref_padrao: 2.01.01.15.*
tipo_match: PREFIXO
categoria_plr: provisoes
categoria_fco: ajustar_conforme_metodologia
categoria_capag: provisoes
natureza_fluxo: provisao
status_regra: ativa

cod_cta_ref_padrao: 2.01.01.*
tipo_match: PREFIXO
categoria_plr: null
categoria_fco: null
categoria_capag: null
natureza_fluxo: null
status_regra: bloqueada
observacao: Prefixo contém naturezas econômicas diferentes. Não usar para classificação final.

---

## 12. TRATAMENTO POR FINALIDADE

A tabela metodológica não deve ter apenas uma categoria única.

O mesmo COD_CTA_REF deve poder ter tratamentos diferentes em PLR, FCO e CAPAG-e.

Exemplo:

COD_CTA_REF:
2.01.01.07.01

Descrição oficial:
Empréstimos e financiamentos

Tratamentos:

PLR:
passivo financeiro

FCO:
não classificar como pagamento operacional a fornecedor

CAPAG-e:
dívida financeira / financiamento

Natureza do fluxo:
financiamento

Isso evita que o sistema trate tudo como uma categoria única e reaproveite indevidamente em todos os cálculos.

---

## 13. ESTRUTURA SUGERIDA DE RESULTADO POR CONTA

Para cada conta da ECD, o sistema deve gerar um objeto assim:

Conta societária:
1725

Nome da conta:
EMPRESTIMO - SICOOB CREDICITRUS - C

COD_CTA_REF informado:
2.01.01.07.01

Descrição oficial:
Empréstimos e financiamentos

Regra metodológica aplicada:
2.01.01.07.*

Categoria PLR:
passivo financeiro

Categoria FCO:
excluir fluxo operacional / fluxo de financiamento

Categoria CAPAG-e:
dívida financeira

Status:
mapeado corretamente

Observação:
Conta não deve ser tratada como fornecedor, pois o código referencial pertence ao grupo de empréstimos e financiamentos.

---

## 14. COMPORTAMENTO QUANDO NÃO EXISTIR REGRA METODOLÓGICA

Se o sistema encontrar o COD_CTA_REF na tabela oficial, mas não encontrar regra metodológica aplicável, ele não deve usar uma regra ampla perigosa.

Fluxo correto:

COD_CTA_REF encontrado na tabela oficial
   ↓
Descrição oficial encontrada
   ↓
Nenhuma regra metodológica segura encontrada
   ↓
Classificar como:
   "não mapeado metodologicamente"
   ↓
Enviar para revisão da tabela metodológica

Exemplo:

cod_cta_ref: 2.01.01.XX.XX
descricao_oficial: encontrada
metodologia: não encontrada

Resultado:

status: NAO_MAPEADO_METODOLOGICAMENTE
ação: revisar tabela metodológica
não classificar automaticamente como fornecedor, cliente, tributo ou outro grupo genérico

---

## 15. COMPORTAMENTO QUANDO O CÓDIGO NÃO EXISTIR NA TABELA OFICIAL

Se a ECD trouxer um COD_CTA_REF que não existe na tabela oficial carregada, o sistema deve verificar:

1. A tabela oficial carregada é do leiaute correto?
2. A vigência está correta?
3. O ano-calendário está correto?
4. O tipo de entidade está correto?
5. O código foi informado com formatação diferente?
6. O código está obsoleto?
7. Falta atualizar a base oficial?

Resultado possível:

status: COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL
ação: revisar base oficial ou leiaute aplicado

O sistema não deve inventar a descrição.

---

## 16. VALIDAÇÕES AUTOMÁTICAS DA TABELA METODOLÓGICA

Antes de usar a tabela em produção, o sistema deve validar:

1. Existem prefixos amplos ativos que possuem filhos com tratamentos diferentes?
2. Existem regras duplicadas para o mesmo código?
3. Existe conflito entre regra exata e regra por prefixo?
4. Existem códigos metodológicos que não existem na tabela oficial?
5. Existem códigos oficiais relevantes sem metodologia?
6. Existem regras vencidas sendo usadas?
7. Existem regras bloqueadas sendo aplicadas?
8. Existem tratamentos iguais sendo aplicados a naturezas oficiais diferentes sem justificativa?
9. Existem categorias FCO incompatíveis com a natureza oficial?
10. Existem códigos de dívida sendo tratados como fornecedor?

---

## 17. TESTES DE REGRESSÃO OBRIGATÓRIOS

Criar uma bateria de testes para impedir que o erro volte.

### Teste 1 — Empréstimo não pode virar fornecedor

Entrada:
COD_CTA_REF = 2.01.01.07.01

Resultado esperado:
categoria_fco ≠ pagamentos_fornecedores
categoria_capag = divida_financeira ou equivalente
natureza_fluxo = financiamento

---

### Teste 2 — Fornecedor pode virar fornecedor

Entrada:
COD_CTA_REF = 2.01.01.01.XX

Resultado esperado:
categoria_fco = pagamentos_fornecedores
categoria_plr = fornecedores

---

### Teste 3 — Tributo a recuperar não pode virar cliente

Entrada:
COD_CTA_REF = 1.01.02.03.XX

Resultado esperado:
categoria_plr = tributos_a_recuperar
categoria_fco ≠ recebimento_clientes

---

### Teste 4 — Prefixo bloqueado não pode classificar

Entrada:
COD_CTA_REF = 2.01.01.99.99
Regra disponível:
2.01.01.* = bloqueada

Resultado esperado:
status = NAO_MAPEADO_METODOLOGICAMENTE
ação = revisar metodologia

---

### Teste 5 — Regra mais específica vence

Regras:
2.01.01.* → fornecedores
2.01.01.07.* → empréstimos

Entrada:
2.01.01.07.01

Resultado esperado:
aplicar 2.01.01.07.*
não aplicar 2.01.01.*

---

## 18. ALGORITMO DE MATCH DA TABELA METODOLÓGICA

Entrada:
COD_CTA_REF = 2.01.01.07.01

Passo 1:
Buscar regra exata:
2.01.01.07.01

Se encontrar regra ativa:
aplicar.

Passo 2:
Buscar prefixo mais específico:
2.01.01.07.*

Se encontrar regra ativa:
aplicar.

Passo 3:
Buscar prefixo superior:
2.01.01.*

Se encontrar regra ativa:
verificar se é segura.

Se status = BLOQUEADA:
não aplicar.

Se status = GENERICA_PERIGOSA:
não aplicar.

Se status = GENERICA_SEGURA:
aplicar.

Passo 4:
Se nenhuma regra segura for encontrada:
retornar NAO_MAPEADO_METODOLOGICAMENTE.

---

## 19. PSEUDOCÓDIGO

function classificar_cod_cta_ref(cod_cta_ref, ano, leiaute, finalidade):

    registro_oficial = buscar_tabela_oficial(cod_cta_ref, ano, leiaute)

    if registro_oficial == null:
        return {
            status: "COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL",
            cod_cta_ref: cod_cta_ref,
            acao: "revisar_base_oficial"
        }

    candidatos = buscar_regras_metodologicas_por_especificidade(cod_cta_ref, ano)

    for regra in candidatos:

        if regra.status_regra == "BLOQUEADA":
            continue

        if regra.status_regra == "GENERICA_PERIGOSA":
            continue

        if regra.status_regra == "EM_REVISAO":
            continue

        if regra.status_regra == "ATIVA" or regra.status_regra == "GENERICA_SEGURA":

            tratamento = obter_tratamento_por_finalidade(regra, finalidade)

            if tratamento == null:
                continue

            return {
                status: "MAPEADO",
                cod_cta_ref: cod_cta_ref,
                descricao_oficial: registro_oficial.descricao_oficial,
                regra_aplicada: regra.cod_cta_ref_padrao,
                finalidade: finalidade,
                tratamento: tratamento,
                categoria_plr: regra.categoria_plr,
                categoria_fco: regra.categoria_fco,
                categoria_capag: regra.categoria_capag,
                natureza_fluxo: regra.natureza_fluxo
            }

    return {
        status: "NAO_MAPEADO_METODOLOGICAMENTE",
        cod_cta_ref: cod_cta_ref,
        descricao_oficial: registro_oficial.descricao_oficial,
        acao: "revisar_tabela_metodologica"
    }

---

## 20. EXEMPLO COMPLETO

### Entrada da ECD

Conta societária:
1725

Nome:
EMPRESTIMO - SICOOB CREDICITRUS - C

COD_CTA_REF:
2.01.01.07.01

---

### Consulta à tabela oficial

2.01.01.07.01
   ↓
Empréstimos e financiamentos

---

### Consulta à tabela metodológica

Busca:

1. 2.01.01.07.01
2. 2.01.01.07.*
3. 2.01.01.*

Regra encontrada:

2.01.01.07.* → empréstimos e financiamentos

---

### Resultado

Conta:
1725 - EMPRESTIMO - SICOOB CREDICITRUS - C

COD_CTA_REF:
2.01.01.07.01

Descrição oficial:
Empréstimos e financiamentos

Regra aplicada:
2.01.01.07.*

PLR:
passivo financeiro

FCO:
não classificar como pagamento a fornecedor

CAPAG-e:
dívida financeira

Natureza do fluxo:
financiamento

Status:
mapeado corretamente

---

## 21. REGRA DE OURO

O sistema deve preservar a granularidade do COD_CTA_REF informado na ECD.

Um código específico nunca deve ser reduzido a uma categoria genérica se essa redução alterar seu tratamento econômico.

Em outras palavras:

2.01.01.07.01 não pode virar fornecedor apenas porque começa com 2.01.01.

A regra correta é:

COD_CTA_REF específico
   ↓
descrição oficial
   ↓
tratamento metodológico específico
   ↓
classificação interna por finalidade

---

## 22. CONCLUSÃO

O sistema deve ter duas bases separadas:

1. Tabela oficial do plano referencial
   - serve para entender o significado formal do COD_CTA_REF.

2. Tabela metodológica interna
   - serve para definir como aquele código será tratado em PLR, FCO, CAPAG-e e demais cálculos.

O erro atual ocorre porque a tabela metodológica está genérica demais.

O upgrade correto é:

- importar/versionar a tabela oficial;
- quebrar regras amplas em subprefixos específicos;
- bloquear prefixos perigosos;
- aplicar sempre a regra mais específica;
- separar tratamentos por finalidade;
- nunca classificar automaticamente quando não houver regra segura.