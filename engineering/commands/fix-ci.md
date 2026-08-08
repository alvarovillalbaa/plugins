---
name: fix-ci
description: Diagnose failing continuous-integration checks, apply targeted local fixes, and verify the affected checks without assuming a hosting provider.
argument-hint: "[change, branch, or check] [--max-iterations N]"
allowed-tools: [Agent, Bash, Read, Grep, AskUserQuestion, Skill]
hide-from-slash-command-tool: "true"
---

Use skills: **cicd**, **prs**, and **quality-assurance**.

1. **Detect the CI surface** — Read repository configuration and use the configured provider or project-local tooling. For GitHub, `gh pr checks` and `gh run view --log-failed` are valid adapters; do not assume they exist elsewhere.
2. **Classify failures** — Label each failure as flaky, real, or infrastructure. Retry a flaky check only when the request authorizes the external action.
3. **Reproduce locally** — Run the same narrow command used by CI. If it cannot be reproduced, compare environment and configuration before changing code.
4. **Fix the root cause** — Change only the implicated surface. Do not bundle unrelated cleanup or one commit per check as an unconditional policy.
5. **Verify locally** — Re-run the failing check, then a broader gate when the touched surface has high fan-out.
6. **Request external-action approval** — Committing, pushing, rerunning hosted CI, or commenting on a change requires explicit authorization unless the original request already granted that exact action.
7. **Report** — Return each check's classification, root cause, local evidence, remaining infrastructure issues, and current hosted status if verified.

## Boundary

This command fixes already-failing CI. Use `check-agent-compat` for repository readiness and `review-pr` for code-review findings.
