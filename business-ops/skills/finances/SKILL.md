---
name: finances
description: >-
  Router for expense and bill ops, reconciliation, financial planning, taxes,
  fundraising, month-end close, quantitative analysis, fundamentals
  analysis, and macro analysis.
---

# Finances Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`expense-bill-ops`](../expense-bill-ops/SKILL.md) - expense operations, bill monitoring, receipt intake, categorization, recurring bill calendars, and spend alerts
- [`reconciliation`](../reconciliation/SKILL.md) - bank reconciliation, GL/subledger tie-outs, receipt matching, variance explanation, and evidence tracking
- [`financial-planning`](../financial-planning/SKILL.md) - financial planning, CFO briefings, burn/runway, scenario models, budgets, forecasts, and board-ready finance narratives
- [`taxes`](../taxes/SKILL.md) - tax document readiness, evidence packaging, tax-year checklists, entity scoping, and filing-prep organization
- [`fundraising`](../fundraising/SKILL.md) - fundraising finance support, diligence materials, investor data rooms, process diagnostics, and finance-backed investor answers
- [`month-end-close`](../month-end-close/SKILL.md) - month-end close calendars, owners, blockers, dependencies, close dashboards, T+ cadences, and accelerated close work
- [`quantitative-analysis`](../quantitative-analysis/SKILL.md) - quantitative finance analysis, modeling, portfolio metrics, statistical analysis, and structured numerical decision support
- [`fundamentals-analysis`](../fundamentals-analysis/SKILL.md) - fundamental company analysis, financial statement review, unit economics, valuation inputs, and business quality assessment
- [`macro-analysis`](../macro-analysis/SKILL.md) - macro analysis, market regime review, rates/inflation/currency context, sector-level implications, and scenario framing

## Route

| User asks for | Use |
| --- | --- |
| expense operations, bill monitoring, receipt intake, categorization, recurring bill calendars, and spend alerts | [`expense-bill-ops`](../expense-bill-ops/SKILL.md) |
| bank reconciliation, GL/subledger tie-outs, receipt matching, variance explanation, and evidence tracking | [`reconciliation`](../reconciliation/SKILL.md) |
| financial planning, CFO briefings, burn/runway, scenario models, budgets, forecasts, and board-ready finance narratives | [`financial-planning`](../financial-planning/SKILL.md) |
| tax document readiness, evidence packaging, tax-year checklists, entity scoping, and filing-prep organization | [`taxes`](../taxes/SKILL.md) |
| fundraising finance support, diligence materials, investor data rooms, process diagnostics, and finance-backed investor answers | [`fundraising`](../fundraising/SKILL.md) |
| month-end close calendars, owners, blockers, dependencies, close dashboards, T+ cadences, and accelerated close work | [`month-end-close`](../month-end-close/SKILL.md) |
| quantitative finance analysis, modeling, portfolio metrics, statistical analysis, and structured numerical decision support | [`quantitative-analysis`](../quantitative-analysis/SKILL.md) |
| fundamental company analysis, financial statement review, unit economics, valuation inputs, and business quality assessment | [`fundamentals-analysis`](../fundamentals-analysis/SKILL.md) |
| macro analysis, market regime review, rates/inflation/currency context, sector-level implications, and scenario framing | [`macro-analysis`](../macro-analysis/SKILL.md) |

## Chain Rules

- `reporting`
- `research`
- `product-marketing`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
