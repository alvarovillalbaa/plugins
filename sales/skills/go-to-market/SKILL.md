---
name: go-to-market
description: >-
  Router for first-customer GTM, launch GTM, growth experimentation, technical
  sales, revenue intelligence, revenue ops, customer growth/retention, and
  commercial docs.
---

# Go To Market Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`first-customer-gtm`](../first-customer-gtm/SKILL.md) - first-customer selling, early wedge selection, founder-led sales, design partners, and first proof loops
- [`launch-gtm`](../launch-gtm/SKILL.md) - launch GTM planning, announcement motion, campaign sequencing, launch channels, and launch retrospectives
- [`growth-experimentation`](../growth-experimentation/SKILL.md) - growth experiments, channel tests, scoring, weekly growth loops, pacing alerts, and experiment readouts
- [`technical-sales`](../technical-sales/SKILL.md) - technical sales motions, solution fit, discovery-to-demo translation, technical objections, and proof-of-concept framing
- [`revenue-intelligence`](../revenue-intelligence/SKILL.md) - revenue intelligence, account signals, pipeline risk, opportunity analysis, forecast inputs, and buying committee insight
- [`revenue-ops`](../revenue-ops/SKILL.md) - revenue operations, CRM stages, lifecycle definitions, handoff rules, pipeline hygiene, and operating metrics
- [`customer-growth-retention`](../customer-growth-retention/SKILL.md) - customer growth, retention, expansion, churn-risk review, lifecycle nudges, and customer success GTM
- [`commercial-docs`](../commercial-docs/SKILL.md) - commercial documents, sales one-pagers, objection docs, mutual action plans, security questionnaires, and proposal support

## Route

| User asks for | Use |
| --- | --- |
| first-customer selling, early wedge selection, founder-led sales, design partners, and first proof loops | [`first-customer-gtm`](../first-customer-gtm/SKILL.md) |
| launch GTM planning, announcement motion, campaign sequencing, launch channels, and launch retrospectives | [`launch-gtm`](../launch-gtm/SKILL.md) |
| growth experiments, channel tests, scoring, weekly growth loops, pacing alerts, and experiment readouts | [`growth-experimentation`](../growth-experimentation/SKILL.md) |
| technical sales motions, solution fit, discovery-to-demo translation, technical objections, and proof-of-concept framing | [`technical-sales`](../technical-sales/SKILL.md) |
| revenue intelligence, account signals, pipeline risk, opportunity analysis, forecast inputs, and buying committee insight | [`revenue-intelligence`](../revenue-intelligence/SKILL.md) |
| revenue operations, CRM stages, lifecycle definitions, handoff rules, pipeline hygiene, and operating metrics | [`revenue-ops`](../revenue-ops/SKILL.md) |
| customer growth, retention, expansion, churn-risk review, lifecycle nudges, and customer success GTM | [`customer-growth-retention`](../customer-growth-retention/SKILL.md) |
| commercial documents, sales one-pagers, objection docs, mutual action plans, security questionnaires, and proposal support | [`commercial-docs`](../commercial-docs/SKILL.md) |

## Chain Rules

- `product-marketing`
- `product-development`
- `message-outreach`
- `sales-pipeline`
- `prospect-research`
- `research`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
