# Planejamento geral dos ajustes do sistema

## Objetivo geral

Organizar a arquitetura, a documentacao e o fluxo de evolucao do `capag_v2` antes de executar mudancas funcionais amplas.

O objetivo nao e implementar tudo de uma vez. O objetivo e quebrar a reorganizacao em tarefas pequenas, sequenciais e verificaveis, para que cada uma possa ser analisada e aprovada antes da execucao.

## Problema que este plano resolve

O projeto evoluiu em varias frentes:

- backend `FastAPI`;
- motor Python em `src/capag/`;
- frontend `React + Vite`;
- UI legada `Streamlit`;
- specs numeradas de `spec-00` a `spec-12`;
- novas ideias em `docs/reference/`;
- tasks historicas em `tasks/`;
- instrucoes operacionais em `README.md`, `AGENTS.md`, `CLAUDE.md`;
- skills em `.agents/skills/` e `.claude/skills/`.

Hoje ha sinais de desalinhamento entre esses materiais. Antes de implementar novas capacidades, o projeto precisa deixar clara a fonte de verdade, a organizacao das specs, a arquitetura esperada e o caminho de evolucao.

## Principios do plano

- Primeiro alinhar documentacao e arquitetura.
- Depois criar tasks executaveis.
- Depois alterar codigo.
- Depois atualizar skills/agentes.
- Nao misturar mudanca documental, backend, frontend, design e skills na mesma execucao.
- Reconhecer a arquitetura original da V2 em memoria, mas decidir explicitamente se a nova arquitetura passara a ter banco de dados e persistencia.
- Manter proibicoes que continuam independentes do banco: sem `DuckDB`, sem CSV como exportacao oficial e sem regra de negocio duplicada no frontend.
- Preservar `Decimal` no backend para valores contabeis e prudenciais.
- Preservar `openpyxl` como motor de exportacao Excel.

## Organizacao revisada por modulos

Este planejamento passa a ser organizado por modulos dentro de `tmp_deu_a_louca/`.

### Modulo 0 - Organizacao, arquitetura e design

Pasta:

- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/`

Finalidade:

- organizar fonte de verdade;
- organizar specs;
- definir arquitetura-alvo;
- definir arquitetura de rotas do React;
- definir organizacao de pastas do frontend;
- definir design system;
- definir estrategia de testes e validacao;
- definir higiene de repositorio e artefatos;
- consolidar a propria pasta temporaria de planejamento;
- decidir arquitetura de banco de dados e persistencia antes dos modulos funcionais;
- alinhar `README.md`, `AGENTS.md`, `CLAUDE.md`;
- alinhar tasks e skills.

Este modulo vem antes dos modulos funcionais porque o sistema precisa voltar a ter direcao arquitetural clara.

### Modulo 1 - Camada declarada

Pasta:

- `tmp_deu_a_louca/modulo-01-camada-declarada/`

Finalidade:

- organizar a leitura declarada atual do sistema;
- adaptar a realidade descrita em `docs/reference/ajuste_modulo_principal.md`;
- separar plano referencial oficial de metodologia interna;
- corrigir impactos em assets, motor, API, frontend, exportacao e testes;
- preservar `I051` como classificacao declarada da ECD.

Este modulo nao e a analise comportamental. Ele organiza o resultado oficial declarado baseado em `ECD + I051 + metodologia versionada`.

### Modulo 2 - CAPAG Reclassificada

Pasta:

- `tmp_deu_a_louca/modulo-02-capag-reclassificada/`

Finalidade:

- planejar a segunda leitura da ECD;
- preservar a classificacao declarada, mas confronta-la com comportamento observado;
- montar razao por conta;
- calcular perfis comportamentais;
- aplicar regras deterministicas por familia contabil;
- gerar score, confianca, evidencias e justificativas;
- comparar resultado declarado e resultado reclassificado;
- permitir revisao humana;
- planejar exportacao comparativa;
- considerar banco de dados e persistencia conforme decisao transversal do modulo 0.

### Modulo 3 - Contrato CAPAG-E, PLRA, FCA e ROA

Pasta:

- `tmp_deu_a_louca/modulo-03-contrato-capag-e-plra-fca-roa/`

Finalidade:

- oficializar a linguagem canonica da `CAPAG-E`;
- mapear `PLR ajustado` para `PLRA`;
- separar `FCO` de `FCA`;
- definir metodos, formulas, status e bloqueios;
- criar contrato comum para API, frontend, exportacao e laudo.

Este modulo e fundacional para os modulos 4 a 7.

### Modulo 4 - Evidencias, justificativas e avaliacao de ativos

Pasta:

- `tmp_deu_a_louca/modulo-04-evidencias-avaliacao-ativos/`

Finalidade:

- estruturar evidencias por ajuste;
- definir materialidade;
- definir justificativas do analista;
- tratar ativos com liquidacao forcada;
- definir bloqueios e ressalvas que afetam `PLRA` e laudo.

### Modulo 5 - DFC direto completo e FCA

Pasta:

- `tmp_deu_a_louca/modulo-05-dfc-direto-fca/`

Finalidade:

- evoluir `FCO` para `DFC` direta completa;
- separar fluxos operacionais, investimento e financiamento;
- calcular `FCA`;
- auditar lancamentos e pendencias;
- alimentar o metodo `CAPAG-E = PLRA + FCA`.

### Modulo 6 - Motor ROA + PLRA

Pasta:

- `tmp_deu_a_louca/modulo-06-motor-roa-plra/`

Finalidade:

- implementar o caminho alternativo `CAPAG-E = ROA + PLRA`;
- classificar contas de resultado;
- calcular `ROA`;
- tratar pressoes complementares de caixa;
- integrar evidencias e pendencias.

### Modulo 7 - Gerador de laudo CAPAG-E

Pasta:

- `tmp_deu_a_louca/modulo-07-gerador-laudo-capag-e/`

Finalidade:

- transformar resultados, evidencias, bloqueios e ressalvas em laudo estruturado;
- consumir `PLRA`, `FCA`, `ROA` e `CAPAG-E` ja calculados;
- gerar exportacao de laudo sem recalcular motores.

### Modulo 8 - Governanca de metodologia

Pasta:

- `tmp_deu_a_louca/modulo-08-governanca-metodologia/`

Finalidade:

- alinhar manuais, specs, assets, codigo, testes e laudo;
- criar rastreabilidade metodologica;
- definir validacoes automatizadas;
- atualizar `README.md`, `AGENTS.md`, `CLAUDE.md` e skills por ultimo.

## Sequencia inicial proposta

1. Auditar documentos e conflitos de fonte de verdade.
2. Criar indice oficial das specs e classificar specs atuais.
3. Oficializar a arquitetura-alvo do repositorio.
4. Planejar rotas explicitas no React.
5. Planejar reorganizacao das pastas do frontend.
6. Criar documento de design visual do frontend.
7. Definir estrategia de testes e validacao.
8. Definir higiene de repositorio e artefatos.
9. Decidir banco de dados e persistencia.
10. Consolidar `tmp_deu_a_louca/` para eliminar duplicidade.
11. Atualizar `README.md`, `AGENTS.md` e `CLAUDE.md` somente depois das decisoes anteriores.
12. Revisar tasks e skills somente depois dos documentos operacionais.
13. Planejar a camada declarada.
14. Oficializar o plano referencial oficial e a metodologia interna.
15. Planejar ajustes de assets, motor, API, frontend, exportacao, banco e testes da camada declarada.
16. Planejar o modulo 2 de CAPAG reclassificada/comportamental.
17. Planejar persistencia de perfis, scores, evidencias, revisoes e precedentes conforme decisao de banco.
18. Planejar contrato canonico `CAPAG-E`, `PLRA`, `FCA` e `ROA`.
19. Planejar evidencias, justificativas, materialidade e avaliacao de ativos.
20. Planejar DFC direto completo e `FCA`.
21. Planejar motor `ROA + PLRA`.
22. Planejar gerador de laudo `CAPAG-E`.
23. Planejar governanca final de manuais, specs, assets, metodologia e skills.

## Como usar estes arquivos

Este arquivo e o indice geral.

As tarefas detalhadas ficam nas subpastas `modulo-*`.

Os arquivos soltos da primeira versao `01-*.md` a `13-*.md` foram substituidos pelos modulos e nao fazem mais parte da leitura oficial.

Antes de executar uma tarefa:

- ler o arquivo correspondente;
- confirmar se o escopo esta correto;
- ajustar o texto se necessario;
- aprovar a execucao daquela tarefa;
- somente entao implementar.

## Fora do escopo deste planejamento

- Implementar rotas React agora.
- Reorganizar codigo agora.
- Alterar specs oficiais agora.
- Alterar skills agora.
- Rodar refatoracoes automaticas.
- Criar banco de dados, persistencia ou administracao de regras pela interface sem decisao arquitetural propria.
