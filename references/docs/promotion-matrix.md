# Promotion Matrix

Last updated: 2026-06-26

Use this matrix when a memory entry, lesson, raw source, generated improvement, or documentation finding might become durable project knowledge.

| Signal | Canonical target | Owner skill | Notes |
| --- | --- | --- | --- |
| Runtime instruction that should affect future agent behavior | `CLAUDE.md` or `.claude/rules/` | `memory` | Promote only recurring, actionable rules. Remove duplicate auto-memory after promotion. |
| User, company, customer, environment, or project fact | `facts/YYYY/MM-DD/*.md` unless `BRAIN.md` maps facts elsewhere | `brain` + `code-documentation` | Facts are evidence. Compile into `knowledge/` only when they become maintained understanding. |
| Reusable debugging or operational fix | `fixes/YYYY/MM-DD/*.md` | `code-documentation` | Include symptom, root cause, fix, verification, and affected owners. |
| Reusable lesson from repeated work | `lessons/YYYY/MM-DD/*.md` | `learning` | Keep lessons short and evidence-backed. Promote broader rules to memory only when they should guide future sessions. |
| Raw source, transcript, export, or unreadable pointer | `raw/YYYY/MM-DD/` with status metadata | `ingestion` | Mark `unprocessed`, `processed`, or `blocked`; use `blocked_reason` for unreadable sources. |
| Maintained synthesis or wiki page | `knowledge/`, `cookbook/`, `runbooks/`, `research/`, or `references/` | `brain` + `ingestion` | Rewrite owner pages into current truth and preserve source provenance. |
| Skill prompt, reference, script, eval, template, or example improvement | Source skill path plus `.skill-improvements/` patch bundle when proposed upstream | `auto-improve` + `skill-eval-loop` | Classify with `scripts/skillctl.py`; keep local overlays out of upstream. |
| Agent-harness or autoresearch round logs/results | `.skill-improvements/` | `agent-harness` | Generated review artifacts are not durable memory. Promote only adopted lessons through `lessons/` or source docs. |
| Human-readable policy or repo convention | Closest living owner doc under `references/docs/`, `skills-chaining-map.md`, or a skill reference | `code-documentation` | Update living docs instead of burying current policy in an audit. |

## Rules

- Prefer the highest-priority owner that changes future behavior: memory rules before facts, facts before raw notes, living docs before historical audit notes.
- Keep evidence and current truth separate: timestamped folders preserve history; living docs carry the current contract.
- Do not promote secrets, credentials, personal contact details, or private customer data into upstream-safe skill source.
- Generated artifacts stay generated until a human adopts a lesson or source change.
