# TASK-011A - Criar artefato governado de fronteiras de camadas

## SPEC De Origem

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

## Dependencias

- `TASK-011-auditar-fronteiras-de-camadas.md`
- `TASK-011B-reorganizar-documentacao-oficial-arquitetura.md`

Esta TASK so deve ser executada depois que a auditoria de fronteiras de camadas estiver homologada e a documentacao oficial de arquitetura estiver reorganizada em `docs/architecture/`.

## Objetivo

Criar um artefato governado complementar de arquitetura para registrar as fronteiras entre camadas backend, responsabilidades, dependencias permitidas e proibidas, sem alterar a arquitetura aprovada nem criar contratos funcionais.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `logs/LOG-011-auditar-fronteiras-de-camadas.md`

## Escopo Exato

- Criar `docs/architecture/layer-boundaries.md`.
- Registrar que o artefato complementa `docs/architecture/architecture.md` e nao substitui a arquitetura principal.
- Consolidar a matriz de fronteiras para:
  - `api`;
  - `application`;
  - `domain`;
  - `io`;
  - `engine`;
  - `repositories`;
  - `export`;
  - `report`.
- Para cada camada, registrar:
  - responsabilidades;
  - entradas;
  - saidas;
  - dependencias permitidas;
  - dependencias proibidas.
- Registrar proibicoes transversais ja aprovadas:
  - frontend nao parseia ECD;
  - frontend nao recalcula `PLRA`, `FCA`, `ROA` ou `CAPAG-E`;
  - frontend nao decide classificacao comportamental;
  - frontend nao aplica metodologia prudencial;
  - frontend nao altera status retornado pelo backend;
  - exportacao nao recalcula motores;
  - laudo nao recalcula motores;
  - `domain` nao depende de FastAPI, SQLAlchemy, React ou openpyxl.
- Registrar lacunas que dependem de implementacao futura, sem resolve-las.
- Registrar que detalhes funcionais de endpoints, schemas, models, payloads, motores, persistencia, exportacao e laudo pertencem a SPECs/TASKs funcionais posteriores.

## Fora De Escopo

- Alterar `docs/architecture/architecture.md`.
- Alterar PRD.
- Alterar SPECs.
- Alterar TASKs existentes.
- Alterar `tasks/README.md`.
- Alterar `AGENTS.md`.
- Criar codigo.
- Criar imports, interfaces, classes, endpoints, schemas, models, repositories, motores, exportacao ou laudo.
- Definir contrato de API.
- Definir regra de dominio.
- Definir formula prudencial, fonte normativa, politica de precisao/arredondamento ou golden cases.
- Criar validacao automatizada de imports entre camadas.

## Passos Executaveis

1. Ler `logs/LOG-011-auditar-fronteiras-de-camadas.md`.
2. Ler as secoes de responsabilidades e dependencias em `docs/architecture/architecture.md`.
3. Ler `specs/SPEC-001-modulo-0-fundacao-governada.md`.
4. Criar `docs/architecture/layer-boundaries.md`.
5. Consolidar a matriz de fronteiras sem adicionar decisao arquitetural nova.
6. Declarar explicitamente que o documento e complementar e deve deferir para `docs/architecture/architecture.md` em caso de divergencia.
7. Validar que nenhum outro documento governado, codigo, SPEC ou TASK foi alterado.

## Arquivos Ou Areas Provaveis

- `docs/architecture/layer-boundaries.md`

## Criterios De Aceite

- `docs/architecture/layer-boundaries.md` existe.
- O artefato aponta para `docs/architecture/architecture.md` como arquitetura principal.
- O artefato cita `specs/SPEC-001-modulo-0-fundacao-governada.md` como SPEC de origem.
- O artefato contem matriz para `api`, `application`, `domain`, `io`, `engine`, `repositories`, `export` e `report`.
- Cada camada possui responsabilidades, entradas, saidas, dependencias permitidas e dependencias proibidas.
- O artefato registra as proibicoes transversais aprovadas.
- O artefato nao cria arquitetura nova, contrato funcional, regra de dominio, formula prudencial, arredondamento, schema, endpoint ou classe.
- Nenhum arquivo alem de `docs/architecture/layer-boundaries.md` e alterado.

## Validacao Esperada

- Executar `test -f docs/architecture/layer-boundaries.md`.
- Executar `git diff --stat` e confirmar que a execucao alterou apenas `docs/architecture/layer-boundaries.md`.
- Conferir manualmente que o documento nao contradiz `docs/architecture/architecture.md` nem `SPEC-001`.
- Conferir manualmente que o documento nao define contrato funcional, regra de dominio, formula prudencial, schema, endpoint ou classe.

## Riscos

- Risco: o artefato virar arquitetura paralela.
  Mitigacao: declarar que ele complementa `docs/architecture/architecture.md` e nao substitui a arquitetura principal.

- Risco: a matriz introduzir decisao arquitetural nova.
  Mitigacao: limitar o conteudo a PRD, arquitetura, SPEC-001 e log homologado da TASK-011.

- Risco: antecipar contratos funcionais de modulos posteriores.
  Mitigacao: registrar lacunas e bloquear detalhes de endpoints, schemas, models, payloads e motores para SPECs/TASKs funcionais.

## Bloqueios Pendentes

Bloqueada ate homologacao da `TASK-011` e da `TASK-011B`.

Permanece bloqueado qualquer trabalho que tente alterar arquitetura principal, PRD, SPECs, TASKs existentes, codigo, contratos funcionais, regras de dominio, formulas prudenciais, arredondamento, schemas, endpoints ou classes durante esta TASK.
