#!/usr/bin/env python3
"""Audit command coverage, ownership conflicts, excess, and portability."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MAX_COMMAND_LINES = 100
REQUIRED_FRONTMATTER = ("name", "description", "argument-hint", "allowed-tools")
PORTABILITY_PATTERNS = (
    ("named organization", re.compile(r"\b(?:cl" + r"ous|agent\s+" + r"company)\b", re.IGNORECASE)),
    ("maintainer identity", re.compile(r"alvaro" + r"villalbaa?", re.IGNORECASE)),
    ("absolute macOS user path", re.compile(r"/Users/[^/\s]+/")),
    ("absolute Linux user path", re.compile(r"/home/[^/\s]+/")),
    ("absolute Windows user path", re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\s]+\\\\")),
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
EXAMPLE_EMAIL_DOMAINS = {"example.com", "example.net", "example.org"}
PLACEHOLDER_RE = re.compile(r"\[(?:TODO|PLACEHOLDER)(?::[^\]]*)?\]|Placeholder for ", re.IGNORECASE)
CAPABILITY_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
OWNER_RE = re.compile(r"^[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*$")
REPLACEMENT_REF_RE = re.compile(r"\b[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*\b")


@dataclass(frozen=True)
class CommandRecord:
    path: str
    capability: str
    owner: str
    boundary: str


@dataclass(frozen=True)
class DepartmentSummary:
    name: str
    command_count: int
    cataloged_count: int


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return result
        match = re.match(r"^([A-Za-z][A-Za-z0-9-]*):\s*(.*)$", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return {}


def parse_profile_list(path: Path, key: str) -> list[str]:
    values: list[str] = []
    active = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw == f"{key}:":
            active = True
            continue
        if active and raw and not raw.startswith(" "):
            break
        if not active:
            continue
        match = re.fullmatch(r"  - ([a-z0-9]+(?:-[a-z0-9]+)*)", raw)
        if match:
            values.append(match.group(1))
    return values


def command_slug(public_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", public_name.casefold()).strip("-")


def normalized_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        text = parts[2] if len(parts) == 3 else text
    return re.sub(r"\s+", " ", text).strip().casefold()


def read_catalog(path: Path) -> tuple[dict[str, Any], list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, [f"{path}: missing command capability registry"]
    except json.JSONDecodeError as exc:
        return {}, [f"{path}:{exc.lineno}: invalid JSON: {exc.msg}"]
    if not isinstance(data, dict):
        return {}, [f"{path}: registry root must be an object"]
    return data, []


def parse_records(data: dict[str, Any], catalog: Path, root: Path) -> tuple[list[CommandRecord], list[dict[str, str]], list[str]]:
    failures: list[str] = []
    records: list[CommandRecord] = []
    retired: list[dict[str, str]] = []
    label = rel(catalog, root) if catalog.is_relative_to(root) else catalog.as_posix()

    if data.get("schema_version") != 1:
        failures.append(f"{label}: schema_version must be 1")
    if not str(data.get("selection_rule", "")).strip():
        failures.append(f"{label}: selection_rule is required")

    raw_commands = data.get("commands")
    if not isinstance(raw_commands, list):
        failures.append(f"{label}: commands must be a list")
        raw_commands = []
    for index, raw in enumerate(raw_commands):
        location = f"{label}:commands[{index}]"
        if not isinstance(raw, dict):
            failures.append(f"{location}: entry must be an object")
            continue
        values = {key: str(raw.get(key, "")).strip() for key in ("path", "capability", "owner", "boundary")}
        for key, value in values.items():
            if not value:
                failures.append(f"{location}: {key} is required")
        if values["capability"] and not CAPABILITY_RE.fullmatch(values["capability"]):
            failures.append(f"{location}: capability must use lowercase dot/hyphen notation")
        if values["owner"] and not OWNER_RE.fullmatch(values["owner"]):
            failures.append(f"{location}: owner must be `<plugin>/<skill>`")
        if all(values.values()):
            records.append(CommandRecord(**values))

    raw_retired = data.get("retired", [])
    if not isinstance(raw_retired, list):
        failures.append(f"{label}: retired must be a list")
        raw_retired = []
    for index, raw in enumerate(raw_retired):
        location = f"{label}:retired[{index}]"
        if not isinstance(raw, dict):
            failures.append(f"{location}: entry must be an object")
            continue
        item = {key: str(raw.get(key, "")).strip() for key in ("path", "replacement", "reason")}
        for key, value in item.items():
            if not value:
                failures.append(f"{location}: {key} is required")
        if all(item.values()):
            retired.append(item)
    return records, retired, failures


def audit(root: Path, catalog_path: Path | None = None) -> tuple[list[str], list[DepartmentSummary], list[CommandRecord], list[dict[str, str]]]:
    root = root.resolve()
    catalog = (catalog_path or root / "references" / "command-capabilities.json").resolve()
    failures: list[str] = []
    data, catalog_failures = read_catalog(catalog)
    failures.extend(catalog_failures)
    records, retired, record_failures = parse_records(data, catalog, root) if data else ([], [], [])
    failures.extend(record_failures)

    departments = sorted(
        path.parent
        for path in root.glob("*/profile.yaml")
        if (path.parent / "commands").is_dir() and (path.parent / "skills").is_dir()
    )
    command_files = sorted(
        path
        for department in departments
        for path in (department / "commands").glob("*.md")
        if path.name != "README.md"
    )
    actual_paths = {rel(path, root) for path in command_files}
    catalog_paths = [record.path for record in records]

    for duplicate, count in sorted(Counter(catalog_paths).items()):
        if count > 1:
            failures.append(f"{rel(catalog, root)}: duplicate command path `{duplicate}`")
    for duplicate, count in sorted(Counter(record.capability for record in records).items()):
        if count > 1:
            failures.append(f"{rel(catalog, root)}: duplicate capability `{duplicate}`")

    missing_from_catalog = sorted(actual_paths - set(catalog_paths))
    missing_from_disk = sorted(set(catalog_paths) - actual_paths)
    if missing_from_catalog:
        failures.append("commands missing from capability registry: " + ", ".join(missing_from_catalog))
    if missing_from_disk:
        failures.append("cataloged commands missing on disk: " + ", ".join(missing_from_disk))

    skill_owners = {
        f"{department.name}/{skill.parent.name}"
        for department in departments
        for skill in (department / "skills").glob("*/SKILL.md")
    }
    for record in records:
        if record.owner not in skill_owners:
            failures.append(f"{record.path}: canonical owner `{record.owner}` does not exist")
    active_command_ids = {
        f"{path.parts[-3]}/{path.stem}"
        for path in command_files
    }
    replacement_targets = skill_owners | active_command_ids
    for item in retired:
        refs = REPLACEMENT_REF_RE.findall(item["replacement"])
        if not refs:
            failures.append(f"{item['path']}: replacement must name at least one `<plugin>/<skill-or-command>` target")
        for ref in refs:
            if ref not in replacement_targets:
                failures.append(f"{item['path']}: replacement target `{ref}` does not exist")

    summaries: list[DepartmentSummary] = []
    cataloged_by_department = Counter(Path(record.path).parts[0] for record in records)
    record_by_path = {record.path: record for record in records}
    body_hashes: dict[str, list[str]] = {}
    for department in departments:
        profile = department / "profile.yaml"
        profiled = set(parse_profile_list(profile, "commands"))
        files = sorted(path for path in (department / "commands").glob("*.md") if path.name != "README.md")
        stems = {path.stem for path in files}
        if profiled != stems:
            missing_profile = sorted(stems - profiled)
            missing_disk = sorted(profiled - stems)
            if missing_profile:
                failures.append(f"{rel(profile, root)}: commands missing from profile: " + ", ".join(missing_profile))
            if missing_disk:
                failures.append(f"{rel(profile, root)}: profiled commands missing on disk: " + ", ".join(missing_disk))

        local_skills = {path.parent.name for path in (department / "skills").glob("*/SKILL.md")}
        for path in files:
            path_label = rel(path, root)
            frontmatter = parse_frontmatter(path)
            if not frontmatter:
                failures.append(f"{path_label}: missing or unterminated frontmatter")
                continue
            for field in REQUIRED_FRONTMATTER:
                if not frontmatter.get(field, "").strip():
                    failures.append(f"{path_label}: missing command frontmatter `{field}`")
            name = frontmatter.get("name", "")
            if name and command_slug(name) != path.stem:
                failures.append(f"{path_label}: public name `{name}` must normalize to `{path.stem}`")
            if name in local_skills:
                failures.append(
                    f"{path_label}: public name `{name}` conflicts with same-plugin skill `{department.name}/{name}`"
                )
            allowed_tools = frontmatter.get("allowed-tools", "")
            if allowed_tools and not (allowed_tools.startswith("[") and allowed_tools.endswith("]")):
                failures.append(f"{path_label}: allowed-tools must use bracketed list syntax")
            if allowed_tools and "Skill" not in allowed_tools:
                failures.append(f"{path_label}: routed commands must allow the `Skill` tool")

            text = path.read_text(encoding="utf-8")
            record = record_by_path.get(path_label)
            if record:
                owner_skill = record.owner.split("/", 1)[1]
                if not re.search(rf"(?<![a-z0-9-]){re.escape(owner_skill)}(?![a-z0-9-])", text, re.IGNORECASE):
                    failures.append(f"{path_label}: does not route to canonical owner `{record.owner}`")
            line_count = len(text.splitlines())
            if line_count > MAX_COMMAND_LINES:
                failures.append(f"{path_label}: {line_count} lines exceeds the {MAX_COMMAND_LINES}-line command limit")
            if PLACEHOLDER_RE.search(text):
                failures.append(f"{path_label}: unresolved placeholder text is not allowed")
            for label, pattern in PORTABILITY_PATTERNS:
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    failures.append(f"{path_label}:{line}: {label} is not allowed in reusable commands")
            for match in EMAIL_RE.finditer(text):
                if match.group(1).casefold() in EXAMPLE_EMAIL_DOMAINS:
                    continue
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{path_label}:{line}: email address is not allowed in reusable commands")

            digest = hashlib.sha256(normalized_body(path).encode("utf-8")).hexdigest()
            body_hashes.setdefault(digest, []).append(path_label)

        summaries.append(
            DepartmentSummary(
                name=department.name,
                command_count=len(files),
                cataloged_count=cataloged_by_department[department.name],
            )
        )

    for paths in sorted(body_hashes.values()):
        if len(paths) > 1:
            failures.append("exact duplicate command bodies: " + ", ".join(paths))
    for item in retired:
        if (root / item["path"]).exists():
            failures.append(f"{item['path']}: retired command must remain absent")
    if not departments:
        failures.append("no department plugins with commands and skills directories found")
    return failures, summaries, records, retired


def render_report(root: Path, summaries: list[DepartmentSummary], records: list[CommandRecord], retired: list[dict[str, str]], selection_rule: str) -> str:
    lines = [
        "# Commands Review — Current",
        "",
        "## Result",
        "",
        f"- {len(summaries)} department plugins reviewed.",
        f"- {sum(item.command_count for item in summaries)} active commands cataloged with unique capabilities and canonical skill owners.",
        f"- {len(retired)} redundant or conflicting commands retired with functional replacements.",
        "- Every active command is present on disk, in its plugin profile, and in the capability registry.",
        "- Atomic capabilities remain directly invokable as skills; commands are not added merely to mirror a skill.",
        "",
        "## Selection rule",
        "",
        selection_rule,
        "",
        "## Plugin coverage",
        "",
        "| Plugin | Active commands | Cataloged |",
        "| --- | ---: | ---: |",
    ]
    for summary in summaries:
        lines.append(f"| `{summary.name}` | {summary.command_count} | {summary.cataloged_count} |")
    lines.extend(
        [
            "",
            "## Capability ownership",
            "",
            "| Command | Capability | Canonical owner | Boundary |",
            "| --- | --- | --- | --- |",
        ]
    )
    for record in records:
        command = f"`{Path(record.path).parts[0]}/{Path(record.path).stem}`"
        lines.append(f"| {command} | `{record.capability}` | `{record.owner}` | {record.boundary} |")
    lines.extend(
        [
            "",
            "## Retired commands",
            "",
            "| Removed file | Replacement | Reason |",
            "| --- | --- | --- |",
        ]
    )
    for item in retired:
        lines.append(f"| `{item['path']}` | `{item['replacement']}` | {item['reason']} |")
    lines.extend(
        [
            "",
            "## Verification contract",
            "",
            "Run `python3 scripts/audit_commands.py .` to enforce inventory parity, unique capability ownership, explicit routing to resolvable owners, Skill-tool availability, same-plugin skill/command collision prevention, thin command size, duplicate-body rejection, and portability checks.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit plugin commands for complete, unique, necessary, and reusable workflows."
    )
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--catalog", help="override command capability registry path")
    parser.add_argument("--report", help="write the current Markdown coverage matrix")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    catalog = Path(args.catalog).resolve() if args.catalog else root / "references" / "command-capabilities.json"
    failures, summaries, records, retired = audit(root, catalog)

    for summary in summaries:
        print(f"{summary.name}: {summary.cataloged_count}/{summary.command_count} commands cataloged")
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    if args.report:
        data, _ = read_catalog(catalog)
        report = render_report(root, summaries, records, retired, str(data["selection_rule"]))
        report_path = Path(args.report)
        if not report_path.is_absolute():
            report_path = root / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        print(f"Wrote {rel(report_path, root)}")
    print(f"Validated {len(records)} command capability contract(s) across {len(summaries)} plugin(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
