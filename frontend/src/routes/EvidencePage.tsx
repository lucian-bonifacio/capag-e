import {
  AlertCircle,
  CheckCircle2,
  Download,
  FileCheck2,
  Landmark,
  Pencil,
  Plus,
  RefreshCcw,
  Save,
  ShieldAlert,
  X,
} from "lucide-react";
import { FormEvent, useMemo, useState } from "react";

import type {
  AssetValuationList,
  AssetValuationUpdatePayload,
  Evidence,
  EvidenceCreatePayload,
  EvidenceList,
  EvidenceStatus,
  EvidenceUpdatePayload,
  MaterialityLevel,
  MethodComponent,
} from "../api/evidence";
import { evidenceExportUrl } from "../api/evidence";
import { formatCurrency } from "../lib/formatters";
import "./EvidencePage.css";

type Props = {
  analysisId: string;
  year: string;
  evidences?: EvidenceList;
  assets?: AssetValuationList;
  isLoading: boolean;
  isError: boolean;
  isSaving: boolean;
  errorMessage?: string;
  onRetry: () => void;
  onCreateEvidence: (payload: EvidenceCreatePayload) => Promise<void>;
  onUpdateEvidence: (
    evidenceId: string,
    payload: EvidenceUpdatePayload,
  ) => Promise<void>;
  onUpdateAsset: (
    assessmentId: string,
    payload: AssetValuationUpdatePayload,
  ) => Promise<void>;
};

type Tab = "evidences" | "assets";
type BadgeTone = "success" | "warning" | "danger" | "neutral";

const evidenceStatusLabels: Record<EvidenceStatus, string> = {
  nao_exigida: "Não exigida",
  pendente: "Pendente",
  informada: "Informada",
  validada: "Validada",
  dispensada_com_justificativa: "Dispensada",
  rejeitada: "Rejeitada",
};
const materialityLabels: Record<MaterialityLevel, string> = {
  baixa: "Baixa",
  media: "Média",
  alta: "Alta",
  critica: "Crítica",
};

function statusTone(evidence: Evidence): BadgeTone {
  if (evidence.blocks_final_report) return "danger";
  if (evidence.requires_reservation || evidence.evidence_status === "pendente") {
    return "warning";
  }
  if (evidence.evidence_status === "validada") return "success";
  return "neutral";
}

function formatPercent(value: string | null): string {
  if (value === null) return "Base indisponível";
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 2,
    style: "percent",
  }).format(Number(value));
}

function Modal({
  children,
  onClose,
  subtitle,
  title,
}: {
  children: React.ReactNode;
  onClose: () => void;
  subtitle: string;
  title: string;
}) {
  return (
    <div
      className="evidence-dialog-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
      role="presentation"
    >
      <section
        aria-labelledby="evidence-dialog-title"
        aria-modal="true"
        className="evidence-dialog"
        role="dialog"
      >
        <header className="evidence-dialog-header">
          <div>
            <h2 id="evidence-dialog-title">{title}</h2>
            <p>{subtitle}</p>
          </div>
          <button
            aria-label="Fechar"
            className="evidence-icon-button"
            onClick={onClose}
            title="Fechar"
            type="button"
          >
            <X aria-hidden="true" size={18} />
          </button>
        </header>
        {children}
      </section>
    </div>
  );
}

function EvidenceCreateDialog({
  isSaving,
  onClose,
  onSubmit,
}: {
  isSaving: boolean;
  onClose: () => void;
  onSubmit: (payload: EvidenceCreatePayload) => Promise<void>;
}) {
  const [component, setComponent] = useState<MethodComponent>("PLRA");
  const [status, setStatus] = useState<EvidenceStatus>("pendente");
  const [error, setError] = useState<string>();

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const justification = String(data.get("justification") ?? "").trim();
    if (status === "dispensada_com_justificativa" && !justification) {
      setError("A dispensa exige justificativa.");
      return;
    }
    setError(undefined);
    await onSubmit({
      scope_type: String(data.get("scopeType")) as EvidenceCreatePayload["scope_type"],
      scope_key: String(data.get("scopeKey")),
      adjustment_type: String(data.get("adjustmentType")),
      method_component: component,
      amount_impact: String(data.get("amountImpact")),
      impact_base_value: String(data.get("impactBase") || "").trim() || null,
      required_evidence_type:
        String(data.get("evidenceType") || "").trim() || null,
      evidence_status: status,
      analyst_justification: justification || null,
      review_notes: String(data.get("reviewNotes") || "").trim() || null,
      can_change_capag_status: data.get("changesStatus") === "on",
      can_reverse_prudential_sign: data.get("reversesSign") === "on",
    });
    onClose();
  }

  return (
    <Modal
      onClose={onClose}
      subtitle="A materialidade e os bloqueios serão calculados pelo backend."
      title="Nova evidência"
    >
      <form className="evidence-form" onSubmit={submit}>
        <div className="evidence-form-grid">
          <label>
            Componente
            <select value={component} onChange={(e) => setComponent(e.target.value as MethodComponent)}>
              {(["PLRA", "FCA", "ROA", "CAPAG-E"] as MethodComponent[]).map((item) => (
                <option key={item} value={item}>{item}</option>
              ))}
            </select>
          </label>
          <label>
            Escopo
            <select defaultValue="account" name="scopeType">
              <option value="account">Conta</option>
              <option value="methodology_group">Grupo metodológico</option>
              <option value="macrogroup">Macrogrupo</option>
              <option value="asset_valuation">Avaliação de ativo</option>
              <option value="manual_override">Override manual</option>
              <option value="capag_assessment">Assessment CAPAG-E</option>
            </select>
          </label>
          <label>
            Chave do escopo
            <input name="scopeKey" required />
          </label>
          <label>
            Tipo de ajuste
            <input name="adjustmentType" required />
          </label>
          <label>
            Impacto monetário
            <input inputMode="decimal" name="amountImpact" required />
          </label>
          <label>
            Valor-base
            <input inputMode="decimal" name="impactBase" />
          </label>
          <label>
            Status
            <select value={status} onChange={(e) => setStatus(e.target.value as EvidenceStatus)}>
              {Object.entries(evidenceStatusLabels).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </label>
          <label>
            Tipo de evidência
            <input name="evidenceType" />
          </label>
        </div>
        <label>
          Justificativa do analista
          <textarea name="justification" rows={3} />
        </label>
        <label>
          Notas de revisão
          <textarea name="reviewNotes" rows={2} />
        </label>
        <div className="evidence-checks">
          <label><input name="changesStatus" type="checkbox" /> Pode alterar o status CAPAG-E</label>
          <label><input name="reversesSign" type="checkbox" /> Pode inverter sinal prudencial</label>
        </div>
        {error ? <p className="form-error" role="alert">{error}</p> : null}
        <footer className="evidence-dialog-footer">
          <button className="button-secondary" onClick={onClose} type="button">Cancelar</button>
          <button className="button-primary" disabled={isSaving} type="submit">
            <Save aria-hidden="true" size={16} />
            {isSaving ? "Salvando..." : "Registrar"}
          </button>
        </footer>
      </form>
    </Modal>
  );
}

function EvidenceReviewDialog({
  evidence,
  isSaving,
  onClose,
  onSubmit,
}: {
  evidence: Evidence;
  isSaving: boolean;
  onClose: () => void;
  onSubmit: (payload: EvidenceUpdatePayload) => Promise<void>;
}) {
  const [status, setStatus] = useState(evidence.evidence_status);
  const [overrideEnabled, setOverrideEnabled] = useState(false);
  const [error, setError] = useState<string>();

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const justification = String(data.get("justification") ?? "").trim();
    const overrideJustification = String(data.get("overrideJustification") ?? "").trim();
    if (status === "dispensada_com_justificativa" && !justification) {
      setError("A dispensa exige justificativa.");
      return;
    }
    if (overrideEnabled && !overrideJustification) {
      setError("O override exige justificativa.");
      return;
    }
    setError(undefined);
    await onSubmit({
      required_evidence_type: String(data.get("evidenceType") || "").trim() || null,
      evidence_status: status,
      analyst_justification: justification || null,
      review_notes: String(data.get("reviewNotes") || "").trim() || null,
      materiality_override: overrideEnabled
        ? {
            materiality_level: String(data.get("overrideLevel")) as MaterialityLevel,
            justification: overrideJustification,
          }
        : null,
    });
    onClose();
  }

  return (
    <Modal
      onClose={onClose}
      subtitle={`${evidence.method_component} · ${evidence.scope_key}`}
      title="Revisar evidência"
    >
      <form className="evidence-form" onSubmit={submit}>
        <div className="evidence-readonly-band">
          <span>Materialidade atual</span>
          <strong>{materialityLabels[evidence.materiality_level]}</strong>
          <span>Impacto</span>
          <strong className="tnum">{formatCurrency(evidence.amount_impact)}</strong>
        </div>
        <div className="evidence-form-grid">
          <label>
            Status
            <select value={status} onChange={(e) => setStatus(e.target.value as EvidenceStatus)}>
              {Object.entries(evidenceStatusLabels).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </label>
          <label>
            Tipo de evidência
            <input defaultValue={evidence.required_evidence_type ?? ""} name="evidenceType" />
          </label>
        </div>
        <label>
          Justificativa do analista
          <textarea defaultValue={evidence.analyst_justification ?? ""} name="justification" rows={3} />
        </label>
        <label>
          Notas de revisão
          <textarea defaultValue={evidence.review_notes ?? ""} name="reviewNotes" rows={2} />
        </label>
        <label className="evidence-override-toggle">
          <input checked={overrideEnabled} onChange={(e) => setOverrideEnabled(e.target.checked)} type="checkbox" />
          Aplicar override de materialidade
        </label>
        {overrideEnabled ? (
          <div className="evidence-form-grid">
            <label>
              Nova materialidade
              <select defaultValue={evidence.materiality_level} name="overrideLevel">
                {Object.entries(materialityLabels).map(([value, label]) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </select>
            </label>
            <label>
              Justificativa do override
              <input name="overrideJustification" />
            </label>
          </div>
        ) : null}
        {error ? <p className="form-error" role="alert">{error}</p> : null}
        <footer className="evidence-dialog-footer">
          <button className="button-secondary" onClick={onClose} type="button">Cancelar</button>
          <button className="button-primary" disabled={isSaving} type="submit">
            <Save aria-hidden="true" size={16} />
            {isSaving ? "Salvando..." : "Salvar revisão"}
          </button>
        </footer>
      </form>
    </Modal>
  );
}

function AssetDialog({
  analysisId,
  evidences,
  isSaving,
  onClose,
  onSubmit,
  year,
}: {
  analysisId: string;
  evidences: Evidence[];
  isSaving: boolean;
  onClose: () => void;
  onSubmit: (assessmentId: string, payload: AssetValuationUpdatePayload) => Promise<void>;
  year: string;
}) {
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const accountCode = String(data.get("accountCode"));
    await onSubmit(`asset-${accountCode}`, {
      analysis_id: analysisId,
      exercise_year: Number(year),
      account_code: accountCode,
      realizability_classification: String(data.get("realizability")),
      valuation_required: data.get("required") === "on",
      valuation_basis: String(data.get("basis")),
      forced_liquidation_value: String(data.get("forcedValue") || "").trim() || null,
      analyst_adjusted_value: String(data.get("analystValue") || "").trim() || null,
      essentiality_status: String(data.get("essentiality")),
      valuation_status: String(data.get("status")),
      evidence_id: String(data.get("evidenceId") || "").trim() || null,
    });
    onClose();
  }

  return (
    <Modal
      onClose={onClose}
      subtitle="O valor contábil e o deságio serão obtidos da ECD e da política vigente."
      title="Registrar avaliação de ativo"
    >
      <form className="evidence-form" onSubmit={submit}>
        <div className="evidence-form-grid">
          <label>Conta ECD<input name="accountCode" required /></label>
          <label>
            Realizabilidade
            <select defaultValue="realizavel_longo_prazo" name="realizability">
              <option value="liquidez_imediata">Liquidez imediata</option>
              <option value="realizavel_curto_prazo">Curto prazo</option>
              <option value="realizavel_longo_prazo">Longo prazo</option>
              <option value="liquidacao_forcada_exige_laudo">Liquidação forçada</option>
              <option value="ativo_operacional_essencial">Ativo essencial</option>
              <option value="ativo_sem_realizabilidade">Sem realizabilidade</option>
              <option value="ativo_condicional">Condicional</option>
            </select>
          </label>
          <label>
            Base de avaliação
            <select defaultValue="politica_interna" name="basis">
              <option value="politica_interna">Política interna</option>
              <option value="laudo_abnt_nbr_14653">Laudo ABNT NBR 14653</option>
              <option value="documento_suporte">Documento suporte</option>
              <option value="estimativa_analista">Estimativa do analista</option>
              <option value="nao_aplicavel">Não aplicável</option>
            </select>
          </label>
          <label>
            Status
            <select defaultValue="pendente" name="status">
              <option value="nao_exigida">Não exigida</option>
              <option value="pendente">Pendente</option>
              <option value="validada">Validada</option>
              <option value="rejeitada">Rejeitada</option>
              <option value="bloqueante">Bloqueante</option>
            </select>
          </label>
          <label>Liquidação forçada<input inputMode="decimal" name="forcedValue" /></label>
          <label>Valor ajustado manual<input inputMode="decimal" name="analystValue" /></label>
          <label>
            Essencialidade
            <select defaultValue="nao_essencial" name="essentiality">
              <option value="nao_essencial">Não essencial</option>
              <option value="essencial">Essencial</option>
              <option value="em_revisao">Em revisão</option>
            </select>
          </label>
          <label>
            Evidência vinculada
            <select defaultValue="" name="evidenceId">
              <option value="">Sem vínculo</option>
              {evidences.map((evidence) => (
                <option key={evidence.evidence_id} value={evidence.evidence_id}>
                  {evidence.scope_key} · {evidenceStatusLabels[evidence.evidence_status]}
                </option>
              ))}
            </select>
          </label>
        </div>
        <label className="evidence-override-toggle">
          <input name="required" type="checkbox" /> Avaliação obrigatória
        </label>
        <footer className="evidence-dialog-footer">
          <button className="button-secondary" onClick={onClose} type="button">Cancelar</button>
          <button className="button-primary" disabled={isSaving} type="submit">
            <Save aria-hidden="true" size={16} />
            {isSaving ? "Salvando..." : "Registrar avaliação"}
          </button>
        </footer>
      </form>
    </Modal>
  );
}

export function EvidencePage({
  analysisId,
  assets,
  errorMessage,
  evidences,
  isError,
  isLoading,
  isSaving,
  onCreateEvidence,
  onRetry,
  onUpdateAsset,
  onUpdateEvidence,
  year,
}: Props) {
  const [tab, setTab] = useState<Tab>("evidences");
  const [component, setComponent] = useState<MethodComponent | "all">("all");
  const [status, setStatus] = useState<EvidenceStatus | "all">("all");
  const [createOpen, setCreateOpen] = useState(false);
  const [assetOpen, setAssetOpen] = useState(false);
  const [selected, setSelected] = useState<Evidence>();

  const filtered = useMemo(
    () =>
      (evidences?.items ?? []).filter(
        (item) =>
          (component === "all" || item.method_component === component) &&
          (status === "all" || item.evidence_status === status),
      ),
    [component, evidences, status],
  );
  const totalBlocking = evidences?.summaries.reduce((sum, item) => sum + item.blocking, 0) ?? 0;
  const totalReservations = evidences?.summaries.reduce((sum, item) => sum + item.reservations, 0) ?? 0;

  return (
    <>
      <header className="app-topbar">
        <div>
          <h1 className="app-title">Evidências e avaliação de ativos</h1>
          <p className="app-subtitle">
            Análise <span className="tnum">{analysisId}</span> · Exercício <span className="tnum">{year}</span>
          </p>
        </div>
        <div className="evidence-topbar-actions">
          <a className="button-secondary" href={evidenceExportUrl(analysisId, year)}>
            <Download aria-hidden="true" size={16} />
            Exportar Excel
          </a>
          <button
            className="button-primary"
            onClick={() => tab === "evidences" ? setCreateOpen(true) : setAssetOpen(true)}
            type="button"
          >
            <Plus aria-hidden="true" size={16} />
            {tab === "evidences" ? "Nova evidência" : "Registrar avaliação"}
          </button>
        </div>
      </header>

      <main className="app-content evidence-content">
        <section aria-label="Resumo documental" className="evidence-summary">
          <div><FileCheck2 aria-hidden="true" size={18} /><span>Evidências</span><strong className="tnum">{evidences?.items.length ?? 0}</strong></div>
          <div><ShieldAlert aria-hidden="true" size={18} /><span>Bloqueios</span><strong className="tnum">{totalBlocking}</strong></div>
          <div><AlertCircle aria-hidden="true" size={18} /><span>Ressalvas</span><strong className="tnum">{totalReservations}</strong></div>
          <div><Landmark aria-hidden="true" size={18} /><span>Ativos bloqueados</span><strong className="tnum">{assets?.blocking_count ?? 0}</strong></div>
        </section>

        <div className="evidence-tabs" role="tablist">
          <button aria-selected={tab === "evidences"} onClick={() => setTab("evidences")} role="tab" type="button">Evidências <span className="tnum">{evidences?.items.length ?? 0}</span></button>
          <button aria-selected={tab === "assets"} onClick={() => setTab("assets")} role="tab" type="button">Avaliação de ativos <span className="tnum">{assets?.items.length ?? 0}</span></button>
        </div>

        {isLoading ? (
          <section aria-label="Carregando evidências" className="app-panel evidence-state">
            <div className="skeleton-row" /><div className="skeleton-table" />
          </section>
        ) : null}
        {!isLoading && isError ? (
          <section className="app-panel evidence-state" role="alert">
            <AlertCircle aria-hidden="true" size={22} />
            <div><h2>Erro ao consultar evidências</h2><p>{errorMessage ?? "A consulta não pôde ser concluída."}</p>
              <button className="button-secondary" onClick={onRetry} type="button"><RefreshCcw aria-hidden="true" size={16} />Tentar novamente</button>
            </div>
          </section>
        ) : null}

        {!isLoading && !isError && tab === "evidences" ? (
          <section className="evidence-workspace">
            <div className="evidence-toolbar">
              <label>Componente<select value={component} onChange={(e) => setComponent(e.target.value as MethodComponent | "all")}><option value="all">Todos</option>{(["PLRA", "FCA", "ROA", "CAPAG-E"] as MethodComponent[]).map((item) => <option key={item}>{item}</option>)}</select></label>
              <label>Status<select value={status} onChange={(e) => setStatus(e.target.value as EvidenceStatus | "all")}><option value="all">Todos</option>{Object.entries(evidenceStatusLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
            </div>
            {filtered.length === 0 ? <div className="app-panel evidence-empty">Sem registros.</div> : (
              <div className="evidence-table-wrap">
                <table className="evidence-table">
                  <thead><tr><th>Escopo</th><th>Componente</th><th className="numeric">Impacto</th><th>Materialidade</th><th>Status</th><th>Decisão</th><th aria-label="Ações" /></tr></thead>
                  <tbody>{filtered.map((item) => (
                    <tr key={item.evidence_id}>
                      <td><strong>{item.scope_key}</strong><small>{item.adjustment_type} · {item.scope_type}</small></td>
                      <td>{item.method_component}</td>
                      <td className="numeric"><strong className="tnum">{formatCurrency(item.amount_impact)}</strong><small className="tnum">{formatPercent(item.impact_percent)}</small></td>
                      <td><strong>{materialityLabels[item.materiality_level]}</strong><small>{item.materiality_source === "override_manual" ? "Override manual" : "Política default"}</small></td>
                      <td><span className="status-badge" data-variant={statusTone(item)}>{evidenceStatusLabels[item.evidence_status]}</span></td>
                      <td>{item.blocks_final_report ? <span className="evidence-decision danger">Bloqueia resultado</span> : item.requires_reservation ? <span className="evidence-decision warning">Exige ressalva</span> : <span className="evidence-decision success"><CheckCircle2 aria-hidden="true" size={14} />Regular</span>}</td>
                      <td><button aria-label={`Revisar ${item.scope_key}`} className="evidence-icon-button" onClick={() => setSelected(item)} title="Revisar evidência" type="button"><Pencil aria-hidden="true" size={16} /></button></td>
                    </tr>
                  ))}</tbody>
                </table>
              </div>
            )}
          </section>
        ) : null}

        {!isLoading && !isError && tab === "assets" ? (
          <section className="evidence-workspace">
            {(assets?.items.length ?? 0) === 0 ? <div className="app-panel evidence-empty">Sem avaliações registradas.</div> : (
              <div className="evidence-table-wrap">
                <table className="evidence-table asset-table">
                  <thead><tr><th>Ativo</th><th className="numeric">Valor contábil</th><th className="numeric">Deságio</th><th className="numeric">Valor default</th><th className="numeric">Valor avaliado</th><th>Status</th></tr></thead>
                  <tbody>{assets?.items.map((asset) => (
                    <tr key={asset.assessment_id}>
                      <td><strong>{asset.account_name}</strong><small className="tnum">{asset.account_code} · {asset.reference_code}</small></td>
                      <td className="numeric tnum">{formatCurrency(asset.book_value)}</td>
                      <td className="numeric tnum">{formatPercent(asset.default_desagio_percent)}</td>
                      <td className="numeric tnum">{formatCurrency(asset.default_economic_value)}</td>
                      <td className="numeric"><strong className="tnum">{formatCurrency(asset.final_economic_value)}</strong><small>{asset.final_value_source}</small></td>
                      <td><span className="status-badge" data-variant={asset.blocks_plra ? "danger" : "success"}>{asset.blocks_plra ? "Bloqueia PLRA" : asset.valuation_status}</span>{asset.blocking_reasons.map((reason) => <small key={reason}>{reason}</small>)}</td>
                    </tr>
                  ))}</tbody>
                </table>
              </div>
            )}
          </section>
        ) : null}
      </main>

      {createOpen ? <EvidenceCreateDialog isSaving={isSaving} onClose={() => setCreateOpen(false)} onSubmit={onCreateEvidence} /> : null}
      {selected ? <EvidenceReviewDialog evidence={selected} isSaving={isSaving} onClose={() => setSelected(undefined)} onSubmit={(payload) => onUpdateEvidence(selected.evidence_id, payload)} /> : null}
      {assetOpen ? <AssetDialog analysisId={analysisId} evidences={evidences?.items ?? []} isSaving={isSaving} onClose={() => setAssetOpen(false)} onSubmit={onUpdateAsset} year={year} /> : null}
    </>
  );
}
