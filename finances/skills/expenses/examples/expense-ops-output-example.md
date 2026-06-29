# Example expense ops output (excerpt)

## 1. Scope

- Reporting period: `2026-04-01` to `2026-04-24`
- Scope: US operating entity, corporate card + AP utility bills
- Base currency: USD
- Sources loaded: card export, Gmail receipts, `bills.json`

## 2. Spend Summary

| Metric | Value | Notes |
|--------|-------|-------|
| Total spend | $18,420 | Excludes payroll and tax remittances |
| Transaction count | 96 | 11 still in review |
| Largest category | software | 31% of spend |
| Largest transaction | $4,800 AWS invoice | Monthly infrastructure true-up |

## 4. Budget Status

| Budget | Actual | Variance | Variance % | Remaining / Daily Run Rate |
|--------|--------|----------|------------|-----------------------------|
| $20,000 | $18,420 | -$1,580 | -7.9% | $263/day through month-end |

## 5. Review Queue

| Item ID | Issue | Severity | Owner | Next Action | Evidence |
|---------|-------|----------|-------|-------------|----------|
| `txn-044` | Uncategorized `AMZN Mktp` charge | investigate | Ops | check receipt and apply merchant rule | [Drive/Receipts/2026-04] |
| `txn-071` | Possible duplicate Uber charge | review_now | Finance | confirm card auth vs settled transaction | [Bank feed] |
| `bill-utilities-2026-04` | Internet bill increased 18% | investigate | Finance | validate plan change before payment | [Invoice #8821] |

## 6. Upcoming Bills

| Bill | Due Date | Days Until Due | Amount | Autopay | Owner | Next Action |
|------|----------|----------------|--------|---------|-------|-------------|
| Rent | 2026-05-01 | 6 | $6,000 | no | CEO | queue ACH |
| Internet | 2026-04-28 | 3 | $420 | yes | Finance | confirm amount change |
| Figma | 2026-04-26 | 1 | $180 | yes | Ops | verify card limit |

## 7. Actions

- Immediate: confirm whether `txn-071` is a duplicate before booking April travel spend.
- This week: add merchant rule for Amazon marketplace charges split by memo or receipt.
- Before close: clear all 11 review items or carry them to the close blocker list.
