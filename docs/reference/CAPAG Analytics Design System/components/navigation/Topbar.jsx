import React from "react";

/**
 * Topbar — simple top bar for the admin shell.
 * Title on the left, optional actions on the right.
 */
export function Topbar({ title, subtitle, breadcrumb = null, actions = null, style = {} }) {
  return (
    <header
      style={{
        height: "var(--topbar-height)",
        flex: "none",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "var(--space-4)",
        padding: "0 var(--space-8)",
        background: "var(--surface-card)",
        borderBottom: "1px solid var(--border)",
        ...style,
      }}
    >
      <div style={{ minWidth: 0 }}>
        {breadcrumb && (
          <div style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", marginBottom: 2 }}>
            {breadcrumb}
          </div>
        )}
        <div style={{ display: "flex", alignItems: "baseline", gap: 10, minWidth: 0 }}>
          <h1
            style={{
              margin: 0,
              fontSize: "var(--text-xl)",
              fontWeight: "var(--weight-semibold)",
              color: "var(--text-primary)",
              letterSpacing: "var(--tracking-tight)",
              whiteSpace: "nowrap",
            }}
          >
            {title}
          </h1>
          {subtitle && (
            <span style={{ fontSize: "var(--text-sm)", color: "var(--text-secondary)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", minWidth: 0 }}>{subtitle}</span>
          )}
        </div>
      </div>
      {actions && (
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", flex: "none" }}>
          {actions}
        </div>
      )}
    </header>
  );
}
