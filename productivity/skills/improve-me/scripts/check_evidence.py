#!/usr/bin/env python3
"""Audit an improve-me evidence ledger for provenance, freshness, and policy gaps."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


SOURCE_TYPES = {"current", "loaded_memory", "repo_local_memory", "approved_private"}
KINDS = {"fact", "inference"}


def parse_date(raw: object, field: str, item_id: str, errors: list[str]) -> dt.date | None:
    if raw in (None, "", "unknown"):
        return None
    if not isinstance(raw, str):
        errors.append(f"{item_id}: {field} must be an ISO date or 'unknown'")
        return None
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        errors.append(f"{item_id}: {field} is not a valid ISO date: {raw}")
        return None


def audit(payload: object, as_of: dt.date) -> dict[str, object]:
    items = payload.get("evidence") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        return {"status": "fail", "errors": ["input must be a list or an object with an evidence list"]}

    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    counts = {"fact": 0, "inference": 0, "current": 0, "stale": 0, "unknown": 0}

    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"item {index}: must be an object")
            continue
        item_id = str(item.get("id", "")).strip() or f"item-{index}"
        if item_id in seen:
            errors.append(f"{item_id}: duplicate id")
        seen.add(item_id)
        if not str(item.get("claim", "")).strip():
            errors.append(f"{item_id}: claim is required")
        if not str(item.get("source", "")).strip():
            errors.append(f"{item_id}: source is required")

        kind = item.get("kind")
        if kind not in KINDS:
            errors.append(f"{item_id}: kind must be fact or inference")
        else:
            counts[kind] += 1
        source_type = item.get("source_type")
        if source_type not in SOURCE_TYPES:
            errors.append(f"{item_id}: source_type is not allowed")
        if source_type == "approved_private" and item.get("access_approved") is not True:
            errors.append(f"{item_id}: approved_private evidence requires access_approved=true")
        if kind == "inference" and not item.get("basis_ids"):
            errors.append(f"{item_id}: inference requires non-empty basis_ids")

        observed = parse_date(item.get("observed_at", "unknown"), "observed_at", item_id, errors)
        fresh_until = parse_date(item.get("fresh_until"), "fresh_until", item_id, errors)
        if observed and observed > as_of:
            errors.append(f"{item_id}: observed_at is after as-of date")
        if fresh_until and observed and fresh_until < observed:
            errors.append(f"{item_id}: fresh_until precedes observed_at")
        if fresh_until and fresh_until < as_of:
            counts["stale"] += 1
            warnings.append(f"{item_id}: evidence is stale as of {as_of.isoformat()}")
        elif observed is None:
            counts["unknown"] += 1
            warnings.append(f"{item_id}: freshness is unknown")
        else:
            counts["current"] += 1

    unknown_basis = []
    for item in items:
        if isinstance(item, dict) and item.get("kind") == "inference":
            for basis in item.get("basis_ids", []):
                if str(basis) not in seen:
                    unknown_basis.append(f"{item.get('id', '<unknown>')}: missing basis id {basis}")
    errors.extend(unknown_basis)
    status = "fail" if errors else "warn" if warnings else "pass"
    return {"status": status, "as_of": as_of.isoformat(), "counts": counts, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON evidence ledger")
    parser.add_argument("--as-of", default=dt.date.today().isoformat(), help="ISO audit date")
    args = parser.parse_args()
    try:
        as_of = dt.date.fromisoformat(args.as_of)
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "errors": [str(exc)]}, indent=2))
        return 2
    result = audit(payload, as_of)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
