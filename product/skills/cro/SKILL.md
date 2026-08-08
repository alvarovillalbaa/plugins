---
name: cro
description: Use for conversion-rate optimization for pages and funnels, page diagnostics, CTA promises, proof placement, and test ideas. Child of `product-marketing`.
---

# Cro

This child skill owns conversion-rate optimization for pages and funnels, page diagnostics, CTA promises, proof placement, and test ideas. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about conversion-rate optimization for pages and funnels, page diagnostics, CTA promises, proof placement, and test ideas.
- The parent router [`../product-marketing/SKILL.md`](../product-marketing/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `content`, `discoverability`, `go-to-market`, `frontend`, `reporting` when the task crosses this child's boundary.
- Chain to [`../experiments/SKILL.md`](../experiments/SKILL.md) for sample sizing, statistical decision rules, and experiment execution; CRO owns the conversion hypothesis and page diagnosis, not a second statistics implementation.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `hallmark`: Audit, redesign, study, or build UI with anti-AI-slop design constraints. Install: `python3 scripts/install-external-skills.py --skill hallmark --agent codex`.
- `browserbase-ui-test`: Use Browserbase UI testing guidance for browser-level product verification. Install: `python3 scripts/install-external-skills.py --skill browserbase-ui-test --agent codex`.
- `userinterface-wiki`: Use interface-pattern references for layout, components, states, and product UI decisions. Install: `python3 scripts/install-external-skills.py --skill userinterface-wiki --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.

## Merged Sources

This skill preserves the former conversion-focused copy assets under `references/conversion-copy-source/`.
