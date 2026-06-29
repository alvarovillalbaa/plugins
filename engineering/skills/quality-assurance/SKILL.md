---
name: quality-assurance
description: Router for test strategy, browser QA, backend tests, flakes, performance routing, security, and AI eval testing.
---

# Quality Assurance Router

## Children

- [`test-strategy-coverage`](../test-strategy-coverage/SKILL.md) - Test Strategy Coverage work.
- [`frontend-e2e`](../frontend-e2e/SKILL.md) - Frontend E2e work.
- [`backend-testing`](../backend-testing/SKILL.md) - Backend Testing work.
- [`flake`](../flake/SKILL.md) - Flake work.
- [`security`](../security/SKILL.md) - Security work.
- [`ai-evals`](../ai-evals/SKILL.md) - Ai Evals work.

## Route

| Request | Use |
| --- | --- |
| test strategy coverage requests | [`test-strategy-coverage`](../test-strategy-coverage/SKILL.md) |
| frontend e2e requests | [`frontend-e2e`](../frontend-e2e/SKILL.md) |
| backend testing requests | [`backend-testing`](../backend-testing/SKILL.md) |
| flake requests | [`flake`](../flake/SKILL.md) |
| security requests | [`security`](../security/SKILL.md) |
| ai evals requests | [`ai-evals`](../ai-evals/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `pentest`
- `ai-engineering/ai-evals-observability`
- `frontend/performance`
- `frontend`
- `backend`
- `prs`
- `cloud`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `deslop`: Remove AI-generated code slop from the current diff without changing behavior. Install: `python scripts/install-external-skills.py --skill deslop --agent codex`.
- `thermo-nuclear-code-quality-review`: Run an unusually strict maintainability and abstraction-quality review. Install: `python scripts/install-external-skills.py --skill thermo-nuclear-code-quality-review --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python scripts/install-external-skills.py --skill no-mistakes --agent codex`.
- `improve`: Run a read-only senior codebase audit and write execution-ready plans for other agents. Install: `python scripts/install-external-skills.py --skill improve --agent codex`.
- `browserbase-ui-test`: Use Browserbase UI testing guidance for browser-level product verification. Install: `python scripts/install-external-skills.py --skill browserbase-ui-test --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
