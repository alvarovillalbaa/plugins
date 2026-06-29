# Eval Results Report: <suite name>

- **Run date:** <YYYY-MM-DD>
- **Model:** <id>
- **Dataset:** <path> (<n> cases)
- **Commit / prompt version:** <sha or version>

## Headline

| Metric | Value | Gate | Pass? |
| --- | --- | --- | --- |
| Accuracy | <x.x%> | ≥ <y%> | <yes/no> |
| Precision | <0.xx> | — | — |
| Recall | <0.xx> | — | — |
| F1 | <0.xx> | — | — |

<One sentence: ship / block / investigate.>

## Comparison to baseline

| Metric | Previous | Current | Δ |
| --- | --- | --- | --- |
| Accuracy | <%> | <%> | <+/-> |

<Did anything regress? Which run is the baseline?>

## Failures

| id | input (short) | expected | predicted | category |
| --- | --- | --- | --- | --- |
| <id> | <...> | <...> | <...> | <model-miss / bad-label / ambiguous> |

## Analysis

<Patterns across failures. Are they real model misses, dataset/labeling issues,
or scorer artifacts? What is the single highest-leverage fix?>

## Actions

- [ ] <fix prompt / add few-shot / relabel case / adjust scorer>
- [ ] Re-run and confirm gate passes
- [ ] <update baseline if intentionally moved>

## Reproduce

```bash
python scripts/run_evals.py --dataset <path> --model <id> --out evals/results.json
```
