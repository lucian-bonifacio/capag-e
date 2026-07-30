import { ClipboardCheck } from "lucide-react";
import type { CSSProperties } from "react";
import { Switch } from "./Switch";
import "./AccountRow.css";
import { formatCurrency } from "../../lib/formatters";

export type AccountRowProps = {
  accountName: string;
  accountCode?: string;
  value: string | bigint;
  percentage?: number;
  isIncluded: boolean;
  onToggleInclude: (included: boolean) => void;
  onAudit: () => void;
  showSwitch?: boolean;
  statusLabel?: string;
  statusVariant?: "success" | "warning" | "danger";
  isLedgerMode?: boolean;
  depth?: number;
  isStructural?: boolean;
};

function toTitleCase(str: string) {
  return str
    .toLowerCase()
    .split(' ')
    .map((word) => {
      // Pequenas palavras de ligação não capitalizamos (exceto se for a primeira, mas para contas contábeis é ok)
      if (['e', 'de', 'da', 'do', 'das', 'dos', 'a', 'o', 'em', 'para', 'com', 'sem', 'por'].includes(word)) {
        return word;
      }
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(' ');
}

export function AccountRow({
  accountName,
  accountCode,
  value,
  percentage,
  isIncluded,
  onToggleInclude,
  onAudit,
  showSwitch = true,
  statusLabel,
  statusVariant,
  isLedgerMode = false,
  depth = 0,
  isStructural = false,
}: AccountRowProps) {
  const percentageStr = percentage !== undefined ? `${percentage.toFixed(1).replace(".", ",")}%` : "";
  const indentation = `${Math.min(Math.max(depth, 0), 6) * 16}px`;

  return (
    <div
      className={`account-row ${!isIncluded ? "account-row-excluded" : ""} ${isLedgerMode ? "account-row-ledger" : ""} ${isStructural ? "account-row-structural" : ""}`}
      style={{ "--account-row-indent": indentation } as CSSProperties}
    >
      <div className="account-row-main">
        <span className="account-row-name">
          {toTitleCase(accountName)}
          {statusLabel && (
            <span className="status-badge" data-variant={statusVariant ?? "warning"}>
              {statusLabel}
            </span>
          )}
        </span>
        {accountCode && <span className="account-row-code tnum">{accountCode}</span>}
      </div>

      {isLedgerMode && percentageStr && (
        <div className="account-row-percentage tnum">{percentageStr}</div>
      )}

      <div className="account-row-value tnum">{formatCurrency(value)}</div>

      <div className="account-row-actions">
        {showSwitch && (
          <Switch
            checked={isIncluded}
            onChange={onToggleInclude}
            aria-label={`Incluir conta ${accountName}`}
            variant="soft"
          />
        )}
        <button
          type="button"
          className="button-ghost button-sm account-row-audit"
          onClick={onAudit}
          aria-label={`Auditar conta ${accountName}`}
        >
          <ClipboardCheck aria-hidden="true" size={16} />
        </button>
      </div>
    </div>
  );
}
