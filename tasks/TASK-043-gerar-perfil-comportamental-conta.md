# TASK-043 - Gerar perfil comportamental por conta

## SPEC De Origem

- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Dependencias

- `TASK-042-normalizacao-razao-comportamental.md`

## Objetivo

Gerar `BehavioralAccountProfile` por conta com métricas financeiras, de contrapartida, textuais e hierárquicas, sem decidir reclassificação final.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-003-modulo-2-capag-reclassificada.md`

## Escopo Exato

- Calcular métricas financeiras com `Decimal`.
- Calcular métricas de contrapartida.
- Registrar sinais textuais e hierárquicos como evidências, não como decisão isolada.
- Associar versão metodológica.

## Fora De Escopo

- Calcular score final.
- Aplicar revisão humana.
- Criar cenário reclassificado.
- Criar API ou frontend.

## Passos Executaveis

1. Ler razão comportamental.
2. Implementar perfil por conta.
3. Criar testes de métricas.
4. Validar que não há recomendação final nesta TASK.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Perfil contém métricas mínimas da SPEC-003.
- Evidências positivas e negativas são preservadas.
- Nome/histórico não decide família sozinho.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: perfil virar classificação.
  Mitigação: separar métricas de decisão.

## Bloqueios Pendentes

Bloqueada até razão comportamental existir.
