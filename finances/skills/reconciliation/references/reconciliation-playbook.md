# Reconciliation Playbook

This reference adds detail for reconciliation work.

## Reconciliation Types

### Bank Reconciliation

Compare bank statement balance to GL cash balance as of the same date.

Standard structure:

```text
Balance per bank statement
+ Deposits in transit
- Outstanding checks
+/- Bank errors
= Adjusted bank balance

Balance per GL
+ Interest or credits not recorded
- Bank fees not recorded
+/- GL errors
= Adjusted GL balance
Difference
```

### GL To Subledger

Compare the GL control account to the detailed subledger.

Common examples:

- AR control vs AR aging
- AP control vs AP aging
- fixed assets vs FA register
- inventory vs valuation report
- prepaid expenses vs amortization schedule
- accrued liabilities vs detail schedule

### Intercompany

Compare one entity's receivable to the counterparty payable and verify
eliminations.

## Common Causes Of Differences

- manual journal entries posted to the GL but not reflected in the subledger
- timing delays in interface or batch posting
- transactions recorded by one entity but not the other
- classification errors
- FX rate mismatches
- duplicates, omissions, or wrong-sign entries

## Exception Categories

### Timing Difference

Normal lag that should clear within the standard processing cycle.

Examples:

- outstanding checks
- deposits in transit
- pending approvals
- subsystem items not yet interfaced

### Adjustment Required

Needs a correcting entry or system fix.

Examples:

- unrecorded bank fees
- unrecorded interest
- duplicate entries
- wrong account or wrong amount
- missing entry in one system

### Investigate

The cause is not yet known or the item is stale enough to require escalation.

Examples:

- unexplained differences
- disputed items
- aged open items
- recurring unexplained variance

## Aging Guidance

Default buckets:

- `0-30 days`: current
- `31-60 days`: investigate
- `61-90 days`: escalate
- `90+ days`: management review

Track:

- amount
- originated date
- age in days
- category
- owner
- status

## Escalation Triggers

Adapt thresholds to the organization's materiality, but do not skip explicit
triggers. Default examples:

- large individual item
- large aggregate unresolved balance
- item older than 60 days
- item older than 90 days
- any unexplained close-blocking difference
- recurring growth over 3 or more periods

## Best Practices

- compare totals first, then drill into rows
- never reconcile across mixed periods or mixed entities
- keep preparer, reviewer, and evidence together
- do not carry open items forever without root-cause analysis
- if a difference repeats, propose a process fix, not just a month-end patch
