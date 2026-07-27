import { expect, test } from "@playwright/test";


test("exibe assessment parcial sem apresenta-lo como final", async ({ page }) => {
  await page.route(
    "**/api/v1/analyses/7/exercises/2024/capag-assessment",
    async (route) => {
      await route.fulfill({
        json: {
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
          warnings: [],
          limitations: ["FCA parcial: somente FCO disponivel."],
          blocking_issues: [],
          methodology_version_id: "metodologia-2024.1",
        },
      });
    },
  );

  await page.goto("/analises/7/exercicios/2024/resultado");

  await expect(
    page.getByRole("heading", { name: "Resultado CAPAG-E" }),
  ).toBeVisible();
  await expect(page.getByText("R$ 540.000,00")).toBeVisible();
  await expect(page.getByRole("heading", { name: "FCA parcial" })).toBeVisible();
  await expect(page.getByText("Parcial").first()).toBeVisible();
  await expect(page.getByText("FCA final")).toHaveCount(0);
});
