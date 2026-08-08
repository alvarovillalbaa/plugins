---
name: user-stories
description: Use for user stories, acceptance criteria, epic breakdown, story point estimation, sprint planning, and Definition of Done. Child of `product-development`.
---

# User Stories

This child skill owns user stories, acceptance criteria, epic breakdown, story point estimation, sprint planning, and Definition of Done. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about user stories, acceptance criteria, epic breakdown, story point estimation, sprint planning, and Definition of Done.
- The parent router [`../product-development/SKILL.md`](../product-development/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `product-marketing`, `frontend/onboarding-flows`, `quality-assurance/testing`, `quality-assurance`, `code-documentation`, `reporting` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.
- Keep stories acceptance-focused. Do not encode payload transformations, compatibility shims, or implementation facades as acceptance criteria.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `codex-loop`: Run Codex PRD/story loops with one fresh subagent per story. Install: `python3 scripts/install-external-skills.py --skill codex-loop --agent codex`.
- `claude-loop`: Run Claude PRD/story loops with one fresh subagent per story. Install: `python3 scripts/install-external-skills.py --skill claude-loop --agent codex`.
- `ralph-prd`: Use Ralph PRD guidance for product-spec structure before execution loops. Install: `python3 scripts/install-external-skills.py --skill ralph-prd --agent codex`.
- `ralph-playbook`: Reference-only: Use as Ralph playbook context for PRD-to-execution loops. No installer target.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
