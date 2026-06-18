# TASK-074 - Validar status do laudo

## SPEC De Origem

- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Dependencias

- `TASK-073-modelar-dominio-laudo-capag-e.md`

## Objetivo

Implementar validações para emissão de laudo final, preliminar, com ressalvas ou bloqueado, sem recalcular resultados.

## Fontes Usadas

- `docs/product/PRD.md`
- `docs/architecture/architecture.md`
- `specs/SPEC-008-modulo-7-gerador-laudo-capag-e.md`

## Escopo Exato

- Validar método definido.
- Validar `PLRA` final.
- Validar `FCA` ou `ROA` conforme método.
- Validar evidências críticas.
- Validar versão metodológica.

## Fora De Escopo

- Gerar arquivo.
- Criar UI.
- Recalcular motores.
- Definir formato DOCX/PDF.

## Passos Executaveis

1. Implementar validador de status.
2. Mapear falhas para bloqueios ou ressalvas.
3. Criar testes de status final, preliminar e bloqueado.

## Arquivos Ou Areas Provaveis

- `backend/app/report/`
- `backend/tests/`

## Criterios De Aceite

- Laudo final exige componentes suficientes.
- Evidência crítica pendente bloqueia ou ressalva conforme contrato.
- Status é explícito.

## Validacao Esperada

- Executar testes backend via `docker compose`.

## Riscos

- Risco: emitir laudo final com pendência.
  Mitigação: validações bloqueantes obrigatórias.

## Bloqueios Pendentes

Bloqueada até domínio do laudo existir.
