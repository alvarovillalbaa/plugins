# Statistical Methods

## Why Mann-Whitney U (not t-test)

Marketing metrics — impressions, click-through rates, open rates, engagement — are often right-skewed with outliers. The Mann-Whitney U test is non-parametric and does not assume normality. That does not make a universal small sample sufficient: pre-declare the observation floor from the metric, expected effect, variance, power, and stopping plan.

## Dual Threshold Rule

A variant must clear **both** gates to become a `keep`:

| Gate | Default | Rationale |
|------|---------|-----------|
| `p < P_WINNER` (0.05) | Statistical significance | Controls false positive rate |
| `lift ≥ LIFT_WIN` (15%) | Practical significance | Avoids "significant but useless" results |

A common pitfall in experimentation is declaring tiny, statistically-significant effects as wins. The lift gate ensures the improvement is meaningful enough to change behavior.

## Bootstrap Confidence Intervals

Bootstrap CI (1,000 resamples, 95% interval) estimates the plausible range of true lift. A CI of [8.2, 41.7]% tells you the true effect is almost certainly positive, but you should plan for the conservative end.

## Trending Detection

Early signal at p < 0.10 with at least `TRENDING_MIN_SAMPLES` observations per variant triggers `trending` status — a configurable watch signal, not a decision. Continue collecting data to the experiment's pre-declared floor before treating a result as confirmed.

## Sample Size Thresholds

Pass the approved floor with `--min-samples N` on `create`. Do not infer it from channel volume: volume changes how quickly evidence arrives, not how much evidence the decision requires. If a defensible floor is unavailable, keep the experiment in planning rather than allowing the engine to invent one.
