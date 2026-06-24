import { render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";

const summaryResponse = {
  analysis_id: 7,
  year: 2024,
  accounts_count: 2,
  methodology_version_id: "metodologia-2024.1",
  status_counts: {
    MAPEADO: 1,
    NAO_MAPEADO_METODOLOGICAMENTE: 1,
  },
};

const accountsResponse = {
  analysis_id: 7,
  year: 2024,
  accounts: [
    {
      account_code: "1725",
      account_name: "Emprestimo - Sicoob",
      declared_reference_code: "2.01.01.07.01",
      official_description: "Emprestimos e financiamentos",
      official_reference_status: "ATIVA",
      methodology_rule_applied: "2.01.01.07.01",
      methodology_rule_status: "ATIVA",
      purpose: "FCO",
      plra_category: null,
      fco_category: "FINANCIAMENTO",
      capag_category: null,
      flow_nature: "FINANCIAMENTO",
      treatment: "excluir_operacional",
      base_value: "100000.00",
      considered_value: "0.00",
      final_status: "MAPEADO",
      observation: null,
      recommended_action: null,
      methodology_version_id: "metodologia-2024.1",
    },
    {
      account_code: "3001",
      account_name: "Conta sem regra",
      declared_reference_code: "9.99.99",
      official_description: null,
      official_reference_status: "ATIVA",
      methodology_rule_applied: null,
      methodology_rule_status: null,
      purpose: "AUDITORIA",
      plra_category: null,
      fco_category: null,
      capag_category: null,
      flow_nature: null,
      treatment: null,
      base_value: "10.00",
      considered_value: "10.00",
      final_status: "NAO_MAPEADO_METODOLOGICAMENTE",
      observation: "Sem regra metodologica exata.",
      recommended_action: "revisar_metodologia",
      methodology_version_id: "metodologia-2024.1",
    },
  ],
};

function mockSuccessfulApi(accounts = accountsResponse) {
  const fetchMock = vi.fn((url: string) => {
    const body = url.endsWith("/accounts") ? accounts : summaryResponse;

    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve(body),
    } as Response);
  });

  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

describe("declared layer route", () => {
  beforeEach(() => {
    window.history.pushState(
      {},
      "",
      "/analises/7/exercicios/2024/declarada",
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders the declared layer returned by the API without changing status values", async () => {
    const fetchMock = mockSuccessfulApi();

    render(<App />);

    expect(screen.getByText("CAPAG Analytics")).toBeInTheDocument();
    expect(
      await screen.findByRole("heading", { name: "Camada Declarada" }),
    ).toBeInTheDocument();
    expect(await screen.findByText("metodologia-2024.1")).toBeInTheDocument();
    expect(screen.getAllByText("MAPEADO").length).toBeGreaterThan(0);
    expect(
      screen.getAllByText("NAO_MAPEADO_METODOLOGICAMENTE").length,
    ).toBeGreaterThan(0);
    expect(screen.getByText("100000.00")).toHaveClass("tnum");
    expect(screen.getAllByText("2.01.01.07.01")[0]).toHaveClass("tnum");

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/7/exercises/2024/declared",
    );
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/7/exercises/2024/declared/accounts",
    );
  });

  it("renders the empty state when the API returns no accounts", async () => {
    mockSuccessfulApi({ ...accountsResponse, accounts: [] });

    render(<App />);

    expect(await screen.findByText("Sem registros.")).toBeInTheDocument();
    expect(
      screen.getByText("A camada declarada ainda não possui contas persistidas para o exercício."),
    ).toBeInTheDocument();
  });

  it("renders the error state when the API request fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 503,
        } as Response),
      ),
    );

    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "Erro ao carregar camada declarada" }),
    ).toBeInTheDocument();
  });
});
