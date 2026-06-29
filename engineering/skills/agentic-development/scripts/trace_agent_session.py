#!/usr/bin/env python3
"""Parse an agentic-dev tool-call trace (JSONL) into a session summary.

Reads the trace emitted by hooks/pre-tool.sh (one JSON object per line) and
produces either a markdown summary or a JSON rollup: total calls, per-tool
counts, the call timeline, and the session wall-clock span.

Usage:
  trace_agent_session.py --trace .agentic/traces/<id>.jsonl
  trace_agent_session.py --trace <file> --format json
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime


def load_events(path: str) -> list[dict]:
    events = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"warning: skipping malformed line {line_no}", file=sys.stderr)
    return events


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def summarize(events: list[dict]) -> dict:
    tool_counts = Counter(e.get("tool", "unknown") for e in events)
    timestamps = [t for t in (parse_ts(e.get("ts")) for e in events) if t]
    span_seconds = None
    if len(timestamps) >= 2:
        span_seconds = (max(timestamps) - min(timestamps)).total_seconds()

    return {
        "total_calls": len(events),
        "unique_tools": len(tool_counts),
        "tool_counts": dict(tool_counts.most_common()),
        "started_at": min(timestamps).isoformat() if timestamps else None,
        "ended_at": max(timestamps).isoformat() if timestamps else None,
        "span_seconds": span_seconds,
        "timeline": [
            {"ts": e.get("ts"), "tool": e.get("tool")} for e in events
        ],
    }


def render_markdown(summary: dict, session: str) -> str:
    lines = [f"# Agentic Session Summary: {session}", ""]
    lines.append(f"- Total tool calls: {summary['total_calls']}")
    lines.append(f"- Unique tools: {summary['unique_tools']}")
    if summary["started_at"]:
        lines.append(f"- Started: {summary['started_at']}")
        lines.append(f"- Ended: {summary['ended_at']}")
    if summary["span_seconds"] is not None:
        lines.append(f"- Wall-clock span: {summary['span_seconds']:.0f}s")
    lines += ["", "## Tool usage", ""]
    for tool, count in summary["tool_counts"].items():
        lines.append(f"- `{tool}`: {count}")
    lines += ["", "## Timeline", ""]
    for entry in summary["timeline"]:
        lines.append(f"- {entry['ts']} → `{entry['tool']}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize an agentic-dev trace.")
    parser.add_argument("--trace", required=True, help="Path to the JSONL trace file.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        events = load_events(args.trace)
    except FileNotFoundError:
        print(f"Error: trace not found: {args.trace}", file=sys.stderr)
        return 2

    summary = summarize(events)

    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        session = args.trace.rsplit("/", 1)[-1].replace(".jsonl", "")
        print(render_markdown(summary, session))
    return 0


if __name__ == "__main__":
    sys.exit(main())
