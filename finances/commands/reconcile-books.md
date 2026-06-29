---
name: reconcile-books
description: Reconcile bank statements, receipts, and ledger rows into auditable outputs using the finances skill.
argument-hint: "[statements, receipts, or reconciliation context]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **finances** — `skills/finances/SKILL.md`, focusing on **Mode 1:
Reconciliation** and the references under `skills/finances/references/`.

1. **Gather the finance inputs** – Ask for statements, transaction exports, receipts, and desired output format.
2. **Normalize the data** – Extract or structure transactions into a consistent row format with ISO dates, entity, and currency.
3. **Reconcile the sources** – Match receipts, compare both sides, and classify every exception as timing, adjustment required, or investigate.
4. **Prepare the audit view** – Produce the structured output, reconciling items table, journal-entry queue, and unresolved follow-up list.
5. **Deliver** – Output reconciled rows, summary stats, aging/escalation notes, and the items that still need human confirmation.
