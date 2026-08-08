#!/usr/bin/env python3
"""Audit plugin agents for coverage, overlap, necessity, and portability."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = ("Primary skills", "Routing boundaries")
PORTABILITY_PATTERNS = (
    ("named organization", re.compile(r"\b(?:cl" + r"ous|agent\s+" + r"company)\b", re.IGNORECASE)),
    ("maintainer identity", re.compile(r"alvaro" + r"villalbaa?", re.IGNORECASE)),
    ("absolute macOS user path", re.compile(r"/Users/[^/\s]+/")),
    ("absolute Linux user path", re.compile(r"/home/[^/\s]+/")),
    ("absolute Windows user path", re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\s]+\\\\")),
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
EXAMPLE_EMAIL_DOMAINS = {"example.com", "example.net", "example.org"}
SKILL_REF_RE = re.compile(r"^- `([a-z0-9]+(?:-[a-z0-9]+)*)`(?:\s|$)", re.MULTILINE)
HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
MAX_AGENT_LINES = 220
HIGH_OVERLAP_RATIO = 0.75
HIGH_OVERLAP_MIN_SHARED = 1


@dataclass(frozen=True)
class AgentRecord:
    department: str
    name: str
    path: Path
    skills: frozenset[str]
    boundary: str


@dataclass(frozen=True)
class DepartmentSummary:
    name: str
    skill_count: int
    covered_skill_count: int
    agent_count: int


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


def section(text: str, heading: str) -> str:
    matches = list(HEADING_RE.finditer(text))
    wanted = heading.casefold()
    for index, match in enumerate(matches):
        if match.group(1).strip().casefold() != wanted:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[match.end():end].strip()
    return ""


def scope_declaration(text: str) -> str:
    explicit = section(text, "Scope")
    if explicit:
        return explicit
    match = re.search(r"^\*\*Scope:\*\*\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def normalized_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        text = parts[2] if len(parts) == 3 else text
    return re.sub(r"\s+", " ", text).strip().casefold()


def audit(root: Path) -> tuple[list[str], list[DepartmentSummary], list[AgentRecord]]:
    root = root.resolve()
    failures: list[str] = []
    summaries: list[DepartmentSummary] = []
    records: list[AgentRecord] = []
    departments = sorted(
        path.parent
        for path in root.glob("*/profile.yaml")
        if (path.parent / "agents").is_dir() and (path.parent / "skills").is_dir()
    )
    all_skill_names = {
        path.parent.name
        for department in departments
        for path in (department / "skills").glob("*/SKILL.md")
    }

    for department in departments:
        profile = department / "profile.yaml"
        profile_agents = set(parse_profile_list(profile, "agents"))
        profile_skills = set(parse_profile_list(profile, "skills"))
        agent_files = sorted(path for path in (department / "agents").glob("*.md") if path.name != "README.md")
        agent_stems = {path.stem for path in agent_files}
        if profile_agents != agent_stems:
            missing_profile = sorted(agent_stems - profile_agents)
            missing_disk = sorted(profile_agents - agent_stems)
            if missing_profile:
                failures.append(f"{rel(profile, root)}: agents missing from profile: " + ", ".join(missing_profile))
            if missing_disk:
                failures.append(f"{rel(profile, root)}: profiled agents missing on disk: " + ", ".join(missing_disk))

        local_records: list[AgentRecord] = []
        for path in agent_files:
            label = rel(path, root)
            text = path.read_text(encoding="utf-8")
            frontmatter = parse_frontmatter(path)
            if not frontmatter:
                failures.append(f"{label}: missing or unterminated frontmatter")
                continue
            for field in ("name", "description"):
                if not frontmatter.get(field, "").strip():
                    failures.append(f"{label}: missing agent frontmatter `{field}`")
            if frontmatter.get("name") and frontmatter["name"] != path.stem:
                failures.append(f"{label}: agent name `{frontmatter['name']}` must match file stem `{path.stem}`")
            for required in REQUIRED_SECTIONS:
                if not section(text, required):
                    failures.append(f"{label}: missing or empty `## {required}` section")
            if not scope_declaration(text):
                failures.append(f"{label}: missing or empty Scope declaration")
            skills = frozenset(SKILL_REF_RE.findall(section(text, "Primary skills")))
            if not skills:
                failures.append(f"{label}: Primary skills must list at least one skill")
            for skill in sorted(skills - all_skill_names):
                failures.append(f"{label}: references unknown primary skill `{skill}`")
            if len(text.splitlines()) > MAX_AGENT_LINES:
                failures.append(f"{label}: exceeds the {MAX_AGENT_LINES}-line reusable-agent limit")
            for portability_label, pattern in PORTABILITY_PATTERNS:
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    failures.append(f"{label}:{line}: {portability_label} is not allowed in reusable agents")
            for match in EMAIL_RE.finditer(text):
                if match.group(1).casefold() in EXAMPLE_EMAIL_DOMAINS:
                    continue
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{label}:{line}: email address is not allowed in reusable agents")
            record = AgentRecord(
                department=department.name,
                name=path.stem,
                path=path,
                skills=skills,
                boundary=section(text, "Routing boundaries"),
            )
            records.append(record)
            local_records.append(record)

        covered = set().union(*(record.skills for record in local_records)) if local_records else set()
        uncovered = sorted(profile_skills - covered)
        if uncovered:
            failures.append(f"{rel(profile, root)}: local skills missing agent coverage: " + ", ".join(uncovered))

        for index, left in enumerate(local_records):
            for right in local_records[index + 1:]:
                shared = left.skills & right.skills
                if left.skills == right.skills:
                    failures.append(
                        f"{left.department}/agents: exact duplicate primary-skill coverage for `{left.name}` and `{right.name}`"
                    )
                    continue
                denominator = min(len(left.skills), len(right.skills))
                ratio = len(shared) / denominator if denominator else 0
                if len(shared) < HIGH_OVERLAP_MIN_SHARED or ratio < HIGH_OVERLAP_RATIO:
                    continue
                if right.name not in left.boundary or left.name not in right.boundary:
                    failures.append(
                        f"{left.department}/agents: high-overlap agents `{left.name}` and `{right.name}` "
                        f"share {len(shared)}/{denominator} skills without mutual routing boundaries"
                    )

        summaries.append(
            DepartmentSummary(
                name=department.name,
                skill_count=len(profile_skills),
                covered_skill_count=len(profile_skills & covered),
                agent_count=len(agent_files),
            )
        )

    body_hashes: dict[str, list[str]] = {}
    for record in records:
        digest = hashlib.sha256(normalized_body(record.path).encode("utf-8")).hexdigest()
        body_hashes.setdefault(digest, []).append(rel(record.path, root))
    for paths in sorted(body_hashes.values()):
        if len(paths) > 1:
            failures.append("exact duplicate agent bodies: " + ", ".join(paths))
    for duplicate, count in sorted(Counter(record.name for record in records).items()):
        if count > 1:
            failures.append(f"duplicate agent public name `{duplicate}` appears {count} times")
    if not departments:
        failures.append("no department plugins with agents and skills directories found")
    return failures, summaries, records


def render_report(summaries: list[DepartmentSummary], records: list[AgentRecord]) -> str:
    lines = [
        "# Agents Review — Current",
        "",
        "## Result",
        "",
        f"- {len(summaries)} department plugins reviewed.",
        f"- {len(records)} generalized agents provide full coverage for {sum(item.skill_count for item in summaries)} plugin skills.",
        "- Every agent is registered in its plugin profile and declares explicit routing boundaries.",
        "- Exact duplicates are rejected; high-overlap roles require mutual handoff boundaries.",
        "",
        "## Plugin coverage",
        "",
        "| Plugin | Agents | Skills covered |",
        "| --- | ---: | ---: |",
    ]
    for summary in summaries:
        lines.append(f"| `{summary.name}` | {summary.agent_count} | {summary.covered_skill_count}/{summary.skill_count} |")
    lines.extend(
        [
            "",
            "## Agent capability routing",
            "",
            "| Agent | Primary skills |",
            "| --- | --- |",
        ]
    )
    for record in records:
        skills = ", ".join(f"`{skill}`" for skill in sorted(record.skills))
        lines.append(f"| `{record.department}/{record.name}` | {skills} |")
    lines.extend(
        [
            "",
            "## Verification contract",
            "",
            "Run `python3 scripts/audit_agents.py .` to enforce profile parity, complete same-plugin skill coverage, resolvable skills, explicit routing boundaries, duplicate and high-overlap detection, bounded size, and portability checks.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit plugin agents for complete, non-conflicting, necessary, and reusable coverage."
    )
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--report", help="write the current Markdown coverage matrix")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    failures, summaries, records = audit(root)

    for summary in summaries:
        print(
            f"{summary.name}: {summary.covered_skill_count}/{summary.skill_count} skills covered "
            f"by {summary.agent_count} agent(s)"
        )
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        print(f"Agent audit failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1
    if args.report:
        report_path = Path(args.report)
        if not report_path.is_absolute():
            report_path = root / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_report(summaries, records), encoding="utf-8")
        print(f"Wrote {rel(report_path, root)}")
    print(f"Validated {len(records)} agent contract(s) across {len(summaries)} plugin(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
