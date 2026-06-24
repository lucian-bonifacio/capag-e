import { AlertTriangle, ClipboardCheck, RefreshCcw } from "lucide-react";
import { useMemo } from "react";

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

const warningStatuses = new Set([
  "NAO_MAPEADO_METODOLOGICAMENTE",
  "COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL",
  "SEM_VINCULO_REFERENCIAL",
  "REGRA_EM_REVISAO",
]);

const dangerStatuses = new Set(["REGRA_BLOQUEADA", "REGRA_DEPRECIADA"]);

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

function StatusBadge({ status }: { status: string }) {
  return (
    <span className="status-badge" data-variant={badgeVariant(status)}>
      {status}
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

export function DeclaredLayerPage({
  analysisId,
  year,
  summary,
  accounts = [],
  isLoading,
  isError,
  onRetry,
}: DeclaredLayerPageProps) {
  const statusEntries = useMemo(
    () => Object.entries(summary?.status_counts ?? {}).sort(([a], [b]) => a.localeCompare(b)),
    [summary?.status_counts],
  );

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
            <section className="summary-grid" aria-label="Resumo da camada declarada">
              <SummaryCard
                label="Contas"
                value={String(summary.accounts_count)}
                hint="snapshot declarado"
              />
              <SummaryCard
                label="Versão"
                value={summary.methodology_version_id ?? "sem versão"}
                hint="metodologia aplicada"
              />
              <SummaryCard
                label="Status"
                value={String(statusEntries.length)}
                hint="categorias retornadas"
              />
            </section>

            <section className="declared-card">
              <div className="section-header">
                <div>
                  <p className="eyebrow">Status Metodológico</p>
                  <h2>Distribuição por conta</h2>
                </div>
              </div>

              {statusEntries.length > 0 ? (
                <div className="status-list">
                  {statusEntries.map(([status, count]) => (
                    <div className="status-list-item" key={status}>
                      <StatusBadge status={status} />
                      <span className="tnum">{count}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="muted-text">Sem registros.</p>
              )}
            </section>

            {accounts.length === 0 ? (
              <EmptyState />
            ) : (
              <section className="declared-card declared-table-card">
                <div className="section-header">
                  <div>
                    <p className="eyebrow">Contas Declaradas</p>
                    <h2>Classificação recebida da API</h2>
                  </div>
                </div>

                <div className="table-scroll">
                  <table className="declared-table">
                    <thead>
                      <tr>
                        <th>Conta</th>
                        <th>Referencial ECD</th>
                        <th>Descrição oficial</th>
                        <th>Metodologia</th>
                        <th>Status</th>
                        <th>Valor base</th>
                        <th>Valor considerado</th>
                        <th>Ação</th>
                      </tr>
                    </thead>
                    <tbody>
                      {accounts.map((account) => (
                        <tr key={`${account.account_code}-${account.purpose ?? "sem-finalidade"}`}>
                          <td>
                            <strong className="tnum">{account.account_code}</strong>
                            <span>{account.account_name}</span>
                          </td>
                          <td className="tnum">{account.declared_reference_code ?? "sem vínculo"}</td>
                          <td>{account.official_description ?? "sem descrição oficial"}</td>
                          <td>
                            <span>{account.methodology_rule_applied ?? "sem regra"}</span>
                            <small>{account.treatment ?? "sem tratamento"}</small>
                          </td>
                          <td>
                            <StatusBadge status={account.final_status} />
                          </td>
                          <td className="tnum numeric">{account.base_value}</td>
                          <td className="tnum numeric">{account.considered_value}</td>
                          <td>{account.recommended_action ?? "Sem ação"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}
          </>
        ) : null}
      </main>
    </>
  );
}
