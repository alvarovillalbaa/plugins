#!/usr/bin/env python3
"""Run every bundled Python contract test in an isolated process."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


def discover(root: Path) -> list[Path]:
    tests = set(root.glob("scripts/tests/test_*.py"))
    for department in (
        "system",
        "marketing",
        "sales",
        "engineering",
        "product",
        "finances",
        "productivity",
    ):
        tests.update((root / department / "skills").glob("*/scripts/test_*.py"))
    discovered: list[Path] = []
    for path in tests:
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        if "unittest.main(" in source or re.search(r"^\s*def test_", source, re.MULTILINE):
            discovered.append(path)
    return sorted(discovered)


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    if not root.is_dir():
        print(f"Test root is not a directory: {root}", file=sys.stderr)
        return 2
    tests = discover(root)
    if not tests:
        print(f"No bundled Python contract tests found under {root}")
        return 0

    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    failures: list[Path] = []
    for test in tests:
        relative = test.relative_to(root)
        print(f"\n==> {relative}", flush=True)
        try:
            completed = subprocess.run(
                [sys.executable, str(test)],
                cwd=root,
                env=environment,
                timeout=300,
                check=False,
            )
        except subprocess.TimeoutExpired:
            print(f"Timed out after 300 seconds: {relative}", file=sys.stderr)
            failures.append(relative)
            continue
        if completed.returncode != 0:
            failures.append(relative)

    if failures:
        print("\nBundled contract test failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"\nPassed {len(tests)} bundled Python contract test file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
