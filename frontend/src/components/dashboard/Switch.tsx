import "./Switch.css";

type SwitchProps = {
  checked: boolean;
  onChange: (checked: boolean) => void;
  "aria-label": string;
  size?: "sm" | "md";
  variant?: "solid" | "soft";
  disabled?: boolean;
};

export function Switch({
  checked,
  onChange,
  "aria-label": ariaLabel,
  size = "sm",
  variant = "soft",
  disabled = false,
}: SwitchProps) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={ariaLabel}
      disabled={disabled}
      className={`custom-switch custom-switch-${size} custom-switch-${variant}`}
      onClick={() => onChange(!checked)}
    >
      <span className="custom-switch-thumb" />
    </button>
  );
}
