---
name: model-scenarios
description: Build, review, or extend a financial model and produce scenario outputs using the finances skill.
argument-hint: "[business model, spreadsheet, or scenario question]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skills: **planning** and **quantitative**.

1. **Gather the model context** – Ask for the business type, stage, key drivers, historicals, or existing spreadsheet.
2. **Confirm the scenarios** – Define base, upside, downside, or any named scenarios the user wants.
3. **Build or review the model** – Produce assumptions, formula logic, scenario outputs, and structural notes on how the model ties together.
4. **Call out risks** – Highlight inconsistent assumptions, formula risk, broken ties to actuals, or model blind spots.
5. **Deliver** – Output the scenario view, assumptions table, and the few sensitivities that actually drive the result.

## Boundary

This command owns forward-looking models and scenarios. It does not reconcile books or alter source-of-record financial data.
