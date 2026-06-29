---
name: tech-debt
description: >-
  Use for technical-debt elimination, refactor plans, dependency cleanup,
  anti-pattern removal, and schedulable debt cadences. Child skill of
  `agentic-development`; route here from the parent router when this lane is
  the narrowest owner.
---

# Tech Debt Management

This child skill owns technical-debt elimination, refactor plans, dependency cleanup, anti-pattern removal, and schedulable debt cadences. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about technical-debt elimination, refactor plans, dependency cleanup, anti-pattern removal, and schedulable debt cadences.
- The parent router [`../agentic-development/SKILL.md`](../agentic-development/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## References

- `references/code-simplification.md` — scope rules, behavior-preservation, external chain points
- `references/deslop-simplify-guide.md` — deslop (remove low-quality code: vague names, noise, weak error handling, dead code) and simplify (same behavior, less code: deduplication, control flow, stdlib) with checklists and output format
- `references/refactor-planning.md` — planning refactor work safely

## Chain Rules

- Chain to `frontend`, `backend`, `quality-assurance`, `code-documentation`, `cloud`, `prs`, `skills-management` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.
- Remove compatibility residue instead of wrapping it. Prefer deleting stale aliases, shims, facade layers, and route bridges once the canonical owner is clear.
- Pair debt cleanup with focused proof and the nearest durable documentation update when behavior or ownership changes.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `deslop`: Remove AI-generated code slop from the current diff without changing behavior. Install: `python scripts/install-external-skills.py --skill deslop --agent codex`.
- `thermo-nuclear-code-quality-review`: Run an unusually strict maintainability and abstraction-quality review. Install: `python scripts/install-external-skills.py --skill thermo-nuclear-code-quality-review --agent codex`.
- `improve`: Run a read-only senior codebase audit and write execution-ready plans for other agents. Install: `python scripts/install-external-skills.py --skill improve --agent codex`.
- `codebase-design`: Use deep-module vocabulary for interface, seam, depth, locality, and testability decisions. Install: `python scripts/install-external-skills.py --skill codebase-design --agent codex`.
- `improve-codebase-architecture`: Find deepening opportunities and produce visual architecture-review candidates. Install: `python scripts/install-external-skills.py --skill improve-codebase-architecture --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python scripts/install-external-skills.py --skill grill-with-docs --agent codex`.
- `tdd`: Use external test-first workflow for public-interface behavior changes. Install: `python scripts/install-external-skills.py --skill tdd --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
