# 01 - Matriz de cobertura da SPEC-06

## Objetivo

Garantir que todos os pontos de `docs/specs/spec-06-contrato-capag-e-plra-fca-roa.md` estejam cobertos no planejamento do Modulo 03.

## Matriz

| Secao da SPEC-06 | Cobertura no Modulo 03 |
|---|---|
| Objetivo | `00-visao-geral.md` |
| Motivacao | `00-visao-geral.md` |
| Escopo | `00-visao-geral.md` |
| Definicoes canonicas | `02-contrato-dominio-capag-e.md` |
| `PLR bruto` | `02-contrato-dominio-capag-e.md` |
| `PLRA` | `02-contrato-dominio-capag-e.md` |
| `FCO` | `02-contrato-dominio-capag-e.md` |
| `FCA` | `02-contrato-dominio-capag-e.md`, `03-status-bloqueios-metodos.md` |
| `ROA` | `02-contrato-dominio-capag-e.md`, `03-status-bloqueios-metodos.md` |
| `CAPAG-E` | `02-contrato-dominio-capag-e.md`, `03-status-bloqueios-metodos.md` |
| Contrato de resultado | `02-contrato-dominio-capag-e.md` |
| Regras de formula | `03-status-bloqueios-metodos.md` |
| Regras numericas | `02-contrato-dominio-capag-e.md`, `05-testes-contrato-capag-e.md` |
| Compatibilidade com sistema atual | `02-contrato-dominio-capag-e.md`, `06-roadmap-execucao-modulo-3.md` |
| API e serializacao | `04-api-exportacao-ui-contrato.md` |
| UI | `04-api-exportacao-ui-contrato.md` |
| Exportacao | `04-api-exportacao-ui-contrato.md` |
| Testes obrigatorios | `05-testes-contrato-capag-e.md` |
| Criterios de aceite | `06-roadmap-execucao-modulo-3.md` |

## Lacunas identificadas

- O sistema atual ainda usa majoritariamente `PLR ajustado`, `FCO` e `CAPAG-e`.
- A distincao formal entre `FCO` e `FCA` precisa entrar no dominio e na API.
- A escolha do metodo de `CAPAG-E` ainda precisa ser explicitada.
- O frontend precisa deixar de apresentar valores finais sem status metodologico.
- A exportacao precisa incluir o bloco `contrato_capag_e`.

## Criterio de sucesso

Nenhum motor futuro deve precisar inventar nomes, status ou formulas por conta propria.

