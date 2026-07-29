import {
  AlertCircle,
  AlertTriangle,
  Ban,
  Calculator,
  ClipboardCheck,
  Download,
  RefreshCcw,
  Scale,
  X,
} from "lucide-react";

import type { ComponentStatus } from "../api/capag";
import type { PlraAudit, PlraAuditRow, PlraCalculation } from "../api/plra";
import { plraExportUrl } from "../api/plra";
import { formatCurrency } from "../lib/formatters";
import "./PlraPage.css";

type PlraPageProps = {
  analysisId: string;
  year: string;
  calculation?: PlraCalculation;
  audit?: PlraAudit;
  errorMessage?: string;
  errorStatus?: number;
  isAuditError: boolean;
  isAuditLoading: boolean;
  isAuditOpen: boolean;
  isError: boolean;
  isLoading: boolean;
  isRunning: boolean;
  onAuditClose: () => void;
  onAuditOpen: () => void;
  onRetry: () => void;
  onRun: () => void;
};

type BadgeVariant = "success" | "warning" | "danger" | "neutral";

const statusLabels: Record<ComponentStatus, string> = {
  nao_calculado: "Não calculado",
  calculado: "Calculado",
  parcial: "Parcial",
  bloqueado_por_pendencia: "Bloqueado por pendência",
  bloqueado_por_evidencia: "Bloqueado por evidência",
  erro_metodologico: "Erro metodológico",
};

const inclusionLabels: Record<PlraAuditRow["inclusion_status"], string> = {
  incluido_ativo: "Ativo incluído",
  incluido_passivo: "Passivo incluído",
  excluido: "Excluída",
  pendente: "Pendente",
  ignorado_hierarquia: "Fora por hierarquia",
  sem_vinculo_referencial: "Sem vínculo",
  nao_patrimonial: "Não patrimonial",
};

function statusVariant(status: ComponentStatus): BadgeVariant {
  if (status === "calculado") return "success";
  if (status === "parcial" || status === "nao_calculado") return "warning";
  return "danger";
}

function StatusBadge({ status }: { status: ComponentStatus }) {
  return (
    <span className="status-badge" data-variant={statusVariant(status)}>
      {statusLabels[status]}
    </span>
  );
}

function SummaryItem({ label, value }: { label: string; value: string }) {
  return (
    <article className="plra-summary-item">
      <span>{label}</span>
      <strong className="tnum">{formatCurrency(value)}</strong>
    </article>
  );
}

function MessageSection({
  icon: Icon,
  items,
  title,
  tone,
}: {
  icon: typeof AlertCircle;
  items: string[];
  title: string;
  tone: "danger" | "warning" | "neutral";
}) {
  return (
    <section className="plra-message-section" data-tone={tone}>
      <div className="plra-message-heading">
        <Icon aria-hidden="true" size={18} />
        <h2>{title}</h2>
        <span className="tnum">{items.length}</span>
      </div>
      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>Sem registros.</p>
      )}
    </section>
  );
}

function LoadingState() {
  return (
    <section aria-label="Carregando PLRA" className="app-panel plra-state">
      <div className="skeleton-row" />
      <div className="skeleton-row skeleton-row-short" />
      <div className="skeleton-table plra-skeleton" />
    </section>
  );
}

function EmptyState({ isRunning, onRun }: Pick<PlraPageProps, "isRunning" | "onRun">) {
  return (
    <section className="app-panel plra-state">
      <Calculator aria-hidden="true" size={24} />
      <div>
        <h2>PLRA não calculado</h2>
        <p>Não há snapshot persistido para este exercício.</p>
        <button
          className="button-primary"
          disabled={isRunning}
          onClick={onRun}
          type="button"
        >
          <Calculator aria-hidden="true" size={16} />
          {isRunning ? "Calculando..." : "Calcular PLRA"}
        </button>
      </div>
    </section>
  );
}

function ErrorState({
  message,
  onRetry,
}: {
  message?: string;
  onRetry: () => void;
}) {
  return (
    <section className="app-panel plra-state" role="alert">
      <AlertCircle aria-hidden="true" size={24} />
      <div>
        <h2>Erro ao consultar PLRA</h2>
        <p>{message ?? "O snapshot PLRA não pôde ser consultado."}</p>
        <button className="button-secondary" onClick={onRetry} type="button">
          <RefreshCcw aria-hidden="true" size={16} />
          Tentar novamente
        </button>
      </div>
    </section>
  );
}

function sourceLabel(row: PlraAuditRow): string {
  if (row.valuation_source === "default_interno") {
    return "Política interna default";
  }
  if (row.valuation_source === "avaliacao_validada") {
    return "Avaliação validada";
  }
  return "Não aplicável";
}

function formatPercent(value: string | null): string {
  if (value === null) return "—";
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 4,
    style: "percent",
  }).format(Number(value));
}

function AuditDialog({
  audit,
  isError,
  isLoading,
  onClose,
}: {
  audit?: PlraAudit;
  isError: boolean;
  isLoading: boolean;
  onClose: () => void;
}) {
  return (
    <div className="plra-dialog-backdrop" role="presentation">
      <section
        aria-labelledby="plra-audit-title"
        aria-modal="true"
        className="plra-dialog"
        role="dialog"
      >
        <header className="plra-dialog-header">
          <div>
            <h2 id="plra-audit-title">Auditoria do PLRA</h2>
            <p>Memória persistida por conta e regra metodológica.</p>
          </div>
          <button
            aria-label="Fechar auditoria"
            className="plra-icon-button"
            onClick={onClose}
            title="Fechar auditoria"
            type="button"
          >
            <X aria-hidden="true" size={18} />
          </button>
        </header>

        <div className="plra-dialog-body">
          {isLoading ? <p>Carregando memória de cálculo...</p> : null}
          {isError ? (
            <p className="plra-audit-error" role="alert">
              A auditoria não pôde ser consultada.
            </p>
          ) : null}
          {!isLoading && !isError && audit?.rows.length === 0 ? (
            <p>Sem registros.</p>
          ) : null}
          {!isLoading && !isError && audit && audit.rows.length > 0 ? (
            <div className="plra-audit-scroll">
              <table className="plra-audit-table">
                <thead>
                  <tr>
                    <th>Conta</th>
                    <th>Tratamento</th>
                    <th className="numeric">Valor contábil</th>
                    <th className="numeric">Deságio default</th>
                    <th className="numeric">Valor default</th>
                    <th className="numeric">Avaliação validada</th>
                    <th className="numeric">Valor final</th>
                    <th>Fonte</th>
                  </tr>
                </thead>
                <tbody>
                  {audit.rows.map((row) => (
                    <tr key={row.account_code}>
                      <td>
                        <strong>{row.account_name}</strong>
                        <span className="tnum">{row.account_code}</span>
                        <small className="tnum">
                          {row.declared_reference_code ?? "Sem COD_CTA_REF"}
                        </small>
                      </td>
                      <td>
                        <strong>{inclusionLabels[row.inclusion_status]}</strong>
                        <small>{row.reason}</small>
                      </td>
                      <td className="numeric tnum">{formatCurrency(row.base_value)}</td>
                      <td className="numeric tnum">
                        {formatPercent(row.default_discount_percent)}
                      </td>
                      <td className="numeric tnum">
                        {formatCurrency(row.default_economic_value)}
                      </td>
                      <td className="numeric tnum">
                        {row.validated_valuation_value === null
                          ? "—"
                          : formatCurrency(row.validated_valuation_value)}
                      </td>
                      <td className="numeric tnum">
                        {formatCurrency(row.final_economic_value)}
                      </td>
                      <td>{sourceLabel(row)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : null}
        </div>

        <footer className="plra-dialog-footer">
          <span className="tnum">
            {audit ? `${audit.rows.length} contas` : "Auditoria PLRA"}
          </span>
          <button className="button-secondary" onClick={onClose} type="button">
            Fechar
          </button>
        </footer>
      </section>
    </div>
  );
}

export function PlraPage({
  analysisId,
  audit,
  calculation,
  errorMessage,
  errorStatus,
  isAuditError,
  isAuditLoading,
  isAuditOpen,
  isError,
  isLoading,
  isRunning,
  onAuditClose,
  onAuditOpen,
  onRetry,
  onRun,
  year,
}: PlraPageProps) {
  return (
    <>
      <header className="app-topbar">
        <div>
          <h1 className="app-title">Patrimônio Líquido Realizável Ajustado</h1>
          <p className="app-subtitle">
            Análise <span className="tnum">{analysisId}</span> · Exercício{" "}
            <span className="tnum">{year}</span>
          </p>
        </div>
        <div className="plra-topbar-actions">
          {calculation ? (
            <a
              className="button-secondary"
              href={plraExportUrl(analysisId, year)}
            >
              <Download aria-hidden="true" size={16} />
              Exportar Excel
            </a>
          ) : null}
          <button
            className="button-primary"
            disabled={isRunning}
            onClick={onRun}
            type="button"
          >
            <RefreshCcw aria-hidden="true" size={16} />
            {isRunning ? "Calculando..." : calculation ? "Recalcular" : "Calcular PLRA"}
          </button>
        </div>
      </header>

      <main className="app-content plra-content">
        {isLoading ? <LoadingState /> : null}
        {!isLoading && isError && errorStatus === 404 ? (
          <EmptyState isRunning={isRunning} onRun={onRun} />
        ) : null}
        {!isLoading && isError && errorStatus !== 404 ? (
          <ErrorState message={errorMessage} onRetry={onRetry} />
        ) : null}

        {!isLoading && !isError && calculation ? (
          <>
            <section className="plra-result-band">
              <div className="plra-result-main">
                <p className="eyebrow">PLRA</p>
                <strong className="plra-result-value tnum">
                  {formatCurrency(calculation.plra_value)}
                </strong>
                <StatusBadge status={calculation.plra_status} />
              </div>
              <dl className="plra-meta">
                <div>
                  <dt>Fórmula</dt>
                  <dd>{calculation.calculation_formula}</dd>
                </div>
                <div>
                  <dt>Versão metodológica</dt>
                  <dd className="tnum">{calculation.methodology_version_id}</dd>
                </div>
                <div>
                  <dt>Estado do balanço declarado</dt>
                  <dd>{calculation.balance_status}</dd>
                </div>
              </dl>
            </section>

            <section aria-label="Resumo PLRA" className="plra-summary-grid">
              <SummaryItem label="Ativos brutos" value={calculation.gross_assets_value} />
              <SummaryItem
                label="Ativos ajustados"
                value={calculation.adjusted_assets_value}
              />
              <SummaryItem
                label="Passivos exigíveis"
                value={calculation.gross_economic_liabilities_value}
              />
              <SummaryItem label="PLR bruto" value={calculation.plr_gross_value} />
            </section>

            <section className="app-panel plra-audit-entry">
              <div>
                <div className="plra-section-title">
                  <ClipboardCheck aria-hidden="true" size={19} />
                  <h2>Memória por conta</h2>
                </div>
                <p>
                  Valores contábeis, política default, avaliações e tratamento final.
                </p>
              </div>
              <button className="button-secondary" onClick={onAuditOpen} type="button">
                <ClipboardCheck aria-hidden="true" size={16} />
                Abrir auditoria
              </button>
            </section>

            <div className="plra-messages">
              <MessageSection
                icon={Ban}
                items={calculation.blocking_issues}
                title="Bloqueios"
                tone="danger"
              />
              <MessageSection
                icon={AlertTriangle}
                items={[...calculation.pending_accounts, ...calculation.limitations]}
                title="Pendências e limitações"
                tone="warning"
              />
              <MessageSection
                icon={AlertCircle}
                items={calculation.warnings}
                title="Avisos"
                tone="neutral"
              />
            </div>

            <footer className="plra-snapshot-footer">
              <Scale aria-hidden="true" size={15} />
              <span>
                Snapshot calculado em{" "}
                <time className="tnum" dateTime={calculation.calculated_at}>
                  {new Intl.DateTimeFormat("pt-BR", {
                    dateStyle: "short",
                    timeStyle: "short",
                  }).format(new Date(calculation.calculated_at))}
                </time>
              </span>
            </footer>
          </>
        ) : null}
      </main>

      {isAuditOpen ? (
        <AuditDialog
          audit={audit}
          isError={isAuditError}
          isLoading={isAuditLoading}
          onClose={onAuditClose}
        />
      ) : null}
    </>
  );
}
