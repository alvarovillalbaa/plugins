# Reporting — Routing Guide

Router for all reporting work. Routes to the appropriate reporting skill.

## When to Use This Skill Directly

- Building a new recurring report from scratch.
- Auditing report quality across the team.
- Deciding which report type fits a stakeholder need.

## Report Type Decision Matrix

| Stakeholder | Cadence | Report Type | Skill |
|-------------|---------|-------------|-------|
| CEO/Board | Weekly/Monthly | Executive summary | handle directly |
| Marketing | Weekly | Growth metrics | handle directly |
| Engineering | Sprint | Velocity and incidents | handle directly |
| Finance | Monthly | P&L and cash | finances/fiscal-close |
| Product | Weekly | Experiment results | product/experiments |

## Routing Decision Tree

```
Is this a code quality or PR review report?
  → code-review

Is this a content quality audit?
  → content-audit

Is this a design quality review?
  → design-review

Is this a market research report?
  → market-competitor-research

Is this a financial performance report?
  → finances plugin

Is this a general operational/executive report?
  → handle directly
```

## Reporting Standards

- **Lead with the headline**: Open with the most important finding, not background.
- **Context before data**: Explain what the number means before showing the number.
- **Action-oriented**: Every report ends with recommended actions, not just observations.
- **Data freshness**: Note the data cutoff date in every report.
- **Concise by default**: Aim for 1-page summaries; appendix for detail.
