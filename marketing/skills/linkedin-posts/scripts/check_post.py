#!/usr/bin/env python3
"""
Validate a LinkedIn post before publishing.

Usage:
    python check_post.py <post.txt>
    echo "Post text..." | python check_post.py --stdin
"""

import re
import sys
from pathlib import Path

CHAR_CUTOFF = 210  # LinkedIn "see more" threshold
OPTIMAL_WORDS_MIN = 100
OPTIMAL_WORDS_MAX = 350

SLOP_WORDS = [
    "delve", "leverage", "synergy", "robust", "cutting-edge", "game-changing",
    "seamlessly", "certainly", "absolutely", "I'd be happy", "comprehensive",
    "invaluable", "transformative", "harness the power", "crucial", "pivotal",
]

ENGAGEMENT_SIGNALS = [
    "?", "comment", "share", "what do you think", "thoughts?",
    "agree?", "reply", "follow", "tag someone",
]


def analyze(text: str) -> None:
    lines = text.strip().splitlines()
    word_count = len(text.split())
    char_count = len(text)
    first_line = lines[0].strip() if lines else ""
    first_line_chars = len(first_line)

    print("=== LinkedIn Post Check ===\n")

    # Hook analysis
    print(f"Hook (first line): {first_line[:80]}{'...' if len(first_line) > 80 else ''}")
    print(f"  Length: {first_line_chars} chars", end="")
    if first_line_chars > CHAR_CUTOFF:
        print(f" ⚠ (over {CHAR_CUTOFF}-char feed cutoff — hook will be cut off)")
    elif first_line_chars < 30:
        print(" ⚠ (very short — may not hook reader)")
    else:
        print(" ✓")

    # Length
    print(f"\nWord count: {word_count}", end="")
    if OPTIMAL_WORDS_MIN <= word_count <= OPTIMAL_WORDS_MAX:
        print(" ✓")
    elif word_count < OPTIMAL_WORDS_MIN:
        print(f" ⚠ (under optimal minimum of {OPTIMAL_WORDS_MIN})")
    else:
        print(f" ⚠ (over optimal maximum of {OPTIMAL_WORDS_MAX})")

    print(f"Total chars: {char_count}")

    # Slop check
    text_lower = text.lower()
    found_slop = [w for w in SLOP_WORDS if w in text_lower]
    if found_slop:
        print(f"\n⚠ Slop words: {', '.join(found_slop)}")
        print("  → Run through humanizing skill before publishing.")
    else:
        print("\n✓ No slop words detected.")

    # Engagement signal
    has_engagement = any(s in text_lower for s in ENGAGEMENT_SIGNALS)
    if has_engagement:
        print("✓ Engagement signal (question or CTA) detected.")
    else:
        print("⚠ No clear engagement signal. Add a question or CTA at the end.")

    # Multiple CTAs
    cta_count = sum(1 for s in ["comment", "share", "follow", "subscribe", "dm me"] if s in text_lower)
    if cta_count > 2:
        print(f"⚠ Multiple CTAs ({cta_count}) detected. Stick to one ask per post.")


def main() -> None:
    if "--stdin" in sys.argv or not sys.stdin.isatty():
        text = sys.stdin.read()
    elif len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"Error: {path} not found", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
    else:
        print("Usage: python check_post.py <post.txt>", file=sys.stderr)
        sys.exit(1)

    analyze(text)


if __name__ == "__main__":
    main()
