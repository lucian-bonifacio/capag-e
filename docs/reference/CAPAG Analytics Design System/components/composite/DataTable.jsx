import React from "react";

/**
 * DataTable — analytical table for AUDIT views only (inside a Dialog or
 * secondary screen). Not for the dashboard.
 * `columns`: [{ key, header, align, width, render }]
 * `rows`: array of row objects.
 */
export function DataTable({ columns = [], rows = [], emptyText = "Sem registros." }) {
  return (
    <div
      style={{
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
        overflow: "hidden",
      }}
    >
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontFamily: "var(--font-sans)",
          fontSize: "var(--text-sm)",
        }}
      >
        <thead>
          <tr style={{ background: "var(--surface-inset)" }}>
            {columns.map((c) => (
              <th
                key={c.key}
                style={{
                  textAlign: c.align || "left",
                  padding: "10px 14px",
                  fontSize: "var(--text-xs)",
                  fontWeight: "var(--weight-semibold)",
                  letterSpacing: "var(--tracking-wide)",
                  textTransform: "uppercase",
                  color: "var(--text-secondary)",
                  borderBottom: "1px solid var(--border)",
                  width: c.width,
                  whiteSpace: "nowrap",
                }}
              >
                {c.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length}
                style={{ padding: "24px 14px", textAlign: "center", color: "var(--text-secondary)" }}
              >
                {emptyText}
              </td>
            </tr>
          ) : (
            rows.map((row, i) => (
              <tr
                key={row.id ?? i}
                style={{ background: i % 2 ? "var(--surface-inset)" : "var(--surface-card)" }}
              >
                {columns.map((c) => (
                  <td
                    key={c.key}
                    className={c.numeric ? "tnum" : undefined}
                    style={{
                      textAlign: c.align || "left",
                      padding: "10px 14px",
                      color: "var(--text-primary)",
                      borderBottom: i === rows.length - 1 ? "none" : "1px solid var(--border)",
                      whiteSpace: c.wrap ? "normal" : "nowrap",
                      fontVariantNumeric: c.numeric ? "tabular-nums" : undefined,
                    }}
                  >
                    {c.render ? c.render(row[c.key], row) : row[c.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
