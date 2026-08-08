---
name: improve-me
description: >-
  Turn evidence about the user's own work into a focused improvement plan with
  prioritized experiments. Only on explicit request; routes roasting to
  `roast-me` and rubric reviews to `my-performance`.
---

# Improve Me

Convert evidence into a small, testable growth plan. Coach the user's behavior and work without inventing a biography, diagnosing them, or treating memory as automatically current.

## Children

- [`roast-me`](../roast-me/SKILL.md) - Deliver an explicitly requested, sharp, constructive roast.
- [`my-performance`](../my-performance/SKILL.md) - Evaluate a stated role and period against a declared rubric.

## Workflow

1. Confirm that the current request directly asks for personal or professional improvement or explicitly invokes this skill. Do not infer coaching consent from unrelated work or background memory.
2. State the improvement objective, context, time horizon, and desired outcome. Infer only low-risk omissions and label each inference.
3. Build an evidence ledger from the current conversation, already loaded memory, and repo-local memory. Read [`references/evidence-and-memory-policy.md`](references/evidence-and-memory-policy.md) before using historical memory.
4. Record a source, observation date, and freshness judgment for every material claim. Mark missing areas `not evaluated`; never convert missing evidence into a weakness.
5. Separate observed facts from interpretations. Test each interpretation against at least one plausible alternative explanation.
6. Identify no more than three leverage points. Rank them by expected impact, user control, evidence strength, and reversibility.
7. Design one bounded experiment per selected leverage point. Define the baseline, action, trigger, success measure, guardrail, review date, and continue/adjust/stop rule.
8. Schedule lightweight check-ins in the artifact only. Do not mutate a calendar or send reminders without explicit approval at the point of action.
9. Produce the plan with [`templates/growth-plan.md`](templates/growth-plan.md). Lead with the highest-leverage action and keep the evidence ledger auditable.

## Evidence and Privacy Gates

- Use only current user-provided context, already loaded memory, and repo-local memory by default.
- Ask for explicit authorization before opening a new private source such as email, calendar, Slack, Drive, HR records, or a private analytics system.
- Treat permission to read one source as scoped to that source and this task; do not infer permission to search adjacent systems.
- Request separate explicit approval before writing, promoting, or deleting memory. Present memory candidates as drafts until approved.
- Exclude protected or sensitive traits from causal explanations. Do not infer health, disability, religion, ethnicity, sexuality, political views, trauma, or diagnoses.
- Prefer behavior, decisions, work products, and outcomes that the user can change.
- Label stale or conflicting evidence and avoid a confident recommendation until the conflict is resolved or disclosed.

## Output Contract

Return:

1. `Objective and horizon`
2. `Evidence ledger` with fact, inference, and not-evaluated labels
3. `Top leverage points` with evidence strength and rationale
4. `Experiments` with measures, guardrails, and review dates
5. `Check-in plan`
6. `Unknowns and memory candidates`

Do not produce a numeric personal score. Route a requested score or formal review to [`my-performance`](../my-performance/SKILL.md).

## Chain Rules

- `memory`
- `personalize/calibration`
- `reporting`

## Resources

- Read [`references/evidence-and-memory-policy.md`](references/evidence-and-memory-policy.md) for provenance, freshness, and privacy rules.
- Run [`scripts/check_evidence.py`](scripts/check_evidence.py) to audit a structured evidence ledger before relying on it.
- Use [`templates/growth-plan.md`](templates/growth-plan.md) for the final artifact.
- Compare against [`examples/coaching-example.md`](examples/coaching-example.md) for a partial-evidence example.
- Apply [`references/post-run-checklist.md`](references/post-run-checklist.md)
  before returning the result.
