# Nova Especificacao Conceitual - Modulo de Analise Comportamental e Reclassificacao

## 1. Decisao conceitual central

O sistema deve passar a suportar duas leituras paralelas da mesma ECD:

1. **Analise Declarada**
   - Mantem o comportamento atual do sistema.
   - Usa o `I051` como classificacao referencial declarada na ECD.
   - Calcula `PLR`, `FCO` e `CAPAG-e` a partir da metodologia vigente.
   - Responde a pergunta: "qual e o resultado se a ECD for aceita conforme entregue?"

2. **Analise Comportamental**
   - Cria uma segunda leitura da ECD.
   - Nao usa o `I051` como verdade decisoria principal.
   - Reinterpreta a substancia da conta a partir de saldos, lancamentos, historicos, contrapartidas, recorrencia e materialidade.
   - Responde a pergunta: "o que os movimentos mostram que essa conta realmente parece ser?"

As duas analises devem coexistir. A analise comportamental nao apaga, substitui ou reescreve a classificacao original da ECD. Ela preserva o `I051` como dado declarado e o confronta com a substancia economica observada.

## 2. Objetivo do novo modulo

O modulo de analise comportamental existe para reduzir ao maximo a interferencia humana na revisao metodologica, sem eliminar rastreabilidade.

Seus objetivos sao:

- detectar contas cuja classificacao referencial declarada parece incompatível com o comportamento real;
- sugerir familia contabil provavel para cada conta;
- atribuir score de confianca e evidencias objetivas;
- gerar um cenario alternativo de `PLR` e `CAPAG-e` com base na reclassificacao comportamental;
- explicar a diferenca entre o resultado declarado e o resultado comportamental;
- direcionar revisao humana apenas para contas ambiguas, sensiveis ou materialmente relevantes.

## 3. O que permanece no sistema atual

O modulo novo nao deve invalidar o motor atual.

Devem permanecer:

- parser proprio da ECD;
- processamento em memoria;
- ausencia de banco de dados na V2;
- ausencia de persistencia de sessoes;
- uso de `Decimal` para valores contabeis e prudenciais;
- `I051` como fonte da classificacao declarada;
- metodologia interna versionada para o calculo oficial atual;
- exportacao apenas em `Excel`;
- frontend sem regra de negocio central duplicada.

A analise atual continua necessaria porque representa a leitura formal da ECD entregue.

## 4. Nova leitura paralela da ECD

A analise comportamental deve construir uma camada propria a partir da ECD completa.

Ela deve usar principalmente:

- `I050` para plano de contas e hierarquia;
- `I051` como classificacao original declarada;
- `I155` para saldos anuais;
- `I200` e `I250` para lancamentos e partidas;
- historicos dos lancamentos e partidas;
- contrapartidas por lancamento;
- recorrencia dos movimentos;
- natureza tipica do saldo;
- materialidade dos valores.

Registros adicionais, como `I052`, `I355`, `J100` e `J150`, podem ser considerados em evolucoes futuras, desde que nao alterem a premissa da V2 sem decisao arquitetural explicita.

## 5. Pipeline conceitual

O fluxo conceitual do novo modulo e:

1. Receber a ECD ja parseada e normalizada.
2. Montar o razao por conta contabil.
3. Identificar contrapartidas por lancamento.
4. Calcular perfil comportamental por conta.
5. Aplicar regras deterministicas por familia contabil.
6. Calcular score por familia.
7. Escolher familia vencedora quando houver confianca suficiente.
8. Mapear familia/subfamilia para codigo referencial sugerido.
9. Comparar classificacao sugerida com o `I051` original.
10. Gerar acao recomendada: manter, reclassificar, revisar ou sem conclusao.
11. Calcular cenario comportamental de `PLR` e `CAPAG-e`.
12. Explicar diferencas entre a analise declarada e a analise comportamental.

## 6. Modelo de saida esperado

Para cada conta analisada, o modulo deve produzir:

- codigo da conta;
- nome da conta;
- caminho hierarquico;
- codigo referencial original informado no `I051`;
- familia comportamental sugerida;
- codigo referencial sugerido, quando aplicavel;
- score de confianca;
- nivel de confianca;
- acao recomendada;
- evidencias positivas;
- evidencias negativas;
- justificativa auditavel;
- impacto potencial no `PLR`;
- impacto potencial na `CAPAG-e`, quando houver `FCO` final utilizavel.

No nivel consolidado, o sistema deve produzir:

- `PLR` pela analise declarada;
- `PLR` pela analise comportamental;
- `CAPAG-e` pela analise declarada;
- `CAPAG-e` pela analise comportamental;
- diferenca entre os cenarios;
- contas que explicam a diferenca;
- contas com reclassificacao automatica no cenario comportamental;
- contas enviadas para revisao.

## 7. Politica de confianca

O modulo deve reduzir interferencia humana por meio de uma politica objetiva de confianca.

Diretriz inicial:

- **Alta confianca**: aplicar automaticamente no cenario comportamental.
- **Media confianca**: sugerir reclassificacao e marcar revisao recomendada.
- **Baixa confianca**: nao reclassificar automaticamente.
- **Sem conclusao**: manter a classificacao declarada apenas como referencia comparativa.

O sistema deve ser conservador quando houver:

- score baixo;
- diferenca pequena entre primeira e segunda familia;
- poucos lancamentos;
- lancamentos compostos demais;
- historicos genericos;
- conta sintética;
- conta de encerramento;
- conta transitória;
- comportamento instavel entre periodos;
- materialidade elevada com evidencia insuficiente;
- tributos;
- partes relacionadas;
- patrimonio liquido;
- classificacoes sensiveis.

Regra orientadora:

> Melhor enviar uma conta material ou ambigua para revisao do que produzir uma reclassificacao automatica com confianca falsa.

## 8. Familias contabeis iniciais

O MVP do modulo comportamental deve comecar por familias com comportamento mais caracteristico:

1. Bancos e disponibilidades
2. Clientes
3. Fornecedores
4. Adiantamento a fornecedores
5. Imobilizado
6. Despesas operacionais
7. Receitas

Essas familias permitem validar a tese com menor risco porque possuem sinais relativamente fortes em saldos, contrapartidas e recorrencia.

## 9. Relacao com a revisao humana

O objetivo nao e eliminar completamente o especialista, mas mudar o papel da revisao humana.

No fluxo atual, o usuario pode precisar interpretar muitas contas.

No fluxo comportamental desejado:

- o sistema resolve automaticamente casos obvios no cenario comportamental;
- o sistema explica divergencias relevantes;
- o usuario revisa apenas casos ambiguos, sensiveis ou materiais;
- toda decisao humana deve ficar rastreavel;
- revisoes humanas podem virar precedentes em uma evolucao futura.

Na V2, precedentes nao devem depender de banco de dados ou persistencia operacional. Caso sejam usados, devem permanecer como artefatos internos versionados ou dados temporarios da sessao.

## 10. Relacao com o motor atual de PLR e CAPAG

O motor atual continua sendo a base da analise declarada.

Para a analise comportamental, existem duas possibilidades futuras:

1. Gerar apenas um relatorio de divergencias e impactos potenciais.
2. Gerar um cenario completo de `PLR` e `CAPAG-e` comportamental.

A segunda opcao e mais poderosa, mas exige cuidado para separar claramente:

- resultado declarado pela ECD;
- resultado comportamental sugerido;
- decisoes manuais do usuario;
- evidencias e justificativas;
- diferencas entre cenarios.

Nenhuma reclassificacao comportamental deve alterar silenciosamente o resultado declarado.

## 11. Relacao com exportacao e laudo

A exportacao futura deve permitir demonstrar as duas leituras.

Abas ou secoes possiveis:

- resumo dos cenarios;
- comparativo entre analise declarada e comportamental;
- contas reclassificadas no cenario comportamental;
- contas mantidas;
- contas em revisao;
- evidencias por conta;
- justificativas;
- impacto por conta no `PLR`;
- impacto consolidado na `CAPAG-e`.

Essa estrutura fortalece a defesa tecnica porque mostra:

- o que foi declarado na ECD;
- o que o comportamento contabil sugere;
- quais evidencias sustentam a divergencia;
- quanto a divergencia altera o resultado.

## 12. Fronteiras arquiteturais da V2

Para permanecer compativel com a arquitetura atual, o novo modulo nao deve introduzir na V2:

- banco de dados;
- persistencia de sessoes;
- historico operacional de importacoes;
- administracao de regras pela interface;
- exportacao `CSV`;
- classificacao por IA generativa como nucleo decisorio;
- regra de negocio duplicada no frontend.

O nucleo decisorio deve ser deterministico, auditavel e testavel.

IA generativa pode ser avaliada futuramente apenas como camada auxiliar para:

- agrupar historicos semelhantes;
- sugerir sinonimos;
- explicar decisoes em linguagem natural;
- apoiar casos ambiguos.

A decisao principal deve permanecer em regras, scores e evidencias estruturadas.

## 13. Linguagem recomendada

Evitar dizer que o sistema "ignora o I051" de forma absoluta.

Formula recomendada:

> O modulo comportamental preserva o `I051` como classificacao declarada, mas nao o usa como verdade decisoria principal na segunda analise. Ele confronta a classificacao declarada com a substancia economica observada nos movimentos da conta.

Essa formulacao protege a rastreabilidade e deixa clara a coexistencia entre forma declarada e substancia observada.

## 14. Conclusao conceitual

O novo modulo deve ser tratado como um modulo completo de segunda analise, e nao como simples upgrade do classificador atual.

A arquitetura conceitual desejada e:

```text
ECD
 ├─ Analise Declarada
 │   └─ usa I051 como classificacao referencial declarada
 │
 └─ Analise Comportamental
     ├─ monta razao por conta
     ├─ calcula perfil comportamental
     ├─ aplica regras e scores
     ├─ sugere familia e referencial
     ├─ compara com o I051
     └─ gera cenario comportamental e evidencias
```

A ECD mostra a forma declarada. A analise comportamental mostra a substancia observada.

O valor do modulo esta justamente em preservar as duas visoes, comparar seus efeitos e reduzir a intervencao humana aos casos em que a automacao nao deve decidir sozinha.
