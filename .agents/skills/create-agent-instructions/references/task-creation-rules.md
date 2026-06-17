# Regras Para Criar TASKs

## Regra Central

TASK nasce de SPEC suficiente.

Não criar TASK quando a SPEC ainda tiver decisão essencial pendente.

## TASK Deve Conter

- referência à SPEC de origem;
- objetivo da TASK;
- escopo exato;
- fora de escopo;
- passos executáveis;
- arquivos, módulos ou áreas prováveis;
- critérios de aceite herdados ou derivados da SPEC;
- validação esperada;
- riscos;
- bloqueios pendentes, se houver.

## TASK Não Deve Decidir

- arquitetura;
- contrato de API;
- regra de domínio;
- fórmula;
- fonte normativa;
- política de arredondamento;
- padrão visual;
- estratégia de teste crítica.

Se a TASK precisar decidir qualquer item acima, a SPEC está incompleta.

## Relação SPEC -> TASK

Uma SPEC pode gerar uma ou mais TASKs.

Ao dividir TASKs:

- manter cada TASK executável de forma independente;
- preservar dependências entre TASKs;
- não duplicar escopo;
- não criar TASK ampla demais;
- manter critérios de aceite verificáveis.

## Bloqueios Em TASKs

Registrar bloqueio quando:

- SPEC de origem não existir;
- SPEC não tiver critério de aceite;
- SPEC não definir contrato necessário;
- SPEC não definir fonte normativa ou regra;
- SPEC tiver decisão pendente que afete a TASK;
- validação esperada não estiver clara.
