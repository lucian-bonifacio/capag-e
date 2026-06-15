---
name: frontend-react-spec
description: Apoiar a criação e revisão de SPECs do CAPAG com impacto em frontend React/Vite. Use quando uma SPEC precisar definir telas, fluxos, estados de UI, ag-grid-react, consumo de API, validações de UX, acessibilidade, erros ou interação sem duplicar regra de negócio.
---

# Frontend React Spec CAPAG

## Objetivo

Esta skill apoia a criação de qualquer SPEC do CAPAG que envolva frontend React/Vite, garantindo que telas, fluxos, estados, contratos com API, tabelas, interação e critérios de UX estejam claros antes de uma task ser escrita.

Use quando uma SPEC tocar `web/`, React, Vite, `ag-grid-react`, telas, filtros, upload, análise, exportação, consumo de API, estados de carregamento, erros, acessibilidade ou experiência de usuário. Não use para implementar código, criar task, aprovar documento ou substituir `document-control`.

## Pergunta Central

Ao criar ou revisar uma SPEC que envolva frontend, responda sempre:

> Para executar a task futura com segurança, qual comportamento de tela, estado de UI, contrato de API, interação e critério visual precisa estar explícito para evitar decisão de UX ou regra de negócio durante a execução?

Se a SPEC não puder definir isso com as decisões existentes, registre bloqueio ou decisão pendente.

## Fontes

Antes de apoiar uma SPEC, leia o mínimo necessário:

- `AGENTS.md`;
- `docs/design/DESIGN.md`, quando existir;
- PRD e documentos oficiais relacionados ao escopo;
- SPEC alvo, quando já existir;
- contratos backend relacionados;
- arquivos em `web/` apenas quando for necessário confirmar tela, componente, estado ou padrão atual.

Se houver divergência material entre fontes, pare e faça uma pergunta direta ao usuário antes de prosseguir.

## Visão Frontend Obrigatória

Ao criar ou revisar uma SPEC que envolva frontend, garanta que ela cubra os blocos aplicáveis.

Fluxo e tela:

- usuário, objetivo e fluxo de interação;
- tela, componente ou região afetada;
- navegação, transição, modal, painel, tabela ou formulário;
- estados de vazio, carregamento, sucesso, erro, alerta e bloqueio;
- comportamento responsivo quando aplicável.

Contrato com API:

- endpoint ou contrato consumido;
- dados necessários para renderização;
- transformação permitida no frontend;
- campos estáveis exigidos para tabelas e componentes;
- tratamento de erro, alerta e estado intermediário;
- compatibilidade com contratos existentes.

Tabelas e dados:

- uso de `ag-grid-react` quando a SPEC envolver tabelas;
- colunas, labels, ordenação, filtros, agrupamentos e ações;
- identificação de linha, seleção, edição e confirmação;
- formatação de valores sem recalcular regra de negócio;
- exportação, download ou visualização quando aplicável.

UX e acessibilidade:

- comandos disponíveis e estados desabilitados;
- feedback visual necessário;
- mensagens de erro ou alerta acionáveis;
- navegação por teclado e acessibilidade básica quando aplicável;
- consistência com padrões visuais existentes.

Qualidade:

- critérios visuais de aceite;
- casos de dados pequenos, grandes, ausentes ou inconsistentes;
- impacto em testes de componente, integração ou build;
- risco de regressão em fluxo de usuário existente.

## Regras de Camada

A SPEC deve preservar:

- frontend como consumidor de contratos e estados;
- regra prudencial e regra de negócio central fora do frontend;
- cálculos contábeis, fiscais, financeiros e prudenciais no backend/engine;
- formatação visual separada de regra de negócio;
- contratos de API claros para evitar inferência no cliente.

Não duplique regra sensível no frontend. Não use frontend para corrigir, recalcular ou reinterpretar resultado que deveria vir do backend.

## Fluxo para SPEC

1. Identifique o fluxo de usuário e a tela ou componente afetado.
2. Defina estados de UI e comportamento esperado.
3. Especifique contrato de API consumido e dados necessários.
4. Descreva tabelas, colunas, ações, filtros e formatações.
5. Separe formatação de regra de negócio.
6. Inclua erros, alertas, loading, vazio e bloqueios.
7. Escreva critérios visuais e funcionais de aceite para a task futura.
8. Declare riscos, decisões pendentes e fora de escopo.

## Critérios Frontend de Aceite

Uma SPEC que envolva frontend só está clara quando permite responder:

- qual tela, componente ou fluxo será criado ou alterado;
- quais dados a UI precisa receber;
- quais estados a UI deve representar;
- quais ações o usuário pode executar;
- como erro, alerta, loading e vazio aparecem;
- quais tabelas, colunas e filtros existem;
- qual regra não pode ser implementada no frontend;
- quais critérios visuais ou testes comprovam o comportamento.

## Bloqueios

Pare imediatamente, não tente contornar a regra e faça uma pergunta direta ao usuário quando houver:

- contrato de API ausente ou indefinido;
- regra de negócio exigida na UI;
- comportamento visual ou fluxo de usuário indefinido;
- estado de erro, loading ou vazio necessário mas não especificado;
- tentativa de duplicar cálculo prudencial no frontend;
- divergência material entre design, PRD, contrato de API e código existente.

## Formato Esperado da SPEC

Ao redigir texto para uma SPEC ou seção frontend de SPEC, use esta estrutura em Markdown. Preserve o front matter e o `Controle Documental` definidos pela governança do projeto quando estiver editando o documento inteiro.

```markdown
# [Título da SPEC]

## Contexto e Fluxo de Usuário

[Explique o fluxo, tela ou componente que a SPEC precisa resolver.]

## Visão Frontend

### Tela e Estados

- [Tela, componente, estados de loading, vazio, sucesso, erro, alerta e bloqueio.]

### Contrato com API

- [Dados consumidos, campos necessários, erros e compatibilidade.]

### Tabelas e Interações

- [ag-grid, colunas, filtros, seleção, ações e formatação.]

### UX e Acessibilidade

- [Feedback, mensagens, comandos, teclado e restrições visuais.]

## Critérios Frontend de Aceite

- [ ] [Critério verificável que uma task futura consiga confirmar.]

## Riscos e Decisões Pendentes

- [Risco, decisão pendente ou bloqueio.]

## Fora de Escopo

- [O que a SPEC não deve resolver.]
```

## Limites

Esta skill não cria task, não implementa frontend, não define regra de negócio, não aprova documento e não substitui `document-control` ou `design-lab-capag`.

O produto esperado é orientação ou texto para a parte frontend de uma SPEC, com comportamento de UI suficiente para que a task futura não precise decidir UX, contrato ou regra durante a execução.
