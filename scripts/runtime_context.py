#!/usr/bin/env python3
"""Resolve project personalization and invocation-scoped component variables."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
COMPONENT_ID_RE = re.compile(
    r"^(?:plugin|skill|command|rule|agent|external-skill):[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)?$"
)
NAMED_PLACEHOLDER_RE = re.compile(
    r"\{\{\s*([a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)+)\s*\}\}"
)


class RuntimeContextError(Exception):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeContextError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeContextError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeContextError(f"expected a JSON object in {path}")
    return data


def contract_path(project: Path, explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    installed = project / ".agents" / "runtime-contract.json"
    if installed.exists():
        return installed
    return ROOT / "references" / "runtime-contract.json"


def get_nested(data: dict[str, Any], dotted_key: str) -> Any:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def set_nested(data: dict[str, Any], dotted_key: str, value: Any) -> None:
    parts = [part for part in dotted_key.split(".") if part]
    if not parts:
        raise RuntimeContextError("variable name must not be empty")
    current = data
    for part in parts[:-1]:
        child = current.setdefault(part, {})
        if not isinstance(child, dict):
            raise RuntimeContextError(f"cannot set {dotted_key}: {part} is already a scalar")
        current = child
    current[parts[-1]] = value


def parse_assignment(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise RuntimeContextError(f"expected name=value, got: {raw}")
    name, value = raw.split("=", 1)
    name = name.strip()
    if not name:
        raise RuntimeContextError(f"expected a variable name in: {raw}")
    return name, value.strip()


def coerce_value(raw: Any, definition: dict[str, Any]) -> Any:
    variable_type = definition.get("type", "string")
    if variable_type == "string":
        return str(raw)
    if variable_type == "boolean":
        if isinstance(raw, bool):
            return raw
        lowered = str(raw).strip().lower()
        if lowered in {"true", "yes", "1", "on"}:
            return True
        if lowered in {"false", "no", "0", "off"}:
            return False
        raise RuntimeContextError(f"expected a boolean, got: {raw}")
    if variable_type == "number":
        try:
            return float(raw) if "." in str(raw) else int(raw)
        except ValueError as exc:
            raise RuntimeContextError(f"expected a number, got: {raw}") from exc
    if variable_type == "string-list":
        if isinstance(raw, list):
            return [str(item) for item in raw]
        return [item.strip() for item in str(raw).split(",") if item.strip()]
    raise RuntimeContextError(f"unsupported variable type: {variable_type}")


def component_variables(contract: dict[str, Any], component: str) -> list[str]:
    personalization = contract.get("personalization", {})
    defaults = personalization.get("default_variables", []) if isinstance(personalization, dict) else []
    applies_to = personalization.get("applies_to", []) if isinstance(personalization, dict) else []
    enabled_by_default = bool(
        personalization.get("enabled_by_default", False)
        if isinstance(personalization, dict)
        else False
    )
    components = contract.get("components", {})
    component_data = components.get(component, {}) if isinstance(components, dict) else {}
    component_policy = (
        component_data.get("personalization", "inherit")
        if isinstance(component_data, dict)
        else "inherit"
    )
    component_kind = component.split(":", 1)[0]
    enabled = component_policy == "enabled" or (
        component_policy == "inherit"
        and enabled_by_default
        and component_kind in applies_to
    )
    if component_policy == "disabled" or not enabled:
        return []
    declared = component_data.get("variables", []) if isinstance(component_data, dict) else []
    return list(dict.fromkeys([str(item) for item in [*defaults, *declared]]))


def prompt_missing_values(
    names: list[str],
    definitions: dict[str, Any],
    *,
    input_fn: Callable[[str], str] = input,
) -> dict[str, Any]:
    """Collect required invocation values without persisting them."""

    values: dict[str, Any] = {}
    for name in names:
        definition = definitions.get(name)
        if not isinstance(definition, dict):
            raise RuntimeContextError(f"invalid variable definition: {name}")
        answer = input_fn(f"{definition.get('prompt', name)}: ").strip()
        if not answer:
            raise RuntimeContextError(f"required invocation variable was not provided: {name}")
        values[name] = coerce_value(answer, definition)
    return values


def render_placeholders(
    template: str,
    values: dict[str, Any],
    *,
    arguments: str | None = None,
) -> str:
    """Render canonical named variables and the optional raw invocation string."""

    missing: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in values:
            missing.add(name)
            return match.group(0)
        value = values[name]
        return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)

    rendered = NAMED_PLACEHOLDER_RE.sub(replace, template)
    if missing:
        raise RuntimeContextError(
            "unresolved runtime placeholder(s): " + ", ".join(sorted(missing))
        )
    if "$ARGUMENTS" in rendered:
        if arguments is None:
            raise RuntimeContextError("template uses $ARGUMENTS but no raw arguments were supplied")
        rendered = rendered.replace("$ARGUMENTS", arguments)
    return rendered


def local_store_path(project: Path, contract: dict[str, Any]) -> Path:
    personalization = contract.get("personalization", {})
    relative = ".agents/personalization.local.json"
    if isinstance(personalization, dict):
        relative = str(personalization.get("project_store", relative))
    relative_path = Path(relative)
    if (
        relative_path.is_absolute()
        or not relative_path.parts
        or relative_path.parts[0] != ".agents"
        or any(part in {"", ".", ".."} for part in relative_path.parts)
    ):
        raise RuntimeContextError(
            "runtime personalization.project_store must remain under .agents/"
        )
    project_root = project.expanduser().resolve()
    candidate = project_root / relative_path
    resolved = candidate.resolve(strict=False)
    if not resolved.is_relative_to(project_root):
        raise RuntimeContextError(
            "runtime personalization.project_store escapes the project through a symlink"
        )
    return candidate


def load_local_values(project: Path, contract: dict[str, Any]) -> dict[str, Any]:
    path = local_store_path(project, contract)
    return read_json(path) if path.exists() else {}


def atomic_write_json(path: Path, data: dict[str, Any], private: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temp = Path(raw_temp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        if private:
            temp.chmod(0o600)
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def assignment_values(
    assignments: list[str], definitions: dict[str, Any], *, reject_unknown: bool = True
) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for raw in assignments:
        name, value = parse_assignment(raw)
        definition = definitions.get(name)
        if not isinstance(definition, dict):
            if reject_unknown:
                raise RuntimeContextError(f"unknown runtime variable: {name}")
            definition = {"type": "string"}
        values[name] = coerce_value(value, definition)
    return values


def resolve_context(
    *,
    project: Path,
    component: str,
    invocation: dict[str, Any] | None = None,
    session: dict[str, Any] | None = None,
    contract_file: Path | None = None,
    allow_missing: bool = False,
) -> dict[str, Any]:
    if not COMPONENT_ID_RE.fullmatch(component):
        raise RuntimeContextError(f"invalid component identity: {component}")
    contract = read_json(contract_file or contract_path(project))
    variables = contract.get("variables", {})
    definitions = variables.get("definitions", {}) if isinstance(variables, dict) else {}
    if not isinstance(definitions, dict):
        raise RuntimeContextError("runtime contract variables.definitions must be an object")
    resolution_order = (
        variables.get("resolution_order", []) if isinstance(variables, dict) else []
    )
    if (
        not isinstance(resolution_order, list)
        or not resolution_order
        or any(
            source not in {"invocation", "session", "project", "default"}
            for source in resolution_order
        )
    ):
        raise RuntimeContextError("runtime contract variables.resolution_order is invalid")
    project_values = load_local_values(project, contract)
    invocation = invocation or {}
    session = session or {}

    resolved: dict[str, Any] = {}
    sources: dict[str, str] = {}
    missing: list[str] = []
    for name in component_variables(contract, component):
        definition = definitions.get(name)
        if not isinstance(definition, dict):
            raise RuntimeContextError(f"invalid variable definition: {name}")
        candidates = {
            "invocation": invocation.get(name),
            "session": session.get(name),
            "project": get_nested(project_values, name),
            "default": definition.get("default"),
        }
        for source in resolution_order:
            if source == "project" and (
                definition.get("scope") != "project" or definition.get("sensitive")
            ):
                continue
            value = candidates[source]
            if value is not None and value != "":
                resolved[name] = coerce_value(value, definition)
                sources[name] = source
                break
        else:
            if definition.get("required"):
                missing.append(name)

    if missing and not allow_missing:
        formatted = ", ".join(missing)
        raise RuntimeContextError(f"missing required invocation variable(s) for {component}: {formatted}")
    return {
        "schema_version": 1,
        "component": component,
        "values": resolved,
        "sources": sources,
        "missing_required": missing,
    }


def configure_project(
    *, project: Path, assignments: list[str], contract_file: Path | None = None
) -> Path:
    contract = read_json(contract_file or contract_path(project))
    variables = contract.get("variables", {})
    definitions = variables.get("definitions", {}) if isinstance(variables, dict) else {}
    if not isinstance(definitions, dict):
        raise RuntimeContextError("runtime contract variables.definitions must be an object")
    values = load_local_values(project, contract)
    for name, value in assignment_values(assignments, definitions).items():
        definition = definitions[name]
        if definition.get("sensitive"):
            raise RuntimeContextError(f"refusing to persist sensitive runtime variable: {name}")
        if definition.get("scope") != "project":
            raise RuntimeContextError(f"{name} is {definition.get('scope')}-scoped and must be supplied per run")
        set_nested(values, name, value)
    out = local_store_path(project, contract)
    atomic_write_json(out, values, private=True)
    return out


def interactive_configure(
    *, project: Path, contract_file: Path | None = None, input_fn: Callable[[str], str] = input
) -> Path:
    contract = read_json(contract_file or contract_path(project))
    variables = contract.get("variables", {})
    definitions = variables.get("definitions", {}) if isinstance(variables, dict) else {}
    assignments: list[str] = []
    for name, definition in definitions.items():
        if not isinstance(definition, dict) or definition.get("scope") != "project" or definition.get("sensitive"):
            continue
        current = get_nested(load_local_values(project, contract), name)
        suffix = f" [{current}]" if current not in (None, "") else ""
        answer = input_fn(f"{definition.get('prompt', name)}{suffix}: ").strip()
        if answer:
            assignments.append(f"{name}={answer}")
    if not assignments and local_store_path(project, contract).exists():
        return local_store_path(project, contract)
    return configure_project(project=project, assignments=assignments, contract_file=contract_file)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Configure and resolve installed component runtime variables.")
    sub = parser.add_subparsers(dest="command", required=True)

    configure = sub.add_parser("configure", help="Persist non-sensitive project-scoped personalization.")
    configure.add_argument("--project", default=".")
    configure.add_argument("--contract")
    configure.add_argument("--set", action="append", default=[])

    resolve = sub.add_parser("resolve", help="Resolve one component's effective runtime context.")
    resolve.add_argument("component")
    resolve.add_argument("--project", default=".")
    resolve.add_argument("--contract")
    resolve.add_argument("--set", action="append", default=[], help="Invocation value as name=value.")
    resolve.add_argument("--session", action="append", default=[], help="Session value as name=value.")
    resolve.add_argument("--allow-missing", action="store_true")
    resolve.add_argument("--render", help="Render this UTF-8 template with the resolved values")
    resolve.add_argument("--output", help="Write rendered text here instead of stdout")
    resolve.add_argument("--arguments", help="Raw value for a template's $ARGUMENTS token")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project = Path(args.project).expanduser().resolve()
    explicit_contract = Path(args.contract).expanduser().resolve() if args.contract else None
    try:
        contract = read_json(explicit_contract or contract_path(project))
        variables = contract.get("variables", {})
        definitions = variables.get("definitions", {}) if isinstance(variables, dict) else {}
        if args.command == "configure":
            if args.set:
                out = configure_project(project=project, assignments=args.set, contract_file=explicit_contract)
            elif sys.stdin.isatty():
                out = interactive_configure(project=project, contract_file=explicit_contract)
            else:
                raise RuntimeContextError("configure without --set requires an interactive terminal")
            print(out)
            return 0

        if args.output and not args.render:
            raise RuntimeContextError("--output requires --render")

        invocation = assignment_values(args.set, definitions)
        session = assignment_values(args.session, definitions)
        result = resolve_context(
            project=project,
            component=args.component,
            invocation=invocation,
            session=session,
            contract_file=explicit_contract,
            allow_missing=True,
        )
        if result["missing_required"] and not args.allow_missing:
            if not sys.stdin.isatty():
                missing = ", ".join(result["missing_required"])
                raise RuntimeContextError(
                    f"missing required invocation variable(s) for {args.component}: {missing}"
                )
            invocation.update(
                prompt_missing_values(result["missing_required"], definitions)
            )
            result = resolve_context(
                project=project,
                component=args.component,
                invocation=invocation,
                session=session,
                contract_file=explicit_contract,
            )
        if args.render:
            template_path = Path(args.render).expanduser().resolve()
            rendered = render_placeholders(
                template_path.read_text(encoding="utf-8"),
                result["values"],
                arguments=args.arguments,
            )
            if args.output:
                output = Path(args.output).expanduser().resolve()
                output.parent.mkdir(parents=True, exist_ok=True)
                fd, raw_temp = tempfile.mkstemp(prefix=f".{output.name}.", dir=str(output.parent))
                temp = Path(raw_temp)
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as handle:
                        handle.write(rendered)
                    os.replace(temp, output)
                finally:
                    if temp.exists():
                        temp.unlink()
                print(output)
            else:
                print(rendered, end="" if rendered.endswith("\n") else "\n")
        else:
            print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    except (OSError, RuntimeContextError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
