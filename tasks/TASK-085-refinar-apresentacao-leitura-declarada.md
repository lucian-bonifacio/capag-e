# TASK-085 - Refinar apresentacao da leitura declarada

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-040-criar-ui-camada-declarada.md`
- `TASK-041H-integrar-ui-analise-importada-real.md`
- `TASK-041J-validar-fluxo-end-to-end-declarada.md`
- `TASK-041M-gerenciar-importacoes-ecd-existentes.md`

## Objetivo

Melhorar a apresentacao da leitura declarada por conta para que o usuario consiga distinguir contas estruturais, contas analiticas, pendencias de cobertura, valores relevantes e dados declarados pela ECD sem interpretar a tabela como classificacao CAPAG-E final.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`
- `tasks/TASK-041H-integrar-ui-analise-importada-real.md`
- `tasks/TASK-041J-validar-fluxo-end-to-end-declarada.md`

## Escopo Exato

- Renomear a tabela de `Classificação recebida da API` para nomenclatura fiel ao objetivo da tela, como `Leitura declarada por conta`.
- Criar resumo acionavel antes da tabela com total de contas, quantidade por status e acesso rapido aos grupos de pendencia.
- Criar filtros rapidos por status declaratorio/metodologico, incluindo no minimo `Todas`, `Com vinculo`, `Sem vinculo`, `Codigo fora da base oficial`, `Sem regra` e `Mapeadas`.
- Separar visualmente contas estruturais/sinteticas de contas analiticas/classificaveis, evitando que contas de hierarquia com valor zero dominem a primeira leitura.
- Destacar contas com valor base relevante e permitir ordenacao ou foco por materialidade sem recalcular regra de negocio.
- Trocar status tecnicos longos por labels legiveis na UI, preservando o codigo tecnico em detalhe, tooltip ou area secundaria.
- Separar visualmente `Declaracao ECD` de `Cobertura metodologica`, mantendo claro o que veio do arquivo e o que foi interpretado pelo sistema.
- Adicionar detalhe por conta com dados usados na leitura declarada: conta `I050`, vinculo `I051`, saldo `I155`, regra ou ausencia de regra, status final e acao recomendada.
- Criar modo ou filtro `Pendencias` para focar registros que exigem acao: sem vinculo, codigo fora da base oficial e sem regra metodologica.
- Exibir hierarquia de contas de forma recolhivel ou agrupada usando os padroes governados em `docs/frontend`, especialmente `Accordion`, `BalanceGroup`, `AccountRow` e/ou `BalanceLedger` quando aplicaveis.
- Expor no contrato de contas declaradas os metadados hierarquicos do `I050`: tipo da conta, nivel, conta superior e ordem de exibicao.
- Renderizar a hierarquia visual usando os metadados formais do `I050`, sem inferir grupos por prefixo de codigo.
- Manter a UI consumindo apenas os payloads da API, sem recalcular matcher, regra prudencial, PLRA, FCO, FCA, ROA ou CAPAG-E no frontend.

## Fora De Escopo

- Alterar regra prudencial, metodologia interna, matcher ou plano referencial oficial.
- Criar classificacao CAPAG-E final.
- Criar reclassificacao comportamental.
- Criar editor de regras metodologicas.
- Persistir decisoes humanas ou revisoes de conta.
- Salvar novos artefatos de laudo ou Excel.

## Passos Executaveis

1. Ler a tela atual da camada declarada, contratos de API e componentes/estilos existentes.
2. Definir modelo de apresentacao que separe resumo, filtros, pendencias, hierarquia e detalhe por conta.
3. Ajustar componentes da tela declarada para nomenclatura mais precisa e status legiveis.
4. Implementar filtros rapidos e modo `Pendencias` sem alterar dados retornados pelo backend.
5. Implementar apresentacao hierarquica ou agrupada conforme `docs/frontend`.
6. Implementar detalhe por conta preservando fonte declaratoria e cobertura metodologica.
7. Criar ou ajustar testes frontend para filtros, labels, detalhe, pendencias e hierarquia.
8. Ajustar E2E para garantir que a tela continua abrindo a analise real sem recalcular regra no frontend.
9. Validar manualmente com `ECD 2024 DATAPACK.txt` e `ECD 2024 INVENTCLOUD.txt` em execucoes separadas.

## Arquivos Ou Areas Provaveis

- `frontend/src/routes/DeclaredLayerPage.tsx`
- `frontend/src/App.css`
- `frontend/src/api/declared.ts`
- `frontend/src/test/runner.test.tsx`
- `frontend/e2e/declared-layer.spec.ts`
- `backend/app/schemas/declared.py`
- `backend/app/api/declared.py`
- `backend/tests/test_declared_api.py`

## Criterios De Aceite

- A tela deixa claro que se trata de leitura declarada/diagnostico da ECD, nao classificacao CAPAG-E final.
- Contas estruturais/sinteticas nao dominam a primeira leitura da tabela.
- O usuario consegue filtrar rapidamente pendencias e status principais.
- Status tecnicos longos aparecem em linguagem legivel, com codigo tecnico ainda acessivel.
- Contas com valor relevante ficam mais faceis de identificar.
- O detalhe por conta mostra fonte declaratoria e cobertura metodologica sem recalcular resultado.
- A hierarquia de contas usa padroes governados de `docs/frontend`.
- A hierarquia de contas vem de `I050` (`IND_CTA`, `NIVEL`, `COD_CTA_SUP` e ordem/linha), nao de prefixos inferidos no frontend.
- Frontend nao recalcula regra de negocio nem altera status retornado pelo backend.
- DATAPACK e INVENTCLOUD continuam abrindo e exibindo resultados da camada declarada.

## Validacao Esperada

- Executar testes frontend via `docker compose`.
- Executar build frontend via `docker compose`.
- Executar E2E Playwright via Docker Compose.
- Validar manualmente, em testes separados, `docs/reference/ecd-example/ECD 2024 DATAPACK.txt` e `docs/reference/ecd-example/ECD 2024 INVENTCLOUD.txt`.
- Conferir ausencia de `float` em arquivos alterados.

## Riscos

- Risco: a UI parecer uma classificacao final CAPAG-E.
  Mitigacao: nomenclatura explicita de leitura declarada e separacao entre declaracao ECD e cobertura metodologica.

- Risco: hierarquia esconder pendencias relevantes.
  Mitigacao: manter modo `Pendencias` e resumo acionavel sempre disponiveis.

- Risco: frontend introduzir regra de negocio por conveniencia.
  Mitigacao: usar apenas campos retornados pela API e restringir calculos locais a contagem/filtro/apresentacao.

## Bloqueios Pendentes

Nenhum.
