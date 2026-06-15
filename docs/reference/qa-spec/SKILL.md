---
name: qa-spec
description: Apoiar a criação e revisão de SPECs do CAPAG com impacto em qualidade e testes. Use quando uma SPEC precisar definir estratégia de validação, critérios de aceite, pytest, testes unitários, integração, golden tests, regressão, fixtures ou evidências de qualidade.
---

# QA Spec CAPAG

## Objetivo

Esta skill apoia a criação de qualquer SPEC do CAPAG que envolva qualidade, validação ou testes, garantindo que critérios de aceite, estratégia de testes, fixtures, golden cases e evidências estejam claros antes de uma task ser escrita.

Use quando uma SPEC tocar comportamento testável, parser ECD, cálculo, exportação Excel, API, frontend, regressão, fixtures, golden tests, integração ou validação manual. Não use para implementar testes, criar task, aprovar documento ou substituir `document-control`.

## Pergunta Central

Ao criar ou revisar uma SPEC que envolva qualidade ou testes, responda sempre:

> Para executar a task futura com segurança, quais evidências, testes, fixtures, golden cases e critérios de aceite precisam estar explícitos para comprovar que o comportamento esperado foi entregue sem regressão?

Se a SPEC não puder definir isso com as decisões existentes, registre bloqueio ou decisão pendente.

## Fontes

Antes de apoiar uma SPEC, leia o mínimo necessário:

- `AGENTS.md`;
- SPEC alvo, quando já existir;
- PRD, arquitetura, ADRs e documentos oficiais relacionados ao escopo;
- testes existentes em `tests/` apenas quando for necessário confirmar padrão, fixture ou cobertura atual;
- código relacionado apenas quando for necessário confirmar comportamento, risco ou ponto de integração.

Se houver divergência material entre fontes, pare e faça uma pergunta direta ao usuário antes de prosseguir.

## Visão QA Obrigatória

Ao criar ou revisar uma SPEC que envolva qualidade ou testes, garanta que ela cubra os blocos aplicáveis.

Comportamento esperado:

- regra ou fluxo que precisa ser comprovado;
- entradas, saídas, estados e erros;
- critérios de aceite verificáveis;
- fora de escopo e comportamento não garantido.

Estratégia de testes:

- testes unitários para regras puras;
- testes de integração para fluxo entre camadas;
- golden tests para cálculo, ECD, Excel ou resultado fixo esperado;
- testes de API quando houver contrato HTTP;
- testes de frontend/build quando houver UI;
- validação manual quando automação não for proporcional.

Dados de teste:

- fixtures necessárias;
- casos nominais;
- casos de borda;
- dados inválidos ou incompletos;
- massas históricas ou regressivas quando aplicável;
- resultado esperado e justificativa.

Risco e regressão:

- risco funcional, arquitetural, numérico ou operacional;
- comportamento existente que não pode mudar;
- compatibilidade com contratos, Excel, API ou UI;
- necessidade de teste de regressão;
- ausência de teste e justificativa aceitável.

Evidência:

- comando de validação esperado;
- arquivo de teste ou fixture esperado;
- métrica de sucesso;
- logs, screenshots ou artefatos quando aplicável;
- critério objetivo para considerar a task pronta.

## Regras de Teste CAPAG

A SPEC deve respeitar:

- `pytest` para backend;
- testes unitários para regra pura;
- testes de integração para fluxo entre camadas;
- golden tests para cálculo, ECD, Excel ou resultado fixo esperado;
- validação proporcional ao risco;
- justificativa explícita quando teste automatizado não for executado;
- valores contábeis, fiscais, financeiros e prudenciais sem `float`.

## Fluxo para SPEC

1. Identifique o comportamento que precisa ser comprovado.
2. Separe critérios de aceite funcionais, técnicos e regressivos.
3. Defina nível de teste por risco: unitário, integração, golden, API, frontend, build ou manual.
4. Especifique fixtures, entradas, saídas e resultados esperados.
5. Inclua casos de borda, erros e dados inválidos.
6. Defina comandos de validação e evidências esperadas.
7. Registre lacunas de cobertura e justificativas aceitáveis.
8. Declare riscos, decisões pendentes e fora de escopo.

## Critérios QA de Aceite

Uma SPEC que envolva qualidade ou testes só está clara quando permite responder:

- qual comportamento será comprovado;
- qual teste será criado ou atualizado;
- qual fixture ou golden case será usado;
- qual entrada e resultado esperado validam a regra;
- qual regressão precisa ser evitada;
- qual comando deve ser executado;
- qual evidência comprova sucesso;
- quando ausência de teste é aceitável.

## Bloqueios

Pare imediatamente, não tente contornar a regra e faça uma pergunta direta ao usuário quando houver:

- critério de aceite não verificável;
- resultado esperado indefinido;
- regra de cálculo ou arredondamento indefinida;
- ausência de fixture ou golden case para comportamento de alto risco;
- teste necessário sem dados de entrada;
- risco de regressão sem estratégia de validação;
- divergência material entre SPEC, código e comportamento esperado.

## Formato Esperado da SPEC

Ao redigir texto para uma SPEC ou seção QA de SPEC, use esta estrutura em Markdown. Preserve o front matter e o `Controle Documental` definidos pela governança do projeto quando estiver editando o documento inteiro.

```markdown
# [Título da SPEC]

## Contexto de Qualidade

[Explique o comportamento que precisa ser comprovado e o risco envolvido.]

## Estratégia de Testes

### Unitários

- [Regras puras e casos esperados.]

### Integração

- [Fluxos entre camadas e contratos.]

### Golden Tests

- [Entrada fixa, resultado esperado e justificativa.]

### Frontend/API/Build

- [Validações de contrato, UI ou build quando aplicável.]

## Dados de Teste

- [Fixtures, massas, casos nominais, bordas e inválidos.]

## Critérios QA de Aceite

- [ ] [Critério verificável que uma task futura consiga confirmar.]

## Comandos e Evidências

- Comando:
- Evidência esperada:

## Riscos e Lacunas

- [Risco, lacuna de cobertura, justificativa ou decisão pendente.]

## Fora de Escopo

- [O que a SPEC não deve validar.]
```

## Limites

Esta skill não cria task, não implementa teste, não aprova documento e não substitui `document-control`.

O produto esperado é orientação ou texto para a parte QA de uma SPEC, com critérios e evidências suficientes para que a task futura não precise decidir estratégia de teste durante a execução.
