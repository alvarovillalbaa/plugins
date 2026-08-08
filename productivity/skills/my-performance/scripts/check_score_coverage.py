#!/usr/bin/env python3
"""Validate evidence sufficiency and weighted coverage in a performance review."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def iso_date(value: object) -> dt.date | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def validate(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return {"status": "fail", "errors": ["input must be a JSON object"]}
    errors: list[str] = []
    warnings: list[str] = []
    role = str(payload.get("role", "")).strip()
    period = payload.get("period", {})
    start = iso_date(period.get("start")) if isinstance(period, dict) else None
    end = iso_date(period.get("end")) if isinstance(period, dict) else None
    if not role:
        errors.append("role is required")
    if not start or not end or start > end:
        errors.append("period requires valid start and end dates")

    evidence = payload.get("evidence", [])
    criteria = payload.get("criteria", [])
    if not isinstance(evidence, list) or not isinstance(criteria, list) or not criteria:
        errors.append("evidence must be a list and criteria a non-empty list")
        return {"status": "fail", "errors": errors}

    by_id: dict[str, dict[str, object]] = {}
    for index, item in enumerate(evidence, 1):
        if not isinstance(item, dict):
            errors.append(f"evidence {index} must be an object")
            continue
        item_id = str(item.get("id", "")).strip()
        if not item_id or item_id in by_id:
            errors.append(f"evidence {index} requires a unique id")
            continue
        by_id[item_id] = item

    total_weight = 0.0
    scoreable_weight = 0.0
    result_criteria: list[dict[str, object]] = []
    for index, criterion in enumerate(criteria, 1):
        if not isinstance(criterion, dict):
            errors.append(f"criterion {index} must be an object")
            continue
        criterion_id = str(criterion.get("id", "")).strip() or f"criterion-{index}"
        try:
            weight = float(criterion.get("weight"))
            if weight <= 0:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{criterion_id}: weight must be positive")
            continue
        total_weight += weight
        ids = criterion.get("evidence_ids", [])
        if not isinstance(ids, list):
            errors.append(f"{criterion_id}: evidence_ids must be a list")
            ids = []
        valid_items = []
        for item_id in ids:
            item = by_id.get(str(item_id))
            if not item:
                errors.append(f"{criterion_id}: unknown evidence id {item_id}")
                continue
            observed = iso_date(item.get("observed_at"))
            if start and end and observed and start <= observed <= end:
                valid_items.append(item)
            else:
                warnings.append(f"{criterion_id}: evidence {item_id} is undated or outside the review period")
        sources = {str(item.get("source", "")).strip() for item in valid_items if str(item.get("source", "")).strip()}
        direct = any(item.get("authoritative_direct_measure") is True for item in valid_items)
        scoreable = direct or len(sources) >= 2
        if scoreable:
            scoreable_weight += weight
            if not isinstance(criterion.get("score"), (int, float)):
                errors.append(f"{criterion_id}: scoreable criterion requires a numeric score")
        elif criterion.get("score") is not None:
            errors.append(f"{criterion_id}: insufficient evidence; score must be null")
        result_criteria.append({"id": criterion_id, "scoreable": scoreable, "in_period_evidence": len(valid_items)})

    coverage = scoreable_weight / total_weight if total_weight else 0.0
    overall = payload.get("overall_score")
    if overall is not None and coverage < 0.75:
        errors.append("overall_score requires at least 75% weighted coverage")
    if overall is not None and not isinstance(overall, (int, float)):
        errors.append("overall_score must be numeric or null")
    status = "fail" if errors else "warn" if warnings else "pass"
    return {
        "status": status,
        "weighted_coverage": round(coverage, 4),
        "overall_score_allowed": coverage >= 0.75,
        "criteria": result_criteria,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Structured performance review JSON")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "errors": [str(exc)]}, indent=2))
        return 2
    result = validate(payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
