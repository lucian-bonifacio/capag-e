import type { CapagAssessment, ComponentStatus } from "./capag";

export type RoaBlock =
  | "receita_bruta"
  | "deducoes_receita"
  | "tributos_receita"
  | "custos_operacionais"
  | "despesas_operacionais"
  | "resultado_financeiro"
  | "resultado_nao_operacional"
  | "pressoes_complementares_caixa";

export type RoaRowStatus =
  | "incluido"
  | "excluido"
  | "pendente_revisao"
  | "sem_regra"
  | "pendente_evidencia"
  | "decisao_manual_aplicada";

export type RoaComponentSummary = {
  block: RoaBlock;
  component_code: string;
  component_label: string;
  value: string;
  account_count: number;
};

export type RoaAuditRow = {
  account_code: string;
  account_name: string;
  reference_code: string | null;
  reference_description: string | null;
  roa_block: RoaBlock | null;
  component_roa: string | null;
  component_label: string | null;
  base_value: string;
  signed_value: string;
  treatment: string;
  final_status: RoaRowStatus;
  pending_reason: string | null;
  evidence_id: string | null;
  line_reference: number;
  macrogroup: string | null;
  required_evidence_type: string | null;
  source_detail: string | null;
};

export type RoaPendingGroup = {
  code: string;
  message: string;
  account_code: string | null;
  reference_code: string | null;
  blocks_roa: boolean;
  materiality_level: string | null;
  evidence_id: string | null;
};

export type RoaCalculation = {
  exercise_year: number;
  gross_revenue: string;
  deductions: string;
  revenue_taxes: string;
  net_operating_revenue: string;
  operating_costs: string;
  operating_expenses: string;
  financial_result: string;
  non_operating_result: string;
  cash_pressure_adjustments: string;
  roa_preliminary: string;
  roa_final: string;
  roa_status: ComponentStatus;
  component_summaries: RoaComponentSummary[];
  audit_rows: RoaAuditRow[];
  pending_groups: RoaPendingGroup[];
  alerts: string[];
  limitations: string[];
  methodology_version_id: string;
  capag_assessment: CapagAssessment | null;
};

export type RoaDecisionPayload = {
  action: "incluir" | "excluir";
  account_code: string;
  justification: string;
  evidence_id?: string;
};

export class RoaApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "RoaApiError";
    this.status = status;
  }
}

export function fetchRoa(
  analysisId: string,
  year: string,
): Promise<RoaCalculation> {
  return fetchJson<RoaCalculation>(baseUrl(analysisId, year));
}

export function runRoa(
  analysisId: string,
  year: string,
): Promise<RoaCalculation> {
  return fetchJson<RoaCalculation>(`${baseUrl(analysisId, year)}/run`, {
    method: "POST",
  });
}

export function createRoaDecision(
  analysisId: string,
  year: string,
  payload: RoaDecisionPayload,
): Promise<RoaCalculation> {
  return fetchJson<RoaCalculation>(`${baseUrl(analysisId, year)}/decisions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function roaExportUrl(analysisId: string, year: string): string {
  return `${baseUrl(analysisId, year)}/export.xlsx`;
}

function baseUrl(analysisId: string, year: string): string {
  return `/api/v1/analyses/${encodeURIComponent(analysisId)}/exercises/${encodeURIComponent(year)}/roa`;
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  if (!response.ok) {
    throw new RoaApiError(response.status, await parseErrorMessage(response));
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
