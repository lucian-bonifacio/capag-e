# Lente Domain Engine CAPAG

Esta lente é específica do projeto CAPAG e de domínios prudenciais/contábeis equivalentes.

Não aplicar genericamente em outros projetos sem adaptação explícita do usuário.

Esta lente foi consolidada nesta skill como especialização de domínio/engine para o projeto CAPAG.

O `AGENTS.md` gerado não deve citar materiais históricos de referência como fontes operacionais. As fontes diretas devem ser os documentos oficiais atuais do projeto.

## Quando Aplicar

Aplicar quando uma SPEC envolver:

- domínio prudencial ou contábil;
- engine de cálculo;
- regras de CAPAG-e;
- PLR;
- FCO;
- auditoria;
- classificação prudencial;
- valores contábeis, fiscais, financeiros ou prudenciais;
- `Decimal`;
- arredondamento;
- integração de cálculo com parser, API, frontend ou exportação.

## SPEC Deve Explicitar

- conceitos, entidades, estados e invariantes afetados;
- dono da regra prudencial;
- entradas conceituais exigidas;
- saídas, alertas e diagnósticos;
- fórmula, método ou critério prudencial;
- fonte normativa ou decisão aprovada;
- uso obrigatório de `Decimal`;
- escala, quantização e política de arredondamento;
- onde o arredondamento ocorre;
- onde o arredondamento não deve ocorrer;
- tratamento de zero, nulo, sinal, período, exercício e moeda;
- evidências para auditoria;
- etapas intermediárias preservadas;
- contrato de saída para API, frontend ou exportação;
- golden cases e testes esperados.

## Fontes Normativas

Regra contábil, fiscal, financeira, prudencial, fórmula, arredondamento, classificação ou critério metodológico exige fonte normativa identificada.

Usar como fonte:

- PRD oficial do projeto;
- arquitetura oficial do projeto;
- documentos governados aprovados;
- manuais, normas, portarias ou notas técnicas oficialmente incorporadas ao projeto;
- ADRs ou decisões técnicas aprovadas;
- fonte indicada explicitamente pelo usuário.

Código existente, testes e worklogs são evidência de comportamento atual, não fonte normativa suficiente.

## Bloqueios

Bloquear quando houver:

- regra prudencial indefinida;
- fórmula indefinida;
- política de arredondamento indefinida;
- fonte normativa ausente;
- tentativa de usar `float`;
- tentativa de duplicar regra no frontend, API ou exportação;
- ausência de golden case para comportamento de alto risco.

## Observação Para Projetos Não CAPAG

Em projetos genéricos, substituir esta lente por uma lente de domínio equivalente do projeto.

Não carregar termos CAPAG, PLR, FCO ou CAPAG-e para outro projeto sem autorização explícita.
