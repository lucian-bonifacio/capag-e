# Contrato De Carga Do Plano Referencial Oficial

## 1. Identificacao

- SPEC: `SPEC-010`.
- TASK: `TASK-089`.
- Versao do contrato: `1.0.0`.
- Fonte inicial aprovada: SPED/RFB, ECF Leiaute 11, ano-calendario 2024.
- Escopo inicial aprovado: `PJ_GERAL`, abas `L100A` e `L300A`.

## 2. Principios

- O asset valida e descreve o `COD_CTA_REF` declarado no `I051`.
- O asset nao infere codigo alternativo e nao define regra prudencial.
- Toda versao publicada deriva de um documento aprovado e identificado por
  SHA-256.
- Atualizacao de fonte ou conversao gera nova versao imutavel.
- O leiaute da declaracao e o leiaute da fonte sao metadados distintos.
- O asset versionado permanece a fonte reproduzivel da carga operacional.

## 3. Manifesto Obrigatorio

O JSON publicado deve conter:

| Campo | Tipo | Regra |
| --- | --- | --- |
| `asset_type` | string | Valor fixo `official_reference_accounts` |
| `schema_version` | string | Versao semantica do contrato |
| `official_version_id` | string | Identificador imutavel e unico da versao |
| `base_status` | string | Estado governado da base |
| `approval_status` | string | Estado da aprovacao da fonte |
| `methodology_version_id` | string | Versao metodologica compativel com a execucao |
| `source_document_name` | string | Nome oficial do arquivo |
| `source_document_hash` | string | SHA-256 minusculo com 64 caracteres |
| `source_document_date` | string | Data ISO da atualizacao oficial |
| `source_url_or_reference` | string | URL oficial ou referencia governada |
| `source_publisher` | string | Orgao publicador |
| `source_system` | string | Sistema que publica a fonte, inicialmente `ECF` |
| `source_layout` | string | Leiaute da fonte, inicialmente `ECF_11` |
| `source_calendar_year` | inteiro | Ano-calendario coberto |
| `declaration_layout` | string | Leiaute declaratorio compativel, inicialmente `ECD_9` |
| `entity_type` | string | Tipo de entidade, inicialmente `PJ_GERAL` |
| `source_sheets` | lista de strings | Abas importadas |
| `source_record_count` | inteiro | Total de codigos validos nas abas |
| `asset_record_count` | inteiro | Total de registros convertidos |
| `coverage_status` | string | Resultado da cobertura |
| `required_fields` | lista de strings | Campos obrigatorios por registro |
| `records` | lista de objetos | Contas oficiais convertidas |

Campos opcionais do manifesto:

- `approval_notes`;
- `loaded_at`;
- `loaded_by`;
- `superseded_by`;
- `change_reason`;
- `special_situations_year`;

Datas de aprovacao e carga podem ser registradas em auditoria externa. Quando
presentes no asset, devem usar ISO 8601 e nao podem alterar o identificador de
uma versao ja publicada.

## 4. Registro Obrigatorio

Cada item de `records` deve conter:

| Campo | Tipo | Regra |
| --- | --- | --- |
| `reference_code` | string | Codigo exato e nao vazio |
| `official_description` | string | Descricao oficial nao vazia |
| `parent_reference_code` | string ou nulo | Codigo superior existente na mesma versao |
| `level` | inteiro | Nivel positivo coerente com a hierarquia |
| `nature` | string | `ATIVO`, `PASSIVO`, `PATRIMONIO_LIQUIDO` ou `RESULTADO` |
| `valid_from` | inteiro | Ano inicial derivado de `source_valid_from` |
| `valid_to` | inteiro ou nulo | Ano final derivado de `source_valid_to` |
| `layout` | string | Leiaute declaratorio usado no matcher |
| `entity_type` | string | Tipo de entidade |
| `source` | string | Identificador curto da fonte/versionamento |
| `status` | string | Estado governado do codigo |
| `methodology_version_id` | string | Versao metodologica compativel |
| `source_sheet` | string | Aba oficial de origem |
| `source_type` | string | `A` analitica ou `S` sintetica |
| `source_nature_code` | string | Codigo de natureza preservado da fonte |
| `source_valid_from` | string | Data oficial em ISO 8601 |
| `source_valid_to` | string ou nulo | Data oficial em ISO 8601 |
| `official_guidance` | string ou nulo | Orientacao oficial preservada |
| `validation_notes` | string ou nulo | Divergencia estrutural preservada e justificativa de revisao |

Campos adicionais so podem ser introduzidos por nova versao do schema. Campos
desconhecidos podem ser preservados por leitores tolerantes, mas nao substituem
os obrigatorios.

## 5. Estados E Transicoes

Estados permitidos para `base_status`:

- `rascunho`;
- `em_validacao`;
- `aprovada`;
- `publicada`;
- `substituida`;
- `bloqueada`.

Fluxo normal:

`rascunho -> em_validacao -> aprovada -> publicada -> substituida`

Uma base em qualquer estado pode ir para `bloqueada` por decisao governada.
Desbloqueio exige nova decisao registrada. Uma versao `publicada` nao pode
retornar a `rascunho` nem ser sobrescrita.

Estados permitidos por codigo:

- `ATIVA`;
- `INATIVA`;
- `EM_REVISAO`;
- `BLOQUEADA`.

Para a conversao inicial:

- codigo sem `DT_FIM` recebe `ATIVA`;
- codigo com `DT_FIM` anterior ao fim do ano-calendario recebe `INATIVA`;
- divergencia nao resolvida recebe `EM_REVISAO` ou bloqueia a publicacao;
- `BLOQUEADA` exige justificativa governada.
- `EM_REVISAO` e `BLOQUEADA` exigem `validation_notes`.

## 6. Validacoes Obrigatorias

Antes da publicacao:

1. validar tipo e presenca de todos os campos;
2. validar SHA-256, URL oficial, versao e origem;
3. validar `asset_record_count == len(records)`;
4. validar `source_record_count == asset_record_count` para cobertura completa;
5. rejeitar chave duplicada por
   `(reference_code, layout, entity_type, valid_from, valid_to)`;
6. validar formato e ordem das vigencias;
7. validar status e naturezas permitidos;
8. validar que toda conta com pai referencia um registro da mesma versao;
9. validar que `level` do filho e maior que o nivel do pai;
10. rejeitar ciclos de hierarquia;
11. validar compatibilidade entre natureza oficial e codigo preservado;
12. validar cobertura de 100% das abas aprovadas;
13. validar cobertura de 100% dos `COD_CTA_REF` do DATAPACK de regressao.

## 7. Publicacao E Bloqueio

Uma base pode ser `publicada` somente quando:

- a fonte estiver aprovada;
- hash e origem forem verificaveis;
- o contrato da carga estiver aprovado;
- a cobertura estiver aprovada e validada;
- todas as validacoes estruturais passarem;
- eventuais lacunas estiverem registradas e nao forem impeditivas.

O loader operacional deve rejeitar:

- asset ausente, vazio ou JSON invalido;
- manifesto incompleto;
- fonte sem hash valido;
- base em estado diferente de `publicada`;
- contagem divergente;
- registro incompleto ou invalido;
- duplicidade, hierarquia quebrada ou ciclo;
- vigencia, status, natureza, leiaute ou entidade invalidos.

Um codigo ausente na versao publicada continua sendo uma pendencia por conta:
`COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL`.

## 8. Erros Governados

Codigos internos recomendados:

- `OFFICIAL_REFERENCE_ASSET_NOT_FOUND`;
- `OFFICIAL_REFERENCE_ASSET_INVALID_JSON`;
- `OFFICIAL_REFERENCE_MANIFEST_INVALID`;
- `OFFICIAL_REFERENCE_SOURCE_HASH_INVALID`;
- `OFFICIAL_REFERENCE_BASE_NOT_PUBLISHED`;
- `OFFICIAL_REFERENCE_RECORD_INVALID`;
- `OFFICIAL_REFERENCE_DUPLICATE`;
- `OFFICIAL_REFERENCE_HIERARCHY_INVALID`;
- `OFFICIAL_REFERENCE_VALIDITY_INVALID`;
- `OFFICIAL_REFERENCE_COVERAGE_INVALID`.

Esses erros sao de configuracao do sistema. Pendencias de um `COD_CTA_REF`
declarado permanecem no resultado por conta e nao transformam toda analise em
erro HTTP quando o processamento parcial for possivel.

## 9. Contrato Da Primeira Versao

- `official_version_id`:
  `sped-ecf-11-ac2024-pj-geral-2025-11-09-v1`;
- `source_layout`: `ECF_11`;
- `source_calendar_year`: `2024`;
- `declaration_layout`: `ECD_9`;
- `entity_type`: `PJ_GERAL`;
- `source_sheets`: `L100A`, `L300A`;
- `source_record_count`: `1109`;
- cobertura esperada da conversao: `1109/1109`;
- cobertura esperada do DATAPACK: `58/58`.

A fonte possui uma divergencia estrutural conhecida: a conta
`3.11.05.01.01.01` informa nivel `5`, igual ao nivel da conta superior. O valor
oficial deve ser preservado e o codigo publicado como `EM_REVISAO`, com nota de
validacao, sem correcao local.

## 10. Aprovacao

O usuario autorizou em 2026-07-24 a execucao continua de todas as TASKs
planejadas, incluindo os gates apresentados para fonte, contrato e cobertura.
A homologacao consolidada do grupo permanece pendente.
