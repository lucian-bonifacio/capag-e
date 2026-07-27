import type { ComponentStatus } from "./capag";

export type DfcActivity =
  | "operacional"
  | "investimento"
  | "financiamento"
  | "nao_classificado";

export type DfcRowStatus =
  | "incluido"
  | "excluido"
  | "nao_classificado"
  | "fluxo_incompativel"
  | "pendente_evidencia"
  | "decisao_manual_aplicada";

export type DfcComponentSummary = {
  activity: Exclude<DfcActivity, "nao_classificado">;
  component_code: string;
  component_label: string;
  value: string;
  movement_count: number;
};

export type DfcAuditRow = {
  entry_number: string;
  entry_date: string | null;
  cash_account_code: string;
  cash_flow_direction: "entrada" | "saida";
  counterparty_account_code: string;
  counterparty_account_name: string;
  counterparty_reference_code: string | null;
  dfc_activity: DfcActivity;
  dfc_component_code: string | null;
  dfc_component_label: string | null;
  movement_value: string;
  included_value: string;
  final_status: DfcRowStatus;
  pending_reason: string | null;
  history: string | null;
  line_number: number;
};

export type DfcPendingIssue = {
  code: string;
  message: string;
  entry_number: string | null;
  line_number: number | null;
  materiality_level: string | null;
  blocks_fca: boolean;
};

export type DfcCalculation = {
  exercise_year: number;
  automatic_value: string;
  operational_flow: string;
  investment_flow: string;
  financing_flow: string;
  manual_adjustments_value: string;
  fca_value: string;
  fca_status: ComponentStatus;
  component_summaries: DfcComponentSummary[];
  audit_rows: DfcAuditRow[];
  pending_issues: DfcPendingIssue[];
  alerts: string[];
  limitations: string[];
  methodology_version_id: string;
};

export type DfcDecisionPayload =
  | {
      action: "incluir";
      entry_number: string;
      line_number: number;
      activity: Exclude<DfcActivity, "nao_classificado">;
      component_code: string;
      justification: string;
      evidence_id?: string;
    }
  | {
      action: "excluir";
      entry_number: string;
      line_number: number;
      justification: string;
      evidence_id?: string;
    };

export class DfcApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "DfcApiError";
    this.status = status;
  }
}

export function fetchDfc(
  analysisId: string,
  year: string,
): Promise<DfcCalculation> {
  return fetchJson<DfcCalculation>(baseUrl(analysisId, year));
}

export function runDfc(
  analysisId: string,
  year: string,
): Promise<DfcCalculation> {
  return fetchJson<DfcCalculation>(`${baseUrl(analysisId, year)}/run`, {
    method: "POST",
  });
}

export function createDfcDecision(
  analysisId: string,
  year: string,
  payload: DfcDecisionPayload,
): Promise<DfcCalculation> {
  return fetchJson<DfcCalculation>(`${baseUrl(analysisId, year)}/decisions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function dfcExportUrl(analysisId: string, year: string): string {
  return `${baseUrl(analysisId, year)}/export.xlsx`;
}

function baseUrl(analysisId: string, year: string): string {
  return `/api/v1/analyses/${encodeURIComponent(analysisId)}/exercises/${encodeURIComponent(year)}/dfc`;
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  if (!response.ok) {
    throw new DfcApiError(response.status, await parseErrorMessage(response));
  }
  return response.json() as Promise<T>;
}

async function parseErrorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as {
      detail?: { message?: string };
      message?: string;
    };
    return body.detail?.message ?? body.message ?? `HTTP ${response.status}`;
  } catch {
    return `HTTP ${response.status}`;
  }
}
