import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import type { DeclaredBalanceResponse } from "../api/declared";

const balanceResponse: DeclaredBalanceResponse = {
  analysis_id: "7",
  year: 2024,
  balance_status: "VALIDO",
  is_blocking: false,
  j005_period_start: "2024-01-01",
  j005_period_end: "2024-12-31",
  assets_final_amount: "800.00",
  liabilities_and_equity_final_amount: "800.00",
  difference: "0.00",
  limitations: [],
  rows: [
    {
      aggregation_code: "ATIVO",
      aggregation_code_type: "T",
      aggregation_level: 1,
      parent_aggregation_code: null,
      balance_group: "A",
      description: "Ativo",
      initial_amount: "100.00",
      initial_debit_credit_indicator: "D",
      final_amount: "800.00",
      final_debit_credit_indicator: "D",
      explanatory_note_reference: null,
      line_number: 30,
      structural_status: "VALIDA",
      reconciliation_status: null,
      reconciled_amount: null,
      difference: null,
      component_count: 0,
      children: [
        {
          aggregation_code: "AGL-CAIXA",
          aggregation_code_type: "D",
          aggregation_level: 2,
          parent_aggregation_code: "ATIVO",
          balance_group: "A",
          description: "Banco conta movimento",
          initial_amount: "100.00",
          initial_debit_credit_indicator: "D",
          final_amount: "800.00",
          final_debit_credit_indicator: "D",
          explanatory_note_reference: "N1",
          line_number: 31,
          structural_status: "VALIDA",
          reconciliation_status: "CONCILIADA",
          reconciled_amount: "800.00",
          difference: "0.00",
          component_count: 1,
          children: [],
        },
      ],
    },
    {
      aggregation_code: "PASSIVO",
      aggregation_code_type: "T",
      aggregation_level: 1,
      parent_aggregation_code: null,
      balance_group: "P",
      description: "Passivo e patrimônio líquido",
      initial_amount: "100.00",
      initial_debit_credit_indicator: "C",
      final_amount: "800.00",
      final_debit_credit_indicator: "C",
      explanatory_note_reference: null,
      line_number: 32,
      structural_status: "VALIDA",
      reconciliation_status: null,
      reconciled_amount: null,
      difference: null,
      component_count: 0,
      children: [
        {
          aggregation_code: "AGL-CAPITAL",
          aggregation_code_type: "D",
          aggregation_level: 2,
          parent_aggregation_code: "PASSIVO",
          balance_group: "P",
          description: "Capital social",
          initial_amount: "100.00",
          initial_debit_credit_indicator: "C",
          final_amount: "800.00",
          final_debit_credit_indicator: "C",
          explanatory_note_reference: null,
          line_number: 33,
          structural_status: "VALIDA",
          reconciliation_status: "CONCILIADA",
          reconciled_amount: "-800.00",
          difference: "0.00",
          component_count: 1,
          children: [],
        },
      ],
    },
  ],
};

const componentsResponse = {
  analysis_id: "7",
  year: 2024,
  aggregation_code: "AGL-CAIXA",
  rows: [
    {
      account_code: "1.01.01.001",
      account_name: "Banco conta movimento",
      cost_center_code: "CC01",
      final_amount: "800.00",
      final_debit_credit_indicator: "D",
      signed_final_amount: "800.00",
      i052_line_number: 5,
      i155_line_number: 9,
    },
  ],
};

function mockBalanceApi(balance = balanceResponse) {
  const fetchMock = vi.fn((url: string) => {
    const body = url.includes("/components") ? componentsResponse : balance;
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve(body),
    } as Response);
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

describe("declared balance route", () => {
  beforeEach(() => {
    window.history.pushState({}, "", "/analises/7/exercicios/2024/declarada");
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders the J100 tree and values exactly as returned by the API", async () => {
    const fetchMock = mockBalanceApi();

    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "Balanço Patrimonial" }),
    ).toBeInTheDocument();
    expect(await screen.findByText("Válido")).toBeInTheDocument();
    expect(screen.getByText("Banco conta movimento")).toBeInTheDocument();
    expect(screen.getByText("Capital social")).toBeInTheDocument();
    expect(screen.getAllByText("R$ 800,00")[0]).toHaveClass("tnum");
    expect(screen.getAllByText(/Saldo inicial: R\$ 100,00/)[0]).toHaveClass("tnum");
    expect(screen.getAllByText("Conciliada")).toHaveLength(2);
    expect(screen.queryByRole("checkbox")).not.toBeInTheDocument();
    expect(screen.getByText("Visão declarada · sem ajustes")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/7/exercises/2024/declared/balance/accounts",
      undefined,
    );
  });

  it("loads I050 I052 and I155 components only when requested", async () => {
    const fetchMock = mockBalanceApi();

    render(<App />);
    const componentButtons = await screen.findAllByRole("button", {
      name: "Ver componentes (1)",
    });
    fireEvent.click(componentButtons[0]);

    expect(
      await screen.findByRole("dialog", {
        name: "Componentes — Banco conta movimento",
      }),
    ).toBeInTheDocument();
    expect(screen.getByText("CC01")).toHaveClass("tnum");
    expect(screen.getByText("1.01.01.001")).toHaveClass("tnum");
    expect(screen.getByText(/I052 linha 5/)).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/7/exercises/2024/declared/balance/accounts/AGL-CAIXA/components",
      undefined,
    );
  });

  it("shows an objective empty state and backend limitations", async () => {
    mockBalanceApi({
      ...balanceResponse,
      balance_status: "OBRIGATORIO_AUSENTE",
      is_blocking: true,
      assets_final_amount: null,
      liabilities_and_equity_final_amount: null,
      difference: null,
      rows: [],
      limitations: ["J100_OBRIGATORIO_AUSENTE"],
    });

    render(<App />);

    expect(await screen.findByText("Balanço ausente")).toBeInTheDocument();
    expect(screen.getByText("Balanço J100 obrigatório ausente.")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Balanço declarado indisponível" }),
    ).toBeInTheDocument();
  });

  it("renders the error state when the balance API fails", async () => {
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
      await screen.findByRole("heading", {
        name: "Erro ao carregar balanço patrimonial",
      }),
    ).toBeInTheDocument();
  });
});

describe("ecd import route", () => {
  beforeEach(() => {
    window.history.pushState({}, "", "/importar-ecd");
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("routes analysis navigation to the latest imported ECD", async () => {
    const existingImport = {
      analysis_id: "analysis-existing",
      company_id: "company-existing",
      ecd_file_id: "ecd-existing",
      original_filename: "valid.ecd",
      content_hash: "sha256:abc",
      layout: "ECD_2024",
      period_start: "2024-01-01",
      period_end: "2024-12-31",
      imported_at: "2026-07-07T10:00:00Z",
      year: 2024,
      methodology_version_id: "metodologia-2024.1",
      status: "concluido",
      parser_version: "2.1.0",
      balance_preparation_status: "PRONTA_PARA_CONCILIACAO",
      reprocessed: false,
    };
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ imports: [existingImport] }),
        } as Response),
      ),
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("link", { name: "Balanço Patrimonial" })).toHaveAttribute(
        "href",
        "/analises/analysis-existing/exercicios/2024/declarada",
      );
    });
  });

  it("keeps analysis navigation on the import route when no ECD exists", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ imports: [] }),
        } as Response),
      ),
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("link", { name: "Balanço Patrimonial" })).toHaveAttribute(
        "href",
        "/importar-ecd",
      );
    });
  });

  it("imports an ECD, runs declared layer and opens the returned analysis", async () => {
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url === "/api/v1/ecd/imports" && !init?.method) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ imports: [] }),
        } as Response);
      }
      if (url === "/api/v1/ecd/import" && init?.method === "POST") {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              analysis_id: "analysis-real",
              company_id: "company-real",
              ecd_file_id: "ecd-real",
              year: 2024,
              methodology_version_id: "metodologia-2024.1",
              status: "nao_executado",
              parser_version: "2.1.0",
              balance_preparation_status: "PRONTA_PARA_CONCILIACAO",
              reprocessed: false,
            }),
        } as Response);
      }
      if (
        url ===
          "/api/v1/analyses/analysis-real/exercises/2024/declared/run" &&
        init?.method === "POST"
      ) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              analysis_id: "analysis-real",
              year: 2024,
              status: "concluido",
              snapshots_created: 2,
              status_counts: { MAPEADO: 2 },
            }),
        } as Response);
      }
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({ ...balanceResponse, analysis_id: "analysis-real" }),
      } as Response);
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    const fileInput = screen.getByLabelText(/Nenhum arquivo selecionado/i);
    fireEvent.change(fileInput, {
      target: { files: [new File(["|0000|LECD|2024|"], "valid.ecd")] },
    });
    fireEvent.click(screen.getByRole("button", { name: "Importar ECD" }));

    expect(await screen.findByText("Análise analysis-real criada para 2024.")).toBeInTheDocument();
    expect(await screen.findByText("2 snapshots; status concluido.")).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Abrir análise" })).not.toBeDisabled();
    });
    fireEvent.click(screen.getByRole("button", { name: "Abrir análise" }));

    expect(await screen.findByText("analysis-real")).toHaveClass("tnum");
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/analysis-real/exercises/2024/declared/run",
      { method: "POST" },
    );
  });

  it("shows an existing analysis when the uploaded ECD was already imported", async () => {
    const existingImport = {
      analysis_id: "analysis-existing",
      company_id: "company-existing",
      ecd_file_id: "ecd-existing",
      original_filename: "valid.ecd",
      content_hash: "sha256:abc",
      layout: "ECD_2024",
      period_start: "2024-01-01",
      period_end: "2024-12-31",
      imported_at: "2026-07-07T10:00:00Z",
      year: 2024,
      methodology_version_id: "metodologia-2024.1",
      status: "concluido",
      parser_version: "2.1.0",
      balance_preparation_status: "PRONTA_PARA_CONCILIACAO",
      reprocessed: false,
    };
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url === "/api/v1/ecd/imports" && !init?.method) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ imports: [existingImport] }),
        } as Response);
      }
      if (url === "/api/v1/ecd/import" && init?.method === "POST") {
        return Promise.resolve({
          ok: false,
          status: 409,
          json: () =>
            Promise.resolve({
              detail: {
                error_code: "ECD_ALREADY_IMPORTED",
                message: "Este arquivo ECD ja foi importado.",
                existing_import: existingImport,
              },
            }),
        } as Response);
      }
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({ ...balanceResponse, analysis_id: "analysis-existing" }),
      } as Response);
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    const fileInput = screen.getByLabelText(/Nenhum arquivo selecionado/i);
    fireEvent.change(fileInput, {
      target: { files: [new File(["|0000|LECD|2024|"], "valid.ecd")] },
    });
    fireEvent.click(screen.getByRole("button", { name: "Importar ECD" }));

    expect(await screen.findByText("Este arquivo ECD ja foi importado.")).toBeInTheDocument();
    expect(await screen.findByText("analysis-existing")).toHaveClass("tnum");
    fireEvent.click(screen.getByRole("button", { name: "Abrir análise existente" }));
    expect(
      await screen.findByRole("heading", { name: "Balanço Patrimonial" }),
    ).toBeInTheDocument();
    expect(await screen.findByText("analysis-existing")).toHaveClass("tnum");
    expect(fetchMock).not.toHaveBeenCalledWith(
      "/api/v1/analyses/analysis-existing/exercises/2024/declared/run",
      { method: "POST" },
    );
  });
});
