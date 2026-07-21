import { type ReactNode } from "react";
import { type LucideIcon } from "lucide-react";
import "./SegmentedControl.css";

export type SegmentedControlOption = {
  id: string;
  label: string;
  icon?: LucideIcon;
};

type SegmentedControlProps = {
  value: string;
  onChange: (id: string) => void;
  options: SegmentedControlOption[];
  "aria-label"?: string;
};

export function SegmentedControl({
  value,
  onChange,
  options,
  "aria-label": ariaLabel,
}: SegmentedControlProps) {
  return (
    <div
      className="segmented-control"
      role="radiogroup"
      aria-label={ariaLabel}
    >
      {options.map((option) => {
        const isSelected = option.id === value;
        const Icon = option.icon;

        return (
          <button
            key={option.id}
            type="button"
            role="radio"
            aria-checked={isSelected}
            className="segmented-control-item"
            data-selected={isSelected}
            onClick={() => onChange(option.id)}
          >
            {Icon ? <Icon aria-hidden="true" size={16} /> : null}
            <span>{option.label}</span>
          </button>
        );
      })}
    </div>
  );
}
