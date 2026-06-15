# 11 - Decisao arquitetural sobre banco de dados e persistencia

## Objetivo

Definir se a nova arquitetura do sistema passara a usar banco de dados, quais dados serao persistidos e em que momento essa mudanca entrara no roadmap.

## Ponto de decisao

Decidir se banco de dados passa a ser parte da arquitetura-alvo do projeto antes da implementacao dos modulos 1 e 2.

## Por que esta tarefa existe

A arquitetura atual da V2 foi desenhada sem banco de dados e sem persistencia de sessao.

Porem, a reorganizacao do sistema indica necessidades que podem justificar banco:

- catalogo oficial do plano referencial;
- metodologia versionada;
- snapshots de analise declarada;
- auditoria historica;
- resultados comparativos;
- perfis comportamentais;
- scores;
- evidencias;
- revisoes humanas;
- precedentes;
- futura rastreabilidade por empresa, exercicio e usuario.

## Arquivos e areas correlatas

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/specs/spec-00-visao-geral-e-decisoes-arquiteturais.md`
- futuras specs do modulo 1
- futuras specs do modulo 2
- `src/capag/api/`
- `src/capag/application/`, se aprovado
- `src/capag/domain/`
- `src/capag/engine/`
- `src/capag/assets/`
- `tests/`

## Perguntas que precisam ser respondidas

- O banco sera obrigatorio ja no Modulo 1?
- O banco sera obrigatorio apenas no Modulo 2?
- O sistema continuara aceitando modo em memoria para desenvolvimento/teste?
- Qual banco sera usado?
- Havera ORM ou acesso SQL direto?
- Como serao migracoes?
- O que continua como asset versionado no repositorio?
- O que vira dado operacional persistido?
- Como separar configuracao metodologica de resultado de analise?
- Como lidar com historico e auditoria?
- Como lidar com multiempresa, multiusuario e permissoes?
- Como limpar dados sensiveis em ambiente local?

## Possiveis categorias de dados

### Dados referenciais/metodologicos

- plano referencial oficial;
- metodologia PLR;
- metodologia FCO;
- mapeamentos familia -> referencial;
- regras comportamentais;
- politicas de desagio.

### Dados operacionais

- empresas;
- arquivos ECD importados;
- exercicios;
- sessoes/analises;
- resultados calculados;
- snapshots de payload;
- exportacoes geradas.

### Dados de auditoria

- audit rows;
- memoria de calculo;
- alertas;
- inconsistencias;
- justificativas;
- evidencias.

### Dados comportamentais

- razao por conta;
- perfis comportamentais;
- scores por familia;
- classificacoes sugeridas;
- comparativos declarado vs reclassificado.

### Dados humanos

- revisoes;
- comentarios;
- decisoes;
- precedentes;
- usuario revisor;
- data/hora.

## Entregavel

Uma decisao arquitetural documentada sobre banco de dados e persistencia.

## Criterios de sucesso

- Fica claro se a nova arquitetura tera banco.
- Fica claro o que sera persistido e o que continuara versionado como asset.
- Modulo 1 e Modulo 2 nao tomam decisoes conflitantes.
- `README.md`, `AGENTS.md`, `CLAUDE.md` e skills so serao atualizados depois desta decisao.

## Fora do escopo

- Escolher banco sem analisar impactos.
- Implementar persistencia.
- Criar migracoes.
- Alterar codigo fora de `tmp_deu_a_louca/`.

