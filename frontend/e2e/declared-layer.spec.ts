import { expect, test } from "@playwright/test";

const declaredBalance = {
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

test("exibe a arvore J100 sem switches ou recalculo local", async ({ page }) => {
  let releaseBalance: () => void = () => undefined;
  const balanceReady = new Promise<void>((resolve) => {
    releaseBalance = resolve;
  });
  await page.route(
    "**/api/v1/analyses/7/exercises/2024/declared/balance/accounts",
    async (route) => {
      await balanceReady;
      await route.fulfill({ json: declaredBalance });
    },
  );

  await page.goto("/analises/7/exercicios/2024/declarada");
  await expect(page.getByText("Carregando balanço declarado da ECD.")).toBeVisible();
  releaseBalance();

  await expect(page.getByRole("heading", { name: "Balanço Patrimonial" })).toBeVisible();
  await expect(page.getByText("Válido")).toBeVisible();
  await expect(page.getByText("Banco conta movimento")).toBeVisible();
  await expect(page.getByText("Capital social")).toBeVisible();
  await expect(page.getByText("Visão declarada · sem ajustes")).toBeVisible();
  await expect(page.getByRole("checkbox")).toHaveCount(0);
});

test("abre os componentes I050 I052 e I155 sob demanda", async ({ page }) => {
  await page.route(
    "**/api/v1/analyses/7/exercises/2024/declared/balance/accounts",
    async (route) => route.fulfill({ json: declaredBalance }),
  );
  await page.route(
    "**/api/v1/analyses/7/exercises/2024/declared/balance/accounts/AGL-CAIXA/components",
    async (route) =>
      route.fulfill({
        json: {
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
        },
      }),
  );

  await page.goto("/analises/7/exercicios/2024/declarada");
  await page.getByRole("button", { name: "Ver componentes (1)" }).first().click();

  await expect(
    page.getByRole("dialog", { name: "Componentes — Banco conta movimento" }),
  ).toBeVisible();
  await expect(page.getByText("1.01.01.001")).toBeVisible();
  await expect(page.getByText("CC01")).toBeVisible();
  await expect(page.getByText(/I052 linha 5/)).toBeVisible();
});

test("exibe estado bloqueante e limitacao sem fabricar balanco", async ({ page }) => {
  await page.route(
    "**/api/v1/analyses/7/exercises/2024/declared/balance/accounts",
    async (route) =>
      route.fulfill({
        json: {
          ...declaredBalance,
          balance_status: "OBRIGATORIO_AUSENTE",
          is_blocking: true,
          assets_final_amount: null,
          liabilities_and_equity_final_amount: null,
          difference: null,
          rows: [],
          limitations: ["J100_OBRIGATORIO_AUSENTE"],
        },
      }),
  );

  await page.goto("/analises/7/exercicios/2024/declarada");

  await expect(page.getByText("Balanço ausente")).toBeVisible();
  await expect(page.getByText("Balanço J100 obrigatório ausente.")).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Balanço declarado indisponível" }),
  ).toBeVisible();
});

test("exibe erro recuperavel quando a API do balanco falha", async ({ page }) => {
  await page.route(
    "**/api/v1/analyses/7/exercises/2024/declared/balance/accounts",
    async (route) => route.fulfill({ status: 503, json: { detail: "indisponivel" } }),
  );

  await page.goto("/analises/7/exercicios/2024/declarada");

  await expect(
    page.getByRole("heading", { name: "Erro ao carregar balanço patrimonial" }),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Tentar novamente" })).toBeVisible();
});
