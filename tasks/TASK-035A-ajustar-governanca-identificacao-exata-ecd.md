# TASK-035A - Ajustar governanca da identificacao exata da ECD

## SPEC De Origem

- `specs/SPEC-002-modulo-1-camada-declarada.md`

## Dependencias

- `TASK-035-estruturar-assets-camada-declarada.md`

## Objetivo

Ajustar os artefatos governados da camada declarada para registrar que a identificacao parte sempre do `COD_CTA_REF` exato declarado na ECD, cabendo ao plano referencial oficial validar/enriquecer esse codigo e a metodologia interna aplicar tratamento sem inferencia por prefixo.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-036-implementar-matcher-metodologico-declarado.md`
- Decisao do usuario nesta sessao: plano oficial valida/enriquece o codigo exato da ECD; metodologia interna nao deve inferir tratamento por prefixo.

## Escopo Exato

- Atualizar a SPEC-002 para trocar a regra de match metodologico por prefixo pela regra de tratamento por codigo exato.
- Registrar que o plano referencial oficial funciona como legenda, validador e enriquecedor do `COD_CTA_REF` declarado, sem identificar codigo alternativo.
- Ajustar campos ou exemplos de assets metodologicos quando mencionarem `match_type` ou padroes por prefixo incompatíveis com a nova decisao.
- Ajustar a `TASK-036` para que sua execucao implemente apenas tratamento metodologico por codigo exato.
- Registrar no log da `TASK-036` que a primeira execucao foi devolvida para ajuste por mudanca governada de decisao.

## Fora De Escopo

- Implementar o matcher ajustado.
- Popular plano referencial oficial completo.
- Criar regras metodologicas reais.
- Implementar parser ECD, API, frontend, Excel ou laudo.
- Alterar regra prudencial, formula, arredondamento ou contrato de API.

## Passos Executaveis

1. Atualizar a SPEC-002 nos trechos de decisoes, metodologia interna, algoritmo de match, criterios de aceite e testes esperados.
2. Ajustar os templates de assets da camada declarada apenas se houver campo ou valor que contradiga a identificacao exata.
3. Ajustar a `TASK-036` para remover criterio de prefixo e exigir match metodologico exato.
4. Atualizar o log da `TASK-036` para registrar ajuste solicitado.
5. Validar diff restrito aos artefatos governados e templates afetados.

## Arquivos Ou Areas Provaveis

- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `tasks/TASK-036-implementar-matcher-metodologico-declarado.md`
- `backend/app/assets/methodology/internal_methodology_rules.template.json`
- `logs/LOG-036-implementar-matcher-metodologico-declarado.md`

## Criterios De Aceite

- SPEC-002 afirma que a identificacao usa o codigo exato vindo da ECD.
- SPEC-002 afirma que o plano referencial oficial valida/enriquece o codigo declarado, sem inferir codigo alternativo.
- SPEC-002 afirma que a metodologia interna aplica tratamento por codigo exato, sem fallback por prefixo.
- TASK-036 passa a exigir matcher exato e status `NAO_MAPEADO_METODOLOGICAMENTE` quando nao houver regra metodologica exata.
- Nenhuma implementacao de motor e executada nesta TASK.

## Validacao Esperada

- Conferir `git diff --stat`.
- Conferir que os diffs ficam restritos a SPEC, TASK, templates de assets quando necessario e log da TASK-036.
- Validar que nao foi criada regra metodologica real.

## Riscos

- Risco: manter texto antigo permitindo prefixo seguro em algum trecho da SPEC.
  Mitigacao: revisar decisoes, algoritmo, criterios de aceite e testes esperados.
- Risco: misturar ajuste governado com implementacao do matcher.
  Mitigacao: limitar esta TASK a artefatos governados e deixar implementacao para a TASK-036.

## Bloqueios Pendentes

Nenhum.

