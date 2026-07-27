import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import type {
  AssetValuationList,
  Evidence,
  EvidenceList,
} from "../api/evidence";


const evidence: Evidence = {
  evidence_id: "evidence-1",
  exercise_year: 2024,
  scope_type: "account",
  scope_key: "asset-1",
  adjustment_type: "avaliacao_ativo",
  method_component: "PLRA",
  amount_impact: "100.00",
  impact_base_value: "1000.00",
  impact_percent: "0.100000",
  materiality_level: "critica",
  materiality_source: "politica_default",
  minimum_materiality_level: "baixa",
  required_evidence_type: "laudo_abnt_nbr_14653",
  evidence_status: "pendente",
  analyst_justification: "Avaliação em andamento.",
  review_notes: null,
  blocks_final_report: true,
  requires_reservation: false,
  human_review_required: false,
  decision_reasons: ["EVIDENCIA_PENDENTE"],
  materiality_overrides: [],
  methodology_version_id: "metodologia-2024.1",
};

const evidenceList: EvidenceList = {
  items: [evidence],
  summaries: [
    {
      method_component: "PLRA",
      total: 1,
      blocking: 1,
      reservations: 0,
      pending: 1,
    },
  ],
};

const assets: AssetValuationList = {
  blocking_count: 1,
  items: [
    {
      assessment_id: "valuation-1",
      exercise_year: 2024,
      account_code: "asset-1",
      account_name: "Máquinas e equipamentos",
      reference_code: "1.02.03.01.06",
      macrogroup: "ATIVO_REALIZAVEL",
      book_value: "1000.00",
      default_desagio_percent: "0.800000",
      default_economic_value: "200.00",
      valuation_required: true,
      realizability_classification: "liquidacao_forcada_exige_laudo",
      valuation_basis: "laudo_abnt_nbr_14653",
      forced_liquidation_value: null,
      analyst_adjusted_value: null,
      final_economic_value: "200.00",
      final_value_source: "politica_default",
      essentiality_status: "nao_essencial",
      evidence_id: "evidence-1",
      valuation_status: "pendente",
      blocks_plra: true,
      blocking_reasons: ["ATIVO_MATERIAL_SEM_LAUDO_VALIDADO"],
      methodology_version_id: "metodologia-2024.1",
    },
  ],
};

describe("Evidence route", () => {
  beforeEach(() => {
    window.history.pushState(
      {},
      "",
      "/analises/analysis-1/exercicios/2024/evidencias",
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders backend materiality, impact and blocking summaries", async () => {
    mockApi();
    render(<App />);

    expect(
      await screen.findByRole("heading", {
        name: "Evidências e avaliação de ativos",
      }),
    ).toBeInTheDocument();
    expect(await screen.findByText("R$ 100,00")).toHaveClass("tnum");
    expect(screen.getByText("10%")).toHaveClass("tnum");
    expect(screen.getByText("Crítica")).toBeInTheDocument();
    expect(screen.getByText("Bloqueia resultado")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Evidências" })).toHaveAttribute(
      "href",
      "/analises/analysis-1/exercicios/2024/evidencias",
    );
    expect(screen.getByRole("link", { name: "Exportar Excel" })).toHaveAttribute(
      "href",
      "/api/v1/analyses/analysis-1/exercises/2024/evidences/export.xlsx",
    );
  });

  it("requires justification locally and sends a controlled override", async () => {
    const fetchMock = mockApi();
    render(<App />);
    await screen.findByText("R$ 100,00");

    fireEvent.click(screen.getByRole("button", { name: "Revisar asset-1" }));
    fireEvent.click(
      screen.getByRole("checkbox", {
        name: "Aplicar override de materialidade",
      }),
    );
    fireEvent.click(screen.getByRole("button", { name: "Salvar revisão" }));
    expect(
      screen.getByText("O override exige justificativa."),
    ).toBeInTheDocument();

    fireEvent.change(
      screen.getByLabelText("Justificativa do override"),
      { target: { value: "Risco operacional confirmado." } },
    );
    fireEvent.change(screen.getByLabelText("Nova materialidade"), {
      target: { value: "alta" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Salvar revisão" }));

    await waitFor(() => {
      const call = fetchMock.mock.calls.find(([url, init]) =>
        String(url).endsWith("/api/v1/evidences/evidence-1") &&
        (init as RequestInit | undefined)?.method === "PUT",
      );
      expect(call).toBeDefined();
      expect(JSON.parse((call?.[1] as RequestInit).body as string)).toMatchObject({
        materiality_override: {
          materiality_level: "alta",
          justification: "Risco operacional confirmado.",
        },
      });
    });
  });

  it("shows persisted asset values and explicit PLRA block", async () => {
    mockApi();
    render(<App />);
    await screen.findByText("R$ 100,00");

    fireEvent.click(
      screen.getByRole("tab", { name: /Avaliação de ativos/ }),
    );

    expect(await screen.findByText("Máquinas e equipamentos")).toBeInTheDocument();
    expect(screen.getByText("80%")).toHaveClass("tnum");
    expect(screen.getAllByText("R$ 200,00")).toHaveLength(2);
    expect(screen.getByText("Bloqueia PLRA")).toBeInTheDocument();
    expect(
      screen.getByText("ATIVO_MATERIAL_SEM_LAUDO_VALIDADO"),
    ).toBeInTheDocument();
  });
});

function mockApi() {
  const fetchMock = vi.fn((url: string, init?: RequestInit) => {
    if (init?.method === "PUT") {
      return response(200, {
        ...evidence,
        materiality_level: "alta",
        materiality_source: "override_manual",
      });
    }
    if (url.endsWith("/assets/valuations")) {
      return response(200, assets);
    }
    return response(200, evidenceList);
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

function response(status: number, body: object): Promise<Response> {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(body),
  } as Response);
}
