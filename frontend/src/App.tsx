import { Activity, ClipboardList, FileInput, LayoutDashboard, Scale } from "lucide-react";
import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { BrowserRouter, Navigate, Route, Routes, useParams } from "react-router-dom";

import { fetchDeclaredAccounts, fetchDeclaredSummary } from "./api/declared";
import { DeclaredLayerPage } from "./routes/DeclaredLayerPage";
import "./App.css";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, active: false },
  { label: "Camada Declarada", icon: ClipboardList, active: true },
  { label: "Balanco Patrimonial", icon: Scale, active: false },
  { label: "Auditoria", icon: Activity, active: false },
  { label: "Importar ECD", icon: FileInput, active: false },
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
  return (
    <div className="app-shell">
      <aside className="app-sidebar" aria-label="Navegacao principal">
        <div className="app-brand">CAPAG Analytics</div>
        <nav className="app-nav">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <div
                className="app-nav-item"
                data-active={item.active}
                key={item.label}
              >
                <Icon aria-hidden="true" size={18} strokeWidth={1.8} />
                <span>{item.label}</span>
              </div>
            );
          })}
        </nav>
      </aside>

      <div className="app-main">
        <Routes>
          <Route
            element={<DeclaredLayerRoute />}
            path="/analises/:analysisId/exercicios/:year/declarada"
          />
          <Route
            element={<Navigate replace to="/analises/1/exercicios/2024/declarada" />}
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
