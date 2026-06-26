# Tax Document Ops

Use this reference when the user needs a tax-document inventory, missing-item
checklist, or a cleaner filing package for an advisor.

## Goal

Produce a reviewable year-specific package that shows what documents exist,
what is probably missing, and where each item lives.

## Suggested Folder Structure

Use a stable pattern such as:

`Taxes/<YYYY>/`

Suggested subfolders:

- `01-income`
- `02-deductions`
- `03-business`
- `04-investments`
- `05-property-and-insurance`
- `06-medical-and-dependents`
- `07-correspondence`
- `08-review`

## Common Categories

Use filename and source context to classify:

- `W-2 (Wages)`
- `1099 (Income)`
- `1098 (Deductions)`
- `Receipts & Expenses`
- `Charitable Donations`
- `Medical Expenses`
- `Property Tax`
- `Mortgage Interest`
- `Investment Records`
- `Business/Self-Employment`
- `Education/Dependents`
- `Insurance`
- `State & Local Tax`
- `Retirement`
- `Uncategorized`

## Review Rules

Always flag:

- duplicate files
- unreadable or password-protected files
- files without clear year or issuer context
- categories that are missing but plausibly applicable
- mixed-year folders

Be careful with missing-document language. Say `likely missing` or
`not found in the current folder` instead of claiming the user definitely
needs the item.

## Checklist Status Values

Use:

- `found`
- `likely_missing`
- `duplicate`
- `needs_review`
- `not_applicable`

## Script Use

Use `scripts/tax_document_inventory.py` when the user has a local folder of tax
documents. It is non-destructive: it scans and categorizes files, then emits a
JSON or Markdown inventory without moving anything.
