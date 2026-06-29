#!/usr/bin/env python3
"""Read-only inventory for a BRAIN.md-bounded second brain."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Iterable


AFS_MEMORY_DIRS = (
    "logs",
    "lessons",
    "facts",
    "fixes",
    "steers",
    "models",
    "reflections",
)

AFS_OPERATIONAL_DIRS = (
    "audits",
    "raw",
    "plans",
    "specs",
    "sources",
    "lib",
    "objects",
    "templates",
)

AFS_TRUTH_DIRS = (
    "references",
    "cookbook",
    "knowledge",
    "runbooks",
    "research",
)

TOOLS = (
    "xurl",
    "defuddle",
    "yt-dlp",
    "pdftotext",
    "mutool",
    "pdfinfo",
    "tesseract",
    "pandoc",
    "jq",
)

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".cache",
}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")


def iter_files(root: Path, names: set[str] | None = None) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            if names is None or filename in names:
                yield base / filename


def read_prefix(path: Path, limit: int = 65536) -> str:
    try:
        with path.open("rb") as handle:
            return handle.read(limit).decode("utf-8", errors="replace")
    except OSError:
        return ""


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = read_prefix(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = FIELD_RE.match(line.strip())
        if field:
            fields[field.group(1).lower()] = field.group(2).strip().strip("\"'")
    return fields


def detect_brains(root: Path) -> list[Path]:
    return sorted(iter_files(root, {"BRAIN.md"}))


def infer_mode(root: Path, brain_files: list[Path]) -> str:
    if not brain_files:
        return "missing"
    if len(brain_files) > 1:
        return "ambiguous"

    text = read_prefix(brain_files[0]).lower()
    if "native" in text:
        return "native"
    if "partial-afs" in text or "partial afs" in text:
        return "partial-afs"
    if "strict-afs" in text or "strict afs" in text:
        return "strict-afs"

    known_dirs = set(AFS_MEMORY_DIRS + AFS_OPERATIONAL_DIRS + AFS_TRUTH_DIRS)
    existing = {p.name for p in root.iterdir() if p.is_dir()} if root.exists() else set()
    return "partial-afs" if existing & known_dirs else "strict-afs"


def active_root(root: Path, brain_files: list[Path]) -> Path:
    if len(brain_files) == 1:
        return brain_files[0].parent
    return root


def folder_map(root: Path) -> dict[str, dict[str, str | bool]]:
    mapping: dict[str, dict[str, str | bool]] = {}
    for name in AFS_MEMORY_DIRS + AFS_OPERATIONAL_DIRS + AFS_TRUTH_DIRS:
        path = root / name
        mapping[name] = {
            "path": str(path),
            "exists": path.is_dir(),
        }
    return mapping


def classify_source(path: Path, fields: dict[str, str]) -> str:
    source = fields.get("source")
    if source:
        return source.lower()
    suffix = path.suffix.lower().lstrip(".")
    return suffix or "no-extension"


def raw_inventory(root: Path) -> dict[str, object]:
    raw_root = root / "raw"
    result: dict[str, object] = {
        "path": str(raw_root),
        "exists": raw_root.is_dir(),
        "total_files": 0,
        "by_status": {},
        "by_source": {},
        "blocked": [],
    }
    if not raw_root.is_dir():
        return result

    by_status: Counter[str] = Counter()
    by_source: Counter[str] = Counter()
    blocked: list[dict[str, str]] = []
    total = 0

    for path in sorted(p for p in iter_files(raw_root) if p.is_file()):
        total += 1
        fields = parse_frontmatter(path)
        status = fields.get("status", "unprocessed").lower() or "unprocessed"
        source = classify_source(path, fields)
        by_status[status] += 1
        by_source[source] += 1
        if status == "blocked":
            blocked.append(
                {
                    "path": str(path),
                    "blocked_reason": fields.get("blocked_reason", ""),
                }
            )

    result["total_files"] = total
    result["by_status"] = dict(sorted(by_status.items()))
    result["by_source"] = dict(sorted(by_source.items()))
    result["blocked"] = blocked
    return result


def memory_inventory(root: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for name in AFS_MEMORY_DIRS:
        directory = root / name
        if not directory.is_dir():
            result[name] = {"exists": False, "files": 0}
            continue
        count = sum(1 for path in iter_files(directory) if path.is_file())
        result[name] = {"exists": True, "files": count}
    return result


def tool_inventory() -> dict[str, str | None]:
    return {tool: shutil.which(tool) for tool in TOOLS}


def build_inventory(root: Path, include_memory: bool) -> dict[str, object]:
    root = root.resolve()
    brain_files = detect_brains(root)
    boundary = active_root(root, brain_files)
    data: dict[str, object] = {
        "target_root": str(root),
        "brain_count": len(brain_files),
        "brain_files": [str(path) for path in brain_files],
        "active_root": str(boundary),
        "mode": infer_mode(boundary, brain_files),
        "folders": folder_map(boundary),
        "raw": raw_inventory(boundary),
        "tools": tool_inventory(),
    }
    if include_memory:
        data["memory"] = memory_inventory(boundary)
    return data


def print_text(data: dict[str, object]) -> None:
    print(f"Target root: {data['target_root']}")
    print(f"Brain count: {data['brain_count']}")
    for path in data["brain_files"]:  # type: ignore[index]
        print(f"  - {path}")
    print(f"Active root: {data['active_root']}")
    print(f"Mode: {data['mode']}")

    raw = data["raw"]  # type: ignore[assignment]
    print("\nRaw queue:")
    print(f"  Path: {raw['path']}")
    print(f"  Exists: {raw['exists']}")
    print(f"  Total files: {raw['total_files']}")
    print(f"  By status: {raw['by_status']}")
    print(f"  By source: {raw['by_source']}")
    if raw["blocked"]:
        print("  Blocked:")
        for item in raw["blocked"]:
            reason = item.get("blocked_reason") or "unspecified"
            print(f"    - {item['path']} ({reason})")

    if "memory" in data:
        print("\nMemory candidates:")
        memory = data["memory"]  # type: ignore[assignment]
        for name, item in memory.items():
            print(f"  {name}: {item['files'] if item['exists'] else 0}")

    print("\nTools:")
    tools = data["tools"]  # type: ignore[assignment]
    for tool, path in tools.items():
        print(f"  {tool}: {path or 'missing'}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="target root to inspect")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--include-memory",
        action="store_true",
        help="include repo-local AFS Memory folder counts",
    )
    args = parser.parse_args()

    data = build_inventory(Path(args.root), include_memory=args.include_memory)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print_text(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
