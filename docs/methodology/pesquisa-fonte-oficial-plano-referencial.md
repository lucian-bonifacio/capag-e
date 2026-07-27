# Pesquisa Da Fonte Oficial Do Plano Referencial

## 1. Estado Da Decisao

- Status: aprovada para execucao no grupo; homologacao final pendente.
- Data da pesquisa: 2026-07-24.
- TASK: `TASK-088`.
- SPEC: `SPEC-010`.
- Efeito operacional atual: nenhum. A fonte pesquisada nao foi incorporada ao asset, banco, API ou motor.

## 2. Objetivo

Identificar uma fonte oficial, reproduzivel e adequada para validar e enriquecer o
`COD_CTA_REF` declarado no registro `I051` da ECD, preservando a separacao entre:

- o leiaute da escrituracao ECD;
- o leiaute do documento oficial que publica os planos referenciais;
- a metodologia interna e os calculos prudenciais do CAPAG.

## 3. Fontes Candidatas

| Fonte | Origem e acesso | Formato | Cobertura | Confiabilidade | Limitacoes e riscos |
| --- | --- | --- | --- | --- | --- |
| Tabelas Dinamicas e Planos de Contas Referenciais - ECF Leiaute 11 | Portal oficial SPED/RFB no `gov.br`, arquivo oficial para ano-calendario 2024 e situacoes especiais de 2025 | XLSX estruturado | Planos patrimoniais e de resultado para PJ em geral, financeiras, seguradoras e entidades de previdencia, alem das demais tabelas do leiaute | Alta: fonte primaria oficial, versionada por leiaute e periodo | O leiaute do documento e da ECF e nao deve ser confundido com o leiaute da ECD; a URL oficial pode receber atualizacoes, portanto o hash do arquivo obtido deve ser preservado |
| Manual de Orientacao da ECD - Leiaute 9, atualizacao de novembro de 2024 | Portal oficial SPED/RFB no `gov.br`; aplicavel a partir do ano-calendario 2020 | PDF | Contrato tecnico da ECD e semantica do registro `I051` | Alta como fonte complementar | Nao fornece, em formato tabular completo, o conjunto de contas necessario para popular o asset |
| Tabelas Dinamicas e Planos de Contas Referenciais - ECF Leiaute 10 | Portal oficial SPED/RFB no `gov.br` | XLSX estruturado | Ano-calendario 2023 e situacoes especiais de 2024 | Alta | Periodo anterior ao DATAPACK de teste; inadequado como versao primaria para o ano-calendario 2024 |
| Tabelas Dinamicas e Planos de Contas Referenciais - ECF Leiaute 12 | Portal oficial SPED/RFB no `gov.br` | XLSX estruturado | Ano-calendario 2025 e situacoes especiais de 2026 | Alta | Periodo posterior ao DATAPACK de teste; a versao mais nova nao substitui a versao aplicavel ao periodo analisado |
| Asset inicial `official_reference_accounts.json` | Repositorio CAPAG | JSON | Tres registros de apoio estrutural | Baixa como fonte oficial completa | Cobertura deliberadamente minima e sem documento oficial aprovado; nao serve como origem final |
| Materiais locais em `docs/reference/` | Referencias historicas autorizadas para esta pesquisa | Markdown, TXT e PDF | Exemplos, propostas e documentos auxiliares | Variavel | Nao sao fonte normativa direta conforme `AGENTS.md` e `SPEC-010` |

## 4. Fonte Recomendada

Recomenda-se aprovar:

- documento: `Tabelas Dinamicas e Planos de Contas Referenciais - Leiaute 11`;
- orgao publicador: Receita Federal do Brasil, portal SPED;
- ano-calendario: 2024;
- situacoes especiais: 2025;
- atualizacao identificada no portal: 09/11/2025;
- formato: XLSX;
- tipo de entidade inicial: `PJ_GERAL`;
- abas iniciais: `L100A` para contas patrimoniais e `L300A` para contas de resultado;
- SHA-256 do arquivo pesquisado:
  `0c66a19ce859cdc7a1eee137896243100cbaa26239ffa8ed3044762f3e359397`.

Pagina oficial:

`https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecf`

Arquivo oficial pesquisado:

`https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecf/manuais-e-documentos-tecnicos/tabelas_dinamicas_ecf_leiaute_11_09_11_2025_ac_2024_sit_esp_2025.xlsx/@@display-file/file`

Manual complementar da ECD pesquisado:

`https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/ecd/manuais-e-documentos-tecnicos/manual_de_orientacao_da_ecd_leiaute_9_atualizacao_nov_2024.pdf/@@display-file/file`

## 5. Estrutura Encontrada

A aba `L100A`, denominada `Plano de Contas Referencial - Contas Patrimoniais -
PJ do Lucro Real - PJ em Geral`, contem 722 codigos reconhecidos, incluindo as
contas-raiz `1` e `2`.

A aba `L300A`, destinada as contas de resultado da mesma categoria de entidade,
contem 387 codigos reconhecidos, incluindo a conta-raiz `3`.

As duas abas fornecem os campos oficiais:

- `CODIGO`;
- `DESCRICAO`;
- `DT_INI`;
- `DT_FIM`;
- `TIPO`;
- `CONTA SUPERIOR`;
- `NIVEL`;
- `NATUREZA`;
- `ORIENTACOES`.

Esses campos permitem derivar os campos minimos da `SPEC-010`. O mapeamento
definitivo, os metadados adicionais e as regras de conversao pertencem a
`TASK-089`.

## 6. Cobertura Do DATAPACK 2024

Arquivo autorizado para o teste:

`docs/reference/ecd-example/ECD 2024 DATAPACK.txt`

Periodo declarado no registro `0000`: 01/01/2024 a 31/12/2024.

Resultado da comparacao exata dos codigos declarados em `I051`:

| Medida | Resultado |
| --- | ---: |
| Codigos `I051` distintos | 58 |
| Encontrados em `L100A` | 34 |
| Encontrados em `L300A` | 24 |
| Encontrados nas duas abas | 0 |
| Nao encontrados | 0 |
| Cobertura combinada | 100% |

Essa medicao comprova aderencia ao DATAPACK usado nos testes, mas nao comprova
sozinha cobertura universal de toda ECD ou de outros tipos de entidade.

## 7. Criterio De Cobertura Recomendado

Para a primeira carga governada, recomenda-se:

1. importar todos os codigos oficiais das abas `L100A` e `L300A`, incluindo
   contas sinteticas e analiticas;
2. preservar descricao, hierarquia, nivel, natureza, vigencia, tipo e
   orientacoes da fonte;
3. classificar o escopo como `PJ_GERAL`, ano-calendario 2024;
4. exigir cobertura de 100% dos registros validos das duas abas na conversao;
5. exigir cobertura de 100% dos `COD_CTA_REF` do DATAPACK como teste de
   regressao, sem limitar o asset aos codigos presentes nesse arquivo;
6. registrar lacunas de outros tipos de entidade como escopo nao publicado,
   sem preencher por inferencia.

## 8. Distincao De Leiautes

O arquivo de teste usa a ECD Leiaute 9, aplicavel desde o ano-calendario 2020.
O plano recomendado e publicado no conjunto da ECF Leiaute 11 para o
ano-calendario 2024.

O contrato de carga deve registrar esses conceitos separadamente. A recomendacao
para a `TASK-089` e manter, no minimo:

- `declaration_layout`: `ECD_9`;
- `source_system`: `ECF`;
- `source_layout`: `ECF_11`;
- `source_calendar_year`: `2024`;
- `entity_type`: `PJ_GERAL`.

Registrar apenas `layout: ECD_2024` perderia informacao sobre a origem e poderia
misturar versoes tecnicas diferentes.

## 9. Lacunas E Riscos

- A recomendacao cobre inicialmente PJ em geral. Outros tipos de entidade
  exigem escopo e publicacao proprios.
- O XLSX oficial precisa ser convertido por processo deterministico, validado e
  rastreado pelo hash antes de publicacao.
- Atualizacao posterior do arquivo oficial deve gerar nova versao e novo hash;
  nao deve substituir silenciosamente uma versao ja usada.
- A aplicabilidade por periodo deve considerar `DT_INI` e `DT_FIM`, sem assumir
  que todo codigo do arquivo esta ativo para qualquer data.
- A correspondencia de 100% no DATAPACK nao autoriza inferir codigo para contas
  sem `I051`.
- O plano oficial descreve e valida a declaracao. Ele nao define tratamento
  PLRA, FCO, FCA, ROA ou CAPAG-E.
- A conta oficial `3.11.05.01.01.01` informa nivel `5`, igual ao da conta
  superior. A carga deve preservar o valor e marcar o codigo `EM_REVISAO`.

## 10. Decisao

Em 2026-07-24, o usuario autorizou expressamente a execucao continua de todas as
TASKs planejadas e a homologacao consolidada ao final. A autorizacao libera:

- fonte oficial: XLSX SPED/RFB da ECF Leiaute 11 para ano-calendario 2024;
- escopo inicial: `PJ_GERAL`, abas `L100A` e `L300A`;
- criterio de cobertura definido na secao 7;
- separacao entre leiaute declaratorio `ECD_9` e leiaute da fonte `ECF_11`.

A aprovacao libera contrato, validacao e preparacao do asset. A homologacao da
entrega permanece pendente junto com o grupo completo.
