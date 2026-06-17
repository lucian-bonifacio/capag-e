# Instruções Para Agentes

## 1. Objetivo

Este arquivo orienta agentes de IA, assistentes de código e ferramentas automatizadas na criação de SPECs e TASKs do projeto CAPAG.

O foco deste documento é governar:

- criação de SPECs a partir de PRD, arquitetura e documentos governados;
- criação de TASKs correspondentes a SPECs suficientes;
- decisões técnicas, bloqueios, critérios de aceite e validações que precisam estar explícitos antes de uma TASK.

## 2. Fontes Obrigatórias

Antes de criar ou revisar qualquer SPEC ou TASK, leia as fontes aplicáveis.

Fontes base obrigatórias:

- `docs/product/PRD.md`
- `docs/architecture.md`

Fontes de frontend governadas, quando a SPEC ou TASK envolver UI, telas, componentes, UX ou visual:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Materiais históricos de referência já foram usados para consolidar o PRD e a arquitetura. Não use esses materiais como fonte direta para novas SPECs ou TASKs, salvo autorização explícita do usuário.

Se existirem ADRs, decisões técnicas ou documentos governados adicionais aprovados, eles prevalecem sobre inferências e devem ser considerados antes da SPEC ou TASK.

## 3. Fluxo Obrigatório: PRD -> Arquitetura -> SPEC -> TASK

O fluxo obrigatório é:

```text
PRD + Arquitetura + Docs governados
        ↓
SPECs especializadas
        ↓
TASKs correspondentes
```

Regras:

- SPEC vem antes da TASK.
- TASK nasce de SPEC suficiente.
- Uma SPEC insuficiente não deve virar TASK.
- Se faltar decisão, fonte, contrato, regra, critério de aceite ou validação, registre bloqueio e faça pergunta direta ao usuário.
- Não preencha lacunas técnicas, metodológicas ou normativas com suposição silenciosa.

## 4. Regras Para Criar SPECs

Toda SPEC deve transformar PRD, arquitetura e documentos governados em uma especificação técnica verificável.

Uma SPEC deve explicitar:

- objetivo técnico;
- contexto e problema;
- fontes usadas;
- escopo;
- fora de escopo;
- decisões já aprovadas;
- decisões pendentes;
- contratos;
- responsabilidades por camada ou área;
- dados de entrada e saída;
- estados e erros relevantes;
- critérios de aceite verificáveis;
- estratégia de validação esperada;
- riscos e mitigação;
- bloqueios.

Uma SPEC não deve:

- esconder decisão pendente;
- deixar contrato para a TASK decidir;
- deixar regra de negócio para a TASK decidir;
- deixar critério de aceite subjetivo;
- usar execução de trabalho como substituto de decisão técnica;
- duplicar regra de domínio em camada errada.

Quando a SPEC atravessar mais de uma área, aplique mais de uma lente especializada.

## 5. Lentes Especializadas Para SPECs

### 5.1 Lente Arquitetural

Use quando a SPEC envolver:

- camadas;
- fronteiras;
- contratos;
- responsabilidades;
- ADRs;
- riscos técnicos;
- dependências entre módulos;
- mudança estrutural.

A SPEC deve explicitar:

- dono da regra ou responsabilidade;
- camadas afetadas;
- camadas que não devem ser afetadas;
- contratos de entrada e saída;
- dependências permitidas e proibidas;
- impacto em dados, migração, compatibilidade e exportação;
- auditoria, rastreabilidade e observabilidade;
- critérios arquiteturais de aceite;
- ADRs necessários e bloqueios.

Bloqueie quando a SPEC exigir decisão arquitetural ausente.

### 5.2 Lente Backend FastAPI

Use quando a SPEC envolver:

- rotas FastAPI;
- schemas;
- validação;
- serialização;
- contratos HTTP;
- erros;
- upload ou importação;
- integração da API com domínio, parser, engine ou exportação.

A SPEC deve explicitar:

- endpoint, método e path;
- path params, query params, headers e body;
- schemas de request, response e erro;
- códigos de status;
- validações da API;
- validações delegadas ao domínio, IO, engine ou export;
- contrato consumido pelo frontend;
- representação de valores precisos sem `float`;
- observabilidade e diagnósticos;
- testes de contrato e integração.

Bloqueie quando faltar contrato de API, formato de erro ou separação de responsabilidade.

### 5.3 Lente Frontend React

Use quando a SPEC envolver:

- telas;
- fluxos;
- estados de UI;
- consumo de API;
- tabelas;
- upload;
- erros;
- acessibilidade;
- documentos visuais governados.

A SPEC deve explicitar:

- tela ou componente afetado;
- usuário e fluxo;
- estados de vazio, loading, sucesso, erro, alerta e bloqueio;
- contrato de API consumido;
- dados necessários para renderização;
- tabelas, colunas, filtros, ações e formatação;
- interação e acessibilidade mínima;
- critérios visuais de aceite;
- regra que não pode ficar no frontend.

Para SPECs frontend, observe obrigatoriamente:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Bloqueie quando faltar contrato de API, estado de UI essencial ou critério visual.

### 5.4 Lente QA

Use quando a SPEC precisar definir:

- estratégia de validação;
- critérios de aceite;
- testes unitários;
- testes de integração;
- golden tests;
- fixtures;
- regressão;
- evidências de qualidade.

A SPEC deve explicitar:

- comportamento esperado;
- entradas e saídas;
- critérios verificáveis;
- nível de teste proporcional ao risco;
- fixtures;
- casos nominais;
- casos de borda;
- dados inválidos;
- golden cases quando necessário;
- comandos e evidências esperadas;
- lacunas de cobertura justificadas.

Bloqueie quando critério de aceite não for verificável ou resultado esperado estiver indefinido.

## 6. Regras Para Criar TASKs

TASK nasce de SPEC suficiente.

Não crie TASK quando a SPEC ainda tiver decisão essencial pendente.

Toda TASK deve conter:

- referência à SPEC de origem;
- objetivo da TASK;
- escopo exato;
- fora de escopo;
- passos executáveis;
- arquivos, módulos ou áreas prováveis;
- critérios de aceite herdados ou derivados da SPEC;
- validação esperada;
- riscos;
- bloqueios pendentes, se houver.

TASK não deve decidir:

- arquitetura;
- contrato de API;
- regra de domínio;
- fórmula;
- fonte normativa;
- política de arredondamento;
- padrão visual;
- estratégia de teste crítica.

Se a TASK precisar decidir qualquer item acima, a SPEC está incompleta.

Uma SPEC pode gerar uma ou mais TASKs. Ao dividir TASKs:

- mantenha cada TASK executável de forma independente;
- preserve dependências entre TASKs;
- não duplique escopo;
- não crie TASK ampla demais;
- mantenha critérios de aceite verificáveis.

## 7. Decisões Técnicas E Bloqueios

Registre bloqueio e faça pergunta direta ao usuário quando faltar:

- decisão arquitetural;
- contrato de API;
- fonte normativa;
- regra de domínio;
- regra de cálculo;
- política de precisão ou arredondamento;
- comportamento de tela;
- estado de erro, loading, vazio, sucesso, alerta ou bloqueio;
- critério de aceite verificável;
- resultado esperado para teste;
- estratégia de teste necessária.

Não contorne bloqueios por conveniência.

Não trate código existente, testes ou worklogs como fonte normativa suficiente para criar ou alterar regra prudencial, contábil, fiscal, financeira ou metodológica.

## 8. Documentos De Frontend Governados

Os documentos de frontend são fonte obrigatória para SPECs e TASKs que envolvam UI, visual, componentes, layout ou experiência de uso:

- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

Esses documentos definem:

- tokens visuais;
- regras objetivas de componentes;
- padrões de tela;
- CSS variables e aliases compatíveis com Tailwind/shadcn.

SPECs frontend devem declarar explicitamente quais regras desses documentos afetam o escopo.

TASKs frontend devem herdar essas restrições da SPEC de origem.

## 9. Domain Engine Específico Do Projeto

A lente de domínio/engine é específica do CAPAG e de domínios prudenciais/contábeis equivalentes.

Não generalize automaticamente para outros projetos sem adaptação explícita.

Use essa lente quando uma SPEC envolver:

- domínio prudencial ou contábil;
- engine de cálculo;
- regras de CAPAG-E;
- PLR;
- FCO;
- auditoria;
- classificação prudencial;
- valores contábeis, fiscais, financeiros ou prudenciais;
- `Decimal`;
- arredondamento;
- integração de cálculo com parser, API, frontend ou exportação.

SPECs com essa lente devem explicitar:

- conceitos, entidades, estados e invariantes afetados;
- dono da regra prudencial;
- entradas conceituais exigidas;
- saídas, alertas e diagnósticos;
- fórmula, método ou critério prudencial;
- fonte normativa ou decisão aprovada;
- uso obrigatório de `Decimal`;
- escala, quantização e política de arredondamento;
- onde o arredondamento ocorre;
- onde o arredondamento não deve ocorrer;
- tratamento de zero, nulo, sinal, período, exercício e moeda;
- evidências para auditoria;
- etapas intermediárias preservadas;
- contrato de saída para API, frontend ou exportação;
- golden cases e testes esperados.

Bloqueie quando houver:

- regra prudencial indefinida;
- fórmula indefinida;
- política de arredondamento indefinida;
- fonte normativa ausente;
- tentativa de usar `float`;
- tentativa de duplicar regra no frontend, API ou exportação;
- ausência de golden case para comportamento de alto risco.
