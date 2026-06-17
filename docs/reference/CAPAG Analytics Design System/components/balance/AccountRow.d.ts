import * as React from "react";

export interface AccountRowProps {
  /** Account name, e.g. "Caixa e Equivalentes". */
  name: React.ReactNode;
  /** Account code, e.g. "1.1.1.01". */
  code?: React.ReactNode;
  /** Formatted value, e.g. "R$ 4.210.500,00". */
  value: React.ReactNode;
  /** Whether the account is included in CAPAG calculations. @default true */
  included?: boolean;
  /** Toggle include/exclude. Receives the next boolean. */
  onToggle?: (next: boolean) => void;
  /** Open the analytical audit for this account. */
  onAudit?: () => void;
}

/** A single contábil account row: name, value, include/exclude Switch, audit action. */
export function AccountRow(props: AccountRowProps): JSX.Element;
