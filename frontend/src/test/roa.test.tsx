import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import type { RoaCalculation } from "../api/roa";


const calculation: RoaCalculation = {
  exercise_year: 2024,
  gross_revenue: "100000.00",
  deductions: "5000.00",
  revenue_taxes: "10000.00",
  net_operating_revenue: "85000.00",
  operating_costs: "30000.00",
  operating_expenses: "15000.00",
  financial_result: "-2000.00",
  non_operating_result: "0.00",
  cash_pressure_adjustments: "0.00",
  roa_preliminary: "38000.00",
  roa_final: "38000.00",
  roa_status: "bloqueado_por_pendencia",
  component_summaries: [
    {
      block: "receita_bruta",
      component_code: "receita_vendas_servicos",
      component_label: "Receita de vendas e serviços",
      value: "100000.00",
      account_count: 1,
    },
    {
      block: "resultado_nao_operacional",
      component_code: "receitas_nao_operacionais",
      component_label: "Receitas não operacionais",
      value: "0.00",
      account_count: 0,
    },
  ],
  audit_rows: [
    {
      account_code: "sales",
      account_name: "Receita de vendas",
      reference_code: "3.01.01.01.01.04",
      reference_description: "Receita de venda de mercadorias",
      roa_block: "receita_bruta",
      component_roa: "receita_vendas_servicos",
      component_label: "Receita de vendas e serviços",
      base_value: "100000.00",
      signed_value: "100000.00",
      treatment: "incluir_automaticamente",
      final_status: "incluido",
      pending_reason: null,
      evidence_id: null,
      line_reference: 100,
      macrogroup: "RECEITA_OPERACIONAL",
      required_evidence_type: "documento_fiscal_receita",
      source_detail: null,
    },
    {
      account_code: "other-revenue",
      account_name: "Outras receitas",
      reference_code: "3.01.01.05.01.01",
      reference_description: "Receitas diversas",
      roa_block: "resultado_nao_operacional",
      component_roa: "receitas_nao_operacionais",
      component_label: "Receitas não operacionais",
      base_value: "20000.00",
      signed_value: "0.00",
      treatment: "condicional",
      final_status: "pendente_revisao",
      pending_reason: "Reclassificar receita.",
      evidence_id: null,
      line_reference: 120,
      macrogroup: "RESULTADO_NAO_OPERACIONAL",
      required_evidence_type: "documento_suporte_nao_operacional",
      source_detail: null,
    },
  ],
  pending_groups: [
    {
      code: "CONTA_ROA_CONDICIONAL",
      message: "Conta condicional exige revisão antes do ROA final.",
      account_code: "other-revenue",
      reference_code: "3.01.01.05.01.01",
      blocks_roa: true,
      materiality_level: null,
      evidence_id: null,
    },
  ],
  alerts: [],
  limitations: [
    "Conferencia J150 indisponivel; ROA calculado a partir de I155 e codigo referencial.",
  ],
  methodology_version_id: "metodologia-2024.1",
  capag_assessment: {
    exercise_year: 2024,
    method: "roa_plra",
    plra_value: "500000.00",
    plra_status: "calculado",
    fca_value: null,
    fca_status: "nao_calculado",
    roa_value: "38000.00",
    roa_status: "bloqueado_por_pendencia",
    capag_e_value: null,
    capag_e_status: "bloqueado",
    unavailable_reason: "ROA final indisponível.",
    calculation_basis: "PLRA=500000.00; FCA=indisponivel; ROA=38000.00",
    methodology_formula: "CAPAG-E = PLRA + ROA",
    warnings: [],
    limitations: [],
    blocking_issues: ["ROA_FINAL_INDISPONIVEL"],
    methodology_version_id: "metodologia-2024.1",
    balance_status: "VALIDO",
  },
};

describe("ROA route", () => {
  beforeEach(() => {
    window.history.pushState(
      {},
      "",
      "/analises/analysis-1/exercicios/2024/roa",
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders API values, CAPAG integration, pending issues and audit", async () => {
    vi.stubGlobal("fetch", vi.fn(() => response(200, calculation)));
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "ROA e CAPAG-E" }),
    ).toBeInTheDocument();
    expect(await screen.findAllByText("R$ 38.000,00")).not.toHaveLength(0);
    expect(screen.getByText("CAPAG-E = PLRA + ROA")).toBeInTheDocument();
    expect(screen.getByText("R$ 500.000,00")).toHaveClass("tnum");
    expect(screen.getByText("CONTA_ROA_CONDICIONAL")).toBeInTheDocument();
    expect(screen.getByText("Outras receitas")).toBeInTheDocument();
    expect(screen.getByText("Bloqueado por pendência")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "ROA" })).toHaveAttribute(
      "href",
      "/analises/analysis-1/exercicios/2024/roa",
    );
    expect(screen.getByRole("link", { name: "Exportar Excel" })).toHaveAttribute(
      "href",
      "/api/v1/analyses/analysis-1/exercises/2024/roa/export.xlsx",
    );
  });

  it("submits a governed conditional decision", async () => {
    const decided: RoaCalculation = {
      ...calculation,
      non_operating_result: "20000.00",
      roa_preliminary: "58000.00",
      roa_final: "58000.00",
      roa_status: "calculado",
      pending_groups: [],
      audit_rows: [
        calculation.audit_rows[0],
        {
          ...calculation.audit_rows[1],
          signed_value: "20000.00",
          final_status: "decisao_manual_aplicada",
          pending_reason: null,
        },
      ],
      capag_assessment: {
        ...calculation.capag_assessment!,
        roa_value: "58000.00",
        roa_status: "calculado",
        capag_e_value: "558000.00",
        capag_e_status: "calculado",
        unavailable_reason: null,
        blocking_issues: [],
      },
    };
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.endsWith("/decisions") && init?.method === "POST") {
        return response(200, decided);
      }
      return response(200, calculation);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);
    await screen.findByText("Outras receitas");

    fireEvent.click(
      screen.getByRole("button", { name: "Decidir conta other-revenue" }),
    );
    expect(
      screen.getByRole("dialog", { name: "Decisão sobre conta" }),
    ).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Justificativa"), {
      target: { value: "Receita conciliada e pertinente." },
    });
    fireEvent.click(screen.getByRole("button", { name: "Aplicar decisão" }));

    expect(await screen.findAllByText("R$ 58.000,00")).not.toHaveLength(0);
    expect(screen.getByText("R$ 558.000,00")).toHaveClass("tnum");
    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "/api/v1/analyses/analysis-1/exercises/2024/roa/decisions",
        expect.objectContaining({ method: "POST" }),
      ),
    );
    const decisionCall = fetchMock.mock.calls.find(([url]) =>
      url.endsWith("/decisions"),
    );
    expect(JSON.parse(String(decisionCall?.[1]?.body))).toEqual({
      action: "incluir",
      account_code: "other-revenue",
      justification: "Receita conciliada e pertinente.",
    });
  });

  it("runs ROA from the empty state", async () => {
    const fetchMock = vi.fn((_url: string, init?: RequestInit) => {
      if (init?.method === "POST") return response(200, calculation);
      return response(404, { detail: { message: "ROA not found." } });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "ROA não calculado" }),
    ).toBeInTheDocument();
    fireEvent.click(screen.getAllByRole("button", { name: "Calcular ROA" })[0]);

    expect(await screen.findAllByText("R$ 38.000,00")).not.toHaveLength(0);
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/analysis-1/exercises/2024/roa/run",
      { method: "POST" },
    );
  });
});

function response(status: number, body: object): Promise<Response> {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(body),
  } as Response);
}
