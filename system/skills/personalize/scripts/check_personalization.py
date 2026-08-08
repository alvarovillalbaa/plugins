#!/usr/bin/env python3
"""
Check that core personalization files are present and non-empty.

Usage:
    python check_personalization.py [plugin_root]
    python check_personalization.py .
"""

import sys
from pathlib import Path

EXPECTED_FILES = [
    "profile.yaml",
    "skills/voice/references",
    "skills/icp/references",
]

PROFILE_KEYS = [
    "name",
    "description",
    "voice",
    "icp",
]


def check_profile(root: Path) -> list[str]:
    issues = []
    profile = root / "profile.yaml"
    if not profile.exists():
        issues.append(f"Missing: {profile}")
        return issues

    text = profile.read_text(encoding="utf-8")
    for key in PROFILE_KEYS:
        if f"{key}:" not in text:
            issues.append(f"profile.yaml is missing key: '{key}'")

    return issues


def check_skill_dirs(root: Path) -> list[str]:
    issues = []
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        issues.append(f"No skills/ directory found at {root}")
        return issues

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            issues.append(f"Missing SKILL.md in: {skill_dir.name}")
        elif skill_md.stat().st_size < 50:
            issues.append(f"SKILL.md too small (possibly empty) in: {skill_dir.name}")

    return issues


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Checking personalization config at: {root.resolve()}\n")
    issues: list[str] = []
    issues.extend(check_profile(root))
    issues.extend(check_skill_dirs(root))

    if issues:
        print(f"⚠ {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("✓ Personalization config looks complete.")


if __name__ == "__main__":
    main()
