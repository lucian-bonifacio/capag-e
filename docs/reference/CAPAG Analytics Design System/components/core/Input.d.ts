import * as React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Icon shown inside, before the field (e.g. search glyph). */
  iconLeft?: React.ReactNode;
  /** @default "md" */
  size?: "sm" | "md";
  /** Style for the outer wrapper. */
  wrapperStyle?: React.CSSProperties;
}

/** Text / search input field with optional leading icon. */
export function Input(props: InputProps): JSX.Element;
