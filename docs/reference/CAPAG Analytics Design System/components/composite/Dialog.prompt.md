**Dialog** — modal overlay. This is **where the analytical audit table belongs** — never inline on the dashboard. Soft slate scrim, centered white panel.

```jsx
<Dialog open={open} onClose={close} title="Auditoria — Ativo Circulante" subtitle="18 contas · R$ 21,4 mi"
  footer={<><Button variant="secondary" onClick={close}>Fechar</Button><Button>Exportar</Button></>}>
  <DataTable columns={…} rows={…} />
</Dialog>
```

Controlled via `open` + `onClose`. Closes on Escape or scrim click. Use it for "Auditar conta" / "Ver auditoria" detail views.
