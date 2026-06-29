# Example: CRO Experiment for a SaaS Free-Trial Signup Page

Page: `/signup` for "Acme Analytics". Baseline: 4.0% of page visitors complete signup. ~9,000 visitors/week.

## Diagnosis

Funnel drop-off concentrates at the form step: 62% reach the form, only 6.5% of those submit. Session replays show users abandoning at the "company size" and "credit card" fields.

## Hypothesis

> Because requiring a credit card up front triggers cost/commitment anxiety (see `buyer-psychology`), removing it from the trial signup will increase form-submit rate without materially hurting trial→paid conversion.

## Test design

- **Control (A):** current form with credit card required.
- **Variant (B):** no credit card; trial converts via in-app prompt on day 12.
- **Primary metric:** signup completion rate (visitor → account created).
- **Guardrail metric:** trial → paid conversion (must not drop > 15% relative).
- **Unit:** visitor, randomized at first page load.

## Sizing

Baseline 4.0%, minimum detectable effect +0.8pp (4.0% → 4.8%), power 80%, alpha 5%, two-sided. Required ≈ 9,100 per arm → ~2 weeks at current traffic. (See `scripts/calculate_sample_size.py`.)

## Result (after 15 days)

| Arm | Visitors | Signups | Rate |
| --- | --- | --- | --- |
| A (control) | 9,240 | 370 | 4.00% |
| B (no CC) | 9,310 | 489 | 5.25% |

Lift: +1.25pp (+31% relative), p = 0.003. Guardrail: trial→paid 22% (A) vs 19% (B), −13% relative — within tolerance.

## Decision

Ship B. Net paid conversions per week rose despite lower trial→paid rate because the top-of-funnel gain dominated. Follow up with an experiment on the day-12 in-app conversion prompt.
