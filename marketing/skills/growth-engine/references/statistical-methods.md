# Statistical Methods

## Why Mann-Whitney U (not t-test)

Marketing metrics — impressions, click-through rates, open rates, engagement — are rarely normally distributed. They tend to be right-skewed with outliers from viral posts or unusually strong campaigns. The Mann-Whitney U test is non-parametric: it makes no normality assumption and works reliably with small samples (n ≥ 10 per variant for high-volume channels).

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

Early signal at p < 0.10 with ≥ 15 samples triggers `trending` status — a watch signal, not a decision. Continue collecting data before treating as confirmed.

## Sample Size Thresholds

| Channel type | Min samples/variant | Why |
|---|---|---|
| High-volume (content, email) | 10 | Data arrives fast; 10 observations sufficient for early signal |
| Low-volume (seo, linkedin, blog) | 30 | Slower data; need more to overcome noise |

Override with `--min-samples N` on `create` if your channel behaves differently.
