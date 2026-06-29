---
name: backend-testing
description: >-
  Use for backend tests, API contract tests, service integration tests,
  fixtures, queues, jobs, and persistence test seams. Child skill of
  `quality-assurance`; route here from the parent router when this lane is
  the narrowest owner.
---

# Backend Test Engineering

This child skill owns backend tests, API contract tests, service integration tests, fixtures, queues, jobs, and persistence test seams. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about backend tests, API contract tests, service integration tests, fixtures, queues, jobs, and persistence test seams.
- The parent router [`../quality-assurance/SKILL.md`](../quality-assurance/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## References

Load the reference that matches the work:

- `references/backend-testing.md` — language-agnostic backend QA strategy
- `references/python-backend-tests.md` — pytest, Django/DRF, Celery, signals, serializer/view patterns
- `references/code-tests-cookbook.md` — project-specific rules: TDD workflow, ECS runner, Celery patterns, OAuth 7-scenario template, mocking rules, CI targets
- `references/django-drf-testing.md` — DRF-specific examples
- `references/integration-testing.md` — integration test patterns

## Chain Rules

- Chain to `pentest`, `ai-engineering/ai-evals-observability`, `frontend`, `backend`, `prs`, `cloud` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `deslop`: Remove AI-generated code slop from the current diff without changing behavior. Install: `python scripts/install-external-skills.py --skill deslop --agent codex`.
- `thermo-nuclear-code-quality-review`: Run an unusually strict maintainability and abstraction-quality review. Install: `python scripts/install-external-skills.py --skill thermo-nuclear-code-quality-review --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python scripts/install-external-skills.py --skill no-mistakes --agent codex`.
- `improve`: Run a read-only senior codebase audit and write execution-ready plans for other agents. Install: `python scripts/install-external-skills.py --skill improve --agent codex`.
- `codebase-design`: Use deep-module vocabulary for interface, seam, depth, locality, and testability decisions. Install: `python scripts/install-external-skills.py --skill codebase-design --agent codex`.
- `improve-codebase-architecture`: Find deepening opportunities and produce visual architecture-review candidates. Install: `python scripts/install-external-skills.py --skill improve-codebase-architecture --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python scripts/install-external-skills.py --skill grill-with-docs --agent codex`.
- `tdd`: Use external test-first workflow for public-interface behavior changes. Install: `python scripts/install-external-skills.py --skill tdd --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
