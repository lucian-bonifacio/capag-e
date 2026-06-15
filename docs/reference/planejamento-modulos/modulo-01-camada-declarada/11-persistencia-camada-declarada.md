# 11 - Persistencia da camada declarada

## Objetivo

Planejar quais dados da camada declarada devem ser persistidos caso a nova arquitetura aprove banco de dados.

## Ponto de decisao

Decidir se a camada declarada sera recalculada sempre a partir da ECD em memoria ou se tera snapshots persistidos por empresa/exercicio/arquivo.

## Dependencia arquitetural

Esta tarefa depende de:

- `tmp_deu_a_louca/modulo-00-organizacao-arquitetura-design/11-decisao-banco-dados-persistencia.md`

## Dados candidatos a persistencia

- empresa;
- arquivo ECD importado;
- hash do arquivo;
- exercicio;
- plano de contas extraido;
- vinculos `I051`;
- saldos anuais;
- lancamentos e partidas necessarios;
- resultado PLR declarado;
- resultado FCO declarado;
- resultado CAPAG-e declarado;
- linhas de auditoria;
- alertas;
- inconsistencias;
- exportacoes geradas;
- versao da metodologia usada.

## Cuidados

- Persistir resultado sem perder capacidade de reproduzir calculo.
- Registrar versao dos assets/metodologia usados.
- Evitar que alteracao futura da metodologia apague resultado historico.
- Definir se ECD bruta sera armazenada ou apenas hash/metadados.
- Definir regras de dados sensiveis.

## Arquivos correlatos futuros

- futuro modulo de persistencia;
- `src/capag/domain/models.py`;
- `src/capag/engine/plr.py`;
- `src/capag/engine/fco.py`;
- `src/capag/export/excel.py`;
- `src/capag/api/`.

## Entregavel

Modelo de persistencia da camada declarada, se banco for aprovado.

## Criterios de sucesso

- A camada declarada fica rastreavel no tempo.
- Resultado historico nao muda silenciosamente com metodologia nova.
- Persistencia nao substitui os testes do motor.

## Fora do escopo

- Criar tabelas reais agora.
- Alterar codigo.

