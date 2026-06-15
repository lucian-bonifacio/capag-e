# 12 - Matriz de cobertura do ajuste do modulo principal

## Objetivo

Garantir rastreabilidade entre todas as secoes de `docs/reference/ajuste_modulo_principal.md`, o sistema atual e as tarefas do Modulo 1.

## Ponto de decisao

Decidir se esta matriz sera mantida como checklist obrigatorio quando o Modulo 1 virar specs/tasks oficiais.

## Cobertura de `docs/reference/ajuste_modulo_principal.md`

| Secao do documento | Tema | Arquivo(s) do Modulo 1 |
|---|---|---|
| 1 | Premissa central | `00-visao-geral.md`, `02-spec-camada-declarada.md` |
| 2 | Problema atual | `00-visao-geral.md`, `01-diagnostico-estado-atual.md`, `18-gap-analysis-sistema-atual-vs-modulo-1.md` |
| 3 | Principio correto | `02-spec-camada-declarada.md`, `03-plano-referencial-oficial.md`, `04-metodologia-interna-plr.md`, `05-metodologia-interna-fco.md` |
| 4 | Camada 1 - tabela oficial | `03-plano-referencial-oficial.md` |
| 5 | Camada 2 - tabela metodologica interna | `04-metodologia-interna-plr.md`, `05-metodologia-interna-fco.md`, `13-status-regras-e-bloqueio-prefixo-amplo.md` |
| 6 | Fluxo geral do processamento | `02-spec-camada-declarada.md`, `10-roadmap-execucao-modulo-1.md` |
| 7 | Fluxo detalhado | `01-diagnostico-estado-atual.md`, `03-plano-referencial-oficial.md`, `04-metodologia-interna-plr.md`, `05-metodologia-interna-fco.md` |
| 8 | Regra de especificidade | `15-algoritmo-match-metodologico.md` |
| 9 | Bloqueio de prefixo amplo | `13-status-regras-e-bloqueio-prefixo-amplo.md` |
| 10 | Status das regras metodologicas | `13-status-regras-e-bloqueio-prefixo-amplo.md` |
| 11 | Exemplo de tabela metodologica corrigida | `04-metodologia-interna-plr.md`, `05-metodologia-interna-fco.md`, `13-status-regras-e-bloqueio-prefixo-amplo.md` |
| 12 | Tratamento por finalidade | `04-metodologia-interna-plr.md`, `05-metodologia-interna-fco.md`, `16-resultado-por-conta-declarada.md` |
| 13 | Resultado por conta | `16-resultado-por-conta-declarada.md` |
| 14 | Sem regra metodologica | `15-algoritmo-match-metodologico.md`, `16-resultado-por-conta-declarada.md` |
| 15 | Codigo ausente na tabela oficial | `03-plano-referencial-oficial.md`, `16-resultado-por-conta-declarada.md` |
| 16 | Validacoes automaticas | `14-validacoes-automaticas-metodologia.md` |
| 17 | Testes de regressao | `09-testes-camada-declarada.md`, `14-validacoes-automaticas-metodologia.md` |
| 18 | Algoritmo de match | `15-algoritmo-match-metodologico.md` |
| 19 | Pseudocodigo | `15-algoritmo-match-metodologico.md` |
| 20 | Exemplo completo | `17-exemplo-completo-conta-1725.md` |
| 21 | Regra de ouro | `00-visao-geral.md`, `15-algoritmo-match-metodologico.md`, `17-exemplo-completo-conta-1725.md` |
| 22 | Conclusao | `00-visao-geral.md`, `10-roadmap-execucao-modulo-1.md` |

## Cobertura do sistema atual

| Funcionalidade atual | Situacao | Arquivo(s) de planejamento |
|---|---|---|
| Parser le `I051` | existente | `01-diagnostico-estado-atual.md`, `18-gap-analysis-sistema-atual-vs-modulo-1.md` |
| Normalizador preserva `COD_CTA_REF` sem catalogo local | existente | `01-diagnostico-estado-atual.md`, `18-gap-analysis-sistema-atual-vs-modulo-1.md` |
| Catalogo referencial simples | existente, insuficiente para plano oficial completo | `03-plano-referencial-oficial.md`, `18-gap-analysis-sistema-atual-vs-modulo-1.md` |
| Matching exato/prefixo mais especifico PLR | existente | `15-algoritmo-match-metodologico.md`, `18-gap-analysis-sistema-atual-vs-modulo-1.md` |
| Matching exato/prefixo mais especifico FCO | existente | `15-algoritmo-match-metodologico.md`, `18-gap-analysis-sistema-atual-vs-modulo-1.md` |
| Status de regra metodologica | lacuna | `13-status-regras-e-bloqueio-prefixo-amplo.md` |
| Prefixo amplo bloqueado | lacuna | `13-status-regras-e-bloqueio-prefixo-amplo.md` |
| Validacao automatica da metodologia | lacuna | `14-validacoes-automaticas-metodologia.md` |
| Resultado por finalidade em estrutura unificada | lacuna | `16-resultado-por-conta-declarada.md` |
| Testes obrigatorios do documento | parcial | `09-testes-camada-declarada.md`, `14-validacoes-automaticas-metodologia.md` |

## Entregavel

Checklist de cobertura completa do Modulo 1.

## Criterios de sucesso

- Nenhuma secao do documento de referencia fica sem destino.
- Lacunas entre sistema atual e modulo desejado ficam explicitas.

