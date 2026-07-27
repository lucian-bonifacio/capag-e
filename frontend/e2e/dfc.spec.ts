import { readFileSync } from "node:fs";

import { expect, test } from "@playwright/test";


const ECD_PATH =
  "/workspace/docs/reference/ecd-example/ECD 2024 DATAPACK.txt";
const ECD_FILENAME = "ECD 2024 DATAPACK.txt";


test("calcula, exibe e exporta DFC/FCA da ECD governada", async ({
  page,
  request,
}) => {
  const importsResponse = await request.get("/api/v1/ecd/imports");
  expect(importsResponse.ok()).toBeTruthy();
  const importsBody = (await importsResponse.json()) as {
    imports: Array<{
      analysis_id: string;
      original_filename: string;
      year: number;
    }>;
  };
  let imported = importsBody.imports.find(
    (item) => item.original_filename === ECD_FILENAME && item.year === 2024,
  );

  if (!imported) {
    const importResponse = await request.post("/api/v1/ecd/import", {
      multipart: {
        file: {
          buffer: readFileSync(ECD_PATH),
          mimeType: "text/plain",
          name: ECD_FILENAME,
        },
      },
    });
    const importBody = await importResponse.json();
    if (importResponse.status() === 409) {
      imported = importBody.detail.existing_import;
    } else {
      expect(importResponse.ok()).toBeTruthy();
      imported = importBody;
    }
  }

  expect(imported).toBeDefined();
  const analysisId = imported!.analysis_id;
  const dfcBase = `/api/v1/analyses/${analysisId}/exercises/2024/dfc`;
  const runResponse = await request.post(`${dfcBase}/run`);
  expect(runResponse.ok()).toBeTruthy();
  const calculation = (await runResponse.json()) as {
    fca_value: string;
    fca_status: string;
    operational_flow: string;
    investment_flow: string;
    financing_flow: string;
    audit_rows: unknown[];
    pending_issues: unknown[];
  };

  expect(calculation.fca_value).toBe("92988.06");
  expect(calculation.operational_flow).toBe("235884.83");
  expect(calculation.investment_flow).toBe("-28448.78");
  expect(calculation.financing_flow).toBe("-114447.99");
  expect(calculation.fca_status).toBe("bloqueado_por_evidencia");
  expect(calculation.audit_rows).toHaveLength(4251);
  expect(calculation.pending_issues.length).toBeGreaterThan(0);

  const exportResponse = await request.get(`${dfcBase}/export.xlsx`);
  expect(exportResponse.ok()).toBeTruthy();
  expect(exportResponse.headers()["content-type"]).toContain(
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  );
  expect((await exportResponse.body()).byteLength).toBeGreaterThan(1000);

  await page.goto(`/analises/${analysisId}/exercicios/2024/dfc`);
  await expect(page.getByText("R$ 92.988,06")).toBeVisible();
  await expect(page.getByText("Bloqueado por evidência")).toBeVisible();
  await expect(
    page.locator(".dfc-result-band dd").filter({ hasText: /^4251$/ }),
  ).toBeVisible();
  await expect(page.getByRole("link", { name: "Exportar Excel" })).toHaveAttribute(
    "href",
    `${dfcBase}/export.xlsx`,
  );
  await expect(page.getByRole("heading", { name: "Pendências da DFC" })).toBeVisible();
  await expect(page.getByRole("table")).toBeVisible();
});
