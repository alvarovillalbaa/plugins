# Finances — Routing Guide

Router for all finance operations. Routes to specialist child skills.

## Child Skills

| Child | Owns |
|-------|------|
| `expenses` | Expense tracking, categorization, approval workflows |
| `reconciliation` | Bank reconciliation, account matching, variance analysis |
| `planning` | Annual operating plan, budgeting, forecasting |
| `taxes` | Tax filing, compliance, jurisdiction rules |
| `fundraising` | Investor outreach, pitch materials, cap table |
| `fiscal-close` | Month-end and year-end close process |
| `quantitative` | Financial modeling, statistical analysis, cohort analysis |
| `fundamentals` | P&L analysis, ratio analysis, financial health |
| `macro` | Macroeconomic analysis, market signals, context |

## Routing Decision Tree

```
Is this about tracking or categorizing company spending?
  → expenses

Is this about matching transactions or finding discrepancies?
  → reconciliation

Is this about budgets, forecasts, or the annual plan?
  → planning

Is this about tax compliance, filings, or deductions?
  → taxes

Is this about fundraising, investors, or cap table?
  → fundraising

Is this about closing the month or year?
  → fiscal-close

Is this about financial modeling or statistical analysis?
  → quantitative

Is this about reading financial statements or calculating ratios?
  → fundamentals

Is this about macroeconomic context or market signals?
  → macro
```

## Finance Data Handling Rules

- **No PII in shared files**: Customer financial data must not appear in shared skill outputs.
- **Approval thresholds**: Expenditures above $10K require CFO approval before commitment.
- **Source of truth**: Accounting system (QuickBooks/Xero) is authoritative — override spreadsheets.
- **Audit trail**: All financial entries must have a source document reference.
