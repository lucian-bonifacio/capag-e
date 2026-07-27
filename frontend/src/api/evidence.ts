export type MethodComponent = "PLRA" | "FCA" | "ROA" | "CAPAG-E";
export type EvidenceStatus =
  | "nao_exigida"
  | "pendente"
  | "informada"
  | "validada"
  | "dispensada_com_justificativa"
  | "rejeitada";
export type MaterialityLevel = "baixa" | "media" | "alta" | "critica";
export type EvidenceScopeType =
  | "account"
  | "methodology_group"
  | "macrogroup"
  | "fco_movement"
  | "dfc_component"
  | "roa_component"
  | "asset_valuation"
  | "manual_override"
  | "capag_assessment";

export type Evidence = {
  evidence_id: string;
  exercise_year: number;
  scope_type: EvidenceScopeType;
  scope_key: string;
  adjustment_type: string;
  method_component: MethodComponent;
  amount_impact: string;
  impact_base_value: string | null;
  impact_percent: string | null;
  materiality_level: MaterialityLevel;
  materiality_source: "politica_default" | "override_manual";
  minimum_materiality_level: MaterialityLevel;
  required_evidence_type: string | null;
  evidence_status: EvidenceStatus;
  analyst_justification: string | null;
  review_notes: string | null;
  blocks_final_report: boolean;
  requires_reservation: boolean;
  human_review_required: boolean;
  decision_reasons: string[];
  materiality_overrides: Array<{
    before: MaterialityLevel;
    after: MaterialityLevel;
    justification: string;
    overridden_at: string;
  }>;
  methodology_version_id: string;
};

export type EvidenceList = {
  items: Evidence[];
  summaries: Array<{
    method_component: MethodComponent;
    total: number;
    blocking: number;
    reservations: number;
    pending: number;
  }>;
};

export type EvidenceCreatePayload = {
  scope_type: EvidenceScopeType;
  scope_key: string;
  adjustment_type: string;
  method_component: MethodComponent;
  amount_impact: string;
  impact_base_value: string | null;
  required_evidence_type: string | null;
  evidence_status: EvidenceStatus;
  analyst_justification: string | null;
  review_notes: string | null;
  can_change_capag_status: boolean;
  can_reverse_prudential_sign: boolean;
};

export type EvidenceUpdatePayload = {
  required_evidence_type: string | null;
  evidence_status: EvidenceStatus;
  analyst_justification: string | null;
  review_notes: string | null;
  materiality_override: {
    materiality_level: MaterialityLevel;
    justification: string;
  } | null;
};

export type AssetValuation = {
  assessment_id: string;
  exercise_year: number;
  account_code: string;
  account_name: string;
  reference_code: string;
  macrogroup: string;
  book_value: string;
  default_desagio_percent: string;
  default_economic_value: string;
  valuation_required: boolean;
  realizability_classification: string;
  valuation_basis: string;
  forced_liquidation_value: string | null;
  analyst_adjusted_value: string | null;
  final_economic_value: string;
  final_value_source: string;
  essentiality_status: string;
  evidence_id: string | null;
  valuation_status: string;
  blocks_plra: boolean;
  blocking_reasons: string[];
  methodology_version_id: string;
};

export type AssetValuationList = {
  items: AssetValuation[];
  blocking_count: number;
};

export type AssetValuationUpdatePayload = {
  analysis_id: string;
  exercise_year: number;
  account_code: string;
  realizability_classification: string;
  valuation_required: boolean;
  valuation_basis: string;
  forced_liquidation_value: string | null;
  analyst_adjusted_value: string | null;
  essentiality_status: string;
  valuation_status: string;
  evidence_id: string | null;
};

export class EvidenceApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "EvidenceApiError";
    this.status = status;
  }
}

export async function fetchEvidences(
  analysisId: string,
  year: string,
): Promise<EvidenceList> {
  return requestJson(
    `/api/v1/analyses/${encodeURIComponent(analysisId)}/exercises/${encodeURIComponent(year)}/evidences`,
  );
}

export async function createEvidence(
  analysisId: string,
  year: string,
  payload: EvidenceCreatePayload,
): Promise<Evidence> {
  return requestJson(
    `/api/v1/analyses/${encodeURIComponent(analysisId)}/exercises/${encodeURIComponent(year)}/evidences`,
    { body: JSON.stringify(payload), method: "POST" },
  );
}

export async function updateEvidence(
  evidenceId: string,
  payload: EvidenceUpdatePayload,
): Promise<Evidence> {
  return requestJson(`/api/v1/evidences/${encodeURIComponent(evidenceId)}`, {
    body: JSON.stringify(payload),
    method: "PUT",
  });
}

export async function fetchAssetValuations(
  analysisId: string,
  year: string,
): Promise<AssetValuationList> {
  return requestJson(
    `/api/v1/analyses/${encodeURIComponent(analysisId)}/exercises/${encodeURIComponent(year)}/assets/valuations`,
  );
}

export function evidenceExportUrl(
  analysisId: string,
  year: string,
): string {
  return `/api/v1/analyses/${encodeURIComponent(analysisId)}/exercises/${encodeURIComponent(year)}/evidences/export.xlsx`;
}

export async function updateAssetValuation(
  assessmentId: string,
  payload: AssetValuationUpdatePayload,
): Promise<AssetValuation> {
  return requestJson(
    `/api/v1/assets/valuations/${encodeURIComponent(assessmentId)}`,
    { body: JSON.stringify(payload), method: "PUT" },
  );
}

async function requestJson<T>(
  input: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(input, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!response.ok) {
    let message = "A operação de evidências não pôde ser concluída.";
    try {
      const payload = await response.json();
      message = payload.detail?.message ?? message;
    } catch {
      // Keep the stable fallback for non-JSON failures.
    }
    throw new EvidenceApiError(response.status, message);
  }
  return response.json() as Promise<T>;
}
