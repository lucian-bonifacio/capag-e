import React from "react";
import { Chevron } from "../composite/Accordion.jsx";
import { AuditButton } from "./AccountRow.jsx";

/**
 * BalanceGroup — collapsible balance-sheet group.
 * Header shows the group name, account count, total value and percentage.
 * Children are AccountRow elements. A trailing "audit group" action is optional.
 */
export function BalanceGroup({
  name,
  count,
  total,
  percent,
  defaultOpen = true,
  open,
  onToggle,
  onAuditGroup,
  children,
}) {
  const [internal, setInternal] = React.useState(defaultOpen);
  const isOpen = open != null ? open : internal;
  const toggle = () => (onToggle ? onToggle(!isOpen) : setInternal((v) => !v));
  const [hover, setHover] = React.useState(false);

  return (
    <div
      style={{
        background: "var(--surface-card)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
        boxShadow: "var(--shadow-xs)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "var(--space-3)",
          background: hover ? "var(--surface-inset)" : "var(--surface-muted)",
          transition: "background-color 100ms ease",
        }}
      >
        <button
          onClick={toggle}
          onMouseEnter={() => setHover(true)}
          onMouseLeave={() => setHover(false)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "var(--space-3)",
            flex: 1,
            minWidth: 0,
            padding: "11px 14px",
            border: "none",
            background: "transparent",
            cursor: "pointer",
            textAlign: "left",
          }}
        >
          <Chevron open={isOpen} />
          <span style={{ flex: 1, minWidth: 0 }}>
            <span
              style={{
                display: "block",
                fontSize: 12,
                fontWeight: "var(--weight-bold)",
                letterSpacing: "0.05em",
                textTransform: "uppercase",
                color: "var(--text-primary)",
                lineHeight: 1.25,
              }}
            >
              {name}
            </span>
            <span style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              {count} {count === 1 ? "conta" : "contas"}
            </span>
          </span>

          {percent != null && (
            <span
              className="tnum"
              style={{
                fontSize: "var(--text-sm)",
                color: "var(--text-secondary)",
                fontVariantNumeric: "tabular-nums",
                minWidth: 46,
                textAlign: "right",
              }}
            >
              {percent}
            </span>
          )}
          <span
            className="tnum"
            style={{
              fontSize: "var(--text-md)",
              fontWeight: "var(--weight-semibold)",
              color: "var(--text-primary)",
              fontVariantNumeric: "tabular-nums",
              minWidth: 130,
              textAlign: "right",
            }}
          >
            {total}
          </span>
        </button>

        {onAuditGroup && (
          <span style={{ marginRight: "var(--space-4)", display: "flex" }}>
            <AuditButton
              onClick={onAuditGroup}
              title="Ver auditoria do grupo"
              label={`Auditar grupo ${typeof name === "string" ? name : ""}`}
            />
          </span>
        )}
      </div>

      {isOpen && <div>{children}</div>}
    </div>
  );
}
