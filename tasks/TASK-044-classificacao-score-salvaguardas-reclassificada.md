# TASK-044 - Classificacao, score e salvaguardas reclassificadas

## SPEC De Origem

- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Dependencias

- `TASK-043-gerar-perfil-comportamental-conta.md`

## Objetivo

Implementar classificação determinística por família, score, confiança e salvaguardas da camada reclassificada, preservando conservadorismo e revisão humana para casos ambíguos.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Escopo Exato

- Implementar taxonomia MVP de famílias contábeis.
- Aplicar regras determinísticas com evidências positivas e negativas.
- Calcular score e confiança.
- Bloquear falso positivo em casos materiais, ambíguos ou sensíveis.
- Retornar status de revisão quando necessário.

## Fora De Escopo

- Sobrescrever camada declarada.
- Usar IA generativa como decisão.
- Criar UI de revisão.
- Criar exportação ou laudo.

## Passos Executaveis

1. Ler perfis comportamentais.
2. Implementar regras por família.
3. Implementar score e salvaguardas.
4. Criar testes de casos nominais, ambíguos e falso positivo.

## Arquivos Ou Areas Provaveis

- `backend/app/engine/`
- `backend/app/domain/`
- `backend/tests/`

## Criterios De Aceite

- Classificação não usa palavra-chave isolada.
- Falso positivo sensível vai para revisão.
- Score e confiança são auditáveis.
- Camada declarada permanece preservada.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: classificar agressivamente conta ambígua.
  Mitigação: salvaguardas conservadoras e revisão humana.

## Bloqueios Pendentes

Bloqueada até perfil comportamental existir.
