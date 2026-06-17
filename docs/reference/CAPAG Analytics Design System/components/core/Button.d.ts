import * as React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style. @default "primary" */
  variant?: "primary" | "secondary" | "ghost" | "danger";
  /** Control height. @default "md" */
  size?: "sm" | "md";
  disabled?: boolean;
  /** Element rendered before the label (icon). */
  iconLeft?: React.ReactNode;
  /** Element rendered after the label (icon). */
  iconRight?: React.ReactNode;
  children?: React.ReactNode;
}

/**
 * Primary administrative action button.
 * @startingPoint section="Core" subtitle="Buttons, badges, switches & inputs" viewport="700x320"
 */
export function Button(props: ButtonProps): JSX.Element;
