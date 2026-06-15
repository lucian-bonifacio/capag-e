---
name: domain-engine-spec
description: Apoiar a criação e revisão de SPECs do CAPAG com impacto em domínio ou engine. Use quando uma SPEC precisar definir conceitos, invariantes, regras prudenciais, cálculos, auditoria, Decimal, arredondamento, PLR, FCO, CAPAG-e ou integração com parser e exportação.
---

# Domain Engine Spec CAPAG

## Objetivo

Esta skill apoia a criação de qualquer SPEC do CAPAG que envolva domínio, regras prudenciais ou engine de cálculo, garantindo que conceitos, invariantes, fórmulas, precisão, auditoria e critérios verificáveis estejam claros antes de uma task ser escrita.

Use quando uma SPEC tocar `src/capag/domain/`, `src/capag/engine/`, cálculo de PLR, FCO, CAPAG-e, auditoria, classificação prudencial, valores contábeis, `Decimal`, arredondamento ou integração de cálculo com parser/API/exportação. Não use para implementar código, criar task, aprovar documento ou substituir `document-control`.

## Pergunta Central

Ao criar ou revisar uma SPEC que envolva domínio ou engine, responda sempre:

> Para executar a task futura com segurança, qual regra, conceito, fórmula, estado, precisão, arredondamento e evidência de auditoria precisa estar explícita para evitar cálculo ambíguo ou decisão prudencial durante a execução?

Se a SPEC não puder definir isso com as decisões existentes, registre bloqueio ou decisão pendente.

## Fontes

Antes de apoiar uma SPEC, leia o mínimo necessário:

- `AGENTS.md`;
- `docs/architecture/ARCHITECTURE.md`;
- PRD e documentos oficiais relacionados ao escopo;
- SPEC alvo, quando já existir;
- ADRs relacionados em `docs/decisions/`;
- arquivos em `src/capag/domain/` ou `src/capag/engine/` apenas quando for necessário confirmar regra, conceito ou acoplamento atual;
- arquivos em `src/capag/io/`, `src/capag/api/` ou `src/capag/export/` apenas quando a SPEC depender de entrada, contrato ou saída.

Se houver divergência material entre fontes, pare e faça uma pergunta direta ao usuário antes de prosseguir.

## Fontes Normativas

Regra contábil, fiscal, financeira, prudencial, fórmula, arredondamento, classificação ou critério metodológico exige fonte normativa identificada.

Use como fonte normativa apenas:

- documentos oficiais em `docs/reference/`;
- manuais, normas, portarias ou notas técnicas trazidas para o repositório;
- ADRs ou documentos oficiais `APPROVED`;
- fonte indicada explicitamente pelo usuário.

Código existente, testes e worklogs são evidência do comportamento atual, não fonte normativa suficiente para criar ou alterar regra.

Não use pesquisa na internet automaticamente para preencher lacuna normativa. Quando uma fonte externa for necessária, pare, peça autorização ou fonte ao usuário e registre que a fonte precisa de validação humana antes de virar SPEC.

## Visão Domain/Engine Obrigatória

Ao criar ou revisar uma SPEC que envolva domínio ou engine, garanta que ela cubra os blocos aplicáveis.

Domínio:

- conceitos, entidades, estados e invariantes afetados;
- dono da regra de negócio ou regra prudencial;
- entradas conceituais exigidas para a regra;
- saídas e alertas produzidos;
- condições de erro, ausência de dado ou dado inconsistente.

Cálculo e precisão:

- fórmula, método ou critério prudencial a aplicar;
- fonte normativa ou decisão aprovada da regra;
- uso obrigatório de `Decimal` para valores contábeis, fiscais, financeiros ou prudenciais;
- escala, quantização e política de arredondamento;
- local onde o arredondamento ocorre e onde ele não deve ocorrer;
- tratamento de zero, nulo, sinal, período, exercício e moeda quando aplicável.

Auditoria e rastreabilidade:

- evidências necessárias para explicar o resultado;
- origem dos dados usados no cálculo;
- etapas intermediárias que precisam ser preservadas;
- justificativas, alertas e diagnósticos esperados;
- compatibilidade com exportação Excel sem recálculo.

Integração:

- dados esperados do parser ECD ou API;
- contrato de saída para API, frontend ou exportação;
- responsabilidades que pertencem ao domínio;
- responsabilidades que pertencem ao engine;
- responsabilidades que não devem ser duplicadas em frontend ou exportação.

Qualidade:

- casos nominais e de borda;
- fixtures ou golden cases necessários;
- tolerância esperada, quando houver;
- critérios de regressão para evitar mudança silenciosa de resultado;
- impacto esperado em testes unitários, integração ou golden tests.

## Regras de Camada

A SPEC deve preservar:

- `src/capag/domain/` como camada de conceitos, invariantes, estados e alertas;
- `src/capag/engine/` como camada de cálculo, auditoria e regra prudencial;
- `src/capag/io/` como camada de leitura, parsing e normalização de ECD;
- `src/capag/api/` como camada de contrato e serialização, sem regra prudencial central;
- `src/capag/export/` como camada de apresentação Excel, sem recálculo de regra;
- `web/` como consumidor de resultados, sem regra de negócio central.

Não use `float` para valores contábeis, fiscais, financeiros ou prudenciais. Não esconda fórmula, arredondamento ou critério metodológico como detalhe de task futura.

## Fluxo para SPEC

1. Identifique a regra, conceito ou cálculo envolvido.
2. Defina entradas, saídas, estados, alertas e erros.
3. Especifique fórmula, fonte da regra e política de precisão/arredondamento.
4. Separe responsabilidade de domínio, engine, parser, API, exportação e frontend.
5. Descreva evidências de auditoria e rastreabilidade.
6. Defina compatibilidade com resultados existentes e exportação Excel.
7. Escreva critérios de aceite verificáveis para a task futura.
8. Declare riscos, decisões pendentes e fora de escopo.

## Critérios Domain/Engine de Aceite

Uma SPEC que envolva domínio ou engine só está clara quando permite responder:

- qual regra ou conceito será criado ou alterado;
- quais entradas são necessárias;
- qual resultado é produzido;
- qual fórmula, método ou decisão orienta o cálculo;
- onde `Decimal`, escala e arredondamento são aplicados;
- quais casos de borda devem ser cobertos;
- como o resultado será auditado ou explicado;
- onde a regra não pode ser recalculada;
- quais testes comprovam o comportamento.

## Bloqueios

Pare imediatamente, não tente contornar a regra e faça uma pergunta direta ao usuário quando houver:

- regra prudencial, fórmula ou critério metodológico indefinido;
- política de arredondamento ou escala indefinida;
- fonte normativa ou decisão aprovada ausente;
- necessidade de pesquisa externa sem autorização ou sem validação humana;
- tentativa de usar código existente como única fonte normativa;
- tentativa de usar `float` em valor contábil, fiscal, financeiro ou prudencial;
- tentativa de duplicar regra no frontend, API ou exportação;
- divergência material entre documento, código e resultado esperado;
- ausência de golden case quando o risco exigir resultado fixo verificável.

## Formato Esperado da SPEC

Ao redigir texto para uma SPEC ou seção domain/engine de SPEC, use esta estrutura em Markdown. Preserve o front matter e o `Controle Documental` definidos pela governança do projeto quando estiver editando o documento inteiro.

```markdown
# [Título da SPEC]

## Contexto e Regra

[Explique o conceito, regra ou cálculo que a SPEC precisa resolver e identifique a fonte normativa.]

## Visão Domain/Engine

### Domínio

- [Conceitos, invariantes, estados, entradas, saídas e alertas.]

### Cálculo e Precisão

- [Fórmula, fonte normativa, Decimal, escala, arredondamento e casos de borda.]

### Auditoria e Rastreabilidade

- [Evidências, etapas intermediárias, diagnósticos e explicabilidade.]

### Integração

- [Entrada do parser/API, saída para API/frontend/exportação e responsabilidades por camada.]

## Critérios Domain/Engine de Aceite

- [ ] [Critério verificável que uma task futura consiga confirmar.]

## Golden Cases e Testes Esperados

- [Caso fixo, entrada, resultado esperado e justificativa.]

## Riscos e Decisões Pendentes

- [Risco, decisão pendente, fonte externa pendente de validação humana ou bloqueio.]

## Fora de Escopo

- [O que a SPEC não deve resolver.]
```

## Limites

Esta skill não cria task, não implementa engine, não define regra normativa sem fonte aprovada, não aprova documento e não substitui `document-control` ou `architect-spec`.

O produto esperado é orientação ou texto para a parte domain/engine de uma SPEC, com regra e precisão suficientes para que a task futura não precise decidir cálculo durante a execução.
