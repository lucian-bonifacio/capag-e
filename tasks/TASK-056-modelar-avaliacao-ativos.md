# TASK-056 - Modelar avaliacao de ativos

## SPEC De Origem

- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Dependencias

- `TASK-055-modelar-evidencias-materialidade.md`

## Objetivo

Modelar `AssetValuationAssessment`, valor contábil, deságio default, valor de liquidação forçada, valor ajustado e bloqueios de `PLRA`.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture.md`
- `specs/SPEC-005-modulo-4-evidencias-justificativas-ativos.md`

## Escopo Exato

- Criar contratos internos de avaliação de ativos.
- Aplicar política de deságio default existente.
- Permitir valor de liquidação forçada validado.
- Tratar ativo sem realizabilidade como valor econômico zero.
- Preservar essencialidade sem exclusão automática.

## Fora De Escopo

- Avaliação imobiliária real.
- Upload de laudo/anexo.
- Alterar regra de PLRA sem contrato.
- Criar API ou UI.

## Passos Executaveis

1. Modelar `AssetValuationAssessment`.
2. Implementar cálculo de valor econômico final.
3. Integrar evidência por `evidence_id`.
4. Criar testes de deságio, valor manual e zero econômico.

## Arquivos Ou Areas Provaveis

- `backend/app/domain/`
- `backend/app/engine/`
- `backend/tests/`

## Criterios De Aceite

- Valor validado prevalece sobre deságio default.
- Valor manual exige justificativa/evidência.
- Ativo essencial não é excluído automaticamente.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: deságio default virar avaliação real.
  Mitigação: registrar base e status da avaliação.

## Bloqueios Pendentes

Bloqueada até evidências e materialidade existirem.
