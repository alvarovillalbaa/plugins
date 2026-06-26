---
name: quality-assurance
description: >-
  Router for test strategy and coverage, frontend E2E/browser QA, backend test
  engineering, CI flake debugging, performance testing, passive security
  review, and AI eval testing.
---

# Quality Assurance Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`test-strategy-coverage`](../test-strategy-coverage/SKILL.md) - test strategy, regression coverage, suite architecture, test planning, TDD, and coverage improvement
- [`frontend-e2e-browser-qa`](../frontend-e2e-browser-qa/SKILL.md) - browser QA, Playwright/Cypress flows, user-visible state validation, trace capture, and frontend regressions
- [`backend-test-engineering`](../backend-test-engineering/SKILL.md) - backend tests, API contract tests, service integration tests, fixtures, queues, jobs, and persistence test seams
- [`ci-flake-debugging`](../ci-flake-debugging/SKILL.md) - CI failures, flaky tests, ordering problems, environment drift, cache issues, and quality gate recovery
- [`performance-testing`](../performance-testing/SKILL.md) - load tests, latency investigations, profiling, capacity validation, and performance regression evidence
- [`passive-security-review`](../passive-security-review/SKILL.md) - passive security review, threat modeling, secure-code checks, dependency review, and compliance-oriented findings
- [`ai-evals-testing`](../ai-evals-testing/SKILL.md) - LLM, agent, and RAG eval cases, eval datasets, regression thresholds, CI eval gates, and nondeterministic-output test repair

## Route

| User asks for | Use |
| --- | --- |
| test strategy, regression coverage, suite architecture, test planning, TDD, and coverage improvement | [`test-strategy-coverage`](../test-strategy-coverage/SKILL.md) |
| browser QA, Playwright/Cypress flows, user-visible state validation, trace capture, and frontend regressions | [`frontend-e2e-browser-qa`](../frontend-e2e-browser-qa/SKILL.md) |
| backend tests, API contract tests, service integration tests, fixtures, queues, jobs, and persistence test seams | [`backend-test-engineering`](../backend-test-engineering/SKILL.md) |
| CI failures, flaky tests, ordering problems, environment drift, cache issues, and quality gate recovery | [`ci-flake-debugging`](../ci-flake-debugging/SKILL.md) |
| load tests, latency investigations, profiling, capacity validation, and performance regression evidence | [`performance-testing`](../performance-testing/SKILL.md) |
| passive security review, threat modeling, secure-code checks, dependency review, and compliance-oriented findings | [`passive-security-review`](../passive-security-review/SKILL.md) |
| LLM, agent, and RAG eval cases, eval datasets, regression thresholds, CI eval gates, and nondeterministic-output test repair | [`ai-evals-testing`](../ai-evals-testing/SKILL.md) |

## Chain Rules

- `pentest`
- `ai-engineering/ai-evals-observability`
- `frontend`
- `backend`
- `pr-management`
- `cloud-management`

## Parent-Owned References

- `debug-investigation` stays as a parent-level chain/reference, not a child skill.

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `deslop`: Remove AI-generated code slop from the current diff without changing behavior. Install: `python scripts/install-external-skills.py --skill deslop --agent codex`.
- `thermo-nuclear-code-quality-review`: Run an unusually strict maintainability and abstraction-quality review. Install: `python scripts/install-external-skills.py --skill thermo-nuclear-code-quality-review --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python scripts/install-external-skills.py --skill no-mistakes --agent codex`.
- `improve`: Run a read-only senior codebase audit and write execution-ready plans for other agents. Install: `python scripts/install-external-skills.py --skill improve --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
