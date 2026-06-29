#!/usr/bin/env python3
"""
Scan a directory and list all sales collateral with metadata.

Usage:
    python collateral_inventory.py [path_to_collateral_dir]
    python collateral_inventory.py ./collateral
"""

import sys
import re
from pathlib import Path
from datetime import datetime

COLLATERAL_TYPES = {
    "one-pager": ["one-pager", "one_pager", "1-pager"],
    "battlecard": ["battlecard", "battle-card", "battle_card"],
    "case-study": ["case-study", "case_study", "case study"],
    "deck": ["deck", "slides", "presentation"],
    "datasheet": ["datasheet", "data-sheet", "data_sheet"],
    "email": ["email", "template"],
    "proposal": ["proposal", "quote", "sow"],
}


def classify(filename: str) -> str:
    name_lower = filename.lower()
    for ctype, keywords in COLLATERAL_TYPES.items():
        if any(k in name_lower for k in keywords):
            return ctype
    return "other"


def extract_audience(text: str) -> str:
    match = re.search(r"(?:audience|for|target)[:\s]+([^\n]+)", text, re.IGNORECASE)
    return match.group(1).strip()[:60] if match else "—"


def scan(directory: Path) -> None:
    files = sorted(directory.rglob("*.md")) + sorted(directory.rglob("*.pdf"))
    if not files:
        print(f"No collateral files found in: {directory}")
        return

    print(f"\n{'File':<40} {'Type':<12} {'Audience':<30} {'Modified'}")
    print("-" * 100)

    for path in files:
        rel = str(path.relative_to(directory))
        ctype = classify(path.name)
        audience = "—"
        if path.suffix == ".md":
            try:
                text = path.read_text(encoding="utf-8")
                audience = extract_audience(text)
            except Exception:
                pass
        mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
        print(f"{rel:<40} {ctype:<12} {audience:<30} {mtime}")

    print(f"\nTotal: {len(files)} file(s)")


def main() -> None:
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)
    scan(directory)


if __name__ == "__main__":
    main()
