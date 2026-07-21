import { useState, type ReactNode } from "react";
import { ChevronDown, ChevronRight, ClipboardCheck } from "lucide-react";
import { formatCurrency } from "../../lib/formatters";
import "./BalanceGroup.css";

type BalanceGroupProps = {
  groupName: string;
  accountCount: number;
  totalValue: string | bigint;
  percentage?: number;
  onAuditGroup: () => void;
  children: ReactNode;
  defaultOpen?: boolean;
  isLedgerMode?: boolean;
};

export function BalanceGroup({
  groupName,
  accountCount,
  totalValue,
  percentage,
  onAuditGroup,
  children,
  defaultOpen = true,
  isLedgerMode = false,
}: BalanceGroupProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const percentageStr =
    percentage !== undefined ? `${percentage.toFixed(0).replace(".", ",")}%` : "";

  return (
    <div className={`balance-group ${isLedgerMode ? "balance-group-ledger" : ""}`}>
      <header className="balance-group-header">
        <button
          type="button"
          className="balance-group-toggle"
          onClick={() => setIsOpen((prev) => !prev)}
          aria-expanded={isOpen}
        >
          {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          <div className="balance-group-title">
            <strong>{groupName}</strong>
            {isLedgerMode ? (
              <span className="balance-group-count"> - {accountCount} contas</span>
            ) : (
              <span className="balance-group-count">{accountCount} contas</span>
            )}
          </div>
        </button>

        {isLedgerMode ? (
          <>
            <span className="balance-group-percentage tnum">{percentageStr}</span>
            <strong className="balance-group-total tnum">{formatCurrency(totalValue)}</strong>
            <div className="balance-group-actions">
              <button
                type="button"
                className="button-ghost button-sm balance-group-audit"
                onClick={onAuditGroup}
                aria-label={`Auditar grupo ${groupName}`}
              >
                <ClipboardCheck aria-hidden="true" size={16} />
              </button>
            </div>
          </>
        ) : (
          <div className="balance-group-meta">
            {percentageStr && <span className="balance-group-percentage tnum">{percentageStr}</span>}
            <strong className="balance-group-total tnum">{formatCurrency(totalValue)}</strong>
            <button
              type="button"
              className="button-ghost button-sm balance-group-audit"
              onClick={onAuditGroup}
              aria-label={`Auditar grupo ${groupName}`}
            >
              <ClipboardCheck aria-hidden="true" size={16} />
            </button>
          </div>
        )}
      </header>
      
      {isOpen && <div className="balance-group-content">{children}</div>}
    </div>
  );
}
