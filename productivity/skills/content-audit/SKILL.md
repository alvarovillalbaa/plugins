---
name: content-audit
description: Use for content audits, quality checks, decay diagnosis, content refresh plans, and publishing quality gates. Child of `reporting`.
---

# Content Audit

This child skill owns content audits, quality checks, decay diagnosis, content refresh plans, and publishing quality gates. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about content audits, quality checks, decay diagnosis, content refresh plans, and publishing quality gates.
- The parent router [`../reporting/SKILL.md`](../reporting/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `discoverability/geo`, `seo`, `social-media`, `product-marketing` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
