#!/usr/bin/env python3
"""Audit department-plugin rules for coverage, routing integrity, and portability."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = (
    "Department boundary",
    "Routing constraints",
    "Operating defaults",
    "Authorization gates",
    "Quality bar",
)
ROUTE_REF_RE = re.compile(r"`([a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)?)`")
SPECIFICITY_PATTERNS = (
    (
        "named repository or organization",
        re.compile(r"\b(?:CLOU" + r"S|Agent\s+Compan" + r"y)\b", re.IGNORECASE),
    ),
    ("absolute macOS user path", re.compile(r"/Users/[^/\s]+/")),
    ("absolute Linux user path", re.compile(r"/home/[^/\s]+/")),
    ("absolute Windows user path", re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\")),
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
)


@dataclass(frozen=True)
class DepartmentSummary:
    name: str
    skill_count: int
    covered_skill_count: int
    rule_file_count: int


def parse_profile_skills(path: Path) -> list[str]:
    skills: list[str] = []
    in_skills = False

    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw == "skills:":
            in_skills = True
            continue
        if in_skills and raw and not raw.startswith(" "):
            break
        if not in_skills:
            continue
        match = re.fullmatch(r"  - ([a-z0-9]+(?:-[a-z0-9]+)*)", raw)
        if match:
            skills.append(match.group(1))

    return skills


def routing_section(text: str) -> str:
    start_marker = "## Routing constraints"
    end_marker = "## Operating defaults"
    if start_marker not in text or end_marker not in text:
        return ""
    return text.split(start_marker, 1)[1].split(end_marker, 1)[0]


def duplicate_policy_lines(text: str) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not (line.startswith("- ") or line.startswith("| ")):
            continue
        if line in {"| Request shape | Route to |", "| --- | --- |"}:
            continue
        normalized = re.sub(r"\s+", " ", line).casefold()
        if normalized in seen:
            duplicates.add(line)
        seen.add(normalized)
    return sorted(duplicates)


def audit(root: Path) -> tuple[list[str], list[DepartmentSummary]]:
    failures: list[str] = []
    summaries: list[DepartmentSummary] = []
    departments = sorted(
        path.parent
        for path in root.glob("*/profile.yaml")
        if (path.parent / "rules").is_dir()
    )
    department_names = {department.name for department in departments}
    skills_by_department: dict[str, set[str]] = {}
    owners: dict[str, set[str]] = {}

    for department in departments:
        actual = {
            path.parent.name
            for path in (department / "skills").glob("*/SKILL.md")
        }
        skills_by_department[department.name] = actual
        for skill in actual:
            owners.setdefault(skill, set()).add(department.name)

    for department in departments:
        name = department.name
        rules_dir = department / "rules"
        readme_path = rules_dir / "README.md"
        defaults_path = rules_dir / "defaults.md"
        rule_files = sorted(rules_dir.glob("*.md"))

        for required in (readme_path, defaults_path):
            if not required.is_file():
                failures.append(f"{required.relative_to(root)}: missing required rule file")
        if not readme_path.is_file() or not defaults_path.is_file():
            continue

        readme = readme_path.read_text(encoding="utf-8")
        defaults = defaults_path.read_text(encoding="utf-8")
        if "](defaults.md)" not in readme:
            failures.append(
                f"{readme_path.relative_to(root)}: must link to [defaults.md](defaults.md)"
            )

        positions: list[int] = []
        for section in REQUIRED_SECTIONS:
            marker = f"## {section}"
            count = defaults.count(marker)
            if count != 1:
                failures.append(
                    f"{defaults_path.relative_to(root)}: expected one `{marker}` section, found {count}"
                )
            positions.append(defaults.find(marker))
        present_positions = [position for position in positions if position >= 0]
        if present_positions != sorted(present_positions):
            failures.append(
                f"{defaults_path.relative_to(root)}: required sections are out of order"
            )

        profile_skills = set(parse_profile_skills(department / "profile.yaml"))
        actual_skills = skills_by_department[name]
        if profile_skills != actual_skills:
            missing_from_profile = sorted(actual_skills - profile_skills)
            missing_from_disk = sorted(profile_skills - actual_skills)
            if missing_from_profile:
                failures.append(
                    f"{department.relative_to(root)}/profile.yaml: skills missing from profile: "
                    + ", ".join(missing_from_profile)
                )
            if missing_from_disk:
                failures.append(
                    f"{department.relative_to(root)}/profile.yaml: profiled skills missing on disk: "
                    + ", ".join(missing_from_disk)
                )

        route_text = routing_section(defaults)
        route_refs = set(ROUTE_REF_RE.findall(route_text))
        covered = {
            skill
            for skill in profile_skills
            if skill in route_refs or f"{name}/{skill}" in route_refs
        }
        uncovered = sorted(profile_skills - covered)
        if uncovered:
            failures.append(
                f"{defaults_path.relative_to(root)}: local skills missing from routing coverage: "
                + ", ".join(uncovered)
            )

        for ref in sorted(route_refs):
            if "/" in ref:
                owner, skill = ref.split("/", 1)
                if owner not in department_names:
                    failures.append(
                        f"{defaults_path.relative_to(root)}: route `{ref}` names an unknown plugin"
                    )
                elif skill not in skills_by_department[owner]:
                    failures.append(
                        f"{defaults_path.relative_to(root)}: route `{ref}` names a missing skill"
                    )
                continue

            ref_owners = owners.get(ref, set())
            if ref in department_names:
                continue
            if ref_owners and name not in ref_owners:
                qualified = ", ".join(f"{owner}/{ref}" for owner in sorted(ref_owners))
                failures.append(
                    f"{defaults_path.relative_to(root)}: cross-plugin route `{ref}` must be qualified as {qualified}"
                )
            elif not ref_owners:
                failures.append(
                    f"{defaults_path.relative_to(root)}: route `{ref}` does not resolve to a plugin or skill"
                )

        for duplicate in duplicate_policy_lines(defaults):
            failures.append(
                f"{defaults_path.relative_to(root)}: duplicate policy statement: {duplicate}"
            )

        summaries.append(
            DepartmentSummary(
                name=name,
                skill_count=len(profile_skills),
                covered_skill_count=len(covered),
                rule_file_count=len(rule_files),
            )
        )

    all_rule_markdown = sorted(
        path
        for path in root.rglob("*.md")
        if "rules" in path.relative_to(root).parts
    )
    for rule_file in all_rule_markdown:
        text = rule_file.read_text(encoding="utf-8")
        for label, pattern in SPECIFICITY_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                failures.append(
                    f"{rule_file.relative_to(root)}:{line}: {label} is not allowed in reusable plugin rules"
                )

    if not departments:
        failures.append("no department plugins with rules directories found")
    return failures, summaries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit plugin rules for complete, unambiguous, reusable routing."
    )
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    failures, summaries = audit(root)

    for summary in summaries:
        print(
            f"{summary.name}: {summary.covered_skill_count}/{summary.skill_count} skills covered "
            f"across {summary.rule_file_count} rule file(s)"
        )

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        print(f"Rule audit failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1

    print(
        f"Validated {len(summaries)} plugin rule set(s) with complete routing coverage."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
