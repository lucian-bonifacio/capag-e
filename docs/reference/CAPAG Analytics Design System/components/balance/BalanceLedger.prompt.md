Single-column "livro-razão" balance view with columns aligned across every group — the denser alternative to the two-column BalanceGroup layout, good for narrow widths.

```jsx
<BalanceLedger
  eyebrow="Aplicações" title="Ativos" total="R$ 48.200.000,00"
  groups={data.ativos}
  state={incl}
  onToggle={(id, on) => setIncl((p) => ({ ...p, [id]: on }))}
  onAudit={(conta, grupo) => openAudit(conta, grupo)}
  onAuditGroup={(grupo) => openAudit(null, grupo)}
  defaultOpenIds={["ac"]}
/>
```

Each group is `{ id, name, total, percent, contas: [{ id, name, code, value, included }] }`. Macrogroups render UPPERCASE; accounts indent as subgroups and get strikethrough + dimming when excluded. Render one `BalanceLedger` per section (Ativos, Passivos e PL). Toggle against the two-column view with `SegmentedControl`.
