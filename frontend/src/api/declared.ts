export type DeclaredLayerSummary = {
  analysis_id: number;
  year: number;
  accounts_count: number;
  methodology_version_id: string | null;
  status_counts: Record<string, number>;
};

export type DeclaredAccount = {
  account_code: string;
  account_name: string;
  declared_reference_code: string | null;
  official_description: string | null;
  official_reference_status: string | null;
  methodology_rule_applied: string | null;
  methodology_rule_status: string | null;
  purpose: string | null;
  plra_category: string | null;
  fco_category: string | null;
  capag_category: string | null;
  flow_nature: string | null;
  treatment: string | null;
  base_value: string;
  considered_value: string;
  final_status: string;
  observation: string | null;
  recommended_action: string | null;
  methodology_version_id: string;
};

export type DeclaredAccountsResponse = {
  analysis_id: number;
  year: number;
  accounts: DeclaredAccount[];
};

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Falha ao consultar API declarada: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchDeclaredSummary(
  analysisId: string,
  year: string,
): Promise<DeclaredLayerSummary> {
  return fetchJson<DeclaredLayerSummary>(
    `/api/v1/analyses/${analysisId}/exercises/${year}/declared`,
  );
}

export function fetchDeclaredAccounts(
  analysisId: string,
  year: string,
): Promise<DeclaredAccountsResponse> {
  return fetchJson<DeclaredAccountsResponse>(
    `/api/v1/analyses/${analysisId}/exercises/${year}/declared/accounts`,
  );
}
