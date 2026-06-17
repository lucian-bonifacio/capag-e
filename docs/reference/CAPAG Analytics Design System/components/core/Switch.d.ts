import * as React from "react";

export interface SwitchProps {
  /** On/off state (controlled). */
  checked?: boolean;
  /** Called with the next boolean state. */
  onChange?: (next: boolean) => void;
  disabled?: boolean;
  /** @default "md" */
  size?: "sm" | "md";
  /** Visual emphasis of the "on" state. "soft" is a translucent blue, less attention-grabbing (used in balance account rows). @default "solid" */
  tone?: "solid" | "soft";
  "aria-label"?: string;
}

/** Toggle for including/excluding an account from CAPAG calculations. */
export function Switch(props: SwitchProps): JSX.Element;
