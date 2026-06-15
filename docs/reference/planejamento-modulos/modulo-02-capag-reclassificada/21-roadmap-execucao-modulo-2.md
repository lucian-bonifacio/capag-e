# 21 - Roadmap de execucao do modulo 2

## Objetivo

Quebrar o modulo reclassificado em tasks pequenas e cronologicas.

## Sequencia sugerida

1. Decidir nome e linguagem do modulo.
2. Criar spec conceitual oficial.
3. Fechar decisao transversal sobre banco de dados e persistencia.
4. Mapear dados ECD necessarios e gaps do parser.
5. Especificar normalizacao comportamental.
6. Definir persistencia ou estrategia de recalculo dos perfis/scores.
7. Implementar razao por conta.
8. Implementar perfil comportamental.
9. Definir taxonomia MVP.
10. Implementar regras das 7 familias MVP.
11. Implementar motor de score e seguranca.
12. Implementar mapeamento familia -> referencial.
13. Implementar comparacao com camada declarada.
14. Decidir e implementar cenario de impacto ou cenario completo reclassificado.
15. Criar relatorio auditavel.
16. Criar API conforme arquitetura de persistencia aprovada.
17. Criar UI de revisao.
18. Ajustar exportacao comparativa.
19. Criar testes unitarios e integracao.
20. Medir qualidade do MVP.
21. Avaliar precedentes/calibracao persistidos conforme decisao de banco.
22. Usar a matriz de cobertura para verificar que nenhuma secao dos documentos de referencia ficou sem destino.
23. Transformar o exemplo de fluxo por conta em caso de teste ou criterio de aceite.
24. Validar riscos conceituais e salvaguardas antes de liberar classificacao automatica.

## Criterios de sucesso do MVP

- classificar corretamente contas obvias;
- identificar divergencias claras;
- evitar classificacao forcada em casos ambiguos;
- produzir justificativas compreensiveis;
- permitir revisao humana;
- preservar a camada declarada;
- usar banco de dados somente se a decisao arquitetural transversal tiver sido aprovada.
