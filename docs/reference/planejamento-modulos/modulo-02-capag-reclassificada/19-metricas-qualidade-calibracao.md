# 19 - Metricas de qualidade e calibracao

## Objetivo

Definir como medir se o modulo reclassificado esta funcionando bem.

## Metricas principais

- taxa de classificacao automatica;
- taxa de revisao;
- taxa de acerto;
- taxa de divergencia real;
- taxa de falso positivo;
- taxa de falso negativo;
- cobertura por valor;
- cobertura por quantidade.

## Regra importante

Nao medir apenas quantidade de contas.

Materialidade importa: uma conta com valor alto deve pesar mais que uma conta irrelevante.

## Calibracao

Camadas possiveis:

- regras universais;
- camada setorial;
- camada da empresa;
- precedentes aprovados.

## Persistencia

Calibracao persistida depende da decisao arquitetural sobre banco de dados. Se banco for aprovado para o MVP, esta tarefa deve definir quais metricas e calibracoes serao persistidas.

## Entregavel

Spec de metricas de qualidade e calibracao.

## Criterios de sucesso

- O modulo pode ser avaliado por acerto e risco.
- Falso positivo vira metrica central.
