# Loop Patterns Reference

Reference for designing and maintaining repeatable improvement, evaluation, memory, and experimentation loops. A loop is a structured cycle that runs on a trigger, produces a measurable change, and feeds its own next iteration. Loops must be human-started and bounded; surface what they'll change before running unattended.

## What makes a loop (not just a task)

A loop is repeatable and self-improving:
- **Trigger** — what starts it (schedule, event, threshold, manual).
- **Action** — the work performed each cycle.
- **Measurement** — how you know it did better/worse than last time.
- **Feedback** — the result updates state/inputs so the next cycle improves.
- **Stop condition** — when it ends or pauses (goal met, budget spent, no improvement, max iterations).

Without measurement and feedback, you have a recurring task, not an improvement loop.

## The core cycle (Observe → Decide → Act → Measure)

1. **Observe** — gather current state/signals.
2. **Decide** — choose the change to try, based on evidence.
3. **Act** — make the change (gated if risky).
4. **Measure** — evaluate against a metric/baseline.
5. **Feed back** — keep if better, revert/adjust if not; update inputs for the next pass.

This generalizes PDCA (Plan-Do-Check-Act) and OODA. Every loop type below is a specialization.

## Loop types

### Improvement loop
Continuously raise quality of a target (a skill, a doc, a workflow).
- Trigger: cadence or a quality signal.
- Action: identify weakest area → apply a fix → re-measure.
- Stop: quality threshold reached, or diminishing returns.
- Example: `auto-improve` driving skill quality via eval scores.

### Evaluation loop
Score outputs against criteria, repeatedly, to detect regressions and gate changes.
- Trigger: a change to the thing under test, or a schedule.
- Action: run the eval set → score → compare to baseline.
- Stop: pass/fail gate; block regressions.
- See `skill-eval-loop` for skill-specific evaluation.

### Research loop
Iteratively narrow toward an answer.
- Trigger: a question.
- Action: query → assess gaps → refine query → repeat.
- Stop: question answered to confidence, or sources exhausted.
- Multi-pass: broad scan → targeted deep-dives → synthesis.

### Memory/learning loop
Capture and consolidate knowledge over time.
- Trigger: session end, correction, or cadence.
- Action: extract lessons/preferences → dedupe → promote candidates.
- Stop: continuous (maintenance), but each pass is bounded.
- Feeds `lessons`, `memory`, `calibration`, `knowledge-base`.

### Monitoring loop
Watch a metric and act on threshold breaches.
- Trigger: schedule/poll.
- Action: read metric → compare to threshold → alert or act.
- Stop: continuous; each check is cheap and bounded.
- Keep actions on breach human-gated if consequential.

### Experimentation loop
Test hypotheses to learn what works.
- Trigger: a hypothesis.
- Action: define success criterion → run experiment → measure → conclude.
- Stop: criterion met or refuted; pre-commit the success threshold before running.

## Design principles

- **Bound everything** — max iterations, time, or budget. An unbounded loop is a runaway risk.
- **Measure or it's not a loop** — define the metric and baseline before starting.
- **Make each cycle cheap** — small, fast iterations beat large, slow ones; they fail safe and learn faster.
- **Idempotent / safe-to-repeat** — re-running shouldn't corrupt state or double-apply changes.
- **Observable** — each cycle logs what it did and the result, so a human can audit and intervene.
- **Convergent** — the loop should trend toward the goal, not oscillate; if it's not improving, stop.
- **Reversible steps** — prefer changes you can roll back if a cycle regresses.

## Safety & control

- **Human-started and bounded** — loops don't self-launch unattended; a human kicks them off and sets limits.
- **Surface the plan** — before a loop runs autonomously, state what it will change and the stop conditions.
- **Gate risky actions per cycle** — destructive, shared-state, externally-visible, or costly actions still require approval even inside a loop.
- **Kill switch** — every running loop must be cancelable; honor stop signals immediately.
- **Cost-aware** — track resource/time/$ spend across iterations; stop at budget.
- **No silent regressions** — a cycle that makes things worse must revert, not persist.

## Maintaining loops

- **Review periodically** — is the loop still converging and still worth its cost?
- **Tune triggers and thresholds** as conditions change.
- **Retire dead loops** — ones that no longer improve anything are pure overhead.
- **Verify the metric still measures what matters** — a loop optimizing a stale proxy drifts from the real goal (Goodhart's law).

## Handoffs

- Skill quality loops → `auto-improve`, `skill-eval-loop`.
- Knowledge/memory consolidation → `learning`, `lessons`, `memory`, `knowledge-base`.
- Experiment design rigor → product `experiments`.
- Scheduling/orchestration → the relevant runner commands (e.g., `ar-loop`, `ar-run`).
