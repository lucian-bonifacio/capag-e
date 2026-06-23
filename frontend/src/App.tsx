import { Activity, FileInput, LayoutDashboard, Scale } from "lucide-react";

import "./App.css";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, active: true },
  { label: "Balanco Patrimonial", icon: Scale, active: false },
  { label: "Auditoria", icon: Activity, active: false },
  { label: "Importar ECD", icon: FileInput, active: false },
];

export function App() {
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
        <header className="app-topbar">
          <div>
            <h1 className="app-title">Fundacao</h1>
            <p className="app-subtitle">Shell administrativo inicial</p>
          </div>
          <span className="app-status">Sem dados importados</span>
        </header>

        <main className="app-content">
          <section className="app-panel" aria-labelledby="shell-title">
            <p className="eyebrow">Bootstrap</p>
            <h2 id="shell-title">Frontend pronto para proximas telas</h2>
            <p>
              Estrutura visual minima carregada com tokens governados, sem API,
              dados de dominio ou regra prudencial.
            </p>
          </section>
        </main>
      </div>
    </div>
  );
}
