import React from "react";

/**
 * SegmentedControl — compact toggle between a few mutually-exclusive views.
 * Used to switch the balance sheet between "two columns" and "ledger".
 * Controlled: pass `value` and `onChange(id)`.
 */
export function SegmentedControl({ options = [], value, onChange, size = "sm" }) {
  const pad = size === "sm" ? "5px 11px" : "7px 14px";
  const fs = size === "sm" ? "var(--text-sm)" : "var(--text-base)";
  return (
    <div
      role="tablist"
      style={{
        display: "inline-flex",
        gap: 2,
        padding: 3,
        background: "var(--surface-muted)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
      }}
    >
      {options.map((opt) => {
        const selected = opt.id === value;
        return (
          <button
            key={opt.id}
            role="tab"
            aria-selected={selected}
            onClick={() => onChange && onChange(opt.id)}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              padding: pad,
              border: "none",
              borderRadius: "var(--radius-md)",
              fontSize: fs,
              fontWeight: "var(--weight-medium)",
              fontFamily: "inherit",
              cursor: "pointer",
              whiteSpace: "nowrap",
              backgroundColor: selected ? "var(--surface-card)" : "transparent",
              color: selected ? "var(--text-primary)" : "var(--text-secondary)",
              boxShadow: selected ? "var(--shadow-xs)" : "none",
              transition: "color 100ms ease",
            }}
          >
            {opt.icon}
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
