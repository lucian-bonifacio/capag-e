import type { ComponentStatus } from "./capag";
import type { DeclaredBalanceStatus } from "./declared";

export type PlraInclusionStatus =
  | "incluido_ativo"
  | "incluido_passivo"
  | "excluido"
  | "pendente"
  | "ignorado_hierarquia"
  | "sem_vinculo_referencial"
  | "nao_patrimonial";

export type PlraDecisionStatus =
  | "automatica"
  | "validada"
  | "pendente"
  | "nao_aplicavel";

export type PlraCalculation = {
  analysis_id: string;
  exercise_year: number;
  gross_assets_value: string;
  gross_economic_liabilities_value: string;
  adjusted_assets_value: string;
  plr_gross_value: string;
  plra_value: string;
  plra_status: ComponentStatus;
  calculation_formula: string;
  pending_accounts: string[];
  warnings: string[];
  limitations: string[];
  blocking_issues: string[];
  balance_status: DeclaredBalanceStatus;
  methodology_version_id: string;
  calculated_at: string;
};

export type PlraAuditRow = {
  account_code: string;
  account_name: string;
  account_type: string | null;
  account_level: number | null;
  parent_account_code: string | null;
  declared_reference_code: string | null;
  official_description: string | null;
  methodology_rule_id: string | null;
  methodology_group: string | null;
  macrogroup: string | null;
  base_value: string;
  sign: string;
  inclusion_status: PlraInclusionStatus;
  default_discount_percent: string | null;
  default_economic_value: string;
  valuation_source: string | null;
  validated_valuation_value: string | null;
  final_economic_value: string;
  decision_status: PlraDecisionStatus;
  evidence_status: string | null;
  reason: string;
  limitations: string[];
  methodology_version_id: string;
};

export type PlraAudit = {
  analysis_id: string;
  exercise_year: number;
  plra_status: ComponentStatus;
  methodology_version_id: string;
  rows: PlraAuditRow[];
};

export class PlraApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "PlraApiError";
    this.status = status;
  }
}

export function fetchPlra(
  analysisId: string,
  year: string,
): Promise<PlraCalculation> {
  return fetchJson<PlraCalculation>(baseUrl(analysisId, year));
}

export function runPlra(
  analysisId: string,
  year: string,
): Promise<PlraCalculation> {
  return fetchJson<PlraCalculation>(`${baseUrl(analysisId, year)}/run`, {
    method: "POST",
  });
}

export function fetchPlraAudit(
  analysisId: string,
  year: string,
): Promise<PlraAudit> {
  return fetchJson<PlraAudit>(`${baseUrl(analysisId, year)}/audit`);
}

export function plraExportUrl(analysisId: string, year: string): string {
  return `${baseUrl(analysisId, year)}/export.xlsx`;
}

function baseUrl(analysisId: string, year: string): string {
  return `/api/v1/analyses/${analysisId}/exercises/${year}/plra`;
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  if (!response.ok) {
    throw new PlraApiError(response.status, await parseErrorMessage(response));
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
