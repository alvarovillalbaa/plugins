---
name: aeo
description: Use for answer-engine optimization, FAQ coverage, concise answer blocks, entity clarity, and question-oriented content structure. Child of `discoverability`.
---

# AEO Answer Optimization

This child skill owns answer-engine optimization, FAQ coverage, concise answer blocks, entity clarity, and question-oriented content structure. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about answer-engine optimization, FAQ coverage, concise answer blocks, entity clarity, and question-oriented content structure.
- The parent router [`../discoverability/SKILL.md`](../discoverability/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `content`, `product-marketing/cro`, `frontend/performance`, `reporting` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `browserbase-search`: Use Browserbase search guidance for web discovery tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-search --agent codex`.
- `browserbase-fetch`: Use Browserbase fetch guidance for web retrieval tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-fetch --agent codex`.
- `unslop`: Remove generic AI-writing tells while preserving meaning and voice. Install: `python3 scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python3 scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
