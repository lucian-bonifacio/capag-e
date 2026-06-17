**DataTable** — analytical table reserved for **audit views only**. Never place it as the central block of the dashboard; it lives inside a `Dialog` or a secondary screen.

```jsx
<DataTable
  columns={[
    { key: "conta", header: "Conta", wrap: true },
    { key: "codigo", header: "Código" },
    { key: "lancamentos", header: "Lançamentos", align: "right", numeric: true },
    { key: "saldo", header: "Saldo", align: "right", numeric: true },
  ]}
  rows={rows}
/>
```

Uppercase header on inset background, zebra rows, `numeric` columns get tabular figures. Use `render` for custom cells (badges, links).
