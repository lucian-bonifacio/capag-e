import { expect, test } from "@playwright/test";

const declaredSummary = {
  analysis_id: 7,
  year: 2024,
  accounts_count: 2,
  methodology_version_id: "metodologia-2024.1",
  status_counts: {
    MAPEADO: 1,
    NAO_MAPEADO_METODOLOGICAMENTE: 1,
  },
};

const declaredAccounts = {
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

  await expect(page.getByLabel("Carregando camada declarada")).toBeVisible();

  releaseAccounts();

  await expect(page.getByRole("heading", { name: "Camada Declarada" })).toBeVisible();
  await expect(page.getByText("metodologia-2024.1")).toBeVisible();
  await expect(page.getByText("MAPEADO").first()).toBeVisible();
  await expect(page.getByText("NAO_MAPEADO_METODOLOGICAMENTE").first()).toBeVisible();
  await expect(page.getByText("100000.00")).toBeVisible();
  await expect(page.getByText("2.01.01.07.01").first()).toBeVisible();
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
    page.getByRole("heading", { name: "Erro ao carregar camada declarada" }),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Recarregar" })).toBeVisible();
});

test("exibe estado vazio quando a API nao retorna contas", async ({ page }) => {
  await page.route("**/api/v1/analyses/7/exercises/2024/declared", async (route) => {
    await route.fulfill({ json: { ...declaredSummary, accounts_count: 0, status_counts: {} } });
  });

  await page.route("**/api/v1/analyses/7/exercises/2024/declared/accounts", async (route) => {
    await route.fulfill({ json: { ...declaredAccounts, accounts: [] } });
  });

  await page.goto("/analises/7/exercicios/2024/declarada");

  await expect(page.getByText("Sem registros.").first()).toBeVisible();
  await expect(
    page.getByText("A camada declarada ainda não possui contas persistidas para o exercício."),
  ).toBeVisible();
});
