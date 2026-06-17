import * as React from "react";

export interface BalanceGroupProps {
  /** Group name, e.g. "Ativo Circulante". */
  name: React.ReactNode;
  /** Number of accounts in the group. */
  count: number;
  /** Formatted total value, e.g. "R$ 21.430.000,00". */
  total: React.ReactNode;
  /** Share of the side total, e.g. "44%". */
  percent?: React.ReactNode;
  /** Uncontrolled initial open state. @default true */
  defaultOpen?: boolean;
  /** Controlled open state (with onToggle). */
  open?: boolean;
  onToggle?: (next: boolean) => void;
  /** Open audit for the whole group. */
  onAuditGroup?: () => void;
  /** AccountRow children. */
  children?: React.ReactNode;
}

/**
 * Collapsible balance-sheet group: name, account count, total, percent, audit action.
 * @startingPoint section="Balanço" subtitle="Collapsible balance-sheet group" viewport="560x320"
 */
export function BalanceGroup(props: BalanceGroupProps): JSX.Element;
