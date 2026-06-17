import * as React from "react";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
  /** Inner padding. @default "var(--space-6)" */
  padding?: string;
}

export interface CardHeaderProps {
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  /** Right-aligned action area (buttons, etc). */
  action?: React.ReactNode;
  style?: React.CSSProperties;
}

export interface StatCardProps {
  /** Uppercase eyebrow label, e.g. "Liquidez Corrente". */
  label: React.ReactNode;
  /** Large value, e.g. "1,84" or "B". */
  value: React.ReactNode;
  /** Optional supporting line under the value. */
  hint?: React.ReactNode;
  /** Value color. @default "neutral" */
  tone?: "neutral" | "primary" | "success" | "warning" | "danger";
  icon?: React.ReactNode;
  style?: React.CSSProperties;
}

/** White surface container with soft border. */
export function Card(props: CardProps): JSX.Element;
export function CardHeader(props: CardHeaderProps): JSX.Element;
/** KPI / indicator tile for the dashboard top row. */
export function StatCard(props: StatCardProps): JSX.Element;
