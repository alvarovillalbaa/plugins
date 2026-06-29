---
name: polish
description: >-
  Use for UI polish, visual defects, layout fit, spacing, states, motion,
  interaction finish, and screenshot-based cleanup. Child skill of
  `design`; route here from the parent router when this lane is the
  narrowest owner.
---

# Ui Polish Review

This child skill owns UI polish, visual defects, layout fit, spacing, states, motion, interaction finish, and screenshot-based cleanup. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about UI polish, visual defects, layout fit, spacing, states, motion, interaction finish, and screenshot-based cleanup.
- The parent router [`../design/SKILL.md`](../design/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `product-development`, `product-marketing`, `quality-assurance/frontend-e2e`, `quality-assurance`, `code-documentation`, `images`, `visualization` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.
- Defer Fluid Functionalism polish details to the `fluid-functionalism` reference source when motion or hover behavior is in scope.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `hallmark`: Audit, redesign, study, or build UI with anti-AI-slop design constraints. Install: `python scripts/install-external-skills.py --skill hallmark --agent codex`.
- `redesign-skill`: Use redesign guidance for improving existing UI without broad product drift. Install: `python scripts/install-external-skills.py --skill redesign-skill --agent codex`.
- `impeccable`: Use impeccable UI quality guidance for execution-level frontend finish. Install: `python scripts/install-external-skills.py --skill impeccable --agent codex`.
- `emil-design-eng`: Use design-engineering taste rules for high-quality frontend implementation. Install: `python scripts/install-external-skills.py --skill emil-design-eng --agent codex`.
- `review-animations`: Review animation timing, easing, and intent against expert motion guidance. Install: `python scripts/install-external-skills.py --skill review-animations --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
