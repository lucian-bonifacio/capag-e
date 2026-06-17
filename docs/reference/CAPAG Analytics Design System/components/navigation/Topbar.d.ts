import * as React from "react";

export interface TopbarProps {
  title: React.ReactNode;
  /** Small text beside the title. */
  subtitle?: React.ReactNode;
  /** Optional breadcrumb line above the title. */
  breadcrumb?: React.ReactNode;
  /** Right-aligned actions (buttons, search, user). */
  actions?: React.ReactNode;
  style?: React.CSSProperties;
}

/** Simple top bar for the admin shell. */
export function Topbar(props: TopbarProps): JSX.Element;
