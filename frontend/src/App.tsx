import { Activity, ClipboardCheck, LayoutDashboard, Scale, Upload, Search, LogOut } from "lucide-react";
import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { BrowserRouter, Link, Navigate, Route, Routes, useLocation, useParams } from "react-router-dom";

import {
  fetchDeclaredAccounts,
  fetchDeclaredBalanceAccounts,
  fetchDeclaredSummary,
} from "./api/declared";
import { BalanceDashboardPage } from "./routes/BalanceDashboardPage";
import { DeclaredLayerPage } from "./routes/DeclaredLayerPage";
import { ImportEcdPage } from "./routes/ImportEcdPage";
import "./App.css";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/analises/:analysisId/exercicios/:year/declarada", match: "/dashboard" },
  { label: "Balanço Patrimonial", icon: Scale, path: "/analises/:analysisId/exercicios/:year/declarada", match: "/analises/" },
  { label: "Indicadores CAPAG", icon: Activity, path: "#", match: "/indicadores" },
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

function GovernedShell() {
  const location = useLocation();

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
            // Handle parameterized paths roughly for demonstration, in a real app we'd inject params
            const path = item.path.includes(":analysisId") 
              ? item.path.replace(":analysisId", "bc7478b47f261603").replace(":year", "2024") 
              : item.path;

            return (
              <Link
                className="app-nav-item"
                data-active={location.pathname.startsWith(item.match)}
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
