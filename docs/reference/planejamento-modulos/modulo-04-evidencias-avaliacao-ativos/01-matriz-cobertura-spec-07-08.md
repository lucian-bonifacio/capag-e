# 01 - Matriz de cobertura das SPECs 07 e 08

## Objetivo

Garantir cobertura integral das specs de evidencias e avaliacao de ativos.

## SPEC-07

| Secao | Cobertura |
|---|---|
| Objetivo, motivacao e escopo | `00-visao-geral.md` |
| Principio central | `02-modelo-evidencias-materialidade.md` |
| `AdjustmentEvidence` | `02-modelo-evidencias-materialidade.md` |
| `scope_type` | `02-modelo-evidencias-materialidade.md` |
| `adjustment_type` | `02-modelo-evidencias-materialidade.md` |
| `method_component` | `02-modelo-evidencias-materialidade.md` |
| `required_evidence_type` | `02-modelo-evidencias-materialidade.md` |
| `evidence_status` | `02-modelo-evidencias-materialidade.md` |
| `materiality_level` | `02-modelo-evidencias-materialidade.md` |
| Regras de materialidade | `02-modelo-evidencias-materialidade.md` |
| Regras por tipo de ajuste | `04-integracao-plra-bloqueios.md` |
| Integracao com pendencias metodologicas | `04-integracao-plra-bloqueios.md` |
| API | `05-api-frontend-exportacao.md` |
| UI | `05-api-frontend-exportacao.md` |
| Exportacao | `05-api-frontend-exportacao.md` |
| Laudo | `05-api-frontend-exportacao.md` |
| Testes obrigatorios | `06-testes-evidencias-ativos.md` |
| Criterios de aceite | `07-roadmap-execucao-modulo-4.md` |

## SPEC-08

| Secao | Cobertura |
|---|---|
| Objetivo, motivacao e escopo | `00-visao-geral.md` |
| Ativos alvo | `03-avaliacao-ativos-liquidacao-forcada.md` |
| Classificacao de realizabilidade | `03-avaliacao-ativos-liquidacao-forcada.md` |
| `AssetValuationAssessment` | `03-avaliacao-ativos-liquidacao-forcada.md` |
| `valuation_basis` | `03-avaliacao-ativos-liquidacao-forcada.md` |
| `essentiality_status` | `03-avaliacao-ativos-liquidacao-forcada.md` |
| `valuation_status` | `03-avaliacao-ativos-liquidacao-forcada.md` |
| Regras de calculo | `03-avaliacao-ativos-liquidacao-forcada.md`, `04-integracao-plra-bloqueios.md` |
| Regras de bloqueio | `04-integracao-plra-bloqueios.md` |
| Integracao com evidencias | `02-modelo-evidencias-materialidade.md`, `03-avaliacao-ativos-liquidacao-forcada.md` |
| Integracao com PLR/PLRA | `04-integracao-plra-bloqueios.md` |
| UI | `05-api-frontend-exportacao.md` |
| Exportacao | `05-api-frontend-exportacao.md` |
| Laudo | `05-api-frontend-exportacao.md` |
| Testes obrigatorios | `06-testes-evidencias-ativos.md` |
| Criterios de aceite | `07-roadmap-execucao-modulo-4.md` |

## Lacunas identificadas

- O sistema atual tem auditoria tecnica, mas nao trilha documental estruturada por ajuste.
- O sistema atual aplica desagios, mas nao formaliza liquidacao forcada por ativo.
- O sistema ainda nao diferencia evidencia, justificativa, ressalva e bloqueio.
- O frontend ainda precisa de painel proprio para evidencias/ativos.

