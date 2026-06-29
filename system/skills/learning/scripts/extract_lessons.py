#!/usr/bin/env python3
"""
Extract lesson cards from a markdown post-mortem or retrospective.

Looks for structured lesson blocks marked with ```yaml id: ...``` and
outputs them as a lessons index.

Usage:
    python extract_lessons.py retrospective.md
    python extract_lessons.py retrospective.md --output lessons.json
"""

import json
import re
import sys
from pathlib import Path


def extract_yaml_blocks(text: str) -> list[str]:
    pattern = re.compile(r"```ya?ml\n(.*?)```", re.DOTALL)
    return [m.group(1).strip() for m in pattern.finditer(text)]


def parse_simple_yaml(block: str) -> dict:
    result = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"')
    return result


def is_lesson_card(d: dict) -> bool:
    return "id" in d and "lesson" in d


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python extract_lessons.py <file.md> [--output <out.json>]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    blocks = extract_yaml_blocks(text)
    lessons = [parse_simple_yaml(b) for b in blocks if is_lesson_card(parse_simple_yaml(b))]

    if not lessons:
        print("No lesson cards found. Add blocks like:\n```yaml\nid: my-lesson\nlesson: ...\n```")
        return

    print(f"Found {len(lessons)} lesson card(s):\n")
    for lesson in lessons:
        print(f"  [{lesson.get('id')}] {lesson.get('lesson', '')[:80]}")
        if lesson.get("category"):
            print(f"    Category: {lesson['category']}")
        if lesson.get("severity"):
            print(f"    Severity: {lesson['severity']}")
        print()

    if output_path:
        output_path.write_text(json.dumps(lessons, indent=2))
        print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
