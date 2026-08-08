---
name: reporting
description: Route reporting and content audits while directly owning pentest findings, evidence packaging, severity calibration, remediation guidance, and disclosure communication.
---

# Reporting Router

## Children

- [`content-audit`](../content-audit/SKILL.md) - Content Audit work.

## Route

| Request | Use |
| --- | --- |
| content audit requests | [`content-audit`](../content-audit/SKILL.md) |
| Pentest findings, evidence packaging, severity calibration, remediation guidance, or disclosure communication | Handle directly with this skill |

## Pentest Reporting Workflow

1. Confirm the signed engagement scope, affected targets, dates, and audience.
2. Inventory stored evidence and run `scripts/check_pentest_evidence.sh` before drafting.
3. Calibrate severity consistently and distinguish verified impact from plausible risk.
4. Use `templates/full-pentest-report.md` or `scripts/pentest_report_generator.py` for a complete report structure.
5. Include reproduction steps, evidence handles, affected assets, remediation, retest status, and responsible-disclosure constraints.
6. Never invent evidence or silently omit missing proof; label unsupported or unevaluated claims explicitly.

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `research`
- `finances`
- `product-development`
- `pentest`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
