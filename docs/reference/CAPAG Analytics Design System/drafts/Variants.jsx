// CAPAG Analytics — RASCUNHO: variações de layout do Balanço Patrimonial
// V1 (duas colunas, refinada/consistente) · V2 (livro-razão) · V3 = V2 em dark mode azul.
const DSV = window.CAPAGAnalyticsDesignSystem_0c00db;
const { Chevron } = DSV;

// ---------- helpers ----------
const parseBRL = (s) => {
  if (typeof s !== "string") return 0;
  const n = s.replace(/[^0-9,.-]/g, "").replace(/\./g, "").replace(",", ".");
  return parseFloat(n) || 0;
};
const pct = (part, whole) => (whole ? (part / whole) * 100 : 0);
const fmtPct = (n) => n.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + "%";

// ---------- ícone de auditoria (prancheta com check — não mais a lupa) ----------
const AuditGlyph = ({ size = 15 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor"
       strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect width="8" height="4" x="8" y="2" rx="1" />
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
    <path d="m9 14 2 2 4-4" />
  </svg>
);

// botão de auditoria discreto (ghost — moldura só no hover)
function AuditBtn({ onClick, title = "Ver auditoria" }) {
  const [h, setH] = React.useState(false);
  return (
    <button onClick={onClick} title={title} aria-label={title}
      onMouseEnter={() => setH(true)} onMouseLeave={() => setH(false)}
      style={{
        width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center",
        border: "1px solid " + (h ? "var(--blue-100)" : "transparent"),
        background: h ? "var(--primary-soft)" : "transparent",
        color: h ? "var(--primary-text)" : "var(--text-muted)",
        borderRadius: "var(--radius-md)", cursor: "pointer", flex: "none",
        transition: "all 100ms ease",
      }}>
      <AuditGlyph />
    </button>
  );
}

// switch menor e menos chamativo (azul suave)
function MiniSwitch({ checked, onChange }) {
  const w = 32, h = 18, knob = 13, pad = 2.5;
  return (
    <button role="switch" aria-checked={checked} onClick={() => onChange && onChange(!checked)}
      style={{
        position: "relative", width: w, height: h, flex: "none", padding: 0, border: "none",
        borderRadius: 999, cursor: "pointer",
        background: checked ? "rgba(59,130,246,0.45)" : "var(--slate-300)",
        transition: "background 140ms ease",
      }}>
      <span style={{
        position: "absolute", top: pad, left: checked ? w - knob - pad : pad, width: knob, height: knob,
        borderRadius: 999, background: "#FFFFFF", boxShadow: "0 1px 2px rgba(15,23,42,.18)",
        transition: "left 140ms ease",
      }} />
    </button>
  );
}

// macrogrupo em caixa alta (compartilhado pelas versões)
const macroNameStyle = {
  fontSize: 12, fontWeight: 700, letterSpacing: "0.05em", textTransform: "uppercase",
  color: "var(--text-primary)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
};
// nome de conta — recuado, fonte menor, discreto
const acctNameStyle = (on) => ({
  fontSize: "var(--text-sm)", color: "var(--slate-700)",
  whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
  textDecoration: on ? "none" : "line-through",
});
// valor — MESMA fonte/peso/cor do nome da conta
const acctValueStyle = (on) => ({
  fontSize: "var(--text-sm)", fontWeight: 400, color: "var(--slate-700)",
  fontVariantNumeric: "tabular-nums", textAlign: "right",
  textDecoration: on ? "none" : "line-through",
});

// ===================================================================
// VARIANTE 1 — DUAS COLUNAS (refinada, consistente com a V2)
// ===================================================================
function TwoColGroup({ g, incl, toggle, onAudit, onAuditGroup, defaultOpen }) {
  const [open, setOpen] = React.useState(defaultOpen);
  const [hHead, setHHead] = React.useState(false);
  return (
    <div style={{ background: "var(--surface-card)", border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-xs)", overflow: "hidden" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "11px 14px",
        background: hHead ? "var(--surface-inset)" : "var(--surface-muted)", transition: "background 100ms ease" }}
        onMouseEnter={() => setHHead(true)} onMouseLeave={() => setHHead(false)}>
        <button onClick={() => setOpen((v) => !v)}
          style={{ display: "flex", alignItems: "center", gap: 8, flex: 1, minWidth: 0, border: "none",
            background: "transparent", cursor: "pointer", padding: 0, textAlign: "left" }}>
          <Chevron open={open} />
          <span style={{ flex: 1, minWidth: 0 }}>
            <span style={{ display: "block", fontSize: 12, fontWeight: 700, letterSpacing: "0.05em",
              textTransform: "uppercase", color: "var(--text-primary)", lineHeight: 1.25 }}>{g.name}</span>
            <span style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>{g.contas.length} contas</span>
          </span>
        </button>
        <span className="tnum" style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", flex: "none" }}>{g.percent}</span>
        <span className="tnum" style={{ fontSize: "var(--text-sm)", fontWeight: 700, color: "var(--text-primary)", whiteSpace: "nowrap", flex: "none" }}>{g.total}</span>
        <AuditBtn onClick={() => onAuditGroup(g)} title={"Auditar grupo " + g.name} />
      </div>
      {open && g.contas.map((c) => {
        const on = incl[c.id];
        return (
          <div key={c.id} style={{ display: "flex", alignItems: "center", gap: 10,
            padding: "8px 14px 8px 34px", borderTop: "1px solid var(--border)", opacity: on ? 1 : 0.55 }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: "var(--text-sm)", color: "var(--slate-700)", lineHeight: 1.3,
                textDecoration: on ? "none" : "line-through" }}>{c.name}</div>
              <div className="tnum" style={{ fontSize: 11, color: "var(--text-muted)" }}>{c.code}</div>
            </div>
            <div className="tnum" style={{ ...acctValueStyle(on), whiteSpace: "nowrap", minWidth: 96, flex: "none" }}>{c.value}</div>
            <MiniSwitch checked={on} onChange={(val) => toggle(c.id, val)} />
            <AuditBtn onClick={() => onAudit(c, g)} />
          </div>
        );
      })}
    </div>
  );
}

function VariantCurrent({ data, incl, toggle, onAudit, onAuditGroup }) {
  const Col = ({ eyebrow, title, groups, total }) => (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <div>
          <div className="eyebrow">{eyebrow}</div>
          <h2 style={{ margin: "2px 0 0", fontSize: "var(--text-lg)", fontWeight: 600, color: "var(--text-primary)" }}>{title}</h2>
        </div>
        <div className="tnum" style={{ fontSize: "var(--text-sm)", fontWeight: 700, color: "var(--text-primary)" }}>{total}</div>
      </div>
      {groups.map((g) => (
        <TwoColGroup key={g.id} g={g} incl={incl} toggle={toggle} onAudit={onAudit} onAuditGroup={onAuditGroup}
          defaultOpen={g.id === "ac" || g.id === "pc"} />
      ))}
    </div>
  );
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, alignItems: "start" }}>
      <Col eyebrow="Aplicações" title="Ativos" groups={data.ativos} total="R$ 48.200.000,00" />
      <Col eyebrow="Origens" title="Passivos e PL" groups={data.passivos} total="R$ 48.200.000,00" />
    </div>
  );
}

// ===================================================================
// VARIANTE 2 — LIVRO-RAZÃO ALINHADO (coluna única)
// ===================================================================
const GRID = "minmax(0,1fr) 72px 156px 46px 30px";

function LedgerHeader() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: GRID, gap: 12, alignItems: "center",
      padding: "8px 18px", borderBottom: "1px solid var(--border)" }}>
      <div className="eyebrow" style={{ fontSize: 10 }}>Conta</div>
      <div className="eyebrow" style={{ fontSize: 10, textAlign: "right" }}>%</div>
      <div className="eyebrow" style={{ fontSize: 10, textAlign: "right" }}>Valor</div>
      <div className="eyebrow" style={{ fontSize: 10, textAlign: "center" }}>Incluir</div>
      <div></div>
    </div>
  );
}

function LedgerGroup({ g, incl, toggle, onAudit, onAuditGroup, defaultOpen }) {
  const [open, setOpen] = React.useState(defaultOpen);
  const [hHead, setHHead] = React.useState(false);
  const groupTotal = parseBRL(g.total);
  return (
    <div>
      {/* MACROGRUPO */}
      <div style={{ display: "grid", gridTemplateColumns: GRID, gap: 12, alignItems: "center",
        padding: "13px 18px", background: hHead ? "var(--surface-inset)" : "var(--surface-muted)",
        borderTop: "1px solid var(--border)", transition: "background 100ms ease" }}
        onMouseEnter={() => setHHead(true)} onMouseLeave={() => setHHead(false)}>
        <button onClick={() => setOpen((v) => !v)}
          style={{ display: "flex", alignItems: "center", gap: 10, minWidth: 0, border: "none",
            background: "transparent", cursor: "pointer", padding: 0, textAlign: "left" }}>
          <Chevron open={open} />
          <span style={macroNameStyle}>{g.name}</span>
          <span style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", flex: "none" }}>· {g.contas.length} contas</span>
        </button>
        <div className="tnum" style={{ textAlign: "right", fontSize: "var(--text-sm)", color: "var(--text-secondary)" }}>{g.percent}</div>
        <div className="tnum" style={{ textAlign: "right", fontSize: "var(--text-md)", fontWeight: 700, color: "var(--text-primary)" }}>{g.total}</div>
        <div></div>
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <AuditBtn onClick={() => onAuditGroup(g)} title={"Auditar grupo " + g.name} />
        </div>
      </div>
      {/* SUBGRUPOS / CONTAS */}
      {open && g.contas.map((c) => {
        const v = parseBRL(c.value);
        const on = incl[c.id];
        return (
          <div key={c.id} style={{ display: "grid", gridTemplateColumns: GRID, gap: 12, alignItems: "center",
            padding: "8px 18px 8px 52px", borderTop: "1px solid var(--border)", opacity: on ? 1 : 0.55 }}>
            <div style={{ minWidth: 0 }}>
              <div style={acctNameStyle(on)}>{c.name}</div>
              <div className="tnum" style={{ fontSize: 11, color: "var(--text-muted)" }}>{c.code}</div>
            </div>
            <div className="tnum" style={{ textAlign: "right", fontSize: 11, color: "var(--text-muted)" }}>{fmtPct(pct(v, groupTotal))}</div>
            <div className="tnum" style={acctValueStyle(on)}>{c.value}</div>
            <div style={{ display: "flex", justifyContent: "center" }}>
              <MiniSwitch checked={on} onChange={(val) => toggle(c.id, val)} />
            </div>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <AuditBtn onClick={() => onAudit(c, g)} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

function LedgerSection({ eyebrow, title, groups, total, incl, toggle, onAudit, onAuditGroup }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 8 }}>
        <div className="eyebrow">{eyebrow} · {title}</div>
        <div className="tnum" style={{ fontSize: "var(--text-md)", fontWeight: 700, color: "var(--text-primary)" }}>{total}</div>
      </div>
      <LedgerHeader />
      <div style={{ border: "1px solid var(--border)", borderTop: "none",
        borderRadius: "0 0 var(--radius-lg) var(--radius-lg)", overflow: "hidden", background: "var(--surface-card)" }}>
        {groups.map((g) => (
          <LedgerGroup key={g.id} g={g} incl={incl} toggle={toggle} onAudit={onAudit} onAuditGroup={onAuditGroup}
            defaultOpen={g.id === "ac" || g.id === "pc"} />
        ))}
      </div>
    </div>
  );
}

function VariantLedger({ data, incl, toggle, onAudit, onAuditGroup }) {
  return (
    <div>
      <LedgerSection eyebrow="Aplicações" title="Ativos" groups={data.ativos} total="R$ 48.200.000,00"
        incl={incl} toggle={toggle} onAudit={onAudit} onAuditGroup={onAuditGroup} />
      <LedgerSection eyebrow="Origens" title="Passivos e Patrimônio Líquido" groups={data.passivos} total="R$ 48.200.000,00"
        incl={incl} toggle={toggle} onAudit={onAudit} onAuditGroup={onAuditGroup} />
    </div>
  );
}

window.CAPAGVariants = { VariantCurrent, VariantLedger };
