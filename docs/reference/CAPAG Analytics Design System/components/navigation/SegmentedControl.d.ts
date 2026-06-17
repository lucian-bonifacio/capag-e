import * as React from "react";

export interface SegmentedOption {
  /** Stable id returned by onChange. */
  id: string;
  /** Visible label. */
  label: React.ReactNode;
  /** Optional leading icon. */
  icon?: React.ReactNode;
}

export interface SegmentedControlProps {
  /** The choices, left to right. */
  options: SegmentedOption[];
  /** Currently selected option id (controlled). */
  value: string;
  /** Called with the next option id. */
  onChange?: (id: string) => void;
  /** @default "sm" */
  size?: "sm" | "md";
}

/**
 * Compact toggle between a few mutually-exclusive views (e.g. balance-sheet layout).
 * @startingPoint section="Navigation" subtitle="Segmented view toggle" viewport="320x60"
 */
export function SegmentedControl(props: SegmentedControlProps): JSX.Element;
