# 09 - Motor de score, confianca e seguranca

## Objetivo

Definir como o modulo calcula score, nivel de confianca e acao recomendada.

## Ponto de decisao

Decidir limiares iniciais do MVP.

## Criterios iniciais sugeridos

- score >= 80: classificacao automatica no cenario comportamental;
- score entre 60 e 79: sugestao com revisao recomendada;
- score entre 40 e 59: baixa confianca e revisao obrigatoria;
- score < 40: sem classificacao.

## Regra de diferenca entre primeiro e segundo colocado

- diferenca >= 20 pontos: decisao mais segura;
- diferenca < 20 pontos: marcar como ambigua.

## Regras de seguranca

O sistema nao deve reclassificar automaticamente quando houver:

- score baixo;
- diferenca pequena entre familias;
- poucos lancamentos;
- lancamentos compostos demais;
- historico generico;
- conta sintetica;
- conta de encerramento;
- conta transitoria;
- comportamento instavel entre periodos;
- materialidade elevada com evidencia insuficiente;
- tributos;
- partes relacionadas;
- patrimonio liquido;
- classificacoes sensiveis.

## Entregavel

Politica de score, confianca e seguranca.

## Criterios de sucesso

- O modulo prefere revisao humana a falso positivo.
- Decisoes automaticas sao conservadoras.

## Fora do escopo

- Calibrar com banco de precedentes persistido.

