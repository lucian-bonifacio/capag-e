// CAPAG Analytics — Dashboard screen (UI kit)
// Composes the design-system primitives into the real product view.
const DS = window.CAPAGAnalyticsDesignSystem_0c00db;
const { Sidebar, Topbar, StatCard, Card, CardHeader, BalanceGroup, AccountRow, BalanceLedger,
        SegmentedControl, Dialog, DataTable, Button, Input, Badge } = DS;

// ---- icons (inline, Lucide-style stroke) ----
const Ico = (paths) => (props) => (
  <svg width={props && props.size || 18} height={props && props.size || 18} viewBox="0 0 24 24"
       fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">{paths}</svg>
);
const IconDash = Ico(<><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></>);
const IconSheet = Ico(<><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 3v18M3 9h18"/></>);
const IconGauge = Ico(<><path d="m12 14 4-5"/><path d="M3.5 18a9 9 0 1 1 17 0"/></>);
const IconAudit = Ico(<><circle cx="11" cy="11" r="7"/><path d="m20 20-3.2-3.2"/></>);
const IconUpload = Ico(<><path d="M12 15V3m-5 5 5-5 5 5"/><path d="M5 21h14"/></>);
const IconSearch = Ico(<><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></>);
const IconColumns = Ico(<><rect x="3" y="3" width="7" height="18" rx="1"/><rect x="14" y="3" width="7" height="18" rx="1"/></>);
const IconRows = Ico(<><path d="M3 6h18M3 12h18M3 18h18"/></>);

function GroupColumn({ title, eyebrow, groups, total, state, onToggle, onAudit, onAuditGroup }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <div>
          <div className="eyebrow">{eyebrow}</div>
          <h2 style={{ margin: "2px 0 0", fontSize: "var(--text-lg)", fontWeight: 600, color: "var(--text-primary)" }}>{title}</h2>
        </div>
        <div className="tnum" style={{ fontSize: "var(--text-md)", fontWeight: 700, color: "var(--text-primary)" }}>{total}</div>
      </div>
      {groups.map((g) => (
        <BalanceGroup key={g.id} name={g.name} count={g.contas.length} total={g.total} percent={g.percent}
                      defaultOpen={g.id === "ac" || g.id === "pc"} onAuditGroup={() => onAuditGroup(g)}>
          {g.contas.map((c) => (
            <AccountRow key={c.id} name={c.name} code={c.code} value={c.value}
                        included={state[c.id]} onToggle={(v) => onToggle(c.id, v)}
                        onAudit={() => onAudit(c, g)} />
          ))}
        </BalanceGroup>
      ))}
    </div>
  );
}

function Dashboard() {
  const data = window.CAPAG_DATA;
  const [active, setActive] = React.useState("balanco");
  const allGroups = [...data.ativos, ...data.passivos];

  // include/exclude state, keyed by account id
  const initial = {};
  allGroups.forEach((g) => g.contas.forEach((c) => (initial[c.id] = c.included)));
  const [incl, setIncl] = React.useState(initial);
  const toggle = (id, v) => setIncl((p) => ({ ...p, [id]: v }));

  const [audit, setAudit] = React.useState(null); // { title, subtitle }
  const [view, setView] = React.useState("columns"); // "columns" | "ledger"

  const openAccount = (c, g) => setAudit({ title: `Auditoria — ${c.name}`, subtitle: `${c.code} · ${g.name}` });
  const openGroup = (g) => setAudit({ title: `Auditoria — ${g.name}`, subtitle: `${g.contas.length} contas · ${g.total}` });

  const excluded = Object.values(incl).filter((v) => !v).length;

  const auditCols = [
    { key: "data", header: "Data", width: 96 },
    { key: "hist", header: "Histórico", wrap: true },
    { key: "doc", header: "Documento", width: 110 },
    { key: "deb", header: "Débito", align: "right", numeric: true, width: 120 },
    { key: "cred", header: "Crédito", align: "right", numeric: true, width: 120 },
  ];

  return (
    <div style={{ display: "flex", height: "100vh", background: "var(--bg-app)" }}>
      <Sidebar
        activeId={active}
        onSelect={setActive}
        items={[
          { id: "dashboard", label: "Dashboard", icon: <IconDash /> },
          { id: "balanco", label: "Balanço Patrimonial", icon: <IconSheet /> },
          { id: "indicadores", label: "Indicadores CAPAG", icon: <IconGauge /> },
          { id: "auditoria", label: "Auditoria", icon: <IconAudit />, badge: excluded || undefined },
          { id: "importar", label: "Importar ECD", icon: <IconUpload /> },
        ]}
        footer={
          <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "6px 6px" }}>
            <span style={{ width: 30, height: 30, borderRadius: "var(--radius-full)", background: "var(--slate-200)",
                           display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 600, color: "var(--slate-600)" }}>RA</span>
            <div style={{ lineHeight: 1.2 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: "var(--text-primary)" }}>Rafael Auditor</div>
              <div style={{ fontSize: 11, color: "var(--text-secondary)" }}>Analista contábil</div>
            </div>
          </div>
        }
      />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        <Topbar
          title="Balanço Patrimonial"
          subtitle={`${data.entidade} · Exercício ${data.exercicio}`}
          actions={
            <>
              <Input iconLeft={<IconSearch size={16} />} placeholder="Buscar conta ou grupo…" size="sm" wrapperStyle={{ width: 240 }} />
              <Button size="sm" variant="secondary" iconLeft={<IconAudit size={15} />} onClick={() => setAudit({ title: "Auditoria geral", subtitle: "Razão analítico consolidado" })}>Auditoria</Button>
              <Button size="sm" iconLeft={<IconUpload size={15} />}>Importar ECD</Button>
            </>
          }
        />

        <main style={{ flex: 1, overflowY: "auto", padding: "var(--space-8)" }}>
          <div style={{ maxWidth: 920, margin: "0 auto" }}>
            {/* Indicators — calculated, not raw balance values */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
              <div className="eyebrow">Indicadores calculados</div>
              {excluded > 0 && <Badge variant="warning">{excluded} conta{excluded > 1 ? "s" : ""} excluída{excluded > 1 ? "s" : ""} dos cálculos</Badge>}
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(195px, 1fr))", gap: 16, marginBottom: "var(--space-8)" }}>
              {data.indicadores.map((k) => (
                <StatCard key={k.label} label={k.label} value={k.value} tone={k.tone} hint={k.hint} icon={<IconGauge size={16} />} />
              ))}
            </div>

            {/* Balance sheet — switchable view */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
              <div className="eyebrow">Balanço Patrimonial</div>
              <SegmentedControl
                value={view}
                onChange={setView}
                options={[
                  { id: "columns", label: "Duas colunas", icon: <IconColumns size={15} /> },
                  { id: "ledger", label: "Livro-razão", icon: <IconRows size={15} /> },
                ]}
              />
            </div>

            {view === "columns" ? (
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-5)", alignItems: "start" }}>
                <GroupColumn eyebrow="Aplicações" title="Ativos" groups={data.ativos} total="R$ 48.200.000,00"
                             state={incl} onToggle={toggle} onAudit={openAccount} onAuditGroup={openGroup} />
                <GroupColumn eyebrow="Origens" title="Passivos e PL" groups={data.passivos} total="R$ 48.200.000,00"
                             state={incl} onToggle={toggle} onAudit={openAccount} onAuditGroup={openGroup} />
              </div>
            ) : (
              <div>
                <BalanceLedger eyebrow="Aplicações" title="Ativos" total="R$ 48.200.000,00" groups={data.ativos}
                               state={incl} onToggle={toggle} onAudit={openAccount} onAuditGroup={openGroup} defaultOpenIds={["ac"]} />
                <BalanceLedger eyebrow="Origens" title="Passivos e Patrimônio Líquido" total="R$ 48.200.000,00" groups={data.passivos}
                               state={incl} onToggle={toggle} onAudit={openAccount} onAuditGroup={openGroup} defaultOpenIds={["pc"]} />
              </div>
            )}
          </div>
        </main>
      </div>

      <Dialog open={!!audit} onClose={() => setAudit(null)} width={760}
              title={audit && audit.title} subtitle={audit && audit.subtitle}
              footer={<><Button variant="secondary" onClick={() => setAudit(null)}>Fechar</Button><Button>Exportar CSV</Button></>}>
        <div style={{ display: "flex", gap: 16, marginBottom: 16 }}>
          <MiniStat label="Lançamentos" value="6" />
          <MiniStat label="Total débitos" value="R$ 1.192.000,00" />
          <MiniStat label="Total créditos" value="R$ 2.388.600,00" />
        </div>
        <DataTable columns={auditCols} rows={window.CAPAG_DATA.lancamentos} />
      </Dialog>
    </div>
  );
}

function MiniStat({ label, value }) {
  return (
    <div style={{ flex: 1, border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: "10px 14px", background: "var(--surface-inset)" }}>
      <div style={{ fontSize: 11, fontWeight: 600, letterSpacing: ".04em", textTransform: "uppercase", color: "var(--text-secondary)" }}>{label}</div>
      <div className="tnum" style={{ fontSize: 16, fontWeight: 600, color: "var(--text-primary)", marginTop: 3 }}>{value}</div>
    </div>
  );
}

window.Dashboard = Dashboard;
