import { type ReactNode } from "react";
import "./BalanceLedger.css";

type BalanceLedgerProps = {
  children: ReactNode;
};

export function BalanceLedger({ children }: BalanceLedgerProps) {
  return (
    <div className="balance-ledger">
      <div className="balance-ledger-header">
        <span>CONTA</span>
        <span className="balance-ledger-col-perc">%</span>
        <span className="balance-ledger-col-value">VALOR</span>
        <span className="balance-ledger-col-include">INCLUIR</span>
      </div>
      <div className="balance-ledger-content">{children}</div>
    </div>
  );
}
