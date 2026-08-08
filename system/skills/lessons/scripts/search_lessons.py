#!/usr/bin/env python3
"""
Search a lessons library for relevant lessons.

Usage:
    python search_lessons.py --query "database migration"
    python search_lessons.py --category engineering
    python search_lessons.py --severity high
    python search_lessons.py --query "activation" --category product
"""

import argparse
import re
import sys
from pathlib import Path


def extract_lessons(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    lessons = []
    current: dict = {}

    for line in text.splitlines():
        # Detect lesson header
        header_match = re.match(r"^###\s+([A-Z0-9]+)\s+[—–-]\s+(.+)$", line)
        if header_match:
            if current:
                lessons.append(current)
            current = {
                "id": header_match.group(1),
                "title": header_match.group(2),
                "source": str(path),
            }
            continue

        # Parse key-value fields
        kv_match = re.match(r"^\*\*([^*]+)\*\*:\s+(.+)$", line)
        if kv_match and current:
            key = kv_match.group(1).lower()
            value = kv_match.group(2).strip()
            current[key] = value

    if current:
        lessons.append(current)

    return lessons


def search(lessons: list[dict], query: str, category: str, severity: str) -> list[dict]:
    results = []
    for lesson in lessons:
        if category and lesson.get("category", "").lower() != category.lower():
            continue
        if severity and lesson.get("severity", "").lower() != severity.lower():
            continue
        if query:
            searchable = " ".join([
                lesson.get("title", ""),
                lesson.get("lesson", ""),
                lesson.get("context", ""),
                lesson.get("action", ""),
            ]).lower()
            if query.lower() not in searchable:
                continue
        results.append(lesson)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Search lessons library")
    parser.add_argument("--query", default="", help="Keyword search")
    parser.add_argument("--category", default="", help="Filter by category")
    parser.add_argument("--severity", default="", help="Filter by severity")
    parser.add_argument("--dir", default=".", help="Directory to search for lesson files")
    args = parser.parse_args()

    base = Path(args.dir)
    all_lessons: list[dict] = []
    for md_file in sorted(base.rglob("*.md")):
        all_lessons.extend(extract_lessons(md_file))

    if not all_lessons:
        print("No lessons found.")
        return

    results = search(all_lessons, args.query, args.category, args.severity)

    if not results:
        print("No matching lessons.")
        return

    print(f"Found {len(results)} lesson(s):\n")
    for lesson in results:
        print(f"[{lesson.get('id', '?')}] {lesson.get('title', '')}")
        if lesson.get("lesson"):
            print(f"  Lesson   : {lesson['lesson']}")
        if lesson.get("context"):
            print(f"  Context  : {lesson['context']}")
        if lesson.get("action"):
            print(f"  Action   : {lesson['action']}")
        if lesson.get("severity"):
            print(f"  Severity : {lesson['severity']}")
        print()


if __name__ == "__main__":
    main()
