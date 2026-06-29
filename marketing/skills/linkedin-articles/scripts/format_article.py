#!/usr/bin/env python3
"""
Format and validate a LinkedIn article draft.

Usage:
    python format_article.py <article_file.md>
    python format_article.py --stdin < article.md

Checks:
- Word count (LinkedIn articles: 700–2000 words optimal)
- Hook strength (first 3 lines must stand alone)
- Section structure (H2 headers present)
- CTA presence (closing call to action)
- Slop words (AI writing tells)
"""

import re
import sys
from pathlib import Path

SLOP_WORDS = [
    "delve", "leverage", "synergy", "robust", "cutting-edge", "game-changing",
    "seamlessly", "certainly", "absolutely", "of course", "I'd be happy",
    "comprehensive", "invaluable", "transformative", "harness the power",
]

OPTIMAL_MIN_WORDS = 700
OPTIMAL_MAX_WORDS = 2000


def count_words(text: str) -> int:
    return len(text.split())


def check_hook(lines: list[str]) -> list[str]:
    issues = []
    first_lines = [l.strip() for l in lines[:5] if l.strip() and not l.startswith("#")][:3]
    if not first_lines:
        issues.append("No opening lines found — article needs a hook.")
        return issues
    hook_text = " ".join(first_lines)
    if len(hook_text) > 400:
        issues.append("Hook is too long. First 3 lines should be under ~50 words total.")
    if "?" not in hook_text and len(first_lines) < 2:
        issues.append("Hook may be weak — consider a provocative question or bold statement.")
    return issues


def check_structure(text: str) -> list[str]:
    issues = []
    headers = re.findall(r"^#{2,3}\s+.+", text, re.MULTILINE)
    if len(headers) < 2:
        issues.append(f"Only {len(headers)} section header(s) found. Add H2 headers to structure the article.")
    return issues


def check_cta(text: str) -> list[str]:
    issues = []
    cta_signals = ["comment", "share", "newsletter", "follow", "reply", "dm", "link in"]
    last_300 = text[-300:].lower()
    if not any(signal in last_300 for signal in cta_signals):
        issues.append("No CTA detected in the closing. Add a clear call to action (comment, follow, subscribe).")
    return issues


def check_slop(text: str) -> list[str]:
    issues = []
    text_lower = text.lower()
    found = [w for w in SLOP_WORDS if w in text_lower]
    if found:
        issues.append(f"Slop words detected: {', '.join(found)}. Run through humanizing skill.")
    return issues


def analyze(text: str) -> None:
    lines = text.splitlines()
    word_count = count_words(text)

    print(f"📊 Word count: {word_count}", end="")
    if OPTIMAL_MIN_WORDS <= word_count <= OPTIMAL_MAX_WORDS:
        print(" ✓")
    elif word_count < OPTIMAL_MIN_WORDS:
        print(f" ⚠ (under optimal minimum of {OPTIMAL_MIN_WORDS})")
    else:
        print(f" ⚠ (over optimal maximum of {OPTIMAL_MAX_WORDS})")

    all_issues = (
        check_hook(lines)
        + check_structure(text)
        + check_cta(text)
        + check_slop(text)
    )

    if all_issues:
        print("\n⚠ Issues found:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("\n✓ Article passes all checks.")


def main() -> None:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Usage: python format_article.py <article.md>", file=sys.stderr)
        sys.exit(1)

    analyze(text)


if __name__ == "__main__":
    main()
