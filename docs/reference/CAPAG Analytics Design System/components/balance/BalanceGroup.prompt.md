**BalanceGroup** — the collapsible group used to build the Balanço Patrimonial columns. Header shows name, account count, percentage and total; the body is a list of `AccountRow`s.

```jsx
<BalanceGroup name="Ativo Circulante" count={12} total="R$ 21.430.000,00" percent="44%"
  defaultOpen onAuditGroup={() => openAudit(group)}>
  <AccountRow name="Caixa e Equivalentes" code="1.1.1.01" value="R$ 4.210.500,00" included={a} onToggle={setA} onAudit={…} />
  <AccountRow name="Aplicações Financeiras" code="1.1.1.02" value="R$ 8.900.000,00" included={b} onToggle={setB} onAudit={…} />
</BalanceGroup>
```

Lay groups in two columns: **Ativos** on the left, **Passivos e Patrimônio Líquido** on the right. Each group can open a group-level audit via `onAuditGroup`.
