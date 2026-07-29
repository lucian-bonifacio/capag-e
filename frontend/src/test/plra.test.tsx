import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import type { PlraAudit, PlraCalculation } from "../api/plra";


const calculation: PlraCalculation = {
  analysis_id: "analysis-1",
  exercise_year: 2024,
  gross_assets_value: "900000.00",
  gross_economic_liabilities_value: "300000.00",
  adjusted_assets_value: "630000.00",
  plr_gross_value: "600000.00",
  plra_value: "330000.00",
  plra_status: "calculado",
  calculation_formula:
    "PLRA = ativos com valor economico final - passivos economicos exigiveis",
  pending_accounts: [],
  warnings: [],
  limitations: [],
  blocking_issues: [],
  balance_status: "VALIDO",
  methodology_version_id: "metodologia-2024.1",
  calculated_at: "2026-07-24T20:31:00Z",
};

const audit: PlraAudit = {
  analysis_id: "analysis-1",
  exercise_year: 2024,
  plra_status: "calculado",
  methodology_version_id: "metodologia-2024.1",
  rows: [
    {
      account_code: "1101",
      account_name: "Clientes nacionais",
      account_type: "A",
      account_level: 4,
      parent_account_code: "1100",
      declared_reference_code: "1.01.03.01.01",
      official_description: "Duplicatas a receber",
      methodology_rule_id: "PLRA-1.01.03.01.01",
      methodology_group: "clientes",
      macrogroup: "ATIVO_REALIZAVEL",
      base_value: "100000.00",
      sign: "D",
      inclusion_status: "incluido_ativo",
      default_discount_percent: "0.300000",
      default_economic_value: "70000.00",
      valuation_source: "default_interno",
      validated_valuation_value: null,
      final_economic_value: "70000.00",
      decision_status: "automatica",
      evidence_status: null,
      reason: "Clientes sujeitos ao deságio prudencial interno.",
      limitations: [],
      methodology_version_id: "metodologia-2024.1",
    },
  ],
};

describe("PLRA route", () => {
  beforeEach(() => {
    window.history.pushState(
      {},
      "",
      "/analises/analysis-1/exercicios/2024/plra",
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders the persisted calculation without recomputing API values", async () => {
    mockPlraApi();

    render(<App />);

    expect(
      screen.getByRole("heading", {
        name: "Patrimônio Líquido Realizável Ajustado",
      }),
    ).toBeInTheDocument();
    expect(await screen.findByText("R$ 330.000,00")).toHaveClass("tnum");
    expect(screen.getByText("R$ 600.000,00")).toHaveClass("tnum");
    expect(screen.getByText("R$ 630.000,00")).toHaveClass("tnum");
    expect(screen.getByText("metodologia-2024.1")).toHaveClass("tnum");
    expect(screen.getByRole("link", { name: "PLRA" })).toHaveAttribute(
      "href",
      "/analises/analysis-1/exercicios/2024/plra",
    );
    expect(screen.getByRole("link", { name: "Exportar Excel" })).toHaveAttribute(
      "href",
      "/api/v1/analyses/analysis-1/exercises/2024/plra/export.xlsx",
    );
  });

  it("opens account audit and identifies the internal default source", async () => {
    mockPlraApi();
    render(<App />);
    await screen.findByText("R$ 330.000,00");

    fireEvent.click(screen.getByRole("button", { name: "Abrir auditoria" }));

    expect(
      await screen.findByRole("dialog", { name: "Auditoria do PLRA" }),
    ).toBeInTheDocument();
    expect(await screen.findByText("Clientes nacionais")).toBeInTheDocument();
    expect(screen.getByText("30%")).toHaveClass("tnum");
    expect(screen.getByText("Política interna default")).toBeInTheDocument();
    expect(screen.getAllByText("R$ 70.000,00")).toHaveLength(2);
    expect(screen.getAllByText("R$ 70.000,00")[0]).toHaveClass("tnum");
  });

  it("runs PLRA from the empty state using a bodyless command", async () => {
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (init?.method === "POST") {
        return response(200, calculation);
      }
      return response(404, { detail: { message: "PLRA not found." } });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "PLRA não calculado" }),
    ).toBeInTheDocument();
    fireEvent.click(screen.getAllByRole("button", { name: "Calcular PLRA" })[0]);

    expect(await screen.findByText("R$ 330.000,00")).toHaveClass("tnum");
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/analysis-1/exercises/2024/plra/run",
      { method: "POST" },
    );
  });

  it("keeps pending accounts and blocking issues visible", async () => {
    mockPlraApi({
      ...calculation,
      plra_status: "bloqueado_por_evidencia",
      pending_accounts: ["1.2.3 - Imóvel sem avaliação validada"],
      limitations: ["Valor intermediário disponível."],
      blocking_issues: ["EVIDENCIA_CRITICA_PENDENTE"],
    });
    render(<App />);

    expect(
      await screen.findByText("Bloqueado por evidência"),
    ).toBeInTheDocument();
    expect(screen.getByText("EVIDENCIA_CRITICA_PENDENTE")).toBeInTheDocument();
    expect(
      screen.getByText("1.2.3 - Imóvel sem avaliação validada"),
    ).toBeInTheDocument();
    expect(screen.getByText("Valor intermediário disponível.")).toBeInTheDocument();
  });

  it("renders a recoverable API error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        response(503, { detail: { message: "PLRA indisponível." } }),
      ),
    );
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "Erro ao consultar PLRA" }),
    ).toBeInTheDocument();
    expect(screen.getByText("PLRA indisponível.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Tentar novamente" })).toBeInTheDocument();
  });
});

function mockPlraApi(calculationResponse = calculation) {
  const fetchMock = vi.fn((url: string) => {
    const body = url.endsWith("/audit") ? audit : calculationResponse;
    return response(200, body);
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
