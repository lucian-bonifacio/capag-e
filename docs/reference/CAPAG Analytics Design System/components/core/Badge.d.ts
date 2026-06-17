import * as React from "react";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Semantic color. @default "neutral" */
  variant?: "neutral" | "primary" | "success" | "warning" | "danger";
  children?: React.ReactNode;
}

/** Compact status / category label (pill). */
export function Badge(props: BadgeProps): JSX.Element;
