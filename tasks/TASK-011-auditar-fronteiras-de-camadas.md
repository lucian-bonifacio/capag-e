# TASK-011 - Auditar fronteiras de camadas

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-002-auditar-estrutura-minima-repositorio.md`
- `TASK-003-criar-estrutura-backend-minima.md`
- `TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`

Esta TASK so deve ser executada depois que a estrutura minima do repositorio, a estrutura backend minima e o estado das SPECs estiverem tratados ou auditados.

## Objetivo

Auditar e documentar as fronteiras esperadas entre `api`, `application`, `domain`, `io`, `engine`, `repositories`, `export` e `report`, preparando uma matriz de responsabilidades para orientar TASKs futuras sem implementar codigo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- relatorio esperado de `tasks/reports/TASK-002-auditoria-estrutura-minima.md`
- relatorio esperado de `tasks/reports/TASK-005-auditoria-specs.md`

## Escopo Exato

- Criar uma matriz documental de responsabilidades por camada.
- Registrar dependencias permitidas e proibidas entre camadas.
- Registrar proibicoes explicitas:
  - frontend nao parseia ECD;
  - frontend nao recalcula `PLRA`, `FCA`, `ROA` ou `CAPAG-E`;
  - exportacao nao recalcula motores;
  - laudo nao recalcula motores;
  - `domain` nao depende de FastAPI, SQLAlchemy, React ou openpyxl;
  - regra prudencial sensivel fica no backend, nos motores e contratos apropriados.
- Identificar lacunas ou ambiguidades que precisem de TASKs futuras.
- Registrar bloqueios quando fronteiras dependerem de SPEC funcional posterior.

## Fora De Escopo

- Criar ou alterar codigo.
- Criar imports, pacotes, interfaces ou classes.
- Criar endpoints.
- Criar schemas Pydantic.
- Criar modelos SQLAlchemy.
- Criar repositories reais.
- Criar motores.
- Criar exportacao ou laudo.
- Alterar arquitetura ou SPECs.
- Definir regra prudencial, formula, arredondamento ou golden cases.
- Atualizar `tasks/README.md`.

## Passos Executaveis

1. Ler os relatorios das TASKs 002 e 005.
2. Ler as secoes de responsabilidades em `docs/architecture.md` e `SPEC-001`.
3. Criar relatorio em `tasks/reports/TASK-011-fronteiras-de-camadas.md`.
4. Montar matriz com uma linha por camada.
5. Para cada camada, registrar responsabilidades, entradas, saidas, dependencias permitidas e dependencias proibidas.
6. Registrar lacunas e ambiguidades sem resolve-las.
7. Sugerir proximas TASKs pequenas quando houver fronteiras que precisem de detalhamento.
8. Validar que nenhum codigo, SPEC ou documento operacional foi alterado durante a execucao.

## Arquivos Ou Areas Provaveis

- `tasks/reports/TASK-011-fronteiras-de-camadas.md`
- `docs/architecture.md` apenas para leitura
- `specs/SPEC-001-modulo-0-fundacao-governada.md` apenas para leitura
- `backend/` apenas para leitura, se existir

## Criterios De Aceite

- Existe relatorio em `tasks/reports/TASK-011-fronteiras-de-camadas.md`.
- O relatorio cita a SPEC de origem.
- O relatorio contem matriz para `api`, `application`, `domain`, `io`, `engine`, `repositories`, `export` e `report`.
- Cada camada tem responsabilidades e proibicoes registradas.
- O relatorio identifica dependencias permitidas e proibidas.
- Lacunas sao registradas sem alteracao de arquitetura ou SPEC.
- Nenhum codigo, SPEC, documento operacional ou config e alterado.

## Validacao Esperada

- Executar `test -f tasks/reports/TASK-011-fronteiras-de-camadas.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `tasks/reports/TASK-011-fronteiras-de-camadas.md`.
- Conferir manualmente que o relatorio nao cria contrato funcional, regra de dominio, formula prudencial, schema, endpoint ou classe.

## Riscos

- Risco: matriz documental virar decisao arquitetural nova.
  Mitigacao: limitar a matriz ao que ja esta aprovado em PRD, arquitetura e SPEC-001.

- Risco: fronteiras ficarem abstratas demais para orientar TASKs futuras.
  Mitigacao: registrar dependencias permitidas e proibidas de forma objetiva.

- Risco: antecipar contrato funcional de modulo posterior.
  Mitigacao: bloquear qualquer detalhe que dependa de SPEC funcional posterior.

## Bloqueios Pendentes

Bloqueada ate a execucao ou revisao das TASKs 002, 003 e 005.

Permanece bloqueado qualquer trabalho que tente implementar codigo, criar contratos funcionais, alterar arquitetura, alterar SPECs ou definir regra prudencial durante esta TASK.
