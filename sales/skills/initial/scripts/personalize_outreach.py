#!/usr/bin/env python3
"""
Merge prospect data into an outreach template.

Usage:
    python personalize_outreach.py --template template.txt --prospect prospect.json
    python personalize_outreach.py --template template.txt --name "Alice Chen" --company "Acme" --title "VP Eng"

Template variables: {{name}}, {{first_name}}, {{company}}, {{title}}, {{signal}}
"""

import argparse
import json
import re
import sys
from pathlib import Path


def load_prospect(args: argparse.Namespace) -> dict:
    if args.prospect:
        path = Path(args.prospect)
        if not path.exists():
            print(f"Error: {path} not found", file=sys.stderr)
            sys.exit(1)
        return json.loads(path.read_text())

    return {
        "name": args.name or "",
        "company": args.company or "",
        "title": args.title or "",
        "signal": args.signal or "",
    }


def merge(template: str, data: dict) -> str:
    first_name = data.get("name", "").split()[0] if data.get("name") else ""
    merged = template
    merged = merged.replace("{{name}}", data.get("name", ""))
    merged = merged.replace("{{first_name}}", first_name)
    merged = merged.replace("{{company}}", data.get("company", ""))
    merged = merged.replace("{{title}}", data.get("title", ""))
    merged = merged.replace("{{signal}}", data.get("signal", ""))
    return merged


def check_unfilled(text: str) -> list[str]:
    return re.findall(r"\{\{[^}]+\}\}", text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge prospect data into outreach template")
    parser.add_argument("--template", required=True, help="Template file path")
    parser.add_argument("--prospect", help="JSON file with prospect data")
    parser.add_argument("--name", help="Prospect full name")
    parser.add_argument("--company", help="Prospect company")
    parser.add_argument("--title", help="Prospect title")
    parser.add_argument("--signal", help="Personalization signal (recent news/activity)")
    args = parser.parse_args()

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"Error: template {template_path} not found", file=sys.stderr)
        sys.exit(1)

    template = template_path.read_text(encoding="utf-8")
    data = load_prospect(args)
    result = merge(template, data)

    unfilled = check_unfilled(result)
    if unfilled:
        print(f"⚠ Unfilled variables: {', '.join(unfilled)}", file=sys.stderr)

    print(result)


if __name__ == "__main__":
    main()
