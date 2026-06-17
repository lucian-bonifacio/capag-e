import * as React from "react";

export interface DialogProps {
  open: boolean;
  onClose?: () => void;
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  /** Right-aligned footer actions. */
  footer?: React.ReactNode;
  /** Max panel width in px. @default 720 */
  width?: number;
  children?: React.ReactNode;
}

/** Modal overlay for audit detail and other secondary views. */
export function Dialog(props: DialogProps): JSX.Element | null;
