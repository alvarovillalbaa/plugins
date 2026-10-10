#!/usr/bin/env python3
"""Read-only local inventory for an explicitly selected AGENTS.md workspace.

This tool cannot inspect the connected Drive queue. Use the authorized connector
and SOURCES.md to establish remote artifact status.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Iterable


# This script deliberately holds NO copy of the AFS taxonomy. AFS is defined
# externally by the `use-afs` skill; duplicating its folder lists here is what
# caused them to drift out of sync. Surfaces are discovered from the filesystem
# instead, so this tool stays correct when the standard changes.
#
# The only contracts encoded here are brain-owned, not AFS-owned: the raw status
# frontmatter contract and the adaptation-mode vocabulary. See
# ../../brain/references/brain_contract.md

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


def instruction_files(root: Path) -> list[Path]:
    return sorted(iter_files(root, {"AGENTS.md"}))


def infer_mode(root: Path) -> str:
    """Read the explicit workspace's root guidance without guessing a taxonomy.

    Modes are brain vocabulary, not AFS vocabulary. When AGENTS.md does not
    declare one, report `undeclared` rather than guessing: deciding between
    strict and partial requires knowing the AFS taxonomy, which only `use-afs`
    is allowed to define.
    """
    guidance = root / "AGENTS.md"
    if not guidance.is_file():
        return "missing"

    text = read_prefix(guidance).lower()
    if "partial-afs" in text or "partial afs" in text:
        return "partial-afs"
    if "strict-afs" in text or "strict afs" in text:
        return "strict-afs"
    if re.search(r"\bnative(?: company)? (?:mode|standard)\b", text):
        return "native"
    return "undeclared"


def detect_shell(root: Path) -> tuple[Path, str]:
    """Locate the documentation shell and report which installation profile is in use.

    AFS places the shell at the root for empty or sparse folders and inside
    `docs/` for application repositories. Detect which applies rather than
    assuming; `use-afs` remains the authority on what belongs inside.

    A populated `docs/` is the application-profile signal. Root-level directories
    are not a useful counter-signal in an application repo, where most of them
    hold source code rather than documentation surfaces.
    """
    docs = root / "docs"
    if docs.is_dir() and any(
        p.is_dir() and p.name not in SKIP_DIRS and not p.name.startswith(".")
        for p in docs.iterdir()
    ):
        return docs, "docs"
    return root, "root"


def discover_surfaces(root: Path, depth: int = 2) -> dict[str, dict[str, object]]:
    """Inventory the directories that actually exist, without asserting a taxonomy.

    Descends one extra level into directories that contain only subdirectories,
    so type-first surfaces are reported individually rather than as one bucket.
    """
    found: dict[str, dict[str, object]] = {}
    if not root.is_dir():
        return found

    def walk(base: Path, prefix: str, level: int) -> None:
        try:
            entries = sorted(p for p in base.iterdir() if p.is_dir())
        except OSError:
            return
        for entry in entries:
            if entry.name in SKIP_DIRS or entry.name.startswith("."):
                continue
            name = f"{prefix}{entry.name}"
            children = [p for p in entry.iterdir() if p.is_dir() and p.name not in SKIP_DIRS]
            files = sum(1 for p in iter_files(entry) if p.is_file())
            only_dirs = bool(children) and not any(
                p.is_file() for p in entry.iterdir() if not p.name.startswith(".")
            )
            if only_dirs and level < depth:
                walk(entry, f"{name}/", level + 1)
            else:
                found[name] = {"path": str(entry), "files": files}

    walk(root, "", 1)
    return found


def classify_source(path: Path, fields: dict[str, str]) -> str:
    source = fields.get("source")
    if source:
        return source.lower()
    suffix = path.suffix.lower().lstrip(".")
    return suffix or "no-extension"


def intake_inventory(root: Path) -> dict[str, object]:
    """Inventory local legacy status metadata; this is not a Drive queue scan.

    Local captures may retain `status: unprocessed|processed|blocked` metadata.
    Reporting them supports a preservation audit without treating local files
    as the canonical raw store or inferring that the remote queue is empty.
    """
    by_status: Counter[str] = Counter()
    by_source: Counter[str] = Counter()
    by_dir: Counter[str] = Counter()
    blocked: list[dict[str, str]] = []
    total = 0

    for path in sorted(p for p in iter_files(root) if p.is_file()):
        if path.suffix.lower() not in {".md", ".markdown", ".txt", ".json"}:
            continue
        fields = parse_frontmatter(path)
        status = fields.get("status", "").lower()
        if status not in {"unprocessed", "processed", "blocked"}:
            continue

        total += 1
        by_status[status] += 1
        by_source[classify_source(path, fields)] += 1
        try:
            by_dir[str(path.parent.relative_to(root))] += 1
        except ValueError:
            by_dir[str(path.parent)] += 1
        if status == "blocked":
            blocked.append(
                {
                    "path": str(path),
                    "blocked_reason": fields.get("blocked_reason", ""),
                }
            )

    return {
        "total_files": total,
        "by_status": dict(sorted(by_status.items())),
        "by_source": dict(sorted(by_source.items())),
        "by_directory": dict(sorted(by_dir.items())),
        "blocked": blocked,
    }


def tool_inventory() -> dict[str, str | None]:
    return {tool: shutil.which(tool) for tool in TOOLS}


def build_inventory(root: Path, include_memory: bool) -> dict[str, object]:
    root = root.resolve()
    guidance = instruction_files(root)
    shell_root, profile = detect_shell(root)
    data: dict[str, object] = {
        "target_root": str(root),
        "instruction_files": [str(path) for path in guidance],
        "workspace_root": str(root),
        "mode": infer_mode(root),
        "shell_root": str(shell_root),
        "install_profile": profile,
        "surfaces": discover_surfaces(shell_root),
        "local_legacy_intake": intake_inventory(shell_root),
        "drive_intake": {
            "status": "not_inspected",
            "source_catalog": str(root / "SOURCES.md"),
            "reason": "Local inventory has no connected Drive access.",
        },
        "tools": tool_inventory(),
    }
    if include_memory:
        data["surface_file_counts"] = {
            name: info["files"] for name, info in data["surfaces"].items()  # type: ignore[index]
        }
    return data


def print_text(data: dict[str, object]) -> None:
    print(f"Target root: {data['target_root']}")
    print("Applicable scope guidance (nested files do not select a new workspace):")
    for path in data["instruction_files"]:  # type: ignore[index]
        print(f"  - {path}")
    print(f"Workspace root: {data['workspace_root']}")
    print(f"Mode: {data['mode']}")
    print(f"Install profile: {data['install_profile']} (shell: {data['shell_root']})")

    surfaces = data["surfaces"]  # type: ignore[assignment]
    print(f"\nDiscovered surfaces ({len(surfaces)}):")
    for name, info in surfaces.items():
        print(f"  {name}: {info['files']} files")
    print("  (taxonomy validation belongs to use-afs, not this script)")

    print("\nDrive intake: not inspected; inspect SOURCES.md with the authorized connector.")
    intake = data["local_legacy_intake"]  # type: ignore[assignment]
    print("\nLocal legacy status metadata (not the remote source queue):")
    print(f"  Total files: {intake['total_files']}")
    print(f"  By status: {intake['by_status']}")
    print(f"  By source: {intake['by_source']}")
    print(f"  By directory: {intake['by_directory']}")
    if intake["blocked"]:
        print("  Blocked:")
        for item in intake["blocked"]:
            reason = item.get("blocked_reason") or "unspecified"
            print(f"    - {item['path']} ({reason})")

    if "surface_file_counts" in data:
        print("\nMemory candidates (by discovered surface):")
        for name, count in data["surface_file_counts"].items():  # type: ignore[index]
            print(f"  {name}: {count}")

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
        help="include per-surface file counts for discovered surfaces",
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
