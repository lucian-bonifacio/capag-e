**Sidebar** — fixed 240px left navigation for the admin shell. White surface, blue-tinted active item, soft right border.

```jsx
<Sidebar
  activeId="balanco"
  onSelect={setView}
  items={[
    { id: "dashboard", label: "Dashboard", icon: <GridIcon/> },
    { id: "balanco", label: "Balanço Patrimonial", icon: <SheetIcon/> },
    { id: "indicadores", label: "Indicadores CAPAG", icon: <GaugeIcon/> },
    { id: "auditoria", label: "Auditoria", icon: <SearchIcon/>, badge: 3 },
    { id: "importar", label: "Importar ECD", icon: <UploadIcon/> },
  ]}
/>
```

`items` carry `id`, `label`, optional `icon` and `badge`. Active item uses `--sidebar-active-bg` / `--sidebar-active-fg`. Pass a `footer` for the user/account block.
