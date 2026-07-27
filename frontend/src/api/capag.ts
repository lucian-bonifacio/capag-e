export type CapagEMethod =
  | "fca_plra"
  | "roa_plra"
  | "comparativo_fca_roa"
  | "nao_definido";

export type ComponentStatus =
  | "nao_calculado"
  | "calculado"
  | "parcial"
  | "bloqueado_por_pendencia"
  | "bloqueado_por_evidencia"
  | "erro_metodologico";

export type CapagEStatus =
  | "nao_calculado"
  | "parcial"
  | "calculado"
  | "bloqueado"
  | "indisponivel"
  | "erro_metodologico";

export type CapagAssessment = {
  exercise_year: number;
  method: CapagEMethod;
  plra_value: string | null;
  plra_status: ComponentStatus;
  fca_value: string | null;
  fca_status: ComponentStatus;
  roa_value: string | null;
  roa_status: ComponentStatus;
  capag_e_value: string | null;
  capag_e_status: CapagEStatus;
  unavailable_reason: string | null;
  calculation_basis: string;
  methodology_formula: string;
  warnings: string[];
  limitations: string[];
  blocking_issues: string[];
  methodology_version_id: string;
};

export class CapagApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "CapagApiError";
    this.status = status;
  }
}

export async function fetchCapagAssessment(
  analysisId: string,
  year: string,
): Promise<CapagAssessment> {
  const response = await fetch(
    `/api/v1/analyses/${analysisId}/exercises/${year}/capag-assessment`,
  );
  if (!response.ok) {
    throw new CapagApiError(response.status, await parseErrorMessage(response));
  }
  return response.json() as Promise<CapagAssessment>;
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
