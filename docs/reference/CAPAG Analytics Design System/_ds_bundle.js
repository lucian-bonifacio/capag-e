/* @ds-bundle: {"format":3,"namespace":"CAPAGAnalyticsDesignSystem_0c00db","components":[{"name":"AccountRow","sourcePath":"components/balance/AccountRow.jsx"},{"name":"AuditButton","sourcePath":"components/balance/AccountRow.jsx"},{"name":"BalanceGroup","sourcePath":"components/balance/BalanceGroup.jsx"},{"name":"BalanceLedger","sourcePath":"components/balance/BalanceLedger.jsx"},{"name":"Accordion","sourcePath":"components/composite/Accordion.jsx"},{"name":"Chevron","sourcePath":"components/composite/Accordion.jsx"},{"name":"DataTable","sourcePath":"components/composite/DataTable.jsx"},{"name":"Dialog","sourcePath":"components/composite/Dialog.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"CardHeader","sourcePath":"components/core/Card.jsx"},{"name":"StatCard","sourcePath":"components/core/Card.jsx"},{"name":"Input","sourcePath":"components/core/Input.jsx"},{"name":"Switch","sourcePath":"components/core/Switch.jsx"},{"name":"SegmentedControl","sourcePath":"components/navigation/SegmentedControl.jsx"},{"name":"Sidebar","sourcePath":"components/navigation/Sidebar.jsx"},{"name":"Topbar","sourcePath":"components/navigation/Topbar.jsx"}],"sourceHashes":{"components/balance/AccountRow.jsx":"212a1982103a","components/balance/BalanceGroup.jsx":"a8079121d8b3","components/balance/BalanceLedger.jsx":"4b775e15d282","components/composite/Accordion.jsx":"064837c94357","components/composite/DataTable.jsx":"32a30ea5c7f2","components/composite/Dialog.jsx":"eca62501bc08","components/core/Badge.jsx":"e51c041dbd1a","components/core/Button.jsx":"a2e8e4be4672","components/core/Card.jsx":"dad9c9f246a6","components/core/Input.jsx":"09bfb3e6e59f","components/core/Switch.jsx":"69d31bc2cbb6","components/navigation/SegmentedControl.jsx":"29acef42ecac","components/navigation/Sidebar.jsx":"c484f9f97402","components/navigation/Topbar.jsx":"617d82b59acb","drafts/Variants.jsx":"9d38708fc7af","ui_kits/dashboard/Dashboard.jsx":"8fdcefcfd22a","ui_kits/dashboard/data.js":"54aedfc50e80"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.CAPAGAnalyticsDesignSystem_0c00db = window.CAPAGAnalyticsDesignSystem_0c00db || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/composite/Accordion.jsx
try { (() => {
/**
 * Accordion — generic collapsible container.
 * Use `defaultOpen` for uncontrolled, or `open`+`onToggle` for controlled.
 */
function Accordion({
  title,
  meta = null,
  defaultOpen = false,
  open,
  onToggle,
  children
}) {
  const [internal, setInternal] = React.useState(defaultOpen);
  const isOpen = open != null ? open : internal;
  const toggle = () => onToggle ? onToggle(!isOpen) : setInternal(v => !v);
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--surface-card)",
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: toggle,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-3)",
      width: "100%",
      padding: "var(--space-4) var(--space-5)",
      border: "none",
      background: hover ? "var(--surface-inset)" : "transparent",
      cursor: "pointer",
      textAlign: "left",
      transition: "background 100ms ease"
    }
  }, /*#__PURE__*/React.createElement(Chevron, {
    open: isOpen
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--text-primary)"
    }
  }, title), meta), isOpen && /*#__PURE__*/React.createElement("div", {
    style: {
      borderTop: "1px solid var(--border)"
    }
  }, children));
}
function Chevron({
  open
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "16",
    height: "16",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    style: {
      color: "var(--text-muted)",
      flex: "none",
      transform: open ? "rotate(90deg)" : "rotate(0deg)",
      transition: "transform 140ms ease"
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "m9 18 6-6-6-6"
  }));
}
Object.assign(__ds_scope, { Accordion, Chevron });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/composite/Accordion.jsx", error: String((e && e.message) || e) }); }

// components/composite/DataTable.jsx
try { (() => {
/**
 * DataTable — analytical table for AUDIT views only (inside a Dialog or
 * secondary screen). Not for the dashboard.
 * `columns`: [{ key, header, align, width, render }]
 * `rows`: array of row objects.
 */
function DataTable({
  columns = [],
  rows = [],
  emptyText = "Sem registros."
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      width: "100%",
      borderCollapse: "collapse",
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-sm)"
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: "var(--surface-inset)"
    }
  }, columns.map(c => /*#__PURE__*/React.createElement("th", {
    key: c.key,
    style: {
      textAlign: c.align || "left",
      padding: "10px 14px",
      fontSize: "var(--text-xs)",
      fontWeight: "var(--weight-semibold)",
      letterSpacing: "var(--tracking-wide)",
      textTransform: "uppercase",
      color: "var(--text-secondary)",
      borderBottom: "1px solid var(--border)",
      width: c.width,
      whiteSpace: "nowrap"
    }
  }, c.header)))), /*#__PURE__*/React.createElement("tbody", null, rows.length === 0 ? /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("td", {
    colSpan: columns.length,
    style: {
      padding: "24px 14px",
      textAlign: "center",
      color: "var(--text-secondary)"
    }
  }, emptyText)) : rows.map((row, i) => /*#__PURE__*/React.createElement("tr", {
    key: row.id ?? i,
    style: {
      background: i % 2 ? "var(--surface-inset)" : "var(--surface-card)"
    }
  }, columns.map(c => /*#__PURE__*/React.createElement("td", {
    key: c.key,
    className: c.numeric ? "tnum" : undefined,
    style: {
      textAlign: c.align || "left",
      padding: "10px 14px",
      color: "var(--text-primary)",
      borderBottom: i === rows.length - 1 ? "none" : "1px solid var(--border)",
      whiteSpace: c.wrap ? "normal" : "nowrap",
      fontVariantNumeric: c.numeric ? "tabular-nums" : undefined
    }
  }, c.render ? c.render(row[c.key], row) : row[c.key])))))));
}
Object.assign(__ds_scope, { DataTable });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/composite/DataTable.jsx", error: String((e && e.message) || e) }); }

// components/composite/Dialog.jsx
try { (() => {
/**
 * Dialog — modal overlay for audit detail / secondary views.
 * Controlled via `open` + `onClose`. Renders a soft scrim and centered panel.
 */
function Dialog({
  open,
  onClose,
  title,
  subtitle,
  footer,
  width = 720,
  children
}) {
  React.useEffect(() => {
    if (!open) return;
    const onKey = e => e.key === "Escape" && onClose && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);
  if (!open) return null;
  return /*#__PURE__*/React.createElement("div", {
    onMouseDown: e => e.target === e.currentTarget && onClose && onClose(),
    style: {
      position: "fixed",
      inset: 0,
      zIndex: 50,
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "center",
      padding: "8vh 24px 24px",
      background: "rgba(15, 23, 42, 0.40)",
      backdropFilter: "blur(1px)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    role: "dialog",
    "aria-modal": "true",
    style: {
      width: "100%",
      maxWidth: width,
      maxHeight: "84vh",
      display: "flex",
      flexDirection: "column",
      background: "var(--surface-card)",
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-xl)",
      boxShadow: "var(--shadow-overlay)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "space-between",
      gap: "var(--space-4)",
      padding: "var(--space-5) var(--space-6)",
      borderBottom: "1px solid var(--border)",
      flex: "none"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-lg)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--text-primary)",
      letterSpacing: "var(--tracking-tight)"
    }
  }, title), subtitle && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--text-secondary)",
      marginTop: 3
    }
  }, subtitle)), /*#__PURE__*/React.createElement("button", {
    onClick: onClose,
    "aria-label": "Fechar",
    style: {
      width: 32,
      height: 32,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      border: "none",
      background: "transparent",
      borderRadius: "var(--radius-md)",
      cursor: "pointer",
      color: "var(--text-secondary)",
      flex: "none"
    },
    onMouseEnter: e => e.currentTarget.style.background = "var(--surface-muted)",
    onMouseLeave: e => e.currentTarget.style.background = "transparent"
  }, /*#__PURE__*/React.createElement("svg", {
    width: "18",
    height: "18",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18 6 6 18M6 6l12 12"
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "var(--space-6)",
      overflowY: "auto",
      flex: 1
    }
  }, children), footer && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "flex-end",
      gap: "var(--space-3)",
      padding: "var(--space-4) var(--space-6)",
      borderTop: "1px solid var(--border)",
      background: "var(--surface-inset)",
      flex: "none"
    }
  }, footer)));
}
Object.assign(__ds_scope, { Dialog });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/composite/Dialog.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Badge — compact status / category label.
 * Variants: neutral | primary | success | warning | danger
 */
function Badge({
  variant = "neutral",
  children,
  style = {},
  ...rest
}) {
  const variants = {
    neutral: {
      background: "var(--surface-muted)",
      color: "var(--text-secondary)",
      border: "var(--border)"
    },
    primary: {
      background: "var(--primary-soft)",
      color: "var(--primary-text)",
      border: "var(--blue-100)"
    },
    success: {
      background: "var(--success-soft)",
      color: "var(--success-text)",
      border: "#BBF7D0"
    },
    warning: {
      background: "var(--warning-soft)",
      color: "var(--warning-text)",
      border: "#FDE68A"
    },
    danger: {
      background: "var(--danger-soft)",
      color: "var(--danger-text)",
      border: "#FECACA"
    }
  };
  const v = variants[variant] || variants.neutral;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
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
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Button — primary administrative action button.
 * Variants: primary | secondary | ghost | danger
 * Sizes: sm | md
 */
function Button({
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
    sm: {
      height: 32,
      padding: "0 12px",
      fontSize: "var(--text-sm)",
      gap: 6
    },
    md: {
      height: 38,
      padding: "0 16px",
      fontSize: "var(--text-base)",
      gap: 8
    }
  };
  const variants = {
    primary: {
      background: "var(--primary)",
      color: "var(--text-on-brand)",
      border: "1px solid var(--primary)"
    },
    secondary: {
      background: "var(--surface-card)",
      color: "var(--text-primary)",
      border: "1px solid var(--border-strong)"
    },
    ghost: {
      background: "transparent",
      color: "var(--text-secondary)",
      border: "1px solid transparent"
    },
    danger: {
      background: "var(--danger)",
      color: "var(--text-on-brand)",
      border: "1px solid var(--danger)"
    }
  };
  const s = sizes[size] || sizes.md;
  const v = variants[variant] || variants.primary;
  const [hover, setHover] = React.useState(false);
  const hoverStyle = !disabled && hover ? {
    primary: {
      background: "var(--primary-hover)",
      borderColor: "var(--primary-hover)"
    },
    secondary: {
      background: "var(--surface-muted)"
    },
    ghost: {
      background: "var(--surface-muted)",
      color: "var(--text-primary)"
    },
    danger: {
      background: "var(--danger-text)",
      borderColor: "var(--danger-text)"
    }
  }[variant] : {};
  return /*#__PURE__*/React.createElement("button", _extends({
    disabled: disabled,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
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
      ...style
    }
  }, rest), iconLeft, children, iconRight);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Card — white surface container with soft border.
 * Compose with CardHeader / CardBody, or just pass children.
 */
function Card({
  children,
  padding = "var(--space-6)",
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      background: "var(--surface-card)",
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)",
      boxShadow: "var(--shadow-xs)",
      padding,
      ...style
    }
  }, rest), children);
}
function CardHeader({
  title,
  subtitle,
  action,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "space-between",
      gap: "var(--space-4)",
      marginBottom: "var(--space-4)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", null, title && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-lg)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--text-primary)",
      letterSpacing: "var(--tracking-tight)"
    }
  }, title), subtitle && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--text-secondary)",
      marginTop: 2
    }
  }, subtitle)), action);
}

/**
 * StatCard — KPI / indicator tile for the dashboard top row.
 * Shows a label, a large value, and optional delta/hint.
 */
function StatCard({
  label,
  value,
  hint,
  tone = "neutral",
  icon = null,
  style = {}
}) {
  const tones = {
    neutral: "var(--text-primary)",
    primary: "var(--primary)",
    success: "var(--success)",
    warning: "var(--warning-text)",
    danger: "var(--danger)"
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--surface-card)",
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)",
      boxShadow: "var(--shadow-xs)",
      padding: "var(--space-5)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: "var(--space-3)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      fontWeight: "var(--weight-semibold)",
      letterSpacing: "var(--tracking-wide)",
      textTransform: "uppercase",
      color: "var(--text-secondary)"
    }
  }, label), icon && /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--text-muted)",
      display: "flex"
    }
  }, icon)), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      marginTop: "var(--space-3)",
      fontSize: "var(--text-2xl)",
      fontWeight: "var(--weight-semibold)",
      lineHeight: 1.1,
      color: tones[tone] || tones.neutral,
      letterSpacing: "var(--tracking-tight)"
    }
  }, value), hint && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6,
      fontSize: "var(--text-sm)",
      color: "var(--text-secondary)"
    }
  }, hint));
}
Object.assign(__ds_scope, { Card, CardHeader, StatCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Input — text / search field. Pass `iconLeft` for a search glyph.
 */
function Input({
  iconLeft = null,
  size = "md",
  style = {},
  wrapperStyle = {},
  disabled = false,
  ...rest
}) {
  const heights = {
    sm: 32,
    md: 38
  };
  const h = heights[size] || heights.md;
  const [focus, setFocus] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
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
      ...wrapperStyle
    }
  }, iconLeft && /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      color: "var(--text-muted)",
      flex: "none"
    }
  }, iconLeft), /*#__PURE__*/React.createElement("input", _extends({
    disabled: disabled,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      flex: 1,
      minWidth: 0,
      height: "100%",
      border: "none",
      outline: "none",
      background: "transparent",
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-base)",
      color: "var(--text-primary)",
      ...style
    }
  }, rest)));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input.jsx", error: String((e && e.message) || e) }); }

// components/core/Switch.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Switch — toggle for including/excluding an account from calculations.
 * Controlled: pass `checked` and `onChange(nextChecked)`.
 */
function Switch({
  checked = false,
  onChange,
  disabled = false,
  size = "md",
  tone = "solid",
  "aria-label": ariaLabel,
  ...rest
}) {
  const dims = {
    sm: {
      w: 32,
      h: 18,
      knob: 13,
      pad: 2.5
    },
    md: {
      w: 40,
      h: 24,
      knob: 18,
      pad: 3
    }
  };
  const d = dims[size] || dims.md;
  // "soft" = azul translúcido, menos chamativo (linhas de conta do balanço)
  const onColor = tone === "soft" ? "rgba(59,130,246,0.45)" : "var(--primary)";
  return /*#__PURE__*/React.createElement("button", _extends({
    role: "switch",
    "aria-checked": checked,
    "aria-label": ariaLabel,
    disabled: disabled,
    onClick: () => !disabled && onChange && onChange(!checked),
    style: {
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
      transition: "background 140ms ease"
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: d.pad,
      left: checked ? d.w - d.knob - d.pad : d.pad,
      width: d.knob,
      height: d.knob,
      borderRadius: "var(--radius-full)",
      background: "#FFFFFF",
      boxShadow: "var(--shadow-sm)",
      transition: "left 140ms ease"
    }
  }));
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Switch.jsx", error: String((e && e.message) || e) }); }

// components/balance/AccountRow.jsx
try { (() => {
/**
 * AccountRow — a single contábil account inside a balance group.
 * Shows name + code, value, an include/exclude Switch and an audit action.
 * Recuada (subgrupo) sob o macrogrupo. Quando excluída, a linha esmaece e
 * o nome/valor ganham tachado para reforçar que está fora dos cálculos.
 */
function AccountRow({
  name,
  code,
  value,
  included = true,
  onToggle,
  onAudit
}) {
  const [hover, setHover] = React.useState(false);
  const strike = {
    textDecoration: included ? "none" : "line-through"
  };
  return /*#__PURE__*/React.createElement("div", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-3)",
      padding: "8px 14px 8px 46px",
      background: hover ? "var(--surface-inset)" : "transparent",
      borderTop: "1px solid var(--border)",
      transition: "background-color 100ms ease",
      opacity: included ? 1 : 0.55
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--slate-700)",
      lineHeight: 1.3,
      ...strike
    }
  }, name), code && /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      fontSize: 11,
      color: "var(--text-muted)",
      marginTop: 1
    }
  }, code)), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-normal)",
      color: "var(--slate-700)",
      fontVariantNumeric: "tabular-nums",
      textAlign: "right",
      whiteSpace: "nowrap",
      minWidth: 110,
      ...strike
    }
  }, value), /*#__PURE__*/React.createElement(__ds_scope.Switch, {
    size: "sm",
    tone: "soft",
    checked: included,
    onChange: onToggle,
    "aria-label": `${included ? "Excluir" : "Incluir"} ${typeof name === "string" ? name : "conta"} dos cálculos`
  }), /*#__PURE__*/React.createElement(AuditButton, {
    onClick: onAudit,
    label: `Auditar conta ${typeof name === "string" ? name : ""}`
  }));
}

/** Ícone de auditoria (prancheta com check) — substitui a antiga lupa. */
function AuditButton({
  onClick,
  label = "Ver auditoria",
  title = "Ver auditoria"
}) {
  const [h, setH] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    title: title,
    "aria-label": label,
    onMouseEnter: () => setH(true),
    onMouseLeave: () => setH(false),
    style: {
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
      transition: "all 100ms ease"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("rect", {
    width: "8",
    height: "4",
    x: "8",
    y: "2",
    rx: "1"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m9 14 2 2 4-4"
  })));
}
Object.assign(__ds_scope, { AccountRow, AuditButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/balance/AccountRow.jsx", error: String((e && e.message) || e) }); }

// components/balance/BalanceGroup.jsx
try { (() => {
/**
 * BalanceGroup — collapsible balance-sheet group.
 * Header shows the group name, account count, total value and percentage.
 * Children are AccountRow elements. A trailing "audit group" action is optional.
 */
function BalanceGroup({
  name,
  count,
  total,
  percent,
  defaultOpen = true,
  open,
  onToggle,
  onAuditGroup,
  children
}) {
  const [internal, setInternal] = React.useState(defaultOpen);
  const isOpen = open != null ? open : internal;
  const toggle = () => onToggle ? onToggle(!isOpen) : setInternal(v => !v);
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--surface-card)",
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)",
      boxShadow: "var(--shadow-xs)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-3)",
      background: hover ? "var(--surface-inset)" : "var(--surface-muted)",
      transition: "background-color 100ms ease"
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: toggle,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-3)",
      flex: 1,
      minWidth: 0,
      padding: "11px 14px",
      border: "none",
      background: "transparent",
      cursor: "pointer",
      textAlign: "left"
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Chevron, {
    open: isOpen
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontSize: 12,
      fontWeight: "var(--weight-bold)",
      letterSpacing: "0.05em",
      textTransform: "uppercase",
      color: "var(--text-primary)",
      lineHeight: 1.25
    }
  }, name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--text-secondary)"
    }
  }, count, " ", count === 1 ? "conta" : "contas")), percent != null && /*#__PURE__*/React.createElement("span", {
    className: "tnum",
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--text-secondary)",
      fontVariantNumeric: "tabular-nums",
      minWidth: 46,
      textAlign: "right"
    }
  }, percent), /*#__PURE__*/React.createElement("span", {
    className: "tnum",
    style: {
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--text-primary)",
      fontVariantNumeric: "tabular-nums",
      minWidth: 130,
      textAlign: "right"
    }
  }, total)), onAuditGroup && /*#__PURE__*/React.createElement("span", {
    style: {
      marginRight: "var(--space-4)",
      display: "flex"
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.AuditButton, {
    onClick: onAuditGroup,
    title: "Ver auditoria do grupo",
    label: `Auditar grupo ${typeof name === "string" ? name : ""}`
  }))), isOpen && /*#__PURE__*/React.createElement("div", null, children));
}
Object.assign(__ds_scope, { BalanceGroup });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/balance/BalanceGroup.jsx", error: String((e && e.message) || e) }); }

// components/balance/BalanceLedger.jsx
try { (() => {
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
  const v = whole ? part / whole * 100 : 0;
  return v.toLocaleString("pt-BR", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }) + "%";
}
function LedgerHeaderRow() {
  const cell = {
    fontSize: 10,
    fontWeight: "var(--weight-semibold)",
    letterSpacing: "0.06em",
    textTransform: "uppercase",
    color: "var(--text-muted)"
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: GRID,
      gap: 12,
      alignItems: "center",
      padding: "8px 18px",
      borderBottom: "1px solid var(--border)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: cell
  }, "Conta"), /*#__PURE__*/React.createElement("div", {
    style: {
      ...cell,
      textAlign: "right"
    }
  }, "%"), /*#__PURE__*/React.createElement("div", {
    style: {
      ...cell,
      textAlign: "right"
    }
  }, "Valor"), /*#__PURE__*/React.createElement("div", {
    style: {
      ...cell,
      textAlign: "center"
    }
  }, "Incluir"), /*#__PURE__*/React.createElement("div", null));
}
function LedgerGroup({
  group,
  state,
  onToggle,
  onAudit,
  onAuditGroup,
  defaultOpen
}) {
  const [open, setOpen] = React.useState(defaultOpen);
  const [hover, setHover] = React.useState(false);
  const groupTotal = parseBRL(group.total);
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "grid",
      gridTemplateColumns: GRID,
      gap: 12,
      alignItems: "center",
      padding: "13px 18px",
      background: hover ? "var(--surface-inset)" : "var(--surface-muted)",
      borderTop: "1px solid var(--border)",
      transition: "background 100ms ease"
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: () => setOpen(v => !v),
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      minWidth: 0,
      border: "none",
      background: "transparent",
      cursor: "pointer",
      padding: 0,
      textAlign: "left"
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Chevron, {
    open: open
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      fontWeight: "var(--weight-bold)",
      letterSpacing: "0.05em",
      textTransform: "uppercase",
      color: "var(--text-primary)",
      whiteSpace: "nowrap",
      overflow: "hidden",
      textOverflow: "ellipsis"
    }
  }, group.name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--text-secondary)",
      flex: "none"
    }
  }, "\xB7 ", group.contas.length, " contas")), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      textAlign: "right",
      fontSize: "var(--text-sm)",
      color: "var(--text-secondary)",
      fontVariantNumeric: "tabular-nums"
    }
  }, group.percent), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      textAlign: "right",
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-bold)",
      color: "var(--text-primary)",
      fontVariantNumeric: "tabular-nums"
    }
  }, group.total), /*#__PURE__*/React.createElement("div", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "flex-end"
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.AuditButton, {
    onClick: () => onAuditGroup && onAuditGroup(group),
    title: "Ver auditoria do grupo",
    label: `Auditar grupo ${group.name}`
  }))), open && group.contas.map(c => {
    const on = state ? state[c.id] : c.included;
    const strike = {
      textDecoration: on ? "none" : "line-through"
    };
    return /*#__PURE__*/React.createElement("div", {
      key: c.id,
      style: {
        display: "grid",
        gridTemplateColumns: GRID,
        gap: 12,
        alignItems: "center",
        padding: "8px 18px 8px 52px",
        borderTop: "1px solid var(--border)",
        opacity: on ? 1 : 0.55
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        minWidth: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: "var(--text-sm)",
        color: "var(--slate-700)",
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
        ...strike
      }
    }, c.name), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: {
        fontSize: 11,
        color: "var(--text-muted)"
      }
    }, c.code)), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: {
        textAlign: "right",
        fontSize: 11,
        color: "var(--text-muted)",
        fontVariantNumeric: "tabular-nums"
      }
    }, fmtPct(parseBRL(c.value), groupTotal)), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: {
        textAlign: "right",
        fontSize: "var(--text-sm)",
        color: "var(--slate-700)",
        fontVariantNumeric: "tabular-nums",
        ...strike
      }
    }, c.value), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        justifyContent: "center"
      }
    }, /*#__PURE__*/React.createElement(__ds_scope.Switch, {
      size: "sm",
      tone: "soft",
      checked: on,
      onChange: v => onToggle && onToggle(c.id, v),
      "aria-label": `${on ? "Excluir" : "Incluir"} ${c.name}`
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        justifyContent: "flex-end"
      }
    }, /*#__PURE__*/React.createElement(__ds_scope.AuditButton, {
      onClick: () => onAudit && onAudit(c, group),
      label: `Auditar conta ${c.name}`
    })));
  }));
}
function BalanceLedger({
  eyebrow,
  title,
  total,
  groups = [],
  state,
  onToggle,
  onAudit,
  onAuditGroup,
  defaultOpenIds = []
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: "var(--space-6)"
    }
  }, (eyebrow || title || total) && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, eyebrow, eyebrow && title ? " · " : "", title), total && /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-bold)",
      color: "var(--text-primary)",
      fontVariantNumeric: "tabular-nums"
    }
  }, total)), /*#__PURE__*/React.createElement(LedgerHeaderRow, null), /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid var(--border)",
      borderTop: "none",
      borderRadius: "0 0 var(--radius-lg) var(--radius-lg)",
      overflow: "hidden",
      background: "var(--surface-card)"
    }
  }, groups.map(g => /*#__PURE__*/React.createElement(LedgerGroup, {
    key: g.id,
    group: g,
    state: state,
    onToggle: onToggle,
    onAudit: onAudit,
    onAuditGroup: onAuditGroup,
    defaultOpen: defaultOpenIds.includes(g.id)
  }))));
}
Object.assign(__ds_scope, { BalanceLedger });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/balance/BalanceLedger.jsx", error: String((e && e.message) || e) }); }

// components/navigation/SegmentedControl.jsx
try { (() => {
/**
 * SegmentedControl — compact toggle between a few mutually-exclusive views.
 * Used to switch the balance sheet between "two columns" and "ledger".
 * Controlled: pass `value` and `onChange(id)`.
 */
function SegmentedControl({
  options = [],
  value,
  onChange,
  size = "sm"
}) {
  const pad = size === "sm" ? "5px 11px" : "7px 14px";
  const fs = size === "sm" ? "var(--text-sm)" : "var(--text-base)";
  return /*#__PURE__*/React.createElement("div", {
    role: "tablist",
    style: {
      display: "inline-flex",
      gap: 2,
      padding: 3,
      background: "var(--surface-muted)",
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)"
    }
  }, options.map(opt => {
    const selected = opt.id === value;
    return /*#__PURE__*/React.createElement("button", {
      key: opt.id,
      role: "tab",
      "aria-selected": selected,
      onClick: () => onChange && onChange(opt.id),
      style: {
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
        transition: "color 100ms ease"
      }
    }, opt.icon, opt.label);
  }));
}
Object.assign(__ds_scope, { SegmentedControl });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/SegmentedControl.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Sidebar.jsx
try { (() => {
/**
 * Sidebar — fixed left navigation for the admin shell.
 * `items`: [{ id, label, icon, badge }]. Controlled via `activeId` + `onSelect`.
 */
function Sidebar({
  brand = "CAPAG Analytics",
  items = [],
  activeId,
  onSelect,
  footer = null,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("aside", {
    style: {
      width: "var(--sidebar-width)",
      flex: "none",
      height: "100%",
      display: "flex",
      flexDirection: "column",
      background: "var(--sidebar-bg)",
      borderRight: "1px solid var(--border)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: "var(--topbar-height)",
      display: "flex",
      alignItems: "center",
      gap: 10,
      padding: "0 var(--space-5)",
      borderBottom: "1px solid var(--border)",
      flex: "none"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 28,
      height: 28,
      borderRadius: "var(--radius-md)",
      background: "var(--primary)",
      color: "#fff",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontWeight: 700,
      fontSize: 14,
      flex: "none"
    }
  }, "C"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--text-primary)",
      letterSpacing: "var(--tracking-tight)"
    }
  }, brand)), /*#__PURE__*/React.createElement("nav", {
    style: {
      flex: 1,
      overflowY: "auto",
      padding: "var(--space-3)"
    }
  }, items.map(it => {
    const active = it.id === activeId;
    return /*#__PURE__*/React.createElement(SidebarItem, {
      key: it.id,
      item: it,
      active: active,
      onClick: () => onSelect && onSelect(it.id)
    });
  })), footer && /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "var(--space-3)",
      borderTop: "1px solid var(--border)",
      flex: "none"
    }
  }, footer));
}
function SidebarItem({
  item,
  active,
  onClick
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      width: "100%",
      height: 38,
      padding: "0 10px",
      marginBottom: 2,
      border: "none",
      borderRadius: "var(--radius-md)",
      cursor: "pointer",
      textAlign: "left",
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-base)",
      fontWeight: active ? "var(--weight-medium)" : "var(--weight-normal)",
      background: active ? "var(--sidebar-active-bg)" : hover ? "var(--sidebar-item-hover)" : "transparent",
      color: active ? "var(--sidebar-active-fg)" : "var(--sidebar-item)",
      transition: "background 100ms ease, color 100ms ease"
    }
  }, item.icon && /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      flex: "none",
      color: active ? "var(--sidebar-active-fg)" : "var(--text-muted)"
    }
  }, item.icon), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      whiteSpace: "nowrap",
      overflow: "hidden",
      textOverflow: "ellipsis"
    }
  }, item.label), item.badge != null && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      fontWeight: "var(--weight-medium)",
      color: "var(--text-secondary)",
      background: "var(--surface-muted)",
      borderRadius: "var(--radius-full)",
      padding: "1px 7px"
    }
  }, item.badge));
}
Object.assign(__ds_scope, { Sidebar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Sidebar.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Topbar.jsx
try { (() => {
/**
 * Topbar — simple top bar for the admin shell.
 * Title on the left, optional actions on the right.
 */
function Topbar({
  title,
  subtitle,
  breadcrumb = null,
  actions = null,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("header", {
    style: {
      height: "var(--topbar-height)",
      flex: "none",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: "var(--space-4)",
      padding: "0 var(--space-8)",
      background: "var(--surface-card)",
      borderBottom: "1px solid var(--border)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      minWidth: 0
    }
  }, breadcrumb && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--text-secondary)",
      marginBottom: 2
    }
  }, breadcrumb), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: 10,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontSize: "var(--text-xl)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--text-primary)",
      letterSpacing: "var(--tracking-tight)",
      whiteSpace: "nowrap"
    }
  }, title), subtitle && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--text-secondary)",
      whiteSpace: "nowrap",
      overflow: "hidden",
      textOverflow: "ellipsis",
      minWidth: 0
    }
  }, subtitle))), actions && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--space-3)",
      flex: "none"
    }
  }, actions));
}
Object.assign(__ds_scope, { Topbar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Topbar.jsx", error: String((e && e.message) || e) }); }

// drafts/Variants.jsx
try { (() => {
// CAPAG Analytics — RASCUNHO: variações de layout do Balanço Patrimonial
// V1 (duas colunas, refinada/consistente) · V2 (livro-razão) · V3 = V2 em dark mode azul.
const DSV = window.CAPAGAnalyticsDesignSystem_0c00db;
const {
  Chevron
} = DSV;

// ---------- helpers ----------
const parseBRL = s => {
  if (typeof s !== "string") return 0;
  const n = s.replace(/[^0-9,.-]/g, "").replace(/\./g, "").replace(",", ".");
  return parseFloat(n) || 0;
};
const pct = (part, whole) => whole ? part / whole * 100 : 0;
const fmtPct = n => n.toLocaleString("pt-BR", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1
}) + "%";

// ---------- ícone de auditoria (prancheta com check — não mais a lupa) ----------
const AuditGlyph = ({
  size = 15
}) => /*#__PURE__*/React.createElement("svg", {
  width: size,
  height: size,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: "2",
  strokeLinecap: "round",
  strokeLinejoin: "round"
}, /*#__PURE__*/React.createElement("rect", {
  width: "8",
  height: "4",
  x: "8",
  y: "2",
  rx: "1"
}), /*#__PURE__*/React.createElement("path", {
  d: "M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"
}), /*#__PURE__*/React.createElement("path", {
  d: "m9 14 2 2 4-4"
}));

// botão de auditoria discreto (ghost — moldura só no hover)
function AuditBtn({
  onClick,
  title = "Ver auditoria"
}) {
  const [h, setH] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    title: title,
    "aria-label": title,
    onMouseEnter: () => setH(true),
    onMouseLeave: () => setH(false),
    style: {
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
      transition: "all 100ms ease"
    }
  }, /*#__PURE__*/React.createElement(AuditGlyph, null));
}

// switch menor e menos chamativo (azul suave)
function MiniSwitch({
  checked,
  onChange
}) {
  const w = 32,
    h = 18,
    knob = 13,
    pad = 2.5;
  return /*#__PURE__*/React.createElement("button", {
    role: "switch",
    "aria-checked": checked,
    onClick: () => onChange && onChange(!checked),
    style: {
      position: "relative",
      width: w,
      height: h,
      flex: "none",
      padding: 0,
      border: "none",
      borderRadius: 999,
      cursor: "pointer",
      background: checked ? "rgba(59,130,246,0.45)" : "var(--slate-300)",
      transition: "background 140ms ease"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: pad,
      left: checked ? w - knob - pad : pad,
      width: knob,
      height: knob,
      borderRadius: 999,
      background: "#FFFFFF",
      boxShadow: "0 1px 2px rgba(15,23,42,.18)",
      transition: "left 140ms ease"
    }
  }));
}

// macrogrupo em caixa alta (compartilhado pelas versões)
const macroNameStyle = {
  fontSize: 12,
  fontWeight: 700,
  letterSpacing: "0.05em",
  textTransform: "uppercase",
  color: "var(--text-primary)",
  whiteSpace: "nowrap",
  overflow: "hidden",
  textOverflow: "ellipsis"
};
// nome de conta — recuado, fonte menor, discreto
const acctNameStyle = on => ({
  fontSize: "var(--text-sm)",
  color: "var(--slate-700)",
  whiteSpace: "nowrap",
  overflow: "hidden",
  textOverflow: "ellipsis",
  textDecoration: on ? "none" : "line-through"
});
// valor — MESMA fonte/peso/cor do nome da conta
const acctValueStyle = on => ({
  fontSize: "var(--text-sm)",
  fontWeight: 400,
  color: "var(--slate-700)",
  fontVariantNumeric: "tabular-nums",
  textAlign: "right",
  textDecoration: on ? "none" : "line-through"
});

// ===================================================================
// VARIANTE 1 — DUAS COLUNAS (refinada, consistente com a V2)
// ===================================================================
function TwoColGroup({
  g,
  incl,
  toggle,
  onAudit,
  onAuditGroup,
  defaultOpen
}) {
  const [open, setOpen] = React.useState(defaultOpen);
  const [hHead, setHHead] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--surface-card)",
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-lg)",
      boxShadow: "var(--shadow-xs)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      padding: "11px 14px",
      background: hHead ? "var(--surface-inset)" : "var(--surface-muted)",
      transition: "background 100ms ease"
    },
    onMouseEnter: () => setHHead(true),
    onMouseLeave: () => setHHead(false)
  }, /*#__PURE__*/React.createElement("button", {
    onClick: () => setOpen(v => !v),
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      flex: 1,
      minWidth: 0,
      border: "none",
      background: "transparent",
      cursor: "pointer",
      padding: 0,
      textAlign: "left"
    }
  }, /*#__PURE__*/React.createElement(Chevron, {
    open: open
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontSize: 12,
      fontWeight: 700,
      letterSpacing: "0.05em",
      textTransform: "uppercase",
      color: "var(--text-primary)",
      lineHeight: 1.25
    }
  }, g.name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--text-secondary)"
    }
  }, g.contas.length, " contas"))), /*#__PURE__*/React.createElement("span", {
    className: "tnum",
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--text-secondary)",
      flex: "none"
    }
  }, g.percent), /*#__PURE__*/React.createElement("span", {
    className: "tnum",
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: 700,
      color: "var(--text-primary)",
      whiteSpace: "nowrap",
      flex: "none"
    }
  }, g.total), /*#__PURE__*/React.createElement(AuditBtn, {
    onClick: () => onAuditGroup(g),
    title: "Auditar grupo " + g.name
  })), open && g.contas.map(c => {
    const on = incl[c.id];
    return /*#__PURE__*/React.createElement("div", {
      key: c.id,
      style: {
        display: "flex",
        alignItems: "center",
        gap: 10,
        padding: "8px 14px 8px 34px",
        borderTop: "1px solid var(--border)",
        opacity: on ? 1 : 0.55
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1,
        minWidth: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: "var(--text-sm)",
        color: "var(--slate-700)",
        lineHeight: 1.3,
        textDecoration: on ? "none" : "line-through"
      }
    }, c.name), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: {
        fontSize: 11,
        color: "var(--text-muted)"
      }
    }, c.code)), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: {
        ...acctValueStyle(on),
        whiteSpace: "nowrap",
        minWidth: 96,
        flex: "none"
      }
    }, c.value), /*#__PURE__*/React.createElement(MiniSwitch, {
      checked: on,
      onChange: val => toggle(c.id, val)
    }), /*#__PURE__*/React.createElement(AuditBtn, {
      onClick: () => onAudit(c, g)
    }));
  }));
}
function VariantCurrent({
  data,
  incl,
  toggle,
  onAudit,
  onAuditGroup
}) {
  const Col = ({
    eyebrow,
    title,
    groups,
    total
  }) => /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, eyebrow), /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: "2px 0 0",
      fontSize: "var(--text-lg)",
      fontWeight: 600,
      color: "var(--text-primary)"
    }
  }, title)), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: 700,
      color: "var(--text-primary)"
    }
  }, total)), groups.map(g => /*#__PURE__*/React.createElement(TwoColGroup, {
    key: g.id,
    g: g,
    incl: incl,
    toggle: toggle,
    onAudit: onAudit,
    onAuditGroup: onAuditGroup,
    defaultOpen: g.id === "ac" || g.id === "pc"
  })));
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 20,
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement(Col, {
    eyebrow: "Aplica\xE7\xF5es",
    title: "Ativos",
    groups: data.ativos,
    total: "R$ 48.200.000,00"
  }), /*#__PURE__*/React.createElement(Col, {
    eyebrow: "Origens",
    title: "Passivos e PL",
    groups: data.passivos,
    total: "R$ 48.200.000,00"
  }));
}

// ===================================================================
// VARIANTE 2 — LIVRO-RAZÃO ALINHADO (coluna única)
// ===================================================================
const GRID = "minmax(0,1fr) 72px 156px 46px 30px";
function LedgerHeader() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: GRID,
      gap: 12,
      alignItems: "center",
      padding: "8px 18px",
      borderBottom: "1px solid var(--border)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow",
    style: {
      fontSize: 10
    }
  }, "Conta"), /*#__PURE__*/React.createElement("div", {
    className: "eyebrow",
    style: {
      fontSize: 10,
      textAlign: "right"
    }
  }, "%"), /*#__PURE__*/React.createElement("div", {
    className: "eyebrow",
    style: {
      fontSize: 10,
      textAlign: "right"
    }
  }, "Valor"), /*#__PURE__*/React.createElement("div", {
    className: "eyebrow",
    style: {
      fontSize: 10,
      textAlign: "center"
    }
  }, "Incluir"), /*#__PURE__*/React.createElement("div", null));
}
function LedgerGroup({
  g,
  incl,
  toggle,
  onAudit,
  onAuditGroup,
  defaultOpen
}) {
  const [open, setOpen] = React.useState(defaultOpen);
  const [hHead, setHHead] = React.useState(false);
  const groupTotal = parseBRL(g.total);
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: GRID,
      gap: 12,
      alignItems: "center",
      padding: "13px 18px",
      background: hHead ? "var(--surface-inset)" : "var(--surface-muted)",
      borderTop: "1px solid var(--border)",
      transition: "background 100ms ease"
    },
    onMouseEnter: () => setHHead(true),
    onMouseLeave: () => setHHead(false)
  }, /*#__PURE__*/React.createElement("button", {
    onClick: () => setOpen(v => !v),
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      minWidth: 0,
      border: "none",
      background: "transparent",
      cursor: "pointer",
      padding: 0,
      textAlign: "left"
    }
  }, /*#__PURE__*/React.createElement(Chevron, {
    open: open
  }), /*#__PURE__*/React.createElement("span", {
    style: macroNameStyle
  }, g.name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--text-secondary)",
      flex: "none"
    }
  }, "\xB7 ", g.contas.length, " contas")), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      textAlign: "right",
      fontSize: "var(--text-sm)",
      color: "var(--text-secondary)"
    }
  }, g.percent), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      textAlign: "right",
      fontSize: "var(--text-md)",
      fontWeight: 700,
      color: "var(--text-primary)"
    }
  }, g.total), /*#__PURE__*/React.createElement("div", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "flex-end"
    }
  }, /*#__PURE__*/React.createElement(AuditBtn, {
    onClick: () => onAuditGroup(g),
    title: "Auditar grupo " + g.name
  }))), open && g.contas.map(c => {
    const v = parseBRL(c.value);
    const on = incl[c.id];
    return /*#__PURE__*/React.createElement("div", {
      key: c.id,
      style: {
        display: "grid",
        gridTemplateColumns: GRID,
        gap: 12,
        alignItems: "center",
        padding: "8px 18px 8px 52px",
        borderTop: "1px solid var(--border)",
        opacity: on ? 1 : 0.55
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        minWidth: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: acctNameStyle(on)
    }, c.name), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: {
        fontSize: 11,
        color: "var(--text-muted)"
      }
    }, c.code)), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: {
        textAlign: "right",
        fontSize: 11,
        color: "var(--text-muted)"
      }
    }, fmtPct(pct(v, groupTotal))), /*#__PURE__*/React.createElement("div", {
      className: "tnum",
      style: acctValueStyle(on)
    }, c.value), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        justifyContent: "center"
      }
    }, /*#__PURE__*/React.createElement(MiniSwitch, {
      checked: on,
      onChange: val => toggle(c.id, val)
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        justifyContent: "flex-end"
      }
    }, /*#__PURE__*/React.createElement(AuditBtn, {
      onClick: () => onAudit(c, g)
    })));
  }));
}
function LedgerSection({
  eyebrow,
  title,
  groups,
  total,
  incl,
  toggle,
  onAudit,
  onAuditGroup
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, eyebrow, " \xB7 ", title), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      fontSize: "var(--text-md)",
      fontWeight: 700,
      color: "var(--text-primary)"
    }
  }, total)), /*#__PURE__*/React.createElement(LedgerHeader, null), /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid var(--border)",
      borderTop: "none",
      borderRadius: "0 0 var(--radius-lg) var(--radius-lg)",
      overflow: "hidden",
      background: "var(--surface-card)"
    }
  }, groups.map(g => /*#__PURE__*/React.createElement(LedgerGroup, {
    key: g.id,
    g: g,
    incl: incl,
    toggle: toggle,
    onAudit: onAudit,
    onAuditGroup: onAuditGroup,
    defaultOpen: g.id === "ac" || g.id === "pc"
  }))));
}
function VariantLedger({
  data,
  incl,
  toggle,
  onAudit,
  onAuditGroup
}) {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(LedgerSection, {
    eyebrow: "Aplica\xE7\xF5es",
    title: "Ativos",
    groups: data.ativos,
    total: "R$ 48.200.000,00",
    incl: incl,
    toggle: toggle,
    onAudit: onAudit,
    onAuditGroup: onAuditGroup
  }), /*#__PURE__*/React.createElement(LedgerSection, {
    eyebrow: "Origens",
    title: "Passivos e Patrim\xF4nio L\xEDquido",
    groups: data.passivos,
    total: "R$ 48.200.000,00",
    incl: incl,
    toggle: toggle,
    onAudit: onAudit,
    onAuditGroup: onAuditGroup
  }));
}
window.CAPAGVariants = {
  VariantCurrent,
  VariantLedger
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "drafts/Variants.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/Dashboard.jsx
try { (() => {
// CAPAG Analytics — Dashboard screen (UI kit)
// Composes the design-system primitives into the real product view.
const DS = window.CAPAGAnalyticsDesignSystem_0c00db;
const {
  Sidebar,
  Topbar,
  StatCard,
  Card,
  CardHeader,
  BalanceGroup,
  AccountRow,
  BalanceLedger,
  SegmentedControl,
  Dialog,
  DataTable,
  Button,
  Input,
  Badge
} = DS;

// ---- icons (inline, Lucide-style stroke) ----
const Ico = paths => props => /*#__PURE__*/React.createElement("svg", {
  width: props && props.size || 18,
  height: props && props.size || 18,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: "2",
  strokeLinecap: "round",
  strokeLinejoin: "round"
}, paths);
const IconDash = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
  x: "3",
  y: "3",
  width: "7",
  height: "7"
}), /*#__PURE__*/React.createElement("rect", {
  x: "14",
  y: "3",
  width: "7",
  height: "7"
}), /*#__PURE__*/React.createElement("rect", {
  x: "14",
  y: "14",
  width: "7",
  height: "7"
}), /*#__PURE__*/React.createElement("rect", {
  x: "3",
  y: "14",
  width: "7",
  height: "7"
})));
const IconSheet = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
  x: "3",
  y: "3",
  width: "18",
  height: "18",
  rx: "2"
}), /*#__PURE__*/React.createElement("path", {
  d: "M12 3v18M3 9h18"
})));
const IconGauge = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
  d: "m12 14 4-5"
}), /*#__PURE__*/React.createElement("path", {
  d: "M3.5 18a9 9 0 1 1 17 0"
})));
const IconAudit = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
  cx: "11",
  cy: "11",
  r: "7"
}), /*#__PURE__*/React.createElement("path", {
  d: "m20 20-3.2-3.2"
})));
const IconUpload = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
  d: "M12 15V3m-5 5 5-5 5 5"
}), /*#__PURE__*/React.createElement("path", {
  d: "M5 21h14"
})));
const IconSearch = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
  cx: "11",
  cy: "11",
  r: "7"
}), /*#__PURE__*/React.createElement("path", {
  d: "m20 20-3.5-3.5"
})));
const IconColumns = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
  x: "3",
  y: "3",
  width: "7",
  height: "18",
  rx: "1"
}), /*#__PURE__*/React.createElement("rect", {
  x: "14",
  y: "3",
  width: "7",
  height: "18",
  rx: "1"
})));
const IconRows = Ico(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
  d: "M3 6h18M3 12h18M3 18h18"
})));
function GroupColumn({
  title,
  eyebrow,
  groups,
  total,
  state,
  onToggle,
  onAudit,
  onAuditGroup
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, eyebrow), /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: "2px 0 0",
      fontSize: "var(--text-lg)",
      fontWeight: 600,
      color: "var(--text-primary)"
    }
  }, title)), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      fontSize: "var(--text-md)",
      fontWeight: 700,
      color: "var(--text-primary)"
    }
  }, total)), groups.map(g => /*#__PURE__*/React.createElement(BalanceGroup, {
    key: g.id,
    name: g.name,
    count: g.contas.length,
    total: g.total,
    percent: g.percent,
    defaultOpen: g.id === "ac" || g.id === "pc",
    onAuditGroup: () => onAuditGroup(g)
  }, g.contas.map(c => /*#__PURE__*/React.createElement(AccountRow, {
    key: c.id,
    name: c.name,
    code: c.code,
    value: c.value,
    included: state[c.id],
    onToggle: v => onToggle(c.id, v),
    onAudit: () => onAudit(c, g)
  })))));
}
function Dashboard() {
  const data = window.CAPAG_DATA;
  const [active, setActive] = React.useState("balanco");
  const allGroups = [...data.ativos, ...data.passivos];

  // include/exclude state, keyed by account id
  const initial = {};
  allGroups.forEach(g => g.contas.forEach(c => initial[c.id] = c.included));
  const [incl, setIncl] = React.useState(initial);
  const toggle = (id, v) => setIncl(p => ({
    ...p,
    [id]: v
  }));
  const [audit, setAudit] = React.useState(null); // { title, subtitle }
  const [view, setView] = React.useState("columns"); // "columns" | "ledger"

  const openAccount = (c, g) => setAudit({
    title: `Auditoria — ${c.name}`,
    subtitle: `${c.code} · ${g.name}`
  });
  const openGroup = g => setAudit({
    title: `Auditoria — ${g.name}`,
    subtitle: `${g.contas.length} contas · ${g.total}`
  });
  const excluded = Object.values(incl).filter(v => !v).length;
  const auditCols = [{
    key: "data",
    header: "Data",
    width: 96
  }, {
    key: "hist",
    header: "Histórico",
    wrap: true
  }, {
    key: "doc",
    header: "Documento",
    width: 110
  }, {
    key: "deb",
    header: "Débito",
    align: "right",
    numeric: true,
    width: 120
  }, {
    key: "cred",
    header: "Crédito",
    align: "right",
    numeric: true,
    width: 120
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: "100vh",
      background: "var(--bg-app)"
    }
  }, /*#__PURE__*/React.createElement(Sidebar, {
    activeId: active,
    onSelect: setActive,
    items: [{
      id: "dashboard",
      label: "Dashboard",
      icon: /*#__PURE__*/React.createElement(IconDash, null)
    }, {
      id: "balanco",
      label: "Balanço Patrimonial",
      icon: /*#__PURE__*/React.createElement(IconSheet, null)
    }, {
      id: "indicadores",
      label: "Indicadores CAPAG",
      icon: /*#__PURE__*/React.createElement(IconGauge, null)
    }, {
      id: "auditoria",
      label: "Auditoria",
      icon: /*#__PURE__*/React.createElement(IconAudit, null),
      badge: excluded || undefined
    }, {
      id: "importar",
      label: "Importar ECD",
      icon: /*#__PURE__*/React.createElement(IconUpload, null)
    }],
    footer: /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        alignItems: "center",
        gap: 10,
        padding: "6px 6px"
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        width: 30,
        height: 30,
        borderRadius: "var(--radius-full)",
        background: "var(--slate-200)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 12,
        fontWeight: 600,
        color: "var(--slate-600)"
      }
    }, "RA"), /*#__PURE__*/React.createElement("div", {
      style: {
        lineHeight: 1.2
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 13,
        fontWeight: 600,
        color: "var(--text-primary)"
      }
    }, "Rafael Auditor"), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 11,
        color: "var(--text-secondary)"
      }
    }, "Analista cont\xE1bil")))
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: "flex",
      flexDirection: "column",
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement(Topbar, {
    title: "Balan\xE7o Patrimonial",
    subtitle: `${data.entidade} · Exercício ${data.exercicio}`,
    actions: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Input, {
      iconLeft: /*#__PURE__*/React.createElement(IconSearch, {
        size: 16
      }),
      placeholder: "Buscar conta ou grupo\u2026",
      size: "sm",
      wrapperStyle: {
        width: 240
      }
    }), /*#__PURE__*/React.createElement(Button, {
      size: "sm",
      variant: "secondary",
      iconLeft: /*#__PURE__*/React.createElement(IconAudit, {
        size: 15
      }),
      onClick: () => setAudit({
        title: "Auditoria geral",
        subtitle: "Razão analítico consolidado"
      })
    }, "Auditoria"), /*#__PURE__*/React.createElement(Button, {
      size: "sm",
      iconLeft: /*#__PURE__*/React.createElement(IconUpload, {
        size: 15
      })
    }, "Importar ECD"))
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      overflowY: "auto",
      padding: "var(--space-8)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 920,
      margin: "0 auto"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, "Indicadores calculados"), excluded > 0 && /*#__PURE__*/React.createElement(Badge, {
    variant: "warning"
  }, excluded, " conta", excluded > 1 ? "s" : "", " exclu\xEDda", excluded > 1 ? "s" : "", " dos c\xE1lculos")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(195px, 1fr))",
      gap: 16,
      marginBottom: "var(--space-8)"
    }
  }, data.indicadores.map(k => /*#__PURE__*/React.createElement(StatCard, {
    key: k.label,
    label: k.label,
    value: k.value,
    tone: k.tone,
    hint: k.hint,
    icon: /*#__PURE__*/React.createElement(IconGauge, {
      size: 16
    })
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, "Balan\xE7o Patrimonial"), /*#__PURE__*/React.createElement(SegmentedControl, {
    value: view,
    onChange: setView,
    options: [{
      id: "columns",
      label: "Duas colunas",
      icon: /*#__PURE__*/React.createElement(IconColumns, {
        size: 15
      })
    }, {
      id: "ledger",
      label: "Livro-razão",
      icon: /*#__PURE__*/React.createElement(IconRows, {
        size: 15
      })
    }]
  })), view === "columns" ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: "var(--space-5)",
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement(GroupColumn, {
    eyebrow: "Aplica\xE7\xF5es",
    title: "Ativos",
    groups: data.ativos,
    total: "R$ 48.200.000,00",
    state: incl,
    onToggle: toggle,
    onAudit: openAccount,
    onAuditGroup: openGroup
  }), /*#__PURE__*/React.createElement(GroupColumn, {
    eyebrow: "Origens",
    title: "Passivos e PL",
    groups: data.passivos,
    total: "R$ 48.200.000,00",
    state: incl,
    onToggle: toggle,
    onAudit: openAccount,
    onAuditGroup: openGroup
  })) : /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(BalanceLedger, {
    eyebrow: "Aplica\xE7\xF5es",
    title: "Ativos",
    total: "R$ 48.200.000,00",
    groups: data.ativos,
    state: incl,
    onToggle: toggle,
    onAudit: openAccount,
    onAuditGroup: openGroup,
    defaultOpenIds: ["ac"]
  }), /*#__PURE__*/React.createElement(BalanceLedger, {
    eyebrow: "Origens",
    title: "Passivos e Patrim\xF4nio L\xEDquido",
    total: "R$ 48.200.000,00",
    groups: data.passivos,
    state: incl,
    onToggle: toggle,
    onAudit: openAccount,
    onAuditGroup: openGroup,
    defaultOpenIds: ["pc"]
  }))))), /*#__PURE__*/React.createElement(Dialog, {
    open: !!audit,
    onClose: () => setAudit(null),
    width: 760,
    title: audit && audit.title,
    subtitle: audit && audit.subtitle,
    footer: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Button, {
      variant: "secondary",
      onClick: () => setAudit(null)
    }, "Fechar"), /*#__PURE__*/React.createElement(Button, null, "Exportar CSV"))
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 16,
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement(MiniStat, {
    label: "Lan\xE7amentos",
    value: "6"
  }), /*#__PURE__*/React.createElement(MiniStat, {
    label: "Total d\xE9bitos",
    value: "R$ 1.192.000,00"
  }), /*#__PURE__*/React.createElement(MiniStat, {
    label: "Total cr\xE9ditos",
    value: "R$ 2.388.600,00"
  })), /*#__PURE__*/React.createElement(DataTable, {
    columns: auditCols,
    rows: window.CAPAG_DATA.lancamentos
  })));
}
function MiniStat({
  label,
  value
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      border: "1px solid var(--border)",
      borderRadius: "var(--radius-md)",
      padding: "10px 14px",
      background: "var(--surface-inset)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      fontWeight: 600,
      letterSpacing: ".04em",
      textTransform: "uppercase",
      color: "var(--text-secondary)"
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    className: "tnum",
    style: {
      fontSize: 16,
      fontWeight: 600,
      color: "var(--text-primary)",
      marginTop: 3
    }
  }, value));
}
window.Dashboard = Dashboard;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/Dashboard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/data.js
try { (() => {
// CAPAG Analytics — sample balance-sheet data for the UI kit.
// Values in BRL. Codes follow a typical plano de contas público.
window.CAPAG_DATA = {
  exercicio: "2024",
  entidade: "Município de Exemplo",
  indicadores: [{
    label: "Indicador CAPAG",
    value: "B",
    tone: "success",
    hint: "Capacidade de pagamento boa"
  }, {
    label: "Liquidez Corrente",
    value: "1,84",
    tone: "neutral",
    hint: "Meta ≥ 1,00"
  }, {
    label: "Endividamento",
    value: "42,6%",
    tone: "warning",
    hint: "Dívida / RCL"
  }, {
    label: "Poupança Corrente",
    value: "11,2%",
    tone: "primary",
    hint: "Resultado corrente positivo"
  }],
  ativos: [{
    id: "ac",
    name: "Ativo Circulante",
    percent: "44%",
    total: "R$ 21.430.000,00",
    contas: [{
      id: "ac1",
      name: "Caixa e Equivalentes de Caixa",
      code: "1.1.1.01",
      value: "R$ 4.210.500,00",
      included: true
    }, {
      id: "ac2",
      name: "Aplicações Financeiras",
      code: "1.1.1.02",
      value: "R$ 8.900.000,00",
      included: true
    }, {
      id: "ac3",
      name: "Créditos a Receber",
      code: "1.1.2.01",
      value: "R$ 6.319.500,00",
      included: true
    }, {
      id: "ac4",
      name: "Estoques",
      code: "1.1.4.01",
      value: "R$ 1.200.000,00",
      included: true
    }, {
      id: "ac5",
      name: "VPD Pagas Antecipadamente",
      code: "1.1.9.01",
      value: "R$ 800.000,00",
      included: false
    }]
  }, {
    id: "anc",
    name: "Ativo Não Circulante",
    percent: "56%",
    total: "R$ 26.770.000,00",
    contas: [{
      id: "anc1",
      name: "Realizável a Longo Prazo",
      code: "1.2.1.01",
      value: "R$ 3.270.000,00",
      included: true
    }, {
      id: "anc2",
      name: "Investimentos",
      code: "1.2.2.01",
      value: "R$ 2.500.000,00",
      included: true
    }, {
      id: "anc3",
      name: "Imobilizado",
      code: "1.2.3.01",
      value: "R$ 19.500.000,00",
      included: true
    }, {
      id: "anc4",
      name: "Intangível",
      code: "1.2.4.01",
      value: "R$ 1.500.000,00",
      included: true
    }]
  }],
  passivos: [{
    id: "pc",
    name: "Passivo Circulante",
    percent: "24%",
    total: "R$ 11.640.000,00",
    contas: [{
      id: "pc1",
      name: "Fornecedores e Contas a Pagar",
      code: "2.1.3.01",
      value: "R$ 5.140.000,00",
      included: true
    }, {
      id: "pc2",
      name: "Obrigações Trabalhistas",
      code: "2.1.1.01",
      value: "R$ 3.500.000,00",
      included: true
    }, {
      id: "pc3",
      name: "Empréstimos a Curto Prazo",
      code: "2.1.2.01",
      value: "R$ 3.000.000,00",
      included: true
    }]
  }, {
    id: "pnc",
    name: "Passivo Não Circulante",
    percent: "31%",
    total: "R$ 15.000.000,00",
    contas: [{
      id: "pnc1",
      name: "Empréstimos a Longo Prazo",
      code: "2.2.2.01",
      value: "R$ 12.000.000,00",
      included: true
    }, {
      id: "pnc2",
      name: "Provisões a Longo Prazo",
      code: "2.2.7.01",
      value: "R$ 3.000.000,00",
      included: true
    }]
  }, {
    id: "pl",
    name: "Patrimônio Líquido",
    percent: "45%",
    total: "R$ 21.560.000,00",
    contas: [{
      id: "pl1",
      name: "Patrimônio Social e Capital Social",
      code: "2.3.1.01",
      value: "R$ 14.000.000,00",
      included: true
    }, {
      id: "pl2",
      name: "Resultados Acumulados",
      code: "2.3.7.01",
      value: "R$ 7.560.000,00",
      included: true
    }]
  }],
  // Sample analytical ledger for the audit dialog
  lancamentos: [{
    data: "08/01/2024",
    hist: "Recebimento de tributos — IPTU",
    doc: "ARR-0412",
    deb: "—",
    cred: "1.204.000,00"
  }, {
    data: "22/02/2024",
    hist: "Resgate de aplicação automática",
    doc: "APL-0098",
    deb: "—",
    cred: "980.000,00"
  }, {
    data: "15/03/2024",
    hist: "Pagamento de fornecedor — obra praça",
    doc: "PG-3391",
    deb: "842.000,00",
    cred: "—"
  }, {
    data: "30/04/2024",
    hist: "Transferência intragrupo conta única",
    doc: "TR-1180",
    deb: "350.000,00",
    cred: "—"
  }, {
    data: "19/05/2024",
    hist: "Rendimento de aplicação financeira",
    doc: "REN-0571",
    deb: "—",
    cred: "120.400,00"
  }, {
    data: "27/06/2024",
    hist: "Estorno de lançamento duplicado",
    doc: "EST-0042",
    deb: "—",
    cred: "84.200,00"
  }]
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/data.js", error: String((e && e.message) || e) }); }

__ds_ns.AccountRow = __ds_scope.AccountRow;

__ds_ns.AuditButton = __ds_scope.AuditButton;

__ds_ns.BalanceGroup = __ds_scope.BalanceGroup;

__ds_ns.BalanceLedger = __ds_scope.BalanceLedger;

__ds_ns.Accordion = __ds_scope.Accordion;

__ds_ns.Chevron = __ds_scope.Chevron;

__ds_ns.DataTable = __ds_scope.DataTable;

__ds_ns.Dialog = __ds_scope.Dialog;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.CardHeader = __ds_scope.CardHeader;

__ds_ns.StatCard = __ds_scope.StatCard;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Switch = __ds_scope.Switch;

__ds_ns.SegmentedControl = __ds_scope.SegmentedControl;

__ds_ns.Sidebar = __ds_scope.Sidebar;

__ds_ns.Topbar = __ds_scope.Topbar;

})();
