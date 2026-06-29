# Eval Run Example: Intent Classifier (20 cases)

A worked example of running `scripts/run_evals.py` against a small dataset and
reading the result. The task under test classifies a support message into one
of: `billing`, `bug`, `feature`, `other`.

## Dataset (excerpt)

`evals/intent.jsonl`:

```jsonl
{"id": "c1", "input": "I was charged twice this month", "expected": "billing", "match": "exact"}
{"id": "c2", "input": "the export button does nothing", "expected": "bug", "match": "exact"}
{"id": "c3", "input": "can you add dark mode?", "expected": "feature", "match": "exact"}
{"id": "c4", "input": "thanks for the help yesterday", "expected": "other", "match": "exact"}
```

20 cases total, balanced across the four labels.

## Command

```bash
python scripts/run_evals.py \
  --dataset evals/intent.jsonl \
  --provider anthropic \
  --model claude-sonnet-4-6 \
  --out evals/results.json
```

## Output

```
Done: 18/20 passed (accuracy=90.0%, precision=0.95, recall=0.90, f1=0.92)
```

`evals/results.json` summary:

```json
{
  "summary": {
    "total": 20,
    "passed": 18,
    "failed": 2,
    "accuracy": 0.9,
    "precision": 0.95,
    "recall": 0.9,
    "f1": 0.92,
    "model": "claude-sonnet-4-6"
  }
}
```

## Failure triage

The two failures, pulled from `results.json` `cases`:

| id | input | expected | predicted | note |
| --- | --- | --- | --- | --- |
| c12 | "your app crashed and I lost my draft, I want a refund" | bug | billing | genuinely mixed intent; ambiguous label |
| c17 | "how do I change my plan?" | billing | other | model treated it as a how-to question |

- **c12** is a labeling problem, not a model problem — split into multi-label or
  pick the primary intent and document the rule.
- **c17** is a real miss — add a few-shot example clarifying that plan changes
  are billing, then re-run.

## Regression gate

Wire this into CI so accuracy cannot silently drop:

```bash
python scripts/run_evals.py --dataset evals/intent.jsonl --out evals/results.json
python -c "import json,sys; acc=json.load(open('evals/results.json'))['summary']['accuracy']; sys.exit(0 if acc>=0.85 else 1)"
```

The session-end hook archives `results.json` into `evals/history/` so runs are
comparable over time.
