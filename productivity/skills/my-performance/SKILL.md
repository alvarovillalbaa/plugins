---
name: my-performance
description: >-
  Evaluate the user's own performance for a stated role/period against an explicit
  rubric, separating evidence from inference. Self-review only, never covert
  evaluation of others.
---

# My Performance

Produce a fair, decision-useful self-review. Evaluate the declared role and period, not the user's permanent identity or worth.

## Workflow

1. Declare the role, review period, purpose, audience, and rubric before scoring. If the user supplies no rubric, propose and label a provisional rubric; do not present it as an employer's standard.
2. Gather evidence from the current conversation, already loaded memory, and repo-local memory. Ask before accessing a new private source.
3. Normalize every evidence item to a source, observation date, criterion, and freshness judgment. Read [`references/performance-evidence-and-scoring.md`](references/performance-evidence-and-scoring.md).
4. Separate facts from interpretations and mark uncovered criteria `not evaluated`.
5. Score a criterion only when it has enough in-period evidence under the declared coverage rule. Never assign zero for missing coverage.
6. Calculate an overall score only when at least 75% of rubric weight is scoreable. Otherwise report the coverage percentage and omit the overall score.
7. Identify strengths, gaps, and trends. Distinguish a repeated trend from a single event and state confidence.
8. Define no more than three next-period commitments with an owner, measure, target date, and evidence source.
9. Render the review with [`templates/performance-review.md`](templates/performance-review.md)
   and apply [`references/post-run-checklist.md`](references/post-run-checklist.md).

## Evidence and Fairness Gates

- Use current user-provided context, already loaded memory, and repo-local memory by default.
- Obtain explicit authorization before reading email, calendar, Slack, Drive, HR systems, private dashboards, or another new private source.
- Obtain separate approval before writing any conclusion, score, or preference to memory.
- Exclude race, ethnicity, nationality, religion, sex, gender identity, sexual orientation, disability, health, age, pregnancy, political beliefs, trauma, family status, and other protected or sensitive traits from the rubric and explanations.
- Do not diagnose, infer intent, or convert a disputed interpretation into fact.
- Do not rank the user against coworkers unless the user supplies an authorized and legitimate comparison dataset.
- Preserve conflicting evidence and explain how it affects confidence.

## Scoring Contract

- Use the scale and anchors declared in the rubric; do not silently change scales.
- Require either two dated, in-period evidence items from distinct sources or one dated, authoritative direct measure for a criterion score.
- Mark a criterion `not evaluated` when it misses that threshold, even when intuition suggests a score.
- Normalize rubric weights only when the declared weights do not sum to one or 100, and disclose the normalization.
- Report both scored-weight coverage and missing criteria beside any overall score.

Validate a structured review with [`scripts/check_score_coverage.py`](scripts/check_score_coverage.py) before returning a high-stakes or numeric assessment.

## Output Contract

Return:

1. `Review frame` - role, period, purpose, audience, rubric, and scale
2. `Evidence coverage` - sources, freshness, and weighted coverage
3. `Rubric assessment` - score or not evaluated, evidence, inference, and confidence per criterion
4. `Strengths, gaps, and trends`
5. `Overall result` - only when the coverage gate passes
6. `Next-period commitments`
7. `Unknowns and memory candidates`

Route a request for broader growth coaching to [`improve-me`](../improve-me/SKILL.md). Route an explicit request for a sharper rhetorical treatment to [`roast-me`](../roast-me/SKILL.md).

## Resources

- Read [`references/performance-evidence-and-scoring.md`](references/performance-evidence-and-scoring.md) before constructing the rubric or scores.
- Compare against [`examples/partial-coverage-example.md`](examples/partial-coverage-example.md) for correct not-evaluated behavior.
- Use [`templates/performance-review.md`](templates/performance-review.md) for the final artifact.
