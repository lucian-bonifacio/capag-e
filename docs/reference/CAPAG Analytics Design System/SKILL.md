---
name: capag-analytics-design
description: Use this skill to generate well-branded interfaces and assets for CAPAG Analytics — an internal accounting/audit admin system (importação ECD, Balanço Patrimonial, indicadores CAPAG, auditoria analítica). Either for production or throwaway prototypes/mocks. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the `readme.md` file within this skill, and explore the other available files (token CSS under `tokens/`, components under `components/`, the dashboard UI kit under `ui_kits/dashboard/`, and the specimen cards under `guidelines/`).

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view — link `styles.css` for tokens and load `_ds_bundle.js` to mount components via `window.CAPAGAnalyticsDesignSystem_0c00db`. If working on production code, copy the token CSS and read the rules here to become an expert in designing with this brand (shadcn/ui + Tailwind + Inter, light theme).

Key rules to honor:
- Light theme only. No dark mode, no gradients, no strong shadows, no excess of color.
- Fixed palette (Slate neutrals + Blue primary + green/amber/red semantic accents). Do not change it without explicit request.
- Dashboard top shows **calculated indicators** (CAPAG, Liquidez, Endividamento, Poupança Corrente), not raw balance values.
- Balanço Patrimonial in two columns (Ativos | Passivos e PL) using collapsible groups, never a central table.
- Each account row has an include/exclude **switch** and an **audit** action (call it "Auditar conta" / "Ver auditoria", never "filtro").
- The analytical audit table appears only in a modal/dialog or secondary screen — never as the central dashboard block.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.
