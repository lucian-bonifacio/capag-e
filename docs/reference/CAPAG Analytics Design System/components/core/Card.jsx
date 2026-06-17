import React from "react";

/**
 * Card — white surface container with soft border.
 * Compose with CardHeader / CardBody, or just pass children.
 */
export function Card({ children, padding = "var(--space-6)", style = {}, ...rest }) {
  return (
    <div
      style={{
        background: "var(--surface-card)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
        boxShadow: "var(--shadow-xs)",
        padding,
        ...style,
      }}
      {...rest}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, action, style = {} }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "space-between",
        gap: "var(--space-4)",
        marginBottom: "var(--space-4)",
        ...style,
      }}
    >
      <div>
        {title && (
          <div
            style={{
              fontSize: "var(--text-lg)",
              fontWeight: "var(--weight-semibold)",
              color: "var(--text-primary)",
              letterSpacing: "var(--tracking-tight)",
            }}
          >
            {title}
          </div>
        )}
        {subtitle && (
          <div style={{ fontSize: "var(--text-sm)", color: "var(--text-secondary)", marginTop: 2 }}>
            {subtitle}
          </div>
        )}
      </div>
      {action}
    </div>
  );
}

/**
 * StatCard — KPI / indicator tile for the dashboard top row.
 * Shows a label, a large value, and optional delta/hint.
 */
export function StatCard({ label, value, hint, tone = "neutral", icon = null, style = {} }) {
  const tones = {
    neutral: "var(--text-primary)",
    primary: "var(--primary)",
    success: "var(--success)",
    warning: "var(--warning-text)",
    danger: "var(--danger)",
  };
  return (
    <div
      style={{
        background: "var(--surface-card)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
        boxShadow: "var(--shadow-xs)",
        padding: "var(--space-5)",
        ...style,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "var(--space-3)",
        }}
      >
        <span
          style={{
            fontSize: "var(--text-xs)",
            fontWeight: "var(--weight-semibold)",
            letterSpacing: "var(--tracking-wide)",
            textTransform: "uppercase",
            color: "var(--text-secondary)",
          }}
        >
          {label}
        </span>
        {icon && <span style={{ color: "var(--text-muted)", display: "flex" }}>{icon}</span>}
      </div>
      <div
        className="tnum"
        style={{
          marginTop: "var(--space-3)",
          fontSize: "var(--text-2xl)",
          fontWeight: "var(--weight-semibold)",
          lineHeight: 1.1,
          color: tones[tone] || tones.neutral,
          letterSpacing: "var(--tracking-tight)",
        }}
      >
        {value}
      </div>
      {hint && (
        <div style={{ marginTop: 6, fontSize: "var(--text-sm)", color: "var(--text-secondary)" }}>
          {hint}
        </div>
      )}
    </div>
  );
}
