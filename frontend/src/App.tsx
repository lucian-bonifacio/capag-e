import { Activity, ArrowLeftRight, Calculator, ClipboardCheck, Files, LayoutDashboard, Scale, TrendingUp, Upload } from "lucide-react";
import { QueryClient, QueryClientProvider, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { BrowserRouter, Link, Navigate, Route, Routes, useLocation, useParams } from "react-router-dom";

import { CapagApiError, fetchCapagAssessment } from "./api/capag";
import {
  fetchPlra,
  fetchPlraAudit,
  PlraApiError,
  runPlra,
} from "./api/plra";
import {
  fetchDeclaredAccounts,
  fetchDeclaredBalanceAccounts,
  fetchEcdImports,
  fetchDeclaredSummary,
} from "./api/declared";
import {
  createEvidence,
  EvidenceApiError,
  fetchAssetValuations,
  fetchEvidences,
  updateAssetValuation,
  updateEvidence,
} from "./api/evidence";
import {
  createDfcDecision,
  DfcApiError,
  fetchDfc,
  runDfc,
} from "./api/dfc";
import {
  createRoaDecision,
  fetchRoa,
  RoaApiError,
  runRoa,
} from "./api/roa";
import { BalanceDashboardPage } from "./routes/BalanceDashboardPage";
import { CapagAssessmentPage } from "./routes/CapagAssessmentPage";
import { DeclaredLayerPage } from "./routes/DeclaredLayerPage";
import { EvidencePage } from "./routes/EvidencePage";
import { DfcPage } from "./routes/DfcPage";
import { ImportEcdPage } from "./routes/ImportEcdPage";
import { PlraPage } from "./routes/PlraPage";
import { RoaPage } from "./routes/RoaPage";
import "./App.css";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/analises/:analysisId/exercicios/:year/declarada", match: "/dashboard" },
  { label: "Balanço Patrimonial", icon: Scale, path: "/analises/:analysisId/exercicios/:year/declarada", match: "/declarada" },
  { label: "PLRA", icon: Calculator, path: "/analises/:analysisId/exercicios/:year/plra", match: "/plra" },
  { label: "DFC / FCA", icon: ArrowLeftRight, path: "/analises/:analysisId/exercicios/:year/dfc", match: "/dfc" },
  { label: "ROA", icon: TrendingUp, path: "/analises/:analysisId/exercicios/:year/roa", match: "/roa" },
  { label: "Evidências", icon: Files, path: "/analises/:analysisId/exercicios/:year/evidencias", match: "/evidencias" },
  { label: "Indicadores CAPAG", icon: Activity, path: "/analises/:analysisId/exercicios/:year/resultado", match: "/resultado" },
  { label: "Auditoria", icon: ClipboardCheck, path: "/analises/:analysisId/exercicios/:year/auditoria", match: "/auditoria", badge: "1" },
  { label: "Importar ECD", icon: Upload, path: "/importar-ecd", match: "/importar-ecd" },
];

function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        staleTime: 30_000,
      },
    },
  });
}

function DeclaredLayerRoute() {
  const { analysisId = "", year = "" } = useParams();

  const summaryQuery = useQuery({
    queryKey: ["declared-summary", analysisId, year],
    queryFn: () => fetchDeclaredSummary(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });

  const balanceAccountsQuery = useQuery({
    queryKey: ["declared-balance-accounts", analysisId, year],
    queryFn: () => fetchDeclaredBalanceAccounts(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });

  const retry = () => {
    void summaryQuery.refetch();
    void balanceAccountsQuery.refetch();
  };

  return (
    <BalanceDashboardPage
      accounts={balanceAccountsQuery.data?.accounts}
      analysisId={analysisId}
      consistencyWarnings={balanceAccountsQuery.data?.consistency_warnings}
      isError={summaryQuery.isError || balanceAccountsQuery.isError}
      isLoading={summaryQuery.isLoading || balanceAccountsQuery.isLoading}
      onRetry={retry}
      summary={summaryQuery.data}
      year={year}
    />
  );
}

function AuditoriaRoute() {
  const { analysisId = "", year = "" } = useParams();

  const summaryQuery = useQuery({
    queryKey: ["declared-summary", analysisId, year],
    queryFn: () => fetchDeclaredSummary(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });

  const accountsQuery = useQuery({
    queryKey: ["declared-accounts", analysisId, year],
    queryFn: () => fetchDeclaredAccounts(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });

  const retry = () => {
    void summaryQuery.refetch();
    void accountsQuery.refetch();
  };

  return (
    <DeclaredLayerPage
      accounts={accountsQuery.data?.accounts}
      analysisId={analysisId}
      isError={summaryQuery.isError || accountsQuery.isError}
      isLoading={summaryQuery.isLoading || accountsQuery.isLoading}
      onRetry={retry}
      summary={summaryQuery.data}
      year={year}
    />
  );
}

function CapagAssessmentRoute() {
  const { analysisId = "", year = "" } = useParams();
  const assessmentQuery = useQuery({
    queryKey: ["capag-assessment", analysisId, year],
    queryFn: () => fetchCapagAssessment(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });
  const errorStatus =
    assessmentQuery.error instanceof CapagApiError
      ? assessmentQuery.error.status
      : undefined;

  return (
    <CapagAssessmentPage
      analysisId={analysisId}
      assessment={assessmentQuery.data}
      errorStatus={errorStatus}
      isError={assessmentQuery.isError}
      isLoading={assessmentQuery.isLoading}
      onRetry={() => void assessmentQuery.refetch()}
      year={year}
    />
  );
}

function PlraRoute() {
  const { analysisId = "", year = "" } = useParams();
  const queryClient = useQueryClient();
  const [isAuditOpen, setAuditOpen] = useState(false);
  const calculationQuery = useQuery({
    queryKey: ["plra", analysisId, year],
    queryFn: () => fetchPlra(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });
  const auditQuery = useQuery({
    queryKey: ["plra-audit", analysisId, year],
    queryFn: () => fetchPlraAudit(analysisId, year),
    enabled: isAuditOpen && Boolean(calculationQuery.data),
  });
  const runMutation = useMutation({
    mutationFn: () => runPlra(analysisId, year),
    onSuccess: (calculation) => {
      queryClient.setQueryData(["plra", analysisId, year], calculation);
      void queryClient.invalidateQueries({
        queryKey: ["plra-audit", analysisId, year],
      });
      void queryClient.invalidateQueries({
        queryKey: ["capag-assessment", analysisId, year],
      });
    },
  });
  const queryError =
    runMutation.error instanceof PlraApiError
      ? runMutation.error
      : calculationQuery.error instanceof PlraApiError
        ? calculationQuery.error
        : undefined;

  return (
    <PlraPage
      analysisId={analysisId}
      audit={auditQuery.data}
      calculation={calculationQuery.data}
      errorMessage={queryError?.message}
      errorStatus={queryError?.status}
      isAuditError={auditQuery.isError}
      isAuditLoading={auditQuery.isLoading}
      isAuditOpen={isAuditOpen}
      isError={calculationQuery.isError || runMutation.isError}
      isLoading={calculationQuery.isLoading}
      isRunning={runMutation.isPending}
      onAuditClose={() => setAuditOpen(false)}
      onAuditOpen={() => setAuditOpen(true)}
      onRetry={() => void calculationQuery.refetch()}
      onRun={() => runMutation.mutate()}
      year={year}
    />
  );
}

function EvidenceRoute() {
  const { analysisId = "", year = "" } = useParams();
  const queryClient = useQueryClient();
  const evidencesQuery = useQuery({
    queryKey: ["evidences", analysisId, year],
    queryFn: () => fetchEvidences(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });
  const assetsQuery = useQuery({
    queryKey: ["asset-valuations", analysisId, year],
    queryFn: () => fetchAssetValuations(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });
  const refreshDependents = async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ["evidences", analysisId, year] }),
      queryClient.invalidateQueries({ queryKey: ["asset-valuations", analysisId, year] }),
      queryClient.invalidateQueries({ queryKey: ["plra", analysisId, year] }),
      queryClient.invalidateQueries({ queryKey: ["dfc", analysisId, year] }),
      queryClient.invalidateQueries({ queryKey: ["roa", analysisId, year] }),
      queryClient.invalidateQueries({ queryKey: ["capag-assessment", analysisId, year] }),
    ]);
  };
  const createMutation = useMutation({
    mutationFn: (payload: Parameters<typeof createEvidence>[2]) =>
      createEvidence(analysisId, year, payload),
    onSuccess: refreshDependents,
  });
  const updateMutation = useMutation({
    mutationFn: ({
      evidenceId,
      payload,
    }: {
      evidenceId: string;
      payload: Parameters<typeof updateEvidence>[1];
    }) => updateEvidence(evidenceId, payload),
    onSuccess: refreshDependents,
  });
  const assetMutation = useMutation({
    mutationFn: ({
      assessmentId,
      payload,
    }: {
      assessmentId: string;
      payload: Parameters<typeof updateAssetValuation>[1];
    }) => updateAssetValuation(assessmentId, payload),
    onSuccess: refreshDependents,
  });
  const error = [
    createMutation.error,
    updateMutation.error,
    assetMutation.error,
    evidencesQuery.error,
    assetsQuery.error,
  ].find((candidate) => candidate instanceof EvidenceApiError);

  return (
    <EvidencePage
      analysisId={analysisId}
      assets={assetsQuery.data}
      errorMessage={error instanceof Error ? error.message : undefined}
      evidences={evidencesQuery.data}
      isError={evidencesQuery.isError || assetsQuery.isError}
      isLoading={evidencesQuery.isLoading || assetsQuery.isLoading}
      isSaving={
        createMutation.isPending ||
        updateMutation.isPending ||
        assetMutation.isPending
      }
      onCreateEvidence={async (payload) => {
        await createMutation.mutateAsync(payload);
      }}
      onRetry={() => {
        void evidencesQuery.refetch();
        void assetsQuery.refetch();
      }}
      onUpdateAsset={async (assessmentId, payload) => {
        await assetMutation.mutateAsync({ assessmentId, payload });
      }}
      onUpdateEvidence={async (evidenceId, payload) => {
        await updateMutation.mutateAsync({ evidenceId, payload });
      }}
      year={year}
    />
  );
}

function DfcRoute() {
  const { analysisId = "", year = "" } = useParams();
  const queryClient = useQueryClient();
  const calculationQuery = useQuery({
    queryKey: ["dfc", analysisId, year],
    queryFn: () => fetchDfc(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });
  const runMutation = useMutation({
    mutationFn: () => runDfc(analysisId, year),
    onSuccess: (calculation) => {
      queryClient.setQueryData(["dfc", analysisId, year], calculation);
      void queryClient.invalidateQueries({
        queryKey: ["capag-assessment", analysisId, year],
      });
    },
  });
  const decisionMutation = useMutation({
    mutationFn: (payload: Parameters<typeof createDfcDecision>[2]) =>
      createDfcDecision(analysisId, year, payload),
    onSuccess: (calculation) => {
      queryClient.setQueryData(["dfc", analysisId, year], calculation);
      void queryClient.invalidateQueries({
        queryKey: ["capag-assessment", analysisId, year],
      });
    },
  });
  const queryError =
    decisionMutation.error instanceof DfcApiError
      ? decisionMutation.error
      : runMutation.error instanceof DfcApiError
        ? runMutation.error
        : calculationQuery.error instanceof DfcApiError
          ? calculationQuery.error
          : undefined;

  return (
    <DfcPage
      analysisId={analysisId}
      calculation={calculationQuery.data}
      errorMessage={queryError?.message}
      errorStatus={queryError?.status}
      isError={
        calculationQuery.isError ||
        runMutation.isError ||
        decisionMutation.isError
      }
      isLoading={calculationQuery.isLoading}
      isRunning={runMutation.isPending}
      isSavingDecision={decisionMutation.isPending}
      onDecision={async (payload) => {
        await decisionMutation.mutateAsync(payload);
      }}
      onRetry={() => void calculationQuery.refetch()}
      onRun={() => runMutation.mutate()}
      year={year}
    />
  );
}

function RoaRoute() {
  const { analysisId = "", year = "" } = useParams();
  const queryClient = useQueryClient();
  const calculationQuery = useQuery({
    queryKey: ["roa", analysisId, year],
    queryFn: () => fetchRoa(analysisId, year),
    enabled: analysisId.length > 0 && year.length > 0,
  });
  const runMutation = useMutation({
    mutationFn: () => runRoa(analysisId, year),
    onSuccess: (calculation) => {
      queryClient.setQueryData(["roa", analysisId, year], calculation);
      void queryClient.invalidateQueries({
        queryKey: ["capag-assessment", analysisId, year],
      });
    },
  });
  const decisionMutation = useMutation({
    mutationFn: (payload: Parameters<typeof createRoaDecision>[2]) =>
      createRoaDecision(analysisId, year, payload),
    onSuccess: (calculation) => {
      queryClient.setQueryData(["roa", analysisId, year], calculation);
      void queryClient.invalidateQueries({
        queryKey: ["capag-assessment", analysisId, year],
      });
    },
  });
  const queryError =
    decisionMutation.error instanceof RoaApiError
      ? decisionMutation.error
      : runMutation.error instanceof RoaApiError
        ? runMutation.error
        : calculationQuery.error instanceof RoaApiError
          ? calculationQuery.error
          : undefined;

  return (
    <RoaPage
      analysisId={analysisId}
      calculation={calculationQuery.data}
      errorMessage={queryError?.message}
      errorStatus={queryError?.status}
      isError={
        calculationQuery.isError ||
        runMutation.isError ||
        decisionMutation.isError
      }
      isLoading={calculationQuery.isLoading}
      isRunning={runMutation.isPending}
      isSavingDecision={decisionMutation.isPending}
      onDecision={async (payload) => {
        await decisionMutation.mutateAsync(payload);
      }}
      onRetry={() => void calculationQuery.refetch()}
      onRun={() => runMutation.mutate()}
      year={year}
    />
  );
}

function GovernedShell() {
  const location = useLocation();
  const analysisRouteMatch = location.pathname.match(
    /^\/analises\/([^/]+)\/exercicios\/([^/]+)/,
  );
  const importsQuery = useQuery({
    queryKey: ["ecd-imports"],
    queryFn: fetchEcdImports,
  });
  const latestImport = importsQuery.data?.imports?.[0];
  const currentAnalysisId = analysisRouteMatch?.[1] ?? latestImport?.analysis_id;
  const currentYear =
    analysisRouteMatch?.[2] ?? (latestImport ? String(latestImport.year) : undefined);

  return (
    <div className="app-shell">
      <aside className="app-sidebar" aria-label="Navegacao principal">
        <div className="app-brand">
          <div className="brand-logo">C</div>
          <span>CAPAG Analytics</span>
        </div>
        <nav className="app-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            const path = item.path.includes(":analysisId")
              ? currentAnalysisId && currentYear
                ? item.path
                    .replace(":analysisId", currentAnalysisId)
                    .replace(":year", currentYear)
                : "/importar-ecd"
              : item.path;

            return (
              <Link
                className="app-nav-item"
                data-active={location.pathname.endsWith(item.match)}
                key={item.label}
                to={path}
              >
                <Icon aria-hidden="true" size={18} strokeWidth={1.8} />
                <span className="nav-label">{item.label}</span>
                {item.badge && <span className="nav-badge">{item.badge}</span>}
              </Link>
            );
          })}
        </nav>
        <div className="app-sidebar-footer">
          <div className="user-avatar">RA</div>
          <div className="user-info">
            <strong>Rafael Auditor</strong>
            <span>Analista contábil</span>
          </div>
        </div>
      </aside>

      <div className="app-main">
        <Routes>
          <Route
            element={<DeclaredLayerRoute />}
            path="/analises/:analysisId/exercicios/:year/declarada"
          />
          <Route
            element={<AuditoriaRoute />}
            path="/analises/:analysisId/exercicios/:year/auditoria"
          />
          <Route
            element={<CapagAssessmentRoute />}
            path="/analises/:analysisId/exercicios/:year/resultado"
          />
          <Route
            element={<PlraRoute />}
            path="/analises/:analysisId/exercicios/:year/plra"
          />
          <Route
            element={<EvidenceRoute />}
            path="/analises/:analysisId/exercicios/:year/evidencias"
          />
          <Route
            element={<DfcRoute />}
            path="/analises/:analysisId/exercicios/:year/dfc"
          />
          <Route
            element={<RoaRoute />}
            path="/analises/:analysisId/exercicios/:year/roa"
          />
          <Route element={<ImportEcdPage />} path="/importar-ecd" />
          <Route
            element={<Navigate replace to="/importar-ecd" />}
            path="*"
          />
        </Routes>
      </div>
    </div>
  );
}

export function App() {
  const [queryClient] = useState(createQueryClient);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <GovernedShell />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
