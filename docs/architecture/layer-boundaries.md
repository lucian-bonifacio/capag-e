# Fronteiras De Camadas - CAPAG

## 1. Natureza Do Documento

Este artefato complementa `docs/architecture/architecture.md` e registra, de forma objetiva, as fronteiras entre camadas do backend do CAPAG.

Este documento nao substitui a arquitetura principal. Em caso de divergencia, prevalece `docs/architecture/architecture.md`.

## 2. Rastreabilidade

Fontes governadas usadas:

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `logs/LOG-011-auditar-fronteiras-de-camadas.md`

SPEC de origem:

- `specs/SPEC-001-modulo-0-fundacao-governada.md`

Este artefato consolida a auditoria homologada da `TASK-011` sem criar arquitetura nova, contrato funcional, regra de dominio, formula prudencial, politica de arredondamento, schema, endpoint ou classe.

## 3. Principios Transversais

- Regra prudencial sensivel fica no backend, nos motores e contratos apropriados.
- Frontend consome contratos da API e nao reimplementa metodologia prudencial.
- Exportacao e laudo serializam ou montam artefatos a partir de objetos ja calculados.
- Resultados emitidos devem preservar rastreabilidade de metodologia, evidencias, bloqueios e snapshots quando esses contratos forem implementados.
- Detalhes funcionais de endpoints, schemas, models, payloads, motores, persistencia, exportacao e laudo pertencem a SPECs e TASKs funcionais posteriores.

## 4. Matriz De Fronteiras

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

## 5. Proibicoes Transversais

- Frontend nao parseia ECD.
- Frontend nao recalcula `PLRA`, `FCA`, `ROA` ou `CAPAG-E`.
- Frontend nao decide classificacao comportamental.
- Frontend nao aplica metodologia prudencial.
- Frontend nao altera status retornado pelo backend.
- Exportacao nao recalcula motores.
- Laudo nao recalcula motores.
- `domain` nao depende de FastAPI, SQLAlchemy, React ou openpyxl.
- `api` depende de `application`.
- `application` coordena `domain`, `io`, `engine`, `repositories`, `export` e `report`.
- `engine` depende de `domain` e assets/metodologia carregados por interfaces claras.

## 6. Lacunas Para Implementacao Futura

As lacunas abaixo sao constatacoes para SPECs e TASKs futuras. Elas nao sao resolvidas por este documento.

- Ainda nao existem interfaces, contratos internos ou imports reais para validar aderencia automatica das dependencias.
- A fronteira entre `application` e `repositories` precisa ser detalhada quando houver transacoes e modelos persistentes.
- A fronteira entre `engine`, `export` e `report` precisa de testes quando existirem snapshots calculados para garantir que exportacao e laudo nao recalculem.
- A fronteira entre `io` e `engine` precisa ser verificada quando parser ECD e motores forem implementados.
- A fronteira de assets/metodologia depende de TASKs futuras de assets, `MethodologyVersion` e validacoes metodologicas.
- Contratos funcionais de endpoints, schemas, models e payloads pertencem a SPECs e TASKs funcionais posteriores.

## 7. Fora Do Escopo Deste Artefato

Este documento nao define:

- contrato de API;
- regra de dominio;
- formula prudencial;
- politica de precisao ou arredondamento;
- schema, endpoint, classe, interface ou import;
- modelo de persistencia;
- formato final de Excel;
- formato final de laudo;
- validacao automatizada de imports entre camadas.
