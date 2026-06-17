import React from "react";

/**
 * Input — text / search field. Pass `iconLeft` for a search glyph.
 */
export function Input({
  iconLeft = null,
  size = "md",
  style = {},
  wrapperStyle = {},
  disabled = false,
  ...rest
}) {
  const heights = { sm: 32, md: 38 };
  const h = heights[size] || heights.md;
  const [focus, setFocus] = React.useState(false);

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        height: h,
        padding: iconLeft ? "0 12px 0 10px" : "0 12px",
        background: disabled ? "var(--surface-muted)" : "var(--surface-card)",
        border: `1px solid ${focus ? "var(--ring)" : "var(--border-strong)"}`,
        borderRadius: "var(--radius-md)",
        boxShadow: focus ? "0 0 0 3px rgba(37,99,235,0.12)" : "none",
        transition: "border-color 120ms ease, box-shadow 120ms ease",
        ...wrapperStyle,
      }}
    >
      {iconLeft && (
        <span style={{ display: "flex", color: "var(--text-muted)", flex: "none" }}>{iconLeft}</span>
      )}
      <input
        disabled={disabled}
        onFocus={() => setFocus(true)}
        onBlur={() => setFocus(false)}
        style={{
          flex: 1,
          minWidth: 0,
          height: "100%",
          border: "none",
          outline: "none",
          background: "transparent",
          fontFamily: "var(--font-sans)",
          fontSize: "var(--text-base)",
          color: "var(--text-primary)",
          ...style,
        }}
        {...rest}
      />
    </div>
  );
}
