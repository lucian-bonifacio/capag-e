# 00 - Visao geral do Modulo 03

## Objetivo

Definir o contrato canonico de resultado da `CAPAG-E`.

Este modulo transforma a linguagem atual do sistema, baseada em `PLR ajustado`, `FCO` e `CAPAG-e`, em uma linguagem compativel com o laudo e com a resposta da PGFN:

- `PLRA`
- `FCA`
- `ROA`
- `CAPAG-E`

## Fonte principal

- `docs/specs/spec-06-contrato-capag-e-plra-fca-roa.md`

## Papel do modulo

Este modulo deve ser executado antes dos motores novos de `DFC/FCA`, `ROA` e antes do gerador de laudo.

Ele nao calcula tudo sozinho. Ele define:

- nomes canonicos;
- status permitidos;
- metodos aceitos;
- formulas aceitas;
- bloqueios;
- contrato de API;
- contrato de exportacao;
- linguagem de frontend;
- criterios minimos de teste.

## Relacao com modulos anteriores

- Modulo 01 entrega a camada declarada e o `PLR ajustado`.
- Modulo 03 passa a tratar `PLR ajustado` como `PLRA` para fins de laudo.
- Modulo 01 pode continuar exibindo `PLR ajustado` em contexto tecnico.
- Modulo 03 impede que `FCO` seja chamado de `FCA` completo sem ressalva.
- Modulo 02 podera comparar resultado declarado/reclassificado usando o contrato canonico deste modulo.

## Relacao com modulos posteriores

- Modulo 04 usa o contrato para bloquear componentes por evidencia.
- Modulo 05 entrega `FCA` final ou parcial.
- Modulo 06 entrega `ROA` final.
- Modulo 07 consome o contrato para gerar o laudo.
- Modulo 08 garante rastreabilidade e versao metodologica.

## Decisoes centrais

1. `PLRA = PLR ajustado` para fins de laudo.
2. `FCO` nao e sinonimo de `FCA`.
3. Enquanto so existir `FCO`, o sistema deve rotular como `FCA parcial`.
4. `CAPAG-E` so pode ser final com metodo definido.
5. Os metodos aceitos sao:
   - `fca_plra`
   - `roa_plra`
   - `comparativo_fca_roa`
   - `nao_definido`
6. Todo resultado deve carregar valor, status, formula, limitacoes e bloqueios.

## Fora do escopo

- Implementar DFC completa.
- Implementar ROA.
- Gerar laudo textual completo.
- Criar upload de anexos.
- Criar persistencia final.

Esses pontos pertencem aos modulos seguintes.

