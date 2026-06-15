# 06 - Testes de evidencias e ativos

## Objetivo

Definir cobertura minima para a camada documental e patrimonial.

## Testes da SPEC-07

1. Criar evidencia por decisao metodologica manual.
2. Calcular materialidade a partir do impacto.
3. Bloquear laudo final quando evidencia critica estiver pendente.
4. Permitir evidencia dispensada com justificativa.
5. Serializar evidencias na API.
6. Exportar evidencias na aba correta.
7. Garantir que evidencia nao altera valor calculado por si so.

## Testes da SPEC-08

1. Ativo com laudo validado substitui desagio default.
2. Ativo material sem laudo gera bloqueio ou ressalva.
3. Ativo essencial excluido sem justificativa bloqueia.
4. Valor manual exige evidencia.
5. Auditoria exibe valor contabil, default e final.
6. Exportacao inclui aba `avaliacao_ativos`.

## Areas afetadas

- `domain`
- `engine`
- `api`
- `export`
- `frontend`
- `tests`

## Criterio de sucesso

O sistema nao deve conseguir emitir resultado final sem registrar pendencias documentais relevantes.

