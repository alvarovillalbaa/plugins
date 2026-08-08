#!/usr/bin/env python3
"""Score a JSON prospect with a company-defined, JSON-based ICP model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MISSING = object()
OPERATORS = {
    "between",
    "contains",
    "eq",
    "exists",
    "falsy",
    "gt",
    "gte",
    "in",
    "lt",
    "lte",
    "ne",
    "not_in",
    "truthy",
}


class ModelError(ValueError):
    """Raised when an ICP model cannot be evaluated safely."""


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ModelError(f"cannot read {label} `{path}`: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ModelError(f"invalid JSON in {label} `{path}`: {exc}") from exc
    if not isinstance(value, dict):
        raise ModelError(f"{label} must be a JSON object")
    return value


def lookup(value: dict[str, Any], path: str) -> Any:
    current: Any = value
    for segment in path.split("."):
        if not isinstance(current, dict) or segment not in current:
            return MISSING
        current = current[segment]
    return current


def compare(actual: Any, operator: str, expected: Any = None) -> bool:
    if operator == "exists":
        return (actual is not MISSING) is bool(expected)
    if actual is MISSING:
        return False
    if operator == "truthy":
        return bool(actual)
    if operator == "falsy":
        return not bool(actual)
    if operator == "eq":
        return actual == expected
    if operator == "ne":
        return actual != expected
    if operator in {"in", "not_in"}:
        if not isinstance(expected, list):
            raise ModelError(f"operator `{operator}` requires an array value")
        result = actual in expected
        return result if operator == "in" else not result
    if operator == "contains":
        if not isinstance(actual, (str, list, tuple, set, dict)):
            return False
        return expected in actual
    if operator == "between":
        if not isinstance(expected, list) or len(expected) != 2:
            raise ModelError("operator `between` requires a two-item array value")
        return expected[0] <= actual <= expected[1]
    if operator == "gt":
        return actual > expected
    if operator == "gte":
        return actual >= expected
    if operator == "lt":
        return actual < expected
    if operator == "lte":
        return actual <= expected
    raise ModelError(f"unsupported operator `{operator}`")


def validate_rule(rule: Any, path: str, *, weighted: bool) -> dict[str, Any]:
    if not isinstance(rule, dict):
        raise ModelError(f"{path} must be an object")
    for key in ("id", "path", "operator"):
        if not isinstance(rule.get(key), str) or not rule[key].strip():
            raise ModelError(f"{path}.{key} must be a non-empty string")
    if rule["operator"] not in OPERATORS:
        raise ModelError(f"{path}.operator is unsupported: {rule['operator']}")
    if weighted:
        weight = rule.get("weight")
        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
            raise ModelError(f"{path}.weight must be a positive number")
    return rule


def validate_model(model: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    criteria = model.get("criteria")
    disqualifiers = model.get("disqualifiers", [])
    if not isinstance(criteria, list) or not criteria:
        raise ModelError("model.criteria must be a non-empty array")
    if not isinstance(disqualifiers, list):
        raise ModelError("model.disqualifiers must be an array")
    checked_criteria = [
        validate_rule(rule, f"model.criteria[{index}]", weighted=True)
        for index, rule in enumerate(criteria)
    ]
    checked_disqualifiers = [
        validate_rule(rule, f"model.disqualifiers[{index}]", weighted=False)
        for index, rule in enumerate(disqualifiers)
    ]
    return checked_criteria, checked_disqualifiers


def label_for_score(model: dict[str, Any], score: float) -> str:
    thresholds = model.get("thresholds", [])
    if not isinstance(thresholds, list):
        raise ModelError("model.thresholds must be an array")
    parsed: list[tuple[float, str]] = []
    for index, item in enumerate(thresholds):
        if not isinstance(item, dict):
            raise ModelError(f"model.thresholds[{index}] must be an object")
        minimum, label = item.get("min"), item.get("label")
        if not isinstance(minimum, (int, float)) or isinstance(minimum, bool):
            raise ModelError(f"model.thresholds[{index}].min must be numeric")
        if not isinstance(label, str) or not label.strip():
            raise ModelError(f"model.thresholds[{index}].label must be a non-empty string")
        parsed.append((float(minimum), label))
    for minimum, label in sorted(parsed, reverse=True):
        if score >= minimum:
            return label
    return "Unclassified"


def score_prospect(
    model: dict[str, Any], prospect: dict[str, Any], *, strict_missing: bool = False
) -> dict[str, Any]:
    criteria, disqualifiers = validate_model(model)
    results: list[dict[str, Any]] = []
    total_weight = sum(float(rule["weight"]) for rule in criteria)
    matched_weight = 0.0

    for rule in criteria:
        actual = lookup(prospect, rule["path"])
        if strict_missing and actual is MISSING:
            raise ModelError(f"prospect is missing criterion field `{rule['path']}`")
        matched = compare(actual, rule["operator"], rule.get("value"))
        if matched:
            matched_weight += float(rule["weight"])
        results.append(
            {
                "id": rule["id"],
                "label": rule.get("label", rule["id"]),
                "matched": matched,
                "weight": rule["weight"],
                "actual": None if actual is MISSING else actual,
            }
        )

    dq_results: list[dict[str, Any]] = []
    for rule in disqualifiers:
        actual = lookup(prospect, rule["path"])
        matched = compare(actual, rule["operator"], rule.get("value"))
        dq_results.append(
            {
                "id": rule["id"],
                "label": rule.get("label", rule["id"]),
                "matched": matched,
                "actual": None if actual is MISSING else actual,
            }
        )

    disqualified = any(item["matched"] for item in dq_results)
    raw_score = round(100 * matched_weight / total_weight, 2)
    score = 0.0 if disqualified else raw_score
    return {
        "model": model.get("name", "ICP model"),
        "prospect": prospect.get("name", prospect.get("id", "Prospect")),
        "score": score,
        "raw_score": raw_score,
        "matched_weight": matched_weight,
        "total_weight": total_weight,
        "disqualified": disqualified,
        "status": "Disqualified" if disqualified else label_for_score(model, score),
        "criteria": results,
        "disqualifiers": dq_results,
    }


def render_text(result: dict[str, Any]) -> str:
    lines = [
        f"ICP score: {result['prospect']}",
        f"Model: {result['model']}",
        f"Score: {result['score']:.2f}% ({result['matched_weight']:g}/{result['total_weight']:g})",
        f"Status: {result['status']}",
        "",
        "Criteria:",
    ]
    for item in result["criteria"]:
        marker = "+" if item["matched"] else "-"
        lines.append(f"  {marker} {item['label']} (weight {item['weight']:g})")
    matched_dqs = [item for item in result["disqualifiers"] if item["matched"]]
    if matched_dqs:
        lines.extend(["", "Disqualifiers:"])
        lines.extend(f"  ! {item['label']}" for item in matched_dqs)
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score a JSON prospect using an explicit, reusable ICP model."
    )
    parser.add_argument("--model", type=Path, required=True, help="ICP scoring model JSON")
    parser.add_argument("--prospect", type=Path, required=True, help="Prospect data JSON")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument(
        "--strict-missing",
        action="store_true",
        help="Fail when a criterion field is absent instead of treating it as unmatched.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        model = load_object(args.model, "model")
        prospect = load_object(args.prospect, "prospect")
        result = score_prospect(model, prospect, strict_missing=args.strict_missing)
    except (ModelError, TypeError) as exc:
        print(f"score_prospect: {exc}", file=sys.stderr)
        return 2
    if args.output == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
