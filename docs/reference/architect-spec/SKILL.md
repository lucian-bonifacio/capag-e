---
name: architect-spec
description: Apoiar a criação e revisão de SPECs do CAPAG com impacto arquitetural. Use quando uma SPEC precisar definir camadas, fronteiras, contratos, responsabilidades, ADRs, riscos técnicos ou critérios arquiteturais para orientar tasks futuras.
---

# Architect Spec CAPAG

## Objetivo

Esta skill apoia a criação de qualquer SPEC do CAPAG que envolva impacto arquitetural, garantindo que a visão arquitetural necessária esteja clara antes de uma task ser escrita.

Use quando houver necessidade de criar, revisar ou completar uma SPEC que toque arquitetura, camadas, fronteiras, contratos, responsabilidades entre módulos, riscos técnicos ou ADRs. Não use para implementar código, criar task, aprovar documento ou substituir `document-control`.

## Pergunta Central

Ao criar ou revisar uma SPEC que envolva impacto arquitetural, responda sempre:

> Para executar as atividades previstas depois, qual visão arquitetural precisa estar explícita para evitar ambiguidade, acoplamento indevido, duplicação de regra ou mudança estrutural não aprovada?

Se essa visão não puder ser escrita com as decisões existentes, a SPEC deve registrar bloqueio ou decisão pendente.

## Fontes

Antes de apoiar uma SPEC, leia o mínimo necessário:

- `AGENTS.md`;
- `docs/architecture/ARCHITECTURE.md`;
- ADRs relacionados em `docs/decisions/`;
- PRD e documentos oficiais relacionados ao escopo;
- SPEC alvo, quando já existir;
- arquivos do código apenas quando for necessário confirmar responsabilidade atual, acoplamento ou risco técnico.


## Visão Arquitetural Obrigatória

Ao criar ou revisar uma SPEC, garanta que ela cubra os blocos aplicáveis.

Domínio:

- objetivo técnico da mudança e problema arquitetural envolvido;
- dono da regra de negócio ou regra prudencial;
- invariantes, estados e conceitos de domínio afetados;
- critérios de precisão numérica, escala e arredondamento;
- local onde o arredondamento ocorre e local onde ele não deve ocorrer.

Camadas:

- camadas afetadas e camadas que não devem ser afetadas;
- responsabilidade de cada módulo envolvido;
- fronteiras entre API, domínio, parser ECD, engine, exportação e frontend;
- dependências permitidas e dependências proibidas;
- efeitos colaterais, persistência ou ausência explícita de persistência.

Dados e contratos:

- contratos de entrada e saída entre camadas;
- fluxo de dados e transformação dos dados;
- compatibilidade com contratos existentes, versões de API, schemas, arquivos ECD, workbooks Excel e consumidores atuais;
- necessidade de migração, adaptação ou preservação de dados históricos;
- impacto em exportação Excel, mantendo exportação como projeção/apresentação de dados já calculados.

Qualidade operacional:

- requisitos de auditoria, rastreabilidade e explicabilidade;
- logs, erros esperados, diagnósticos, métricas ou pontos de observabilidade necessários;
- impacto esperado em testes unitários, integração ou golden tests;
- critérios arquiteturais de aceite verificáveis.

Riscos e decisões:

- riscos técnicos e mitigação;
- fora de escopo;
- necessidade de ADR antes de seguir;
- decisões pendentes que impedem a SPEC de virar task.

## Baseline CAPAG

Preserve as responsabilidades oficiais:

- `src/capag/api/`: rotas FastAPI, schemas, validação de entrada e serialização;
- `src/capag/domain/`: modelos, estados, invariantes, conceitos e alertas;
- `src/capag/io/`: leitura, parsing e normalização de ECD;
- `src/capag/engine/`: cálculos de PLR, FCO, CAPAG-e e auditoria;
- `src/capag/export/`: serialização de workbook Excel com openpyxl;
- `src/capag/assets/`: artefatos internos versionados usados pelo motor;
- `web/`: React/Vite, sem regra de negócio central.

Não introduza banco de dados, persistência de sessões, novo framework, novo motor de exportação ou novo padrão arquitetural dentro de uma SPEC sem ADR e aprovação explícita.

## Fluxo para SPEC

1. Identifique o objetivo da SPEC e o comportamento que ela pretende viabilizar.
2. Liste as camadas e módulos afetados.
3. Defina responsabilidades por camada, separando o que deve mudar do que deve permanecer estável.
4. Descreva contratos, dados, estados e fluxo entre módulos.
5. Verifique restrições de stack, `Decimal`, arredondamento, compatibilidade, observabilidade, frontend sem regra central, parser sem cálculo prudencial e exportação sem recálculo.
6. Aponte ADRs necessários antes da SPEC ou como bloqueio dentro dela.
7. Escreva critérios arquiteturais de aceite que uma task futura consiga verificar.
8. Declare riscos, dependências e fora de escopo.

## Critérios Arquiteturais de Aceite

Uma SPEC com impacto arquitetural só está clara quando permite responder:

- qual camada é dona de cada responsabilidade;
- quais módulos podem depender de quais outros módulos;
- qual contrato será consumido ou produzido;
- onde a regra de negócio será executada;
- onde a regra de negócio não pode ser executada;
- onde precisão, escala e arredondamento serão definidos;
- como compatibilidade e migração serão tratadas;
- como o resultado será rastreado ou auditado;
- como erros, logs ou diagnósticos necessários serão observados;
- que tipo de teste comprova que a arquitetura foi respeitada;
- qual decisão precisa de ADR antes de virar task.

## ADR

Marque ADR como obrigatório na SPEC quando a mudança envolver:

- stack;
- banco de dados, DuckDB ou persistência;
- paths oficiais;
- mudança estrutural ou difícil de reverter;
- quebra ou alteração relevante de fronteira entre camadas;
- mudança de responsabilidade entre módulos;
- nova dependência relevante;
- novo padrão arquitetural;
- fluxo SDD ou governança;
- compatibilidade ou migração com impacto amplo;
- critério metodológico sensível de cálculo, arredondamento, auditoria ou exportação.

A SPEC não deve esconder decisão arquitetural pendente como detalhe de task futura.

## Bloqueios

Pare imediatamente, não tente contornar a regra e faça uma pergunta direta ao usuário quando houver:

- ausência de decisão arquitetural necessária para escrever a SPEC;
- necessidade de ADR ainda não registrada;
- tentativa de mover responsabilidade central sem decisão aprovada;
- regra de cálculo, arredondamento ou auditoria indefinida;
- risco de duplicar regra prudencial no frontend;
- risco de recalcular regra de negócio na exportação;
- divergência material entre documento e código.

## Formato Esperado da SPEC

Ao redigir texto para uma SPEC ou seção arquitetural de SPEC, use esta estrutura em Markdown. Preserve o front matter e o `Controle Documental` definidos pela governança do projeto quando estiver editando o documento inteiro.

```markdown
# [Título da SPEC]

## Contexto e Problema

[Responda à Pergunta Central e explique o problema arquitetural que a SPEC precisa resolver.]

## Visão Arquitetural

### Domínio

- [Regra, conceito, invariante, precisão, escala ou arredondamento afetado.]

### Camadas e Responsabilidades

- [Camadas afetadas, módulos responsáveis, fronteiras e dependências permitidas/proibidas.]

### Dados e Contratos

- [Contratos, entradas, saídas, fluxo de dados, compatibilidade, migração e impacto em Excel.]

### Qualidade Operacional

- [Auditoria, rastreabilidade, observabilidade, erros esperados, diagnósticos e testes.]

## Critérios Arquiteturais de Aceite

- [ ] [Critério verificável que uma task futura consiga confirmar.]

## Riscos e ADRs Necessários

- [Risco, mitigação, decisão pendente ou ADR obrigatório antes de virar task.]

## Fora de Escopo

- [O que a SPEC não deve resolver.]
```

## Limites

Esta skill não cria task, não implementa código, não aprova documento e não substitui `document-control`.

O produto esperado é orientação ou texto para a parte arquitetural de uma SPEC, com visão suficiente para que a task futura não precise decidir arquitetura durante a execução.
