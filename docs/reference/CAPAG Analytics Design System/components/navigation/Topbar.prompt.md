**Topbar** — 60px top bar pairing with the Sidebar. Page title on the left, actions (search, buttons, user) on the right.

```jsx
<Topbar
  title="Balanço Patrimonial"
  subtitle="Exercício 2024"
  actions={<><Input iconLeft={<SearchIcon/>} placeholder="Buscar…" /><Button>Importar ECD</Button></>}
/>
```

Keep it simple and flat — white background, single bottom border, no shadow. Use `breadcrumb` for a small context line above the title.
