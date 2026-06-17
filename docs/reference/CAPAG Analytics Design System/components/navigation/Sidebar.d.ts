import * as React from "react";

export interface SidebarNavItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  /** Optional trailing count/badge. */
  badge?: React.ReactNode;
}

export interface SidebarProps {
  /** Brand label next to the logo mark. @default "CAPAG Analytics" */
  brand?: string;
  items: SidebarNavItem[];
  /** Id of the active item. */
  activeId?: string;
  onSelect?: (id: string) => void;
  /** Optional footer area (user, settings). */
  footer?: React.ReactNode;
  style?: React.CSSProperties;
}

/**
 * Fixed left navigation for the admin shell.
 * @startingPoint section="Navigation" subtitle="Fixed admin sidebar" viewport="260x560"
 */
export function Sidebar(props: SidebarProps): JSX.Element;
