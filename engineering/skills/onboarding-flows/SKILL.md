---
name: onboarding-flows
description: Use for signup, onboarding, activation, empty states, checklists, tours, verification flows, and activation instrumentation. Child of `frontend`.
---

# Onboarding Flows

This child skill owns signup, onboarding, activation, empty states, checklists, tours, verification flows, and activation instrumentation. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about signup, onboarding, activation, empty states, checklists, tours, verification flows, and activation instrumentation.
- The parent router [`../frontend/SKILL.md`](../frontend/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `product-development`, `product-marketing`, `testing/frontend-e2e`, `images`, `visualization` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `hallmark`: Audit, redesign, study, or build UI with anti-AI-slop design constraints. Install: `python3 scripts/install-external-skills.py --skill hallmark --agent codex`.
- `taste-skill`: Use taste guidance for visual direction, hierarchy, and UI polish decisions. Install: `python3 scripts/install-external-skills.py --skill taste-skill --agent codex`.
- `userinterface-wiki`: Use interface-pattern references for layout, components, states, and product UI decisions. Install: `python3 scripts/install-external-skills.py --skill userinterface-wiki --agent codex`.
- `browserbase-ui-test`: Use Browserbase UI testing guidance for browser-level product verification. Install: `python3 scripts/install-external-skills.py --skill browserbase-ui-test --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
