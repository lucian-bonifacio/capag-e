import React from "react";

/**
 * Switch — toggle for including/excluding an account from calculations.
 * Controlled: pass `checked` and `onChange(nextChecked)`.
 */
export function Switch({
  checked = false,
  onChange,
  disabled = false,
  size = "md",
  tone = "solid",
  "aria-label": ariaLabel,
  ...rest
}) {
  const dims = {
    sm: { w: 32, h: 18, knob: 13, pad: 2.5 },
    md: { w: 40, h: 24, knob: 18, pad: 3 },
  };
  const d = dims[size] || dims.md;
  // "soft" = azul translúcido, menos chamativo (linhas de conta do balanço)
  const onColor = tone === "soft" ? "rgba(59,130,246,0.45)" : "var(--primary)";

  return (
    <button
      role="switch"
      aria-checked={checked}
      aria-label={ariaLabel}
      disabled={disabled}
      onClick={() => !disabled && onChange && onChange(!checked)}
      style={{
        position: "relative",
        width: d.w,
        height: d.h,
        flex: "none",
        padding: 0,
        border: "none",
        borderRadius: "var(--radius-full)",
        cursor: disabled ? "not-allowed" : "pointer",
        background: checked ? onColor : "var(--slate-300)",
        opacity: disabled ? 0.5 : 1,
        transition: "background 140ms ease",
      }}
      {...rest}
    >
      <span
        style={{
          position: "absolute",
          top: d.pad,
          left: checked ? d.w - d.knob - d.pad : d.pad,
          width: d.knob,
          height: d.knob,
          borderRadius: "var(--radius-full)",
          background: "#FFFFFF",
          boxShadow: "var(--shadow-sm)",
          transition: "left 140ms ease",
        }}
      />
    </button>
  );
}
