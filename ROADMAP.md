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

ID: TASK-014
Título: Configurar testes backend mínimos
Status: aguardando_homologacao
Task: `tasks/TASK-014-configurar-testes-backend-minimos.md`
Log: `logs/LOG-014-configurar-testes-backend-minimos.md`

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

17. [ ] Configurar testes backend mínimos
    - Status: aguardando_homologacao
    - Task: `tasks/TASK-014-configurar-testes-backend-minimos.md`
    - Log: `logs/LOG-014-configurar-testes-backend-minimos.md`

18. [ ] Configurar testes frontend mínimos
    - Status: pendente
    - Task: `tasks/TASK-015-configurar-testes-frontend-minimos.md`
    - Log: `logs/LOG-015-configurar-testes-frontend-minimos.md`

19. [ ] Configurar CI mínimo
    - Status: pendente
    - Task: `tasks/TASK-016-configurar-ci-minimo.md`
    - Log: `logs/LOG-016-configurar-ci-minimo.md`

20. [ ] Configurar Alembic mínimo
    - Status: pendente
    - Task: `tasks/TASK-017-configurar-alembic-minimo.md`
    - Log: `logs/LOG-017-configurar-alembic-minimo.md`

21. [ ] Criar validação de assets metodológicos mínima
    - Status: pendente
    - Task: `tasks/TASK-018-criar-validacao-assets-metodologicos-minima.md`
    - Log: `logs/LOG-018-criar-validacao-assets-metodologicos-minima.md`

22. [ ] Auditar higiene de repositório e artefatos
    - Status: pendente
    - Task: `tasks/TASK-019-auditar-higiene-repositorio-e-artefatos.md`
    - Log: `logs/LOG-019-auditar-higiene-repositorio-e-artefatos.md`

23. [ ] Ajustar gitignore mínimo
    - Status: pendente
    - Task: `tasks/TASK-020-ajustar-gitignore-minimo.md`
    - Log: `logs/LOG-020-ajustar-gitignore-minimo.md`

24. [ ] Refinar AGENTS.md
    - Status: pendente
    - Task: `tasks/TASK-021-refinar-agents-md.md`
    - Log: `logs/LOG-021-refinar-agents-md.md`

25. [ ] Refinar TODOLIST.md
    - Status: pendente
    - Task: `tasks/TASK-022-refinar-todolist.md`
    - Log: `logs/LOG-022-refinar-todolist.md`

26. [ ] Criar ou refinar README do projeto
    - Status: pendente
    - Task: `tasks/TASK-023-criar-ou-refinar-readme-projeto.md`
    - Log: `logs/LOG-023-criar-ou-refinar-readme-projeto.md`

27. [ ] Auditar dependências backend
    - Status: pendente
    - Task: `tasks/TASK-024-auditar-dependencias-backend.md`
    - Log: `logs/LOG-024-auditar-dependencias-backend.md`

28. [ ] Configurar dependências backend mínimas
    - Status: pendente
    - Task: `tasks/TASK-025-configurar-dependencias-backend-minimas.md`
    - Log: `logs/LOG-025-configurar-dependencias-backend-minimas.md`

29. [ ] Auditar dependências frontend
    - Status: pendente
    - Task: `tasks/TASK-026-auditar-dependencias-frontend.md`
    - Log: `logs/LOG-026-auditar-dependencias-frontend.md`

30. [ ] Configurar dependências frontend mínimas
    - Status: pendente
    - Task: `tasks/TASK-027-configurar-dependencias-frontend-minimas.md`
    - Log: `logs/LOG-027-configurar-dependencias-frontend-minimas.md`

31. [ ] Criar app FastAPI mínimo
    - Status: pendente
    - Task: `tasks/TASK-028-criar-app-fastapi-minimo.md`
    - Log: `logs/LOG-028-criar-app-fastapi-minimo.md`

32. [ ] Criar shell frontend mínimo
    - Status: pendente
    - Task: `tasks/TASK-029-criar-shell-frontend-minimo.md`
    - Log: `logs/LOG-029-criar-shell-frontend-minimo.md`

33. [ ] Auditar rastreabilidade TASKs e SPECs
    - Status: pendente
    - Task: `tasks/TASK-030-auditar-rastreabilidade-tasks-specs.md`
    - Log: `logs/LOG-030-auditar-rastreabilidade-tasks-specs.md`

34. [ ] Criar matriz de execução das TASKs de fundação
    - Status: pendente
    - Task: `tasks/TASK-031-criar-matriz-execucao-tasks-fundacao.md`
    - Log: `logs/LOG-031-criar-matriz-execucao-tasks-fundacao.md`

35. [ ] Auditar prontidão da fundação governada
    - Status: pendente
    - Task: `tasks/TASK-032-auditar-prontidao-fundacao-governada.md`
    - Log: `logs/LOG-032-auditar-prontidao-fundacao-governada.md`

36. [ ] Atualizar status do TODOLIST após fundação
    - Status: pendente
    - Task: `tasks/TASK-033-atualizar-status-todolist-pos-fundacao.md`
    - Log: `logs/LOG-033-atualizar-status-todolist-pos-fundacao.md`

37. [ ] Encerrar SPEC-001 e liberar próxima SPEC
    - Status: pendente
    - Task: `tasks/TASK-034-encerrar-spec-001-e-liberar-proxima-spec.md`
    - Log: `logs/LOG-034-encerrar-spec-001-e-liberar-proxima-spec.md`

38. [ ] Estruturar assets da camada declarada
    - Status: pendente
    - Task: `tasks/TASK-035-estruturar-assets-camada-declarada.md`
    - Log: `logs/LOG-035-estruturar-assets-camada-declarada.md`

39. [ ] Implementar matcher metodológico declarado
    - Status: pendente
    - Task: `tasks/TASK-036-implementar-matcher-metodologico-declarado.md`
    - Log: `logs/LOG-036-implementar-matcher-metodologico-declarado.md`

40. [ ] Modelar resultado por conta declarada
    - Status: pendente
    - Task: `tasks/TASK-037-modelar-resultado-conta-declarada.md`
    - Log: `logs/LOG-037-modelar-resultado-conta-declarada.md`

41. [ ] Persistir snapshots da camada declarada
    - Status: pendente
    - Task: `tasks/TASK-038-persistir-snapshots-camada-declarada.md`
    - Log: `logs/LOG-038-persistir-snapshots-camada-declarada.md`

42. [ ] Criar API da camada declarada
    - Status: pendente
    - Task: `tasks/TASK-039-criar-api-camada-declarada.md`
    - Log: `logs/LOG-039-criar-api-camada-declarada.md`

43. [ ] Criar UI da camada declarada
    - Status: pendente
    - Task: `tasks/TASK-040-criar-ui-camada-declarada.md`
    - Log: `logs/LOG-040-criar-ui-camada-declarada.md`

44. [ ] Exportação e testes da camada declarada
    - Status: pendente
    - Task: `tasks/TASK-041-exportacao-e-testes-camada-declarada.md`
    - Log: `logs/LOG-041-exportacao-e-testes-camada-declarada.md`

45. [ ] Normalização e razão comportamental
    - Status: pendente
    - Task: `tasks/TASK-042-normalizacao-razao-comportamental.md`
    - Log: `logs/LOG-042-normalizacao-razao-comportamental.md`

46. [ ] Gerar perfil comportamental por conta
    - Status: pendente
    - Task: `tasks/TASK-043-gerar-perfil-comportamental-conta.md`
    - Log: `logs/LOG-043-gerar-perfil-comportamental-conta.md`

47. [ ] Classificação, score e salvaguardas reclassificadas
    - Status: pendente
    - Task: `tasks/TASK-044-classificacao-score-salvaguardas-reclassificada.md`
    - Log: `logs/LOG-044-classificacao-score-salvaguardas-reclassificada.md`

48. [ ] Cenário reclassificado e revisão humana
    - Status: pendente
    - Task: `tasks/TASK-045-cenario-reclassificado-revisao-humana.md`
    - Log: `logs/LOG-045-cenario-reclassificado-revisao-humana.md`

49. [ ] Criar API da camada reclassificada
    - Status: pendente
    - Task: `tasks/TASK-046-criar-api-camada-reclassificada.md`
    - Log: `logs/LOG-046-criar-api-camada-reclassificada.md`

50. [ ] Criar UI de revisão reclassificada
    - Status: pendente
    - Task: `tasks/TASK-047-criar-ui-revisao-reclassificada.md`
    - Log: `logs/LOG-047-criar-ui-revisao-reclassificada.md`

51. [ ] Exportação e testes da camada reclassificada
    - Status: pendente
    - Task: `tasks/TASK-048-exportacao-e-testes-reclassificada.md`
    - Log: `logs/LOG-048-exportacao-e-testes-reclassificada.md`

52. [ ] Modelar contrato de domínio CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-049-modelar-contrato-dominio-capag-e.md`
    - Log: `logs/LOG-049-modelar-contrato-dominio-capag-e.md`

53. [ ] Implementar motor do contrato CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-050-implementar-motor-contrato-capag-e.md`
    - Log: `logs/LOG-050-implementar-motor-contrato-capag-e.md`

54. [ ] Persistir assessment CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-051-persistir-assessment-capag-e.md`
    - Log: `logs/LOG-051-persistir-assessment-capag-e.md`

55. [ ] Criar API CAPAG assessment
    - Status: pendente
    - Task: `tasks/TASK-052-criar-api-capag-assessment.md`
    - Log: `logs/LOG-052-criar-api-capag-assessment.md`

56. [ ] Criar UI de resultado CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-053-criar-ui-resultado-capag-e.md`
    - Log: `logs/LOG-053-criar-ui-resultado-capag-e.md`

57. [ ] Exportação e testes do contrato CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-054-exportacao-e-testes-contrato-capag-e.md`
    - Log: `logs/LOG-054-exportacao-e-testes-contrato-capag-e.md`

58. [ ] Modelar evidências e materialidade
    - Status: pendente
    - Task: `tasks/TASK-055-modelar-evidencias-materialidade.md`
    - Log: `logs/LOG-055-modelar-evidencias-materialidade.md`

59. [ ] Modelar avaliação de ativos
    - Status: pendente
    - Task: `tasks/TASK-056-modelar-avaliacao-ativos.md`
    - Log: `logs/LOG-056-modelar-avaliacao-ativos.md`

60. [ ] Persistir e integrar bloqueios de evidências
    - Status: pendente
    - Task: `tasks/TASK-057-persistir-e-integrar-bloqueios-evidencias.md`
    - Log: `logs/LOG-057-persistir-e-integrar-bloqueios-evidencias.md`

61. [ ] Criar API de evidências e ativos
    - Status: pendente
    - Task: `tasks/TASK-058-criar-api-evidencias-ativos.md`
    - Log: `logs/LOG-058-criar-api-evidencias-ativos.md`

62. [ ] Criar UI de evidências e ativos
    - Status: pendente
    - Task: `tasks/TASK-059-criar-ui-evidencias-ativos.md`
    - Log: `logs/LOG-059-criar-ui-evidencias-ativos.md`

63. [ ] Exportação e testes de evidências e ativos
    - Status: pendente
    - Task: `tasks/TASK-060-exportacao-e-testes-evidencias-ativos.md`
    - Log: `logs/LOG-060-exportacao-e-testes-evidencias-ativos.md`

64. [ ] Estruturar metodologia DFC e disponibilidades
    - Status: pendente
    - Task: `tasks/TASK-061-estruturar-metodologia-dfc-disponibilidades.md`
    - Log: `logs/LOG-061-estruturar-metodologia-dfc-disponibilidades.md`

65. [ ] Implementar motor DFC direta
    - Status: pendente
    - Task: `tasks/TASK-062-implementar-motor-dfc-direta.md`
    - Log: `logs/LOG-062-implementar-motor-dfc-direta.md`

66. [ ] Calcular FCA, pendências e evidências
    - Status: pendente
    - Task: `tasks/TASK-063-calcular-fca-pendencias-evidencias.md`
    - Log: `logs/LOG-063-calcular-fca-pendencias-evidencias.md`

67. [ ] Criar API DFC/FCA
    - Status: pendente
    - Task: `tasks/TASK-064-criar-api-dfc-fca.md`
    - Log: `logs/LOG-064-criar-api-dfc-fca.md`

68. [ ] Criar UI DFC/FCA
    - Status: pendente
    - Task: `tasks/TASK-065-criar-ui-dfc-fca.md`
    - Log: `logs/LOG-065-criar-ui-dfc-fca.md`

69. [ ] Exportação e testes DFC/FCA
    - Status: pendente
    - Task: `tasks/TASK-066-exportacao-e-testes-dfc-fca.md`
    - Log: `logs/LOG-066-exportacao-e-testes-dfc-fca.md`

70. [ ] Estruturar assets ROA
    - Status: pendente
    - Task: `tasks/TASK-067-estruturar-assets-roa.md`
    - Log: `logs/LOG-067-estruturar-assets-roa.md`

71. [ ] Implementar motor ROA
    - Status: pendente
    - Task: `tasks/TASK-068-implementar-motor-roa.md`
    - Log: `logs/LOG-068-implementar-motor-roa.md`

72. [ ] Integrar pressões e evidências ROA
    - Status: pendente
    - Task: `tasks/TASK-069-integrar-pressoes-evidencias-roa.md`
    - Log: `logs/LOG-069-integrar-pressoes-evidencias-roa.md`

73. [ ] Integrar ROA + PLRA ao CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-070-integrar-roa-plra-capag-e.md`
    - Log: `logs/LOG-070-integrar-roa-plra-capag-e.md`

74. [ ] Criar API e UI ROA
    - Status: pendente
    - Task: `tasks/TASK-071-criar-api-ui-roa.md`
    - Log: `logs/LOG-071-criar-api-ui-roa.md`

75. [ ] Exportação e testes ROA + PLRA
    - Status: pendente
    - Task: `tasks/TASK-072-exportacao-e-testes-roa-plra.md`
    - Log: `logs/LOG-072-exportacao-e-testes-roa-plra.md`

76. [ ] Modelar domínio do laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-073-modelar-dominio-laudo-capag-e.md`
    - Log: `logs/LOG-073-modelar-dominio-laudo-capag-e.md`

77. [ ] Validar status do laudo
    - Status: pendente
    - Task: `tasks/TASK-074-validar-status-laudo.md`
    - Log: `logs/LOG-074-validar-status-laudo.md`

78. [ ] Gerar Excel de laudo estruturado
    - Status: pendente
    - Task: `tasks/TASK-075-gerar-excel-laudo-estruturado.md`
    - Log: `logs/LOG-075-gerar-excel-laudo-estruturado.md`

79. [ ] Criar API de laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-076-criar-api-laudo-capag-e.md`
    - Log: `logs/LOG-076-criar-api-laudo-capag-e.md`

80. [ ] Criar UI de laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-077-criar-ui-laudo-capag-e.md`
    - Log: `logs/LOG-077-criar-ui-laudo-capag-e.md`

81. [ ] Testes do laudo CAPAG-E
    - Status: pendente
    - Task: `tasks/TASK-078-testes-laudo-capag-e.md`
    - Log: `logs/LOG-078-testes-laudo-capag-e.md`

82. [ ] Criar matriz de rastreabilidade metodológica
    - Status: pendente
    - Task: `tasks/TASK-079-criar-matriz-rastreabilidade-metodologica.md`
    - Log: `logs/LOG-079-criar-matriz-rastreabilidade-metodologica.md`

83. [ ] Modelar MethodologyVersion e assets governados
    - Status: pendente
    - Task: `tasks/TASK-080-modelar-methodology-version-assets.md`
    - Log: `logs/LOG-080-modelar-methodology-version-assets.md`

84. [ ] Validações e cobertura metodológica
    - Status: pendente
    - Task: `tasks/TASK-081-validacoes-cobertura-metodologica.md`
    - Log: `logs/LOG-081-validacoes-cobertura-metodologica.md`

85. [ ] Criar changelog metodológico
    - Status: pendente
    - Task: `tasks/TASK-082-criar-changelog-metodologico.md`
    - Log: `logs/LOG-082-criar-changelog-metodologico.md`

86. [ ] Criar UI de governança metodológica
    - Status: pendente
    - Task: `tasks/TASK-083-criar-ui-governanca-metodologica.md`
    - Log: `logs/LOG-083-criar-ui-governanca-metodologica.md`

87. [ ] Testes de governança e documentos operacionais finais
    - Status: pendente
    - Task: `tasks/TASK-084-testes-governanca-e-documentos-operacionais-finais.md`
    - Log: `logs/LOG-084-testes-governanca-e-documentos-operacionais-finais.md`
