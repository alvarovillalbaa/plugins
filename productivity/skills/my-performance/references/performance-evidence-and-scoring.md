# Performance Evidence and Scoring

## Review frame

Declare these fields before assessment:

- role and scope;
- period start and end dates;
- review purpose and audience;
- rubric criteria, anchors, weights, and scoring scale;
- evidence-coverage rule.

Treat a missing frame as a drafting problem, not permission to improvise a definitive score. Label an agent-proposed rubric `provisional` until the user accepts it.

## Evidence contract

Record each item with a stable ID, source, source type, observation date, and the criterion it informs. Keep evidence inside the review period unless it establishes an explicitly labeled historical baseline.

Use only current context, loaded memory, and repo-local memory by default. Ask before opening new private sources. Ask separately before saving the review or any derived conclusion to memory.

Classify statements as facts or inferences. Mark absent criterion coverage `not evaluated`. Do not treat a missing outcome, missing peer feedback, or unavailable system as poor performance.

## Default sufficiency rule

Score a criterion only when it has either:

1. two in-period evidence items from distinct sources; or
2. one in-period authoritative direct measure.

Examples of direct measures include an accepted delivery record, a verified target result, or an authoritative system metric that maps directly to the criterion. A self-report can be important evidence but is not automatically an authoritative direct measure.

Allow the user or organization to replace this rule only by declaring another rule in the review frame. Never lower the threshold silently.

## Weighted coverage

Calculate scoreable coverage as:

`sum(weight of scoreable criteria) / sum(weight of all criteria)`

Publish an overall score only when coverage is at least 75%. Keep every unscoreable criterion out of the numerator and out of the score calculation; do not coerce it to zero. Show the coverage percentage beside the score.

If the weights do not sum to one or 100, normalize them proportionally and disclose the operation. Do not invent a weight for a criterion with no declared weight; request or propose one as part of a provisional rubric.

## Trend discipline

Call something a trend only when evidence spans multiple points in time. Call a single event an observation. Label the direction, period, evidence IDs, and confidence. Preserve contradictions rather than averaging them out narratively.

## Fairness boundaries

Exclude protected and sensitive traits from criteria and causal explanations. Do not diagnose, infer intent, score personality, or compare against coworkers without a legitimate, authorized comparison set. Keep the assessment centered on role expectations, observable behavior, work products, and outcomes.
