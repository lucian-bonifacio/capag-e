import React from "react";

/**
 * Button — primary administrative action button.
 * Variants: primary | secondary | ghost | danger
 * Sizes: sm | md
 */
export function Button({
  variant = "primary",
  size = "md",
  disabled = false,
  iconLeft = null,
  iconRight = null,
  children,
  style = {},
  ...rest
}) {
  const sizes = {
    sm: { height: 32, padding: "0 12px", fontSize: "var(--text-sm)", gap: 6 },
    md: { height: 38, padding: "0 16px", fontSize: "var(--text-base)", gap: 8 },
  };

  const variants = {
    primary: {
      background: "var(--primary)",
      color: "var(--text-on-brand)",
      border: "1px solid var(--primary)",
    },
    secondary: {
      background: "var(--surface-card)",
      color: "var(--text-primary)",
      border: "1px solid var(--border-strong)",
    },
    ghost: {
      background: "transparent",
      color: "var(--text-secondary)",
      border: "1px solid transparent",
    },
    danger: {
      background: "var(--danger)",
      color: "var(--text-on-brand)",
      border: "1px solid var(--danger)",
    },
  };

  const s = sizes[size] || sizes.md;
  const v = variants[variant] || variants.primary;

  const [hover, setHover] = React.useState(false);

  const hoverStyle = !disabled && hover
    ? {
        primary: { background: "var(--primary-hover)", borderColor: "var(--primary-hover)" },
        secondary: { background: "var(--surface-muted)" },
        ghost: { background: "var(--surface-muted)", color: "var(--text-primary)" },
        danger: { background: "var(--danger-text)", borderColor: "var(--danger-text)" },
      }[variant]
    : {};

  return (
    <button
      disabled={disabled}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: s.gap,
        height: s.height,
        padding: s.padding,
        fontFamily: "var(--font-sans)",
        fontSize: s.fontSize,
        fontWeight: "var(--weight-medium)",
        lineHeight: 1,
        borderRadius: "var(--radius-md)",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.5 : 1,
        whiteSpace: "nowrap",
        transition: "background 120ms ease, border-color 120ms ease",
        ...v,
        ...hoverStyle,
        ...style,
      }}
      {...rest}
    >
      {iconLeft}
      {children}
      {iconRight}
    </button>
  );
}
