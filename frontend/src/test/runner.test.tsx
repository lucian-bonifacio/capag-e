import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "../App";
import type { DeclaredAccountsResponse } from "../api/declared";

const summaryResponse = {
  analysis_id: "7",
  year: 2024,
  total_accounts: 5,
  methodology_version_id: "metodologia-2024.1",
  status_counts: {
    MAPEADO: 1,
    COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL: 1,
    NAO_MAPEADO_METODOLOGICAMENTE: 1,
    SEM_VINCULO_REFERENCIAL: 1,
  },
};

const accountsResponse: DeclaredAccountsResponse = {
  analysis_id: "7",
  year: 2024,
  accounts: [
    {
      account_code: "1",
      account_name: "Ativo",
      account_type: "S",
      account_nature: "01",
      account_level: 1,
      parent_account_code: null,
      account_order: 1,
      declared_reference_code: null,
      official_description: null,
      official_reference_status: null,
      methodology_rule_applied: null,
      methodology_rule_status: null,
      purpose: null,
      plra_category: null,
      fco_category: null,
      capag_category: null,
      flow_nature: null,
      treatment: null,
      base_value: "100510.00",
      considered_value: "100510.00",
      final_status: "SEM_VINCULO_REFERENCIAL",
      observation: "Conta estrutural sem vinculo.",
      recommended_action: "revisar_vinculo_referencial",
      methodology_version_id: "metodologia-2024.1",
    },
    {
      account_code: "1.1",
      account_name: "Ativo Circulante",
      account_type: "S",
      account_nature: "01",
      account_level: 2,
      parent_account_code: "1",
      account_order: 2,
      declared_reference_code: null,
      official_description: null,
      official_reference_status: null,
      methodology_rule_applied: null,
      methodology_rule_status: null,
      purpose: null,
      plra_category: null,
      fco_category: null,
      capag_category: null,
      flow_nature: null,
      treatment: null,
      base_value: "100510.00",
      considered_value: "100510.00",
      final_status: "SEM_VINCULO_REFERENCIAL",
      observation: "Conta estrutural sem vinculo.",
      recommended_action: "revisar_vinculo_referencial",
      methodology_version_id: "metodologia-2024.1",
    },
    {
      account_code: "1725",
      account_name: "Emprestimo - Sicoob",
      account_type: "A",
      account_nature: "01",
      account_level: 3,
      parent_account_code: "1.1",
      account_order: 3,
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
      account_type: "A",
      account_nature: "01",
      account_level: 3,
      parent_account_code: "1.1",
      account_order: 4,
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
    {
      account_code: "4001",
      account_name: "Codigo fora da base",
      account_type: "A",
      account_nature: "01",
      account_level: 3,
      parent_account_code: "1.1",
      account_order: 5,
      declared_reference_code: "8.88.88",
      official_description: null,
      official_reference_status: null,
      methodology_rule_applied: null,
      methodology_rule_status: null,
      purpose: "AUDITORIA",
      plra_category: null,
      fco_category: null,
      capag_category: null,
      flow_nature: null,
      treatment: null,
      base_value: "500.00",
      considered_value: "500.00",
      final_status: "COD_CTA_REF_NAO_ENCONTRADO_NA_TABELA_OFICIAL",
      observation: "Codigo referencial ausente no plano oficial.",
      recommended_action: "revisar_base_oficial",
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

  it("renders the balance dashboard returned by the declared accounts API", async () => {
    const fetchMock = mockSuccessfulApi();

    render(<App />);

    expect(screen.getByText("CAPAG Analytics")).toBeInTheDocument();
    expect(
      await screen.findByRole("heading", { name: "Balanço Patrimonial" }),
    ).toBeInTheDocument();
    expect((await screen.findAllByText("Emprestimo - Sicoob")).length).toBeGreaterThan(0);
    expect(screen.getByText("Conta sem Regra")).toBeInTheDocument();
    expect(screen.getAllByText("R$ 100.000,00")[0]).toHaveClass("tnum");
    expect(screen.getAllByText("1725")[0]).toHaveClass("tnum");

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/7/exercises/2024/declared",
      undefined,
    );
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/analyses/7/exercises/2024/declared/balance/accounts",
      undefined,
    );
  });

  it("keeps declared accounts accessible from the balance dashboard", async () => {
    mockSuccessfulApi();

    render(<App />);

    expect(await screen.findByText("Codigo Fora da Base")).toBeInTheDocument();
    expect(screen.getAllByText("4001").length).toBeGreaterThan(0);
    expect(screen.getByRole("link", { name: "Auditoria" })).toHaveAttribute(
      "href",
      "/analises/7/exercicios/2024/auditoria",
    );
  });

  it("uses the ECD hierarchy without repeating the synthetic group as a child row", async () => {
    mockSuccessfulApi({
      ...accountsResponse,
      accounts: [
        {
          ...accountsResponse.accounts[0],
          account_code: "1",
          account_name: "Ativo",
          account_level: 1,
          parent_account_code: null,
          account_order: 1,
        },
        {
          ...accountsResponse.accounts[1],
          account_code: "1.1",
          account_name: "Ativo Circulante",
          account_level: 2,
          parent_account_code: "1",
          account_order: 2,
          base_value: "100.00",
          considered_value: "100.00",
        },
        {
          ...accountsResponse.accounts[2],
          account_code: "1.1.1",
          account_name: "Caixa e equivalentes",
          account_level: 3,
          parent_account_code: "1.1",
          account_order: 3,
          account_type: "S",
          base_value: "0.00",
          considered_value: "0.00",
        },
        {
          ...accountsResponse.accounts[2],
          account_code: "1.1.1.01",
          account_name: "Banco conta movimento",
          account_level: 4,
          parent_account_code: "1.1.1",
          account_order: 4,
          account_type: "A",
          base_value: "100.00",
          considered_value: "100.00",
        },
      ],
    });

    render(<App />);

    expect(await screen.findByText("Ativo Circulante")).toBeInTheDocument();
    expect(screen.getAllByText("Ativo Circulante")).toHaveLength(1);
    expect(screen.getByText("Caixa e Equivalentes")).toBeInTheDocument();
    expect(screen.getAllByText("R$ 100,00").length).toBeGreaterThan(0);
    expect(screen.queryByText("Banco Conta Movimento")).not.toBeInTheDocument();
  });

  it("keeps result accounts out of the balance sheet and warns when it does not close", async () => {
    mockSuccessfulApi({
      ...accountsResponse,
      accounts: [
        {
          ...accountsResponse.accounts[0],
          account_code: "1",
          account_name: "Ativo",
          account_nature: "01",
          base_value: "100.00",
          considered_value: "100.00",
        },
        {
          ...accountsResponse.accounts[0],
          account_code: "2",
          account_name: "Passivo",
          account_nature: "02",
          base_value: "90.00",
          considered_value: "90.00",
        },
        {
          ...accountsResponse.accounts[0],
          account_code: "3",
          account_name: "Resultado do exercicio",
          account_nature: "04",
          base_value: "999.00",
          considered_value: "999.00",
        },
      ],
    });

    render(<App />);

    expect((await screen.findAllByText("Ativo")).length).toBeGreaterThan(0);
    expect(screen.getAllByText("Passivo").length).toBeGreaterThan(0);
    expect(screen.queryByText("Resultado do Exercicio")).not.toBeInTheDocument();
    expect(screen.getByText("Balanço não fecha.")).toBeInTheDocument();
    expect(screen.getByText(/R\$ 10,00/)).toBeInTheDocument();
  });

  it("shows J100 and I050 consistency warnings returned by the balance API", async () => {
    mockSuccessfulApi({
      ...accountsResponse,
      consistency_warnings: [
        {
          warning_code: "J100_SEM_I050",
          account_code: "9.9",
          account_name: "Conta J100 sem I050",
          message: "Linha do J100 sem conta correspondente no I050.",
        },
      ],
    });

    render(<App />);

    expect(await screen.findByText("Consistência J100 x I050")).toBeInTheDocument();
    expect(screen.getByText("1 apontamento")).toBeInTheDocument();
    expect(screen.getByText("9.9")).toBeInTheDocument();
    expect(screen.getByText("Conta J100 sem I050")).toBeInTheDocument();
    expect(screen.getByText("Linha do J100 sem conta correspondente no I050.")).toBeInTheDocument();
  });

  it("renders the empty state when the API returns no accounts", async () => {
    mockSuccessfulApi({ ...accountsResponse, accounts: [] });

    render(<App />);

    expect(
      await screen.findByText("Sem contas declaradas para montar a hierarquia da ECD."),
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
      await screen.findByRole("heading", { name: "Erro ao carregar balanço patrimonial" }),
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

      if (url === "/api/v1/analyses/analysis-real/exercises/2024/declared") {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ ...summaryResponse, analysis_id: "analysis-real" }),
        } as Response);
      }

      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ ...accountsResponse, analysis_id: "analysis-real" }),
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

      if (url === "/api/v1/analyses/analysis-existing/exercises/2024/declared") {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ ...summaryResponse, analysis_id: "analysis-existing" }),
        } as Response);
      }

      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ ...accountsResponse, analysis_id: "analysis-existing" }),
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
    expect(await screen.findByRole("heading", { name: "Balanço Patrimonial" })).toBeInTheDocument();
    expect(await screen.findByText("analysis-existing")).toHaveClass("tnum");
    expect(fetchMock).not.toHaveBeenCalledWith(
      "/api/v1/analyses/analysis-existing/exercises/2024/declared/run",
      { method: "POST" },
    );
  });
});
