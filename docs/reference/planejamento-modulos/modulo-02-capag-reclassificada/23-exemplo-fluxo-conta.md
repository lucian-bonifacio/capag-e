# 23 - Exemplo de fluxo para uma conta

## Objetivo

Manter um exemplo concreto de ponta a ponta para validar se o Modulo 2 esta coerente.

## Ponto de decisao

Decidir se este exemplo sera usado como fixture/teste de aceitacao quando o modulo for implementado.

## Exemplo base

Conta:

- `PARS PRODUTOS DE PROCESSAMENTO DE DADOS LTDA`

Classificacao declarada:

- `I051 original = 1.01.02.02.01`

Comportamento observado hipotetico:

- saldo tipico credor;
- creditos contra despesas operacionais;
- debitos contra banco;
- historicos com pagamento, nota fiscal e boleto;
- nome parece razao social de fornecedor.

## Fluxo esperado

1. O parser le o `I050`.
2. O parser le o `I051` original.
3. O modulo comportamental localiza partidas `I250` da conta.
4. O razao por conta e montado.
5. As contrapartidas sao classificadas.
6. O perfil comportamental e calculado.
7. As regras de familia sao aplicadas.
8. O score por familia e calculado.
9. A familia `FORNECEDORES` vence com alta confianca.
10. O sistema mapeia para uma classificacao referencial sugerida de fornecedor/passivo.
11. O sistema compara com o `I051` original.
12. Como o original indica ativo e o comportamento indica passivo, a acao recomendada e `reclassificar`.
13. O relatorio explica as evidencias.
14. Se a confianca for alta e nao houver salvaguarda, entra no cenario reclassificado.
15. Se houver ambiguidade/materialidade sensivel, vai para revisao humana.

## Saida esperada por conta

- conta original;
- `I051` original;
- familia sugerida;
- codigo referencial sugerido;
- score;
- confianca;
- acao recomendada;
- evidencias positivas;
- evidencias negativas;
- justificativa;
- impacto no PLR/CAPAG-e;
- status de revisao.

## Como usar este exemplo

Este exemplo deve ser usado para conferir:

- se o modulo nao decide apenas por nome;
- se saldo, contrapartida e historico entram na decisao;
- se o `I051` original e preservado;
- se a divergencia fica explicavel;
- se a reclassificacao nao altera silenciosamente a camada declarada.

## Criterios de sucesso

- O exemplo percorre todas as etapas principais do Modulo 2.
- A justificativa final seria compreensivel por contador, auditor ou usuario tecnico.

## Fora do escopo

- Tratar este exemplo como regra universal.
- Assumir que todo nome empresarial e fornecedor.

