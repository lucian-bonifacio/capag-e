**Switch** — toggles whether a contábil account is **included** or **excluded** from the CAPAG calculations. Blue when on, slate when off.

```jsx
<Switch checked={included} onChange={setIncluded} aria-label="Incluir conta nos cálculos" />
```

Controlled only: pass `checked` and handle `onChange(next)`. Sizes `sm` / `md`. Always supply `aria-label` describing what the toggle includes/excludes.
