# TASK-093 - Desenhar CRUD controlado do plano referencial

## SPEC De Origem

- `specs/SPEC-010-governanca-plano-referencial-oficial.md`

## Dependencias

- `TASK-092-desenhar-persistencia-versionamento-plano-referencial.md`

## Objetivo

Desenhar a administracao controlada do plano referencial oficial, incluindo operacoes permitidas, permissoes, auditoria, publicacao, bloqueio, comparacao de versoes e limites contra edicao livre de metodologia.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-001-modulo-0-fundacao-governada.md`
- `specs/SPEC-002-modulo-1-camada-declarada.md`
- `specs/SPEC-009-modulo-8-governanca-metodologia.md`
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`
- desenho tecnico da `TASK-092`
- documentos frontend governados, se houver desenho de UX

## Escopo Exato

- Definir operacoes administrativas permitidas e proibidas.
- Definir regras de permissao, justificativa e auditoria.
- Definir estados e transicoes de publicacao, bloqueio e substituicao.
- Definir UX conceitual para consulta, importacao, validacao, publicacao, bloqueio e comparacao de versoes.
- Definir criterios para futura API administrativa.
- Garantir que CRUD nao permita recalculo prudencial nem sugestao de reclassificacao.

## Fora De Escopo

- Implementar tela, endpoint, permissao ou migration.
- Editar regra prudencial ou metodologia interna.
- Permitir edicao livre de codigo publicado.
- Excluir historico.
- Alterar vigencia retroativamente sem nova versao e auditoria.

## Passos Executaveis

1. Ler `SPEC-010`, desenho de persistencia e documentos frontend se aplicavel.
2. Definir operacoes permitidas e proibidas.
3. Definir estados, transicoes, justificativas e trilha de auditoria.
4. Desenhar fluxos administrativos conceituais.
5. Definir gates para futuras TASKs de API e UI.
6. Registrar criterios de aceite para implementacao futura.

## Arquivos Ou Areas Provaveis

- `docs/methodology/`
- `docs/frontend/`, se houver artefato de UX governado
- `specs/SPEC-010-governanca-plano-referencial-oficial.md`, se houver ajuste aprovado

## Criterios De Aceite

- Operacoes administrativas permitidas e proibidas estao claras.
- Publicacao, bloqueio e substituicao exigem justificativa e auditoria.
- Edicao de codigo publicado nao altera historico silenciosamente.
- CRUD nao permite alterar metodologia prudencial.
- Futuros endpoints e telas tem gates definidos.

## Validacao Esperada

- Revisar consistencia documental contra PRD, arquitetura, documentos frontend e `SPEC-010`.
- Conferir que nenhuma UI, API ou migration foi implementada.
- Registrar ausencia de testes automatizados quando a entrega for somente desenho.

## Riscos

- Risco: CRUD virar editor livre de metodologia.
  Mitigacao: separar plano oficial de metodologia interna e exigir auditoria.

- Risco: UI sugerir reclassificacao por conta.
  Mitigacao: limitar UX a consulta e administracao da base oficial.

## Bloqueios Pendentes

- Modelo de persistencia/versionamento aprovado.
- Regras de permissao, auditoria e publicacao aprovadas antes de implementacao executiva.
