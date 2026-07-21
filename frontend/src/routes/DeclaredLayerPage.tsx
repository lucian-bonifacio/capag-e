import {
  AlertTriangle,
  ChevronDown,
  ClipboardCheck,
  ListFilter,
  RefreshCcw,
} from "lucide-react";
import { useMemo, useState } from "react";

import type { DeclaredAccount, DeclaredLayerSummary } from "../api/declared";

type DeclaredLayerPageProps = {
  analysisId: string;
  year: string;
  summary?: DeclaredLayerSummary;
  accounts?: DeclaredAccount[];
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
};

type FilterId =
  | "all"
  | "linked"
  | "missing-link"
  | "missing-official"
  | "missing-rule"
  | "mapped"
  | "pending";

type AccountPresentation = DeclaredAccount & {
  displayKey: string;
  depth: number;
  isPending: boolean;
  isStructural: boolean;
};

const warningStatuses = new Set([
  "NAO_MAPEADO_METODOLOGICAMENTE",
  "COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL",
  "SEM_VINCULO_REFERENCIAL",
  "REGRA_EM_REVISAO",
]);

const dangerStatuses = new Set(["REGRA_BLOQUEADA", "REGRA_DEPRECIADA"]);

const pendingStatuses = new Set([
  ...warningStatuses,
  ...dangerStatuses,
  "EXCLUIDO_AUTOMATICAMENTE",
]);

const statusLabels: Record<string, string> = {
  MAPEADO: "Mapeada",
  NAO_MAPEADO_METODOLOGICAMENTE: "Sem regra",
  COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL: "Fora da base oficial",
  SEM_VINCULO_REFERENCIAL: "Sem vinculo",
  REGRA_BLOQUEADA: "Regra bloqueada",
  REGRA_EM_REVISAO: "Regra em revisao",
  REGRA_DEPRECIADA: "Regra depreciada",
  EXCLUIDO_AUTOMATICAMENTE: "Excluida",
  INCLUIDO_AUTOMATICAMENTE: "Incluida",
};

const recommendedActionLabels: Record<string, string> = {
  revisar_base_oficial: "Revisar base oficial",
  revisar_metodologia: "Revisar metodologia",
  revisar_vinculo_referencial: "Revisar vinculo referencial na ECD",
};

const filters: Array<{ id: FilterId; label: string }> = [
  { id: "all", label: "Todas" },
  { id: "linked", label: "Com vinculo" },
  { id: "missing-link", label: "Sem vinculo" },
  { id: "missing-official", label: "Codigo fora da base oficial" },
  { id: "missing-rule", label: "Sem regra" },
  { id: "mapped", label: "Mapeadas" },
  { id: "pending", label: "Pendencias" },
];

function badgeVariant(status: string): "success" | "warning" | "danger" | "neutral" {
  if (status === "MAPEADO" || status === "INCLUIDO_AUTOMATICAMENTE") {
    return "success";
  }

  if (dangerStatuses.has(status)) {
    return "danger";
  }

  if (warningStatuses.has(status) || status === "EXCLUIDO_AUTOMATICAMENTE") {
    return "warning";
  }

  return "neutral";
}

function statusLabel(status: string): string {
  return statusLabels[status] ?? status;
}

function actionLabel(action: string | null): string {
  if (!action) {
    return "Sem acao";
  }

  return recommendedActionLabels[action] ?? action.replace(/_/g, " ");
}

function actionShortLabel(action: string | null): string {
  return action ? "Revisar" : "Sem acao";
}

function toMinorUnits(value: string): bigint {
  const normalized = value.trim().replace(",", ".");
  const negative = normalized.startsWith("-");
  const unsigned = normalized.replace(/^-/, "");
  const [integerPart = "0", decimalPart = ""] = unsigned.split(".");
  const cents = `${integerPart.replace(/\D/g, "") || "0"}${decimalPart.padEnd(2, "0").slice(0, 2)}`;
  const amount = BigInt(cents || "0");
  return negative ? -amount : amount;
}

function absMinorUnits(value: string): bigint {
  const amount = toMinorUnits(value);
  return amount < 0n ? -amount : amount;
}

function accountDepth(accountCode: string): number {
  return accountCode ? 0 : 0;
}

function compareAccountCode(a: AccountPresentation, b: AccountPresentation): number {
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

function buildPresentation(account: DeclaredAccount, index: number): AccountPresentation {
  const materiality = absMinorUnits(account.base_value);
  const hasNoValue = materiality === 0n && absMinorUnits(account.considered_value) === 0n;
  const depth = account.account_level === null ? accountDepth(account.account_code) : account.account_level - 1;

  return {
    ...account,
    displayKey: `${account.account_code}-${account.purpose ?? "sem-finalidade"}-${index}`,
    depth: Math.max(0, Math.min(depth, 5)),
    isPending: pendingStatuses.has(account.final_status),
    isStructural: account.account_type === "S" || hasNoValue,
  };
}

function matchesFilter(account: AccountPresentation, filter: FilterId): boolean {
  if (filter === "all") {
    return true;
  }

  if (filter === "linked") {
    return Boolean(account.declared_reference_code);
  }

  if (filter === "missing-link") {
    return account.final_status === "SEM_VINCULO_REFERENCIAL";
  }

  if (filter === "missing-official") {
    return account.final_status === "COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL";
  }

  if (filter === "missing-rule") {
    return account.final_status === "NAO_MAPEADO_METODOLOGICAMENTE";
  }

  if (filter === "mapped") {
    return account.final_status === "MAPEADO";
  }

  return account.isPending;
}

function StatusBadge({ status }: { status: string }) {
  return (
    <span className="status-badge" data-variant={badgeVariant(status)} title={status}>
      {statusLabel(status)}
    </span>
  );
}

function SummaryCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint?: string;
}) {
  return (
    <article className="summary-card">
      <p className="eyebrow">{label}</p>
      <strong className="summary-value tnum">{value}</strong>
      {hint ? <span>{hint}</span> : null}
    </article>
  );
}

function LoadingState() {
  return (
    <section className="declared-card" aria-label="Carregando camada declarada">
      <div className="skeleton-row" />
      <div className="skeleton-row skeleton-row-short" />
      <div className="skeleton-table" />
    </section>
  );
}

function ErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <section className="declared-card state-card" aria-live="polite">
      <AlertTriangle aria-hidden="true" size={18} />
      <div>
        <h2>Erro ao carregar camada declarada</h2>
        <p>Não foi possível consultar os snapshots declarados para esta análise.</p>
      </div>
      <button className="button-secondary" onClick={onRetry} type="button">
        <RefreshCcw aria-hidden="true" size={16} />
        Recarregar
      </button>
    </section>
  );
}

function EmptyState() {
  return (
    <section className="declared-card state-card">
      <ClipboardCheck aria-hidden="true" size={18} />
      <div>
        <h2>Sem registros.</h2>
        <p>A camada declarada ainda não possui contas persistidas para o exercício.</p>
      </div>
    </section>
  );
}

function AccountDetail({ account }: { account: AccountPresentation }) {
  return (
    <div className="account-detail">
      <section aria-label="Declaração ECD">
        <p className="eyebrow">Declaracao ECD</p>
        <dl>
          <div>
            <dt>I050</dt>
            <dd>
              <span className="tnum">{account.account_code}</span> · {account.account_name}
            </dd>
          </div>
          <div>
            <dt>I051</dt>
            <dd className="tnum">{account.declared_reference_code ?? "sem vinculo"}</dd>
          </div>
          <div>
            <dt>I155</dt>
            <dd className="tnum">{account.base_value}</dd>
          </div>
        </dl>
      </section>

      <section aria-label="Cobertura metodológica">
        <p className="eyebrow">Cobertura metodologica</p>
        <dl>
          <div>
            <dt>Status tecnico</dt>
            <dd className="tnum">{account.final_status}</dd>
          </div>
          <div>
            <dt>Plano oficial</dt>
            <dd>{account.official_description ?? "sem descricao oficial"}</dd>
          </div>
          <div>
            <dt>Regra</dt>
            <dd className="tnum">{account.methodology_rule_applied ?? "sem regra"}</dd>
          </div>
          <div>
            <dt>Tratamento</dt>
            <dd>{account.treatment ?? "sem tratamento"}</dd>
          </div>
          <div>
            <dt>Acao recomendada</dt>
            <dd>{actionLabel(account.recommended_action)}</dd>
          </div>
        </dl>
        {account.observation ? <p className="detail-note">{account.observation}</p> : null}
      </section>
    </div>
  );
}

function AccountRow({ account }: { account: AccountPresentation }) {
  return (
    <details
      className={`account-row account-depth-${account.depth}`}
      data-structural={account.isStructural}
    >
      <summary>
        <span className="account-cell account-cell-main ledger-cell-account">
          <ChevronDown aria-hidden="true" size={16} />
          <span>
            <strong>{account.account_name}</strong>
            <small className="tnum">{account.account_code}</small>
          </span>
        </span>
        <span className="account-cell tnum">
          <span className="tnum">{account.declared_reference_code ?? "sem vinculo"}</span>
        </span>
        <span className="account-cell">
          <StatusBadge status={account.final_status} />
        </span>
        <span className="account-cell ledger-cell-muted">
          {account.official_description ?? "sem descricao oficial"}
        </span>
        <span className="account-cell numeric">
          <span className="tnum">{account.base_value}</span>
        </span>
        <span className="account-cell numeric">
          <span className="tnum">{account.considered_value}</span>
        </span>
        <span className="account-cell ledger-cell-muted">
          {actionShortLabel(account.recommended_action)}
        </span>
      </summary>
      <AccountDetail account={account} />
    </details>
  );
}

export function DeclaredLayerPage({
  analysisId,
  year,
  summary,
  accounts = [],
  isLoading,
  isError,
  onRetry,
}: DeclaredLayerPageProps) {
  const [activeFilter, setActiveFilter] = useState<FilterId>("all");

  const statusEntries = useMemo(
    () => Object.entries(summary?.status_counts ?? {}).sort(([a], [b]) => a.localeCompare(b)),
    [summary?.status_counts],
  );

  const presentedAccounts = useMemo(
    () => accounts.map(buildPresentation).sort(compareAccountCode),
    [accounts],
  );

  const filteredAccounts = useMemo(
    () => presentedAccounts.filter((account) => matchesFilter(account, activeFilter)),
    [activeFilter, presentedAccounts],
  );

  const structuralCount = presentedAccounts.filter((account) => account.isStructural).length;
  const analyticalCount = presentedAccounts.length - structuralCount;
  const pendingCount = presentedAccounts.filter((account) => account.isPending).length;
  const linkedCount = presentedAccounts.filter((account) => account.declared_reference_code).length;

  return (
    <>
      <header className="app-topbar">
        <div>
          <h1 className="app-title">Camada Declarada</h1>
          <p className="app-subtitle">
            Análise <span className="tnum">{analysisId}</span> · Exercício{" "}
            <span className="tnum">{year}</span>
          </p>
        </div>
        <span className="app-status">Leitura ECD</span>
      </header>

      <main className="app-content declared-content">
        {isLoading ? <LoadingState /> : null}
        {isError ? <ErrorState onRetry={onRetry} /> : null}

        {!isLoading && !isError && summary ? (
          <>
            <section className="summary-grid summary-grid-wide" aria-label="Resumo da camada declarada">
              <SummaryCard
                label="Contas"
                value={String(summary.total_accounts)}
                hint={`${analyticalCount} analiticas · ${structuralCount} estruturais`}
              />
              <SummaryCard
                label="Vinculos I051"
                value={String(linkedCount)}
                hint="contas com referencial declarado"
              />
              <SummaryCard
                label="Pendencias"
                value={String(pendingCount)}
                hint="itens que exigem revisao"
              />
              <SummaryCard
                label="Versao"
                value={summary.methodology_version_id ?? "sem versao"}
                hint="metodologia aplicada"
              />
            </section>

            <section className="declared-card">
              <div className="section-header">
                <div>
                  <p className="eyebrow">Diagnostico declaratorio</p>
                  <h2>Resumo acionavel</h2>
                </div>
                <button className="button-secondary" onClick={() => setActiveFilter("pending")} type="button">
                  <ListFilter aria-hidden="true" size={16} />
                  Pendencias
                </button>
              </div>

              {statusEntries.length > 0 ? (
                <div className="status-list">
                  {statusEntries.map(([status, count]) => (
                    <button
                      className="status-list-item"
                      key={status}
                      onClick={() => {
                        if (status === "MAPEADO") setActiveFilter("mapped");
                        else if (status === "SEM_VINCULO_REFERENCIAL") setActiveFilter("missing-link");
                        else if (status === "COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL") {
                          setActiveFilter("missing-official");
                        } else if (status === "NAO_MAPEADO_METODOLOGICAMENTE") setActiveFilter("missing-rule");
                        else setActiveFilter("pending");
                      }}
                      type="button"
                    >
                      <StatusBadge status={status} />
                      <span className="tnum">{count}</span>
                    </button>
                  ))}
                </div>
              ) : (
                <p className="muted-text">Sem registros.</p>
              )}
            </section>

            {accounts.length === 0 ? (
              <EmptyState />
            ) : (
              <section className="declared-card declared-ledger-card">
                <div className="section-header">
                  <div>
                    <p className="eyebrow">Contas declaradas</p>
                    <h2>Leitura declarada por conta</h2>
                  </div>
                </div>

                <div className="filter-bar" aria-label="Filtros da leitura declarada">
                  {filters.map((filter) => (
                    <button
                      aria-pressed={activeFilter === filter.id}
                      className="filter-pill"
                      data-active={activeFilter === filter.id}
                      key={filter.id}
                      onClick={() => setActiveFilter(filter.id)}
                      type="button"
                    >
                      {filter.label}
                    </button>
                  ))}
                </div>

                {filteredAccounts.length > 0 ? (
                  <div className="balance-ledger">
                    <div className="ledger-header" aria-hidden="true">
                      <span>Conta</span>
                      <span>Referencial ECD</span>
                      <span>Status</span>
                      <span>Descricao oficial</span>
                      <span>Valor base</span>
                      <span>Valor considerado</span>
                      <span>Acao</span>
                    </div>
                    <div className="account-ledger account-ledger-standalone">
                      {filteredAccounts.map((account) => (
                        <AccountRow account={account} key={account.displayKey} />
                      ))}
                    </div>
                  </div>
                ) : (
                  <p className="muted-text">Nenhuma conta encontrada para o filtro selecionado.</p>
                )}
              </section>
            )}
          </>
        ) : null}
      </main>
    </>
  );
}
