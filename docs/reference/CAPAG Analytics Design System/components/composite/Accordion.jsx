import React from "react";

/**
 * Accordion — generic collapsible container.
 * Use `defaultOpen` for uncontrolled, or `open`+`onToggle` for controlled.
 */
export function Accordion({ title, meta = null, defaultOpen = false, open, onToggle, children }) {
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
        overflow: "hidden",
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
          width: "100%",
          padding: "var(--space-4) var(--space-5)",
          border: "none",
          background: hover ? "var(--surface-inset)" : "transparent",
          cursor: "pointer",
          textAlign: "left",
          transition: "background 100ms ease",
        }}
      >
        <Chevron open={isOpen} />
        <span
          style={{
            flex: 1,
            fontSize: "var(--text-md)",
            fontWeight: "var(--weight-semibold)",
            color: "var(--text-primary)",
          }}
        >
          {title}
        </span>
        {meta}
      </button>
      {isOpen && <div style={{ borderTop: "1px solid var(--border)" }}>{children}</div>}
    </div>
  );
}

export function Chevron({ open }) {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{
        color: "var(--text-muted)",
        flex: "none",
        transform: open ? "rotate(90deg)" : "rotate(0deg)",
        transition: "transform 140ms ease",
      }}
    >
      <path d="m9 18 6-6-6-6" />
    </svg>
  );
}
