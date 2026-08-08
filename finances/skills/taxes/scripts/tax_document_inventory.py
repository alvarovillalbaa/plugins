#!/usr/bin/env python3
"""Scan a directory of tax documents and emit a categorized inventory."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ALLOWED_EXTENSIONS = {
    ".csv",
    ".doc",
    ".docx",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".txt",
    ".xlsx",
}

CATEGORY_RULES = [
    ("W-2 (Wages)", re.compile(r"\bw-?2\b|\bw2\b", re.IGNORECASE)),
    (
        "1099 (Income)",
        re.compile(r"\b1099(?:-(?:misc|nec|int|div|b|s|r|g|k|sa|c))?\b", re.IGNORECASE),
    ),
    ("1098 (Deductions)", re.compile(r"\b1098(?:-(?:t|e|c))?\b", re.IGNORECASE)),
    ("Charitable Donations", re.compile(r"donat|charit|contrib|501c", re.IGNORECASE)),
    (
        "Medical Expenses",
        re.compile(r"medic|health|dental|vision|hsa|fsa|pharma|rx", re.IGNORECASE),
    ),
    ("Property Tax", re.compile(r"property.?tax|prop.?tax|real.?estate", re.IGNORECASE)),
    ("Mortgage Interest", re.compile(r"mortgage|home.?loan", re.IGNORECASE)),
    (
        "Investment Records",
        re.compile(r"invest|stock|trade|capital|brokerage|dividend", re.IGNORECASE),
    ),
    (
        "Business/Self-Employment",
        re.compile(r"business|self.?employ|freelance|invoice|contract", re.IGNORECASE),
    ),
    (
        "Education/Dependents",
        re.compile(r"child|depend|daycare|tuition|student|529|education", re.IGNORECASE),
    ),
    ("Insurance", re.compile(r"insurance|premium", re.IGNORECASE)),
    ("State & Local Tax", re.compile(r"state.?tax|local.?tax|\bsalt\b", re.IGNORECASE)),
    ("Retirement", re.compile(r"retire|ira|401k|pension|roth", re.IGNORECASE)),
    ("Receipts & Expenses", re.compile(r"receipt|expense", re.IGNORECASE)),
]

COMMON_CATEGORIES = [
    "W-2 (Wages)",
    "1099 (Income)",
    "Receipts & Expenses",
    "Medical Expenses",
    "Charitable Donations",
    "Insurance",
    "Investment Records",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Categorize tax documents in a local directory without moving files."
    )
    parser.add_argument("docs_dir", help="Directory containing tax documents")
    parser.add_argument("--tax-year", default=str(datetime.now(timezone.utc).year))
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum directory depth to scan relative to docs_dir",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format",
    )
    return parser.parse_args()


def categorize(name: str) -> str:
    for category, pattern in CATEGORY_RULES:
        if pattern.search(name):
            return category
    return "Uncategorized"


def iter_files(root: Path, max_depth: int) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        try:
            rel_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if len(rel_parts) - 1 > max_depth:
            continue
        paths.append(path)
    return paths


def build_inventory(root: Path, tax_year: str, max_depth: int) -> dict:
    files = []
    for path in iter_files(root, max_depth=max_depth):
        stat = path.stat()
        rel_path = str(path.relative_to(root))
        category = categorize(path.name)
        modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime(
            "%Y-%m-%d"
        )
        files.append(
            {
                "name": path.name,
                "path": rel_path,
                "size_bytes": stat.st_size,
                "modified": modified,
                "category": category,
            }
        )

    by_category: dict[str, list[dict]] = defaultdict(list)
    by_name: dict[str, list[str]] = defaultdict(list)
    for item in files:
        by_category[item["category"]].append(item)
        by_name[item["name"].lower()].append(item["path"])

    duplicate_names = {
        name: paths for name, paths in by_name.items() if len(paths) > 1
    }
    categories_found = sorted(by_category.keys())
    missing_categories = [cat for cat in COMMON_CATEGORIES if cat not in categories_found]

    return {
        "docs_dir": str(root),
        "tax_year": tax_year,
        "total_files": len(files),
        "categories_found": categories_found,
        "missing_categories": missing_categories,
        "duplicate_names": duplicate_names,
        "files": files,
        "by_category": [
            {
                "category": category,
                "count": len(items),
                "files": [item["name"] for item in items],
            }
            for category, items in sorted(by_category.items())
        ],
    }


def render_markdown(inventory: dict) -> str:
    lines = [
        f"# Tax Document Inventory - {inventory['tax_year']}",
        "",
        f"- Source folder: `{inventory['docs_dir']}`",
        f"- Total files: `{inventory['total_files']}`",
        "",
        "## Documents by Category",
        "",
        "| Category | Count | Files |",
        "|----------|-------|-------|",
    ]

    for group in inventory["by_category"]:
        files = ", ".join(group["files"]) if group["files"] else "-"
        lines.append(f"| {group['category']} | {group['count']} | {files} |")

    lines.extend(["", "## Likely Missing Categories", ""])
    if inventory["missing_categories"]:
        for category in inventory["missing_categories"]:
            lines.append(f"- {category}")
    else:
        lines.append("- None from the common baseline set")

    lines.extend(["", "## Duplicate Filenames", ""])
    if inventory["duplicate_names"]:
        for name, paths in sorted(inventory["duplicate_names"].items()):
            rendered_paths = ", ".join(f"`{path}`" for path in paths)
            lines.append(f"- `{name}`: {rendered_paths}")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `likely missing` means the file was not found in the scanned folder; it may not apply.",
            "- This script is non-destructive and does not move or rename files.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = Path(args.docs_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Directory not found: {root}")

    inventory = build_inventory(root=root, tax_year=args.tax_year, max_depth=args.max_depth)
    if args.format == "json":
        print(json.dumps(inventory, indent=2, sort_keys=True))
    else:
        print(render_markdown(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
