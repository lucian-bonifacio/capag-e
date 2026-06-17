import React from "react";
import { Switch } from "../core/Switch.jsx";

/**
 * AccountRow — a single contábil account inside a balance group.
 * Shows name + code, value, an include/exclude Switch and an audit action.
 * Recuada (subgrupo) sob o macrogrupo. Quando excluída, a linha esmaece e
 * o nome/valor ganham tachado para reforçar que está fora dos cálculos.
 */
export function AccountRow({
  name,
  code,
  value,
  included = true,
  onToggle,
  onAudit,
}) {
  const [hover, setHover] = React.useState(false);
  const strike = { textDecoration: included ? "none" : "line-through" };
  return (
    <div
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        alignItems: "center",
        gap: "var(--space-3)",
        padding: "8px 14px 8px 46px",
        background: hover ? "var(--surface-inset)" : "transparent",
        borderTop: "1px solid var(--border)",
        transition: "background-color 100ms ease",
        opacity: included ? 1 : 0.55,
      }}
    >
      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          style={{
            fontSize: "var(--text-sm)",
            color: "var(--slate-700)",
            lineHeight: 1.3,
            ...strike,
          }}
        >
          {name}
        </div>
        {code && (
          <div className="tnum" style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 1 }}>
            {code}
          </div>
        )}
      </div>

      <div
        className="tnum"
        style={{
          fontSize: "var(--text-sm)",
          fontWeight: "var(--weight-normal)",
          color: "var(--slate-700)",
          fontVariantNumeric: "tabular-nums",
          textAlign: "right",
          whiteSpace: "nowrap",
          minWidth: 110,
          ...strike,
        }}
      >
        {value}
      </div>

      <Switch
        size="sm"
        tone="soft"
        checked={included}
        onChange={onToggle}
        aria-label={`${included ? "Excluir" : "Incluir"} ${typeof name === "string" ? name : "conta"} dos cálculos`}
      />

      <AuditButton onClick={onAudit} label={`Auditar conta ${typeof name === "string" ? name : ""}`} />
    </div>
  );
}

/** Ícone de auditoria (prancheta com check) — substitui a antiga lupa. */
export function AuditButton({ onClick, label = "Ver auditoria", title = "Ver auditoria" }) {
  const [h, setH] = React.useState(false);
  return (
    <button
      onClick={onClick}
      title={title}
      aria-label={label}
      onMouseEnter={() => setH(true)}
      onMouseLeave={() => setH(false)}
      style={{
        width: 28,
        height: 28,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        border: "1px solid " + (h ? "var(--blue-100)" : "transparent"),
        background: h ? "var(--primary-soft)" : "transparent",
        color: h ? "var(--primary-text)" : "var(--text-muted)",
        borderRadius: "var(--radius-md)",
        cursor: "pointer",
        flex: "none",
        transition: "all 100ms ease",
      }}
    >
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect width="8" height="4" x="8" y="2" rx="1" />
        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
        <path d="m9 14 2 2 4-4" />
      </svg>
    </button>
  );
}
