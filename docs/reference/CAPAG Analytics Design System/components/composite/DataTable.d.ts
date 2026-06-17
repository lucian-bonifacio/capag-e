import * as React from "react";

export interface DataTableColumn {
  key: string;
  header: React.ReactNode;
  align?: "left" | "center" | "right";
  width?: number | string;
  /** Tabular numerals + right-friendly money column. */
  numeric?: boolean;
  /** Allow wrapping (default: nowrap). */
  wrap?: boolean;
  /** Custom cell renderer. */
  render?: (value: any, row: any) => React.ReactNode;
}

export interface DataTableProps {
  columns: DataTableColumn[];
  rows: any[];
  emptyText?: string;
}

/** Analytical table for AUDIT views only — place inside a Dialog or secondary screen. */
export function DataTable(props: DataTableProps): JSX.Element;
