# Skill Evaluation Methods Reference

Reference for evaluating skill quality: running evals, scoring outputs, regression checks, prompt/skill mutation proposals, and improvement gates. The premise: improve skills with evidence, not vibes. A skill change ships only if an eval shows it's better and not regressed. Mutations and promotions are human-gated.

## Why eval skills

Skills are prompts/instructions that shape agent behavior. Edits feel like improvements but often regress — they help one case and break three others. An eval loop makes quality measurable: define what "good" means, test against it, and gate changes on the result.

## Building an eval set

The eval set is the contract for what the skill should do.
- **Representative cases** — cover the skill's main jobs, not just the easy path.
- **Edge cases** — the inputs that previously broke, ambiguous requests, boundary conditions.
- **Negative cases** — inputs the skill should *decline* or route elsewhere (tests boundaries and safety gates).
- **Golden outputs or rubrics** — for each case, either an ideal output or a scoring rubric describing what good looks like.
- **Held-out set** — keep some cases unseen during tuning to detect overfitting to the eval.

Grow the eval set from real failures: every time the skill misbehaves, add that case so it can never silently regress again.

## Scoring methods

| Method | How | Best for |
| --- | --- | --- |
| **Exact/structural match** | Output matches expected exactly or by structure | Deterministic outputs, formats |
| **Rubric scoring** | Score against explicit criteria (1–5 per dimension) | Quality/judgment outputs |
| **LLM-as-judge** | A model grades output vs. rubric/golden | Scalable qualitative grading |
| **Pairwise comparison** | Judge picks better of two (old vs. new) | Detecting improvement/regression |
| **Human review** | A person scores | Ground truth, high-stakes gates |

Scoring discipline:
- **Define rubric dimensions explicitly** (e.g., correctness, completeness, format-adherence, safety, tone). Score each, don't give one fuzzy number.
- **LLM-as-judge cautions** — judges have biases (length, position, self-preference). Use a clear rubric, randomize order in pairwise, and spot-check against human judgment.
- **Calibrate the judge** — verify it agrees with human scores on a sample before trusting it at scale.

## Regression checks

The core safety function: don't let an "improvement" break what worked.
1. **Baseline** — score the current skill on the full eval set; record it.
2. **Apply the change** — the proposed mutation.
3. **Re-score** — run the same eval set.
4. **Compare** — overall and per-case. A change that lifts the average but regresses specific cases is suspect.
5. **Gate** — only ship if it improves (or holds) without regressing protected cases.

Protect a set of must-not-regress cases (safety gates, known past failures) — these are hard blockers regardless of average.

## Mutation proposals

When evals reveal weakness, propose targeted changes:
- **Diagnose first** — which cases fail, and why? Cluster failures to find the root (ambiguous instruction, missing guidance, wrong routing, over-broad scope).
- **Smallest effective change** — adjust the specific instruction causing failures; don't rewrite the whole skill. Large rewrites regress unpredictably.
- **One change at a time** — isolate variables so you know what caused the score change. Bundled edits make attribution impossible.
- **Hypothesis-driven** — state what you expect the change to improve before testing it.
- **Test, then propose** — bring the eval delta with the proposal, not just the edit.

Common mutation types: clarify an ambiguous instruction, add a missing case/example, tighten scope/routing, add a safety gate, remove a counterproductive rule.

## Improvement gates

Explicit criteria a change must pass to ship:
- **Net improvement** on the eval set (above noise).
- **No protected-case regressions.**
- **Held-out set confirms** it's not overfit.
- **Safety/boundary cases still pass.**
- **Human approval** for the change (mutations to skills are human-gated — they alter behavior broadly).

Fail any gate → don't ship; iterate or revert.

## The eval loop

Wire it as a loop (see `loops`):
1. Run evals → score.
2. Identify weakest cases.
3. Propose a targeted mutation (hypothesis).
4. Re-run evals → compare to baseline.
5. Gate: improvement + no regression + approval → ship; else revert/iterate.
6. Add new failures to the eval set.
Bound the loop (max iterations) and keep each change small and reversible.

## Pitfalls

- **Overfitting to the eval** — gaming the test set instead of real quality. Use held-out cases.
- **Goodhart's law** — optimizing the metric, not the behavior. Keep the rubric aligned to real outcomes; revisit it.
- **Judge bias** — trusting LLM scores uncritically. Calibrate and spot-check.
- **Bundled changes** — can't attribute results. One change at a time.
- **Average hides regressions** — always check per-case, protect known cases.
- **No baseline** — "it seems better" isn't evidence. Always compare to a recorded baseline.

## Quality gates

- **Evidence required** — no skill change ships without an eval showing net improvement and no protected-case regression.
- **Reversible** — keep the prior version; revert on regression.
- **Human-gated** — skill mutations and promotion need approval.
- **Grow the eval set** from real failures so regressions can't recur silently.

## Handoffs

- Applying approved skill edits → `plugins-management`.
- Orchestrating the loop on a cadence → `loops`, `auto-improve`.
- Failures worth a durable lesson → `lessons`.
- Deep eval/observability tooling for AI features → engineering `ai-evals-observability`, `ai-evals`.
