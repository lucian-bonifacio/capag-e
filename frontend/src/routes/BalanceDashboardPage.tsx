import { useEffect, useMemo, useState } from "react";
import { Activity, AlertTriangle, CheckCircle2, ClipboardCheck, Columns, List, Search, Upload, X } from "lucide-react";
import { Link } from "react-router-dom";

import { AccountRow } from "../components/dashboard/AccountRow";
import { BalanceGroup } from "../components/dashboard/BalanceGroup";
import { BalanceLedger } from "../components/dashboard/BalanceLedger";
import { SegmentedControl } from "../components/dashboard/SegmentedControl";
import { StatCard } from "../components/dashboard/StatCard";
import {
  fetchDeclaredBalanceComponents,
  type DeclaredBalanceComponentsResponse,
  type DeclaredBalanceLineStatus,
  type DeclaredBalanceResponse,
  type DeclaredBalanceRow,
  type DeclaredBalanceStatus,
} from "../api/declared";
import { formatCurrency } from "../lib/formatters";
import "./BalanceDashboardPage.css";

type BalanceDashboardPageProps = {
  analysisId: string;
  year: string;
  balance?: DeclaredBalanceResponse;
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
};

type SelectedRow = {
  aggregationCode: string;
  description: string;
  declaredAmount: string;
  reconciledAmount: string | null;
  difference: string | null;
  reconciliationStatus: DeclaredBalanceLineStatus | null;
  componentCount: number;
};

type ViewMode = "columns" | "ledger";

type DashboardRow = {
  row: DeclaredBalanceRow;
  depth: number;
};

type DashboardGroup = {
  id: string;
  title: string;
  root: DeclaredBalanceRow;
  rows: DashboardRow[];
  side: "asset" | "liabilityEquity";
};

const BALANCE_STATUS: Record<
  DeclaredBalanceStatus,
  { label: string; detail: string; variant: "success" | "warning" | "danger" | "neutral" }
> = {
  VALIDO: {
    label: "Válido",
    detail: "Estrutura e linhas de detalhe conciliadas.",
    variant: "success",
  },
  DIVERGENTE: {
    label: "Conciliação pendente",
    detail:
      "A ECD foi importada, mas existem divergências entre J100 e I050/I052/I155.",
    variant: "warning",
  },
  OBRIGATORIO_AUSENTE: {
    label: "Balanço ausente",
    detail: "O Balanço Patrimonial era obrigatório, mas não foi declarado.",
    variant: "danger",
  },
  ESTRUTURA_INVALIDA: {
    label: "Estrutura inválida",
    detail: "A estrutura declarada não atende às regras do J100.",
    variant: "danger",
  },
  NAO_OBRIGATORIO: {
    label: "Não obrigatório",
    detail: "O Bloco J não era obrigatório para este período.",
    variant: "neutral",
  },
};

const LINE_STATUS: Record<
  DeclaredBalanceLineStatus,
  { label: string; variant: "success" | "warning" | "danger" }
> = {
  CONCILIADA: { label: "Conciliada", variant: "success" },
  DIVERGENTE: { label: "Divergente", variant: "warning" },
  SEM_I052: { label: "Sem vínculo I052", variant: "danger" },
  SEM_SALDO_I155: { label: "Sem saldo I155", variant: "danger" },
};

function normalizeText(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toUpperCase();
}

function formatPeriod(value: string | null): string {
  if (!value) {
    return "Não informado";
  }

  const [year, month, day] = value.split("-");
  return `${day}/${month}/${year}`;
}

function limitationText(code: string): string {
  const known: Record<string, string> = {
    BLOCO_J_NAO_OBRIGATORIO: "Bloco J não obrigatório para o período.",
    I010_AUSENTE_OU_AMBIGUO: "Forma de escrituração I010 ausente ou ambígua.",
    I030_AUSENTE_OU_AMBIGUO: "Data de encerramento I030 ausente ou ambígua.",
    J100_OBRIGATORIO_AUSENTE: "Balanço J100 obrigatório ausente.",
    J150_OBRIGATORIO_AUSENTE: "Demonstração J150 obrigatória ausente.",
    MULTIPLOS_J005_APLICAVEIS: "Mais de um J005 aplicável ao encerramento.",
    J100_LADOS_DIVERGENTES: "Ativo e Passivo + PL não apresentam o mesmo total.",
  };

  return known[code] ?? code.split("_").join(" ").toLocaleLowerCase("pt-BR");
}

function countProblemRows(rows: DeclaredBalanceRow[]): number {
  return rows.reduce((total, row) => {
    const current =
      row.reconciliation_status && row.reconciliation_status !== "CONCILIADA"
        ? 1
        : 0;
    return total + current + countProblemRows(row.children);
  }, 0);
}

function countDetailRows(rows: DeclaredBalanceRow[]): number {
  return rows.reduce((total, row) => {
    const current = row.aggregation_code_type === "D" ? 1 : 0;
    return total + current + countDetailRows(row.children);
  }, 0);
}

function rowMatches(row: DeclaredBalanceRow, query: string): boolean {
  const normalized = query.trim().toLocaleLowerCase("pt-BR");

  if (!normalized) {
    return true;
  }

  if (
    row.description.toLocaleLowerCase("pt-BR").includes(normalized) ||
    row.aggregation_code.toLocaleLowerCase("pt-BR").includes(normalized)
  ) {
    return true;
  }

  return row.children.some((child) => rowMatches(child, query));
}

function isBroadRoot(row: DeclaredBalanceRow): boolean {
  const name = normalizeText(row.description);

  return (
    name === "ATIVO" ||
    name === "PASSIVO" ||
    name === "PATRIMONIO LIQUIDO" ||
    name === "PASSIVO E PATRIMONIO LIQUIDO" ||
    name === "PASSIVO E PATRIMONIO SOCIAL"
  );
}

function compareRows(a: DeclaredBalanceRow, b: DeclaredBalanceRow): number {
  return a.line_number - b.line_number;
}

function collectDeepestSyntheticDescendants(row: DeclaredBalanceRow): DeclaredBalanceRow[] {
  return row.children.flatMap((child) => {
    if (child.aggregation_code_type !== "T") {
      return collectDeepestSyntheticDescendants(child);
    }

    const nestedSyntheticRows = collectDeepestSyntheticDescendants(child);

    if (nestedSyntheticRows.length > 0) {
      return nestedSyntheticRows;
    }

    return [child];
  });
}

function collectDetailsOutsideSyntheticBranches(row: DeclaredBalanceRow): DeclaredBalanceRow[] {
  return row.children.flatMap((child) => {
    if (child.aggregation_code_type === "T") {
      return [];
    }

    return [child, ...collectDetailsOutsideSyntheticBranches(child)];
  });
}

function collectPresentationRows(root: DeclaredBalanceRow): DashboardRow[] {
  const summaryRows = collectDeepestSyntheticDescendants(root);
  const rows =
    summaryRows.length > 0
      ? [
          ...summaryRows,
          ...collectDetailsOutsideSyntheticBranches(root),
        ].sort(compareRows)
      : root.children.length > 0
        ? root.children
        : [root];

  const uniqueRows = rows.filter(
    (row, index, allRows) =>
      allRows.findIndex((candidate) => candidate.aggregation_code === row.aggregation_code) ===
      index,
  );

  return uniqueRows.map((row) => ({
    row,
    depth: Math.max(0, row.aggregation_level - root.aggregation_level - 1),
  }));
}

function buildDashboardGroups(rows: DeclaredBalanceRow[], query: string): DashboardGroup[] {
  const groupRoots = rows.flatMap((root) => {
    if (isBroadRoot(root) && root.children.length > 0) {
      return root.children;
    }

    return [root];
  });

  return groupRoots.flatMap((root) => {
    if (!rowMatches(root, query)) {
      return [];
    }

    const side = root.balance_group === "A" ? "asset" : "liabilityEquity";
    const presentationRows = collectPresentationRows(root).filter(({ row }) =>
      rowMatches(row, query),
    );

    return [
      {
        id: root.aggregation_code,
        root,
        rows: presentationRows.length > 0 ? presentationRows : [{ row: root, depth: 0 }],
        side,
        title: root.description,
      },
    ];
  });
}

function lineStatusFor(row: DeclaredBalanceRow) {
  if (!row.reconciliation_status || row.reconciliation_status === "CONCILIADA") {
    return null;
  }

  return LINE_STATUS[row.reconciliation_status];
}

export function BalanceDashboardPage({
  analysisId,
  year,
  balance,
  isLoading,
  isError,
  onRetry,
}: BalanceDashboardPageProps) {
  const [selectedRow, setSelectedRow] = useState<SelectedRow | null>(null);
  const [components, setComponents] =
    useState<DeclaredBalanceComponentsResponse | null>(null);
  const [componentsLoading, setComponentsLoading] = useState(false);
  const [componentsError, setComponentsError] = useState(false);
  const [viewMode, setViewMode] = useState<ViewMode>("columns");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    if (!selectedRow) {
      return;
    }

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        closeComponents();
      }
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [selectedRow]);

  const grouped = useMemo(
    () => (balance ? buildDashboardGroups(balance.rows, searchQuery) : []),
    [balance, searchQuery],
  );

  const closeComponents = () => {
    setSelectedRow(null);
    setComponents(null);
    setComponentsError(false);
  };

  const openComponents = async (row: DeclaredBalanceRow) => {
    setSelectedRow({
      aggregationCode: row.aggregation_code,
      description: row.description,
      declaredAmount: row.final_amount,
      reconciledAmount: row.reconciled_amount,
      difference: row.difference,
      reconciliationStatus: row.reconciliation_status,
      componentCount: row.component_count,
    });
    setComponents(null);
    setComponentsError(false);
    setComponentsLoading(true);
    try {
      const result = await fetchDeclaredBalanceComponents(
        analysisId,
        year,
        row.aggregation_code,
      );
      setComponents(result);
    } catch {
      setComponentsError(true);
    } finally {
      setComponentsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <main className="app-content balance-dashboard-content">
        <section className="dashboard-section state-card">
          <h1>Balanço Patrimonial</h1>
          <p>Carregando balanço declarado da ECD.</p>
        </section>
      </main>
    );
  }

  if (isError || !balance) {
    return (
      <main className="app-content balance-dashboard-content">
        <section className="dashboard-section state-card" aria-live="polite">
          <h1>Erro ao carregar balanço patrimonial</h1>
          <p>Não foi possível consultar o balanço declarado para esta análise.</p>
          <button className="button-secondary" onClick={onRetry} type="button">
            Tentar novamente
          </button>
        </section>
      </main>
    );
  }

  const status = BALANCE_STATUS[balance.balance_status];
  const assetGroups = grouped.filter((group) => group.side === "asset");
  const liabilityEquityGroups = grouped.filter((group) => group.side === "liabilityEquity");
  const problemRows = countProblemRows(balance.rows);
  const totalDetails = countDetailRows(balance.rows);

  const renderAccountRows = (rows: DashboardRow[]) =>
    rows.map(({ row, depth }) => {
      const status = lineStatusFor(row);

      return (
        <AccountRow
          key={row.aggregation_code}
          accountName={row.description}
          accountCode={row.aggregation_code}
          value={row.final_amount}
          isIncluded
          showSwitch={false}
          depth={depth}
          isStructural={row.aggregation_code_type === "T"}
          statusLabel={status?.label}
          statusVariant={status?.variant}
          onToggleInclude={() => undefined}
          onAudit={() => openComponents(row)}
          isLedgerMode={viewMode === "ledger"}
        />
      );
    });

  const renderGroup = (group: DashboardGroup, globalTotal: string | null) => (
    <BalanceGroup
      key={group.id}
      groupName={group.title}
      accountCount={group.rows.length}
      totalValue={group.root.final_amount}
      onAuditGroup={() => openComponents(group.root)}
      isLedgerMode={viewMode === "ledger"}
      percentage={undefined}
    >
      {renderAccountRows(group.rows)}
      {globalTotal === null ? null : null}
    </BalanceGroup>
  );

  return (
    <>
      <header className="app-topbar">
        <div className="topbar-title-row">
          <h1 className="app-title">Balanço Patrimonial</h1>
          <p className="app-subtitle">
            Análise <span className="tnum">{analysisId}</span> · Exercício{" "}
            <span className="tnum">{year}</span>
          </p>
        </div>
        <div className="topbar-actions">
          <div className="search-input-wrap">
            <Search size={16} />
            <input
              type="text"
              placeholder="Buscar conta ou grupo..."
              className="search-input"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
            />
          </div>
          <Link
            to={`/analises/${analysisId}/exercicios/${year}/auditoria`}
            className="button-secondary"
          >
            <ClipboardCheck aria-hidden="true" size={16} />
            Auditoria
          </Link>
          <Link to="/importar-ecd" className="button-primary">
            <Upload aria-hidden="true" size={16} />
            Importar ECD
          </Link>
        </div>
      </header>

      <main className="app-content balance-dashboard-content">
        <section className="dashboard-section">
          <div className="section-header-compact">
            <h2 className="eyebrow">Indicadores Calculados</h2>
            {balance.is_blocking && (
              <span className="status-badge" data-variant="warning">
                Resultado anual indisponível
              </span>
            )}
          </div>

          <div className="indicators-grid">
            <StatCard
              label="Base declarada"
              value={status.label}
              hint={status.detail}
              variant={status.variant}
              icon={balance.balance_status === "VALIDO" ? CheckCircle2 : AlertTriangle}
            />
            <StatCard
              label="Ativo"
              value={
                balance.assets_final_amount === null
                  ? "N/D"
                  : formatCurrency(balance.assets_final_amount)
              }
              hint="Saldo final J100"
              variant="neutral"
              icon={Activity}
            />
            <StatCard
              label="Passivo + PL"
              value={
                balance.liabilities_and_equity_final_amount === null
                  ? "N/D"
                  : formatCurrency(balance.liabilities_and_equity_final_amount)
              }
              hint="Saldo final J100"
              variant="neutral"
              icon={Activity}
            />
            <StatCard
              label="Divergências"
              value={String(problemRows)}
              hint={`${totalDetails} linhas de detalhe J100`}
              variant={problemRows > 0 ? "warning" : "success"}
              icon={Activity}
            />
          </div>
        </section>

        <section className="declared-status-panel" aria-live="polite">
          <div className="declared-status-heading">
            {balance.balance_status === "VALIDO" ? (
              <CheckCircle2 aria-hidden="true" size={20} />
            ) : (
              <AlertTriangle aria-hidden="true" size={20} />
            )}
            <div>
              <span className="eyebrow">Base declarada</span>
              <div className="declared-status-title">
                <span className="status-badge" data-variant={status.variant}>
                  {status.label}
                </span>
                <span>{status.detail}</span>
              </div>
            </div>
          </div>
          <dl className="declared-status-meta">
            <div>
              <dt>Período J005</dt>
              <dd className="tnum">
                {formatPeriod(balance.j005_period_start)} a{" "}
                {formatPeriod(balance.j005_period_end)}
              </dd>
            </div>
            <div>
              <dt>Diferença dos lados</dt>
              <dd className="tnum">
                {balance.difference === null
                  ? "Não disponível"
                  : formatCurrency(balance.difference)}
              </dd>
            </div>
            <div>
              <dt>Resultado anual</dt>
              <dd>{balance.is_blocking ? "Indisponível" : "Disponível"}</dd>
            </div>
            <div>
              <dt>Divergências</dt>
              <dd className="tnum">{problemRows}</dd>
            </div>
          </dl>
        </section>

        {balance.limitations.length > 0 && (
          <section className="declared-limitations" aria-label="Limitações do balanço">
            <strong>Limitações identificadas</strong>
            <ul>
              {balance.limitations.map((limitation) => (
                <li key={limitation}>{limitationText(limitation)}</li>
              ))}
            </ul>
          </section>
        )}

        <section className="dashboard-section">
          <div className="balance-header-row">
            <h2 className="eyebrow">Balanço Patrimonial</h2>
            <SegmentedControl
              value={viewMode}
              onChange={(value) => setViewMode(value as ViewMode)}
              options={[
                { id: "columns", label: "Duas colunas", icon: Columns },
                { id: "ledger", label: "Livro-razão", icon: List },
              ]}
              aria-label="Modo de visualização do balanço"
            />
          </div>

          {balance.rows.length === 0 ? (
            <section className="state-card">
              <h2>Balanço declarado indisponível</h2>
              <p>Sem linhas J100 aplicáveis para apresentar.</p>
            </section>
          ) : viewMode === "columns" ? (
            <div className="balance-columns">
              <div className="balance-column">
                <div className="column-header">
                  <span className="eyebrow">Ativo</span>
                  <span className="column-total tnum">
                    {balance.assets_final_amount === null
                      ? "Não disponível"
                      : formatCurrency(balance.assets_final_amount)}
                  </span>
                </div>
                <h3 className="column-title">Ativo</h3>
                {assetGroups.map((group) =>
                  renderGroup(group, balance.assets_final_amount),
                )}
              </div>
              <div className="balance-column">
                <div className="column-header">
                  <span className="eyebrow">Passivo e patrimônio líquido</span>
                  <span className="column-total tnum">
                    {balance.liabilities_and_equity_final_amount === null
                      ? "Não disponível"
                      : formatCurrency(balance.liabilities_and_equity_final_amount)}
                  </span>
                </div>
                <h3 className="column-title">Passivo e PL</h3>
                {liabilityEquityGroups.map((group) =>
                  renderGroup(group, balance.liabilities_and_equity_final_amount),
                )}
              </div>
            </div>
          ) : (
            <BalanceLedger>
              <div className="ledger-section">
                <div className="column-header">
                  <span className="eyebrow">Ativo</span>
                  <span className="column-total tnum">
                    {balance.assets_final_amount === null
                      ? "Não disponível"
                      : formatCurrency(balance.assets_final_amount)}
                  </span>
                </div>
                {assetGroups.map((group) =>
                  renderGroup(group, balance.assets_final_amount),
                )}
              </div>
              <div className="ledger-section" style={{ marginTop: "var(--space-8)" }}>
                <div className="column-header">
                  <span className="eyebrow">Passivo e patrimônio líquido</span>
                  <span className="column-total tnum">
                    {balance.liabilities_and_equity_final_amount === null
                      ? "Não disponível"
                      : formatCurrency(balance.liabilities_and_equity_final_amount)}
                  </span>
                </div>
                {liabilityEquityGroups.map((group) =>
                  renderGroup(group, balance.liabilities_and_equity_final_amount),
                )}
              </div>
            </BalanceLedger>
          )}
        </section>
      </main>

      {selectedRow && (
        <div
          className="dialog-scrim"
          role="presentation"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeComponents();
            }
          }}
        >
          <section
            aria-labelledby="components-dialog-title"
            aria-modal="true"
            className="components-dialog"
            role="dialog"
          >
            <header className="components-dialog-header">
              <div>
                <h2 id="components-dialog-title">
                  Componentes — {selectedRow.description}
                </h2>
                <p className="tnum">
                  Código de aglutinação {selectedRow.aggregationCode}
                </p>
              </div>
              <button
                type="button"
                className="button-ghost dialog-close"
                aria-label="Fechar"
                onClick={closeComponents}
              >
                <X aria-hidden="true" size={18} />
              </button>
            </header>

            <div className="components-dialog-body">
              <dl className="component-summary">
                <div>
                  <dt>Valor declarado J100</dt>
                  <dd className="tnum">{formatCurrency(selectedRow.declaredAmount)}</dd>
                </div>
                <div>
                  <dt>Valor conciliado I155</dt>
                  <dd className="tnum">
                    {selectedRow.reconciledAmount === null
                      ? "Não disponível"
                      : formatCurrency(selectedRow.reconciledAmount)}
                  </dd>
                </div>
                <div>
                  <dt>Diferença</dt>
                  <dd className="tnum">
                    {selectedRow.difference === null
                      ? "Não disponível"
                      : formatCurrency(selectedRow.difference)}
                  </dd>
                </div>
                <div>
                  <dt>Status</dt>
                  <dd>
                    {selectedRow.reconciliationStatus
                      ? LINE_STATUS[selectedRow.reconciliationStatus].label
                      : "Não informado"}
                  </dd>
                </div>
              </dl>
              {componentsLoading && <p>Carregando componentes.</p>}
              {componentsError && (
                <p className="components-error">
                  Não foi possível consultar os componentes desta linha.
                </p>
              )}
              {!componentsLoading && !componentsError && components?.rows.length === 0 && (
                <p>
                  {selectedRow.reconciliationStatus === "SEM_I052"
                    ? "Nenhum vínculo I052 foi encontrado para este código de aglutinação. O CAPAG não consegue relacionar esta linha J100 às contas analíticas."
                    : "Sem registros."}
                </p>
              )}
              {!componentsLoading && !componentsError && components && components.rows.length > 0 && (
                <div className="components-table-wrap">
                  <table className="components-table">
                    <thead>
                      <tr>
                        <th>Conta</th>
                        <th>Centro de custo</th>
                        <th className="numeric">Saldo final</th>
                        <th>Origem</th>
                      </tr>
                    </thead>
                    <tbody>
                      {components.rows.map((component) => (
                        <tr
                          key={`${component.account_code}-${component.cost_center_code ?? ""}-${component.i052_line_number}`}
                        >
                          <td>
                            <strong>{component.account_name}</strong>
                            <span className="tnum">{component.account_code}</span>
                          </td>
                          <td className="tnum">
                            {component.cost_center_code ?? "Sem centro de custo"}
                          </td>
                          <td className="numeric tnum">
                            {component.final_amount === null
                              ? "Sem saldo I155"
                              : `${formatCurrency(component.final_amount)} ${component.final_debit_credit_indicator ?? ""}`}
                          </td>
                          <td className="component-source tnum">
                            I052 linha {component.i052_line_number}
                            <br />
                            {component.i155_line_number === null
                              ? "I155 ausente"
                              : `I155 linha ${component.i155_line_number}`}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            <footer className="components-dialog-footer">
              <button
                className="button-secondary"
                type="button"
                onClick={closeComponents}
              >
                Fechar
              </button>
            </footer>
          </section>
        </div>
      )}
    </>
  );
}
