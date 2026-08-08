#!/usr/bin/env python3
"""Generate deterministic, machine-readable discovery artifacts for this repo.

The generator treats department ``profile.yaml`` files as the ordered component
inventory and reads public names/descriptions from skill, command, and agent
frontmatter. It intentionally describes source assets only: it does not
advertise a hosted API, agent endpoint, authentication service, or live MCP
server.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Sequence
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]


def detect_repository_slug(root: Path) -> str:
    """Resolve the canonical repository without embedding a maintainer identity."""

    configured = os.environ.get("PLUGIN_BUNDLE_REPOSITORY", "").strip()
    if configured:
        return configured.removesuffix(".git").strip("/")
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(root),
            check=True,
            text=True,
            capture_output=True,
        )
        remote = result.stdout.strip().removesuffix(".git")
        if remote.startswith("git@") and ":" in remote:
            remote = remote.split(":", 1)[1]
        elif "://" in remote:
            remote = remote.split("://", 1)[1].partition("/")[2]
        parts = [part for part in remote.strip("/").split("/") if part]
        if len(parts) >= 2:
            return "/".join(parts[-2:])
    except (OSError, subprocess.CalledProcessError):
        pass

    metadata_path = root / "codemeta.json"
    if metadata_path.is_file():
        try:
            repository_url = str(json.loads(metadata_path.read_text(encoding="utf-8"))["codeRepository"])
            parts = [part for part in repository_url.removesuffix(".git").strip("/").split("/") if part]
            if len(parts) >= 2:
                return "/".join(parts[-2:])
        except (KeyError, OSError, json.JSONDecodeError):
            pass
    return "local/plugin-bundle"


REPOSITORY = detect_repository_slug(ROOT)
REPOSITORY_URL = f"https://github.com/{REPOSITORY}"
RAW_URL = f"https://raw.githubusercontent.com/{REPOSITORY}/main"
DEFAULT_BRANCH = "main"
OUTPUT_FILES = ("catalog.json", "llms.txt", "llms-full.txt", "context7.json")
PROFILE_LIST_FIELDS = ("platforms", "skills", "commands", "agents", "team")
FRONTMATTER_BOUNDARY = "---"
TOP_LEVEL_FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:[ \t]*(.*))?$")


class DiscoveryError(ValueError):
    """Raised when source metadata cannot produce a truthful catalog."""


def normalize_text(value: str) -> str:
    """Collapse YAML/Markdown prose to one deterministic display line."""

    return re.sub(r"\s+", " ", value).strip()


def count_label(value: int, singular: str, plural: str | None = None) -> str:
    return f"{value} {singular if value == 1 else plural or singular + 's'}"


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
        return str(parsed)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_top_level_yaml(text: str, source: Path) -> dict[str, str | list[str]]:
    """Parse the small top-level YAML subset used by profiles/frontmatter.

    This deliberately avoids a third-party YAML dependency. It supports plain
    and quoted scalars, folded/literal blocks, and indented scalar lists. Nested
    mappings are outside the discovery metadata contract and are ignored.
    """

    lines = text.splitlines()
    result: dict[str, str | list[str]] = {}
    index = 0
    while index < len(lines):
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#") or raw[:1].isspace():
            index += 1
            continue

        match = TOP_LEVEL_FIELD_RE.match(raw)
        if not match:
            raise DiscoveryError(f"{source}: unsupported top-level YAML line: {raw}")
        key, raw_value = match.groups()
        value = (raw_value or "").strip()

        if value in {">", ">-", ">+", "|", "|-", "|+"}:
            index += 1
            block: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                if candidate and not candidate[:1].isspace():
                    break
                block.append(candidate.strip())
                index += 1
            result[key] = normalize_text(" ".join(block))
            continue

        if not value:
            index += 1
            items: list[str] = []
            has_nested_mapping = False
            while index < len(lines):
                candidate = lines[index]
                if candidate and not candidate[:1].isspace():
                    break
                stripped = candidate.strip()
                if stripped.startswith("- "):
                    items.append(parse_scalar(stripped[2:]))
                elif stripped and not stripped.startswith("#"):
                    has_nested_mapping = True
                index += 1
            result[key] = "" if has_nested_mapping else items
            continue

        result[key] = parse_scalar(value)
        index += 1

    return result


def read_frontmatter(path: Path) -> dict[str, str | list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        raise DiscoveryError(f"{path}: missing opening frontmatter boundary")
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == FRONTMATTER_BOUNDARY
        )
    except StopIteration as exc:
        raise DiscoveryError(f"{path}: missing closing frontmatter boundary") from exc
    return parse_top_level_yaml("\n".join(lines[1:end]), path)


def required_string(data: dict[str, str | list[str]], key: str, source: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not normalize_text(value):
        raise DiscoveryError(f"{source}: `{key}` must be a non-empty scalar")
    return normalize_text(value)


def list_field(data: dict[str, str | list[str]], key: str, source: Path) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise DiscoveryError(f"{source}: `{key}` must be a list")
    return [normalize_text(item) for item in value if normalize_text(item)]


def github_url(path: str, *, directory: bool = False) -> str:
    action = "tree" if directory else "blob"
    encoded = quote(path, safe="/")
    return f"{REPOSITORY_URL}/{action}/{DEFAULT_BRANCH}/{encoded}"


def raw_url(path: str) -> str:
    return f"{RAW_URL}/{quote(path, safe='/')}"


def relative_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def component_record(
    path: Path,
    root: Path,
    department: str,
    kind: str,
    install_name: str,
) -> dict[str, str]:
    metadata = read_frontmatter(path)
    public_name = required_string(metadata, "name", path)
    description = required_string(metadata, "description", path)
    source_path = relative_path(path, root)
    return {
        "id": f"{department}/{kind}/{install_name}",
        "name": public_name,
        "install_name": install_name,
        "qualified_name": f"{department}/{install_name}",
        "description": description,
        "path": source_path,
        "url": github_url(source_path),
        "raw_url": raw_url(source_path),
    }


def first_markdown_paragraph(path: Path) -> str:
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            if current:
                paragraphs.append(current)
                current = []
            continue
        if line.startswith(("#", "```", "- ", "* ", "|")):
            if current:
                paragraphs.append(current)
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append(current)
    if not paragraphs:
        raise DiscoveryError(f"{path}: no descriptive paragraph found")
    return normalize_text(" ".join(paragraphs[0]))


def rule_record(path: Path, root: Path, department: str) -> dict[str, str]:
    install_name = path.stem
    source_path = relative_path(path, root)
    return {
        "id": f"{department}/rule/{install_name}",
        "name": install_name,
        "install_name": install_name,
        "qualified_name": f"{department}/{install_name}",
        "description": first_markdown_paragraph(path),
        "path": source_path,
        "url": github_url(source_path),
        "raw_url": raw_url(source_path),
    }


def validate_inventory(
    profile_path: Path,
    kind: str,
    declared: list[str],
    discovered: list[str],
) -> None:
    if declared == discovered:
        return
    missing = [name for name in discovered if name not in declared]
    absent = [name for name in declared if name not in discovered]
    details: list[str] = []
    if missing:
        details.append(f"missing from profile: {', '.join(missing)}")
    if absent:
        details.append(f"missing on disk: {', '.join(absent)}")
    if not missing and not absent:
        details.append("profile order differs from disk order")
    raise DiscoveryError(f"{profile_path}: {kind} inventory drift ({'; '.join(details)})")


def discover_component_paths(department_path: Path, kind: str) -> dict[str, Path]:
    if kind == "skills":
        paths = sorted((department_path / "skills").glob("*/SKILL.md"))
        return {path.parent.name: path for path in paths}
    paths = sorted((department_path / kind).glob("*.md"))
    return {path.stem: path for path in paths if path.name != "README.md"}


def manifest_records(department_path: Path, root: Path) -> dict[str, dict[str, str]]:
    manifests = {
        "claude": department_path / ".claude-plugin" / "plugin.json",
        "codex": department_path / ".codex-plugin" / "plugin.json",
        "cursor": department_path / ".cursor-plugin" / "plugin.json",
    }
    records: dict[str, dict[str, str]] = {}
    for platform, path in manifests.items():
        if not path.is_file():
            continue
        source_path = relative_path(path, root)
        records[platform] = {
            "path": source_path,
            "url": github_url(source_path),
            "raw_url": raw_url(source_path),
        }
    return records


def build_plugin(profile_path: Path, root: Path) -> dict[str, object]:
    department_path = profile_path.parent
    profile = parse_top_level_yaml(profile_path.read_text(encoding="utf-8"), profile_path)
    slug = required_string(profile, "slug", profile_path)
    if slug != department_path.name:
        raise DiscoveryError(
            f"{profile_path}: slug `{slug}` does not match directory `{department_path.name}`"
        )

    version = required_string(profile, "version", profile_path)
    mission = required_string(profile, "mission", profile_path)
    declared = {field: list_field(profile, field, profile_path) for field in PROFILE_LIST_FIELDS}

    records: dict[str, list[dict[str, str]]] = {}
    for kind, singular in (("skills", "skill"), ("commands", "command"), ("agents", "agent")):
        paths = discover_component_paths(department_path, kind)
        discovered = sorted(paths)
        if set(declared[kind]) != set(discovered):
            validate_inventory(profile_path, kind, declared[kind], discovered)
        records[kind] = [
            component_record(paths[name], root, slug, singular, name)
            for name in declared[kind]
        ]

    rule_paths = discover_component_paths(department_path, "rules")
    records["rules"] = [rule_record(rule_paths[name], root, slug) for name in sorted(rule_paths)]

    source_path = relative_path(department_path, root)
    return {
        "id": slug,
        "name": slug,
        "version": version,
        "mission": mission,
        "platforms": declared["platforms"],
        "team": declared["team"],
        "path": source_path,
        "url": github_url(source_path, directory=True),
        "profile": {
            "path": relative_path(profile_path, root),
            "url": github_url(relative_path(profile_path, root)),
            "raw_url": raw_url(relative_path(profile_path, root)),
        },
        "manifests": manifest_records(department_path, root),
        "counts": {kind: len(records[kind]) for kind in ("skills", "commands", "agents", "rules")},
        **records,
    }


def build_catalog(root: Path) -> dict[str, object]:
    root = root.resolve()
    profile_paths = sorted(root.glob("*/profile.yaml"), key=lambda path: path.parent.name)
    if not profile_paths:
        raise DiscoveryError(f"{root}: no department profile.yaml files found")
    plugins = [build_plugin(path, root) for path in profile_paths]
    counts = {
        "plugins": len(plugins),
        "skills": sum(plugin["counts"]["skills"] for plugin in plugins),  # type: ignore[index]
        "commands": sum(plugin["counts"]["commands"] for plugin in plugins),  # type: ignore[index]
        "agents": sum(plugin["counts"]["agents"] for plugin in plugins),  # type: ignore[index]
        "rules": sum(plugin["counts"]["rules"] for plugin in plugins),  # type: ignore[index]
    }
    return {
        "schema_version": 1,
        "name": "Agent Company Plugins",
        "description": (
            "Source catalog for portable department plugins, skills, commands, agents, "
            "and runtime-neutral rules for Claude, Codex, and Cursor."
        ),
        "scope": (
            "Version-controlled source assets only. This catalog does not advertise a "
            "hosted API, callable agent endpoint, authentication service, or live MCP server."
        ),
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "default_branch": DEFAULT_BRANCH,
        "generated_by": "scripts/generate_discovery_catalog.py",
        "generated_from": [
            "*/profile.yaml",
            "*/skills/*/SKILL.md frontmatter",
            "*/commands/*.md frontmatter",
            "*/agents/*.md frontmatter",
            "*/rules/*.md",
        ],
        "counts": counts,
        "canonical_documents": {
            "readme": github_url("README.md"),
            "agent_guidance": github_url("AGENTS.md"),
            "quick_start": github_url("QUICK_START.md"),
            "installation": github_url("references/docs/INSTALLATION.md"),
            "requirement_coverage": github_url("references/docs/REQUIREMENT-COVERAGE.md"),
            "architecture": github_url("references/docs/ARCHITECTURE.md"),
            "component_graph": raw_url("component-graph.json"),
            "component_graph_contract": raw_url("references/component-graph.json"),
            "runtime_contract": raw_url("references/runtime-contract.json"),
            "changelog": github_url("CHANGELOG.md"),
            "license": github_url("LICENSE"),
            "llms": raw_url("llms.txt"),
            "llms_full": raw_url("llms-full.txt"),
            "catalog": raw_url("catalog.json"),
            "codemeta": raw_url("codemeta.json"),
            "citation": github_url("CITATION.cff"),
        },
        "plugins": plugins,
    }


def render_catalog_json(catalog: dict[str, object]) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def render_llms_txt(catalog: dict[str, object]) -> str:
    counts = catalog["counts"]
    plugins = catalog["plugins"]
    lines = [
        "# Agent Company Plugins",
        "",
        "> Portable department plugins, skills, commands, agents, and runtime-neutral rules for Claude, Codex, and Cursor.",
        "",
        (
            f"This source repository currently catalogs {counts['plugins']} plugins, "  # type: ignore[index]
            f"{counts['skills']} skills, {counts['commands']} commands, "  # type: ignore[index]
            f"{counts['agents']} agents, and {counts['rules']} rule sets."  # type: ignore[index]
        ),
        "",
        "## Canonical Sources",
        "",
        f"- [Repository]({REPOSITORY_URL}): canonical source and release history",
        f"- [README]({github_url('README.md')}): overview and installation guidance",
        f"- [Agent guidance]({github_url('AGENTS.md')}): repository and runtime invariants for coding agents",
        f"- [Quick Start]({github_url('QUICK_START.md')}): supported installation workflows",
        f"- [Installation contract]({github_url('references/docs/INSTALLATION.md')}): preferred interactive command, flat layout, and no-loss updates",
        f"- [Requirement coverage]({github_url('references/docs/REQUIREMENT-COVERAGE.md')}): implementation and verification map",
        f"- [Machine-readable catalog]({raw_url('catalog.json')}): complete structured inventory",
        f"- [Full LLM catalog]({raw_url('llms-full.txt')}): descriptions and source links for every component",
        f"- [Typed component graph]({raw_url('component-graph.json')}): complete recursive internal, external, plugin, and cross-element relationship inventory",
        f"- [Component graph contract]({raw_url('references/component-graph.json')}): explicit references, source inventories, and resolution policy",
        f"- [Runtime context contract]({raw_url('references/runtime-contract.json')}): inherited personalization and dynamic variables",
        f"- [CodeMeta]({raw_url('codemeta.json')}): structured software-project metadata",
        f"- [Citation metadata]({github_url('CITATION.cff')}): software citation information",
        f"- [Architecture]({github_url('references/docs/ARCHITECTURE.md')}): source and plugin model",
        f"- [Changelog]({github_url('CHANGELOG.md')}): current changes and deprecations",
        "",
        "## Plugins",
        "",
    ]
    for plugin in plugins:  # type: ignore[assignment]
        lines.append(
            f"- [`{plugin['name']}`]({plugin['url']}): {plugin['mission']} "
            f"({count_label(plugin['counts']['skills'], 'skill')}, "
            f"{count_label(plugin['counts']['commands'], 'command')}, "
            f"{count_label(plugin['counts']['agents'], 'agent')})"
        )
    lines += [
        "",
        "## Instructions for Large Language Models",
        "",
        "- Treat this repository and the linked source files as authoritative for current component names, descriptions, and ownership.",
        "- Use `catalog.json` or `llms-full.txt` to select the narrowest matching plugin, skill, command, or agent.",
        "- Follow the installation contract and prefer the first-party project installer; do not infer install paths from the source layout alone.",
        "- For unresolved installed-update conflicts, use the explicit first-party `reconcile` workflow only to export provider-neutral review context; use `--accept-local` only after explicit human approval of an already-applied component resolution, and never infer that either mode invokes AI or edits the component target.",
        "- Treat graph edges as conditional relationship candidates: select only task-relevant available nodes, traverse breadth-first without a depth cap, visit each node once, and report rather than re-enter cycle edges.",
        "- Do not infer a hosted API, callable agent endpoint, authentication service, or live MCP server from these source manifests.",
        "- Distinguish canonical source files from local runtime copies, generated outputs, and user-specific personalization.",
        "",
    ]
    return "\n".join(lines)


def component_markdown(record: dict[str, str]) -> str:
    public_suffix = ""
    if record["name"] != record["install_name"]:
        public_suffix = f"; public name `{record['name']}`"
    return (
        f"- [`{record['install_name']}`]({record['url']})"
        f" (`{record['qualified_name']}`{public_suffix}) — {record['description']}"
    )


def render_llms_full_txt(catalog: dict[str, object]) -> str:
    counts = catalog["counts"]
    lines = [
        "# Agent Company Plugins — Full Catalog",
        "",
        "> Complete source inventory for external LLMs and agents. Generated deterministically from repository metadata.",
        "",
        "## Scope",
        "",
        f"- Canonical repository: [{REPOSITORY}]({REPOSITORY_URL})",
        f"- Default branch: `{DEFAULT_BRANCH}`",
        (
            f"- Inventory: {counts['plugins']} plugins, {counts['skills']} skills, "  # type: ignore[index]
            f"{counts['commands']} commands, {counts['agents']} agents, and "  # type: ignore[index]
            f"{counts['rules']} rule sets"  # type: ignore[index]
        ),
        "- This document describes version-controlled source assets. It does not advertise a hosted API, agent endpoint, authentication service, or live MCP server.",
        "",
        "## Canonical Documents",
        "",
        f"- [README]({github_url('README.md')})",
        f"- [Agent guidance]({github_url('AGENTS.md')})",
        f"- [Quick Start]({github_url('QUICK_START.md')})",
        f"- [Installation contract]({github_url('references/docs/INSTALLATION.md')})",
        f"- [Requirement coverage]({github_url('references/docs/REQUIREMENT-COVERAGE.md')})",
        f"- [Architecture]({github_url('references/docs/ARCHITECTURE.md')})",
        f"- [Typed component graph]({raw_url('component-graph.json')})",
        f"- [Component graph contract]({raw_url('references/component-graph.json')})",
        f"- [Runtime context contract]({raw_url('references/runtime-contract.json')})",
        f"- [CodeMeta]({raw_url('codemeta.json')})",
        f"- [Citation metadata]({github_url('CITATION.cff')})",
        f"- [Changelog]({github_url('CHANGELOG.md')})",
        f"- [License]({github_url('LICENSE')})",
        f"- [Machine-readable catalog]({raw_url('catalog.json')})",
        "",
        "## Component Selection Rules",
        "",
        "- Prefer the narrowest component whose description matches the requested outcome.",
        "- A skill is an atomic or routing capability; a command is a stable workflow entry point; an agent orchestrates multi-step work; a rule set supplies department-wide defaults.",
        "- Use qualified names when the owning department matters.",
        "- Verify current installation guidance before copying source assets into a runtime or project.",
        "- Treat reconciliation bundles as suggestion-only local review data, never as source authority or proof that an update conflict was resolved; post-review `--accept-local` is explicit metadata adoption, not patch application.",
        "",
        "## Plugin Catalog",
        "",
    ]

    for plugin in catalog["plugins"]:  # type: ignore[assignment]
        lines += [
            f"### `{plugin['name']}`",
            "",
            plugin["mission"],
            "",
            f"- Version: `{plugin['version']}`",
            f"- Platforms declared by profile: {', '.join(f'`{item}`' for item in plugin['platforms'])}",
            f"- [Plugin source]({plugin['url']})",
            f"- [Profile]({plugin['profile']['url']})",
            f"- Team roles: {', '.join(plugin['team']) if plugin['team'] else 'not declared'}",
            "",
        ]
        for key, title in (
            ("skills", "Skills"),
            ("commands", "Commands"),
            ("agents", "Agents"),
            ("rules", "Rule sets"),
        ):
            records = plugin[key]
            lines += [f"#### {title} ({len(records)})", ""]
            if records:
                lines.extend(component_markdown(record) for record in records)
            else:
                lines.append("- None declared.")
            lines.append("")

    return "\n".join(lines)


def render_context7_json(catalog: dict[str, object]) -> str:
    counts = catalog["counts"]
    context = {
        "description": (
            "Agent Company is a source repository of portable department plugins, "
            "skills, commands, agents, and runtime-neutral rules for Claude, Codex, "
            "and Cursor."
        ),
        "excludeFolders": [
            ".git",
            ".github",
            ".playwright-mcp",
            "docs/audits",
            "docs/changelog",
            "scripts/tests",
        ],
        "rules": [
            (
                f"The checked-in catalog currently indexes {counts['plugins']} plugins, "  # type: ignore[index]
                f"{counts['skills']} skills, {counts['commands']} commands, and "  # type: ignore[index]
                f"{counts['agents']} agents."
            ),
            "Read catalog.json or llms-full.txt for current component paths, ownership, and descriptions.",
            "Read AGENTS.md for repository and installed-runtime invariants before modifying components.",
            "Treat each department profile.yaml as the canonical ordered inventory for its skills, commands, and agents.",
            "Treat SKILL.md and command or agent frontmatter descriptions as canonical routing summaries.",
            "Follow README.md and QUICK_START.md for current installation guidance; do not infer install paths from source layout alone.",
            "Treat project reconciliation bundles as provider-neutral, suggestion-only review data; only explicit post-review `--accept-local` may adopt an already-applied component resolution, and neither mode authorizes model invocation, patch application, or managed-target mutation.",
            "Use component-graph.json as the complete relationship inventory; use references/component-graph.json plus scripts/component_graph.py to regenerate and resolve cycle-safe conditional candidates.",
            "Use references/runtime-contract.json for inherited personalization and invocation-scoped variables.",
            "Do not infer a hosted API, callable agent endpoint, authentication service, or live MCP server from this source repository.",
        ],
    }
    return json.dumps(context, indent=2, ensure_ascii=False) + "\n"


def render_outputs(root: Path) -> dict[str, str]:
    catalog = build_catalog(root)
    return {
        "catalog.json": render_catalog_json(catalog),
        "llms.txt": render_llms_txt(catalog),
        "llms-full.txt": render_llms_full_txt(catalog),
        "context7.json": render_context7_json(catalog),
    }


def write_outputs(root: Path, outputs: dict[str, str]) -> None:
    for name in OUTPUT_FILES:
        (root / name).write_text(outputs[name], encoding="utf-8")


def stale_outputs(root: Path, outputs: dict[str, str]) -> list[str]:
    stale: list[str] = []
    for name in OUTPUT_FILES:
        path = root / name
        if not path.is_file() or path.read_text(encoding="utf-8") != outputs[name]:
            stale.append(name)
    return stale


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when checked-in artifacts differ from generated content",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        outputs = render_outputs(root)
    except (DiscoveryError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        stale = stale_outputs(root, outputs)
        if stale:
            print(f"stale discoverability artifacts: {', '.join(stale)}", file=sys.stderr)
            return 1
        print(f"Discoverability artifacts are current: {', '.join(OUTPUT_FILES)}")
        return 0

    write_outputs(root, outputs)
    print(f"Generated discoverability artifacts: {', '.join(OUTPUT_FILES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
