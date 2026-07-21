import { ReactNode } from "react";
import { type LucideIcon } from "lucide-react";
import "./StatCard.css";

export type StatCardVariant = "neutral" | "primary" | "success" | "warning" | "danger";

type StatCardProps = {
  label: string;
  value: ReactNode;
  hint?: ReactNode;
  icon?: LucideIcon;
  variant?: StatCardVariant;
};

export function StatCard({ label, value, hint, icon: Icon, variant = "neutral" }: StatCardProps) {
  return (
    <article className={`stat-card stat-card-${variant}`}>
      <header className="stat-card-header">
        <h3 className="eyebrow">{label}</h3>
        {Icon ? <Icon aria-hidden="true" size={16} className="stat-card-icon" /> : null}
      </header>
      <div className="stat-card-content">
        <strong className="stat-card-value tnum">{value}</strong>
        {hint ? <div className="stat-card-hint">{hint}</div> : null}
      </div>
    </article>
  );
}
