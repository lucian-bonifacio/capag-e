import React from "react";

/**
 * Badge — compact status / category label.
 * Variants: neutral | primary | success | warning | danger
 */
export function Badge({ variant = "neutral", children, style = {}, ...rest }) {
  const variants = {
    neutral: { background: "var(--surface-muted)", color: "var(--text-secondary)", border: "var(--border)" },
    primary: { background: "var(--primary-soft)", color: "var(--primary-text)", border: "var(--blue-100)" },
    success: { background: "var(--success-soft)", color: "var(--success-text)", border: "#BBF7D0" },
    warning: { background: "var(--warning-soft)", color: "var(--warning-text)", border: "#FDE68A" },
    danger:  { background: "var(--danger-soft)",  color: "var(--danger-text)",  border: "#FECACA" },
  };
  const v = variants[variant] || variants.neutral;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 5,
        height: 22,
        padding: "0 9px",
        fontFamily: "var(--font-sans)",
        fontSize: "var(--text-xs)",
        fontWeight: "var(--weight-medium)",
        lineHeight: 1,
        borderRadius: "var(--radius-full)",
        background: v.background,
        color: v.color,
        border: `1px solid ${v.border}`,
        whiteSpace: "nowrap",
        ...style,
      }}
      {...rest}
    >
      {children}
    </span>
  );
}
