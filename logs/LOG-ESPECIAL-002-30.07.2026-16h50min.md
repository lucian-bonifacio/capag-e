# LOG ESPECIAL - 002 - 30/07/2026 16h50min - Pendencias Pos-Homologacao Da SPEC-012

## Contexto

Este log especial substitui, para retomada futura, a pendencia operacional do
`logs/LOG-ESPECIAL-001-29.07.2026-23h16min.md`.

O grupo `TASK-101` a `TASK-108`, referente a
`specs/SPEC-012-modulo-1c-balanco-patrimonial-declarado.md`, foi homologado
pelo usuario em 30/07/2026.

Os logs individuais `LOG-101` a `LOG-108` foram atualizados para `concluido` e
`aprovado`. O `ROADMAP.md` foi atualizado para marcar o grupo como concluido.

## Pendencias Remanescentes

### 1. Criar TASK Governada Para Gates De Frontend, Design, UI E UX

Pendencia obrigatoria registrada por decisao do usuario:

- criar uma TASK governada para revisar e ajustar as skills governadas,
  principalmente as skills de execucao de TASKs, com gate forte para ajustes de
  frontend, design, UI e UX.

Diretrizes desejadas:

- identificar explicitamente a referencia visual governada antes de implementar;
- tratar tela anterior aprovada como baseline visual quando existir;
- exigir autorizacao expressa para mudancas visuais relevantes;
- impedir que ajuste tecnico altere layout, fonte, espacamento, densidade,
  componentes visuais ou hierarquia visual sem autorizacao;
- em homologacao, tratar reprovacao visual relacionada ao grupo como ajuste da
  TASK atual;
- validar comparacao objetiva com baseline aprovado quando houver referencia.

Encaminhamento:

- na proxima sessao, aplicar o fluxo governado adequado para confirmar a criacao
  da TASK;
- se confirmado, usar `task-planner`;
- criar a TASK sem executa-la no mesmo passo, salvo nova autorizacao explicita.

### 2. Decidir Regra Futura Para CAPAG-E Com `DIVERGENTE` Auditado

Ainda nao aprovado:

- criar regra governada futura para permitir CAPAG-E mesmo com divergencia,
  desde que exista auditoria suficiente.

Observacao:

- esta regra nao pertence a camada declarada pura da `SPEC-012`;
- exige nova decisao governada, pois altera elegibilidade/metodologia do
  resultado final.

### 3. Decidir SPEC Ou TASK Para Simulacoes Manuais

Ainda precisa ser decidido:

- se sera criada nova SPEC para simulacao/revisao prudencial manual;
- se essa SPEC deve vir antes da execucao completa da camada reclassificada ou
  comportamental;
- como switches devem operar em contas sinteticas e analiticas;
- como evitar dupla exclusao entre conta sintetica e filhos;
- se cenarios serao descartaveis ou persistidos;
- como registrar justificativa, evidencia e impacto em PLRA/CAPAG-E;
- como diferenciar teste exploratorio de resultado final.

### 4. Deliberar Sobre Versionamento E Arquivos Temporarios

Pendente desde logs especiais anteriores:

- decidir se `.playwright-mcp/` deve ser integralmente ignorada;
- decidir se os arquivos ja rastreados de `.playwright-mcp/` devem sair do
  indice do Git sem apagar inicialmente as copias locais;
- avaliar planilha `.xlsx` rastreada em `.playwright-mcp/`, inclusive quanto a
  dados contabeis e necessidade de preservacao;
- confirmar `.agents/` como conteudo governado e versionado;
- definir tratamento de `.codex/`;
- confirmar `.github/` como automacao versionada;
- definir rotina para separar fonte reproduzivel, evidencia governada e
  artefato temporario.

Nenhuma limpeza ou exclusao foi executada nesta sessao.

## Roteiro Para A Proxima Sessao

1. Ler integralmente este log especial.
2. Informar ao usuario que o Log Especial de pendencias pos-homologacao foi
   consultado.
3. Tratar primeiro a pendencia obrigatoria de criar TASK governada para gates de
   frontend/design/UI/UX.
4. Pedir confirmacao explicita antes de criar qualquer TASK.
5. Apos resolver a pendencia obrigatoria, recalcular a proxima tarefa pelo fluxo
   normal do `ROADMAP.md`.
