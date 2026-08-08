#!/usr/bin/env bash
# Validate JSON files, optionally against one JSON Schema.

set -euo pipefail

python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def iter_json_files(inputs: list[str]):
    seen = set()
    for raw in inputs:
        path = Path(raw).expanduser()
        candidates = [path] if path.is_file() else path.rglob("*.json") if path.is_dir() else []
        for candidate in candidates:
            if any(part in {".git", "node_modules", ".playwright-mcp"} for part in candidate.parts):
                continue
            resolved = candidate.resolve()
            if candidate.suffix == ".json" and resolved not in seen:
                seen.add(resolved)
                yield candidate


parser = argparse.ArgumentParser(description="Validate JSON files in one or more files/directories.")
parser.add_argument("paths", nargs="*", default=["."], help="JSON file or directory (default: current directory)")
parser.add_argument("--schema", help="Optional JSON Schema applied to every selected file")
args = parser.parse_args()

schema = None
if args.schema:
    schema_path = Path(args.schema).expanduser()
    if not schema_path.is_file():
        parser.error(f"schema file not found: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if importlib.util.find_spec("jsonschema") is None:
        parser.error("--schema requires the `jsonschema` Python package")
    import jsonschema

failures = []
files = list(iter_json_files(args.paths))
if not files:
    parser.error("no JSON files found")

for path in files:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if schema is not None:
            jsonschema.validate(instance=payload, schema=schema)
    except Exception as exc:
        failures.append(f"{path}: {exc}")

if failures:
    for failure in failures:
        print(failure, file=sys.stderr)
    raise SystemExit(1)

print(f"Validated {len(files)} JSON file(s).")
PY
