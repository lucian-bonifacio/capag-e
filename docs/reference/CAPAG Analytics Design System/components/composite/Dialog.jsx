import React from "react";

/**
 * Dialog — modal overlay for audit detail / secondary views.
 * Controlled via `open` + `onClose`. Renders a soft scrim and centered panel.
 */
export function Dialog({ open, onClose, title, subtitle, footer, width = 720, children }) {
  React.useEffect(() => {
    if (!open) return;
    const onKey = (e) => e.key === "Escape" && onClose && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      onMouseDown={(e) => e.target === e.currentTarget && onClose && onClose()}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 50,
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        padding: "8vh 24px 24px",
        background: "rgba(15, 23, 42, 0.40)",
        backdropFilter: "blur(1px)",
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        style={{
          width: "100%",
          maxWidth: width,
          maxHeight: "84vh",
          display: "flex",
          flexDirection: "column",
          background: "var(--surface-card)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius-xl)",
          boxShadow: "var(--shadow-overlay)",
          overflow: "hidden",
        }}
      >
        {/* Header */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-start",
            justifyContent: "space-between",
            gap: "var(--space-4)",
            padding: "var(--space-5) var(--space-6)",
            borderBottom: "1px solid var(--border)",
            flex: "none",
          }}
        >
          <div>
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
            {subtitle && (
              <div style={{ fontSize: "var(--text-sm)", color: "var(--text-secondary)", marginTop: 3 }}>
                {subtitle}
              </div>
            )}
          </div>
          <button
            onClick={onClose}
            aria-label="Fechar"
            style={{
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
              flex: "none",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.background = "var(--surface-muted)")}
            onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <path d="M18 6 6 18M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Body */}
        <div style={{ padding: "var(--space-6)", overflowY: "auto", flex: 1 }}>{children}</div>

        {/* Footer */}
        {footer && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-end",
              gap: "var(--space-3)",
              padding: "var(--space-4) var(--space-6)",
              borderTop: "1px solid var(--border)",
              background: "var(--surface-inset)",
              flex: "none",
            }}
          >
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
