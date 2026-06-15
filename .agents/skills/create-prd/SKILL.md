---
name: create-prd
description: Criar Product Requirements Documents por meio de entrevista reflexiva. Use quando o usuário quiser transformar uma ideia, conceito de produto, funcionalidade, fluxo ou requisito vago em um PRD final com layout Markdown fixo, fazendo uma pergunta por vez e guiando respostas incertas.
---

# Criar PRD

## Objetivo

Use esta skill para entrevistar o usuario e produzir a versao final de um Product Requirements Document a partir de uma ideia incompleta, exploratoria ou pouco estruturada.

A skill e generica e nao deve assumir empresa, repositorio, governanca de projeto, processo de produto, stack de implementacao ou path especifico, salvo quando o usuario informar.

## Regras da Entrevista

Comece fazendo exatamente uma pergunta de abertura:

```text
Qual é a sua ideia? O que você tem em mente?
```

Depois da resposta do usuario, use ate quatro perguntas principais adicionais como padrao, sempre uma por vez. Nao sacrifique confiabilidade para cumprir esse limite: se uma informacao ausente puder tornar o PRD fraco, enganoso ou internamente inconsistente, continue perguntando de forma focada.

Trate a conversa como reflexiva: o usuario pode nao saber responder tudo, entao guie com alternativas concretas, exemplos e tradeoffs, sem transformar a entrevista em um formulario longo.

Use estas areas de pergunta, adaptando a formulacao a ideia:

- ideia e contexto;
- usuarios-alvo e casos de uso;
- problema, resultado desejado e criterios de sucesso;
- escopo funcional, fluxos e limites;
- restricoes, riscos, dependencias, decisoes em aberto e referencias existentes.

Nao faca todas as perguntas de uma vez. Faca uma pergunta, espere a resposta e decida a proxima melhor pergunta.

## Pedido de Referencias

Em algum momento da entrevista, preferencialmente depois de entender a ideia e antes de gerar o PRD, pergunte se existem referencias que devam ser consideradas.

A pergunta deve ser simples e pode citar exemplos:

```text
Existe alguma referencia que eu deva considerar? Pode ser documento, link, produto parecido, tela, planilha, requisito antigo, regra interna, concorrente ou qualquer material que ajude.
```

Se o usuario nao tiver referencias, continue normalmente. Se houver referencias, use-as como insumo de produto, sem copiar texto automaticamente e sem assumir que elas substituem as respostas da entrevista.

## Tratamento de Lacunas

Infira decisoes implicitas razoaveis quando forem de baixo risco e consistentes com as respostas do usuario. Registre premissas importantes dentro do PRD.

Faca mais de cinco perguntas quando isso for necessario para preservar a confiabilidade do PRD. Mantenha perguntas adicionais focadas e uma por vez.

Se o usuario pedir para gerar o PRD cedo, produza o melhor PRD possivel e registre pontos fracos em `Riscos e Pontos em Aberto`.

## Geracao do PRD

Quando houver informacao suficiente, gere o PRD final em Markdown usando exatamente o layout abaixo. Preserve titulos e ordem. Nao adicione, remova ou renomeie secoes, salvo se o usuario mudar explicitamente o template.

Gere o PRD como entrega consolidada da entrevista, registrando premissas, riscos e pontos em aberto quando necessario.

Escreva em linguagem clara de produto. Evite detalhes de implementacao, salvo quando forem restricoes necessarias ou informacao explicita do usuario.

## Criterios de Confiabilidade

Ao redigir o PRD, sustente cada secao com evidencias, decisoes explicitas, limites claros e criterios testaveis. Se uma informacao importante nao tiver evidencia ou decisao suficiente, registre como premissa, risco ou ponto em aberto.

Mantenha a diferenca entre `Nao Objetivos` e `Fora do Escopo`:

- `Nao Objetivos`: resultados que o produto nao pretende alcancar.
- `Fora do Escopo`: funcionalidades, entregas ou capacidades que nao entram nesta versao.

Exemplo:

- Nao objetivo: reduzir churn no curto prazo.
- Fora do escopo: criar programa de fidelidade.

## Layout Obrigatorio de Saida

```markdown
---
name: prd
description: Documento de requisitos de produto que define problema, objetivos, usuários, escopo, requisitos, critérios de sucesso e restrições.
---

# PRD - [Nome do Produto ou Funcionalidade]

## 1. Contexto

## 2. Problema

## 3. Objetivos

## 4. Não Objetivos

## 5. Usuários e Personas

## 6. Escopo Funcional

## 7. Requisitos do Produto

## 8. Fluxos Principais

## 9. Critérios de Sucesso

## 10. Restrições e Premissas

## 11. Riscos e Pontos em Aberto

## 12. Fora do Escopo

## 13. Critérios de Aceite do PRD
```

## Checklist de Qualidade

Antes de finalizar, verifique:

- a primeira pergunta da entrevista foi a pergunta obrigatoria de abertura;
- as perguntas foram feitas uma por vez;
- o usuario foi perguntado sobre referencias existentes;
- o PRD segue exatamente o layout obrigatorio;
- as premissas estao explicitas quando o usuario nao soube responder algo;
- os criterios de sucesso sao observaveis ou mensuraveis quando possivel;
- cada secao esta apoiada por evidencias, decisoes explicitas, limites claros ou criterios testaveis;
- `Nao Objetivos` descreve resultados nao pretendidos;
- `Fora do Escopo` descreve funcionalidades ou entregas excluidas desta versao;
- escopo e fora de escopo nao se contradizem;
- riscos e decisoes em aberto nao foram escondidos como requisitos.
