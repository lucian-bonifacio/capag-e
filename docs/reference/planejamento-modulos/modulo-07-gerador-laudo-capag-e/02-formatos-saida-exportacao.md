# 02 - Formatos de saida e exportacao

## Objetivo

Definir saidas do laudo.

## Implementacao minima

- `Excel` com abas de memoria e laudo estruturado.

## Implementacao desejavel futura

- `DOCX`;
- `PDF`;
- pacote de anexos.

## Regra

O laudo deve serializar resultados calculados e evidencias.

Nao deve executar regra de negocio adicional.

## Abas futuras

- `laudo_resumo`
- `laudo_metodologia`
- `laudo_ressalvas`
- `laudo_evidencias`

## Criterio de sucesso

O Excel deve permitir reconstruir a conclusao do laudo sem depender da UI.

