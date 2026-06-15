# Plano de Implementação Técnico Exaustivo — Novo Fluxo Pós-Upload CAPAG-e V2

Este documento registra cada decisão técnica, de UX e de regra de negócio alinhada em diálogo. Nenhum arquivo, campo, estado ou comportamento visual foi omitido.

---

## Inventário dos Arquivos Atuais Afetados

### Frontend (React/Vite) — `web/src/`

| Arquivo | Função atual | O que acontece neste plano |
|---|---|---|
| [App.jsx](file:///Ubuntu/home/lucian/capag_v2/web/src/App.jsx) | Renderiza upload, card principal, carrossel, auditoria e pendências em sequência linear | **Refatorado**: passa a ser orquestrador de Views por estado |
| [PlrCarousel.jsx](file:///Ubuntu/home/lucian/capag_v2/web/src/components/PlrCarousel.jsx) | Carrossel com 3 slides: `RawCompositionCard`, `ClassicPlrCard`, `AdjustedPlrCard` | **Aposentado**: cada slide vira uma View independente no Hub |
| [PendingMethodologies.jsx](file:///Ubuntu/home/lucian/capag_v2/web/src/components/PendingMethodologies.jsx) | Lista grupos condicionais + painel AgGrid de resolução por grupo | **Reutilizado parcialmente**: a lógica do `GroupResolutionPanel` será base para a 3ª tela |
| [AccountAuditRows.jsx](file:///Ubuntu/home/lucian/capag_v2/web/src/components/AccountAuditRows.jsx) | Modal com tabela HTML de auditoria (sem AgGrid) | **Reutilizado**: será chamado pela 2ª tela como tabela analítica em página separada |
| [api.js](file:///Ubuntu/home/lucian/capag_v2/web/src/lib/api.js) | Funções `uploadEcdFile`, `resetSession`, `applyMethodologyGroupDecisions`, `getMethodologyOptions` | **Expandido**: novas funções para simulação macro e aplicação em lote |
| [index.css](file:///Ubuntu/home/lucian/capag_v2/web/src/styles/index.css) | Design system: variáveis CSS, glassmorphism, badges, carrossel, tabelas | **Expandido**: novas classes para switches, estados de inativação, barras de progresso |

### Backend (Python/FastAPI) — `src/capag/`

| Arquivo | Função atual | O que acontece neste plano |
|---|---|---|
| [routes.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/routes.py) | Rotas: `/upload`, `/calculate-fco`, `/methodology`, `/methodology/group-decisions`, `/methodology/clear`, `/session/reset` | **Expandido**: nova rota `/methodology/simulate-macro` |
| [schemas.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/schemas.py) | Schemas: `FcoUpdateRequest`, `MethodologyDecisionRequest`, `MethodologyGroupDecisionsRequest`, `MethodologyClearRequest` | **Expandido**: novo schema `MacroSimulationRequest` |
| [presentation.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/presentation.py) | Função `exercise_payload()` que serializa o exercício e enriquece com heurísticas e orientações condicionais | **Sem alteração estrutural** |
| [session_state.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/session_state.py) | Singleton `_active_session` com `get_active_session()`, `reset_active_session()`, `get_active_exercise()` | **Sem alteração** |
| [plr.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/engine/plr.py) | Função `calculate_plr_result(normalized, manual_decisions)` — pipeline completo de classificação, deságio e cálculo | **Expandido**: nova função de simulação macro que aceita exclusões de macrogrupo e deságios customizados |
| [heuristics.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/engine/heuristics.py) | Função `suggest_treatment(account_name)` que retorna `HeuristicSuggestion` com `suggested_action`, `suggested_reclassification_key`, `confidence`, `reason` | **Sem alteração** |
| [fco.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/engine/fco.py) | Função `calculate_fco_result(normalized)` — cálculo do FCO automático por método direto | **Sem alteração** |
| [capag.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/engine/capag.py) | Função `apply_capag_result(result, fco)` — fórmula `CAPAG-e = FCO + PLR` | **Sem alteração** |
| [models.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/domain/models.py) | Modelos: `AnalysisSession`, `ExerciseAnalysis`, `ExerciseResult`, `FcoExercise`, `AccountAuditRow`, `PendingMethodologyGroup`, `ManualMethodologyDecision`, `ManualDecisionType` (`KEEP_ORIGINAL`, `EXCLUDE_FROM_CALCULATION`, `RECLASSIFY`) | **Sem alteração estrutural** |

### Artefatos Metodológicos — `src/capag/assets/methodology/`

| Arquivo | Conteúdo atual |
|---|---|
| [tabela_metodologica_plr.csv](file:///Ubuntu/home/lucian/capag_v2/src/capag/assets/methodology/tabela_metodologica_plr.csv) | 28 regras. Fornecedores e Empréstimos marcados como `condicional` |
| [componentes_formula_plr.csv](file:///Ubuntu/home/lucian/capag_v2/src/capag/assets/methodology/componentes_formula_plr.csv) | 12 componentes (6 ativos + 6 passivos) |
| [politica_desagios_plr.json](file:///Ubuntu/home/lucian/capag_v2/src/capag/assets/methodology/politica_desagios_plr.json) | 14 regras de deságio por `regra_principal` |

---

## Fase 0 — Hub de Navegação (Orquestrador de Views)

### Decisão Arquitetural

Após o upload da ECD, o usuário **não** verá mais a tela linear atual (card de métricas → carrossel → pendências). Em vez disso, verá um **Hub com 3 cards de acesso**, cada um abrindo uma View dedicada com layout próprio. A navegação entre as Views usa o padrão **"Entrar e Sair"** (botão `← Voltar ao Hub`), e **não** abas persistentes — porque cada View tem estrutura completamente diferente, e abas causariam confusão visual ao mudar de layout drasticamente.

### Modificações em [App.jsx](file:///Ubuntu/home/lucian/capag_v2/web/src/App.jsx)

**Estado de navegação:**
```jsx
const [activeView, setActiveView] = useState('hub')
```

**Lógica de renderização condicional (substitui as linhas 100–224 atuais):**
```
Se !exercise → renderiza <UploadCloud /> (upload, como hoje)
Se activeView === 'hub' → renderiza <HubDashboard />
Se activeView === 'ecd_mirror' → renderiza <EcdMirrorView />
Se activeView === 'macro_simulator' → renderiza <MacroScenarioSimulator />
Se activeView === 'analytic_review' → renderiza <AnalyticConditionalReview />
```

**Props que cada View recebe:**
- `exercise` — objeto `ExerciseAnalysis` completo retornado pela API
- `setExercise` — setter do estado para atualizar após recálculos
- `onBack={() => setActiveView('hub')}` — função de retorno ao Hub

**Componentes aposentados:**
- O `<PlrCarousel />` (linhas 207) deixa de ser renderizado no `App.jsx`.
- O `<PendingMethodologies />` (linha 222) deixa de ser renderizado diretamente. Sua lógica será absorvida pela 3ª View.
- O modal do `<AccountAuditRows />` (linhas 215-220) deixa de existir no `App.jsx`. Será acessível como sub-view da 2ª tela.

### Novo Componente: `web/src/components/HubDashboard.jsx`

**Cabeçalho fixo:**
- Exibe `exercise.year`, `exercise.imported_file.company_name` e `exercise.imported_file.company_cnpj`.
- Botão `Importar nova ECD` (chama `resetSession()` e `setExercise(null)`).

**Banner de Alertas de Integridade (condicional):**
- Renderizado **apenas** se `exercise.result.alerts` contiver alertas com `severity === 'bloqueante'` do tipo `AlertCode.MISSING_REFERENCE_FOR_CALC` (contas sem I051).
- Exibido como barra vermelha no topo, acima dos cards.
- *Nota:* Este alerta é sobre integridade do **arquivo**, não sobre pendências metodológicas.

**Grid de 3 Cards (`grid-template-columns: repeat(3, 1fr)`):**

| Card | Título | Descrição | Ação |
|---|---|---|---|
| 1 | **Espelho da ECD** | Análise crua de Ativos e Passivos. Sem filtros prudenciais, sem deságios, sem pendências. | `onClick={() => setActiveView('ecd_mirror')}` |
| 2 | **Simulador Macrometodológico** | Teste de cenários incluindo/excluindo macrogrupos inteiros e ajustando deságios. | `onClick={() => setActiveView('macro_simulator')}` |
| 3 | **Revisão Analítica de Contas Condicionais** | Resolução de contas pendentes com sugestões inteligentes e ações em massa. | `onClick={() => setActiveView('analytic_review')}` |

**Badge de pendências no Card 3:**
- Exibe um badge vermelho com o número de contas condicionais não resolvidas: `exercise.result.methodology_pending_accounts.length`.
- Se `=== 0`, exibe badge verde `Todas resolvidas`.

**Cada card exibe apenas nome + descrição textual.** Nenhuma métrica numérica é exibida no Hub.

---

## Fase 1 — Tela 1: Espelho da ECD (`EcdMirrorView`)

### Objetivo Funcional
Exibir uma fotografia fiel do Balanço Patrimonial da empresa conforme lido da ECD. Sem filtros, deságios, exclusões ou pendências. Uma análise **crua e completa**.

### Novo Componente: `web/src/components/EcdMirrorView.jsx`

**Botão de retorno:**
```jsx
<button onClick={onBack}>← Voltar ao Hub</button>
```

**Seção 1 — Barra de Fórmulas Presumidas:**

Dois banners horizontais compactos que exibem a fórmula contábil de forma explícita e linear:

- **Linha 1:** `Ativos Brutos (R$ X) − Passivos Exigíveis Brutos (R$ Y) = PLR Presumido (R$ Z)`
- **Linha 2:** `FCO Automático (R$ A) + PLR Presumido (R$ Z) = CAPAG Presumida (R$ B)`

**Fonte dos dados:**
- `Ativos Brutos` = soma de `base_value` de todas as `audit_rows` onde `classification` começa com `ativo_`
- `Passivos Exigíveis Brutos` = soma de `base_value` de todas as `audit_rows` onde `classification` começa com `passivo_` (excluindo `macrogroup === 'patrimonio_liquido'`)
- `PLR Presumido` = Ativos Brutos − Passivos Exigíveis Brutos (calculado no React, pois é apenas soma/subtração dos dados já retornados pela API)
- `FCO Automático` = `exercise.fco.fco_automatico_calculado` (campo já existente no payload)
- `CAPAG Presumida` = FCO Automático + PLR Presumido

> **Decisão:** Estes cálculos presumidos são **exclusivamente visuais** desta tela. Não afetam o PLR oficial nem a CAPAG-e oficial da sessão.

**Seção 2 — Balanço Patrimonial Lado a Lado:**

Layout CSS: `display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem`.

**Coluna Esquerda — Ativos:**
- O frontend itera sobre as `audit_rows` e agrupa por `macrogroup` onde `classification` começa com `ativo_`.
- Para cada macrogrupo encontrado (ex: `ativos_circulantes`, `ativos_nao_circulantes`):
  - **Linha principal destacada** (fonte grande, negrito, cor `var(--accent-color)`): Nome do macrogrupo + Total do macrogrupo.
  - **Linhas secundárias** (fonte menor, cor `var(--text-secondary)`): Subtotais agrupados por `methodology_group` (ex: `caixa`, `bancos`, `clientes_normais`, `estoques`).

**Coluna Direita — Passivos e PL:**
- Mesma estrutura visual simétrica (linha principal destacada + linhas secundárias).
- Inclui o macrogrupo `patrimonio_liquido` (exibido mas **não contabilizado** no PLR presumido acima).

> **Decisão:** Os macrogrupos são **dinâmicos** — determinados pelos dados reais do `audit_rows` retornado pela API após o processamento da ECD. Se a empresa não tiver estoques, o grupo simplesmente não aparece.

**Seção 3 — Informação Visual:**
- **Barra horizontal empilhada (Progress Bar)** mostrando a proporção Circulante vs Não Circulante tanto para Ativos quanto para Passivos.
- Permite visualizar instantaneamente o perfil de liquidez e endividamento da empresa.

### Tratamento de Alertas nesta Tela
- **Não exibe nenhum alerta de pendência metodológica.** Esta é uma visão crua.
- Se houver contas sem vínculo referencial (campo `reference_code === null` no `audit_rows`), exibir um banner informativo discreto: `⚠️ X contas da ECD não possuem vínculo referencial (I051) e não foram classificadas.`

### Mudanças no Backend
- **Nenhuma rota nova necessária.** Todos os dados já existem no payload `exercise_payload()` retornado por `POST /api/upload`.

---

## Fase 2 — Tela 2: Simulador por Macrogrupos (`MacroScenarioSimulator`)

### Objetivo Funcional
Permitir ao analista testar cenários contábeis rápidos, confiando na classificação original da ECD. O analista pode incluir/excluir macrogrupos inteiros, ajustar deságios e alternar entre FCO automático e manual. Cada alteração recalcula o PLR e CAPAG simulados em tempo real.

### Novo Componente: `web/src/components/MacroScenarioSimulator.jsx`

**Botão de retorno:**
```jsx
<button onClick={onBack}>← Voltar ao Hub</button>
```

**Seção 1 — Resultados em Tempo Real (Sticky Header):**
- Barra fixa no topo (`position: sticky; top: 0`) com fundo escuro e glassmorphism.
- Exibe: `PLR Simulado: R$ X` | `CAPAG Simulada: R$ Y`
- Atualiza instantaneamente a cada interação do usuário.

**Seção 2 — Controle do FCO:**
- **Texto informativo:** `FCO Automático (Método Direto): R$ X` — valor lido de `exercise.fco.fco_automatico_calculado`.
- **Switch:** `[ ] Informar FCO Manual (Sobrescrever)`.
- **Input numérico:** `<input type="number" disabled={!switchAtivo} />`.
- **Comportamento:** Por padrão o input está `disabled=true`. Se o switch for ativado, o input libera. Ao digitar um valor, a CAPAG simulada recalcula usando o valor manual em vez do automático.

**Seção 3 — Painel de Controle de Macrogrupos (Dinâmico):**

A lista de macrogrupos é gerada **dinamicamente** a partir dos dados reais da ECD importada:
```jsx
const macrogroups = Object.entries(
  auditRows.reduce((acc, row) => {
    const key = row.macrogroup
    acc[key] = (acc[key] || 0) + Number(row.base_value)
    return acc
  }, {})
)
```

Para cada macrogrupo, renderizar uma linha de controle com:

| Elemento | Tipo | Comportamento |
|---|---|---|
| **Nome do macrogrupo** | Texto | Ex: `ATIVOS CIRCULANTES` |
| **Saldo bruto** | Texto | Ex: `R$ 26.181.242,37` |
| **Switch Incluir/Excluir** | Toggle (`<input type="checkbox">`) | Ativado = incluído no cálculo. Desativado = excluído. |
| **Input Deságio %** | `<input type="number">` | Apenas para macrogrupos de natureza `ativo`. Valor inicial lido de [politica_desagios_plr.json](file:///Ubuntu/home/lucian/capag_v2/src/capag/assets/methodology/politica_desagios_plr.json). |

**Comportamento visual de exclusão (decisão UX crítica):**

Quando o switch é **desativado**:
1. O container do macrogrupo recebe `opacity: 0.4` (apagado mas visível).
2. O valor do saldo recebe `text-decoration: line-through` (tachado).
3. O switch muda de cor (de verde/azul para cinza escuro).
4. A label muda para `Excluído do cálculo` em vermelho.
5. O macrogrupo **NÃO desaparece** da tela — permanece visível para o analista poder reativar com um clique.

**Seção 4 — Botão "Abrir Auditoria Analítica":**
- Um botão discreto que navega para uma sub-view em tela cheia exibindo todas as contas contábeis daquele cenário simulado.
- A tabela de auditoria é **sem agrupamentos** (flat list), mostrando conta a conta: código, nome, referencial, grupo, saldo, deságio aplicado, valor econômico, status.
- Esta tabela reutiliza a estrutura do componente [AccountAuditRows.jsx](file:///Ubuntu/home/lucian/capag_v2/web/src/components/AccountAuditRows.jsx) existente, mas abre em **página separada** (não como modal sobre a tela do simulador).

### Estado Local React do Simulador
```jsx
const [macroStates, setMacroStates] = useState({})
// Estrutura: { 'ativos_circulantes': { active: true, desagio: 0.20 }, ... }

const [fcoManualActive, setFcoManualActive] = useState(false)
const [fcoManualValue, setFcoManualValue] = useState('')
```

### Contrato Backend — Nova Rota de Simulação

**Arquivo:** [routes.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/routes.py)

**Nova rota:** `POST /api/methodology/simulate-macro`

**Novo schema em** [schemas.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/schemas.py)**:**
```python
class MacroSimulationRequest(BaseModel):
    year: int
    excluded_macrogroups: list[str]          # ex: ["patrimonio_liquido", "estoques"]
    custom_desagios: dict[str, str]          # ex: {"ativos_circulantes": "0.30"}
    fco_manual_override: str | None = None   # ex: "4821472.51" ou None
```

**Lógica da rota:**
1. Localiza o exercício na sessão ativa via `get_active_exercise(year)`.
2. Acessa `exercise.imported_file.normalized_ecd` (a base ECD completa em memória).
3. Chama uma **nova função** em [plr.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/engine/plr.py): `simulate_macro_plr(normalized, excluded_macrogroups, custom_desagios)`.
4. Esta função **não altera** o estado oficial da `AnalysisSession`. Ela executa uma variação read-only do pipeline de `calculate_plr_result`, filtrando os macrogrupos excluídos e substituindo os deságios padrão pelos customizados.
5. Retorna um payload leve contendo apenas: `plr_simulado`, `capag_simulada`, `ativos_simulados`, `passivos_simulados`, e opcionalmente `audit_rows_simuladas` para a tabela de auditoria.

> **Decisão Arquitetural:** A simulação **não** grava nada na sessão. Regra de negócio permanece no backend. O frontend não duplica fórmulas de PLR.

### Tratamento de Alertas nesta Tela
- **Não exibe alertas de pendência condicional individual.**
- Exibe apenas um **indicador informativo discreto** no topo: `⚠️ Existem X contas condicionais sendo consideradas sob a regra padrão de seus macrogrupos.`

---

## Fase 3 — Tela 3: Revisão Analítica de Contas Condicionais (`AnalyticConditionalReview`)

### Objetivo Funcional
Permitir ao analista resolver individualmente cada conta classificada como `condicional` pela [tabela_metodologica_plr.csv](file:///Ubuntu/home/lucian/capag_v2/src/capag/assets/methodology/tabela_metodologica_plr.csv). É a única tela onde as pendências oficiais do exercício são resolvidas.

### Novo Componente: `web/src/components/AnalyticConditionalReview.jsx`

**Botão de retorno:**
```jsx
<button onClick={onBack}>← Voltar ao Hub</button>
```

**Seção 1 — Barra de Progresso de Resolução:**
- Componente visual: `Contas Resolvidas: X de Y` com barra de progresso preenchida.
- `Y` = total de contas condicionais (`exercise.result.methodology_pending_accounts.length` + contas já resolvidas).
- `X` = contas onde `status === 'Resolvido'`.
- **Regra:** O PLR Ajustado oficial e a CAPAG-e oficial só ficam disponíveis quando a barra atinge 100%.

**Seção 2 — Filtros Rápidos:**
- Grupo de 3 botões no topo da tabela:
  - `[Apenas Pendentes]` — filtra contas onde nenhuma decisão foi tomada.
  - `[Resolvidas]` — filtra contas onde já existe decisão (manual ou aceita do sistema).
  - `[Todas]` — sem filtro.
- **Barra de Pesquisa Global:** Input de texto que filtra instantaneamente por código de conta, nome ou grupo.

**Seção 3 — Botão Supremo em Lote:**
```
⚡ Aplicar todas as sugestões do sistema (X pendentes)
```

**Regras de funcionamento do botão supremo:**

1. O botão itera sobre **todas as contas atualmente visíveis na grid**.
2. Para cada conta, verifica o **estado interno** da conta:
   - Se `status === 'Pendente'` → aplica a sugestão do campo `suggested_action` (calculado por [heuristics.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/engine/heuristics.py) via [presentation.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/presentation.py), linha 78-84).
   - Se `status === 'Resolvido'` → **NÃO TOCA**. A decisão manual do analista tem **prioridade absoluta** e nunca é sobrescrita pela automação.
3. Após aplicar, envia o payload em lote para `POST /api/methodology/group-decisions`.

> **Regra de Ouro:** A partir do momento em que o analista clica em qualquer botão manual (Manter, Excluir ou Reclassificar) em uma conta, essa conta muda para `status === 'Resolvido'` e fica **protegida** de qualquer ação em lote futura.

**Seção 4 — Tabela AgGrid (Virtual Scrolling):**

Usa `ag-grid-react` (já instalado no projeto, usado em [PendingMethodologies.jsx](file:///Ubuntu/home/lucian/capag_v2/web/src/components/PendingMethodologies.jsx)) com renderização virtualizada para suportar milhares de linhas a 60 FPS.

**Colunas da tabela:**

| # | Campo | Header | Tipo | Editável? | Origem do Dado |
|---|---|---|---|---|---|
| 1 | `account_code` | Conta | Texto | Não | `PendingMethodologyAccount.account_code` |
| 2 | `account_name` | Nome da Conta | Texto | Não | `PendingMethodologyAccount.account_name` |
| 3 | `base_value` | Saldo | Moeda | Não | `PendingMethodologyAccount.base_value` |
| 4 | `suggested_action` | Sugestão do Sistema | Badge + Botão | Não (mas com botão `[✓ Aceitar]`) | `HeuristicSuggestion.suggested_action` via `presentation.py` |
| 5 | `decision_action` | Decisão Manual | 3 Botões Pill | Sim (interativo) | Estado local React |
| 6 | `decision_reclassification_key` | Destino (se Reclassificar) | Dropdown/Select | Sim (condicional) | Populado por `get_reclassification_options()` da rota `GET /api/methodology/options` |

**Detalhamento da Coluna 4 — "Sugestão do Sistema":**
- Cell Renderer customizado que exibe:
  - Um **Badge colorido** com a sugestão: `Manter` (verde), `Excluir` (vermelho), `Reclassificar para [destino]` (roxo).
  - O nível de confiança: `confidence` (`alta`, `media`, `baixa`) — vindo de `HeuristicSuggestion.confidence`.
  - O motivo: `reason` — tooltip ao passar o mouse.
  - Um botão circular `[✓ Aceitar]` que aplica a sugestão para aquela conta individual e muda o status para `Resolvido`.

**Detalhamento da Coluna 5 — "Decisão Manual" (As 3 Ações):**
- Cell Renderer customizado com **3 botões Pill** lado a lado:
  - `[Manter]` — Aplica `ManualDecisionType.KEEP_ORIGINAL` (`manter_classificacao_original`). Inclui a conta no cálculo com deságio padrão do grupo.
  - `[Excluir]` — Aplica `ManualDecisionType.EXCLUDE_FROM_CALCULATION` (`excluir_do_calculo`). A linha inteira do AgGrid recebe `opacity: 0.4` e `text-decoration: line-through` no saldo.
  - `[Reclassificar]` — Aplica `ManualDecisionType.RECLASSIFY` (`reclassificar`). Ativa a Coluna 6 (dropdown) para que o analista escolha o grupo de destino.
- **Ao clicar em qualquer um dos 3 botões**, a conta muda imediatamente para `status === 'Resolvido'` no estado local React.

**Detalhamento da Coluna 6 — "Destino":**
- Um `<select>` populado pela resposta de `GET /api/methodology/options` (função `get_reclassification_options()` de [plr.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/engine/plr.py), linha 211-248).
- Cada opção mostra: `[código referencial] - [rótulo]` (ex: `2.01.02.01.01 - Empréstimos bancários`).
- Este campo fica **desabilitado** até que o botão `[Reclassificar]` seja clicado na Coluna 5.

**Envio ao Backend:**
- O componente coleta todas as decisões da grid (via `gridRef.current.api.forEachNode`) e envia para `POST /api/methodology/group-decisions` em [routes.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/api/routes.py) (linhas 87-103).
- O backend executa `AnalysisSession.set_methodology_decision()` (em [models.py](file:///Ubuntu/home/lucian/capag_v2/src/capag/domain/models.py), linhas 744-766) para cada conta do lote, e depois recalcula o PLR oficial via `run_exercise_analysis()`.

### Tratamento de Alertas nesta Tela
- **Os alertas são os protagonistas.** Cada conta pendente exibe um ícone `⚠️` amarelo. À medida que o analista resolve, o ícone muda para `✅` verde.
- A barra de progresso no topo reflete o avanço.
- Quando 100% das contas estiverem resolvidas, o Hub exibirá `PLR Disponível` e a CAPAG-e será calculável (se houver FCO válido).

---

## Questões em Aberto para Revisão

> [!IMPORTANT]
> 1. **Você concorda** que o Hub exibirá apenas nome + descrição nos cards, sem nenhuma métrica numérica prévia?

> [!IMPORTANT]
> 2. **Rota efêmera do Simulador (Fase 2):** A simulação não grava nada na sessão. O PLR oficial da sessão continua bloqueado se houver pendências condicionais. O "PLR Simulado" existe apenas enquanto a tela está aberta. Essa separação entre "simulação" e "oficial" está clara e aceita?

> [!IMPORTANT]
> 3. **Regra de Ouro do Botão Supremo (Fase 3):** O botão "Aplicar Sugestões" atua **apenas** nas contas com `status === 'Pendente'`, nunca sobrescreve decisão manual. Confirma?
