# Modulo 0 - Organizacao, arquitetura e design

## Objetivo

Criar a base de governanca do projeto antes de qualquer mudanca funcional grande.

Este modulo existe porque o sistema desviou em varias direcoes ao mesmo tempo. Antes de mexer em motor, frontend, metodologia ou reclassificacao, o projeto precisa declarar:

- qual e a arquitetura-alvo;
- qual e a fonte de verdade;
- como as specs serao organizadas;
- como o frontend deve navegar e se organizar;
- qual e o padrao visual do produto;
- como `README.md`, `AGENTS.md`, `CLAUDE.md`, tasks e skills devem conversar.

## Por que este e o modulo 0

Sim, existe um modulo 0.

Ele nao e um modulo funcional do produto. Ele e o modulo de organizacao do sistema.

Sem ele, qualquer trabalho no modulo 1, modulo comportamental, frontend ou skills vai continuar sendo feito em cima de documentos desalinhados.

## Resultado esperado

Ao final do modulo 0, o projeto deve ter:

- specs indexadas;
- arquitetura-alvo definida;
- frontend com direcao de rotas explicitas;
- design frontend documentado;
- estrategia de testes e validacao definida;
- higiene de repositorio e artefatos definida;
- propria pasta de planejamento consolidada, sem duplicidade confusa;
- decisao arquitetural sobre banco de dados e persistencia;
- documentos operacionais alinhados;
- roadmap de tasks revisado;
- skills preparadas para obedecer a nova organizacao.

## Ordem obrigatoria dentro do modulo

Os documentos operacionais e as skills devem ser ajustados por ultimo.

Motivo:

- `README.md`, `AGENTS.md` e `CLAUDE.md` devem refletir a arquitetura aprovada, nao antecipar decisoes ainda instaveis.
- `.agents/skills/` e `.claude/skills/` devem obedecer os documentos oficiais, nao definir a arquitetura por conta propria.
- Se os agentes forem atualizados antes da arquitetura final, eles podem consolidar premissas erradas.

## Banco de dados e persistencia

Na arquitetura vigente da V2, banco de dados e persistencia de sessao estavam fora do escopo.

Porem, a reorganizacao atual aponta que os modulos seguintes podem precisar de banco de dados:

- Modulo 1 - Camada declarada: plano referencial oficial, metodologia versionada, auditoria declarada, snapshots e rastreabilidade.
- Modulo 2 - CAPAG Reclassificada: perfis comportamentais, scores, evidencias, revisoes humanas, precedentes e comparativos.
- Modulo 3 - Contrato CAPAG-E: metodos, status, formulas, bloqueios e nomenclatura canonica.
- Modulo 4 - Evidencias e ativos: justificativas, materialidade, liquidacao forcada e suporte documental.
- Modulo 5 - DFC/FCA: fluxos operacionais, investimento, financiamento e auditoria por lancamento.
- Modulo 6 - ROA/PLRA: contas de resultado, pressoes complementares e caminho alternativo de CAPAG-E.
- Modulo 7 - Laudo: emissao estruturada sem recalculo dos motores.
- Modulo 8 - Governanca: manuais, specs, assets, testes, metodologia, agentes e skills.

Por isso, banco de dados deixa de ser apenas uma observacao futura e passa a exigir uma decisao arquitetural propria dentro do modulo 0, antes da implementacao dos modulos funcionais afetados.

Essa decisao deve justificar:

- por que a V2 em memoria deixou de atender;
- quais dados seriam persistidos;
- como isso afeta seguranca, auditoria, multiusuario, historico, deploy e testes;
- como preservar rastreabilidade sem transformar a interface em administracao operacional indevida.

Enquanto essa decisao nao for aprovada e especificada, tasks de implementacao devem tratar banco de dados como pendencia arquitetural, nao como detalhe local.

O planejamento deve separar claramente:

- arquitetura atual em memoria;
- arquitetura futura com banco;
- dados versionados como assets;
- dados operacionais persistidos;
- dados de auditoria;
- dados de precedentes.

## Fora do escopo

- Implementar modulo declarado.
- Implementar modulo comportamental.
- Introduzir banco de dados sem spec arquitetural propria.
- Introduzir persistencia de sessao sem decisao explicita.
- Alterar arquivos fora de `tmp_deu_a_louca/` durante esta fase de planejamento.
