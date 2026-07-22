export type DeclaredLayerSummary = {
  analysis_id: string;
  year: number;
  total_accounts: number;
  methodology_version_id: string | null;
  status_counts: Record<string, number>;
};

export type DeclaredAccount = {
  account_code: string;
  account_name: string;
  account_type: string | null;
  account_nature: string | null;
  account_level: number | null;
  parent_account_code: string | null;
  account_order: number | null;
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

export type DeclaredBalanceConsistencyWarning = {
  warning_code: string;
  account_code: string;
  account_name: string;
  message: string;
};

export type DeclaredAccountsResponse = {
  analysis_id: string;
  year: number;
  accounts: DeclaredAccount[];
  consistency_warnings?: DeclaredBalanceConsistencyWarning[];
};

export type EcdImportResponse = {
  analysis_id: string;
  company_id: string;
  ecd_file_id: string;
  year: number;
  methodology_version_id: string;
  status: string;
};

export type ExistingEcdImport = EcdImportResponse & {
  original_filename: string;
  content_hash: string;
  layout: string;
  period_start: string;
  period_end: string;
  imported_at: string;
};

export type EcdImportListResponse = {
  imports: ExistingEcdImport[];
};

export type EcdImportDeleteResponse = {
  ecd_file_id: string;
  analysis_id: string;
  deleted: boolean;
};

export type DeclaredRunResponse = {
  analysis_id: string;
  year: number;
  status: string;
  snapshots_created: number;
  status_counts: Record<string, number>;
};

export class EcdImportConflictError extends Error {
  existingImport: ExistingEcdImport;

  constructor(message: string, existingImport: ExistingEcdImport) {
    super(message);
    this.name = "EcdImportConflictError";
    this.existingImport = existingImport;
  }
}

async function parseApiError(response: Response): Promise<Error> {
  try {
    const body = (await response.json()) as {
      detail?: {
        error_code?: string;
        existing_import?: ExistingEcdImport;
        message?: string;
      };
      message?: string;
    };
    const message = body.detail?.message ?? body.message ?? `HTTP ${response.status}`;

    if (
      response.status === 409 &&
      body.detail?.error_code === "ECD_ALREADY_IMPORTED" &&
      body.detail.existing_import
    ) {
      return new EcdImportConflictError(message, body.detail.existing_import);
    }

    return new Error(message);
  } catch {
    return new Error(`HTTP ${response.status}`);
  }
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);

  if (!response.ok) {
    throw await parseApiError(response);
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

export function fetchDeclaredBalanceAccounts(
  analysisId: string,
  year: string,
): Promise<DeclaredAccountsResponse> {
  return fetchJson<DeclaredAccountsResponse>(
    `/api/v1/analyses/${analysisId}/exercises/${year}/declared/balance/accounts`,
  );
}

export function importEcd(file: File): Promise<EcdImportResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return fetchJson<EcdImportResponse>("/api/v1/ecd/import", {
    body: formData,
    method: "POST",
  });
}

export function fetchEcdImports(): Promise<EcdImportListResponse> {
  return fetchJson<EcdImportListResponse>("/api/v1/ecd/imports");
}

export function deleteEcdImport(ecdFileId: string): Promise<EcdImportDeleteResponse> {
  return fetchJson<EcdImportDeleteResponse>(`/api/v1/ecd/imports/${ecdFileId}`, {
    method: "DELETE",
  });
}

export function runDeclaredLayer(
  analysisId: string,
  year: number,
): Promise<DeclaredRunResponse> {
  return fetchJson<DeclaredRunResponse>(
    `/api/v1/analyses/${analysisId}/exercises/${year}/declared/run`,
    { method: "POST" },
  );
}
