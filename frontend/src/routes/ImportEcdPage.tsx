import { AlertTriangle, CheckCircle2, FileInput, Loader2, Play, Trash2, Upload } from "lucide-react";
import { useQueryClient } from "@tanstack/react-query";
import { type FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  EcdImportConflictError,
  deleteEcdImport,
  fetchEcdImports,
  importEcd,
  runDeclaredLayer,
  type DeclaredRunResponse,
  type EcdImportResponse,
  type ExistingEcdImport,
} from "../api/declared";

type ImportStep = "idle" | "importing" | "running" | "success" | "error";

function statusLabel(step: ImportStep) {
  if (step === "importing") {
    return "Importando";
  }

  if (step === "running") {
    return "Processando";
  }

  if (step === "success") {
    return "Concluido";
  }

  if (step === "error") {
    return "Erro";
  }

  return "Aguardando";
}

function statusVariant(step: ImportStep): "neutral" | "warning" | "success" | "danger" {
  if (step === "success") {
    return "success";
  }

  if (step === "error") {
    return "danger";
  }

  if (step === "importing" || step === "running") {
    return "warning";
  }

  return "neutral";
}

export function ImportEcdPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [file, setFile] = useState<File | null>(null);
  const [step, setStep] = useState<ImportStep>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [importResult, setImportResult] = useState<EcdImportResponse | null>(null);
  const [runResult, setRunResult] = useState<DeclaredRunResponse | null>(null);
  const [existingImport, setExistingImport] = useState<ExistingEcdImport | null>(null);
  const [existingImports, setExistingImports] = useState<ExistingEcdImport[]>([]);
  const [importsError, setImportsError] = useState<string | null>(null);
  const [removingEcdFileId, setRemovingEcdFileId] = useState<string | null>(null);

  const isBusy = step === "importing" || step === "running";
  const canOpenAnalysis =
    importResult !== null && (runResult !== null || existingImport !== null) && !isBusy;

  useEffect(() => {
    void loadExistingImports();
  }, []);

  async function loadExistingImports() {
    try {
      setImportsError(null);
      const response = await fetchEcdImports();
      setExistingImports(response.imports);
      queryClient.setQueryData(["ecd-imports"], response);
    } catch (error) {
      setImportsError(
        error instanceof Error ? error.message : "Nao foi possivel carregar importacoes existentes.",
      );
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!file) {
      setStep("error");
      setErrorMessage("Selecione um arquivo ECD antes de importar.");
      return;
    }

    setErrorMessage(null);
    setImportResult(null);
    setRunResult(null);
    setExistingImport(null);

    try {
      setStep("importing");
      const imported = await importEcd(file);
      setImportResult(imported);

      setStep("running");
      const run = await runDeclaredLayer(imported.analysis_id, imported.year);
      setRunResult(run);

      setStep("success");
      await loadExistingImports();
    } catch (error) {
      if (error instanceof EcdImportConflictError) {
        setImportResult(error.existingImport);
        setExistingImport(error.existingImport);
        setStep("error");
        setErrorMessage(error.message);
        await loadExistingImports();
        return;
      }

      setStep("error");
      setErrorMessage(error instanceof Error ? error.message : "Falha ao importar ECD.");
    }
  }

  function openAnalysis() {
    if (!importResult) {
      return;
    }

    navigate(`/analises/${importResult.analysis_id}/exercicios/${importResult.year}/declarada`);
  }

  async function removeExistingImport(existing: ExistingEcdImport) {
    const confirmed = window.confirm(
      `Remover a importacao ${existing.original_filename}? Esta acao apaga a analise e os dados normalizados associados.`,
    );
    if (!confirmed) {
      return;
    }

    try {
      setRemovingEcdFileId(existing.ecd_file_id);
      await deleteEcdImport(existing.ecd_file_id);
      if (importResult?.ecd_file_id === existing.ecd_file_id) {
        setImportResult(null);
        setRunResult(null);
        setExistingImport(null);
        setStep("idle");
      }
      await loadExistingImports();
    } catch (error) {
      setImportsError(error instanceof Error ? error.message : "Nao foi possivel remover a importacao.");
    } finally {
      setRemovingEcdFileId(null);
    }
  }

  return (
    <>
      <header className="app-topbar">
        <div>
          <h1 className="app-title">Importar ECD</h1>
          <p className="app-subtitle">Entrada oficial para análise declarada</p>
        </div>
        <span className="status-badge" data-variant={statusVariant(step)}>
          {statusLabel(step)}
        </span>
      </header>

      <main className="app-content import-content">
        <section className="declared-card import-card">
          <div className="section-header">
            <div>
              <p className="eyebrow">Arquivo ECD</p>
              <h2>Selecionar e importar</h2>
            </div>
          </div>

          <form className="import-form" onSubmit={handleSubmit}>
            <label className="file-picker">
              <FileInput aria-hidden="true" size={20} />
              <span>{file?.name ?? "Nenhum arquivo selecionado"}</span>
              <input
                accept=".ecd,.txt"
                disabled={isBusy}
                onChange={(event) => setFile(event.target.files?.[0] ?? null)}
                type="file"
              />
            </label>

            <div className="import-actions">
              <button className="button-primary" disabled={!file || isBusy} type="submit">
                {isBusy ? <Loader2 aria-hidden="true" size={16} /> : <Upload aria-hidden="true" size={16} />}
                Importar ECD
              </button>
              <button
                className="button-secondary"
                disabled={!canOpenAnalysis}
                onClick={openAnalysis}
                type="button"
              >
                <Play aria-hidden="true" size={16} />
                Abrir análise
              </button>
            </div>
          </form>
        </section>

        <section className="declared-card">
          <div className="section-header">
            <div>
              <p className="eyebrow">Status</p>
              <h2>Processamento da análise</h2>
            </div>
          </div>

          <div className="event-list">
            <div className="event-row">
              <span className="event-icon" data-variant={importResult ? "success" : "neutral"}>
                {importResult ? <CheckCircle2 aria-hidden="true" size={16} /> : <FileInput aria-hidden="true" size={16} />}
              </span>
              <div>
                <strong>Importação ECD</strong>
                <span>
                  {importResult
                    ? `Análise ${importResult.analysis_id} ${
                        existingImport ? "existente" : "criada"
                      } para ${importResult.year}.`
                    : "Aguardando envio do arquivo."}
                </span>
              </div>
            </div>

            <div className="event-row">
              <span className="event-icon" data-variant={runResult ? "success" : "neutral"}>
                {runResult ? <CheckCircle2 aria-hidden="true" size={16} /> : <Play aria-hidden="true" size={16} />}
              </span>
              <div>
                <strong>Camada declarada</strong>
                <span>
                  {runResult
                    ? `${runResult.snapshots_created} snapshots; status ${runResult.status}.`
                    : "Aguardando execução no backend."}
                </span>
              </div>
            </div>

            {errorMessage ? (
              <div className="event-row">
                <span className="event-icon" data-variant="danger">
                  <AlertTriangle aria-hidden="true" size={16} />
                </span>
                <div>
                  <strong>Falha</strong>
                  <span>{errorMessage}</span>
                  {existingImport ? (
                    <button className="inline-action" onClick={openAnalysis} type="button">
                      Abrir análise existente
                    </button>
                  ) : null}
                </div>
              </div>
            ) : null}
          </div>
        </section>

        <section className="declared-card">
          <div className="section-header">
            <div>
              <p className="eyebrow">Importações existentes</p>
              <h2>Análises disponíveis</h2>
            </div>
          </div>

          {importsError ? (
            <div className="event-row">
              <span className="event-icon" data-variant="danger">
                <AlertTriangle aria-hidden="true" size={16} />
              </span>
              <div>
                <strong>Falha</strong>
                <span>{importsError}</span>
              </div>
            </div>
          ) : null}

          {existingImports.length === 0 ? (
            <p className="empty-state">Sem registros.</p>
          ) : (
            <div className="imports-table-wrap">
              <table className="imports-table">
                <thead>
                  <tr>
                    <th>Arquivo</th>
                    <th>Período</th>
                    <th>Status</th>
                    <th>Análise</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {existingImports.map((existing) => (
                    <tr key={existing.ecd_file_id}>
                      <td>
                        <strong>{existing.original_filename}</strong>
                        <span className="table-meta tnum">{existing.ecd_file_id}</span>
                      </td>
                      <td className="tnum">{formatPeriod(existing)}</td>
                      <td>
                        <span className="status-badge" data-variant="neutral">
                          {existing.status}
                        </span>
                      </td>
                      <td className="tnum">{existing.analysis_id}</td>
                      <td>
                        <div className="row-actions">
                          <button
                            className="button-secondary"
                            onClick={() =>
                              navigate(
                                `/analises/${existing.analysis_id}/exercicios/${existing.year}/declarada`,
                              )
                            }
                            type="button"
                          >
                            <Play aria-hidden="true" size={16} />
                            Abrir
                          </button>
                          <button
                            className="button-danger"
                            disabled={removingEcdFileId === existing.ecd_file_id}
                            onClick={() => void removeExistingImport(existing)}
                            type="button"
                          >
                            {removingEcdFileId === existing.ecd_file_id ? (
                              <Loader2 aria-hidden="true" size={16} />
                            ) : (
                              <Trash2 aria-hidden="true" size={16} />
                            )}
                            Remover
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </>
  );
}

function formatPeriod(existing: ExistingEcdImport) {
  return `${formatDate(existing.period_start)} a ${formatDate(existing.period_end)}`;
}

function formatDate(value: string) {
  const [year, month, day] = value.split("-");
  return `${day}/${month}/${year}`;
}
