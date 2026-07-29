# LOG ESPECIAL - Retomada Da Homologação Da SPEC-012

## Nota Sobre Este Documento

Este log especial representa a consolidação da execução das `TASK-101` a
`TASK-108`.

Os resultados detalhados, arquivos alterados e validações de cada TASK estão
expostos nos respectivos logs:

- `logs/LOG-101-ampliar-parser-balanco-declarado.md`;
- `logs/LOG-102-persistir-ecd-balanco-declarado.md`;
- `logs/LOG-103-reprocessar-importacoes-ecd-legadas.md`;
- `logs/LOG-104-implementar-conciliacao-balanco-declarado.md`;
- `logs/LOG-105-criar-api-balanco-declarado.md`;
- `logs/LOG-106-criar-ui-balanco-declarado.md`;
- `logs/LOG-107-integrar-validade-balanco-plra-capag.md`;
- `logs/LOG-108-validar-fluxo-balanco-declarado.md`.

Este documento não substitui esses logs. Sua finalidade é permitir a retomada
rápida da homologação consolidada na próxima sessão.

## Estado Atual

- SPEC: `specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`.
- Grupo: `TASK-101` a `TASK-108`.
- Status: `aguardando_homologacao`.
- Próxima ação: ler este documento e retomar a homologação do grupo.

## Arquitetura Implementada

```text
Arquivo ECD original
        |
        v
Parser 2.1.0
        |
        v
PostgreSQL
  - bytes e SHA-256 imutáveis
  - registros ECD normalizados
        |
        v
Motor do Balanço Declarado
  J100 = estrutura e valores apresentados
  I050 -> I052 -> J100 = vínculo de aglutinação
  I155 = saldos usados na conciliação
        |
        v
API específica -> frontend sem recálculo
        |
        v
balance_status -> elegibilidade do PLRA -> elegibilidade da CAPAG-E
```

Responsabilidades essenciais:

- `J100` declara a árvore, descrição, saldo inicial e saldo final do balanço;
- `I052` liga a conta analítica do `I050` ao código de aglutinação do `J100`;
- `I155` fornece o saldo conciliado por conta e centro de custo;
- `I051` não constrói o balanço e permanece como vínculo referencial do PLRA;
- consultas ao balanço não persistem snapshots;
- frontend e Excel apenas apresentam contratos produzidos pelo backend.

## Processo Implementado

1. `TASK-101`: ampliou o parser para os registros necessários ao balanço.
2. `TASK-102`: preservou o arquivo original e persistiu os registros normalizados.
3. `TASK-103`: criou reimportação controlada por mesmo SHA-256, preservando IDs e invalidando resultados derivados.
4. `TASK-104`: criou o motor de obrigatoriedade, árvore, totalizadores e conciliação.
5. `TASK-105`: criou a API específica do balanço e a consulta de componentes.
6. `TASK-106`: criou a tela em duas colunas, sem switches ou cálculos locais.
7. `TASK-107`: propagou `balance_status` para PLRA e CAPAG-E sem alterar fórmulas.
8. `TASK-108`: consolidou testes, corrigiu o `I030` oficial, validou migrations e executou DATAPACK e INVENTCLOUD separadamente.

## Regra Final

- `VALIDO`: permite resultado anual final.
- `DIVERGENTE`, `OBRIGATORIO_AUSENTE`, `ESTRUTURA_INVALIDA` ou
  `NAO_OBRIGATORIO`: preservam valores diagnósticos, mas impedem PLRA/CAPAG-E
  final.
- Esses estados são automáticos, não são switches nem decisões humanas.
- Fórmulas, deságios e tratamentos prudenciais não foram alterados.

## Resultado Consolidado

- Parser final: `2.1.0`.
- Migration final: `0059_parser_2_1`.
- Backend: 278 testes aprovados.
- Frontend: 27 testes e build aprovados.
- Playwright: 9 testes aprovados.
- DATAPACK: `VALIDO`, com 48 linhas de detalhe conciliadas.
- INVENTCLOUD: `DIVERGENTE`, com 502 linhas conciliadas e 19
  `SEM_SALDO_I155`.
- Nenhum valor contábil ou prudencial utiliza `float`.

## Pauta Especial: Versionamento E Arquivos Temporários

Esta pauta foi incluída para apreciação do usuário na próxima sessão. Nenhuma
limpeza ou alteração de versionamento foi executada.

### Diagnóstico Atual

- `.playwright-mcp/`: possui 159 arquivos locais; 92 estão rastreados pelo Git,
  52 logs estão ignorados pela regra geral `*.log` e 15 snapshots YAML estão
  como não rastreados. A pasta não possui regra própria no `.gitignore`.
- Entre os arquivos rastreados de `.playwright-mcp/` existe uma planilha
  `.xlsx`, que pode conter dados contábeis. Os arquivos da pasta são artefatos
  locais de inspeção do MCP Playwright, não os testes reproduzíveis mantidos em
  `frontend/e2e/`.
- `.agents/`: possui 25 arquivos, todos rastreados. Contém skills, regras e
  referências operacionais próprias do projeto.
- `.codex/`: está vazia, sem arquivos rastreados e sem regra no `.gitignore`.
- `.github/`: contém apenas o workflow rastreado `.github/workflows/ci.yml`.
- Caches Python e diretórios de build encontrados no backend já estão cobertos
  pelas regras atuais de `.gitignore`.

### Decisões Pendentes Para A Próxima Sessão

1. Confirmar se `.playwright-mcp/` deve ser integralmente ignorada.
2. Decidir se os 92 arquivos já rastreados devem sair do índice do Git sem
   apagar inicialmente as cópias locais.
3. Avaliar a planilha rastreada antes da limpeza, inclusive quanto a dados
   contábeis e eventual necessidade de preservação.
4. Confirmar `.agents/` como conteúdo governado e versionado do projeto.
5. Definir o tratamento de `.codex/`: manter sem regra enquanto vazia ou
   ignorar somente conteúdos locais que ela venha a gerar.
6. Confirmar `.github/` como automação versionada do projeto.
7. Avaliar outras pastas e padrões de desenvolvimento para separar fonte
   reproduzível, evidência governada e artefato temporário.

### Processo De Exclusão A Ser Definido

O processo deverá distinguir duas operações:

- **exclusão do versionamento**: adicionar regras específicas ao `.gitignore`
  e retirar artefatos já rastreados apenas do índice do Git;
- **exclusão local**: apagar arquivos temporários do disco somente depois de
  confirmar que nenhuma evidência necessária precisa ser preservada.

Antes de qualquer exclusão, deverá ser gerada uma lista objetiva dos arquivos,
classificando cada item como fonte/teste reproduzível, evidência governada ou
artefato temporário. A limpeza deverá usar caminhos explícitos, preservar
`frontend/e2e/`, logs governados e configurações do projeto, e ser registrada
no log correspondente. Também deverá ser decidido se essa verificação ocorrerá
ao final de cada execução ou por uma rotina periódica.

## Roteiro Para A Próxima Sessão

1. Ler este log especial.
2. Confirmar o DATAPACK como `VALIDO`.
3. Revisar o INVENTCLOUD e suas 19 linhas `SEM_SALDO_I155`.
4. Confirmar que a tela reproduz o `J100` e abre componentes `I050/I052/I155`.
5. Confirmar que balanço inválido preserva diagnóstico, mas bloqueia resultado final.
6. Deliberar sobre a pauta especial de versionamento e limpeza de arquivos
   temporários, sem misturá-la automaticamente à homologação funcional.
7. Homologar o grupo ou registrar ajustes relacionados às TASKs `101` a `108`.
