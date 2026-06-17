import * as React from "react";

export interface LedgerAccount {
  id: string;
  name: string;
  code?: string;
  /** Formatted value, e.g. "R$ 1.200.000,00". */
  value: string;
  included?: boolean;
}

export interface LedgerGroupData {
  id: string;
  name: string;
  total: string;
  percent?: string;
  contas: LedgerAccount[];
}

export interface BalanceLedgerProps {
  /** Small label above the section, e.g. "Aplicações". */
  eyebrow?: string;
  /** Section title, e.g. "Ativos". */
  title?: string;
  /** Formatted section total. */
  total?: string;
  /** Groups (macrogrupos) to render. */
  groups: LedgerGroupData[];
  /** Map of account id → included. If omitted, each account's own `included` is used. */
  state?: Record<string, boolean>;
  /** Called when an account switch toggles: (accountId, nextIncluded). */
  onToggle?: (id: string, next: boolean) => void;
  /** Open the analytic audit for an account: (account, group). */
  onAudit?: (account: LedgerAccount, group: LedgerGroupData) => void;
  /** Open the analytic audit for a whole group. */
  onAuditGroup?: (group: LedgerGroupData) => void;
  /** Group ids that start expanded. */
  defaultOpenIds?: string[];
}

/**
 * Single-column "livro-razão" view of a balance section — aligned columns,
 * uppercase macrogroups, indented accounts. Alternative to the two-column
 * BalanceGroup layout; pair with SegmentedControl to let users switch.
 * @startingPoint section="Balanço" subtitle="Ledger (single column) balance view" viewport="860x520"
 */
export function BalanceLedger(props: BalanceLedgerProps): JSX.Element;
