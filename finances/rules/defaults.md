# Finances — Operating Defaults & Routing Rules

Runtime-neutral policy for the Finances plugin. These rules apply to every finance skill and agent. Platform safety requirements and the user's explicitly authorized scope take precedence; narrower skills may add compatible implementation detail but may not relax the authorization gates or contradict the ownership boundaries below.

## Department boundary

Finances owns bookkeeping, reconciliation, planning/FP&A, taxes, fundraising, fiscal close, financial analysis, pricing economics, and financial guardrails. Product owns packaging and pricing strategy; Sales owns quota/territory operations and applies approved prices or discounts to deals; Engineering owns billing UX and payment integrations. Finances validates the economics and records the results without taking over product or go-to-market decisions.

## Routing constraints

Route to the **narrowest** owning skill. The `finances` router selects children; chain when a request crosses lanes.

| Request shape | Route to |
| --- | --- |
| Categorize/monitor spend, burn | `expenses` |
| Match transactions, close books | `reconciliation`, `fiscal-close` |
| Budgets, forecasts, scenarios | `planning`, `quantitative` |
| Tax prep, filing, compliance | `taxes` |
| Raise process, investor materials, cap table | `fundraising` |
| Statement review, unit economics, valuation inputs, business quality | `fundamentals` |
| Pricing economics, margin impact, discount guardrails | `fundamentals`, `planning`, `quantitative` |
| Rates/inflation/FX context, market regime, scenario framing | `macro` |
| Modeling, portfolio metrics, statistical decision support | `quantitative` |

When the same task needs both a number and a narrative (for example, an investor update), chain `quantitative`/`fundamentals` for the figures and `productivity/reporting`/`fundraising` for the message.

## Operating defaults

- **Cite the source of every figure.** Tie numbers to a ledger, statement, model cell, or named document. Never invent or estimate financial figures without flagging the assumption.
- **State period, currency, and basis** (cash vs. accrual) on any output. Convert relative dates to absolute dates.
- **Show the math.** Make assumptions, drivers, and formulas explicit and auditable — no black-box outputs.
- **Round consistently** and keep precision appropriate to the decision; do not imply false precision.
- **Context is supplied, not embedded.** Pull entity, fiscal calendar, accounts, targets, and other organization-specific facts from user-provided or workspace-local sources; never hardcode them into reusable rules.
- **Default tone** is precise, conservative, and decision-oriented. Lead with the answer and the so-what, then the supporting detail.

## Authorization gates

The request may authorize analysis and preparation. Confirm exact amounts, targets, and records at the point of action before committing money movement, books-of-record changes, filings, or external communications.

- **Money movement and bookings**: preview journal entries, ledger edits, payments, and reconciliation changes; commit only when the exact action is authorized and the destination is verified.
- **External financial communications**: draft by default. Sending to investors, auditors, tax authorities, banks, or other external parties requires explicit authorization for the final content and recipients.
- **Tax and compliance filings**: prepare and validate, but submit only through an authorized accountable person or approved filing workflow.
- **Forward-looking statements**: label projections, scenarios, and assumptions clearly as estimates, not facts.
- **Sensitive data**: treat financials, cap tables, and PII as confidential. Do not paste into third-party tools that publish, cache, or index content.

## Quality bar

- Reconcile before reporting — if inputs do not tie out, surface the discrepancy rather than papering over it.
- Distinguish actuals from forecasts and one-offs from recurring in every summary.
- Prefer one well-sourced number over several unsourced ones. When uncertain, give a range and name the driver of the uncertainty.
