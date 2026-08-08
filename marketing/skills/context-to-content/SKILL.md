---
name: context-to-content
description: Use for turning support tickets, customer questions, sales objections, and internal FAQs into content briefs and help articles. Child of `content`.
---

# Support To Content

This child skill owns turning support tickets, customer questions, sales objections, and internal FAQs into content briefs and help articles. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about turning support tickets, customer questions, sales objections, and internal FAQs into content briefs and help articles.
- The parent router [`../content/SKILL.md`](../content/SKILL.md) selects this child.
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
