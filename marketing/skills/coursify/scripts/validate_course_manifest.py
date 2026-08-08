#!/usr/bin/env python3
"""Validate the canonical Coursify JSON manifest with the standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PRODUCTION_STATUSES = {"planned", "in-production", "complete", "blocked", "deferred"}


def _string(value: Any, path: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty string")
        return None
    return value.strip()


def _string_list(
    value: Any,
    path: str,
    errors: list[str],
    *,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array of non-empty strings")
        return []
    if not value and not allow_empty:
        errors.append(f"{path} must be non-empty")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{path}[{index}] must be a non-empty string")
            continue
        normalized = item.strip()
        if normalized in result:
            errors.append(f"{path}[{index}] duplicates {normalized!r}")
            continue
        result.append(normalized)
    return result


def _identifier(
    value: Any,
    path: str,
    errors: list[str],
    seen: set[str],
) -> str | None:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        errors.append(f"{path} must be unique kebab-case")
        return None
    if value in seen:
        errors.append(f"{path} duplicates {value!r}")
        return None
    seen.add(value)
    return value


def _object_array(value: Any, path: str, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        errors.append(f"{path} must be a non-empty array")
        return []
    objects: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{path}[{index}] must be an object")
            continue
        objects.append(item)
    return objects


def _detect_cycle(dependencies: dict[str, list[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for dependency in dependencies.get(node, []):
            cycle = visit(dependency)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in dependencies:
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def validate_manifest(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest must be a JSON object"]

    for key in ("title", "audience", "entry_level", "desired_transformation", "format"):
        _string(data.get(key), key, errors)
    _string_list(data.get("prerequisites"), "prerequisites", errors, allow_empty=True)

    accessibility = data.get("accessibility")
    provisions: list[str] = []
    if not isinstance(accessibility, dict):
        errors.append("accessibility must be an object")
    else:
        _string_list(accessibility.get("needs"), "accessibility.needs", errors, allow_empty=True)
        provisions = _string_list(
            accessibility.get("provisions"),
            "accessibility.provisions",
            errors,
        )
        _string_list(accessibility.get("gaps"), "accessibility.gaps", errors, allow_empty=True)

    source_ids: set[str] = set()
    source_uses: list[tuple[str, list[str]]] = []
    for index, source in enumerate(_object_array(data.get("source_map"), "source_map", errors)):
        prefix = f"source_map[{index}]"
        source_id = _identifier(source.get("id"), f"{prefix}.id", errors, source_ids)
        for key in ("location", "authority_or_date", "notes_or_license"):
            _string(source.get(key), f"{prefix}.{key}", errors)
        used_by = _string_list(source.get("used_by"), f"{prefix}.used_by", errors)
        if source_id:
            source_uses.append((prefix, used_by))

    outcome_ids: set[str] = set()
    for index, outcome in enumerate(_object_array(data.get("outcomes"), "outcomes", errors)):
        prefix = f"outcomes[{index}]"
        _identifier(outcome.get("id"), f"{prefix}.id", errors, outcome_ids)
        _string(outcome.get("statement"), f"{prefix}.statement", errors)
        _string(outcome.get("evidence_of_mastery"), f"{prefix}.evidence_of_mastery", errors)

    modules = _object_array(data.get("modules"), "modules", errors)
    module_ids: set[str] = set()
    module_records: list[tuple[str, dict[str, Any], str | None]] = []
    for index, module in enumerate(modules):
        prefix = f"modules[{index}]"
        module_id = _identifier(module.get("id"), f"{prefix}.id", errors, module_ids)
        _string(module.get("title"), f"{prefix}.title", errors)
        module_records.append((prefix, module, module_id))

    lesson_ids: set[str] = set()
    taught_outcomes: set[str] = set()
    assessed_outcomes: set[str] = set()
    module_dependencies: dict[str, list[str]] = {}
    all_formats: set[str] = set()

    for prefix, module, module_id in module_records:
        prerequisites = _string_list(
            module.get("prerequisites"),
            f"{prefix}.prerequisites",
            errors,
            allow_empty=True,
        )
        if module_id:
            module_dependencies[module_id] = prerequisites
        for prerequisite in prerequisites:
            if prerequisite == module_id:
                errors.append(f"{prefix}.prerequisites cannot reference itself")
            elif prerequisite not in module_ids:
                errors.append(f"{prefix}.prerequisites references unknown {prerequisite!r}")

        aligned = _string_list(module.get("aligned_outcomes"), f"{prefix}.aligned_outcomes", errors)
        valid_aligned: set[str] = set()
        for outcome_id in aligned:
            if outcome_id not in outcome_ids:
                errors.append(f"{prefix}.aligned_outcomes references unknown {outcome_id!r}")
            else:
                valid_aligned.add(outcome_id)
                taught_outcomes.add(outcome_id)

        lessons = _object_array(module.get("lessons"), f"{prefix}.lessons", errors)
        for lesson_index, lesson in enumerate(lessons):
            lesson_prefix = f"{prefix}.lessons[{lesson_index}]"
            _identifier(lesson.get("id"), f"{lesson_prefix}.id", errors, lesson_ids)
            for key in ("title", "objective"):
                _string(lesson.get(key), f"{lesson_prefix}.{key}", errors)
            duration = lesson.get("duration_minutes")
            if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
                errors.append(f"{lesson_prefix}.duration_minutes must be a positive integer")
            formats = _string_list(lesson.get("formats"), f"{lesson_prefix}.formats", errors)
            all_formats.update(item.casefold() for item in formats)
            for source_ref in _string_list(
                lesson.get("source_refs"),
                f"{lesson_prefix}.source_refs",
                errors,
            ):
                if source_ref not in source_ids:
                    errors.append(f"{lesson_prefix}.source_refs references unknown {source_ref!r}")

            exercise = lesson.get("exercise")
            if not isinstance(exercise, dict):
                errors.append(f"{lesson_prefix}.exercise must be an object")
            else:
                _string(exercise.get("type"), f"{lesson_prefix}.exercise.type", errors)
                _string(exercise.get("instructions"), f"{lesson_prefix}.exercise.instructions", errors)

            assessment = lesson.get("assessment")
            if not isinstance(assessment, dict):
                errors.append(f"{lesson_prefix}.assessment must be an object")
                continue
            _string(assessment.get("type"), f"{lesson_prefix}.assessment.type", errors)
            _string(assessment.get("evidence"), f"{lesson_prefix}.assessment.evidence", errors)
            assessment_alignment = _string_list(
                assessment.get("aligned_outcomes"),
                f"{lesson_prefix}.assessment.aligned_outcomes",
                errors,
            )
            for outcome_id in assessment_alignment:
                if outcome_id not in outcome_ids:
                    errors.append(
                        f"{lesson_prefix}.assessment.aligned_outcomes references unknown {outcome_id!r}"
                    )
                elif outcome_id not in valid_aligned:
                    errors.append(
                        f"{lesson_prefix}.assessment.aligned_outcomes references {outcome_id!r} outside its module"
                    )
                else:
                    assessed_outcomes.add(outcome_id)

    cycle = _detect_cycle(module_dependencies)
    if cycle:
        errors.append(f"module prerequisites contain a cycle: {' -> '.join(cycle)}")

    capstone = data.get("capstone")
    if not isinstance(capstone, dict):
        errors.append("capstone must be an object")
    elif not isinstance(capstone.get("required"), bool):
        errors.append("capstone.required must be a boolean")
    elif capstone["required"]:
        for key in (
            "authentic_task",
            "rubric_or_acceptance_criteria",
            "answer_key_location",
            "remediation_path",
        ):
            _string(capstone.get(key), f"capstone.{key}", errors)
        for outcome_id in _string_list(
            capstone.get("aligned_outcomes"),
            "capstone.aligned_outcomes",
            errors,
        ):
            if outcome_id not in outcome_ids:
                errors.append(f"capstone.aligned_outcomes references unknown {outcome_id!r}")
            else:
                assessed_outcomes.add(outcome_id)
    else:
        _string(capstone.get("rationale"), "capstone.rationale", errors)

    production_units: set[str] = set()
    artifact_ids: set[str] = set()
    valid_units = lesson_ids | module_ids | {"course", "capstone"}
    for index, artifact in enumerate(
        _object_array(data.get("production_plan"), "production_plan", errors)
    ):
        prefix = f"production_plan[{index}]"
        _identifier(artifact.get("artifact_id"), f"{prefix}.artifact_id", errors, artifact_ids)
        _string(artifact.get("artifact"), f"{prefix}.artifact", errors)
        unit_id = _string(artifact.get("canonical_unit_id"), f"{prefix}.canonical_unit_id", errors)
        if unit_id:
            if unit_id not in valid_units:
                errors.append(f"{prefix}.canonical_unit_id references unknown {unit_id!r}")
            else:
                production_units.add(unit_id)
        _string(artifact.get("owning_skill"), f"{prefix}.owning_skill", errors)
        status = artifact.get("status")
        if status not in PRODUCTION_STATUSES:
            errors.append(
                f"{prefix}.status must be one of {', '.join(sorted(PRODUCTION_STATUSES))}"
            )
        _string(artifact.get("verification"), f"{prefix}.verification", errors)

    for lesson_id in sorted(lesson_ids - production_units):
        errors.append(f"lesson {lesson_id!r} has no production-plan artifact")
    for missing in sorted(outcome_ids - taught_outcomes):
        errors.append(f"outcome {missing!r} is not aligned to any module")
    for missing in sorted(outcome_ids - assessed_outcomes):
        errors.append(f"outcome {missing!r} is not assessed")

    valid_source_targets = valid_units | outcome_ids
    for prefix, used_by in source_uses:
        for target in used_by:
            if target not in valid_source_targets:
                errors.append(f"{prefix}.used_by references unknown {target!r}")

    accessibility_text = " ".join(provisions).casefold()

    def uses_format(*tokens: str) -> bool:
        return any(token in format_name for format_name in all_formats for token in tokens)

    if uses_format("video", "audio") and not any(
        token in accessibility_text for token in ("caption", "transcript")
    ):
        errors.append("video or audio lessons require captions or transcripts in accessibility.provisions")
    if uses_format("interactive", "html") and "keyboard" not in accessibility_text:
        errors.append("interactive lessons require keyboard access in accessibility.provisions")
    if uses_format("image", "diagram", "slide", "visual") and not any(
        token in accessibility_text for token in ("text alternative", "alt text", "description")
    ):
        errors.append("visual lessons require text alternatives in accessibility.provisions")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Coursify JSON course manifest.")
    parser.add_argument("manifest", type=Path, help="Path to the course manifest JSON file")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable result")
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors = [f"manifest not found: {args.manifest}"]
    except (OSError, UnicodeError) as exc:
        errors = [f"could not read manifest: {exc}"]
    except json.JSONDecodeError as exc:
        errors = [f"invalid JSON at line {exc.lineno} column {exc.colno}: {exc.msg}"]
    else:
        errors = validate_manifest(data)

    result = {"valid": not errors, "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        print(f"Valid course manifest: {args.manifest}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
