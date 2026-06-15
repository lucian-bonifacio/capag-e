---
name: prd
description: Documento de requisitos de produto que define problema, objetivos, usuários, escopo, requisitos, critérios de sucesso e restrições.
---

# PRD - CAPAG

## Controle Documental

| Campo | Valor |
| --- | --- |
| status | DRAFT |
| document_type | PRD |
| created_at | 2026-06-13 |
| updated_at | 2026-06-14 |
| approved_at | null |
| version | 0 |
| revision | 5 |

## 1. Contexto

O `capag` é uma aplicação interna para importar arquivos `ECD`, estruturar dados contábeis, calcular indicadores prudenciais, apoiar análise CAPAG-E e exportar a análise final em `Excel`.

O produto já existe parcialmente e passou por evolução em várias frentes: backend, motor de cálculo, frontend, interface legada, specs, referências metodológicas, tasks, documentos operacionais e skills. O planejamento em `tmp_deu_a_louca/` e os documentos em `docs/reference/` indicam que o próximo passo não é apenas adicionar novas telas ou cálculos, mas consolidar uma visão ampla e governada do produto.

A direção de produto deste PRD é transformar o CAPAG em uma ferramenta interna capaz de produzir, para um único usuário, três entregas conectadas:

1. análise interna auditável;
2. planilha `Excel` final com os resultados e trilhas relevantes;
3. laudo CAPAG-E estruturado, sem recalcular motores.

Este PRD usa como referências os materiais existentes em `docs/reference/` e `tmp_deu_a_louca/`. Não há referências externas adicionais informadas pelo usuário.

## 2. Problema

O CAPAG precisa evoluir de uma automação de leitura e cálculo para uma ferramenta de análise prudencial auditável. O problema central é que a análise CAPAG-E depende de várias camadas que hoje precisam ser melhor separadas, governadas e rastreadas:

- o que a `ECD` declara;
- como o sistema interpreta o `COD_CTA_REF` declarado;
- quando a metodologia interna usa regras amplas demais ou insuficientes;
- quando o comportamento contábil sugere leitura diferente da declarada;
- quais evidências, justificativas e ressalvas sustentam ajustes;
- qual método CAPAG-E está sendo usado;
- se o resultado é final, parcial, bloqueado ou apenas diagnóstico;
- como a análise vira `Excel` e laudo sem perda de rastreabilidade.

Sem uma visão de produto consolidada, novas implementações tendem a reforçar desalinhamentos entre documentação, metodologia, assets, código, testes, exportação e laudo.

## 3. Objetivos

- Consolidar o CAPAG como ferramenta interna de análise CAPAG-E auditável para um único usuário.
- Preservar a leitura declarada da `ECD` como uma camada explícita e rastreável.
- Criar uma segunda leitura reclassificada/comportamental sem substituir silenciosamente a camada declarada.
- Definir uma linguagem canônica para `PLRA`, `FCA`, `ROA` e `CAPAG-E`.
- Estruturar evidências, justificativas, materialidade, bloqueios e ressalvas.
- Evoluir o `FCO` atual para uma DFC direta completa capaz de apurar `FCA`.
- Implementar o caminho alternativo `CAPAG-E = ROA + PLRA`.
- Gerar laudo CAPAG-E e exportação `Excel` a partir de resultados já calculados.
- Manter governança metodológica entre documentos, manuais, specs, assets, testes, código e laudo.
- Organizar a evolução em módulos sequenciais, pequenos, verificáveis e aprováveis.

## 4. Não Objetivos

- Não transformar o CAPAG em produto SaaS, plataforma multiusuário ou sistema comercial neste ciclo de visão.
- Não eliminar a necessidade de julgamento técnico do usuário em casos materiais, ambíguos ou sensíveis.
- Não automatizar decisões prudenciais com IA generativa como núcleo decisório.
- Não buscar velocidade de implementação à custa de rastreabilidade, evidência ou governança.
- Não substituir a `ECD` como fonte declaratória.
- Não produzir laudo que esconda limitações, pendências, ressalvas ou bloqueios.
- Não reduzir a análise CAPAG-E a uma classificação por nome de conta ou palavra-chave.

## 5. Usuários e Personas

### Usuário Único

O produto será usado por uma única pessoa, que concentra todas as funções operacionais e analíticas.

Esse usuário precisa:

- importar arquivos `ECD`;
- conferir empresa, exercício, estrutura, saldos, movimentos e registros relevantes;
- entender a leitura declarada da escrituração;
- revisar divergências entre classificação declarada e comportamento observado;
- avaliar scores, evidências, justificativas, bloqueios e ressalvas;
- decidir quando manter, revisar ou aceitar reclassificações;
- escolher ou validar o método CAPAG-E aplicável;
- gerar análise interna auditável;
- exportar planilha `Excel` final;
- produzir laudo CAPAG-E estruturado.

Como o mesmo usuário executa, revisa e emite a análise, o produto deve favorecer clareza, rastreabilidade e segurança operacional acima de fluxos de aprovação multiusuário.

## 6. Escopo Funcional

### Módulo 0 - Organização, Arquitetura e Design

Criar a base de governança do produto antes de mudanças funcionais amplas. O módulo deve alinhar fonte de verdade, arquitetura-alvo, organização de specs, rotas do frontend, organização visual, estratégia de testes, higiene de repositório, decisão sobre banco de dados e persistência, documentos operacionais e skills.

### Módulo 1 - Camada Declarada

Organizar a leitura declarada baseada na `ECD`, especialmente registros `I050`, `I051`, `I155`, `I200`, `I250` e `J100`. O sistema deve preservar o `COD_CTA_REF` informado no `I051`, separar plano referencial oficial de metodologia interna e impedir classificações inseguras por prefixo amplo.

### Módulo 2 - CAPAG Reclassificada

Criar uma segunda leitura paralela, baseada no comportamento da conta. Essa camada deve considerar nome, hierarquia, saldos, débitos, créditos, contrapartidas, históricos, recorrência, materialidade e precedentes permitidos. O resultado deve indicar score, confiança, evidências, justificativas e recomendação.

### Módulo 3 - Contrato CAPAG-E, PLRA, FCA e ROA

Definir a linguagem canônica de resultado. `PLR ajustado` deve ser tratado como `PLRA` para fins de laudo. `FCO` não deve ser confundido com `FCA` completo. Todo resultado deve carregar valor, status, fórmula, método, limitações e bloqueios.

### Módulo 4 - Evidências, Justificativas e Avaliação de Ativos

Estruturar a camada que torna o cálculo defensável documentalmente. O produto deve vincular ajuste, justificativa, evidência esperada, materialidade, bloqueio, ressalva e impacto no laudo, incluindo tratamento específico para ativos relevantes e liquidação forçada.

### Módulo 5 - DFC Direta Completa e FCA

Evoluir o `FCO` atual para uma DFC direta completa. O sistema deve separar fluxos operacionais, de investimento e de financiamento, apurar `FCA`, registrar pendências de classificação e auditar lançamentos.

### Módulo 6 - Motor ROA + PLRA

Implementar o caminho alternativo `CAPAG-E = ROA + PLRA`. O motor deve classificar contas de resultado, calcular resultado operacional ajustado, tratar pressões complementares de caixa e integrar evidências e pendências.

### Módulo 7 - Gerador de Laudo CAPAG-E

Transformar resultados calculados, evidências, ajustes, bloqueios e ressalvas em laudo estruturado. O laudo deve consumir objetos já calculados e não recalcular `PLRA`, `FCA`, `ROA` ou `CAPAG-E`.

### Módulo 8 - Governança de Metodologia

Consolidar a rastreabilidade entre manuais, specs, assets, código, testes, laudo e documentos operacionais. O produto deve manter matriz de rastreabilidade, status de documentos e assets, validações automatizadas, relatório de cobertura e changelog metodológico.

## 7. Requisitos do Produto

- O produto deve importar `ECD` e estruturar dados contábeis por empresa e exercício.
- O produto deve manter a camada declarada separada da camada reclassificada.
- O produto deve preservar o `I051` como dado declaratório, sem tratá-lo como verdade única para a leitura comportamental.
- O produto deve separar plano referencial oficial, metodologia interna e resultado calculado.
- O produto deve bloquear ou diagnosticar regras metodológicas inseguras, especialmente regras por prefixo amplo.
- O produto deve calcular ou apresentar `PLRA`, `FCA`, `ROA` e `CAPAG-E` com método, status, fórmula, valor, limitações e bloqueios.
- O produto deve rotular `FCO` como componente operacional, não como `FCA` completo.
- O produto deve permitir comparação entre CAPAG declarada e CAPAG reclassificada.
- O produto deve indicar evidências positivas, evidências negativas, materialidade, justificativa e ação recomendada por conta relevante.
- O produto deve favorecer revisão humana em situações ambíguas, sensíveis ou materiais.
- O produto deve gerar trilhas de auditoria suficientes para conferência técnica.
- O produto deve gerar exportação oficial em `Excel`.
- O produto deve gerar laudo CAPAG-E a partir dos resultados calculados, sem recalcular motores.
- O produto deve manter a versão metodológica usada na análise, exportação e laudo.
- O produto deve evoluir por specs e tasks aprovadas, sem misturar governança, backend, frontend, design e metodologia na mesma execução.

## 8. Fluxos Principais

### Fluxo 1 - Preparação Governada

1. O usuário consolida documentos, arquitetura, specs, design, testes e decisões pendentes.
2. O produto passa a ter fonte de verdade clara para orientar implementação.
3. As próximas mudanças funcionais são derivadas de specs e tasks aprovadas.

### Fluxo 2 - Análise Declarada

1. O usuário importa a `ECD`.
2. O sistema lê registros contábeis relevantes.
3. O sistema identifica a classificação declarada no `I051`.
4. O sistema aplica metodologia interna versionada.
5. O sistema apresenta resultados declarados, status, alertas e auditoria.

### Fluxo 3 - Análise Reclassificada

1. O sistema monta a razão e o perfil comportamental por conta.
2. O sistema avalia sinais contábeis, contrapartidas, históricos, recorrência e materialidade.
3. O sistema recomenda manter, reclassificar, revisar ou deixar sem conclusão.
4. O usuário revisa casos relevantes.
5. O sistema compara cenário declarado e cenário reclassificado.

### Fluxo 4 - CAPAG-E por Método Definido

1. O sistema consolida `PLRA`.
2. O sistema apura `FCA` por DFC direta ou `ROA` pelo motor alternativo.
3. O sistema aplica o método CAPAG-E adequado.
4. O sistema mostra resultado final, parcial ou bloqueado com fórmula, status e limitações.

### Fluxo 5 - Evidências, Excel e Laudo

1. O usuário revisa evidências, justificativas, materialidade, bloqueios e ressalvas.
2. O sistema gera análise interna auditável.
3. O sistema exporta planilha `Excel` final.
4. O sistema gera laudo CAPAG-E estruturado sem recalcular resultados.

## 9. Critérios de Sucesso

- O usuário consegue distinguir claramente leitura declarada, leitura reclassificada e resultado final usado no laudo.
- Toda conta material ajustada ou reclassificada possui justificativa, evidência, status e trilha auditável.
- Todo resultado CAPAG-E informa método, fórmula, valor, status, limitações e bloqueios.
- `FCO` não é apresentado como `FCA` completo sem ressalva.
- O produto evita classificação automática insegura por prefixo amplo.
- Casos ambíguos ou materiais são encaminhados para revisão humana em vez de gerar falso positivo silencioso.
- A exportação `Excel` reflete resultados calculados e trilhas relevantes sem recalcular regra de negócio.
- O laudo CAPAG-E consome resultados calculados e evidencia ressalvas, bloqueios e versão metodológica.
- Documentos, specs, assets, código, testes e laudo permanecem rastreáveis entre si.
- A evolução do produto ocorre por módulos sequenciais, com critérios de aceite verificáveis.

## 10. Restrições e Premissas

- O produto é interno e voltado para um único usuário.
- A visão deste PRD é ampla e modular, baseada em `docs/reference/` e `tmp_deu_a_louca/`.
- A `ECD` permanece como fonte declaratória da análise.
- A camada reclassificada não substitui silenciosamente a camada declarada.
- O frontend não deve duplicar regra prudencial sensível.
- A exportação e o laudo não devem recalcular regra de negócio.
- Valores contábeis e prudenciais devem preservar precisão adequada; decisões técnicas específicas pertencem à arquitetura e às specs.
- Banco de dados e persistência são decisões arquiteturais pendentes quando necessários para histórico, auditoria, precedentes, revisões ou metodologia versionada.
- O produto deve preservar rastreabilidade mesmo quando uma etapa estiver parcial ou bloqueada.
- Este PRD não autoriza implementação por si só; ele orienta arquitetura, design, specs e tasks posteriores.

## 11. Riscos e Pontos em Aberto

- Decisão sobre banco de dados e persistência ainda precisa ser definida em documento arquitetural próprio.
- A fronteira entre asset metodológico versionado, dado operacional e dado de auditoria precisa ser explicitada.
- A camada reclassificada pode gerar falso positivo se usar sinais fracos, nome de conta isolado ou regras excessivamente agressivas.
- Regras por prefixo amplo podem distorcer a leitura declarada se não forem bloqueadas ou diagnosticadas.
- A relação entre `FCO`, `FCA`, `ROA`, `PLRA` e `CAPAG-E` precisa permanecer consistente entre API, frontend, Excel e laudo.
- Evidências e materialidade precisam ter status claros para não virar requisito subjetivo sem critério de bloqueio.
- O laudo pode perder confiabilidade se recalcular resultados ou omitir ressalvas.
- A migração da visão ampla para specs executáveis pode gerar tarefas grandes demais se os módulos não forem fatiados.
- Referências em `docs/reference/` e `tmp_deu_a_louca/` contêm detalhes técnicos que devem ser filtrados por arquitetura e specs antes de implementação.

## 12. Fora do Escopo

- Implementar código de produto diretamente a partir deste PRD.
- Criar SaaS, autenticação, permissões, multiusuário ou operação multiempresa simultânea sem decisão futura.
- Introduzir banco de dados ou persistência sem decisão arquitetural própria.
- Usar `DuckDB` ou trocar stack por conveniência local sem aprovação específica.
- Oferecer `CSV` como exportação oficial.
- Criar administração livre de regras metodológicas pela interface sem governança.
- Usar IA generativa como classificador decisório central.
- Fazer upload persistente de anexos, GED, assinatura digital ou protocolo externo.
- Gerar avaliação imobiliária real ou laudo ABNT completo.
- Gerar laudo que recalcule motores em vez de consumir resultados consolidados.

## 13. Critérios de Aceite do PRD

- O PRD consolida a visão ampla modular registrada em `docs/reference/` e `tmp_deu_a_louca/`.
- O PRD descreve um produto interno para um único usuário.
- O PRD deixa explícito que o resultado final esperado reúne análise auditável, exportação `Excel` e laudo CAPAG-E.
- O PRD separa objetivos, não objetivos e fora do escopo sem contradição.
- O PRD distingue camada declarada, camada reclassificada, contrato CAPAG-E, evidências, DFC/FCA, ROA/PLRA, laudo e governança metodológica.
- O PRD registra riscos e decisões em aberto em vez de escondê-los como requisitos.
- O PRD evita detalhamento de implementação que pertença à arquitetura, specs ou tasks.
- O PRD pode orientar a criação ou revisão de arquitetura, design, specs e tasks futuras.
