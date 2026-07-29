import { useEffect, useState, type CSSProperties } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  ClipboardCheck,
  Upload,
  X,
} from "lucide-react";
import { Link } from "react-router-dom";

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
    label: "Divergente",
    detail: "Existem diferenças na conciliação das linhas de detalhe.",
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

function BalanceTreeRow({
  row,
  onOpenComponents,
}: {
  row: DeclaredBalanceRow;
  onOpenComponents: (row: DeclaredBalanceRow) => void;
}) {
  const [isOpen, setIsOpen] = useState(true);
  const isTotalizer = row.aggregation_code_type === "T";
  const lineStatus = row.reconciliation_status
    ? LINE_STATUS[row.reconciliation_status]
    : null;

  return (
    <div
      className={`declared-balance-node ${isTotalizer ? "is-totalizer" : "is-detail"}`}
      data-level={row.aggregation_level}
      style={{ "--node-level": row.aggregation_level } as CSSProperties}
    >
      <div className="declared-balance-row">
        <div className="declared-balance-main">
          {row.children.length > 0 ? (
            <button
              type="button"
              className="tree-toggle"
              aria-expanded={isOpen}
              aria-label={`${isOpen ? "Recolher" : "Expandir"} ${row.description}`}
              onClick={() => setIsOpen((current) => !current)}
            >
              {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>
          ) : (
            <span className="tree-toggle-spacer" aria-hidden="true" />
          )}

          <div className="declared-balance-description">
            <div className="declared-balance-title-line">
              <strong>{row.description}</strong>
              {lineStatus && (
                <span className="status-badge" data-variant={lineStatus.variant}>
                  {lineStatus.label}
                </span>
              )}
              {row.structural_status === "INVALIDA" && (
                <span className="status-badge" data-variant="danger">
                  Estrutura inválida
                </span>
              )}
            </div>
            <span className="declared-balance-code tnum">
              Aglutinação {row.aggregation_code}
            </span>
            <span className="declared-balance-initial tnum">
              Saldo inicial: {formatCurrency(row.initial_amount)}{" "}
              {row.initial_debit_credit_indicator}
            </span>
          </div>
        </div>

        <div className="declared-balance-values">
          <strong className="declared-balance-final tnum">
            {formatCurrency(row.final_amount)}
          </strong>
          <span className="declared-balance-indicator">
            Saldo final {row.final_debit_credit_indicator}
          </span>
          {row.difference !== null && row.reconciliation_status !== "CONCILIADA" && (
            <span className="declared-balance-difference tnum">
              Diferença: {formatCurrency(row.difference)}
            </span>
          )}
        </div>

        <div className="declared-balance-action">
          {!isTotalizer && row.component_count > 0 ? (
            <button
              type="button"
              className="button-ghost button-sm"
              onClick={() => onOpenComponents(row)}
            >
              <ClipboardCheck aria-hidden="true" size={16} />
              Ver componentes ({row.component_count})
            </button>
          ) : !isTotalizer ? (
            <span className="component-empty">Sem componentes</span>
          ) : null}
        </div>
      </div>

      {isOpen && row.children.length > 0 && (
        <div className="declared-balance-children">
          {row.children.map((child) => (
            <BalanceTreeRow
              key={child.aggregation_code}
              row={child}
              onOpenComponents={onOpenComponents}
            />
          ))}
        </div>
      )}
    </div>
  );
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

  useEffect(() => {
    if (!selectedRow) {
      return;
    }

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setSelectedRow(null);
      }
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [selectedRow]);

  const closeComponents = () => {
    setSelectedRow(null);
    setComponents(null);
    setComponentsError(false);
  };

  const openComponents = async (row: DeclaredBalanceRow) => {
    setSelectedRow({
      aggregationCode: row.aggregation_code,
      description: row.description,
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
  const assetRows = balance.rows.filter((row) => row.balance_group === "A");
  const liabilityRows = balance.rows.filter((row) => row.balance_group === "P");

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
          <Link
            to={`/analises/${analysisId}/exercicios/${year}/auditoria`}
            className="button-secondary"
          >
            <ClipboardCheck aria-hidden="true" size={16} />
            Auditoria por conta
          </Link>
          <Link to="/importar-ecd" className="button-primary">
            <Upload aria-hidden="true" size={16} />
            Importar ECD
          </Link>
        </div>
      </header>

      <main className="app-content balance-dashboard-content">
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
              <dd>{balance.is_blocking ? "Bloqueado" : "Base liberada"}</dd>
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

        {balance.rows.length === 0 ? (
          <section className="dashboard-section state-card">
            <h2>Balanço declarado indisponível</h2>
            <p>Sem linhas J100 aplicáveis para apresentar.</p>
          </section>
        ) : (
          <section className="dashboard-section" aria-label="Árvore do J100">
            <div className="balance-header-row">
              <div>
                <h2 className="eyebrow">Demonstração oficial J100</h2>
                <p className="section-description">
                  Saldos finais declarados e conciliação automática das linhas de detalhe.
                </p>
              </div>
              <span className="declared-view-label">Visão declarada · sem ajustes</span>
            </div>

            <div className="declared-balance-columns">
              <section className="declared-balance-side" aria-labelledby="asset-heading">
                <header className="declared-side-header">
                  <div>
                    <span className="eyebrow">Lado do balanço</span>
                    <h3 id="asset-heading">Ativo</h3>
                  </div>
                  <strong className="tnum">
                    {balance.assets_final_amount === null
                      ? "Não disponível"
                      : formatCurrency(balance.assets_final_amount)}
                  </strong>
                </header>
                <div className="declared-tree">
                  {assetRows.map((row) => (
                    <BalanceTreeRow
                      key={row.aggregation_code}
                      row={row}
                      onOpenComponents={openComponents}
                    />
                  ))}
                </div>
              </section>

              <section
                className="declared-balance-side"
                aria-labelledby="liability-heading"
              >
                <header className="declared-side-header">
                  <div>
                    <span className="eyebrow">Lado do balanço</span>
                    <h3 id="liability-heading">Passivo e Patrimônio Líquido</h3>
                  </div>
                  <strong className="tnum">
                    {balance.liabilities_and_equity_final_amount === null
                      ? "Não disponível"
                      : formatCurrency(balance.liabilities_and_equity_final_amount)}
                  </strong>
                </header>
                <div className="declared-tree">
                  {liabilityRows.map((row) => (
                    <BalanceTreeRow
                      key={row.aggregation_code}
                      row={row}
                      onOpenComponents={openComponents}
                    />
                  ))}
                </div>
              </section>
            </div>
          </section>
        )}
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
              {componentsLoading && <p>Carregando componentes.</p>}
              {componentsError && (
                <p className="components-error">
                  Não foi possível consultar os componentes desta linha.
                </p>
              )}
              {!componentsLoading && !componentsError && components?.rows.length === 0 && (
                <p>Sem registros.</p>
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
