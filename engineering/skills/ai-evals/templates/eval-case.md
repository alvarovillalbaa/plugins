# Eval Case: <case id>

A single eval test case. Keep cases small, deterministic to score, and traceable
to a real failure or requirement. The JSONL form consumed by
`scripts/run_evals.py` is at the bottom.

## Intent

<What capability this case checks. Link the requirement, bug, or user report
that motivated it.>

## Input

```text
<exact input handed to the model / system under test>
```

## Expected output

```text
<the correct answer, or the property the answer must satisfy>
```

## Scoring

- **Match mode:** <exact | contains | regex>
- **Rationale:** <why this scorer is right; e.g. "format is fixed" or
  "any phrasing containing the order id is acceptable">
- **Known acceptable variants:** <if any>

## Difficulty / category

- **Category:** <happy-path | edge-case | adversarial | regression>
- **Source:** <synthetic | production log | bug report #...>

## JSONL form

```jsonl
{"id": "<case-id>", "input": "<input>", "expected": "<expected>", "match": "exact"}
```
