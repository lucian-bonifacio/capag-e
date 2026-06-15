# 10 - Roadmap de execucao do modulo 1

## Objetivo

Quebrar a implementacao futura da camada declarada em tasks pequenas e cronologicas.

## Ponto de decisao

Decidir quais tasks oficiais devem ser criadas em `tasks/` quando este planejamento for aprovado.

## Sequencia sugerida

1. Diagnosticar camada declarada atual.
2. Criar spec oficial da camada declarada.
3. Criar spec do plano referencial oficial e metodologia interna.
4. Fechar decisao transversal sobre banco de dados e persistencia.
5. Revisar matriz de cobertura e gap analysis.
6. Definir artefato ou tabela do plano referencial oficial.
7. Definir persistencia/snapshot da camada declarada, se banco for aprovado.
8. Definir status de regras e bloqueio de prefixo amplo.
9. Definir algoritmo de match metodologico seguro.
10. Definir validacoes automaticas da metodologia.
11. Ajustar metodologia PLR para regras especificas.
12. Ajustar metodologia FCO para regras especificas e exclusoes.
13. Ajustar motor/auditoria se necessario.
14. Ajustar resultado por conta/payload/API.
15. Ajustar frontend para exibir dados declarados sem recalcular.
16. Ajustar exportacao Excel.
17. Criar testes unitarios e integracao.
18. Validar exemplo completo da conta `1725`.
19. Atualizar README/AGENTS/CLAUDE/skills depois da implementacao aprovada.

## Criterios de sucesso

- Cada task futura e pequena.
- O modulo declarado e implementado antes do modulo comportamental.
- A alteracao de `ajuste_modulo_principal.md` nao fica escondida em uma unica task grande.
