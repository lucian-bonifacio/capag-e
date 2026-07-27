import {
  AlertCircle,
  AlertTriangle,
  Ban,
  Calculator,
  RefreshCcw,
} from "lucide-react";

import type {
  CapagAssessment,
  CapagEMethod,
  CapagEStatus,
  ComponentStatus,
} from "../api/capag";
import { formatCurrency } from "../lib/formatters";
import "./CapagAssessmentPage.css";

type CapagAssessmentPageProps = {
  analysisId: string;
  year: string;
  assessment?: CapagAssessment;
  errorStatus?: number;
  isError: boolean;
  isLoading: boolean;
  onRetry: () => void;
};

type BadgeVariant = "success" | "warning" | "danger" | "neutral";

const methodLabels: Record<CapagEMethod, string> = {
  fca_plra: "FCA + PLRA",
  roa_plra: "ROA + PLRA",
  comparativo_fca_roa: "Comparativo FCA e ROA",
  nao_definido: "Não definido",
};

const statusLabels: Record<ComponentStatus | CapagEStatus, string> = {
  nao_calculado: "Não calculado",
  calculado: "Calculado",
  parcial: "Parcial",
  bloqueado_por_pendencia: "Bloqueado por pendência",
  bloqueado_por_evidencia: "Bloqueado por evidência",
  erro_metodologico: "Erro metodológico",
  bloqueado: "Bloqueado",
  indisponivel: "Indisponível",
};

function statusVariant(status: ComponentStatus | CapagEStatus): BadgeVariant {
  if (status === "calculado") return "success";
  if (status === "parcial" || status === "nao_calculado") return "warning";
  if (
    status === "bloqueado" ||
    status === "bloqueado_por_evidencia" ||
    status === "bloqueado_por_pendencia" ||
    status === "erro_metodologico"
  ) {
    return "danger";
  }
  return "neutral";
}

function StatusBadge({ status }: { status: ComponentStatus | CapagEStatus }) {
  return (
    <span className="status-badge" data-variant={statusVariant(status)}>
      {statusLabels[status]}
    </span>
  );
}

function ComponentResult({
  label,
  status,
  value,
}: {
  label: string;
  status: ComponentStatus;
  value: string | null;
}) {
  return (
    <article className="capag-component">
      <div className="capag-component-header">
        <h2>{label}</h2>
        <StatusBadge status={status} />
      </div>
      <p className="capag-component-value tnum">
        {value === null ? "Indisponível" : formatCurrency(value)}
      </p>
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
  if (items.length === 0) return null;

  return (
    <section className="capag-message-section" data-tone={tone}>
      <div className="capag-message-heading">
        <Icon aria-hidden="true" size={18} />
        <h2>{title}</h2>
      </div>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

function LoadingState() {
  return (
    <section
      aria-label="Carregando resultado CAPAG-E"
      className="app-panel capag-state"
    >
      <div className="skeleton-row" />
      <div className="skeleton-row skeleton-row-short" />
      <div className="skeleton-table capag-skeleton" />
    </section>
  );
}

function EmptyState() {
  return (
    <section className="app-panel capag-state">
      <Calculator aria-hidden="true" size={24} />
      <div>
        <h2>Assessment CAPAG-E não calculado</h2>
        <p>Não há resultado persistido para este exercício.</p>
      </div>
    </section>
  );
}

function ErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <section className="app-panel capag-state" role="alert">
      <AlertCircle aria-hidden="true" size={24} />
      <div>
        <h2>Erro ao carregar resultado CAPAG-E</h2>
        <p>O snapshot do assessment não pôde ser consultado.</p>
        <button className="secondary-button" onClick={onRetry} type="button">
          <RefreshCcw aria-hidden="true" size={16} />
          Tentar novamente
        </button>
      </div>
    </section>
  );
}

function fcaLabel(status: ComponentStatus): string {
  if (status === "parcial") return "FCA parcial";
  if (status === "calculado") return "FCA final";
  return "FCA";
}

export function CapagAssessmentPage({
  analysisId,
  assessment,
  errorStatus,
  isError,
  isLoading,
  onRetry,
  year,
}: CapagAssessmentPageProps) {
  return (
    <>
      <header className="app-topbar">
        <div>
          <h1 className="app-title">Resultado CAPAG-E</h1>
          <p className="app-subtitle">
            Análise <span className="tnum">{analysisId}</span> · Exercício{" "}
            <span className="tnum">{year}</span>
          </p>
        </div>
        <span className="app-status">Contrato canônico</span>
      </header>

      <main className="app-content capag-content">
        {isLoading ? <LoadingState /> : null}
        {!isLoading && isError && errorStatus === 404 ? <EmptyState /> : null}
        {!isLoading && isError && errorStatus !== 404 ? (
          <ErrorState onRetry={onRetry} />
        ) : null}

        {!isLoading && !isError && assessment ? (
          <>
            <section className="app-panel capag-result-panel">
              <div className="capag-result-primary">
                <p className="eyebrow">Resultado CAPAG-E</p>
                <p className="capag-result-value tnum">
                  {assessment.capag_e_value === null
                    ? "Indisponível"
                    : formatCurrency(assessment.capag_e_value)}
                </p>
                <StatusBadge status={assessment.capag_e_status} />
                {assessment.unavailable_reason ? (
                  <p className="capag-unavailable-reason">
                    {assessment.unavailable_reason}
                  </p>
                ) : null}
              </div>

              <dl className="capag-contract-meta">
                <div>
                  <dt>Método</dt>
                  <dd>{methodLabels[assessment.method]}</dd>
                </div>
                <div>
                  <dt>Fórmula</dt>
                  <dd className="tnum">{assessment.methodology_formula}</dd>
                </div>
                <div>
                  <dt>Base de cálculo</dt>
                  <dd className="tnum">{assessment.calculation_basis}</dd>
                </div>
              </dl>
            </section>

            <section aria-label="Componentes CAPAG-E" className="capag-components">
              <ComponentResult
                label="PLRA"
                status={assessment.plra_status}
                value={assessment.plra_value}
              />
              <ComponentResult
                label={fcaLabel(assessment.fca_status)}
                status={assessment.fca_status}
                value={assessment.fca_value}
              />
              <ComponentResult
                label="ROA"
                status={assessment.roa_status}
                value={assessment.roa_value}
              />
            </section>

            <div className="capag-messages">
              <MessageSection
                icon={Ban}
                items={assessment.blocking_issues}
                title="Bloqueios"
                tone="danger"
              />
              <MessageSection
                icon={AlertTriangle}
                items={assessment.limitations}
                title="Limitações"
                tone="warning"
              />
              <MessageSection
                icon={AlertCircle}
                items={assessment.warnings}
                title="Avisos"
                tone="neutral"
              />
            </div>

            <footer className="capag-methodology-footer">
              <span>Versão metodológica</span>
              <strong className="tnum">{assessment.methodology_version_id}</strong>
            </footer>
          </>
        ) : null}
      </main>
    </>
  );
}
