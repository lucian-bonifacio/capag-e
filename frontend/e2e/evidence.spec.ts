import { readFileSync } from "node:fs";

import { expect, test } from "@playwright/test";
import type { APIRequestContext } from "@playwright/test";


const ECD_PATH =
  "/workspace/docs/reference/ecd-example/ECD 2024 DATAPACK.txt";
const ECD_FILENAME = "ECD 2024 DATAPACK.txt";


test("bloqueia e libera PLRA com evidencia e avaliacao de ativo", async ({
  page,
  request,
}) => {
  const analysisId = await ensureImport(request);
  const evidenceBase = `/api/v1/analyses/${analysisId}/exercises/2024/evidences`;
  const plraBase = `/api/v1/analyses/${analysisId}/exercises/2024/plra`;

  await cleanupPreviousE2eState(request, analysisId, evidenceBase);
  const baselineResponse = await request.post(`${plraBase}/run`);
  expect(baselineResponse.ok()).toBeTruthy();
  const baseline = await baselineResponse.json();
  expect(baseline.plra_status).toBe("calculado");

  const auditResponse = await request.get(`${plraBase}/audit`);
  expect(auditResponse.ok()).toBeTruthy();
  const audit = await auditResponse.json();
  const asset = audit.rows.find(
    (row: {
      inclusion_status: string;
      default_discount_percent: string | null;
    }) =>
      row.inclusion_status === "incluido_ativo" &&
      row.default_discount_percent !== null,
  );
  expect(asset).toBeDefined();

  let evidenceId: string | undefined;
  let assessmentId: string | undefined;
  let validatedAssetPayload: Record<string, unknown> | undefined;
  try {
    const evidenceResponse = await request.post(evidenceBase, {
      data: {
        scope_type: "account",
        scope_key: asset.account_code,
        adjustment_type: "e2e_modulo_4",
        method_component: "PLRA",
        amount_impact: "100.00",
        impact_base_value: "1000.00",
        required_evidence_type: "laudo_abnt_nbr_14653",
        evidence_status: "pendente",
        analyst_justification: "Validação E2E pendente.",
        review_notes: null,
        can_change_capag_status: false,
        can_reverse_prudential_sign: false,
      },
    });
    expect(evidenceResponse.status()).toBe(201);
    const evidence = await evidenceResponse.json();
    evidenceId = evidence.evidence_id;
    expect(evidence.materiality_level).toBe("critica");
    expect(evidence.blocks_final_report).toBe(true);

    assessmentId = `e2e-asset-${asset.account_code}`;
    const pendingAssetPayload = {
      analysis_id: analysisId,
      exercise_year: 2024,
      account_code: asset.account_code,
      realizability_classification: "liquidacao_forcada_exige_laudo",
      valuation_required: true,
      valuation_basis: "laudo_abnt_nbr_14653",
      forced_liquidation_value: asset.default_economic_value,
      analyst_adjusted_value: null,
      essentiality_status: "nao_essencial",
      valuation_status: "pendente",
      evidence_id: evidence.evidence_id,
    };
    validatedAssetPayload = {
      ...pendingAssetPayload,
      valuation_status: "validada",
    };
    const pendingAsset = await request.put(
      `/api/v1/assets/valuations/${assessmentId}`,
      { data: pendingAssetPayload },
    );
    expect(pendingAsset.ok()).toBeTruthy();
    expect((await pendingAsset.json()).blocks_plra).toBe(true);

    const blockedPlraResponse = await request.post(`${plraBase}/run`);
    expect(blockedPlraResponse.ok()).toBeTruthy();
    const blockedPlra = await blockedPlraResponse.json();
    expect(blockedPlra.plra_status).toBe("bloqueado_por_evidencia");
    expect(blockedPlra.plra_value).toBe(baseline.plra_value);

    const blockedCapagResponse = await request.post(
      `/api/v1/analyses/${analysisId}/exercises/2024/capag-assessment/run`,
      { data: { method: "fca_plra", fco_value: "0.00" } },
    );
    expect(blockedCapagResponse.ok()).toBeTruthy();
    expect((await blockedCapagResponse.json()).capag_e_status).toBe("bloqueado");

    const exportResponse = await request.get(`${evidenceBase}/export.xlsx`);
    expect(exportResponse.ok()).toBeTruthy();
    expect(exportResponse.headers()["content-type"]).toContain(
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    );
    expect((await exportResponse.body()).byteLength).toBeGreaterThan(1000);

    await page.goto(
      `/analises/${analysisId}/exercicios/2024/evidencias`,
    );
    await expect(page.getByText("Crítica").last()).toBeVisible();
    await expect(page.getByText("Bloqueia resultado")).toBeVisible();
    await page.getByRole("tab", { name: /Avaliação de ativos/ }).click();
    await expect(page.getByText("Bloqueia PLRA")).toBeVisible();
    await expect(page.getByRole("link", { name: "Exportar Excel" })).toBeVisible();

    const resolvedEvidence = await request.put(
      `/api/v1/evidences/${evidence.evidence_id}`,
      {
        data: {
          required_evidence_type: "laudo_abnt_nbr_14653",
          evidence_status: "validada",
          analyst_justification: "Validação E2E concluída.",
          review_notes: "Evidência conferida.",
          materiality_override: null,
        },
      },
    );
    expect(resolvedEvidence.ok()).toBeTruthy();
    const validatedAsset = await request.put(
      `/api/v1/assets/valuations/${assessmentId}`,
      {
        data: validatedAssetPayload,
      },
    );
    expect(validatedAsset.ok()).toBeTruthy();
    expect((await validatedAsset.json()).blocks_plra).toBe(false);

    const releasedPlraResponse = await request.post(`${plraBase}/run`);
    expect(releasedPlraResponse.ok()).toBeTruthy();
    const releasedPlra = await releasedPlraResponse.json();
    expect(releasedPlra.plra_status).toBe("calculado");
    expect(releasedPlra.plra_value).toBe(baseline.plra_value);

    const releasedCapagResponse = await request.post(
      `/api/v1/analyses/${analysisId}/exercises/2024/capag-assessment/run`,
      { data: { method: "fca_plra", fco_value: "0.00" } },
    );
    expect(releasedCapagResponse.ok()).toBeTruthy();
    expect((await releasedCapagResponse.json()).capag_e_status).toBe("parcial");
  } finally {
    if (evidenceId) {
      await resolveEvidence(request, evidenceId);
    }
    if (assessmentId && validatedAssetPayload) {
      await request.put(`/api/v1/assets/valuations/${assessmentId}`, {
        data: validatedAssetPayload,
      });
    }
    await request.post(`${plraBase}/run`);
  }
});


async function ensureImport(
  request: APIRequestContext,
): Promise<string> {
  const importsResponse = await request.get("/api/v1/ecd/imports");
  expect(importsResponse.ok()).toBeTruthy();
  const importsBody = await importsResponse.json();
  const existing = importsBody.imports.find(
    (item: { original_filename: string }) =>
      item.original_filename === ECD_FILENAME,
  );
  if (existing) return existing.analysis_id;

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
    return importBody.detail.existing_import.analysis_id;
  }
  expect(importResponse.ok()).toBeTruthy();
  return importBody.analysis_id;
}


async function cleanupPreviousE2eState(
  request: APIRequestContext,
  analysisId: string,
  evidenceBase: string,
) {
  const response = await request.get(evidenceBase);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  for (const evidence of body.items) {
    if (
      evidence.adjustment_type === "e2e_modulo_4" &&
      evidence.evidence_status !== "validada"
    ) {
      await resolveEvidence(request, evidence.evidence_id);
    }
  }
  const assetsResponse = await request.get(
    `/api/v1/analyses/${analysisId}/exercises/2024/assets/valuations`,
  );
  expect(assetsResponse.ok()).toBeTruthy();
  const assets = await assetsResponse.json();
  for (const asset of assets.items) {
    if (asset.assessment_id.startsWith("e2e-asset-")) {
      const update = await request.put(
        `/api/v1/assets/valuations/${asset.assessment_id}`,
        {
          data: {
            analysis_id: analysisId,
            exercise_year: 2024,
            account_code: asset.account_code,
            realizability_classification: asset.realizability_classification,
            valuation_required: asset.valuation_required,
            valuation_basis: asset.valuation_basis,
            forced_liquidation_value: asset.forced_liquidation_value,
            analyst_adjusted_value: asset.analyst_adjusted_value,
            essentiality_status: asset.essentiality_status,
            valuation_status: "validada",
            evidence_id: asset.evidence_id,
          },
        },
      );
      expect(update.ok()).toBeTruthy();
    }
  }
}


async function resolveEvidence(
  request: APIRequestContext,
  evidenceId: string,
) {
  return request.put(`/api/v1/evidences/${evidenceId}`, {
    data: {
      required_evidence_type: "laudo_abnt_nbr_14653",
      evidence_status: "validada",
      analyst_justification: "Limpeza do cenário E2E.",
      review_notes: "Evidência conferida.",
      materiality_override: null,
    },
  });
}
