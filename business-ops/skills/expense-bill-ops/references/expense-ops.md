# Expense Operations

Use this reference when the task is about day-to-day spend intake, transaction
categorization, budget monitoring, bill monitoring, or recurring bill reminders.

## Default Operating Cadence

If the user does not specify a cadence, use:

- daily 20:00 local time for new receipt and bank-notification intake
- weekly Sunday 18:00 local time for spend summary and budget review
- weekly Monday 08:00 local time for bill monitoring
- daily 09:00 local time for bills due within the next `3-7` days during active AP review windows

Override the cadence when AP, treasury, or household-finance routines already
exist.

## Canonical Schemas

### Expense row

| Field | Notes |
|-------|-------|
| `date` | Normalize to `YYYY-MM-DD` |
| `description` | Original merchant or bank text |
| `merchant` | Cleaned vendor name when known |
| `amount` | Signed numeric value in base currency or alongside `currency` |
| `currency` | Required if not already normalized |
| `account` | Card, bank, cash, or payable source |
| `category` | One of the controlled categories below |
| `source` | Receipt, bank feed, invoice, manual entry |
| `receipt_link` | File or evidence link when available |
| `invoice_id` | Optional vendor reference |
| `is_recurring` | `true` for subscriptions and scheduled bills |
| `status` | `new`, `review`, `approved`, `paid`, `reimbursable` |

### Recurring bill row

| Field | Notes |
|-------|-------|
| `name` | Bill/vendor name |
| `amount` | Expected amount |
| `currency` | Required if multi-currency |
| `due_day` or `due_date` | Monthly day number or explicit date |
| `autopay` | `true` / `false` |
| `owner` | Person accountable for payment |
| `category` | Utilities, rent, software, debt, etc. |
| `account` | Funding account or card |
| `status` | `scheduled`, `due`, `paid`, `blocked` |
| `last_seen_date` | Last statement or notice seen |
| `statement_link` | Link to statement, invoice, or email thread |

## Categorization Strategy

Use a deterministic-first approach:

1. exact merchant mapping
2. keyword rules on the cleaned description
3. prior approved category for the same merchant
4. manual review for the remainder

Do not silently guess categories for material transactions. Keep the review
queue visible until a human or a stable rule resolves it.

Useful baseline categories:

- `food`
- `transport`
- `utilities`
- `entertainment`
- `shopping`
- `health`
- `housing`
- `education`
- `subscription`
- `software`
- `professional_services`
- `payroll_related`
- `taxes_fees`
- `uncategorized`

## Anomaly And Review Rules

Always flag:

- exact or near-duplicate transactions
- unusually large amounts relative to the merchant or category history
- missing receipt or invoice support for controlled-spend environments
- recurring bills with changed amount versus expected amount
- new billers not seen in prior periods
- expected recurring billers missing from the current cycle
- expenses dated outside the requested reporting period

Recommended review statuses:

- `investigate`
- `needs_support`
- `duplicate_candidate`
- `budget_breach`
- `ready_to_post`

## Budget Monitoring

When a budget exists, compute:

- period actuals
- budget amount
- variance amount
- variance percent
- remaining spend capacity
- implied daily remaining spend if the period is still open

If no formal budget exists, compare against:

- prior period actuals
- rolling average
- runway or burn guardrail

## Reminder Windows For Bills

Default reminder severity:

| Window | Severity | Default action |
|--------|----------|----------------|
| `0-2` days | `urgent` | Notify owner immediately, confirm autopay or payment status |
| `3-7` days | `upcoming` | Queue reminder and verify amount/account |
| `8+` days | `watch` | No active escalation unless the user asks for long-horizon planning |

For monthly recurring bills, watch for month-end rollover edge cases:

- `due_day` exceeds days in month
- next due date falls on weekend or holiday
- amount changed without explanation

## Bill Calendar Build

When the task includes bills, organize them into:

- `overdue`
- `due_this_week`
- `due_this_month`
- `autopay_scheduled`

Search recent sources for:

- `bill`
- `statement`
- `amount due`
- `payment due`
- `invoice`
- `autopay`

Capture:

- biller name
- amount due
- due date
- autopay status
- payment confirmation, if any
- statement or email link

If autopay is unclear, assume manual attention is required.

## Suggested Workpaper Tabs

Use a canonical sheet when multiple rows or reviewers are involved:

- `bill_calendar`
- `expense_review_queue`
- `merchant_rules`
- `budget_vs_actual`

Keep raw imports in a separate tab and preserve formulas or validation in the
review tabs.

## Required Outputs

Use `templates/expense-ops-report.md` when the user needs a memo/report.

Minimum sections:

1. scope and source summary
2. totals and category rollup
3. budget status
4. review queue
5. upcoming bills
6. actions and owners

Use `examples/expense-ops-output-example.md` for tone and structure.
