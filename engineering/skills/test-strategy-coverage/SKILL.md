---
name: test-strategy-coverage
description: >-
  Use for test strategy, regression coverage, suite architecture, test
  planning, TDD, and coverage improvement. Child skill of `quality-assurance`; route here from the parent router when this lane is the
  narrowest owner.
---

# Test Strategy Coverage

This child skill owns test strategy, regression coverage, suite architecture, test planning, TDD, and coverage improvement. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about test strategy, regression coverage, suite architecture, test planning, TDD, and coverage improvement.
- The parent router [`../quality-assurance/SKILL.md`](../quality-assurance/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## References

- `references/test-strategy.md` — test strategy fundamentals
- `references/analyze-tests-methodology.md` — audit methodology: inventory, type coverage check, DB fidelity, TDD readiness, mocking discipline, gap identification
- `references/suite-architecture.md` — test suite architecture patterns
- `references/tdd-iron-laws.md` — TDD discipline and iron laws

## Chain Rules

- Chain to `pentest`, `ai-engineering/ai-evals-observability`, `frontend`, `backend`, `prs`, `cloud` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `codebase-design`: Use deep-module vocabulary for interface, seam, depth, locality, and testability decisions. Install: `python scripts/install-external-skills.py --skill codebase-design --agent codex`.
- `improve-codebase-architecture`: Find deepening opportunities and produce visual architecture-review candidates. Install: `python scripts/install-external-skills.py --skill improve-codebase-architecture --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python scripts/install-external-skills.py --skill grill-with-docs --agent codex`.
- `tdd`: Use external test-first workflow for public-interface behavior changes. Install: `python scripts/install-external-skills.py --skill tdd --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
