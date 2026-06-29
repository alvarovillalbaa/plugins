# Close Management

This reference adds structured month-end close operations adapted from the
`close-management` skill.

## Standard 5-Day Close Checklist

### Pre-Close

- send close calendar and deadline reminders
- confirm cut-off procedures with AP, AR, payroll, and treasury
- verify ERP, payroll, and banking systems are operating normally
- complete preliminary bank reconciliation
- review likely accruals and unusual transactions

### T+1

- finalize cash receipts and disbursements
- run AP accruals
- post payroll and payroll accruals
- post intercompany activity
- complete final bank reconciliation
- run depreciation and prepaid amortization

### T+2

- post revenue recognition and deferred revenue adjustments
- post remaining accruals
- complete AR and AP subledger reconciliations
- record inventory or FX adjustments if applicable
- begin balance sheet reconciliations

### T+3

- complete balance sheet reconciliations
- post adjusting entries from reconciliations
- complete intercompany reconciliation and eliminations
- run preliminary trial balance and preliminary flux analysis
- resolve material variances

### T+4

- post tax provision
- complete equity roll-forward
- finalize entries for soft close
- generate draft financial statements
- perform detailed flux analysis
- run management review

### T+5

- post final review adjustments
- hard close and lock the period
- distribute reporting package
- update forecast with actuals
- run the retrospective

## Dependency Levels

Use dependency levels so close work can run in parallel where possible.

### Level 1

Can start immediately:

- cash posting
- bank statement retrieval
- payroll processing
- depreciation
- prepaid amortization
- AP accrual prep
- intercompany transaction posting

### Level 2

Depends on Level 1 completion:

- bank reconciliation
- revenue recognition
- AR reconciliation
- AP reconciliation
- FX revaluation
- remaining accrual JEs

### Level 3

Depends on Level 2:

- balance sheet reconciliations
- intercompany reconciliation
- adjusting entries from reconciliations
- preliminary trial balance

### Level 4

Depends on Level 3:

- tax provision
- equity roll-forward
- consolidation and eliminations
- draft financial statements
- preliminary flux analysis

### Level 5

Depends on Level 4:

- management review
- final adjustments
- hard close and period lock
- reporting package
- forecast update

## Status Board Schema

Track:

- task
- owner
- deadline
- status
- dependency
- blocker
- notes

Recommended status set:

- `not_started`
- `in_progress`
- `complete`
- `blocked`
- `at_risk`

## Close Metrics

Track over time:

- close duration in business days
- adjusting entries after soft close
- late tasks
- reconciliation exceptions
- corrections or restatements after close

## Accelerated 3-Day Close

### Prerequisites

- recurring JEs are automated
- reconciliations are continuous during the month
- intercompany elimination is largely automated
- pre-close work is finished before month-end
- owners are clear and empowered
- core subsystems are near real time

### Typical 3-Day Shape

- `T+1`: all JEs posted, subledger recs complete, bank rec complete,
  intercompany rec complete, preliminary trial balance
- `T+2`: balance sheet recs, tax provision, consolidation, draft financials,
  flux analysis, management review
- `T+3`: final adjustments, hard close, reporting package, forecast update

## Bottlenecks To Watch

- late AP accruals
- manual recurring entries
- reconciliations started from scratch every month
- intercompany confirmations arriving late
- management review discovering basic issues too late
- missing support documents

## Retrospective Questions

- what went well and should stay the same
- what took longer than expected and why
- what blocker repeated this month
- what variance should have been caught earlier
- what can be automated before next close
