# Pesquisa Oficial Para Construção Do Balanço Patrimonial Da ECD

## 1. Estado Do Documento

- Tipo: pesquisa técnica consolidada.
- Data da pesquisa: 2026-07-28.
- Situação: aprovada pelo usuário para registro documental.
- Efeito operacional imediato: nenhum.
- Efeito metodológico: fundamenta uma futura correção governada da leitura do
  balanço patrimonial, sem alterar por si só fórmula prudencial, SPEC, motor,
  banco, API ou frontend.

Este documento registra o padrão oficial encontrado para apresentar e conferir
o Balanço Patrimonial contido em uma Escrituração Contábil Digital (`ECD`).

## 2. Pergunta Respondida

Qual é o padrão oficial que permite ao PGE do Sped Contábil e a outros sistemas
apresentarem corretamente o Balanço Patrimonial de uma ECD, sem reconstruí-lo
por interpretação livre do nome ou do código das contas?

## 3. Conclusão

O padrão oficial é formado por:

- `J005`: identifica o período e o conjunto das demonstrações contábeis;
- `J100`: declara a estrutura e os valores do Balanço Patrimonial;
- `I052`: relaciona as contas analíticas do plano contábil aos códigos de
  aglutinação usados no `J100`;
- `I050`: contém o plano de contas contábil da pessoa jurídica;
- `I155`: contém os saldos periódicos das contas do `I050`.

O Balanço Patrimonial apresentado ao usuário deve reproduzir o `J100`. Sua
conferência deve seguir o vínculo oficial:

```text
I050 (conta analítica)
        |
        v
I052 (código de aglutinação)
        |
        v
J100 (linha do Balanço Patrimonial)

I155 (saldo da conta) ----> totalização e confronto com o J100
```

O `I051` não constrói o Balanço Patrimonial. Ele vincula uma conta do `I050` ao
plano de contas referencial e atende a outra finalidade declaratória.

## 4. Fontes Oficiais

### 4.1 Manual De Orientação Da ECD

- Documento: Manual de Orientação do Leiaute 9 da ECD.
- Atualização: novembro de 2024.
- Anexo ao Ato Declaratório Executivo Cofis nº 57/2023.
- Órgão: Receita Federal do Brasil / Sped.
- URL:
  `https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecd/manuais-e-documentos-tecnicos/manual_de_orientacao_da_ecd_leiaute_9_atualizacao_nov_2024.pdf/@@display-file/file`
- Consulta realizada em: 2026-07-28.

Trechos relevantes:

- página 47: obrigatoriedade das demonstrações contábeis;
- página 168: regras gerais do Bloco J;
- páginas 170 a 172: registro `J005` e conferência das demonstrações;
- páginas 173 a 178: registro `J100`, campos e validações do Balanço
  Patrimonial.

### 4.2 ReceitanetBX

- Documento: Perguntas e Respostas - ReceitanetBX.
- Órgão: Receita Federal do Brasil.
- URL:
  `https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/download/receitanetbx/perguntas-e-respostas-receitanetbx`
- Consulta realizada em: 2026-07-28.

O ReceitanetBX é um sistema de transmissão de arquivos da base da Receita
Federal para usuários autorizados. Ele permite baixar arquivos da ECD, mas não
é o componente que interpreta ou monta o Balanço Patrimonial. A apresentação e
a validação contábil são funções do PGE do Sped Contábil ou de outro sistema
que implemente corretamente o leiaute da ECD.

## 5. Obrigatoriedade Do Bloco J

Segundo o Manual da ECD, quando:

1. a data de encerramento do exercício social informada no `I030` estiver
   dentro do período informado no registro `0000`; e
2. o indicador da forma de escrituração `I010.IND_ESC` for `G`, `R` ou `B`;

devem existir, no mínimo:

- um `J005` cuja data final seja a data de encerramento do exercício;
- um `J100`, correspondente ao Balanço Patrimonial;
- um `J150`, correspondente à Demonstração do Resultado do Exercício.

O PGE gera erro quando essa obrigação não é cumprida.

Se a data de encerramento estiver fora do período transmitido pela ECD, as
demonstrações contábeis do Bloco J não são obrigatórias.

Para o CAPAG, que exige exercício anual encerrado em `31/12`, a ausência de
`J100` não deve ser compensada silenciosamente por uma reconstrução livre do
balanço. O arquivo deve ser diagnosticado conforme sua obrigação e sua
elegibilidade para a análise anual.

## 6. Como O J100 Representa O Balanço

O `J100` não usa necessariamente os códigos das contas do `I050`. Ele usa
**códigos de aglutinação atribuídos pela própria pessoa jurídica**.

Campos essenciais:

| Campo | Significado | Uso no CAPAG |
| --- | --- | --- |
| `COD_AGL` | Código de aglutinação da linha | Identidade da linha do balanço |
| `IND_COD_AGL` | `T` totalizador ou `D` detalhe | Evitar tratar total e detalhe como a mesma coisa |
| `NIVEL_AGL` | Nível hierárquico | Indentação e estrutura |
| `COD_AGL_SUP` | Código de aglutinação superior | Relação pai-filho |
| `IND_GRP_BAL` | `A` Ativo ou `P` Passivo | Separação dos dois lados do balanço |
| `DESCR_COD_AGL` | Descrição da linha | Nome declarado para apresentação |
| `VL_CTA_INI` | Valor inicial | Comparação com o início do período |
| `IND_DC_BAL_INI` | Natureza devedora ou credora inicial | Sinal do valor inicial |
| `VL_CTA_FIN` | Valor final | Valor principal do balanço na data de encerramento |
| `IND_DC_BAL_FIN` | Natureza devedora ou credora final | Sinal do valor final |
| `NOTA_EXP_REF` | Referência a nota explicativa | Auditoria e apresentação futura |

Para apresentar o balanço no encerramento do exercício, o CAPAG deve usar
`VL_CTA_FIN` e `IND_DC_BAL_FIN`. `VL_CTA_INI` não pode ser apresentado como se
fosse o saldo final.

## 7. Como A Receita Confere O J100

O Manual descreve o seguinte processo:

1. o `I052` associa cada conta analítica do `I050` a um `COD_AGL`;
2. o PGE totaliza os saldos do `I155` na data do balanço para esse código de
   aglutinação;
3. o total calculado é confrontado com o valor declarado na linha de detalhe do
   `J100`;
4. divergências sujeitas às regras de validação geram erro.

O PGE também verifica, entre outras condições:

- existência do `I052` para linhas de detalhe do `J100`;
- compatibilidade entre a natureza da conta do `I050` e o grupo do `J100`;
- existência de exatamente duas linhas de nível 1: uma de Ativo e outra de
  Passivo;
- existência de pelo menos uma linha de detalhe;
- consistência da hierarquia e dos códigos de aglutinação;
- igualdade dos saldos finais calculados e declarados, quando aplicável.

## 8. Regra Recomendada Para O CAPAG

### 8.1 Importação

Preservar integralmente os registros necessários:

- `0000`;
- `I010`;
- `I030`;
- `I050`;
- `I052`;
- `I150`;
- `I155`;
- `J005`;
- `J100`;
- `J150`, quando implementado.

Não descartar campos estruturais ou valores inicial e final do `J100`.

### 8.2 Verificação De Obrigatoriedade

Determinar, pelos registros `0000`, `I010` e `I030`, se o Bloco J é obrigatório
para a ECD importada.

Estados mínimos recomendados:

- `J100_OBRIGATORIO_PRESENTE`;
- `J100_OBRIGATORIO_AUSENTE`;
- `J100_NAO_OBRIGATORIO`;
- `J100_PRESENTE_FORA_DA_OBRIGACAO`;
- `J100_INVALIDO_OU_INCONSISTENTE`.

### 8.3 Construção Visual

Quando existir um `J100` aplicável:

1. selecionar o `J005` correspondente ao encerramento analisado;
2. selecionar os filhos `J100` desse `J005`;
3. manter a ordem declarada;
4. construir a árvore com `NIVEL_AGL` e `COD_AGL_SUP`;
5. separar os lados por `IND_GRP_BAL`;
6. identificar totalizadores e detalhes por `IND_COD_AGL`;
7. mostrar `DESCR_COD_AGL`;
8. usar `VL_CTA_FIN` com `IND_DC_BAL_FIN`;
9. preservar também os valores iniciais para comparação e auditoria;
10. não inferir a hierarquia pelo prefixo do código.

### 8.4 Conciliação

Para cada linha de detalhe do `J100`:

1. localizar as contas analíticas relacionadas pelo `I052`;
2. obter os saldos finais aplicáveis no `I155`;
3. aplicar corretamente os indicadores de débito e crédito;
4. totalizar sem dupla contagem;
5. confrontar o total calculado com `J100.VL_CTA_FIN`;
6. registrar diferença, status e contas componentes.

### 8.5 Cálculos Prudenciais Posteriores

O balanço do `J100` é a demonstração declarada e o envelope de conferência.
Ele não substitui o detalhe analítico necessário aos motores.

Conforme a `SPEC-011`, o PLRA deve continuar usando:

- `I050`: conta, natureza e hierarquia;
- `I051`: vínculo referencial exato;
- `I155`: saldo final anual;
- metodologia interna versionada: tratamento prudencial;
- `J100`: conferência, consistência e auditoria.

Assim, existem duas responsabilidades complementares:

```text
Apresentar o Balanço Patrimonial
    -> usar J005 + J100

Calcular PLRA e outros componentes analíticos
    -> usar I050 + I051 + I155 + metodologia
    -> reconciliar o resultado patrimonial com I052 + J100
```

## 9. Papel Do I051

O `I051`:

- informa o `COD_CTA_REF` declarado para uma conta do `I050`;
- permite validar e enriquecer a conta pelo plano referencial oficial;
- é usado pela metodologia interna e pelos cálculos prudenciais quando o
  contrato exigir código referencial exato.

O `I051` não:

- define a estrutura visual do Balanço Patrimonial;
- substitui o `J100`;
- relaciona diretamente uma linha do `J100` a uma conta do `I050`;
- deve ser confundido com o `I052`.

## 10. Situação Encontrada No CAPAG

A implementação atual já reconhece e persiste linhas `J100`, mas a pesquisa
identificou divergências em relação ao contrato oficial:

1. o parser persiste `COD_AGL` como `account_code`, favorecendo a interpretação
   incorreta de que ele seria `I050.COD_CTA`;
2. para o leiaute completo, o valor persistido vem de `VL_CTA_INI`, não de
   `VL_CTA_FIN`;
3. não são normalizados campos essenciais como `IND_COD_AGL`, `NIVEL_AGL`,
   `COD_AGL_SUP`, `IND_GRP_BAL`, valores finais e referências a notas;
4. a apresentação reaproveita hierarquia e metadados do `I050`, embora a
   hierarquia declarada do balanço esteja no próprio `J100`;
5. os apontamentos `J100_SEM_I050` e `I050_PATRIMONIAL_SEM_J100` comparam
   diretamente códigos que possuem funções distintas;
6. o vínculo oficial `I050 -> I052 -> J100` ainda não está implementado para a
   conciliação numérica.

Arquivos observados:

- `backend/app/io/ecd_parser.py`;
- `backend/app/repositories/ecd_imports.py`;
- `backend/app/application/ecd_import_service.py`;
- `backend/app/application/declared_service.py`.

Essas constatações são diagnóstico documental. A correção do parser, da
persistência, da API, do frontend, das migrations e dos testes exige execução
governada própria.

## 11. Decisões Consolidadas

1. O balanço declarado será reproduzido a partir do `J100`.
2. A hierarquia visual virá do próprio `J100`.
3. O saldo de encerramento será `VL_CTA_FIN`, com seu indicador.
4. A conferência seguirá `I050 + I052 + I155 -> J100`.
5. O `I051` permanecerá separado, destinado ao plano referencial e à
   metodologia.
6. Os motores prudenciais trabalharão com dados analíticos e usarão o `J100`
   como controle, sem recalcular a partir da tela.
7. Ausência ou inconsistência de `J100` será tratada conforme a obrigatoriedade
   oficial e a elegibilidade da ECD para o exercício anual.
8. Nenhum fallback silencioso por nome, prefixo ou associação direta
   `J100.COD_AGL = I050.COD_CTA` será permitido.

## 12. Limites Da Conclusão

Esta pesquisa resolve:

- qual registro apresenta o Balanço Patrimonial;
- como a estrutura hierárquica deve ser lida;
- qual valor representa o encerramento;
- como o PGE confere o balanço;
- a diferença entre `I051` e `I052`;
- a fronteira entre apresentação contábil e cálculo prudencial.

Esta pesquisa não define:

- quais contas entram ou saem do PLRA;
- deságios de ativos;
- tratamento de passivos condicionais;
- decisões humanas por switches;
- fórmulas de FCA, ROA ou CAPAG-E;
- persistência final das decisões do usuário.

