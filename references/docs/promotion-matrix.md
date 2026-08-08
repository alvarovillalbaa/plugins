# Promotion Matrix

Last updated: 2026-08-07

Use this matrix when a memory entry, lesson, raw source, generated improvement, or documentation finding might become durable project knowledge.

This matrix decides **which surface owns a signal and which skill owns the write**. It does not define AFS paths or date formats — resolve those through `use-afs`, which is the only authority for them. If `use-afs` is not installed, stop AFS-pathed work and report the install command. Local deltas live in [`afs-profile.md`](afs-profile.md).

| Signal | Canonical target | Owner skill | Notes |
| --- | --- | --- | --- |
| Runtime instruction that should affect future agent behavior | `CLAUDE.md` or `.claude/rules/` | `memory` | Promote only recurring, actionable rules. Remove duplicate auto-memory after promotion. |
| User, company, customer, environment, or project fact | The AFS fact surface for the fact's type, unless `BRAIN.md` maps facts elsewhere | `brain` + `code-documentation` | Fact surfaces are living, not timestamped. Facts are evidence; compile into the knowledge surface only when they become maintained understanding. |
| Reusable debugging or operational fix | The AFS fix surface | `code-documentation` | Include symptom, root cause, fix, verification, and affected owners. |
| Reusable lesson from repeated work | The AFS lesson surface for the domain | `learning` | Keep lessons short and evidence-backed. Promote broader rules to memory only when they should guide future sessions. |
| Raw source, transcript, export, or unreadable pointer | The AFS raw intake surface, with status metadata | `ingestion` | Mark `unprocessed`, `processed`, or `blocked`; use `blocked_reason` for unreadable sources. |
| Maintained synthesis or wiki page | The AFS source-of-truth surfaces — knowledge, cookbooks, runbooks, research, or references | `brain` + `ingestion` | Rewrite owner pages into current truth and preserve source provenance. |
| Installed skill prompt, reference, script, eval, template, or example improvement | Installed `.agents/skills/<name>/` plus local `.skill-improvements/` review bundle | `auto-improve` + `skill-eval-loop` | Keep the canonical plugin source read-only; retain the change locally through the installed-component merge flow. |
| Explicit canonical skill-source maintenance | Source skill path plus an optional reviewed patch bundle | `plugins-management` + `skill-eval-loop` | This is a separate user-requested workflow and is never inferred from `auto-improve`. |
| Agent-harness or autoresearch round logs/results | `.skill-improvements/` | `agent-harness` | Generated review artifacts are not durable memory. Promote only adopted lessons through `lessons/` or source docs. |
| Human-readable policy or repo convention | Closest living owner doc under `references/docs/`, `skills-chaining-map.md`, or a skill reference | `code-documentation` | Update living docs instead of burying current policy in an audit. |

## Rules

- Prefer the highest-priority owner that changes future behavior: memory rules before facts, facts before raw notes, living docs before historical audit notes.
- Keep evidence and current truth separate: timestamped folders preserve history; living docs carry the current contract.
- Do not promote secrets, credentials, personal contact details, or private customer data into upstream-safe skill source.
- Generated artifacts stay generated until a human adopts a lesson or source change.
