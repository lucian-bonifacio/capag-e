import { expect, test } from "@playwright/test";

const declaredSummary = {
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

const declaredAccounts = {
  analysis_id: "7",
  year: 2024,
  accounts: [
    {
      account_code: "1",
      account_name: "Ativo",
      account_type: "S",
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

test("exibe loading e sucesso da rota declarada sem alterar status da API", async ({ page }) => {
  let releaseAccounts: () => void = () => undefined;
  const accountsReady = new Promise<void>((resolve) => {
    releaseAccounts = resolve;
  });

  await page.route("**/api/v1/analyses/7/exercises/2024/declared", async (route) => {
    await route.fulfill({ json: declaredSummary });
  });

  await page.route("**/api/v1/analyses/7/exercises/2024/declared/accounts", async (route) => {
    await accountsReady;
    await route.fulfill({ json: declaredAccounts });
  });

  await page.goto("/analises/7/exercicios/2024/declarada");

  await expect(page.getByText("Carregando contas declaradas da ECD.")).toBeVisible();

  releaseAccounts();

  await expect(page.getByRole("heading", { name: "Balanço Patrimonial" })).toBeVisible();
  await expect(page.getByText("Emprestimo - Sicoob").first()).toBeVisible();
  await expect(page.getByText("Conta sem Regra").first()).toBeVisible();
  await expect(page.getByText("R$ 100.000,00").first()).toBeVisible();
  await expect(page.getByText("1725").first()).toBeVisible();
  await expect(page.getByText("Codigo Fora da Base").first()).toBeVisible();
  await expect(page.getByText("4001").first()).toBeVisible();
});

test("exibe erro quando a API declarada falha", async ({ page }) => {
  await page.route("**/api/v1/analyses/7/exercises/2024/declared", async (route) => {
    await route.fulfill({ status: 503, json: { detail: "indisponivel" } });
  });

  await page.route("**/api/v1/analyses/7/exercises/2024/declared/accounts", async (route) => {
    await route.fulfill({ json: declaredAccounts });
  });

  await page.goto("/analises/7/exercicios/2024/declarada");

  await expect(
    page.getByRole("heading", { name: "Erro ao carregar balanço patrimonial" }),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Tentar novamente" })).toBeVisible();
});

test("exibe estado vazio quando a API nao retorna contas", async ({ page }) => {
  await page.route("**/api/v1/analyses/7/exercises/2024/declared", async (route) => {
    await route.fulfill({ json: { ...declaredSummary, total_accounts: 0, status_counts: {} } });
  });

  await page.route("**/api/v1/analyses/7/exercises/2024/declared/accounts", async (route) => {
    await route.fulfill({ json: { ...declaredAccounts, accounts: [] } });
  });

  await page.goto("/analises/7/exercicios/2024/declarada");

  await expect(page.getByRole("heading", { name: "Balanço Patrimonial" })).toBeVisible();
  await expect(
    page.getByText("Sem contas declaradas para montar a hierarquia da ECD."),
  ).toBeVisible();
});

test("usa a hierarquia I050 sem repetir grupo sintetico como microgrupo", async ({ page }) => {
  await page.route("**/api/v1/analyses/7/exercises/2024/declared", async (route) => {
    await route.fulfill({ json: declaredSummary });
  });

  await page.route("**/api/v1/analyses/7/exercises/2024/declared/accounts", async (route) => {
    await route.fulfill({
      json: {
        ...declaredAccounts,
        accounts: [
          {
            ...declaredAccounts.accounts[0],
            account_code: "1",
            account_name: "Ativo",
            account_level: 1,
            parent_account_code: null,
            account_order: 1,
          },
          {
            ...declaredAccounts.accounts[1],
            account_code: "1.1",
            account_name: "Ativo Circulante",
            account_level: 2,
            parent_account_code: "1",
            account_order: 2,
            base_value: "100.00",
            considered_value: "100.00",
          },
          {
            ...declaredAccounts.accounts[2],
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
            ...declaredAccounts.accounts[2],
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
      },
    });
  });

  await page.goto("/analises/7/exercicios/2024/declarada");

  await expect(page.getByText("Ativo Circulante", { exact: true })).toHaveCount(1);
  await expect(page.getByText("Caixa e Equivalentes")).toBeVisible();
  await expect(page.getByText("R$ 100,00").first()).toBeVisible();
  await expect(page.getByText("Banco Conta Movimento")).toHaveCount(0);
});

test("importa ECD, executa camada declarada e navega para analise real", async ({ page }) => {
  await page.route("**/api/v1/ecd/imports", async (route) => {
    await route.fulfill({ json: { imports: [] } });
  });

  await page.route("**/api/v1/ecd/import", async (route) => {
    await route.fulfill({
      json: {
        analysis_id: "analysis-real",
        company_id: "company-real",
        ecd_file_id: "ecd-real",
        year: 2024,
        methodology_version_id: "metodologia-2024.1",
        status: "nao_executado",
      },
    });
  });

  await page.route("**/api/v1/analyses/analysis-real/exercises/2024/declared/run", async (route) => {
    await route.fulfill({
      json: {
        analysis_id: "analysis-real",
        year: 2024,
        status: "concluido",
        snapshots_created: 2,
        status_counts: { MAPEADO: 2 },
      },
    });
  });

  await page.route("**/api/v1/analyses/analysis-real/exercises/2024/declared", async (route) => {
    await route.fulfill({ json: { ...declaredSummary, analysis_id: "analysis-real" } });
  });

  await page.route("**/api/v1/analyses/analysis-real/exercises/2024/declared/accounts", async (route) => {
    await route.fulfill({ json: { ...declaredAccounts, analysis_id: "analysis-real" } });
  });

  await page.goto("/importar-ecd");
  await page.getByLabel(/Nenhum arquivo selecionado/).setInputFiles({
    name: "valid.ecd",
    mimeType: "text/plain",
    buffer: Buffer.from("|0000|LECD|2024|"),
  });
  await page.getByRole("button", { name: "Importar ECD" }).click();

  await expect(page.getByText("Análise analysis-real criada para 2024.")).toBeVisible();
  await expect(page.getByText("2 snapshots; status concluido.")).toBeVisible();

  await page.getByRole("button", { name: "Abrir análise" }).click();
  await expect(page).toHaveURL(/\/analises\/analysis-real\/exercicios\/2024\/declarada$/);
  await expect(page.getByText("Análise analysis-real · Exercício 2024")).toBeVisible();
});
