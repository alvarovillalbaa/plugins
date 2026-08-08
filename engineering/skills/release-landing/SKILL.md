---
name: release-landing
description: Use for engineering release landing, merge hygiene, deployment gates, hotfixes, tags, and rollback posture. Child of `agentic-development`.
---

# Release Landing

This child skill owns engineering release landing, merge hygiene, deployment gates, hotfixes, tags, and rollback posture. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about engineering release landing, merge hygiene, deployment gates, hotfixes, tags, and rollback posture.
- The parent router [`../agentic-development/SKILL.md`](../agentic-development/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `frontend`, `backend`, `quality-assurance`, `code-documentation`, `cloud`, `prs`, `plugins-management` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `codex-loop`: Run Codex PRD/story loops with one fresh subagent per story. Install: `python3 scripts/install-external-skills.py --skill codex-loop --agent codex`.
- `claude-loop`: Run Claude PRD/story loops with one fresh subagent per story. Install: `python3 scripts/install-external-skills.py --skill claude-loop --agent codex`.
- `ralph`: Use Ralph-style autonomous execution loops for scoped implementation plans. Install: `python3 scripts/install-external-skills.py --skill ralph --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python3 scripts/install-external-skills.py --skill no-mistakes --agent codex`.
- `clous-sdk-release`: Use Clous-owned SDK release guidance for package and release workflows. Install: `python3 scripts/install-external-skills.py --skill clous-sdk-release --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
