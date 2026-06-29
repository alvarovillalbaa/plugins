#!/usr/bin/env python3
"""
Validate a multi-touch sequence definition for gaps and issues.

Usage:
    python validate_sequence.py sequence.md
"""

import re
import sys
from pathlib import Path


def extract_touches(text: str) -> list[dict]:
    touches = []
    pattern = re.compile(
        r"##\s+Touch\s+(\d+)[^\n]*\n.*?Day\s+(\d+)",
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(text):
        touch_num = int(match.group(1))
        day = int(match.group(2))
        # Detect channel from context
        channel = "unknown"
        ctx = text[match.start():match.start() + 200].lower()
        if "linkedin" in ctx:
            channel = "linkedin"
        elif "email" in ctx:
            channel = "email"
        elif "phone" in ctx or "call" in ctx:
            channel = "phone"
        touches.append({"touch": touch_num, "day": day, "channel": channel})
    return sorted(touches, key=lambda t: t["day"])


def validate(touches: list[dict]) -> list[str]:
    issues = []

    if len(touches) < 3:
        issues.append(f"Only {len(touches)} touch(es) defined. Minimum recommended: 4.")
    if len(touches) > 10:
        issues.append(f"{len(touches)} touches is a lot. Consider capping at 8 for cold outreach.")

    # Check day spacing
    for i in range(1, len(touches)):
        gap = touches[i]["day"] - touches[i - 1]["day"]
        if gap < 2:
            issues.append(
                f"Touch {touches[i]['touch']} is only {gap} day(s) after touch {touches[i-1]['touch']}. "
                f"Minimum gap: 2 days."
            )
        if gap > 14:
            issues.append(
                f"Gap between touch {touches[i-1]['touch']} and {touches[i]['touch']} is {gap} days. "
                f"Prospect may forget who you are."
            )

    # Check channel diversity
    channels = [t["channel"] for t in touches]
    unique_channels = set(c for c in channels if c != "unknown")
    if len(unique_channels) < 2 and len(touches) >= 4:
        issues.append("Single-channel sequence. Mix email + LinkedIn for better response rates.")

    # Check for breakup email
    last_ctx = touches[-1] if touches else {}
    if last_ctx.get("touch", 0) >= 5 and "breakup" not in str(last_ctx):
        # Check the text for a breakup signal
        pass  # hard to detect without more context

    return issues


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_sequence.py <sequence.md>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    touches = extract_touches(text)

    if not touches:
        print("No touches found. Make sure each touch has '## Touch N' and 'Day N' in the header.")
        sys.exit(1)

    print(f"Found {len(touches)} touch(es):\n")
    for t in touches:
        print(f"  Touch {t['touch']:2d} | Day {t['day']:2d} | Channel: {t['channel']}")

    issues = validate(touches)

    if issues:
        print(f"\n⚠ {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✓ Sequence looks good.")


if __name__ == "__main__":
    main()
