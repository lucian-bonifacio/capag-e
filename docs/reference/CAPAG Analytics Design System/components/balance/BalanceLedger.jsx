import React from "react";
import { Chevron } from "../composite/Accordion.jsx";
import { Switch } from "../core/Switch.jsx";
import { AuditButton } from "./AccountRow.jsx";

/**
 * BalanceLedger — single-column "livro-razão" view of a balance section.
 * Columns align across all groups (Conta · % · Valor · Incluir · Auditar).
 * Macrogroups render in uppercase; accounts are indented subgroups, with
 * strikethrough + dimming when excluded. Pairs with SegmentedControl to
 * offer an alternative to the two-column BalanceGroup view.
 */

const GRID = "minmax(0,1fr) 72px 156px 46px 30px";

function parseBRL(s) {
  if (typeof s !== "string") return 0;
  const n = s.replace(/[^0-9,.-]/g, "").replace(/\./g, "").replace(",", ".");
  return parseFloat(n) || 0;
}
function fmtPct(part, whole) {
  const v = whole ? (part / whole) * 100 : 0;
  return v.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + "%";
}

function LedgerHeaderRow() {
  const cell = { fontSize: 10, fontWeight: "var(--weight-semibold)", letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--text-muted)" };
  return (
    <div style={{ display: "grid", gridTemplateColumns: GRID, gap: 12, alignItems: "center", padding: "8px 18px", borderBottom: "1px solid var(--border)" }}>
      <div style={cell}>Conta</div>
      <div style={{ ...cell, textAlign: "right" }}>%</div>
      <div style={{ ...cell, textAlign: "right" }}>Valor</div>
      <div style={{ ...cell, textAlign: "center" }}>Incluir</div>
      <div></div>
    </div>
  );
}

function LedgerGroup({ group, state, onToggle, onAudit, onAuditGroup, defaultOpen }) {
  const [open, setOpen] = React.useState(defaultOpen);
  const [hover, setHover] = React.useState(false);
  const groupTotal = parseBRL(group.total);
  return (
    <div>
      <div
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        style={{ display: "grid", gridTemplateColumns: GRID, gap: 12, alignItems: "center", padding: "13px 18px",
          background: hover ? "var(--surface-inset)" : "var(--surface-muted)", borderTop: "1px solid var(--border)", transition: "background 100ms ease" }}
      >
        <button
          onClick={() => setOpen((v) => !v)}
          style={{ display: "flex", alignItems: "center", gap: 10, minWidth: 0, border: "none", background: "transparent", cursor: "pointer", padding: 0, textAlign: "left" }}
        >
          <Chevron open={open} />
          <span style={{ fontSize: 12, fontWeight: "var(--weight-bold)", letterSpacing: "0.05em", textTransform: "uppercase",
            color: "var(--text-primary)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{group.name}</span>
          <span style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", flex: "none" }}>· {group.contas.length} contas</span>
        </button>
        <div className="tnum" style={{ textAlign: "right", fontSize: "var(--text-sm)", color: "var(--text-secondary)", fontVariantNumeric: "tabular-nums" }}>{group.percent}</div>
        <div className="tnum" style={{ textAlign: "right", fontSize: "var(--text-md)", fontWeight: "var(--weight-bold)", color: "var(--text-primary)", fontVariantNumeric: "tabular-nums" }}>{group.total}</div>
        <div></div>
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <AuditButton onClick={() => onAuditGroup && onAuditGroup(group)} title="Ver auditoria do grupo" label={`Auditar grupo ${group.name}`} />
        </div>
      </div>

      {open && group.contas.map((c) => {
        const on = state ? state[c.id] : c.included;
        const strike = { textDecoration: on ? "none" : "line-through" };
        return (
          <div key={c.id} style={{ display: "grid", gridTemplateColumns: GRID, gap: 12, alignItems: "center", padding: "8px 18px 8px 52px", borderTop: "1px solid var(--border)", opacity: on ? 1 : 0.55 }}>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: "var(--text-sm)", color: "var(--slate-700)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", ...strike }}>{c.name}</div>
              <div className="tnum" style={{ fontSize: 11, color: "var(--text-muted)" }}>{c.code}</div>
            </div>
            <div className="tnum" style={{ textAlign: "right", fontSize: 11, color: "var(--text-muted)", fontVariantNumeric: "tabular-nums" }}>{fmtPct(parseBRL(c.value), groupTotal)}</div>
            <div className="tnum" style={{ textAlign: "right", fontSize: "var(--text-sm)", color: "var(--slate-700)", fontVariantNumeric: "tabular-nums", ...strike }}>{c.value}</div>
            <div style={{ display: "flex", justifyContent: "center" }}>
              <Switch size="sm" tone="soft" checked={on} onChange={(v) => onToggle && onToggle(c.id, v)} aria-label={`${on ? "Excluir" : "Incluir"} ${c.name}`} />
            </div>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <AuditButton onClick={() => onAudit && onAudit(c, group)} label={`Auditar conta ${c.name}`} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function BalanceLedger({ eyebrow, title, total, groups = [], state, onToggle, onAudit, onAuditGroup, defaultOpenIds = [] }) {
  return (
    <div style={{ marginBottom: "var(--space-6)" }}>
      {(eyebrow || title || total) && (
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 8 }}>
          <div className="eyebrow">{eyebrow}{eyebrow && title ? " · " : ""}{title}</div>
          {total && <div className="tnum" style={{ fontSize: "var(--text-md)", fontWeight: "var(--weight-bold)", color: "var(--text-primary)", fontVariantNumeric: "tabular-nums" }}>{total}</div>}
        </div>
      )}
      <LedgerHeaderRow />
      <div style={{ border: "1px solid var(--border)", borderTop: "none", borderRadius: "0 0 var(--radius-lg) var(--radius-lg)", overflow: "hidden", background: "var(--surface-card)" }}>
        {groups.map((g) => (
          <LedgerGroup key={g.id} group={g} state={state} onToggle={onToggle} onAudit={onAudit} onAuditGroup={onAuditGroup}
            defaultOpen={defaultOpenIds.includes(g.id)} />
        ))}
      </div>
    </div>
  );
}
