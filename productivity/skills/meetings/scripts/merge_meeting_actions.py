#!/usr/bin/env python3
"""Merge meeting actions and flag unresolved fields or cross-meeting conflicts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def parse_timestamp(value: object) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def merge(payload: object) -> dict[str, object]:
    meetings = payload.get("meetings") if isinstance(payload, dict) else payload
    if not isinstance(meetings, list):
        return {"status": "fail", "errors": ["input must be a list or an object with a meetings list"]}
    errors: list[str] = []
    warnings: list[str] = []
    actions: list[dict[str, object]] = []
    action_by_id: dict[str, dict[str, object]] = {}
    decisions: dict[str, tuple[str, str]] = {}
    windows: list[tuple[str, dt.datetime, dt.datetime]] = []

    for index, meeting in enumerate(meetings, 1):
        if not isinstance(meeting, dict):
            errors.append(f"meeting {index} must be an object")
            continue
        meeting_id = str(meeting.get("meeting_id", "")).strip() or f"meeting-{index}"
        start = parse_timestamp(meeting.get("scheduled_start"))
        end = parse_timestamp(meeting.get("scheduled_end"))
        if start and end:
            if start >= end:
                errors.append(f"{meeting_id}: scheduled_start must precede scheduled_end")
            else:
                windows.append((meeting_id, start, end))

        for decision in meeting.get("decisions", []):
            if not isinstance(decision, dict):
                errors.append(f"{meeting_id}: decision must be an object")
                continue
            key = str(decision.get("key", "")).strip()
            text = str(decision.get("text", "")).strip()
            if key and text:
                prior = decisions.get(key)
                if prior and prior[0].casefold() != text.casefold():
                    warnings.append(f"decision conflict for {key}: {prior[1]} vs {meeting_id}")
                else:
                    decisions[key] = (text, meeting_id)

        raw_actions = meeting.get("actions", [])
        if not isinstance(raw_actions, list):
            errors.append(f"{meeting_id}: actions must be a list")
            continue
        for action_index, action in enumerate(raw_actions, 1):
            if not isinstance(action, dict):
                errors.append(f"{meeting_id}: action {action_index} must be an object")
                continue
            action_id = str(action.get("id", "")).strip()
            if not action_id:
                errors.append(f"{meeting_id}: action {action_index} requires an id")
                continue
            normalized = dict(action)
            normalized["source_meeting"] = meeting_id
            prior = action_by_id.get(action_id)
            if prior:
                comparable = (str(prior.get("action", "")), str(prior.get("owner", "")), str(prior.get("due_date", "")))
                current = (str(action.get("action", "")), str(action.get("owner", "")), str(action.get("due_date", "")))
                if comparable != current:
                    warnings.append(f"action conflict for {action_id}: {prior['source_meeting']} vs {meeting_id}")
                continue
            if not str(action.get("action", "")).strip():
                errors.append(f"{meeting_id}: action {action_id} requires action text")
            if not str(action.get("owner", "")).strip():
                warnings.append(f"{meeting_id}: action {action_id} has unresolved owner")
            if not str(action.get("due_date", "")).strip():
                warnings.append(f"{meeting_id}: action {action_id} has unresolved due date")
            action_by_id[action_id] = normalized
            actions.append(normalized)

    for index, (left_id, left_start, left_end) in enumerate(windows):
        for right_id, right_start, right_end in windows[index + 1 :]:
            if left_start < right_end and right_start < left_end:
                warnings.append(f"schedule overlap: {left_id} and {right_id}")

    actions.sort(key=lambda item: (str(item.get("due_date", "9999-12-31")), str(item.get("owner", "")), str(item.get("id", ""))))
    status = "fail" if errors else "warn" if warnings else "pass"
    return {"status": status, "meetings": len(meetings), "actions": actions, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON meeting portfolio")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "errors": [str(exc)]}, indent=2))
        return 2
    result = merge(payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
