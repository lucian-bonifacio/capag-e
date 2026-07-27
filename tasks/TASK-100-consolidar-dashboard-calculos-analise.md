# TASK-100 - Consolidar dashboard de calculos da analise

## SPEC De Origem

- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`

## Dependencias

- `TASK-054-exportacao-e-testes-contrato-capag-e.md`
- `TASK-060-exportacao-e-testes-evidencias-ativos.md`
- `TASK-066-exportacao-e-testes-dfc-fca.md`
- `TASK-072-exportacao-e-testes-roa-plra.md`
- `TASK-099-exportacao-testes-plra.md`

## Objetivo

Consolidar PLRA, DFC/FCA, ROA, evidencias e CAPAG-E em uma unica tela operacional da analise, organizada como dashboard com secoes ou abas, preservando os calculos no backend e a rastreabilidade dos snapshots.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-004-modulo-3-contrato-capag-e-plra-fca-roa.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`
- `specs/SPEC-006-modulo-5-dfc-direta-fca.md`
- `specs/SPEC-007-modulo-6-motor-roa-plra.md`
- `specs/SPEC-011-modulo-1b-motor-plra.md`
- `tasks/README.md`
- `docs/frontend/DESIGN_TOKENS.md`
- `docs/frontend/UI_COMPONENT_RULES.md`
- `docs/frontend/SCREEN_PATTERNS.md`
- `frontend/src/styles/globals.css`

## Escopo Exato

- Criar uma tela/dashboard da analise que concentre o estado de PLRA, DFC/FCA, ROA, evidencias e CAPAG-E.
- Organizar cada componente em secoes, abas ou paineis verificaveis, com status, valor, formula, bloqueios, pendencias e acoes principais.
- Manter comandos de calculo e recalculo acionando exclusivamente os endpoints backend existentes.
- Preservar acesso a auditorias, decisoes manuais e exportacoes ja existentes, por drill-down, dialogs, secoes internas ou rotas secundarias quando o volume exigir.
- Ajustar a navegacao lateral para favorecer o fluxo `Importar ECD -> Dashboard da analise -> detalhes/auditoria/exportacao`.
- Reutilizar contratos API e componentes frontend existentes sempre que couber.
- Garantir que valores monetarios, percentuais, formulas e codigos usem `.tnum`.
- Atualizar testes frontend focados no fluxo consolidado.

## Fora De Escopo

- Alterar contratos de API.
- Alterar formulas, regras prudenciais, fontes normativas, arredondamento ou metodologia.
- Recalcular PLRA, DFC/FCA, ROA, evidencias ou CAPAG-E no frontend.
- Remover auditoria, memoria de calculo, pendencias ou bloqueios.
- Implementar novo motor backend.
- Alterar padrao visual governado, tokens ou componentes base sem autorizacao especifica.
- Gerar laudo CAPAG-E.

## Passos Executaveis

1. Ler as SPECs e documentos frontend aplicaveis.
2. Mapear as telas atuais de PLRA, DFC/FCA, ROA, evidencias e CAPAG-E e seus estados de carregamento, vazio, sucesso, erro e bloqueio.
3. Definir a composicao do dashboard usando os padroes governados de shell, topbar, dashboard, cards, badges, botoes, tabs ou secoes.
4. Implementar a tela consolidada sem duplicar regra de calculo.
5. Ajustar rotas e menu lateral para reduzir fragmentacao da jornada.
6. Preservar rotas ou views de detalhe quando forem necessarias para auditoria volumosa.
7. Atualizar testes frontend para importacao, abertura da analise, execucao de calculos e navegacao entre componentes.
8. Executar validacoes via Docker Compose.

## Arquivos Ou Areas Provaveis

- `frontend/src/App.tsx`
- `frontend/src/routes/`
- `frontend/src/api/`
- `frontend/src/test/`
- `frontend/src/styles/globals.css`
- `logs/`
- `ROADMAP.md`

## Criterios De Aceite

- A analise possui uma tela principal unica para acompanhar PLRA, DFC/FCA, ROA, evidencias e CAPAG-E.
- O usuario consegue, a partir da ECD importada, abrir a analise e verificar o estado de todos os componentes sem trocar entre varias telas primarias.
- Cada componente mostra valor, status, formula ou metodo aplicavel, bloqueios, pendencias e acao de calcular/recalcular quando aplicavel.
- Auditorias, decisoes manuais e exportacoes continuam acessiveis.
- O frontend nao recalcula nem transforma valores prudenciais retornados pela API.
- Navegacao direta sem ECD importada volta para `Importar ECD`.
- A UI segue os documentos governados de frontend.

## Validacao Esperada

- Executar `docker compose --profile test run --rm frontend-tests`.
- Quando houver E2E aplicavel, executar `docker compose --profile test run --rm frontend-e2e`.
- Registrar limitacoes objetivas se alguma validacao E2E nao existir ou nao couber no escopo.

## Riscos

- Risco: criar uma tela grande demais e perder auditabilidade.
  Mitigacao: manter resumo no dashboard e detalhes em secoes, tabs, dialogs ou rotas secundarias.

- Risco: misturar resultado final com componente parcial ou bloqueado.
  Mitigacao: preservar badges, status canonicos, bloqueios e limitacoes retornados pelo backend.

- Risco: duplicar regra prudencial no frontend.
  Mitigacao: usar somente valores e status serializados pela API.

## Bloqueios Pendentes

- Execucao depende de autorizacao futura do usuario.
- Homologacao das TASKs de calculos pendentes deve orientar ajustes finos de UX antes ou durante a execucao desta TASK.
