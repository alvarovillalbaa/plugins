#!/usr/bin/env python3
"""Run an eval suite from a JSONL dataset and print a scored summary.

Each dataset line is one case:
  {"id": "c1", "input": "...", "expected": "...", "match": "exact"}

`match` selects the scorer: "exact", "contains", or "regex" (default "exact").
The model call is pluggable: by default a deterministic echo stub runs so the
harness is testable offline. Wire `--provider anthropic` to call a real model
(requires ANTHROPIC_API_KEY and the anthropic SDK).

Outputs a JSON results file and prints precision/recall/accuracy to stderr.

Usage:
  run_evals.py --dataset evals/dataset.jsonl
  run_evals.py --dataset evals/dataset.jsonl --provider anthropic --model claude-sonnet-4-6
  run_evals.py --dataset evals/dataset.jsonl --out evals/results.json
"""

import argparse
import json
import os
import re
import sys


def load_dataset(path: str) -> list[dict]:
    cases = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                cases.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Malformed JSON on line {line_no}: {exc}")
    return cases


def call_stub(prompt: str, _model: str) -> str:
    """Offline default: echoes the input so the harness can be exercised."""
    return prompt


def call_anthropic(prompt: str, model: str) -> str:
    import anthropic

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")


def score(predicted: str, expected: str, mode: str) -> bool:
    p, e = predicted.strip(), expected.strip()
    if mode == "contains":
        return e.lower() in p.lower()
    if mode == "regex":
        return re.search(expected, predicted) is not None
    return p == e


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a JSONL eval suite.")
    parser.add_argument("--dataset", required=True, help="Path to the JSONL dataset.")
    parser.add_argument("--provider", choices=["stub", "anthropic"], default="stub")
    parser.add_argument("--model", default="claude-sonnet-4-6")
    parser.add_argument("--out", help="Write results JSON here (default: stdout).")
    args = parser.parse_args()

    try:
        cases = load_dataset(args.dataset)
    except FileNotFoundError:
        print(f"Error: dataset not found: {args.dataset}", file=sys.stderr)
        return 2

    if not cases:
        print("Error: dataset has 0 cases.", file=sys.stderr)
        return 2

    if args.provider == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("Error: ANTHROPIC_API_KEY not set.", file=sys.stderr)
            return 2
        runner = call_anthropic
    else:
        runner = call_stub

    # tp/fp/fn over a binary "did the output match expectation" view, where a
    # case is "positive" if it has a non-empty expected answer.
    tp = fp = fn = tn = 0
    case_results = []

    for case in cases:
        predicted = runner(case.get("input", ""), args.model)
        expected = case.get("expected", "")
        match_mode = case.get("match", "exact")
        passed = score(predicted, expected, match_mode)
        has_expectation = bool(expected.strip())

        if has_expectation and passed:
            tp += 1
        elif has_expectation and not passed:
            fn += 1
        elif not has_expectation and not predicted.strip():
            tn += 1
        else:
            fp += 1

        case_results.append(
            {
                "id": case.get("id"),
                "passed": passed,
                "expected": expected,
                "predicted": predicted[:500],
                "match": match_mode,
            }
        )

    total = len(cases)
    passed_count = sum(1 for r in case_results if r["passed"])
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    results = {
        "summary": {
            "total": total,
            "passed": passed_count,
            "failed": total - passed_count,
            "accuracy": passed_count / total,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "provider": args.provider,
            "model": args.model,
        },
        "cases": case_results,
    }

    output = json.dumps(results, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(output)
        print(f"Results written to {args.out}", file=sys.stderr)
    else:
        print(output)

    s = results["summary"]
    print(
        f"Done: {s['passed']}/{s['total']} passed "
        f"(accuracy={s['accuracy']:.1%}, precision={s['precision']:.2f}, "
        f"recall={s['recall']:.2f}, f1={s['f1']:.2f})",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
