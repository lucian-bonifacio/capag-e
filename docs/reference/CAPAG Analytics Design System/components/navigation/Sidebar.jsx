import React from "react";

/**
 * Sidebar — fixed left navigation for the admin shell.
 * `items`: [{ id, label, icon, badge }]. Controlled via `activeId` + `onSelect`.
 */
export function Sidebar({
  brand = "CAPAG Analytics",
  items = [],
  activeId,
  onSelect,
  footer = null,
  style = {},
}) {
  return (
    <aside
      style={{
        width: "var(--sidebar-width)",
        flex: "none",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        background: "var(--sidebar-bg)",
        borderRight: "1px solid var(--border)",
        ...style,
      }}
    >
      {/* Brand */}
      <div
        style={{
          height: "var(--topbar-height)",
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "0 var(--space-5)",
          borderBottom: "1px solid var(--border)",
          flex: "none",
        }}
      >
        <span
          style={{
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
            flex: "none",
          }}
        >
          C
        </span>
        <span
          style={{
            fontSize: "var(--text-md)",
            fontWeight: "var(--weight-semibold)",
            color: "var(--text-primary)",
            letterSpacing: "var(--tracking-tight)",
          }}
        >
          {brand}
        </span>
      </div>

      {/* Nav items */}
      <nav style={{ flex: 1, overflowY: "auto", padding: "var(--space-3)" }}>
        {items.map((it) => {
          const active = it.id === activeId;
          return (
            <SidebarItem
              key={it.id}
              item={it}
              active={active}
              onClick={() => onSelect && onSelect(it.id)}
            />
          );
        })}
      </nav>

      {footer && (
        <div style={{ padding: "var(--space-3)", borderTop: "1px solid var(--border)", flex: "none" }}>
          {footer}
        </div>
      )}
    </aside>
  );
}

function SidebarItem({ item, active, onClick }) {
  const [hover, setHover] = React.useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
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
        background: active
          ? "var(--sidebar-active-bg)"
          : hover
          ? "var(--sidebar-item-hover)"
          : "transparent",
        color: active ? "var(--sidebar-active-fg)" : "var(--sidebar-item)",
        transition: "background 100ms ease, color 100ms ease",
      }}
    >
      {item.icon && (
        <span style={{ display: "flex", flex: "none", color: active ? "var(--sidebar-active-fg)" : "var(--text-muted)" }}>
          {item.icon}
        </span>
      )}
      <span style={{ flex: 1, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
        {item.label}
      </span>
      {item.badge != null && (
        <span
          style={{
            fontSize: "var(--text-xs)",
            fontWeight: "var(--weight-medium)",
            color: "var(--text-secondary)",
            background: "var(--surface-muted)",
            borderRadius: "var(--radius-full)",
            padding: "1px 7px",
          }}
        >
          {item.badge}
        </span>
      )}
    </button>
  );
}
