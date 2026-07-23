# TASK-088 - Pesquisar fonte oficial do plano referencial

## SPEC De Origem

- `specs/SPEC-010-governanca-plano-referencial-oficial.md`

## Dependencias

- `TASK-086-tabela-oficial-referencial-obrigatoria.md`

## Objetivo

Pesquisar, comparar e documentar fontes candidatas para o plano referencial oficial usado para validar e enriquecer o `COD_CTA_REF` declarado na ECD.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- `tasks/TASK-086-tabela-oficial-referencial-obrigatoria.md`

## Escopo Exato

- Identificar fontes candidatas para o plano referencial oficial.
- Registrar origem, acesso, formato, cobertura, leiaute, vigencia e tipo de entidade de cada fonte.
- Avaliar confiabilidade, completude, rastreabilidade e riscos de cada fonte.
- Comparar fontes candidatas em documento governado.
- Recomendar uma fonte oficial candidata para aprovacao do usuario.
- Registrar lacunas que impeçam carga operacional completa.

## Fora De Escopo

- Aprovar fonte sem decisao expressa do usuario.
- Popular o asset operacional completo.
- Criar banco, migration, API ou CRUD.
- Alterar metodologia interna, regra prudencial, formula ou arredondamento.
- Usar fonte pesquisada como normativa sem registro governado.

## Passos Executaveis

1. Ler a `SPEC-010` e os contratos de plano referencial da `SPEC-002`.
2. Levantar fontes candidatas autorizadas para pesquisa.
3. Registrar metadados de cada fonte candidata.
4. Comparar cobertura por leiaute, vigencia e tipo de entidade.
5. Registrar riscos, lacunas e criterio de confiabilidade.
6. Preparar recomendacao objetiva para decisao do usuario.
7. Atualizar documento governado de pesquisa da fonte.

## Arquivos Ou Areas Provaveis

- `docs/methodology/`
- `docs/reference/`, somente quando autorizado ou citado por fonte governada
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`, se houver ajuste governado aprovado

## Criterios De Aceite

- Fontes candidatas estao documentadas com origem, formato, cobertura e riscos.
- Recomendacao de fonte oficial candidata esta clara.
- Lacunas impeditivas estao registradas.
- Nenhuma fonte pesquisada foi usada como base operacional sem aprovacao.
- A decisao pendente do usuario esta explicita.

## Validacao Esperada

- Revisar consistencia documental contra `SPEC-010`.
- Conferir que nenhuma alteracao operacional foi feita em asset, banco, API ou motor.
- Registrar ausencia de testes automatizados quando a entrega for somente documental.

## Riscos

- Risco: fonte incompleta parecer suficiente.
  Mitigacao: registrar cobertura, lacunas e vigencia.

- Risco: fonte externa virar normativa por conveniencia.
  Mitigacao: exigir decisao expressa antes de aprovar ou carregar.

## Bloqueios Pendentes

- Aprovacao explicita da fonte oficial pelo usuario.
