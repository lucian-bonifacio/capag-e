import { useMemo, useState } from "react";
import { Activity, ClipboardCheck, Columns, List, Search, Upload } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import type {
  DeclaredAccount,
  DeclaredBalanceConsistencyWarning,
  DeclaredLayerSummary,
} from "../api/declared";
import { StatCard } from "../components/dashboard/StatCard";
import { SegmentedControl } from "../components/dashboard/SegmentedControl";
import { BalanceGroup } from "../components/dashboard/BalanceGroup";
import { AccountRow } from "../components/dashboard/AccountRow";
import { BalanceLedger } from "../components/dashboard/BalanceLedger";
import { decimalToMinorUnits, formatCurrency } from "../lib/formatters";
import "./BalanceDashboardPage.css";

type BalanceDashboardPageProps = {
  analysisId: string;
  year: string;
  summary?: DeclaredLayerSummary;
  accounts?: DeclaredAccount[];
  consistencyWarnings?: DeclaredBalanceConsistencyWarning[];
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
};

type AccountNode = {
  account: DeclaredAccount;
  children: AccountNode[];
  parent: AccountNode | null;
};

type DashboardRow = {
  account: DeclaredAccount;
  amount: bigint;
};

type DashboardGroup = {
  id: string;
  title: string;
  root: DeclaredAccount;
  rows: DashboardRow[];
  side: "asset" | "liabilityEquity";
};

function normalizeText(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toUpperCase();
}

function compareAccounts(a: DeclaredAccount, b: DeclaredAccount): number {
  if (a.account_order !== null && b.account_order !== null) {
    return a.account_order - b.account_order;
  }

  if (a.account_order !== null) {
    return -1;
  }

  if (b.account_order !== null) {
    return 1;
  }

  return a.account_code.localeCompare(b.account_code, "pt-BR", {
    numeric: true,
    sensitivity: "base",
  });
}

function buildAccountTree(accounts: DeclaredAccount[]): AccountNode[] {
  const nodes = new Map<string, AccountNode>();

  accounts.forEach((account) => {
    nodes.set(account.account_code, { account, children: [], parent: null });
  });

  const roots: AccountNode[] = [];

  nodes.forEach((node) => {
    const parent = node.account.parent_account_code
      ? nodes.get(node.account.parent_account_code)
      : undefined;

    if (parent) {
      node.parent = parent;
      parent.children.push(node);
      return;
    }

    roots.push(node);
  });

  const sortNode = (node: AccountNode) => {
    node.children.sort((a, b) => compareAccounts(a.account, b.account));
    node.children.forEach(sortNode);
  };

  roots.sort((a, b) => compareAccounts(a.account, b.account));
  roots.forEach(sortNode);

  return roots;
}

function accountAmount(account: DeclaredAccount): bigint {
  return decimalToMinorUnits(account.base_value);
}

function collectDescendants(node: AccountNode): AccountNode[] {
  return node.children.flatMap((child) => [child, ...collectDescendants(child)]);
}

function isSyntheticNode(node: AccountNode): boolean {
  return node.account.account_type === "S";
}

function collectDeepestSyntheticDescendants(node: AccountNode): AccountNode[] {
  return node.children.flatMap((child) => {
    if (!isSyntheticNode(child)) {
      return collectDeepestSyntheticDescendants(child);
    }

    const nestedSyntheticRows = collectDeepestSyntheticDescendants(child);

    if (nestedSyntheticRows.length > 0) {
      return nestedSyntheticRows;
    }

    return [child];
  });
}

function collectAnalyticalRowsOutsideSyntheticBranches(node: AccountNode): AccountNode[] {
  return node.children.flatMap((child) => {
    if (isSyntheticNode(child)) {
      return [];
    }

    return [child, ...collectAnalyticalRowsOutsideSyntheticBranches(child)];
  });
}

function sumAnalyticalDescendants(node: AccountNode): bigint {
  return collectDescendants(node).reduce((acc, curr) => {
    if (curr.account.account_type === "S") {
      return acc;
    }

    return acc + accountAmount(curr.account);
  }, 0n);
}

function presentationAmount(node: AccountNode): bigint {
  const ownAmount = accountAmount(node.account);

  if (ownAmount !== 0n || !isSyntheticNode(node)) {
    return ownAmount;
  }

  return sumAnalyticalDescendants(node);
}

function collectPresentationRows(node: AccountNode): DashboardRow[] {
  const summaryRows = collectDeepestSyntheticDescendants(node);

  const presentationNodes =
    summaryRows.length === 0
      ? collectDescendants(node)
      : [
          ...summaryRows,
          ...collectAnalyticalRowsOutsideSyntheticBranches(node),
        ].sort((a, b) => compareAccounts(a.account, b.account));

  return presentationNodes.map((presentationNode) => ({
    account: presentationNode.account,
    amount: presentationAmount(presentationNode),
  }));
}

function isBroadRoot(account: DeclaredAccount): boolean {
  const name = normalizeText(account.account_name);

  return (
    name === "ATIVO" ||
    name === "PASSIVO" ||
    name === "PATRIMONIO LIQUIDO" ||
    name === "PASSIVO E PATRIMONIO LIQUIDO" ||
    name === "PASSIVO E PATRIMONIO SOCIAL"
  );
}

function isEquityResultNode(node: AccountNode): boolean {
  return node.account.account_nature === "04";
}

function isBalanceSheetNode(node: AccountNode): boolean {
  return !isEquityResultNode(node);
}

function sideForNode(node: AccountNode): DashboardGroup["side"] | null {
  let current: AccountNode | null = node;

  while (current?.parent) {
    current = current.parent;
  }

  const rootNature = current?.account.account_nature ?? node.account.account_nature;

  if (rootNature === "01") {
    return "asset";
  }

  if (rootNature === "02" || rootNature === "03") {
    return "liabilityEquity";
  }

  const rootName = normalizeText(current?.account.account_name ?? node.account.account_name);
  const nodeName = normalizeText(node.account.account_name);

  if (rootName.includes("ATIVO") || nodeName.startsWith("ATIVO")) {
    return "asset";
  }

  if (
    rootName.includes("PASSIVO") ||
    rootName.includes("PATRIMONIO") ||
    nodeName.startsWith("PASSIVO") ||
    nodeName.startsWith("PATRIMONIO")
  ) {
    return "liabilityEquity";
  }

  return null;
}

function buildDashboardGroups(accounts: DeclaredAccount[]): DashboardGroup[] {
  const roots = buildAccountTree(accounts);
  const groupNodes = roots.flatMap((root) => {
    if (isBroadRoot(root.account) && root.children.length > 0) {
      return root.children;
    }

    return [root];
  });

  return groupNodes.flatMap((node) => {
    if (!isBalanceSheetNode(node)) {
      return [];
    }

    const side = sideForNode(node);

    if (side === null) {
      return [];
    }

    const presentationRows = collectPresentationRows(node);
    const rows =
      presentationRows.length > 0
        ? presentationRows
        : [{ account: node.account, amount: presentationAmount(node) }];

    return [{
      id: node.account.account_code,
      root: node.account,
      rows,
      side,
      title: node.account.account_name,
    }];
  });
}

function sumRows(rows: DashboardRow[], included: Record<string, boolean>): bigint {
  return rows.reduce((acc, curr) => {
    const isIncluded = included[curr.account.account_code] ?? true;

    if (!isIncluded) {
      return acc;
    }

    return acc + curr.amount;
  }, 0n);
}

function groupTotal(group: DashboardGroup, included: Record<string, boolean>): bigint {
  const rootAmount = accountAmount(group.root);

  if (rootAmount !== 0n) {
    return rootAmount;
  }

  return sumRows(group.rows, included);
}

function percentageOf(amount: bigint, total: bigint): number {
  if (total <= 0n) {
    return 0;
  }

  return Number((amount * 1000n) / total) / 10;
}

export function BalanceDashboardPage({
  analysisId,
  year,
  summary,
  accounts = [],
  consistencyWarnings = [],
  isLoading,
  isError,
  onRetry,
}: BalanceDashboardPageProps) {
  const navigate = useNavigate();
  const [viewMode, setViewMode] = useState("columns");
  const [includedAccounts, setIncludedAccounts] = useState<Record<string, boolean>>({});

  const toggleInclude = (code: string, isIncluded: boolean) => {
    setIncludedAccounts((prev) => ({ ...prev, [code]: isIncluded }));
  };

  const grouped = useMemo(() => buildDashboardGroups(accounts), [accounts]);
  const assetGroups = grouped.filter((group) => group.side === "asset");
  const liabilityEquityGroups = grouped.filter((group) => group.side === "liabilityEquity");
  const totalAssets = assetGroups.reduce(
    (acc, group) => acc + groupTotal(group, includedAccounts),
    0n,
  );
  const totalLiabilityEquity = liabilityEquityGroups.reduce(
    (acc, group) => acc + groupTotal(group, includedAccounts),
    0n,
  );
  const balanceDifference = totalAssets - totalLiabilityEquity;
  const visibleConsistencyWarnings = consistencyWarnings.slice(0, 6);

  const renderAccountRows = (rows: DashboardRow[], totalGroup: bigint) => {
    return rows.map(({ account: acc, amount }) => {
      const percentage = percentageOf(amount, totalGroup);
      const isIncluded = includedAccounts[acc.account_code] ?? true;
      const groupLevel = rows[0]?.account.account_level ?? acc.account_level ?? 1;
      const depth = Math.max(0, (acc.account_level ?? groupLevel) - groupLevel);

      return (
        <AccountRow
          key={acc.account_code}
          accountName={acc.account_name}
          accountCode={acc.account_code}
          value={amount}
          percentage={percentage}
          isIncluded={isIncluded}
          depth={depth}
          isStructural={acc.account_type === "S"}
          onToggleInclude={(inc) => toggleInclude(acc.account_code, inc)}
          onAudit={() => navigate(`/analises/${analysisId}/exercicios/${year}/auditoria`)}
          isLedgerMode={viewMode === "ledger"}
        />
      );
    });
  };

  const renderGroup = (group: DashboardGroup, globalTotal: bigint) => {
    const total = groupTotal(group, includedAccounts);
    const percentage = percentageOf(total, globalTotal);

    return (
      <BalanceGroup
        groupName={group.title}
        accountCount={group.rows.length}
        totalValue={total}
        percentage={percentage}
        onAuditGroup={() => navigate(`/analises/${analysisId}/exercicios/${year}/auditoria`)}
        isLedgerMode={viewMode === "ledger"}
      >
        {renderAccountRows(group.rows, total)}
      </BalanceGroup>
    );
  };

  const excludedCount = accounts.filter((account) => includedAccounts[account.account_code] === false).length;

  if (isLoading) {
    return (
      <main className="app-content balance-dashboard-content">
        <section className="dashboard-section state-card">
          <h1>Balanço Patrimonial</h1>
          <p>Carregando contas declaradas da ECD.</p>
        </section>
      </main>
    );
  }

  if (isError) {
    return (
      <main className="app-content balance-dashboard-content">
        <section className="dashboard-section state-card" aria-live="polite">
          <h1>Erro ao carregar balanço patrimonial</h1>
          <p>Não foi possível consultar as contas declaradas para esta análise.</p>
          <button className="button-secondary" onClick={onRetry} type="button">
            Tentar novamente
          </button>
        </section>
      </main>
    );
  }

  if (accounts.length === 0) {
    return (
      <main className="app-content balance-dashboard-content">
        <section className="dashboard-section state-card">
          <h1>Balanço Patrimonial</h1>
          <p>Sem contas declaradas para montar a hierarquia da ECD.</p>
        </section>
      </main>
    );
  }

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
            <input type="text" placeholder="Buscar conta ou grupo..." className="search-input" />
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
            {excludedCount > 0 && (
              <span className="status-badge" data-variant="warning">
                {excludedCount} {excludedCount === 1 ? "conta excluída" : "contas excluídas"} dos cálculos
              </span>
            )}
          </div>

          <div className="indicators-grid">
            <StatCard
              label="Indicador CAPAG"
              value="B"
              hint="Capacidade de pagamento boa"
              variant="success"
              icon={Activity}
            />
            <StatCard
              label="Liquidez Corrente"
              value="1,84"
              hint="Meta ≥ 1,00"
              variant="neutral"
              icon={Activity}
            />
            <StatCard
              label="Endividamento"
              value="42,6%"
              hint="Dívida / RCL"
              variant="warning"
              icon={Activity}
            />
            <StatCard
              label="Poupança Corrente"
              value="11,2%"
              hint="Resultado corrente positivo"
              variant="primary"
              icon={Activity}
            />
          </div>
        </section>

        <section className="dashboard-section">
          <div className="balance-header-row">
            <h2 className="eyebrow">Balanço Patrimonial</h2>
            <SegmentedControl
              value={viewMode}
              onChange={setViewMode}
              options={[
                { id: "columns", label: "Duas colunas", icon: Columns },
                { id: "ledger", label: "Livro-razão", icon: List },
              ]}
              aria-label="Modo de visualização do balanço"
            />
          </div>

          {viewMode === "columns" ? (
            <div className="balance-columns">
              <div className="balance-column">
                <div className="column-header">
                  <span className="eyebrow">Ativo</span>
                  <span className="column-total tnum">{formatCurrency(totalAssets)}</span>
                </div>
                <h3 className="column-title">Ativo</h3>
                {assetGroups.map((group) => (
                  <div key={group.id}>{renderGroup(group, totalAssets)}</div>
                ))}
              </div>
              <div className="balance-column">
                <div className="column-header">
                  <span className="eyebrow">Passivo e patrimônio líquido</span>
                  <span className="column-total tnum">{formatCurrency(totalLiabilityEquity)}</span>
                </div>
                <h3 className="column-title">Passivo e PL</h3>
                {liabilityEquityGroups.map((group) => (
                  <div key={group.id}>{renderGroup(group, totalLiabilityEquity)}</div>
                ))}
              </div>
            </div>
          ) : (
            <BalanceLedger>
              <div className="ledger-section">
                <div className="column-header">
                  <span className="eyebrow">Ativo</span>
                  <span className="column-total tnum">{formatCurrency(totalAssets)}</span>
                </div>
                {assetGroups.map((group) => (
                  <div key={group.id}>{renderGroup(group, totalAssets)}</div>
                ))}
              </div>
              <div className="ledger-section" style={{ marginTop: "var(--space-8)" }}>
                <div className="column-header">
                  <span className="eyebrow">Passivo e patrimônio líquido</span>
                  <span className="column-total tnum">{formatCurrency(totalLiabilityEquity)}</span>
                </div>
                {liabilityEquityGroups.map((group) => (
                  <div key={group.id}>{renderGroup(group, totalLiabilityEquity)}</div>
                ))}
              </div>
            </BalanceLedger>
          )}

          {balanceDifference !== 0n && (
            <div className="balance-alert" role="status">
              <strong>Balanço não fecha.</strong>
              <span>
                Diferença entre Ativo e Passivo + Patrimônio Líquido:{" "}
                <span className="tnum">{formatCurrency(balanceDifference)}</span>.
              </span>
            </div>
          )}

          {consistencyWarnings.length > 0 && (
            <div className="balance-consistency-panel" role="status">
              <div className="balance-consistency-header">
                <strong>Consistência J100 x I050</strong>
                <span className="status-badge" data-variant="warning">
                  {consistencyWarnings.length}{" "}
                  {consistencyWarnings.length === 1 ? "apontamento" : "apontamentos"}
                </span>
              </div>
              <ul className="balance-consistency-list">
                {visibleConsistencyWarnings.map((warning) => (
                  <li key={`${warning.warning_code}-${warning.account_code}`}>
                    <span className="tnum">{warning.account_code}</span>
                    <span>{warning.account_name}</span>
                    <small>{warning.message}</small>
                  </li>
                ))}
              </ul>
              {consistencyWarnings.length > visibleConsistencyWarnings.length && (
                <span className="balance-consistency-more">
                  +{consistencyWarnings.length - visibleConsistencyWarnings.length}{" "}
                  {consistencyWarnings.length - visibleConsistencyWarnings.length === 1
                    ? "apontamento"
                    : "apontamentos"}
                </span>
              )}
            </div>
          )}
        </section>
      </main>
    </>
  );
}
