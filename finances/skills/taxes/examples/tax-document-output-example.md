# Example tax document output (excerpt)

## 1. Scope

- Tax year: `2025`
- Scope: founder household + side-business receipts
- Source folders: `~/Documents/tax-inbox`, Drive `Taxes/2025`
- Reviewer: outside CPA

## 2. Inventory

| Category | Document Name | Status | Source | Path / Link | Notes |
|----------|---------------|--------|--------|-------------|-------|
| `W-2 (Wages)` | `2025-W2-acme.pdf` | `found` | inbox folder | `Taxes/2025/01-income/2025-W2-acme.pdf` | employer name matched |
| `1099 (Income)` | `stripe-1099k-2025.pdf` | `found` | Gmail attachment | Drive link | merchant settlement |
| `Receipts & Expenses` | `aws-receipts-q4.zip` | `found` | Drive | Drive link | needs unzip before CPA review |
| `Charitable Donations` | — | `likely_missing` | not found | — | prior year had 3 donation receipts |

## 3. Likely Missing Items

| Category | Why It May Apply | Current Status | Next Check |
|----------|------------------|----------------|------------|
| `Medical Expenses` | HSA contributions seen in payroll export | `likely_missing` | ask payroll provider / HSA portal |
| `Investment Records` | brokerage transfers in bank feed | `likely_missing` | download year-end brokerage statement |

## 4. Duplicate Or Unclear Items

| Document | Issue | Action |
|----------|-------|--------|
| `1099-nec-final.pdf` and `1099-nec-corrected.pdf` | likely superseded duplicate | confirm corrected copy is authoritative |
| `receipt-021.jpg` | unreadable photo | rescan or replace with PDF |
