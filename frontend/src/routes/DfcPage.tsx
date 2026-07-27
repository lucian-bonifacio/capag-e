import {
  AlertCircle,
  Calculator,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  Download,
  RefreshCcw,
  Search,
  X,
} from "lucide-react";
import { type FormEvent, useEffect, useMemo, useState } from "react";

import type { ComponentStatus } from "../api/capag";
import type {
  DfcActivity,
  DfcAuditRow,
  DfcCalculation,
  DfcDecisionPayload,
  DfcRowStatus,
} from "../api/dfc";
import { dfcExportUrl } from "../api/dfc";
import { formatCurrency } from "../lib/formatters";
import "./DfcPage.css";


type DfcPageProps = {
  analysisId: string;
  calculation?: DfcCalculation;
  errorMessage?: string;
  errorStatus?: number;
  isError: boolean;
  isLoading: boolean;
  isRunning: boolean;
  isSavingDecision: boolean;
  onDecision: (payload: DfcDecisionPayload) => Promise<void>;
  onRetry: () => void;
  onRun: () => void;
  year: string;
};

type ClassifiedActivity = Exclude<DfcActivity, "nao_classificado">;
type ActivityFilter = "todas" | DfcActivity;
type StatusFilter = "todos" | DfcRowStatus;

const PAGE_SIZE = 100;
const statusLabels: Record<ComponentStatus, string> = {
  nao_calculado: "Não calculado",
  calculado: "Calculado",
  parcial: "Parcial",
  bloqueado_por_pendencia: "Bloqueado por pendência",
  bloqueado_por_evidencia: "Bloqueado por evidência",
  erro_metodologico: "Erro metodológico",
};
const activityLabels: Record<DfcActivity, string> = {
  operacional: "Operacional",
  investimento: "Investimento",
  financiamento: "Financiamento",
  nao_classificado: "Não classificado",
};
const rowStatusLabels: Record<DfcRowStatus, string> = {
  incluido: "Incluído",
  excluido: "Excluído",
  nao_classificado: "Não classificado",
  fluxo_incompativel: "Fluxo incompatível",
  pendente_evidencia: "Pendente de evidência",
  decisao_manual_aplicada: "Decisão aplicada",
};

function statusTone(status: ComponentStatus | DfcRowStatus): string {
  if (status === "calculado" || status === "incluido") return "success";
  if (
    status === "parcial" ||
    status === "nao_calculado" ||
    status === "excluido" ||
    status === "decisao_manual_aplicada"
  ) {
    return "warning";
  }
  return "danger";
}

function EmptyState({ isRunning, onRun }: Pick<DfcPageProps, "isRunning" | "onRun">) {
  return (
    <section className="app-panel dfc-state">
      <Calculator aria-hidden="true" size={24} />
      <div>
        <h2>DFC não calculada</h2>
        <p>Não há snapshot persistido para este exercício.</p>
        <button
          className="button-primary"
          disabled={isRunning}
          onClick={onRun}
          type="button"
        >
          <Calculator aria-hidden="true" size={16} />
          {isRunning ? "Calculando..." : "Calcular DFC"}
        </button>
      </div>
    </section>
  );
}

function DecisionDialog({
  calculation,
  isSaving,
  onClose,
  onSubmit,
  row,
}: {
  calculation: DfcCalculation;
  isSaving: boolean;
  onClose: () => void;
  onSubmit: (payload: DfcDecisionPayload) => Promise<void>;
  row: DfcAuditRow;
}) {
  const [action, setAction] = useState<"incluir" | "excluir">("incluir");
  const [activity, setActivity] = useState<ClassifiedActivity>("operacional");
  const components = calculation.component_summaries.filter(
    (component) => component.activity === activity,
  );
  const [componentCode, setComponentCode] = useState(
    components[0]?.component_code ?? "",
  );
  const [justification, setJustification] = useState("");

  useEffect(() => {
    setComponentCode(components[0]?.component_code ?? "");
  }, [activity]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (action === "incluir") {
      await onSubmit({
        action,
        entry_number: row.entry_number,
        line_number: row.line_number,
        activity,
        component_code: componentCode,
        justification,
      });
    } else {
      await onSubmit({
        action,
        entry_number: row.entry_number,
        line_number: row.line_number,
        justification,
      });
    }
  };

  return (
    <div className="dfc-dialog-backdrop" role="presentation">
      <section
        aria-labelledby="dfc-decision-title"
        aria-modal="true"
        className="dfc-dialog"
        role="dialog"
      >
        <header className="dfc-dialog-header">
          <div>
            <h2 id="dfc-decision-title">Decisão sobre movimento</h2>
            <p className="tnum">
              Lançamento {row.entry_number} · Linha {row.line_number}
            </p>
          </div>
          <button
            aria-label="Fechar decisão"
            className="dfc-icon-button"
            onClick={onClose}
            title="Fechar decisão"
            type="button"
          >
            <X aria-hidden="true" size={18} />
          </button>
        </header>
        <form onSubmit={(event) => void submit(event)}>
          <div className="dfc-dialog-body">
            <div className="dfc-movement-context">
              <strong>{row.counterparty_account_name}</strong>
              <span className="tnum">
                {row.counterparty_reference_code ?? "Sem COD_CTA_REF"}
              </span>
              <span className="tnum">{formatCurrency(row.movement_value)}</span>
            </div>
            <fieldset className="dfc-decision-mode">
              <legend>Tratamento</legend>
              <label>
                <input
                  checked={action === "incluir"}
                  name="action"
                  onChange={() => setAction("incluir")}
                  type="radio"
                />
                Incluir
              </label>
              <label>
                <input
                  checked={action === "excluir"}
                  name="action"
                  onChange={() => setAction("excluir")}
                  type="radio"
                />
                Excluir
              </label>
            </fieldset>
            {action === "incluir" ? (
              <div className="dfc-form-grid">
                <label>
                  Atividade
                  <select
                    onChange={(event) =>
                      setActivity(event.target.value as ClassifiedActivity)
                    }
                    value={activity}
                  >
                    <option value="operacional">Operacional</option>
                    <option value="investimento">Investimento</option>
                    <option value="financiamento">Financiamento</option>
                  </select>
                </label>
                <label>
                  Componente
                  <select
                    onChange={(event) => setComponentCode(event.target.value)}
                    required
                    value={componentCode}
                  >
                    {components.map((component) => (
                      <option
                        key={component.component_code}
                        value={component.component_code}
                      >
                        {component.component_label}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            ) : null}
            <label className="dfc-justification">
              Justificativa
              <textarea
                maxLength={4000}
                onChange={(event) => setJustification(event.target.value)}
                required
                rows={4}
                value={justification}
              />
            </label>
          </div>
          <footer className="dfc-dialog-footer">
            <button
              className="button-secondary"
              disabled={isSaving}
              onClick={onClose}
              type="button"
            >
              Cancelar
            </button>
            <button
              className="button-primary"
              disabled={isSaving || !justification.trim()}
              type="submit"
            >
              <ClipboardCheck aria-hidden="true" size={16} />
              {isSaving ? "Aplicando..." : "Aplicar decisão"}
            </button>
          </footer>
        </form>
      </section>
    </div>
  );
}

export function DfcPage({
  analysisId,
  calculation,
  errorMessage,
  errorStatus,
  isError,
  isLoading,
  isRunning,
  isSavingDecision,
  onDecision,
  onRetry,
  onRun,
  year,
}: DfcPageProps) {
  const [activityFilter, setActivityFilter] = useState<ActivityFilter>("todas");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("todos");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [decisionRow, setDecisionRow] = useState<DfcAuditRow>();

  const filteredRows = useMemo(() => {
    if (!calculation) return [];
    const term = search.trim().toLocaleLowerCase("pt-BR");
    return calculation.audit_rows.filter((row) => {
      const matchesActivity =
        activityFilter === "todas" || row.dfc_activity === activityFilter;
      const matchesStatus =
        statusFilter === "todos" || row.final_status === statusFilter;
      const matchesSearch =
        !term ||
        row.entry_number.toLocaleLowerCase("pt-BR").includes(term) ||
        row.counterparty_account_code.toLocaleLowerCase("pt-BR").includes(term) ||
        row.counterparty_account_name.toLocaleLowerCase("pt-BR").includes(term) ||
        (row.history ?? "").toLocaleLowerCase("pt-BR").includes(term);
      return matchesActivity && matchesStatus && matchesSearch;
    });
  }, [activityFilter, calculation, search, statusFilter]);

  useEffect(() => setPage(1), [activityFilter, search, statusFilter]);
  const pageCount = Math.max(1, Math.ceil(filteredRows.length / PAGE_SIZE));
  const currentPage = Math.min(page, pageCount);
  const visibleRows = filteredRows.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE,
  );

  return (
    <>
      <header className="app-topbar">
        <div>
          <h1 className="app-title">DFC direta e FCA</h1>
          <p className="app-subtitle">
            Análise <span className="tnum">{analysisId}</span> · Exercício{" "}
            <span className="tnum">{year}</span>
          </p>
        </div>
        <div className="dfc-topbar-actions">
          {calculation ? (
            <a
              className="button-secondary"
              href={dfcExportUrl(analysisId, year)}
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
            {isRunning ? "Calculando..." : calculation ? "Recalcular" : "Calcular DFC"}
          </button>
        </div>
      </header>

      <main className="app-content dfc-content">
        {isLoading ? (
          <section aria-label="Carregando DFC" className="app-panel dfc-state">
            <div className="skeleton-table dfc-skeleton" />
          </section>
        ) : null}
        {!isLoading && isError && errorStatus !== 404 ? (
          <section className="app-panel dfc-state" role="alert">
            <AlertCircle aria-hidden="true" size={24} />
            <div>
              <h2>Erro ao consultar DFC</h2>
              <p>{errorMessage ?? "O snapshot DFC não pôde ser consultado."}</p>
              <button className="button-secondary" onClick={onRetry} type="button">
                <RefreshCcw aria-hidden="true" size={16} />
                Tentar novamente
              </button>
            </div>
          </section>
        ) : null}
        {!isLoading && (!calculation || errorStatus === 404) ? (
          <EmptyState isRunning={isRunning} onRun={onRun} />
        ) : null}
        {!isLoading && calculation ? (
          <>
            <section className="dfc-result-band">
              <div>
                <span className="dfc-eyebrow">FCA apurado</span>
                <strong className="dfc-result-value tnum">
                  {formatCurrency(calculation.fca_value)}
                </strong>
                <span
                  className="status-badge"
                  data-variant={statusTone(calculation.fca_status)}
                >
                  {statusLabels[calculation.fca_status]}
                </span>
              </div>
              <dl>
                <div>
                  <dt>Versão metodológica</dt>
                  <dd className="tnum">{calculation.methodology_version_id}</dd>
                </div>
                <div>
                  <dt>Movimentos auditáveis</dt>
                  <dd className="tnum">{calculation.audit_rows.length}</dd>
                </div>
                <div>
                  <dt>Pendências</dt>
                  <dd className="tnum">{calculation.pending_issues.length}</dd>
                </div>
              </dl>
            </section>

            <section aria-label="Resumo por atividade" className="dfc-summary-grid">
              <article>
                <span>Operacional</span>
                <strong className="tnum">
                  {formatCurrency(calculation.operational_flow)}
                </strong>
              </article>
              <article>
                <span>Investimento</span>
                <strong className="tnum">
                  {formatCurrency(calculation.investment_flow)}
                </strong>
              </article>
              <article>
                <span>Financiamento</span>
                <strong className="tnum">
                  {formatCurrency(calculation.financing_flow)}
                </strong>
              </article>
              <article>
                <span>Ajustes validados</span>
                <strong className="tnum">
                  {formatCurrency(calculation.manual_adjustments_value)}
                </strong>
              </article>
            </section>

            {calculation.pending_issues.length > 0 ? (
              <section className="dfc-pending-band">
                <div>
                  <AlertCircle aria-hidden="true" size={18} />
                  <h2>Pendências da DFC</h2>
                  <span className="tnum">{calculation.pending_issues.length}</span>
                </div>
                <ul>
                  {calculation.pending_issues.slice(0, 8).map((issue, index) => (
                    <li key={`${issue.code}-${issue.entry_number}-${issue.line_number}-${index}`}>
                      <strong>{issue.code}</strong>
                      <span>
                        {issue.message}
                        {issue.entry_number
                          ? ` Lançamento ${issue.entry_number}, linha ${issue.line_number}.`
                          : ""}
                      </span>
                    </li>
                  ))}
                </ul>
              </section>
            ) : null}

            <section className="dfc-audit-section">
              <header>
                <div>
                  <h2>Movimentos auditáveis</h2>
                  <p>
                    <span className="tnum">{filteredRows.length}</span> de{" "}
                    <span className="tnum">{calculation.audit_rows.length}</span>{" "}
                    movimentos
                  </p>
                </div>
                <div className="dfc-filters">
                  <label className="dfc-search">
                    <Search aria-hidden="true" size={16} />
                    <span className="sr-only">Buscar movimento</span>
                    <input
                      onChange={(event) => setSearch(event.target.value)}
                      placeholder="Buscar lançamento ou conta"
                      value={search}
                    />
                  </label>
                  <label>
                    <span className="sr-only">Atividade</span>
                    <select
                      aria-label="Atividade"
                      onChange={(event) =>
                        setActivityFilter(event.target.value as ActivityFilter)
                      }
                      value={activityFilter}
                    >
                      <option value="todas">Todas as atividades</option>
                      {Object.entries(activityLabels).map(([value, label]) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    <span className="sr-only">Status</span>
                    <select
                      aria-label="Status"
                      onChange={(event) =>
                        setStatusFilter(event.target.value as StatusFilter)
                      }
                      value={statusFilter}
                    >
                      <option value="todos">Todos os status</option>
                      {Object.entries(rowStatusLabels).map(([value, label]) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
              </header>
              <div className="dfc-table-scroll">
                <table className="dfc-table">
                  <thead>
                    <tr>
                      <th>Lançamento</th>
                      <th>Contrapartida</th>
                      <th>Atividade e componente</th>
                      <th>Status</th>
                      <th className="numeric">Movimento</th>
                      <th className="numeric">Incluído</th>
                      <th aria-label="Ações" />
                    </tr>
                  </thead>
                  <tbody>
                    {visibleRows.map((row) => (
                      <tr key={`${row.entry_number}-${row.line_number}`}>
                        <td>
                          <strong className="tnum">{row.entry_number}</strong>
                          <span>{row.entry_date ?? "Sem data"}</span>
                          <small className="tnum">Linha {row.line_number}</small>
                        </td>
                        <td>
                          <strong>{row.counterparty_account_name}</strong>
                          <span className="tnum">{row.counterparty_account_code}</span>
                          <small className="tnum">
                            {row.counterparty_reference_code ?? "Sem COD_CTA_REF"}
                          </small>
                        </td>
                        <td>
                          <strong>{activityLabels[row.dfc_activity]}</strong>
                          <span>{row.dfc_component_label ?? "Sem componente"}</span>
                        </td>
                        <td>
                          <span
                            className="status-badge"
                            data-variant={statusTone(row.final_status)}
                          >
                            {rowStatusLabels[row.final_status]}
                          </span>
                          {row.pending_reason ? <small>{row.pending_reason}</small> : null}
                        </td>
                        <td className="numeric tnum">
                          {formatCurrency(row.movement_value)}
                        </td>
                        <td className="numeric tnum">
                          {formatCurrency(row.included_value)}
                        </td>
                        <td>
                          {row.final_status === "nao_classificado" ||
                          row.final_status === "fluxo_incompativel" ? (
                            <button
                              aria-label={`Decidir lançamento ${row.entry_number}, linha ${row.line_number}`}
                              className="dfc-icon-button"
                              onClick={() => setDecisionRow(row)}
                              title="Registrar decisão"
                              type="button"
                            >
                              <ClipboardCheck aria-hidden="true" size={17} />
                            </button>
                          ) : null}
                        </td>
                      </tr>
                    ))}
                    {visibleRows.length === 0 ? (
                      <tr>
                        <td className="dfc-empty-table" colSpan={7}>
                          Sem registros.
                        </td>
                      </tr>
                    ) : null}
                  </tbody>
                </table>
              </div>
              <footer className="dfc-pagination">
                <span className="tnum">
                  Página {currentPage} de {pageCount}
                </span>
                <div>
                  <button
                    aria-label="Página anterior"
                    className="dfc-icon-button"
                    disabled={currentPage === 1}
                    onClick={() => setPage((value) => Math.max(1, value - 1))}
                    title="Página anterior"
                    type="button"
                  >
                    <ChevronLeft aria-hidden="true" size={17} />
                  </button>
                  <button
                    aria-label="Próxima página"
                    className="dfc-icon-button"
                    disabled={currentPage === pageCount}
                    onClick={() =>
                      setPage((value) => Math.min(pageCount, value + 1))
                    }
                    title="Próxima página"
                    type="button"
                  >
                    <ChevronRight aria-hidden="true" size={17} />
                  </button>
                </div>
              </footer>
            </section>
          </>
        ) : null}
      </main>

      {decisionRow && calculation ? (
        <DecisionDialog
          calculation={calculation}
          isSaving={isSavingDecision}
          onClose={() => setDecisionRow(undefined)}
          onSubmit={async (payload) => {
            await onDecision(payload);
            setDecisionRow(undefined);
          }}
          row={decisionRow}
        />
      ) : null}
    </>
  );
}
