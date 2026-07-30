# ROADMAP

## Instruções De Uso

Antes de executar qualquer item deste roadmap, leia e siga o `AGENTS.md`.

Este arquivo é o painel de controle operacional e o plano mestre de execução do projeto. Ele deve responder rapidamente qual é a próxima tarefa, quais tarefas existem, qual o status de cada uma e onde encontrar o detalhamento e o log de execução.

O detalhamento robusto das tarefas fica em `tasks/`. O log de execução fica em `logs/`.

Status permitidos:

- `pendente`
- `aguardando_homologacao`
- `concluido`

Regras:

- Toda tarefa planejada até a conclusão do projeto deve estar representada neste arquivo.
- A seção `## Próxima Tarefa` deve apontar sempre para o próximo item executável permitido pelo fluxo do `AGENTS.md`.
- Se o usuário pedir algo que ainda não está previsto, siga o fluxo de escopo do `AGENTS.md` antes de alterar este roadmap.
- Tarefas concluídas devem apontar para um arquivo em `tasks/` e um arquivo em `logs/`.
- Não use este arquivo como log de terminal, histórico detalhado de execução ou depósito longo de ideias.
- Atualize este arquivo somente nos momentos definidos no fluxo de trabalho do `AGENTS.md`.

## Próxima Tarefa

Ao iniciar a próxima sessão:

1. Ler integralmente o
   `logs/LOG-ESPECIAL-002-30.07.2026-16h50min.md`.
2. Informar ao usuário que o Log Especial de pendências pós-homologação foi
   consultado.
3. Tratar primeiro a pendência obrigatória de criar TASK governada para melhorar
   os gates das skills em ajustes de frontend/design/UI/UX.
4. Pedir confirmação explícita antes de criar qualquer TASK.
5. Após resolver a pendência obrigatória, recalcular a próxima tarefa pelo fluxo
   normal deste roadmap.

## Lista De Tarefas

1. [x] Criar índice e convenção de TASKs
   - Status: concluido
   - Task: `tasks/TASK-001-criar-indice-e-convencao-de-tasks.md`
   - Log: `logs/LOG-001-criar-indice-e-convencao-de-tasks.md`

2. [x] Auditar estrutura mínima do repositório
   - Status: concluido
   - Task: `tasks/TASK-002-auditar-estrutura-minima-repositorio.md`
   - Log: `logs/LOG-002-auditar-estrutura-minima-repositorio.md`

3. [x] Descontinuar reports em TASKs pendentes
   - Status: concluido
   - Task: `tasks/TASK-002A-descontinuar-reports-em-tasks-pendentes.md`
   - Log: `logs/LOG-002A-descontinuar-reports-em-tasks-pendentes.md`

4. [x] Criar estrutura backend mínima
   - Status: concluido
   - Task: `tasks/TASK-003-criar-estrutura-backend-minima.md`
   - Log: `logs/LOG-003-criar-estrutura-backend-minima.md`

5. [x] Auditar estrutura frontend governada
   - Status: concluido
   - Task: `tasks/TASK-004-auditar-estrutura-frontend-governada.md`
   - Log: `logs/LOG-004-auditar-estrutura-frontend-governada.md`

6. [x] Auditar índice e rastreabilidade de SPECs
   - Status: concluido
   - Task: `tasks/TASK-005-auditar-indice-e-rastreabilidade-de-specs.md`
   - Log: `logs/LOG-005-auditar-indice-e-rastreabilidade-de-specs.md`

7. [x] Auditar validações mínimas do projeto
   - Status: concluido
   - Task: `tasks/TASK-006-auditar-validacoes-minimas-do-projeto.md`
   - Log: `logs/LOG-006-auditar-validacoes-minimas-do-projeto.md`

8. [x] Auditar documentos operacionais e agentes
   - Status: concluido
   - Task: `tasks/TASK-007-auditar-documentos-operacionais-e-agentes.md`
   - Log: `logs/LOG-007-auditar-documentos-operacionais-e-agentes.md`

9. [x] Organizar estrutura frontend mínima
   - Status: concluido
   - Task: `tasks/TASK-008-organizar-estrutura-frontend-minima.md`
   - Log: `logs/LOG-008-organizar-estrutura-frontend-minima.md`

10. [x] Auditar assets metodológicos e versionamento
   - Status: concluido
   - Task: `tasks/TASK-009-auditar-assets-metodologicos-e-versionamento.md`
   - Log: `logs/LOG-009-auditar-assets-metodologicos-e-versionamento.md`

11. [x] Auditar ambiente local e configuração
    - Status: concluido
    - Task: `tasks/TASK-010-auditar-ambiente-local-e-configuracao.md`
    - Log: `logs/LOG-010-auditar-ambiente-local-e-configuracao.md`

12. [x] Auditar fronteiras de camadas
    - Status: concluido
    - Task: `tasks/TASK-011-auditar-fronteiras-de-camadas.md`
    - Log: `logs/LOG-011-auditar-fronteiras-de-camadas.md`

13. [x] Reorganizar documentação oficial de arquitetura
    - Status: concluido
    - Task: `tasks/TASK-011B-reorganizar-documentacao-oficial-arquitetura.md`
    - Log: `logs/LOG-011B-reorganizar-documentacao-oficial-arquitetura.md`

14. [x] Criar artefato governado de fronteiras de camadas
    - Status: concluido
    - Task: `tasks/TASK-011A-criar-artefato-governado-fronteiras-camadas.md`
    - Log: `logs/LOG-011A-criar-artefato-governado-fronteiras-camadas.md`

15. [x] Criar índice oficial de SPECs
    - Status: concluido
    - Task: `tasks/TASK-012-criar-indice-oficial-de-specs.md`
    - Log: `logs/LOG-012-criar-indice-oficial-de-specs.md`

16. [x] Criar configuração Docker Compose mínima
    - Status: concluido
    - Task: `tasks/TASK-013-criar-configuracao-docker-compose-minima.md`
    - Log: `logs/LOG-013-criar-configuracao-docker-compose-minima.md`

17. [x] Nomear containers Docker Compose
    - Status: concluido
    - Task: `tasks/TASK-013A-nomear-containers-docker-compose.md`
    - Log: `logs/LOG-013A-nomear-containers-docker-compose.md`

18. [x] Ajustar Docker Compose dev e politica de env
    - Status: concluido
    - Task: `tasks/TASK-013B-ajustar-docker-compose-dev-env.md`
    - Log: `logs/LOG-013B-ajustar-docker-compose-dev-env.md`

19. [x] Configurar testes backend mínimos
    - Status: concluido
    - Task: `tasks/TASK-014-configurar-testes-backend-minimos.md`
    - Log: `logs/LOG-014-configurar-testes-backend-minimos.md`

20. [x] Configurar testes frontend mínimos
    - Status: concluido
    - Task: `tasks/TASK-015-configurar-testes-frontend-minimos.md`
    - Log: `logs/LOG-015-configurar-testes-frontend-minimos.md`

21. [x] Configurar CI mínimo
    - Status: concluido
    - Task: `tasks/TASK-016-configurar-ci-minimo.md`
    - Log: `logs/LOG-016-configurar-ci-minimo.md`

22. [x] Configurar Alembic mínimo
    - Status: concluido
    - Task: `tasks/TASK-017-configurar-alembic-minimo.md`
    - Log: `logs/LOG-017-configurar-alembic-minimo.md`

23. [x] Criar validação de assets metodológicos mínima
    - Status: concluido
    - Task: `tasks/TASK-018-criar-validacao-assets-metodologicos-minima.md`
    - Log: `logs/LOG-018-criar-validacao-assets-metodologicos-minima.md`

24. [x] Auditar higiene de repositório e artefatos
    - Status: concluido
    - Task: `tasks/TASK-019-auditar-higiene-repositorio-e-artefatos.md`
    - Log: `logs/LOG-019-auditar-higiene-repositorio-e-artefatos.md`

25. [x] Ajustar gitignore mínimo
    - Status: concluido
    - Task: `tasks/TASK-020-ajustar-gitignore-minimo.md`
    - Log: `logs/LOG-020-ajustar-gitignore-minimo.md`

26. [x] Remover artefatos ignorados do índice Git
    - Status: concluido
    - Task: `tasks/TASK-020A-remover-artefatos-ignorados-do-indice-git.md`
    - Log: `logs/LOG-020A-remover-artefatos-ignorados-do-indice-git.md`

27. [x] Refinar AGENTS.md
    - Status: concluido
    - Task: `tasks/TASK-021-refinar-agents-md.md`
    - Log: `logs/LOG-021-refinar-agents-md.md`

28. [x] Descontinuar TODOLIST.md e alinhar ROADMAP
    - Status: concluido
    - Task: `tasks/TASK-021A-descontinuar-todolist-e-alinhar-roadmap.md`
    - Log: `logs/LOG-021A-descontinuar-todolist-e-alinhar-roadmap.md`

29. [x] Registrar descontinuidade do TODOLIST.md
    - Status: concluido
    - Task: `tasks/TASK-022-registrar-descontinuidade-todolist.md`
    - Log: `logs/LOG-022-registrar-descontinuidade-todolist.md`

30. [x] Criar ou refinar README do projeto
    - Status: concluido
    - Task: `tasks/TASK-023-criar-ou-refinar-readme-projeto.md`
    - Log: `logs/LOG-023-criar-ou-refinar-readme-projeto.md`

31. [x] Auditar dependências backend
    - Status: concluido
    - Task: `tasks/TASK-024-auditar-dependencias-backend.md`
    - Log: `logs/LOG-024-auditar-dependencias-backend.md`

32. [x] Configurar dependências backend mínimas
    - Status: concluido
    - Task: `tasks/TASK-025-configurar-dependencias-backend-minimas.md`
    - Log: `logs/LOG-025-configurar-dependencias-backend-minimas.md`

33. [x] Auditar dependências frontend
    - Status: concluido
    - Task: `tasks/TASK-026-auditar-dependencias-frontend.md`
    - Log: `logs/LOG-026-auditar-dependencias-frontend.md`

34. [x] Configurar dependências frontend mínimas
    - Status: concluido
    - Task: `tasks/TASK-027-configurar-dependencias-frontend-minimas.md`
    - Log: `logs/LOG-027-configurar-dependencias-frontend-minimas.md`

35. [x] Criar app FastAPI mínimo
    - Status: concluido
    - Task: `tasks/TASK-028-criar-app-fastapi-minimo.md`
    - Log: `logs/LOG-028-criar-app-fastapi-minimo.md`

36. [x] Criar shell frontend mínimo
    - Status: concluido
    - Task: `tasks/TASK-029-criar-shell-frontend-minimo.md`
    - Log: `logs/LOG-029-criar-shell-frontend-minimo.md`

37. [x] Auditar rastreabilidade TASKs e SPECs
    - Status: concluido
    - Task: `tasks/TASK-030-auditar-rastreabilidade-tasks-specs.md`
    - Log: `logs/LOG-030-auditar-rastreabilidade-tasks-specs.md`

38. [x] Criar matriz de execução das TASKs de fundação
    - Status: concluido
    - Task: `tasks/TASK-031-criar-matriz-execucao-tasks-fundacao.md`
    - Log: `logs/LOG-031-criar-matriz-execucao-tasks-fundacao.md`

39. [x] Auditar prontidão da fundação governada
    - Status: concluido
    - Task: `tasks/TASK-032-auditar-prontidao-fundacao-governada.md`
    - Log: `logs/LOG-032-auditar-prontidao-fundacao-governada.md`

40. [x] Atualizar ROADMAP após fundação
    - Status: concluido
    - Task: `tasks/TASK-033-atualizar-roadmap-pos-fundacao.md`
    - Log: `logs/LOG-033-atualizar-roadmap-pos-fundacao.md`

41. [x] Encerrar SPEC-001 e liberar próxima SPEC
    - Status: concluido
    - Task: `tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`
    - Log: `logs/LOG-034-encerrar-spec-001-e-liberar-proxima-spec.md`

42. [x] Estruturar assets da camada declarada
    - Status: concluido
    - Task: `tasks/TASK-035-estruturar-assets-camada-declarada.md`
    - Log: `logs/LOG-035-estruturar-assets-camada-declarada.md`

43. [x] Ajustar governança da identificação exata da ECD
    - Status: concluido
    - Task: `tasks/TASK-035A-ajustar-governanca-identificacao-exata-ecd.md`
    - Log: `logs/LOG-035A-ajustar-governanca-identificacao-exata-ecd.md`

44. [x] Implementar matcher metodológico declarado
    - Status: concluido
    - Task: `tasks/TASK-036-implementar-matcher-metodologico-declarado.md`
    - Log: `logs/LOG-036-implementar-matcher-metodologico-declarado.md`

45. [x] Modelar resultado por conta declarada
    - Status: concluido
    - Task: `tasks/TASK-037-modelar-resultado-conta-declarada.md`
    - Log: `logs/LOG-037-modelar-resultado-conta-declarada.md`

46. [x] Persistir snapshots da camada declarada
    - Status: concluido
    - Task: `tasks/TASK-038-persistir-snapshots-camada-declarada.md`
    - Log: `logs/LOG-038-persistir-snapshots-camada-declarada.md`

47. [x] Criar API da camada declarada
    - Status: concluido
    - Task: `tasks/TASK-039-criar-api-camada-declarada.md`
    - Log: `logs/LOG-039-criar-api-camada-declarada.md`

48. [x] Criar UI da camada declarada
    - Status: concluido
    - Task: `tasks/TASK-040-criar-ui-camada-declarada.md`
    - Log: `logs/LOG-040-criar-ui-camada-declarada.md`

49. [x] Exportação e testes da camada declarada
    - Status: concluido
    - Task: `tasks/TASK-041-exportacao-e-testes-camada-declarada.md`
    - Log: `logs/LOG-041-exportacao-e-testes-camada-declarada.md`

50. [x] Ajustar fluxo de homologacao por grupo
    - Status: concluido
    - Task: `tasks/TASK-041L-ajustar-fluxo-homologacao-por-grupo.md`
    - Log: `logs/LOG-041L-ajustar-fluxo-homologacao-por-grupo.md`

51. [x] Configurar Playwright E2E da camada declarada
    - Status: concluido
    - Task: `tasks/TASK-041K-configurar-playwright-e2e-camada-declarada.md`
    - Log: `logs/LOG-041K-configurar-playwright-e2e-camada-declarada.md`

52. [x] Modelar importacao ECD e status da analise
    - Status: concluido
    - Task: `tasks/TASK-041A-modelar-importacao-ecd-status-analise.md`
    - Log: `logs/LOG-041A-modelar-importacao-ecd-status-analise.md`

53. [x] Criar migrations da ECD normalizada
    - Status: concluido
    - Task: `tasks/TASK-041B-criar-migrations-ecd-normalizada.md`
    - Log: `logs/LOG-041B-criar-migrations-ecd-normalizada.md`

54. [x] Criar fixtures ECD governadas
    - Status: concluido
    - Task: `tasks/TASK-041C-criar-fixtures-ecd-governadas.md`
    - Log: `logs/LOG-041C-criar-fixtures-ecd-governadas.md`

55. [x] Implementar parser ECD declarado
    - Status: concluido
    - Task: `tasks/TASK-041D-implementar-parser-ecd-declarado.md`
    - Log: `logs/LOG-041D-implementar-parser-ecd-declarado.md`

56. [x] Persistir ECD normalizada
    - Status: concluido
    - Task: `tasks/TASK-041E-persistir-ecd-normalizada.md`
    - Log: `logs/LOG-041E-persistir-ecd-normalizada.md`

57. [x] Criar importacao ECD oficial
    - Status: concluido
    - Task: `tasks/TASK-041F-criar-importacao-ecd-oficial.md`
    - Log: `logs/LOG-041F-criar-importacao-ecd-oficial.md`

58. [x] Executar camada declarada da ECD importada
    - Status: concluido
    - Task: `tasks/TASK-041G-executar-camada-declarada-ecd-importada.md`
    - Log: `logs/LOG-041G-executar-camada-declarada-ecd-importada.md`

59. [x] Integrar UI com analise importada real
    - Status: concluido
    - Task: `tasks/TASK-041H-integrar-ui-analise-importada-real.md`
    - Log: `logs/LOG-041H-integrar-ui-analise-importada-real.md`

60. [x] Criar exportacao Excel acionavel por analise
    - Status: concluido
    - Task: `tasks/TASK-041I-criar-exportacao-excel-acionavel-analise.md`
    - Log: `logs/LOG-041I-criar-exportacao-excel-acionavel-analise.md`

61. [x] Validar fluxo end-to-end da camada declarada
    - Status: concluido
    - Task: `tasks/TASK-041J-validar-fluxo-end-to-end-declarada.md`
    - Log: `logs/LOG-041J-validar-fluxo-end-to-end-declarada.md`

62. [x] Gerenciar importacoes ECD existentes
    - Status: concluido
    - Task: `tasks/TASK-041M-gerenciar-importacoes-ecd-existentes.md`
    - Log: `logs/LOG-041M-gerenciar-importacoes-ecd-existentes.md`

63. [x] Refinar apresentacao da leitura declarada
    - Status: concluido
    - Task: `tasks/TASK-085-refinar-apresentacao-leitura-declarada.md`
    - Log: `logs/LOG-085-refinar-apresentacao-leitura-declarada.md`

64. [x] Ajustar governanca de homologacao
    - Status: concluido
    - Task: `tasks/TASK-085A-ajustar-governanca-homologacao.md`
    - Log: `logs/LOG-085A-ajustar-governanca-homologacao.md`

65. [x] Tabela oficial referencial obrigatoria
    - Status: concluido
    - Task: `tasks/TASK-086-tabela-oficial-referencial-obrigatoria.md`
    - Log: `logs/LOG-086-tabela-oficial-referencial-obrigatoria.md`

66. [x] Tratar contas sem vinculo referencial
    - Status: concluido
    - Task: `tasks/TASK-087-tratar-contas-sem-vinculo-referencial.md`
    - Log: `logs/LOG-087-tratar-contas-sem-vinculo-referencial.md`

67. [x] Modelar contrato de domínio CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-049-modelar-contrato-dominio-capag-e.md`
    - Log: `logs/LOG-049-modelar-contrato-dominio-capag-e.md`

68. [x] Implementar motor do contrato CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-050-implementar-motor-contrato-capag-e.md`
    - Log: `logs/LOG-050-implementar-motor-contrato-capag-e.md`

69. [x] Persistir assessment CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-051-persistir-assessment-capag-e.md`
    - Log: `logs/LOG-051-persistir-assessment-capag-e.md`

70. [x] Criar API CAPAG assessment
    - Status: concluido
    - Task: `tasks/TASK-052-criar-api-capag-assessment.md`
    - Log: `logs/LOG-052-criar-api-capag-assessment.md`

71. [x] Criar UI de resultado CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-053-criar-ui-resultado-capag-e.md`
    - Log: `logs/LOG-053-criar-ui-resultado-capag-e.md`

72. [x] Exportação e testes do contrato CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-054-exportacao-e-testes-contrato-capag-e.md`
    - Log: `logs/LOG-054-exportacao-e-testes-contrato-capag-e.md`

73. [ ] Planejar refinamentos visuais governados
    - Status: pendente
    - Task: `tasks/TASK-054A-planejar-refinamentos-visuais.md`
    - Log: `logs/LOG-054A-planejar-refinamentos-visuais.md`

74. [x] Pesquisar fonte oficial do plano referencial
    - Status: concluido
    - Task: `tasks/TASK-088-pesquisar-fonte-oficial-plano-referencial.md`
    - Log: `logs/LOG-088-pesquisar-fonte-oficial-plano-referencial.md`

75. [x] Definir contrato de carga do plano referencial
    - Status: concluido
    - Task: `tasks/TASK-089-definir-contrato-carga-plano-referencial.md`
    - Log: `logs/LOG-089-definir-contrato-carga-plano-referencial.md`

76. [x] Ampliar validacoes do asset referencial
    - Status: concluido
    - Task: `tasks/TASK-090-ampliar-validacoes-asset-plano-referencial.md`
    - Log: `logs/LOG-090-ampliar-validacoes-asset-plano-referencial.md`

77. [x] Preparar asset completo do plano referencial
    - Status: concluido
    - Task: `tasks/TASK-091-preparar-asset-completo-plano-referencial.md`
    - Log: `logs/LOG-091-preparar-asset-completo-plano-referencial.md`

78. [ ] Desenhar persistencia e versionamento do plano referencial
    - Status: pendente
    - Task: `tasks/TASK-092-desenhar-persistencia-versionamento-plano-referencial.md`
    - Log: `logs/LOG-092-desenhar-persistencia-versionamento-plano-referencial.md`

79. [ ] Desenhar CRUD controlado do plano referencial
    - Status: pendente
    - Task: `tasks/TASK-093-desenhar-crud-controlado-plano-referencial.md`
    - Log: `logs/LOG-093-desenhar-crud-controlado-plano-referencial.md`

80. [x] Ampliar parser do balanco declarado
    - Status: concluido
    - Task: `tasks/TASK-101-ampliar-parser-balanco-declarado.md`
    - Log: `logs/LOG-101-ampliar-parser-balanco-declarado.md`

81. [x] Persistir ECD e balanco declarado
    - Status: concluido
    - Task: `tasks/TASK-102-persistir-ecd-balanco-declarado.md`
    - Log: `logs/LOG-102-persistir-ecd-balanco-declarado.md`

82. [x] Reprocessar importacoes ECD legadas
    - Status: concluido
    - Task: `tasks/TASK-103-reprocessar-importacoes-ecd-legadas.md`
    - Log: `logs/LOG-103-reprocessar-importacoes-ecd-legadas.md`

83. [x] Implementar conciliacao do balanco declarado
    - Status: concluido
    - Task: `tasks/TASK-104-implementar-conciliacao-balanco-declarado.md`
    - Log: `logs/LOG-104-implementar-conciliacao-balanco-declarado.md`

84. [x] Criar API do balanco declarado
    - Status: concluido
    - Task: `tasks/TASK-105-criar-api-balanco-declarado.md`
    - Log: `logs/LOG-105-criar-api-balanco-declarado.md`

85. [x] Criar UI do balanco declarado
    - Status: concluido
    - Task: `tasks/TASK-106-criar-ui-balanco-declarado.md`
    - Log: `logs/LOG-106-criar-ui-balanco-declarado.md`

86. [x] Integrar validade do balanco ao PLRA e CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-107-integrar-validade-balanco-plra-capag.md`
    - Log: `logs/LOG-107-integrar-validade-balanco-plra-capag.md`

87. [x] Validar fluxo do balanco declarado
    - Status: concluido
    - Task: `tasks/TASK-108-validar-fluxo-balanco-declarado.md`
    - Log: `logs/LOG-108-validar-fluxo-balanco-declarado.md`

88. [x] Estruturar metodologia PLRA
    - Status: concluido
    - Task: `tasks/TASK-094-estruturar-metodologia-plra.md`
    - Log: `logs/LOG-094-estruturar-metodologia-plra.md`

89. [x] Implementar motor PLRA
    - Status: concluido
    - Task: `tasks/TASK-095-implementar-motor-plra.md`
    - Log: `logs/LOG-095-implementar-motor-plra.md`

90. [x] Persistir snapshots PLRA
    - Status: concluido
    - Task: `tasks/TASK-096-persistir-snapshots-plra.md`
    - Log: `logs/LOG-096-persistir-snapshots-plra.md`

91. [x] Criar API e integracao PLRA CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-097-criar-api-integracao-plra-capag-e.md`
    - Log: `logs/LOG-097-criar-api-integracao-plra-capag-e.md`

92. [x] Criar UI PLRA
    - Status: concluido
    - Task: `tasks/TASK-098-criar-ui-plra.md`
    - Log: `logs/LOG-098-criar-ui-plra.md`

93. [x] Exportacao e testes PLRA
    - Status: concluido
    - Task: `tasks/TASK-099-exportacao-testes-plra.md`
    - Log: `logs/LOG-099-exportacao-testes-plra.md`

94. [ ] Consolidar dashboard de calculos da analise
    - Status: pendente
    - Task: `tasks/TASK-100-consolidar-dashboard-calculos-analise.md`
    - Log: `logs/LOG-100-consolidar-dashboard-calculos-analise.md`

95. [ ] Normalização e razão comportamental
    - Status: pendente
    - Task: `tasks/TASK-042-normalizacao-razao-comportamental.md`
    - Log: `logs/LOG-042-normalizacao-razao-comportamental.md`

96. [ ] Gerar perfil comportamental por conta
    - Status: pendente
    - Task: `tasks/TASK-043-gerar-perfil-comportamental-conta.md`
    - Log: `logs/LOG-043-gerar-perfil-comportamental-conta.md`

97. [ ] Classificação, score e salvaguardas reclassificadas
    - Status: pendente
    - Task: `tasks/TASK-044-classificacao-score-salvaguardas-reclassificada.md`
    - Log: `logs/LOG-044-classificacao-score-salvaguardas-reclassificada.md`

98. [ ] Cenário reclassificado e revisão humana
    - Status: pendente
    - Task: `tasks/TASK-045-cenario-reclassificado-revisao-humana.md`
    - Log: `logs/LOG-045-cenario-reclassificado-revisao-humana.md`

99. [ ] Criar API da camada reclassificada
    - Status: pendente
    - Task: `tasks/TASK-046-criar-api-camada-reclassificada.md`
    - Log: `logs/LOG-046-criar-api-camada-reclassificada.md`

100. [ ] Criar UI de revisão reclassificada
    - Status: pendente
    - Task: `tasks/TASK-047-criar-ui-revisao-reclassificada.md`
    - Log: `logs/LOG-047-criar-ui-revisao-reclassificada.md`

101. [ ] Exportação e testes da camada reclassificada
    - Status: pendente
    - Task: `tasks/TASK-048-exportacao-e-testes-reclassificada.md`
    - Log: `logs/LOG-048-exportacao-e-testes-reclassificada.md`

102. [x] Modelar evidências e materialidade
    - Status: concluido
    - Task: `tasks/TASK-055-modelar-evidencias-materialidade.md`
    - Log: `logs/LOG-055-modelar-evidencias-materialidade.md`

103. [x] Modelar avaliação de ativos
    - Status: concluido
    - Task: `tasks/TASK-056-modelar-avaliacao-ativos.md`
    - Log: `logs/LOG-056-modelar-avaliacao-ativos.md`

104. [x] Persistir e integrar bloqueios de evidências
    - Status: concluido
    - Task: `tasks/TASK-057-persistir-e-integrar-bloqueios-evidencias.md`
    - Log: `logs/LOG-057-persistir-e-integrar-bloqueios-evidencias.md`

105. [x] Criar API de evidências e ativos
    - Status: concluido
    - Task: `tasks/TASK-058-criar-api-evidencias-ativos.md`
    - Log: `logs/LOG-058-criar-api-evidencias-ativos.md`

106. [x] Criar UI de evidências e ativos
    - Status: concluido
    - Task: `tasks/TASK-059-criar-ui-evidencias-ativos.md`
    - Log: `logs/LOG-059-criar-ui-evidencias-ativos.md`

107. [x] Exportação e testes de evidências e ativos
    - Status: concluido
    - Task: `tasks/TASK-060-exportacao-e-testes-evidencias-ativos.md`
    - Log: `logs/LOG-060-exportacao-e-testes-evidencias-ativos.md`

108. [x] Estruturar metodologia DFC e disponibilidades
    - Status: concluido
    - Task: `tasks/TASK-061-estruturar-metodologia-dfc-disponibilidades.md`
    - Log: `logs/LOG-061-estruturar-metodologia-dfc-disponibilidades.md`

109. [x] Implementar motor DFC direta
    - Status: concluido
    - Task: `tasks/TASK-062-implementar-motor-dfc-direta.md`
    - Log: `logs/LOG-062-implementar-motor-dfc-direta.md`

110. [x] Calcular FCA, pendências e evidências
    - Status: concluido
    - Task: `tasks/TASK-063-calcular-fca-pendencias-evidencias.md`
    - Log: `logs/LOG-063-calcular-fca-pendencias-evidencias.md`

111. [x] Criar API DFC/FCA
    - Status: concluido
    - Task: `tasks/TASK-064-criar-api-dfc-fca.md`
    - Log: `logs/LOG-064-criar-api-dfc-fca.md`

112. [x] Criar UI DFC/FCA
    - Status: concluido
    - Task: `tasks/TASK-065-criar-ui-dfc-fca.md`
    - Log: `logs/LOG-065-criar-ui-dfc-fca.md`

113. [x] Exportação e testes DFC/FCA
    - Status: concluido
    - Task: `tasks/TASK-066-exportacao-e-testes-dfc-fca.md`
    - Log: `logs/LOG-066-exportacao-e-testes-dfc-fca.md`

114. [x] Estruturar assets ROA
    - Status: concluido
    - Task: `tasks/TASK-067-estruturar-assets-roa.md`
    - Log: `logs/LOG-067-estruturar-assets-roa.md`

115. [x] Implementar motor ROA
    - Status: concluido
    - Task: `tasks/TASK-068-implementar-motor-roa.md`
    - Log: `logs/LOG-068-implementar-motor-roa.md`

116. [x] Integrar pressões e evidências ROA
    - Status: concluido
    - Task: `tasks/TASK-069-integrar-pressoes-evidencias-roa.md`
    - Log: `logs/LOG-069-integrar-pressoes-evidencias-roa.md`

117. [x] Integrar ROA + PLRA ao CAPAG-E
    - Status: concluido
    - Task: `tasks/TASK-070-integrar-roa-plra-capag-e.md`
    - Log: `logs/LOG-070-integrar-roa-plra-capag-e.md`

118. [x] Criar API e UI ROA
    - Status: concluido
    - Task: `tasks/TASK-071-criar-api-ui-roa.md`
    - Log: `logs/LOG-071-criar-api-ui-roa.md`

119. [x] Exportação e testes ROA + PLRA
    - Status: concluido
    - Task: `tasks/TASK-072-exportacao-e-testes-roa-plra.md`
    - Log: `logs/LOG-072-exportacao-e-testes-roa-plra.md`

120. [ ] Modelar domínio do laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-073-modelar-dominio-laudo-capag-e.md`
    - Log: `logs/LOG-073-modelar-dominio-laudo-capag-e.md`

121. [ ] Validar status do laudo
    - Status: pendente
    - Task: `tasks/TASK-074-validar-status-laudo.md`
    - Log: `logs/LOG-074-validar-status-laudo.md`

122. [ ] Gerar Excel de laudo estruturado
    - Status: pendente
    - Task: `tasks/TASK-075-gerar-excel-laudo-estruturado.md`
    - Log: `logs/LOG-075-gerar-excel-laudo-estruturado.md`

123. [ ] Criar API de laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-076-criar-api-laudo-capag-e.md`
    - Log: `logs/LOG-076-criar-api-laudo-capag-e.md`

124. [ ] Criar UI de laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-077-criar-ui-laudo-capag-e.md`
    - Log: `logs/LOG-077-criar-ui-laudo-capag-e.md`

125. [ ] Testes do laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-078-testes-laudo-capag-e.md`
    - Log: `logs/LOG-078-testes-laudo-capag-e.md`

126. [ ] Criar matriz de rastreabilidade metodológica
    - Status: pendente
    - Task: `tasks/TASK-079-criar-matriz-rastreabilidade-metodologica.md`
    - Log: `logs/LOG-079-criar-matriz-rastreabilidade-metodologica.md`

127. [ ] Modelar MethodologyVersion e assets governados
    - Status: pendente
    - Task: `tasks/TASK-080-modelar-methodology-version-assets.md`
    - Log: `logs/LOG-080-modelar-methodology-version-assets.md`

128. [ ] Validações e cobertura metodológica
    - Status: pendente
    - Task: `tasks/TASK-081-validacoes-cobertura-metodologica.md`
    - Log: `logs/LOG-081-validacoes-cobertura-metodologica.md`

129. [ ] Criar changelog metodológico
    - Status: pendente
    - Task: `tasks/TASK-082-criar-changelog-metodologico.md`
    - Log: `logs/LOG-082-criar-changelog-metodologico.md`

130. [ ] Criar UI de governança metodológica
    - Status: pendente
    - Task: `tasks/TASK-083-criar-ui-governanca-metodologica.md`
    - Log: `logs/LOG-083-criar-ui-governanca-metodologica.md`

131. [ ] Testes de governança e documentos operacionais finais
    - Status: pendente
    - Task: `tasks/TASK-084-testes-governanca-e-documentos-operacionais-finais.md`
    - Log: `logs/LOG-084-testes-governanca-e-documentos-operacionais-finais.md`
