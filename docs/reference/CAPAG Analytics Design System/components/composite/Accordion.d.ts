import * as React from "react";

export interface AccordionProps {
  title: React.ReactNode;
  /** Right-aligned meta (counts, totals, percent). */
  meta?: React.ReactNode;
  /** Uncontrolled initial open state. */
  defaultOpen?: boolean;
  /** Controlled open state (with onToggle). */
  open?: boolean;
  onToggle?: (next: boolean) => void;
  children?: React.ReactNode;
}

export interface ChevronProps {
  open?: boolean;
}

/** Generic collapsible container; base for balance-sheet groups. */
export function Accordion(props: AccordionProps): JSX.Element;
export function Chevron(props: ChevronProps): JSX.Element;
