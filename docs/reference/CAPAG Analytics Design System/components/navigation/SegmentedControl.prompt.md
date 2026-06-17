Compact toggle between a few mutually-exclusive views — use it to switch the balance sheet between layouts, or any 2–3 option view state.

```jsx
const [view, setView] = React.useState("columns");
<SegmentedControl
  value={view}
  onChange={setView}
  options={[
    { id: "columns", label: "Duas colunas", icon: <IconColumns /> },
    { id: "ledger", label: "Livro-razão", icon: <IconRows /> },
  ]}
/>
```

Controlled only — pass `value` and `onChange(id)`. Keep labels short (1–2 words). `size`: "sm" (default) or "md".
