# LOG - TASK-011 - Auditar fronteiras de camadas

## Referencia

- Task: `tasks/TASK-011-auditar-fronteiras-de-camadas.md`
- SPEC: `specs/SPEC-001-modulo-0-fundacao-governada.md`
- Status: concluido

## Fontes Consultadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `logs/LOG-002-auditar-estrutura-minima-repositorio.md`
- `logs/LOG-005-auditar-indice-e-rastreabilidade-de-specs.md`
- `backend/app/`

## Execucao

- Data: 2026-06-18
- Acao: Auditoria documental das fronteiras entre camadas backend.
- Resumo: Criada matriz objetiva para `api`, `application`, `domain`, `io`, `engine`, `repositories`, `export` e `report`, limitada ao PRD, arquitetura e SPEC-001. A estrutura atual possui apenas pacotes `__init__.py`; nao ha codigo funcional, imports, endpoints, schemas, models, repositories, motores, exportacao ou laudo para auditar implementacao real.

## Matriz De Fronteiras

| Camada | Responsabilidades | Entradas | Saidas | Dependencias permitidas | Dependencias proibidas |
| --- | --- | --- | --- | --- | --- |
| `api` | REST, validacao HTTP, autenticacao/autorizacao, OpenAPI, serializacao e conversao de erros de dominio em respostas HTTP. | Requests HTTP, arquivos enviados, parametros de rota/query e usuario autenticado. | Responses HTTP, payloads serializados e erros HTTP. | Pode depender de `application` e contratos de serializacao aprovados. | Nao deve concentrar regra de negocio, parse ECD, motores prudenciais, persistencia direta, exportacao ou laudo. |
| `application` | Casos de uso, transacoes logicas e orquestracao entre parse, motores, persistencia, exportacao e laudo. | Comandos vindos da API, identificadores de analise/exercicio e objetos de dominio. | Resultados de caso de uso, snapshots coordenados, comandos para persistencia/exportacao/laudo. | Pode depender de `domain`, `io`, `engine`, `repositories`, `export` e `report`. | Nao deve substituir motores, implementar detalhe HTTP, SQL ad hoc, parser bruto ou regra visual. |
| `domain` | Entidades, value objects, estados canonicos, contratos internos, invariantes e objetos de auditoria/rastreabilidade. | Dados canonicos e valores normalizados. | Objetos e estados de dominio. | Deve permanecer independente de frameworks e bibliotecas externas de infraestrutura. | Nao depende de FastAPI, SQLAlchemy, React, openpyxl, filesystem, HTTP ou banco. |
| `io` | Leitura, parse e normalizacao da ECD, preservando texto/linha quando disponivel e convertendo valores para `Decimal`. | Arquivo ECD e registros brutos como `I050`, `I051`, `I155`, `I200`, `I250`, `J100` e futuramente `J150`. | Estruturas intermediarias normalizadas para persistencia e motores. | Pode usar contratos internos e tipos canonicos de dominio quando aprovados. | Nao aplica metodologia prudencial, nao decide classificacao, nao calcula PLRA/FCA/ROA/CAPAG-E e nao monta laudo/exportacao. |
| `engine` | Motores declarados, comportamentais, PLRA, DFC/FCA, ROA, CAPAG-E, auditoria metodologica e governanca de assets. | Dados normalizados, snapshots, assets/metodologia versionados, evidencias e revisoes aplicaveis. | Resultados calculados, auditoria estruturada, status, bloqueios, limitacoes e componentes prudenciais. | Pode depender de `domain` e assets/metodologia carregados por interfaces claras. | Nao deve depender de FastAPI, React, openpyxl ou SQLAlchemy diretamente; nao deve serializar resposta HTTP nem montar UI. |
| `repositories` | Persistencia via SQLAlchemy, consultas transacionais, snapshots e recuperacao de versao metodologica usada. | Entidades/objetos persistiveis e criterios de consulta. | Entidades recuperadas, snapshots e confirmacao de persistencia. | Pode usar SQLAlchemy e banco operacional conforme contratos de persistencia aprovados. | Nao executa regra prudencial, nao parseia ECD, nao monta payload HTTP, nao gera Excel/laudo e nao deve espalhar SQL fora da camada. |
| `export` | Gerar Excel oficial, serializando resultados calculados, auditoria, evidencias, bloqueios e metodologia. | Snapshots, objetos calculados, evidencias, bloqueios e versao metodologica. | Workbook/artefato de exportacao e metadados de exportacao. | Pode consumir objetos calculados e estruturas de laudo/exportacao aprovadas. | Nao recalcula motores, nao altera resultados, nao decide metodologia e nao parseia ECD. |
| `report` | Montar `CapagReport`, validar status do laudo, produzir secoes estruturadas e entregar estrutura para exportacao Excel ou geracao futura. | `CapagEAssessment`, evidencias, bloqueios, snapshots e versao metodologica. | Laudo estruturado, secoes, status, ressalvas e bloqueios. | Pode consumir objetos calculados, evidencias e snapshots. | Nao executa motores, nao recalcula PLRA/FCA/ROA/CAPAG-E, nao parseia ECD e nao persiste diretamente fora dos fluxos aprovados. |

## Proibicoes Transversais Confirmadas

- Frontend nao parseia ECD.
- Frontend nao recalcula `PLRA`, `FCA`, `ROA` ou `CAPAG-E`.
- Frontend nao decide classificacao comportamental, nao aplica metodologia prudencial e nao altera status retornado pelo backend.
- Exportacao nao recalcula motores.
- Laudo nao recalcula motores.
- Regra prudencial sensivel fica no backend, nos motores e contratos apropriados.
- `domain` nao depende de FastAPI, SQLAlchemy, React ou openpyxl.
- `api` depende de `application`.
- `application` coordena `domain`, `io`, `engine`, `repositories`, `export` e `report`.
- `engine` depende de `domain` e assets/metodologia carregados por interfaces claras.

## Lacunas E Ambiguidades

- Ainda nao existem interfaces, contratos internos ou imports reais para validar aderencia automatica das dependencias.
- A fronteira entre `application` e `repositories` precisara ser detalhada quando houver transacoes e modelos persistentes.
- A fronteira entre `engine`, `export` e `report` precisara de testes quando existirem snapshots calculados para garantir que exportacao/laudo nao recalculem.
- A fronteira entre `io` e `engine` precisara ser verificada quando parser ECD e motores forem implementados.
- A fronteira de assets/metodologia depende de TASKs futuras de assets, `MethodologyVersion` e validacoes metodologicas.
- Contratos funcionais de endpoints, schemas, models e payloads pertencem a SPECs/TASKs funcionais posteriores.

## Proximas TASKs Pequenas Sugeridas

- Executar `TASK-012 - Criar indice oficial de SPECs` para fortalecer rastreabilidade documental antes de implementacoes funcionais.
- Executar `TASK-028 - Criar app FastAPI minimo` mantendo `api` fino e sem regra de negocio.
- Executar `TASK-030 - Auditar rastreabilidade TASKs e SPECs` para confirmar se TASKs futuras preservam as fronteiras por SPEC.
- Quando houver codigo funcional, criar ou executar auditoria futura de imports entre camadas para validar aderencia objetiva.

## Arquivos Alterados

- `logs/LOG-011-auditar-fronteiras-de-camadas.md`
- `ROADMAP.md`

## Validacoes

- Comando: `test -f logs/LOG-011-auditar-fronteiras-de-camadas.md`
  - Resultado: arquivo encontrado.
- Comando: `find backend/app -maxdepth 2 -type f -not -name '*.env' | sort`
  - Resultado: encontrados apenas arquivos `__init__.py` dos pacotes estruturais.
- Comando: `git diff --stat`
  - Resultado: a execucao adicionou este log e atualizou `ROADMAP.md` conforme fluxo governado; ja havia alteracoes anteriores pendentes na arvore.
- Conferencia manual:
  - Resultado: o log nao cria contrato funcional, regra de dominio, formula prudencial, schema, endpoint, classe ou decisao arquitetural nova.

## Pendencias Ou Bloqueios

- Nenhum bloqueio para homologacao desta auditoria.

## Homologacao

- Status: aprovada
- Data: 2026-06-18
- Decisao do usuario: Aprovado
- Observacao: TASK homologada pelo usuario.
