# 22 - Matriz de cobertura dos documentos de referencia

## Objetivo

Garantir rastreabilidade entre as 27 secoes de `docs/reference/novo_modulo_reclass.md`, o documento conceitual `docs/reference/nova_spec_nv_modulo.md` e as tarefas do Modulo 2.

## Ponto de decisao

Decidir se esta matriz deve ser mantida como checklist obrigatorio quando o Modulo 2 virar specs/tasks oficiais.

## Cobertura de `docs/reference/novo_modulo_reclass.md`

| Secao do documento | Tema | Arquivo(s) do Modulo 2 |
|---|---|---|
| 1 | Objetivo do sistema | `00-visao-geral.md`, `02-spec-conceitual-oficial.md` |
| 2 | Principio tecnico | `00-visao-geral.md`, `08-regras-deterministicas-familias.md`, `09-motor-score-confianca-seguranca.md` |
| 3 | Visao geral do fluxo | `00-visao-geral.md`, `21-roadmap-execucao-modulo-2.md` |
| 4 | Ingestao da ECD | `03-entrada-ecd-e-dados-necessarios.md` |
| 5 | Normalizacao dos dados | `04-normalizacao-comportamental.md` |
| 6 | Montagem do razao por conta | `05-razao-por-conta-e-contrapartidas.md` |
| 7 | Perfil comportamental | `06-perfil-comportamental-conta.md` |
| 8 | Familias contabeis | `07-taxonomia-familias-contabeis.md` |
| 9 | Regras deterministicas por familia | `08-regras-deterministicas-familias.md` |
| 10 | Motor de score | `09-motor-score-confianca-seguranca.md` |
| 11 | Classificacao em camadas | `10-classificacao-em-camadas-mapeamento-referencial.md` |
| 12 | Mapeamento para conta referencial | `10-classificacao-em-camadas-mapeamento-referencial.md` |
| 13 | Comparacao com o `I051` original | `11-comparacao-com-camada-declarada.md` |
| 14 | Relatorio auditavel | `13-relatorio-auditavel-e-evidencias.md` |
| 15 | Interface de revisao humana | `17-frontend-revisao-comportamental.md` |
| 16 | Aprendizado por precedentes | `14-revisao-humana-precedentes.md` |
| 17 | Calibracao sem perder escala | `19-metricas-qualidade-calibracao.md` |
| 18 | Banco de dados sugerido | `15-banco-dados-evolucao-futura.md`, `../modulo-00-organizacao-arquitetura-design/11-decisao-banco-dados-persistencia.md` |
| 19 | API interna sugerida | `16-api-contratos-backend.md` |
| 20 | Pipeline tecnico | `21-roadmap-execucao-modulo-2.md` |
| 21 | Ordem ideal de implementacao | `21-roadmap-execucao-modulo-2.md` |
| 22 | Metricas de qualidade | `19-metricas-qualidade-calibracao.md` |
| 23 | Regras de seguranca | `09-motor-score-confianca-seguranca.md` |
| 24 | Exemplo de fluxo para uma conta | `23-exemplo-fluxo-conta.md` |
| 25 | Risco principal do projeto | `24-riscos-conceituais-e-salvaguardas.md` |
| 26 | MVP recomendado | `07-taxonomia-familias-contabeis.md`, `20-testes-validacao-mvp.md`, `21-roadmap-execucao-modulo-2.md` |
| 27 | Conclusao tecnica | `00-visao-geral.md`, `21-roadmap-execucao-modulo-2.md`, `24-riscos-conceituais-e-salvaguardas.md` |

## Cobertura de `docs/reference/nova_spec_nv_modulo.md`

| Tema | Arquivo(s) do Modulo 2 |
|---|---|
| Duas leituras paralelas da ECD | `00-visao-geral.md`, `02-spec-conceitual-oficial.md`, `11-comparacao-com-camada-declarada.md` |
| Analise declarada preservada | `00-visao-geral.md`, `11-comparacao-com-camada-declarada.md`, modulo 1 |
| Analise comportamental como segunda leitura | `00-visao-geral.md`, `02-spec-conceitual-oficial.md` |
| Uso de saldos, lancamentos, historicos e contrapartidas | `03-entrada-ecd-e-dados-necessarios.md`, `05-razao-por-conta-e-contrapartidas.md`, `06-perfil-comportamental-conta.md` |
| Pipeline conceitual | `21-roadmap-execucao-modulo-2.md` |
| Modelo de saida por conta e consolidado | `00-visao-geral.md`, `13-relatorio-auditavel-e-evidencias.md` |
| Politica de confianca | `09-motor-score-confianca-seguranca.md` |
| Familias MVP | `07-taxonomia-familias-contabeis.md` |
| Revisao humana | `14-revisao-humana-precedentes.md`, `17-frontend-revisao-comportamental.md` |
| Relacao com PLR/CAPAG | `12-cenario-capag-reclassificada.md` |
| Exportacao e laudo | `18-exportacao-laudo-comparativo.md` |
| Fronteiras arquiteturais | `00-visao-geral.md`, modulo 0 |
| Linguagem recomendada sobre `I051` | `01-nome-escopo-e-linguagem.md` |

## Entregavel

Checklist de cobertura completa do Modulo 2.

## Criterios de sucesso

- Nenhuma secao dos documentos de referencia fica sem destino.
- Qualquer pessoa consegue localizar onde cada ideia sera tratada.

