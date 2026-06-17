**Accordion** — generic collapsible card. Header with a chevron and right-aligned `meta`. Use it for grouping; for the balance sheet prefer the purpose-built `BalanceGroup`.

```jsx
<Accordion title="Ativo Circulante" defaultOpen meta={<Badge variant="neutral">12 contas</Badge>}>
  …rows…
</Accordion>
```

Uncontrolled via `defaultOpen`, or controlled via `open` + `onToggle`. `Chevron` is exported for reuse.
