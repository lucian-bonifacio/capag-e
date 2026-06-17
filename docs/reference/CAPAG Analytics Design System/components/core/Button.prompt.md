**Button** — the standard action control for the admin UI; use `primary` for the main action on a view, `secondary` for neutral actions, `ghost` for low-emphasis/toolbar actions, and `danger` for destructive ones.

```jsx
<Button variant="primary" onClick={save}>Salvar</Button>
<Button variant="secondary" size="sm">Cancelar</Button>
<Button variant="ghost" iconLeft={<SearchIcon/>}>Buscar</Button>
```

Variants: `primary` (blue), `secondary` (white + border), `ghost` (transparent), `danger` (red). Sizes: `sm` (32px), `md` (38px). Pass `iconLeft` / `iconRight` for icons. Never use more than one `primary` button per view.
