import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import type { DfcCalculation } from "../api/dfc";


const calculation: DfcCalculation = {
  exercise_year: 2024,
  automatic_value: "80000.00",
  operational_flow: "120000.00",
  investment_flow: "-25000.00",
  financing_flow: "-15000.00",
  manual_adjustments_value: "0.00",
  fca_value: "80000.00",
  fca_status: "bloqueado_por_pendencia",
  component_summaries: [
    {
      activity: "operacional",
      component_code: "recebimentos_clientes",
      component_label: "Recebimentos de clientes",
      value: "120000.00",
      movement_count: 1,
    },
    {
      activity: "investimento",
      component_code: "compra_imobilizado",
      component_label: "Compra de imobilizado",
      value: "-25000.00",
      movement_count: 1,
    },
    {
      activity: "financiamento",
      component_code: "amortizacao_principal",
      component_label: "Amortização de principal",
      value: "-15000.00",
      movement_count: 1,
    },
  ],
  audit_rows: [
    {
      entry_number: "LCTO-1",
      entry_date: "2024-01-31",
      cash_account_code: "cash",
      cash_flow_direction: "entrada",
      counterparty_account_code: "other",
      counterparty_account_name: "Recebimento em revisão",
      counterparty_reference_code: "1.01.02.03.02",
      dfc_activity: "nao_classificado",
      dfc_component_code: null,
      dfc_component_label: null,
      movement_value: "100.00",
      included_value: "0.00",
      final_status: "nao_classificado",
      pending_reason: "codigo_referencial_sem_regra_dfc",
      history: "Recebimento conciliável",
      line_number: 6,
    },
  ],
  pending_issues: [
    {
      code: "codigo_referencial_sem_regra_dfc",
      message: "Movimento não classificado exige decisão antes do FCA final.",
      entry_number: "LCTO-1",
      line_number: 6,
      materiality_level: "critica",
      blocks_fca: true,
    },
  ],
  alerts: [],
  limitations: [],
  methodology_version_id: "metodologia-2024.1",
};

describe("DFC route", () => {
  beforeEach(() => {
    window.history.pushState(
      {},
      "",
      "/analises/analysis-1/exercicios/2024/dfc",
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders persisted FCA, activities, pending issues and audit rows", async () => {
    mockDfcApi();
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "DFC direta e FCA" }),
    ).toBeInTheDocument();
    expect(await screen.findByText("R$ 80.000,00")).toHaveClass("tnum");
    expect(screen.getByText("R$ 120.000,00")).toHaveClass("tnum");
    expect(screen.getByText("-R$ 25.000,00")).toHaveClass("tnum");
    expect(screen.getByText("Bloqueado por pendência")).toBeInTheDocument();
    expect(screen.getByText("Recebimento em revisão")).toBeInTheDocument();
    expect(
      screen.getAllByText("codigo_referencial_sem_regra_dfc"),
    ).toHaveLength(2);
    expect(screen.getByRole("link", { name: "DFC / FCA" })).toHaveAttribute(
      "href",
      "/analises/analysis-1/exercicios/2024/dfc",
    );
    expect(screen.getByRole("link", { name: "Exportar Excel" })).toHaveAttribute(
      "href",
      "/api/v1/analyses/analysis-1/exercises/2024/dfc/export.xlsx",
    );
  });

  it("filters audit rows without changing API values", async () => {
    mockDfcApi();
    render(<App />);
    await screen.findByText("Recebimento em revisão");

    fireEvent.change(screen.getByLabelText("Atividade"), {
      target: { value: "investimento" },
    });

    expect(screen.getByText("Sem registros.")).toBeInTheDocument();
    expect(screen.getByText("R$ 80.000,00")).toBeInTheDocument();
  });

  it("submits a governed manual inclusion decision", async () => {
    const decided: DfcCalculation = {
      ...calculation,
      fca_value: "80100.00",
      fca_status: "calculado",
      pending_issues: [],
      audit_rows: [
        {
          ...calculation.audit_rows[0],
          dfc_activity: "operacional",
          dfc_component_code: "recebimentos_clientes",
          dfc_component_label: "Recebimentos de clientes",
          included_value: "100.00",
          final_status: "decisao_manual_aplicada",
          pending_reason: null,
        },
      ],
    };
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.endsWith("/decisions") && init?.method === "POST") {
        return response(200, decided);
      }
      return response(200, calculation);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);
    await screen.findByText("Recebimento em revisão");

    fireEvent.click(
      screen.getByRole("button", {
        name: "Decidir lançamento LCTO-1, linha 6",
      }),
    );
    expect(
      screen.getByRole("dialog", { name: "Decisão sobre movimento" }),
    ).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Justificativa"), {
      target: { value: "Recebimento conciliado com extrato." },
    });
    fireEvent.click(screen.getByRole("button", { name: "Aplicar decisão" }));

    expect(await screen.findByText("R$ 80.100,00")).toHaveClass("tnum");
    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "/api/v1/analyses/analysis-1/exercises/2024/dfc/decisions",
        expect.objectContaining({ method: "POST" }),
      ),
    );
    const decisionCall = fetchMock.mock.calls.find(([url]) =>
      url.endsWith("/decisions"),
    );
    expect(JSON.parse(String(decisionCall?.[1]?.body))).toEqual({
      action: "incluir",
      entry_number: "LCTO-1",
      line_number: 6,
      activity: "operacional",
      component_code: "recebimentos_clientes",
      justification: "Recebimento conciliado com extrato.",
    });
  });

  it("runs DFC from the empty state", async () => {
    const fetchMock = vi.fn((_url: string, init?: RequestInit) => {
      if (init?.method === "POST") return response(200, calculation);
      return response(404, { detail: { message: "DFC not found." } });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "DFC não calculada" }),
    ).toBeInTheDocument();
    fireEvent.click(screen.getAllByRole("button", { name: "Calcular DFC" })[0]);

    expect(await screen.findByText("R$ 80.000,00")).toHaveClass("tnum");
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/analysis-1/exercises/2024/dfc/run",
      { method: "POST" },
    );
  });
});

function mockDfcApi() {
  const fetchMock = vi.fn(() => response(200, calculation));
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
