# 05 - Testes do contrato CAPAG-E

## Objetivo

Definir a cobertura minima de testes para impedir regressao conceitual.

## Testes obrigatorios

1. Mapear `plr_ajustado` para `PLRA`.
2. Bloquear `CAPAG-E` sem `PLRA`.
3. Bloquear `FCA + PLRA` sem `FCA`.
4. Bloquear `ROA + PLRA` sem `ROA`.
5. Identificar `FCA parcial` quando so houver `FCO`.
6. Serializar formula selecionada.
7. Garantir uso exclusivo de `Decimal`.

## Areas afetadas

- `domain`
- `engine`
- `api`
- `export`
- `frontend`

## Testes por camada

### Dominio

- Validar status permitidos.
- Validar metodos permitidos.
- Validar bloqueios.

### Engine

- Validar combinacao de componentes.
- Garantir que valores intermediarios sejam preservados.

### API

- Validar payload canonico.
- Validar serializacao de `Decimal` como texto ou formato aprovado.

### Exportacao

- Validar aba/bloco `contrato_capag_e`.
- Validar que a exportacao nao recalcula.

### Frontend

- Validar exibicao de metodo e status.
- Validar que `FCO` nao e exibido como `FCA` final.

## Criterio de sucesso

Uma mudanca futura em `FCA`, `ROA` ou laudo nao deve quebrar a linguagem canonica do sistema sem teste falhar.

