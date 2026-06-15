# 14 - Revisao humana e precedentes

## Objetivo

Planejar como o usuario revisara sugestoes e como precedentes serao tratados sem quebrar a V2.

## Ponto de decisao

Decidir se precedentes entram no MVP ou ficam como fase futura.

## Revisao humana

A interface deve permitir:

- aprovar sugestao;
- rejeitar sugestao;
- escolher outra classificacao;
- marcar como excecao;
- comentar;
- registrar precedente, se permitido.

## Precedentes

Camadas sugeridas:

1. mesma empresa;
2. mesmo grupo economico;
3. mesmo setor;
4. global validado.

## Persistencia

Precedentes persistidos dependem da decisao arquitetural sobre banco de dados.

Alternativas enquanto a decisao nao estiver implementada:

- precedentes temporarios da sessao;
- artefatos internos versionados, se aprovados;
- apenas desenho conceitual para futuro.

## Entregavel

Spec de revisao humana e politica de precedentes.

## Criterios de sucesso

- Revisao humana e rastreavel.
- Precedentes nao viram persistencia escondida.

## Fora do escopo

- Criar banco de precedentes antes da decisao arquitetural transversal.
- Multiusuario.
