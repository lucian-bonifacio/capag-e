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
  RoaAuditRow,
  RoaBlock,
  RoaCalculation,
  RoaDecisionPayload,
  RoaRowStatus,
} from "../api/roa";
import { roaExportUrl } from "../api/roa";
import { formatCurrency } from "../lib/formatters";
import "./RoaPage.css";


type RoaPageProps = {
  analysisId: string;
  calculation?: RoaCalculation;
  errorMessage?: string;
  errorStatus?: number;
  isError: boolean;
  isLoading: boolean;
  isRunning: boolean;
  isSavingDecision: boolean;
  onDecision: (payload: RoaDecisionPayload) => Promise<void>;
  onRetry: () => void;
  onRun: () => void;
  year: string;
};

type BlockFilter = "todos" | RoaBlock;
type StatusFilter = "todos" | RoaRowStatus;

const PAGE_SIZE = 100;
const statusLabels: Record<ComponentStatus, string> = {
  nao_calculado: "Não calculado",
  calculado: "Calculado",
  parcial: "Parcial",
  bloqueado_por_pendencia: "Bloqueado por pendência",
  bloqueado_por_evidencia: "Bloqueado por evidência",
  erro_metodologico: "Erro metodológico",
};
const blockLabels: Record<RoaBlock, string> = {
  receita_bruta: "Receita bruta",
  deducoes_receita: "Deduções da receita",
  tributos_receita: "Tributos sobre receita",
  custos_operacionais: "Custos operacionais",
  despesas_operacionais: "Despesas operacionais",
  resultado_financeiro: "Resultado financeiro",
  resultado_nao_operacional: "Resultado não operacional",
  pressoes_complementares_caixa: "Pressões de caixa",
};
const rowStatusLabels: Record<RoaRowStatus, string> = {
  incluido: "Incluído",
  excluido: "Excluído",
  pendente_revisao: "Revisar",
  sem_regra: "Sem regra",
  pendente_evidencia: "Pendente de evidência",
  decisao_manual_aplicada: "Decisão aplicada",
};

function statusTone(status: ComponentStatus | RoaRowStatus): string {
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

function EmptyState({ isRunning, onRun }: Pick<RoaPageProps, "isRunning" | "onRun">) {
  return (
    <section className="app-panel roa-state">
      <Calculator aria-hidden="true" size={24} />
      <div>
        <h2>ROA não calculado</h2>
        <p>Não há snapshot persistido para este exercício.</p>
        <button
          className="button-primary"
          disabled={isRunning}
          onClick={onRun}
          type="button"
        >
          <Calculator aria-hidden="true" size={16} />
          {isRunning ? "Calculando..." : "Calcular ROA"}
        </button>
      </div>
    </section>
  );
}

function DecisionDialog({
  isSaving,
  onClose,
  onSubmit,
  row,
}: {
  isSaving: boolean;
  onClose: () => void;
  onSubmit: (payload: RoaDecisionPayload) => Promise<void>;
  row: RoaAuditRow;
}) {
  const canInclude = row.final_status === "pendente_revisao";
  const [action, setAction] = useState<"incluir" | "excluir">(
    canInclude ? "incluir" : "excluir",
  );
  const [justification, setJustification] = useState("");
  const [evidenceId, setEvidenceId] = useState(row.evidence_id ?? "");

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    await onSubmit({
      action,
      account_code: row.account_code,
      justification,
      ...(evidenceId.trim() ? { evidence_id: evidenceId.trim() } : {}),
    });
  };

  return (
    <div className="roa-dialog-backdrop" role="presentation">
      <section
        aria-labelledby="roa-decision-title"
        aria-modal="true"
        className="roa-dialog"
        role="dialog"
      >
        <header className="roa-dialog-header">
          <div>
            <h2 id="roa-decision-title">Decisão sobre conta</h2>
            <p className="tnum">{row.account_code}</p>
          </div>
          <button
            aria-label="Fechar decisão"
            className="roa-icon-button"
            onClick={onClose}
            title="Fechar decisão"
            type="button"
          >
            <X aria-hidden="true" size={18} />
          </button>
        </header>
        <form onSubmit={(event) => void submit(event)}>
          <div className="roa-dialog-body">
            <div className="roa-account-context">
              <strong>{row.account_name}</strong>
              <span className="tnum">
                {row.reference_code ?? "Sem COD_CTA_REF"}
              </span>
              <span className="tnum">{formatCurrency(row.base_value)}</span>
            </div>
            <fieldset className="roa-decision-mode">
              <legend>Tratamento</legend>
              <label>
                <input
                  checked={action === "incluir"}
                  disabled={!canInclude}
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
            {!canInclude ? (
              <p className="roa-contract-note">
                A conta não possui regra metodológica e só pode ser excluída.
              </p>
            ) : null}
            <label className="roa-field">
              Evidência vinculada
              <input
                maxLength={64}
                onChange={(event) => setEvidenceId(event.target.value)}
                placeholder="ID opcional"
                value={evidenceId}
              />
            </label>
            <label className="roa-field">
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
          <footer className="roa-dialog-footer">
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

export function RoaPage({
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
}: RoaPageProps) {
  const [blockFilter, setBlockFilter] = useState<BlockFilter>("todos");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("todos");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [decisionRow, setDecisionRow] = useState<RoaAuditRow>();

  const filteredRows = useMemo(() => {
    if (!calculation) return [];
    const term = search.trim().toLocaleLowerCase("pt-BR");
    return calculation.audit_rows.filter((row) => {
      const matchesBlock =
        blockFilter === "todos" || row.roa_block === blockFilter;
      const matchesStatus =
        statusFilter === "todos" || row.final_status === statusFilter;
      const matchesSearch =
        !term ||
        row.account_code.toLocaleLowerCase("pt-BR").includes(term) ||
        row.account_name.toLocaleLowerCase("pt-BR").includes(term) ||
        (row.reference_code ?? "").toLocaleLowerCase("pt-BR").includes(term);
      return matchesBlock && matchesStatus && matchesSearch;
    });
  }, [blockFilter, calculation, search, statusFilter]);

  useEffect(() => setPage(1), [blockFilter, search, statusFilter]);
  const pageCount = Math.max(1, Math.ceil(filteredRows.length / PAGE_SIZE));
  const currentPage = Math.min(page, pageCount);
  const visibleRows = filteredRows.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE,
  );

  return (
    <>
      <header className="app-topbar roa-topbar">
        <div>
          <h1 className="app-title">ROA e CAPAG-E</h1>
          <p className="app-subtitle">
            Análise <span className="tnum">{analysisId}</span> · Exercício{" "}
            <span className="tnum">{year}</span>
          </p>
        </div>
        <div className="roa-topbar-actions">
          {calculation ? (
            <a
              className="button-secondary"
              href={roaExportUrl(analysisId, year)}
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
            {isRunning ? "Calculando..." : calculation ? "Recalcular" : "Calcular ROA"}
          </button>
        </div>
      </header>

      <main className="app-content roa-content">
        {isLoading ? (
          <section aria-label="Carregando ROA" className="app-panel roa-state">
            <div className="skeleton-table roa-skeleton" />
          </section>
        ) : null}
        {!isLoading && isError && errorStatus !== 404 ? (
          <section className="app-panel roa-state" role="alert">
            <AlertCircle aria-hidden="true" size={24} />
            <div>
              <h2>Erro ao consultar ROA</h2>
              <p>{errorMessage ?? "O snapshot ROA não pôde ser consultado."}</p>
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
            <section className="roa-result-band">
              <div>
                <span className="roa-eyebrow">ROA final</span>
                <strong className="roa-result-value tnum">
                  {formatCurrency(calculation.roa_final)}
                </strong>
                <span
                  className="status-badge"
                  data-variant={statusTone(calculation.roa_status)}
                >
                  {statusLabels[calculation.roa_status]}
                </span>
              </div>
              <dl>
                <div>
                  <dt>ROA preliminar</dt>
                  <dd className="tnum">
                    {formatCurrency(calculation.roa_preliminary)}
                  </dd>
                </div>
                <div>
                  <dt>Contas auditáveis</dt>
                  <dd className="tnum">{calculation.audit_rows.length}</dd>
                </div>
                <div>
                  <dt>Pendências</dt>
                  <dd className="tnum">{calculation.pending_groups.length}</dd>
                </div>
              </dl>
            </section>

            <section className="roa-capag-band">
              <header>
                <div>
                  <span className="roa-eyebrow">Integração CAPAG-E</span>
                  <h2>
                    {calculation.capag_assessment?.methodology_formula ??
                      "PLRA ainda não disponível"}
                  </h2>
                </div>
                {calculation.capag_assessment ? (
                  <span
                    className="status-badge"
                    data-variant={
                      calculation.capag_assessment.capag_e_status === "calculado"
                        ? "success"
                        : calculation.capag_assessment.capag_e_status === "parcial"
                          ? "warning"
                          : "danger"
                    }
                  >
                    {calculation.capag_assessment.capag_e_status}
                  </span>
                ) : null}
              </header>
              {calculation.capag_assessment ? (
                <dl>
                  <div>
                    <dt>PLRA</dt>
                    <dd className="tnum">
                      {calculation.capag_assessment.plra_value
                        ? formatCurrency(calculation.capag_assessment.plra_value)
                        : "Indisponível"}
                    </dd>
                  </div>
                  <div>
                    <dt>ROA</dt>
                    <dd className="tnum">
                      {calculation.capag_assessment.roa_value
                        ? formatCurrency(calculation.capag_assessment.roa_value)
                        : "Indisponível"}
                    </dd>
                  </div>
                  {calculation.capag_assessment.fca_value ? (
                    <div>
                      <dt>FCA comparativo</dt>
                      <dd className="tnum">
                        {formatCurrency(calculation.capag_assessment.fca_value)}
                      </dd>
                    </div>
                  ) : null}
                  <div>
                    <dt>CAPAG-E</dt>
                    <dd className="tnum">
                      {calculation.capag_assessment.capag_e_value
                        ? formatCurrency(
                            calculation.capag_assessment.capag_e_value,
                          )
                        : "Sem resultado único"}
                    </dd>
                  </div>
                </dl>
              ) : (
                <p>Execute e finalize o PLRA para disponibilizar o assessment.</p>
              )}
            </section>

            <section aria-label="Componentes do ROA" className="roa-summary-grid">
              {calculation.component_summaries.map((summary) => (
                <article key={summary.component_code}>
                  <span>{summary.component_label}</span>
                  <strong className="tnum">{formatCurrency(summary.value)}</strong>
                  <small className="tnum">
                    {summary.account_count} conta
                    {summary.account_count === 1 ? "" : "s"}
                  </small>
                </article>
              ))}
            </section>

            {calculation.pending_groups.length > 0 ? (
              <section className="roa-pending-band">
                <div>
                  <AlertCircle aria-hidden="true" size={18} />
                  <h2>Pendências do ROA</h2>
                  <span className="tnum">{calculation.pending_groups.length}</span>
                </div>
                <ul>
                  {calculation.pending_groups.slice(0, 10).map((group, index) => (
                    <li
                      key={`${group.code}-${group.account_code}-${group.evidence_id}-${index}`}
                    >
                      <strong>{group.code}</strong>
                      <span>
                        {group.message}
                        {group.account_code ? ` Conta ${group.account_code}.` : ""}
                        {group.evidence_id
                          ? ` Evidência ${group.evidence_id}.`
                          : ""}
                      </span>
                    </li>
                  ))}
                </ul>
              </section>
            ) : null}

            {calculation.limitations.length > 0 || calculation.alerts.length > 0 ? (
              <section className="roa-messages" aria-label="Alertas e limitações">
                {[...calculation.alerts, ...calculation.limitations].map(
                  (message) => (
                    <p key={message}>{message}</p>
                  ),
                )}
              </section>
            ) : null}

            <section className="roa-audit-section">
              <header>
                <div>
                  <h2>Contas de resultado</h2>
                  <p>
                    <span className="tnum">{filteredRows.length}</span> de{" "}
                    <span className="tnum">{calculation.audit_rows.length}</span>{" "}
                    contas
                  </p>
                </div>
                <div className="roa-filters">
                  <label className="roa-search">
                    <Search aria-hidden="true" size={16} />
                    <span className="sr-only">Buscar conta</span>
                    <input
                      onChange={(event) => setSearch(event.target.value)}
                      placeholder="Buscar conta ou código"
                      value={search}
                    />
                  </label>
                  <label>
                    <span className="sr-only">Bloco ROA</span>
                    <select
                      aria-label="Bloco ROA"
                      onChange={(event) =>
                        setBlockFilter(event.target.value as BlockFilter)
                      }
                      value={blockFilter}
                    >
                      <option value="todos">Todos os blocos</option>
                      {Object.entries(blockLabels).map(([value, label]) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    <span className="sr-only">Status da conta</span>
                    <select
                      aria-label="Status da conta"
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
              <div className="roa-table-scroll">
                <table className="roa-table">
                  <thead>
                    <tr>
                      <th>Conta</th>
                      <th>Referencial</th>
                      <th>Bloco e componente</th>
                      <th>Status e evidência</th>
                      <th className="numeric">Movimento base</th>
                      <th className="numeric">Efeito no ROA</th>
                      <th aria-label="Ações" />
                    </tr>
                  </thead>
                  <tbody>
                    {visibleRows.map((row) => (
                      <tr key={row.account_code}>
                        <td>
                          <strong>{row.account_name}</strong>
                          <span className="tnum">{row.account_code}</span>
                          <small className="tnum">
                            Linha {row.line_reference}
                          </small>
                        </td>
                        <td>
                          <strong className="tnum">
                            {row.reference_code ?? "Sem COD_CTA_REF"}
                          </strong>
                          <span>{row.reference_description ?? "Sem descrição"}</span>
                        </td>
                        <td>
                          <strong>
                            {row.roa_block
                              ? blockLabels[row.roa_block]
                              : "Sem bloco"}
                          </strong>
                          <span>{row.component_label ?? "Sem componente"}</span>
                        </td>
                        <td>
                          <span
                            className="status-badge"
                            data-variant={statusTone(row.final_status)}
                          >
                            {rowStatusLabels[row.final_status]}
                          </span>
                          <small>
                            {row.evidence_id
                              ? `Evidência ${row.evidence_id}`
                              : row.required_evidence_type
                                ? `Tipo: ${row.required_evidence_type}`
                                : row.pending_reason}
                          </small>
                        </td>
                        <td className="numeric tnum">
                          {formatCurrency(row.base_value)}
                        </td>
                        <td className="numeric tnum">
                          {formatCurrency(row.signed_value)}
                        </td>
                        <td>
                          {row.final_status === "pendente_revisao" ||
                          row.final_status === "sem_regra" ? (
                            <button
                              aria-label={`Decidir conta ${row.account_code}`}
                              className="roa-icon-button"
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
                        <td className="roa-empty-table" colSpan={7}>
                          Sem registros.
                        </td>
                      </tr>
                    ) : null}
                  </tbody>
                </table>
              </div>
              <footer className="roa-pagination">
                <span className="tnum">
                  Página {currentPage} de {pageCount}
                </span>
                <div>
                  <button
                    aria-label="Página anterior"
                    className="roa-icon-button"
                    disabled={currentPage === 1}
                    onClick={() => setPage((value) => Math.max(1, value - 1))}
                    title="Página anterior"
                    type="button"
                  >
                    <ChevronLeft aria-hidden="true" size={17} />
                  </button>
                  <button
                    aria-label="Próxima página"
                    className="roa-icon-button"
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

      {decisionRow ? (
        <DecisionDialog
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
