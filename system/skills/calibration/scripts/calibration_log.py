#!/usr/bin/env python3
"""
Manage a calibration log for skills and agents.

Usage:
    python calibration_log.py add --skill code-reviewer --change "Narrowed scope" --reason "Too verbose"
    python calibration_log.py list
    python calibration_log.py list --skill code-reviewer
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

DEFAULT_LOG = Path(".calibration-log.json")


def load(path: Path) -> list[dict]:
    if path.exists():
        return json.loads(path.read_text())
    return []


def save(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps(entries, indent=2))


def add_entry(args: argparse.Namespace) -> None:
    path = Path(args.log)
    entries = load(path)
    entry = {
        "date": str(date.today()),
        "skill": args.skill,
        "change": args.change,
        "reason": args.reason,
        "outcome": args.outcome or "",
    }
    entries.append(entry)
    save(path, entries)
    print(f"✓ Added calibration entry for '{args.skill}'.")


def list_entries(args: argparse.Namespace) -> None:
    path = Path(args.log)
    entries = load(path)
    if not entries:
        print("No calibration entries found.")
        return

    if args.skill:
        entries = [e for e in entries if e.get("skill") == args.skill]

    if not entries:
        print(f"No entries for skill '{args.skill}'.")
        return

    for e in sorted(entries, key=lambda x: x["date"], reverse=True):
        print(f"\n[{e['date']}] {e['skill']}")
        print(f"  Change : {e['change']}")
        print(f"  Reason : {e['reason']}")
        if e.get("outcome"):
            print(f"  Outcome: {e['outcome']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Calibration log manager")
    parser.add_argument("--log", default=str(DEFAULT_LOG), help="Log file path")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Add a calibration entry")
    add_p.add_argument("--skill", required=True)
    add_p.add_argument("--change", required=True)
    add_p.add_argument("--reason", required=True)
    add_p.add_argument("--outcome", default="")

    list_p = sub.add_parser("list", help="List calibration entries")
    list_p.add_argument("--skill", default="")

    args = parser.parse_args()
    if args.command == "add":
        add_entry(args)
    elif args.command == "list":
        list_entries(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
