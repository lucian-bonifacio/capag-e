**AccountRow** — one contábil account inside a `BalanceGroup`. Name + code on the left, value, an include/exclude `Switch`, and an audit action button on the right.

```jsx
<AccountRow
  name="Caixa e Equivalentes" code="1.1.1.01"
  value="R$ 4.210.500,00"
  included={inc} onToggle={setInc}
  onAudit={() => openAudit(account)}
/>
```

The `Switch` includes/excludes the account from the calculations; an excluded row dims to 50%. The magnifier button opens the audit detail — label it "Auditar conta" / "Ver auditoria", **never** "filtrar".
