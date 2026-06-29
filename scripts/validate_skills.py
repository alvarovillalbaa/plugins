#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
XML_TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class ParseError(Exception):
    message: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.message} at line {self.line} column {self.column}"


def find_skill_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("SKILL.md"):
        parts = path.parts
        if "skills" in parts:
            files.append(path)
    return sorted(files)


def extract_frontmatter_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ParseError("missing frontmatter start", 1, 1)

    lines = text.splitlines()
    for idx in range(1, len(lines)):
        if lines[idx] == "---":
            return lines[1:idx]

    raise ParseError("missing frontmatter end", len(lines), 1)


def fold_block(lines: list[str]) -> str:
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line == "":
            if current:
                paragraphs.append(" ".join(current))
                current = []
            else:
                paragraphs.append("")
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs).rstrip("\n")


def parse_scalar(value: str, line_no: int) -> str:
    if value[0] in {'"', "'"}:
        quote = value[0]
        if len(value) < 2 or value[-1] != quote:
            raise ParseError("unterminated quoted scalar", line_no, len(value) + 1)
        return value[1:-1]

    bad = value.find(": ")
    if bad != -1:
        raise ParseError("mapping values are not allowed in this context", line_no, bad + 2)

    return value.strip()


def parse_mapping(lines: list[str], start: int, indent: int) -> tuple[dict[str, object], int]:
    data: dict[str, object] = {}
    i = start

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        current_indent = len(raw) - len(raw.lstrip(" "))
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ParseError("unexpected indentation", i + 1, indent + 1)

        line = raw[indent:]
        if ":" not in line:
            raise ParseError("expected key: value mapping", i + 1, indent + 1)

        key, remainder = line.split(":", 1)
        if not key.strip():
            raise ParseError("empty key", i + 1, indent + 1)
        if key != key.strip():
            raise ParseError("invalid key spacing", i + 1, indent + 1)

        if remainder and not remainder.startswith(" "):
            raise ParseError("invalid mapping syntax", i + 1, indent + len(key) + 2)

        value = remainder.lstrip(" ")

        if value in {"|", "|-", "|+", ">", ">-", ">+"}:
            block_indent = indent + 2
            block: list[str] = []
            j = i + 1
            while j < len(lines):
                next_raw = lines[j]
                next_stripped = next_raw.strip()
                next_indent = len(next_raw) - len(next_raw.lstrip(" "))
                if next_stripped and next_indent <= indent:
                    break
                if next_stripped:
                    if next_indent < block_indent:
                        raise ParseError("invalid block scalar indentation", j + 1, next_indent + 1)
                    block.append(next_raw[block_indent:])
                else:
                    block.append("")
                j += 1

            if value.startswith("|"):
                data[key] = "\n".join(block).rstrip("\n")
            else:
                data[key] = fold_block(block)
            i = j
            continue

        if value == "":
            child, j = parse_mapping(lines, i + 1, indent + 2)
            data[key] = child
            i = j
            continue

        data[key] = parse_scalar(value, i + 1)
        i += 1

    return data, i


def parse_frontmatter(path: Path) -> dict[str, object]:
    lines = extract_frontmatter_lines(path)
    data, index = parse_mapping(lines, 0, 0)
    if index != len(lines):
        raise ParseError("failed to parse complete frontmatter", index + 1, 1)
    return data


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        frontmatter = parse_frontmatter(path)
    except ParseError as exc:
        return [f"invalid YAML: {exc}"]

    if not isinstance(frontmatter, dict):
        return ["frontmatter must be a mapping"]

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name:
        errors.append("missing required field: name")
    else:
        if len(name) > 64:
            errors.append("invalid name: exceeds maximum length of 64 characters")
        if not NAME_RE.fullmatch(name):
            errors.append("invalid name: must contain only lowercase letters, numbers, and single hyphens")
        if name != path.parent.name:
            errors.append(
                f"invalid name: must match parent directory name `{path.parent.name}`"
            )

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("missing required field: description")
    else:
        if len(description) > 1024:
            errors.append("invalid description: exceeds maximum length of 1024 characters")
        if XML_TAG_RE.search(description):
            errors.append("invalid description: must not contain XML or HTML tags")

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            errors.append("invalid compatibility: must be a non-empty string when provided")
        elif len(compatibility) > 500:
            errors.append("invalid compatibility: exceeds maximum length of 500 characters")

    metadata = frontmatter.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        errors.append("invalid metadata: must be a mapping when provided")

    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    skill_files = find_skill_files(root)

    if not skill_files:
        print(f"No SKILL.md files found under {root}")
        return 0

    failures = 0
    for skill_file in skill_files:
        errors = validate_skill(skill_file)
        if not errors:
            continue
        failures += 1
        for error in errors:
            print(f"⚠ {skill_file.resolve()}: {error}")

    if failures:
        print(f"\nValidation failed for {failures} skill file(s).", file=sys.stderr)
        return 1

    skillctl = root / "scripts" / "skillctl.py"
    if skillctl.exists():
        checks = [
            [sys.executable, str(skillctl), "meta", "check", "--root", str(root), "--require-all"],
            [sys.executable, str(skillctl), "structure", "check", "--root", str(root)],
            [sys.executable, str(skillctl), "conflicts", "check", "--root", str(root)],
        ]
        for check in checks:
            result = subprocess.run(check, text=True)
            if result.returncode != 0:
                return result.returncode

    print(f"Validated {len(skill_files)} skill file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
