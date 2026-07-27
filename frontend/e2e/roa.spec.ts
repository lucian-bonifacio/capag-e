import { readFileSync } from "node:fs";

import { expect, test } from "@playwright/test";


const ECD_PATH =
  "/workspace/docs/reference/ecd-example/ECD 2024 DATAPACK.txt";
const ECD_FILENAME = "ECD 2024 DATAPACK.txt";


test("calcula, audita e exporta ROA + PLRA da ECD governada", async ({
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
  const roaBase = `/api/v1/analyses/${analysisId}/exercises/2024/roa`;
  const runResponse = await request.post(`${roaBase}/run`);
  expect(runResponse.ok()).toBeTruthy();
  const calculation = (await runResponse.json()) as {
    roa_final: string;
    roa_status: string;
    gross_revenue: string;
    operating_costs: string;
    audit_rows: unknown[];
    pending_groups: Array<{ code: string; blocks_roa: boolean }>;
    limitations: string[];
    capag_assessment: {
      roa_value: string;
      capag_e_status: string;
    } | null;
  };

  expect(calculation.roa_final).toBe("122781.16");
  expect(calculation.gross_revenue).toBe("5659097.92");
  expect(calculation.operating_costs).toBe("3774336.63");
  expect(calculation.roa_status).toBe("bloqueado_por_pendencia");
  expect(calculation.audit_rows).toHaveLength(43);
  expect(calculation.pending_groups).toHaveLength(5);
  expect(
    calculation.pending_groups.filter((group) => group.blocks_roa),
  ).toHaveLength(4);
  expect(calculation.limitations.join(" ")).toContain("J150");
  expect(calculation.capag_assessment?.roa_value).toBe("122781.16");
  expect(calculation.capag_assessment?.capag_e_status).toBe("bloqueado");

  const exportResponse = await request.get(`${roaBase}/export.xlsx`);
  expect(exportResponse.ok()).toBeTruthy();
  expect(exportResponse.headers()["content-type"]).toContain(
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  );
  expect((await exportResponse.body()).byteLength).toBeGreaterThan(1000);

  await page.goto(`/analises/${analysisId}/exercicios/2024/roa`);
  await expect(page.getByText("R$ 122.781,16").first()).toBeVisible();
  await expect(page.getByText("Bloqueado por pendência")).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Pendências do ROA" }),
  ).toBeVisible();
  await expect(page.getByRole("table")).toBeVisible();
  await expect(page.getByRole("link", { name: "Exportar Excel" })).toHaveAttribute(
    "href",
    `${roaBase}/export.xlsx`,
  );
  await page
    .getByRole("button", { name: /Decidir conta/ })
    .first()
    .click();
  await expect(
    page.getByRole("dialog", { name: "Decisão sobre conta" }),
  ).toBeVisible();
});
