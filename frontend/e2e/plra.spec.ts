import { readFileSync } from "node:fs";

import { expect, test } from "@playwright/test";


const ECD_PATH =
  "/workspace/docs/reference/ecd-example/ECD 2024 DATAPACK.txt";
const ECD_FILENAME = "ECD 2024 DATAPACK.txt";


test("calcula PLRA da ECD governada e propaga o snapshot para CAPAG-E", async ({
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
  const plraBase = `/api/v1/analyses/${analysisId}/exercises/2024/plra`;
  const plraRun = await request.post(`${plraBase}/run`);
  expect(plraRun.ok()).toBeTruthy();
  const plra = (await plraRun.json()) as {
    plra_status: string;
    plra_value: string;
  };

  expect(plra.plra_status).toBe("calculado");
  expect(plra.plra_value).toBe("-1045941.70");

  const exportResponse = await request.get(`${plraBase}/export.xlsx`);
  expect(exportResponse.ok()).toBeTruthy();
  expect(exportResponse.headers()["content-type"]).toContain(
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  );

  await page.goto(`/analises/${analysisId}/exercicios/2024/plra`);
  await expect(page.getByText("-R$ 1.045.941,70")).toBeVisible();
  await expect(page.getByText("Calculado", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Abrir auditoria" }).click();
  await expect(page.getByRole("dialog", { name: "Auditoria do PLRA" })).toBeVisible();
  await expect(page.getByText("Política interna default").first()).toBeVisible();
  await page.getByRole("button", { name: "Fechar auditoria" }).click();

  const capagRun = await request.post(
    `/api/v1/analyses/${analysisId}/exercises/2024/capag-assessment/run`,
    {
      data: {
        method: "fca_plra",
        fco_value: "0.00",
      },
    },
  );
  expect(capagRun.ok()).toBeTruthy();
  const capag = (await capagRun.json()) as {
    capag_e_status: string;
    plra_status: string;
    plra_value: string;
  };
  expect(capag.plra_value).toBe(plra.plra_value);
  expect(capag.plra_status).toBe(plra.plra_status);
  expect(capag.capag_e_status).toBe("parcial");

  await page.goto(`/analises/${analysisId}/exercicios/2024/resultado`);
  await expect(page.getByText("-R$ 1.045.941,70").first()).toBeVisible();
  await expect(page.getByText("Parcial").first()).toBeVisible();
});
