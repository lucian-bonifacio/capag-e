**Card / CardHeader / StatCard** — the white surface container used for every panel, plus a `StatCard` for dashboard KPI tiles.

```jsx
<Card>
  <CardHeader title="Balanço Patrimonial" subtitle="Exercício 2024" action={<Button size="sm" variant="secondary">Exportar</Button>} />
  …
</Card>

<StatCard label="Indicador CAPAG" value="B" tone="success" hint="Capacidade de pagamento boa" />
<StatCard label="Liquidez Corrente" value="1,84" tone="neutral" />
```

Cards are white, 1px border, `--radius-lg`, `--shadow-xs` only — never heavy shadows. Use `StatCard` for calculated indicators at the top of the dashboard (never raw balance values). `tone` colors the value for semantic emphasis.
