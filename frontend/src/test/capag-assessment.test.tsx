import { render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import type { CapagAssessment } from "../api/capag";


const partialAssessment: CapagAssessment = {
  exercise_year: 2024,
  method: "fca_plra",
  plra_value: "500000.00",
  plra_status: "calculado",
  fca_value: "40000.00",
  fca_status: "parcial",
  roa_value: null,
  roa_status: "nao_calculado",
  capag_e_value: "540000.00",
  capag_e_status: "parcial",
  unavailable_reason: null,
  calculation_basis: "PLRA=500000.00; FCA=40000.00; ROA=indisponivel",
  methodology_formula: "CAPAG-E = PLRA + FCA",
  warnings: ["Valor sujeito a revisão."],
  limitations: ["FCA parcial: somente FCO disponível."],
  blocking_issues: [],
  methodology_version_id: "metodologia-2024.1",
};


describe("CAPAG-E assessment route", () => {
  beforeEach(() => {
    window.history.pushState(
      {},
      "",
      "/analises/analysis-1/exercicios/2024/resultado",
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders partial status and values exactly as returned by the API", async () => {
    mockResponse(200, partialAssessment);

    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "Resultado CAPAG-E" }),
    ).toBeInTheDocument();
    expect(
      await screen.findByRole("heading", { name: "FCA parcial" }),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Parcial").length).toBeGreaterThan(0);
    expect(screen.getByText("R$ 540.000,00")).toHaveClass("tnum");
    expect(screen.getByText("R$ 500.000,00")).toHaveClass("tnum");
    expect(screen.getByText("CAPAG-E = PLRA + FCA")).toHaveClass("tnum");
    expect(screen.queryByText("FCA final")).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Indicadores CAPAG" })).toHaveAttribute(
      "href",
      "/analises/analysis-1/exercicios/2024/resultado",
    );
  });

  it("renders a calculated assessment without changing the API status", async () => {
    mockResponse(200, {
      ...partialAssessment,
      fca_value: "120000.00",
      fca_status: "calculado",
      capag_e_value: "620000.00",
      capag_e_status: "calculado",
      limitations: [],
    });

    render(<App />);

    expect(await screen.findByText("R$ 620.000,00")).toHaveClass("tnum");
    expect(screen.getByRole("heading", { name: "FCA final" })).toBeInTheDocument();
    expect(screen.getAllByText("Calculado").length).toBeGreaterThan(0);
  });

  it("renders the empty state when no assessment exists", async () => {
    mockResponse(404, {
      detail: { message: "CAPAG-E assessment not found." },
    });

    render(<App />);

    expect(
      await screen.findByRole("heading", {
        name: "Assessment CAPAG-E não calculado",
      }),
    ).toBeInTheDocument();
  });

  it("renders a recoverable error state", async () => {
    mockResponse(503, { detail: { message: "indisponível" } });

    render(<App />);

    expect(
      await screen.findByRole("heading", {
        name: "Erro ao carregar resultado CAPAG-E",
      }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Tentar novamente" })).toBeInTheDocument();
  });
});


function mockResponse(status: number, body: object) {
  vi.stubGlobal(
    "fetch",
    vi.fn(() =>
      Promise.resolve({
        ok: status >= 200 && status < 300,
        status,
        json: () => Promise.resolve(body),
      } as Response),
    ),
  );
}
