#!/usr/bin/env python3
"""
Validate an X (Twitter) DM draft for common issues.

Usage:
    python check_dm.py "Hey [Name], saw your post about..."
    echo "Your message here" | python check_dm.py
"""

import sys

CHAR_LIMIT = 10000  # X DM char limit
OPENER_WARN = 150   # Ideal opener length

SLOP_PHRASES = [
    "i hope this finds you well",
    "i wanted to reach out",
    "touching base",
    "circle back",
    "synergy",
    "leverage",
    "per my last",
    "as per",
    "at your earliest convenience",
    "please don't hesitate",
]

LINK_WARNING = ["http://", "https://"]


def check(message: str) -> None:
    char_count = len(message)
    word_count = len(message.split())

    print("=== X DM Check ===\n")
    print(f"Characters: {char_count}", end="")
    if char_count > CHAR_LIMIT:
        print(f" ✗ (over {CHAR_LIMIT} char limit)")
    elif char_count > OPENER_WARN:
        print(f" ⚠ (consider trimming — DM openers work best under {OPENER_WARN} chars)")
    else:
        print(" ✓")
    print(f"Words: {word_count}")

    # Signal check
    signal_words = ["saw your", "your post", "your tweet", "your thread", "your reply",
                    "you shared", "you mentioned", "from your", "you wrote"]
    has_signal = any(s.lower() in message.lower() for s in signal_words)
    if has_signal:
        print("✓ Signal reference detected.")
    else:
        print("⚠ No signal reference. Reference something specific they did publicly.")

    # CTA check
    cta_words = ["call", "chat", "minutes", "talk", "connect", "worth", "useful"]
    has_cta = any(w in message.lower() for w in cta_words)
    if has_cta:
        print("✓ CTA detected.")
    else:
        print("⚠ No clear CTA. Add one ask at the end.")

    # Multiple CTAs
    cta_count = sum(1 for w in ["call?", "chat?", "talk?", "meet?", "connect?"] if w in message.lower())
    if cta_count > 1:
        print("⚠ Multiple CTAs detected. Pick one.")

    # Link in opener
    has_link = any(l in message for l in LINK_WARNING)
    if has_link:
        print("⚠ Link in DM — avoid links in first message (flags as spam).")

    # Slop phrases
    msg_lower = message.lower()
    found_slop = [p for p in SLOP_PHRASES if p in msg_lower]
    if found_slop:
        print(f"⚠ Cliché phrases: {', '.join(found_slop)}")
    else:
        print("✓ No slop phrases.")

    print()
    if char_count <= OPENER_WARN and has_signal and has_cta and not has_link and not found_slop:
        print("✓ DM looks good.")


def main() -> None:
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    elif not sys.stdin.isatty():
        message = sys.stdin.read().strip()
    else:
        print("Usage: python check_dm.py \"Your DM text here\"", file=sys.stderr)
        sys.exit(1)

    check(message)


if __name__ == "__main__":
    main()
