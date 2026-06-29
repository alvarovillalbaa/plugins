---
name: auto-improve
description: >-
  Route safe self-improvement work for skills, memories, second-brain content,
  and codebase experiment harnesses. Use when a user asks to improve installed
  skills, update skills from memories or second-brain data, classify local vs
  upstream skill changes, personalize skills without leaking private data, or
  run autoresearch-style improvement loops.
---

# Auto Improve Router

This skill is the public entry point for continuous improvement. Keep it thin:
it decides the lane, preserves source/runtime boundaries, and delegates depth
to the owner skill.

## Routes

| Request | Use |
| --- | --- |
| Improve skill prompts, references, scripts, examples, or evals | [`../skill-eval-loop/SKILL.md`](../skill-eval-loop/SKILL.md) |
| Curate or reconcile agent memories | [`../memory/SKILL.md`](../memory/SKILL.md) |
| Improve knowledge from a second-brain or raw sources | [`../brain/SKILL.md`](../brain/SKILL.md) and [`../ingestion/SKILL.md`](../ingestion/SKILL.md) |
| Personalize skills for a user or company | [`../personalize/SKILL.md`](../personalize/SKILL.md) |
| Run repeatable experiment loops | [`../loops/SKILL.md`](../loops/SKILL.md) |
| Improve repo agent harnesses or autoresearch references | [`../../../engineering/skills/agent-harness/SKILL.md`](../../../engineering/skills/agent-harness/SKILL.md) |

## Source And Runtime Rules

- Treat this repository, `alvarovillalbaa/plugins`, as the canonical upstream
  source for bundled skills.
- Treat installed folders under runtime homes such as `~/.codex/skills`,
  `~/.cursor`, `~/.openclaw`, and Claude plugin/cache locations as runtime
  installs. Never promote them to upstream without tracing provenance.
- Locate the nearest `.skillmeta.yml` before classifying an improvement. If no
  metadata exists, treat the target as local-only unless the user explicitly
  identifies an upstream source.
- Keep personalization overlay-only. Upstream receives templates, placeholder
  schemas, examples, and generic scripts, not rendered company or user data.
- Prefer patch bundles for external users and pull requests for authenticated
  maintainers. Never push directly to `main`.

## Tools

Use `scripts/skillctl.py` from the repo root for deterministic checks:

```bash
python3 scripts/skillctl.py meta check --root .
python3 scripts/skillctl.py trace-origin system/skills/auto-improve
python3 scripts/skillctl.py diff-classify --base origin/main --head HEAD --fail-on-private
python3 scripts/skillctl.py propose-upstream --mode patch --title "Improve auto-improve skill"
```

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `skills-management/skill-eval-loop`
- `memory`
- `brain/ingestion`
- `personalize`
- `loops`
- `agentic-development/agent-harness`
- `code-documentation`
- `quality-assurance`

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `writing-great-skills`: Use external skill-authoring quality rules when creating or revising skills. Install: `python scripts/install-external-skills.py --skill writing-great-skills --agent codex`.
- `teach`: Create mission-grounded learning material, resources, records, and lessons. Install: `python scripts/install-external-skills.py --skill teach --agent codex`.
- `grilling`: Interview one decision at a time until a plan or design is sharp. Install: `python scripts/install-external-skills.py --skill grilling --agent codex`.
- `grill-me`: Shortcut into a grilling session for plan or design stress testing. Install: `python scripts/install-external-skills.py --skill grill-me --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python scripts/install-external-skills.py --skill grill-with-docs --agent codex`.
- `codebase-design`: Use deep-module vocabulary for interface, seam, depth, locality, and testability decisions. Install: `python scripts/install-external-skills.py --skill codebase-design --agent codex`.
- `improve-codebase-architecture`: Find deepening opportunities and produce visual architecture-review candidates. Install: `python scripts/install-external-skills.py --skill improve-codebase-architecture --agent codex`.
- `tdd`: Use external test-first workflow for public-interface behavior changes. Install: `python scripts/install-external-skills.py --skill tdd --agent codex`.
- `use-afs`: Use the AFS filesystem layout and naming conventions instead of duplicating local filesystem guidance. Install: `python scripts/install-external-skills.py --skill use-afs --agent codex`.
- `codex-loop`: Run Codex PRD/story loops with one fresh subagent per story. Install: `python scripts/install-external-skills.py --skill codex-loop --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python scripts/install-external-skills.py --skill no-mistakes --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
