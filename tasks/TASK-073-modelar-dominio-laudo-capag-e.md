# TASK-073 - Modelar dominio do laudo CAPAG-E

## SPEC De Origem

- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Dependencias

- `TASK-054-exportacao-e-testes-contrato-capag-e.md`
- `TASK-060-exportacao-e-testes-evidencias-ativos.md`

## Objetivo

Modelar `CapagReport`, `ReportSection`, status do laudo e seções obrigatórias, sem gerar arquivo final nem recalcular motores.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Escopo Exato

- Criar contratos internos do laudo.
- Modelar seções obrigatórias.
- Modelar status `rascunho`, `preliminar`, `com_ressalvas`, `final` e `bloqueado`.
- Referenciar resultados calculados e evidências.

## Fora De Escopo

- Gerar Excel, DOCX ou PDF.
- Recalcular PLRA, FCA, ROA ou CAPAG-E.
- Criar API ou UI.

## Passos Executaveis

1. Ler contratos da SPEC-008.
2. Criar modelos de domínio.
3. Criar testes de construção de seções.

## Arquivos Ou Areas Provaveis

- `backend/app/report/`
- `backend/app/domain/`
- `backend/tests/`

## Criterios De Aceite

- Laudo referencia objetos calculados.
- Seções obrigatórias existem.
- Nenhum motor é chamado pelo domínio do laudo.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: laudo virar motor.
  Mitigação: camada `report` apenas monta artefato.

## Bloqueios Pendentes

Bloqueada até contrato CAPAG-E e evidências existirem.
