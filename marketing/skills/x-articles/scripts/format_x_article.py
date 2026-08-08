#!/usr/bin/env python3
"""
Validate and format an X article draft.

Usage:
    python format_x_article.py <article.md>
"""

import re
import sys
from pathlib import Path

OPTIMAL_WORDS_MIN = 800
OPTIMAL_WORDS_MAX = 3000

SLOP_WORDS = [
    "delve", "leverage", "synergy", "robust", "seamlessly",
    "certainly", "absolutely", "comprehensive", "invaluable",
    "transformative", "harness the power",
]


def analyze(text: str) -> None:
    word_count = len(text.split())
    lines = text.strip().splitlines()

    print("=== X Article Check ===\n")

    # Word count
    print(f"Word count: {word_count}", end="")
    if OPTIMAL_WORDS_MIN <= word_count <= OPTIMAL_WORDS_MAX:
        print(" ✓")
    elif word_count < OPTIMAL_WORDS_MIN:
        print(f" ⚠ (under optimal minimum of {OPTIMAL_WORDS_MIN})")
    else:
        print(f" ⚠ (over optimal maximum of {OPTIMAL_WORDS_MAX})")

    # Opening paragraph
    first_para = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            first_para.append(stripped)
        elif first_para:
            break
    opening = " ".join(first_para)
    print(f"\nOpening: {opening[:120]}{'...' if len(opening) > 120 else ''}")
    if len(opening.split()) > 60:
        print("  ⚠ Opening paragraph is long. Keep it under 50 words to hook the reader.")
    else:
        print("  ✓ Opening length OK.")

    # Headers
    headers = [l for l in lines if re.match(r"^#{2,3}\s+", l)]
    print(f"\nSection headers: {len(headers)}", end="")
    if len(headers) >= 3:
        print(" ✓")
    else:
        print(" ⚠ (add more H2 sections to structure the article)")

    # Slop check
    text_lower = text.lower()
    found = [w for w in SLOP_WORDS if w in text_lower]
    if found:
        print(f"\n⚠ Slop words: {', '.join(found)}")
    else:
        print("\n✓ No slop words.")

    # CTA
    last_200 = text[-200:].lower()
    cta_signals = ["follow", "subscribe", "reply", "comment", "share", "newsletter"]
    if any(s in last_200 for s in cta_signals):
        print("✓ CTA detected in closing.")
    else:
        print("⚠ No CTA at end — add a follow/share/reply ask.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python format_x_article.py <article.md>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    analyze(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
