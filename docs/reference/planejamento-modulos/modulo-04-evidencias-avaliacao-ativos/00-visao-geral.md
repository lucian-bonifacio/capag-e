# 00 - Visao geral do Modulo 04

## Objetivo

Planejar a camada de evidencias, justificativas, materialidade e avaliacao de ativos.

## Fontes principais

- `docs/specs/spec-07-evidencias-justificativas-ajustes-laudo.md`
- `docs/specs/spec-08-avaliacao-ativos-liquidacao-forcada.md`

## Papel do modulo

Este modulo transforma o sistema de calculo em um sistema defensavel documentalmente.

Ele cria a ponte entre:

- ajuste metodologico;
- justificativa do analista;
- evidencia esperada;
- materialidade;
- bloqueio;
- ressalva;
- laudo futuro.

## Por que SPEC-07 e SPEC-08 ficam juntas

A `SPEC-07` define a camada geral de evidencias.

A `SPEC-08` e uma especializacao dessa camada para ativos, liquidacao forcada, essencialidade operacional e impacto no `PLRA`.

Separar demais poderia duplicar regras de materialidade, status e bloqueio.

## Relacao com modulos anteriores

- Modulo 01 gera ajustes e pendencias na camada declarada.
- Modulo 02 gera evidencias comportamentais e revisoes humanas.
- Modulo 03 define componentes `PLRA`, `FCA`, `ROA` e `CAPAG-E`.
- Modulo 04 define quando um ajuste precisa de justificativa/evidencia e quando bloqueia.

## Relacao com modulos posteriores

- Modulo 05 usa evidencias para fluxos de caixa materiais.
- Modulo 06 usa evidencias para despesas, receitas e pressoes materiais.
- Modulo 07 consome evidencias para o laudo.
- Modulo 08 governa metodologia, rastreabilidade e versao dos documentos.

## Fora do escopo

- Upload persistente de anexos.
- Assinatura digital.
- Integracao com GED.
- Geracao automatica de laudo ABNT.
- Avaliacao imobiliaria real.

