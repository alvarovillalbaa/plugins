#!/usr/bin/env python3
"""Build and inspect the repository's typed plugin-component graph.

The checked-in contract is intentionally a small overlay. Repository profiles,
component directories, the chaining map, and external registries remain the
authoritative inventories; this module derives nodes and inferred edges from
them on demand, then adds any explicitly declared typed references. Resolution
returns a relationship candidate closure for a host agent to evaluate; it does
not assert that every related component should execute for every request.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CONTRACT = "references/component-graph.json"
DEFAULT_GENERATED_GRAPH = "component-graph.json"
SCHEMA_VERSION = "1.0"
SLUG_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*"
COMPONENT_ID_RE = re.compile(
    rf"^(?:plugin:{SLUG_PATTERN}|(?:skill|command|rule|agent):{SLUG_PATTERN}/{SLUG_PATTERN}|external-skill:{SLUG_PATTERN})$"
)
BACKTICK_REF_RE = re.compile(r"`([^`]+)`")
RELATIONS = {
    "contains",
    "owns",
    "chains-to",
    "routes-to",
    "references",
    "invokes",
    "spawns",
    "uses",
}
EXECUTION_MODES = {"parallel", "sequential"}
SOURCE_FIELDS = {
    "profiles",
    "chain_map",
    "external_skills",
    "external_sources",
    "command_catalog",
}
REQUIRED_SOURCE_FIELDS = {
    "profiles",
    "chain_map",
    "external_skills",
    "external_sources",
}
DEFAULT_TRAVERSE_RELATIONS = sorted(RELATIONS)


class GraphError(ValueError):
    """Raised when the graph contract or a discovered relationship is invalid."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GraphError(f"duplicate JSON key `{key}`")
        result[key] = value
    return result


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except FileNotFoundError as exc:
        raise GraphError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GraphError(f"{path}:{exc.lineno}: invalid JSON: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise GraphError(f"{path}: root must be an object")
    return data


def _relative_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GraphError(f"{field}: must be a non-empty relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise GraphError(f"{field}: must remain inside the repository")
    return value


def _component_id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not COMPONENT_ID_RE.fullmatch(value):
        raise GraphError(f"{field}: invalid canonical component id `{value}`")
    return value


def load_contract(root: Path, contract_path: Path | None = None) -> tuple[Path, dict[str, Any]]:
    root = root.resolve()
    path = (contract_path or root / DEFAULT_CONTRACT).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise GraphError(f"contract must be inside repository root: {path}") from exc
    data = _read_json(path)

    allowed_root = {"$schema", "schema_version", "sources", "resolution", "references"}
    unknown = sorted(set(data) - allowed_root)
    if unknown:
        raise GraphError(f"{path}: unsupported field(s): {', '.join(unknown)}")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise GraphError(f"{path}: schema_version must be `{SCHEMA_VERSION}`")

    sources = data.get("sources")
    if not isinstance(sources, dict):
        raise GraphError(f"{path}: sources must be an object")
    unknown_sources = sorted(set(sources) - SOURCE_FIELDS)
    missing_sources = sorted(REQUIRED_SOURCE_FIELDS - set(sources))
    if unknown_sources:
        raise GraphError(f"{path}: unsupported source(s): {', '.join(unknown_sources)}")
    if missing_sources:
        raise GraphError(f"{path}: missing source(s): {', '.join(missing_sources)}")
    for key, value in sources.items():
        sources[key] = _relative_path(value, f"sources.{key}")

    resolution = data.get("resolution")
    if not isinstance(resolution, dict):
        raise GraphError(f"{path}: resolution must be an object")
    expected_resolution = {
        "strategy": "breadth-first",
        "breadth_execution": "parallel",
        "cycle_policy": "visit-once-report-edges",
    }
    unknown_resolution = sorted(
        set(resolution) - {*expected_resolution, "traverse_relations"}
    )
    if unknown_resolution:
        raise GraphError(f"{path}: unsupported resolution field(s): {', '.join(unknown_resolution)}")
    for key, expected in expected_resolution.items():
        if resolution.get(key) != expected:
            raise GraphError(f"{path}: resolution.{key} must be `{expected}`")
    traverse = resolution.get("traverse_relations")
    if not isinstance(traverse, list) or not traverse:
        raise GraphError(f"{path}: resolution.traverse_relations must be a non-empty array")
    if any(not isinstance(item, str) or item not in RELATIONS for item in traverse):
        raise GraphError(f"{path}: resolution.traverse_relations contains an unsupported relation")
    if len(traverse) != len(set(traverse)):
        raise GraphError(f"{path}: resolution.traverse_relations must be unique")

    references = data.get("references")
    if not isinstance(references, list):
        raise GraphError(f"{path}: references must be an array")
    allowed_reference = {"from", "to", "relation", "execution", "note"}
    seen_references: set[tuple[str, str, str, str]] = set()
    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(references):
        location = f"{path}:references[{index}]"
        if not isinstance(raw, dict):
            raise GraphError(f"{location}: must be an object")
        extra = sorted(set(raw) - allowed_reference)
        if extra:
            raise GraphError(f"{location}: unsupported field(s): {', '.join(extra)}")
        source = _component_id(raw.get("from"), f"{location}.from")
        target = _component_id(raw.get("to"), f"{location}.to")
        relation = raw.get("relation")
        if not isinstance(relation, str) or relation not in RELATIONS:
            raise GraphError(f"{location}.relation: unsupported relation `{relation}`")
        execution = raw.get("execution", "parallel")
        if not isinstance(execution, str) or execution not in EXECUTION_MODES:
            raise GraphError(f"{location}.execution: must be parallel or sequential")
        note = raw.get("note")
        if note is not None and (not isinstance(note, str) or not note.strip()):
            raise GraphError(f"{location}.note: must be a non-empty string")
        key = (source, target, relation, execution)
        if key in seen_references:
            raise GraphError(f"{location}: duplicate explicit reference")
        seen_references.add(key)
        item: dict[str, Any] = {
            "from": source,
            "to": target,
            "relation": relation,
            "execution": execution,
        }
        if note is not None:
            item["note"] = note.strip()
        normalized.append(item)
    data["references"] = normalized
    return path, data


def _rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _profile_slug(path: Path) -> str:
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("slug:"):
            slug = raw.split(":", 1)[1].strip().strip('"').strip("'")
            if re.fullmatch(SLUG_PATTERN, slug):
                return slug
            raise GraphError(f"{path}: invalid plugin slug `{slug}`")
    raise GraphError(f"{path}: missing plugin slug")


def _registry_entries(path: Path, section: str) -> dict[str, dict[str, str]]:
    if not path.is_file():
        raise GraphError(f"registry not found: {path}")
    entries: dict[str, dict[str, str]] = {}
    current: str | None = None
    active = False
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == f"{section}:":
            active = True
            current = None
            continue
        if not active:
            continue
        if re.fullmatch(rf"  {SLUG_PATTERN}:", line):
            current = stripped[:-1]
            if current in entries:
                raise GraphError(f"{path}:{line_number}: duplicate registry name `{current}`")
            entries[current] = {}
            continue
        if current and line.startswith("    ") and ":" in stripped:
            key, value = stripped.split(":", 1)
            entries[current][key.strip()] = value.strip().strip('"').strip("'")
            continue
        raise GraphError(f"{path}:{line_number}: unsupported registry line")
    return entries


class GraphBuilder:
    def __init__(self, root: Path, contract_path: Path, contract: dict[str, Any]) -> None:
        self.root = root.resolve()
        self.contract_path = contract_path
        self.contract = contract
        self.nodes: dict[str, dict[str, Any]] = {}
        self._edges: dict[tuple[str, str, str, str], set[str]] = {}

    def add_node(self, node: dict[str, Any]) -> None:
        node_id = _component_id(node.get("id"), "node.id")
        existing = self.nodes.get(node_id)
        if existing is not None and existing != node:
            raise GraphError(f"conflicting node declarations for `{node_id}`")
        self.nodes[node_id] = node

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        origin: str,
        execution: str = "parallel",
    ) -> None:
        _component_id(source, "edge.from")
        _component_id(target, "edge.to")
        if relation not in RELATIONS:
            raise GraphError(f"edge relation `{relation}` is unsupported")
        if execution not in EXECUTION_MODES:
            raise GraphError(f"edge execution `{execution}` is unsupported")
        self._edges.setdefault((source, target, relation, execution), set()).add(origin)

    def scan_plugins(self) -> None:
        profile_glob = self.contract["sources"]["profiles"]
        profiles = sorted(path for path in self.root.glob(profile_glob) if path.is_file())
        if not profiles:
            raise GraphError(f"profile scan `{profile_glob}` found no plugins")
        component_specs = {
            "skill": ("skills/*/SKILL.md", lambda path: path.parent.name),
            "command": ("commands/*.md", lambda path: path.stem),
            "rule": ("rules/*.md", lambda path: path.stem),
            "agent": ("agents/*.md", lambda path: path.stem),
        }
        for profile in profiles:
            plugin_dir = profile.parent
            plugin = _profile_slug(profile)
            if plugin != plugin_dir.name:
                raise GraphError(f"{profile}: slug `{plugin}` must match directory `{plugin_dir.name}`")
            plugin_id = f"plugin:{plugin}"
            self.add_node(
                {
                    "id": plugin_id,
                    "kind": "plugin",
                    "name": plugin,
                    "path": _rel(plugin_dir, self.root),
                }
            )
            for kind, (pattern, name_for) in component_specs.items():
                for path in sorted(candidate for candidate in plugin_dir.glob(pattern) if candidate.is_file()):
                    if path.name == "README.md":
                        continue
                    name = name_for(path)
                    if not re.fullmatch(SLUG_PATTERN, name):
                        raise GraphError(f"{path}: component name `{name}` is not canonical")
                    node_id = f"{kind}:{plugin}/{name}"
                    self.add_node(
                        {
                            "id": node_id,
                            "kind": kind,
                            "plugin": plugin,
                            "name": name,
                            "path": _rel(path.parent if kind == "skill" else path, self.root),
                        }
                    )
                    self.add_edge(plugin_id, node_id, "contains", _rel(profile, self.root))

    def scan_external(self) -> None:
        sources = self.contract["sources"]
        registries = (
            (sources["external_skills"], "skills", True),
            (sources["external_sources"], "sources", False),
        )
        for relative, section, installable in registries:
            path = self.root / relative
            for name, metadata in sorted(_registry_entries(path, section).items()):
                node_id = f"external-skill:{name}"
                if node_id in self.nodes:
                    raise GraphError(f"external registry name `{name}` is declared more than once")
                node: dict[str, Any] = {
                    "id": node_id,
                    "kind": "external-skill",
                    "name": name,
                    "path": _rel(path, self.root),
                    "installable": installable,
                }
                for field in ("owner", "repo", "ref", "domain", "install_name"):
                    if metadata.get(field):
                        node[field] = metadata[field]
                self.add_node(node)

    def _skill_index(self) -> dict[str, list[str]]:
        return self._component_index("skill")

    def _component_index(self, kind: str) -> dict[str, list[str]]:
        index: dict[str, list[str]] = {}
        for node_id, node in self.nodes.items():
            if node["kind"] == kind:
                index.setdefault(str(node["name"]), []).append(node_id)
        return {key: sorted(value) for key, value in index.items()}

    def _declared_component(
        self,
        ref: str,
        *,
        kind: str,
        plugin: str,
        index: dict[str, list[str]],
        location: str,
    ) -> str:
        typed_prefix = f"{kind}:"
        if ref.startswith(typed_prefix):
            target = _component_id(ref, location)
            if target not in self.nodes:
                raise GraphError(f"{location}: unknown {kind} `{ref}`")
            return target
        if ":" in ref:
            raise GraphError(f"{location}: expected a {kind} reference, got `{ref}`")
        if "/" in ref:
            parts = ref.split("/")
            if len(parts) != 2 or any(not re.fullmatch(SLUG_PATTERN, part) for part in parts):
                raise GraphError(f"{location}: invalid qualified {kind} reference `{ref}`")
            target = f"{kind}:{parts[0]}/{parts[1]}"
            if target not in self.nodes:
                raise GraphError(f"{location}: unknown {kind} `{ref}`")
            return target
        if not re.fullmatch(SLUG_PATTERN, ref):
            raise GraphError(f"{location}: invalid {kind} reference `{ref}`")

        local = f"{kind}:{plugin}/{ref}"
        if local in self.nodes:
            return local
        matches = index.get(ref, [])
        if not matches:
            raise GraphError(f"{location}: unknown {kind} `{ref}`")
        if len(matches) > 1:
            raise GraphError(
                f"{location}: ambiguous {kind} `{ref}`; qualify it as `<plugin>/{ref}`: "
                f"{', '.join(matches)}"
            )
        return matches[0]

    @staticmethod
    def _markdown_section_lines(
        path: Path,
        headings: set[str],
    ) -> Iterable[tuple[str, int, str]]:
        canonical_headings = {heading.casefold(): heading for heading in headings}
        active: str | None = None
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if raw.startswith("## "):
                heading = raw[3:].strip()
                active = canonical_headings.get(heading.casefold())
                continue
            if active is not None:
                yield active, line_number, raw

    def scan_agent_declarations(self) -> None:
        declarations = {
            "Primary skills": ("skill", "uses"),
            "Commands": ("command", "invokes"),
        }
        indices = {
            kind: self._component_index(kind)
            for kind, _ in declarations.values()
        }
        agent_index = self._component_index("agent")
        agents = sorted(
            (node for node in self.nodes.values() if node["kind"] == "agent"),
            key=lambda node: node["id"],
        )
        for agent in agents:
            path = self.root / agent["path"]
            for heading, line_number, raw in self._markdown_section_lines(
                path, {*declarations, "Routing boundaries"}
            ):
                if heading == "Routing boundaries":
                    location = f"{agent['path']}:{line_number}"
                    for ref in BACKTICK_REF_RE.findall(raw):
                        target = self._known_agent(
                            ref,
                            plugin=str(agent["plugin"]),
                            index=agent_index,
                            location=location,
                        )
                        if target is not None:
                            self.add_edge(agent["id"], target, "routes-to", location)
                    continue
                if not re.match(r"^\s*-\s+", raw):
                    continue
                kind, relation = declarations[heading]
                location = f"{agent['path']}:{line_number}"
                for ref in BACKTICK_REF_RE.findall(raw):
                    target = self._declared_component(
                        ref,
                        kind=kind,
                        plugin=str(agent["plugin"]),
                        index=indices[kind],
                        location=location,
                    )
                    self.add_edge(agent["id"], target, relation, location)

    def _known_agent(
        self,
        ref: str,
        *,
        plugin: str,
        index: dict[str, list[str]],
        location: str,
    ) -> str | None:
        if ref.startswith("agent:"):
            target = _component_id(ref, location)
            if target not in self.nodes:
                raise GraphError(f"{location}: unknown agent `{ref}`")
            return target
        if re.fullmatch(rf"{SLUG_PATTERN}/{SLUG_PATTERN}", ref):
            target = f"agent:{ref}"
            return target if target in self.nodes else None
        if not re.fullmatch(SLUG_PATTERN, ref):
            return None
        local = f"agent:{plugin}/{ref}"
        if local in self.nodes:
            return local
        matches = index.get(ref, [])
        if len(matches) > 1:
            raise GraphError(
                f"{location}: ambiguous agent `{ref}`; qualify it as `<plugin>/{ref}`: "
                f"{', '.join(matches)}"
            )
        return matches[0] if matches else None

    def scan_rule_routes(self) -> None:
        skill_index = self._skill_index()
        rules = sorted(
            (
                node
                for node in self.nodes.values()
                if node["kind"] == "rule" and node["name"] == "defaults"
            ),
            key=lambda node: node["id"],
        )
        for rule in rules:
            path = self.root / rule["path"]
            for _, line_number, raw in self._markdown_section_lines(
                path, {"Routing constraints"}
            ):
                location = f"{rule['path']}:{line_number}"
                for ref in BACKTICK_REF_RE.findall(raw):
                    if ref.startswith("plugin:") or re.match(
                        r"^(?:command|rule|agent|external-skill):", ref
                    ):
                        continue
                    if not (
                        ref.startswith("skill:")
                        or re.fullmatch(SLUG_PATTERN, ref)
                        or re.fullmatch(rf"{SLUG_PATTERN}/{SLUG_PATTERN}", ref)
                    ):
                        continue
                    local = f"skill:{rule['plugin']}/{ref}"
                    if "/" not in ref and not ref.startswith("skill:"):
                        if local not in self.nodes and f"plugin:{ref}" in self.nodes:
                            continue
                    target = self._declared_component(
                        ref,
                        kind="skill",
                        plugin=str(rule["plugin"]),
                        index=skill_index,
                        location=location,
                    )
                    self.add_edge(rule["id"], target, "routes-to", location)

    @staticmethod
    def _unique_skill(name: str, index: dict[str, list[str]], location: str) -> str:
        matches = index.get(name, [])
        if not matches:
            raise GraphError(f"{location}: unknown skill `{name}`")
        if len(matches) > 1:
            raise GraphError(
                f"{location}: ambiguous skill `{name}`; use a typed explicit reference instead: {', '.join(matches)}"
            )
        return matches[0]

    def scan_chain_map(self) -> None:
        path = self.root / self.contract["sources"]["chain_map"]
        if not path.is_file():
            raise GraphError(f"chain map not found: {path}")
        internal_rows: list[tuple[int, str, list[str], list[str]]] = []
        external_rows: list[tuple[int, list[str], list[str]]] = []
        section: str | None = None
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if raw.startswith("## External Chains"):
                section = "external"
                continue
            if raw.startswith("## Chains"):
                section = "internal"
                continue
            if raw.startswith("## "):
                section = None
                continue
            if not raw.startswith("| `"):
                continue
            cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
            if section == "external" and len(cells) >= 2:
                external_rows.append(
                    (line_number, BACKTICK_REF_RE.findall(cells[0]), BACKTICK_REF_RE.findall(cells[1]))
                )
            elif section == "internal" and len(cells) >= 3:
                parents = BACKTICK_REF_RE.findall(cells[0])
                if parents:
                    children = [] if cells[1] == "—" else BACKTICK_REF_RE.findall(cells[1])
                    internal_rows.append((line_number, parents[0], children, BACKTICK_REF_RE.findall(cells[2])))

        skill_index = self._skill_index()
        owner_by_child: dict[str, str] = {}
        for line_number, parent, children, _ in internal_rows:
            for child in children:
                existing = owner_by_child.get(child)
                if existing and existing != parent:
                    raise GraphError(
                        f"{_rel(path, self.root)}:{line_number}: child `{child}` is owned by both `{existing}` and `{parent}`"
                    )
                owner_by_child[child] = parent

        def internal_target(ref: str, location: str) -> str:
            if ref.startswith("skill:"):
                target = _component_id(ref, location)
                if target not in self.nodes:
                    raise GraphError(f"{location}: unknown component `{target}`")
                return target
            if "/" not in ref:
                return self._unique_skill(ref, skill_index, location)
            parts = ref.split("/")
            if len(parts) != 2 or any(not re.fullmatch(SLUG_PATTERN, part) for part in parts):
                raise GraphError(f"{location}: invalid legacy parent/child reference `{ref}`")
            parent, child = parts
            if owner_by_child.get(child) != parent:
                raise GraphError(f"{location}: `{ref}` is not a declared parent/child relationship")
            return self._unique_skill(child, skill_index, location)

        for line_number, parent, children, chains in internal_rows:
            location = f"{_rel(path, self.root)}:{line_number}"
            source = self._unique_skill(parent, skill_index, location)
            for child in children:
                self.add_edge(
                    source,
                    self._unique_skill(child, skill_index, location),
                    "owns",
                    location,
                )
            for ref in chains:
                self.add_edge(source, internal_target(ref, location), "chains-to", location)

        for line_number, internal_names, external_names in external_rows:
            location = f"{_rel(path, self.root)}:{line_number}"
            for internal_name in internal_names:
                source = self._unique_skill(internal_name, skill_index, location)
                for external_name in external_names:
                    target = f"external-skill:{external_name}"
                    if target not in self.nodes:
                        raise GraphError(f"{location}: unknown external skill or source `{external_name}`")
                    self.add_edge(source, target, "chains-to", location)

    def scan_command_catalog(self) -> None:
        relative = self.contract["sources"].get("command_catalog")
        if not relative:
            return
        path = self.root / relative
        data = _read_json(path)
        commands = data.get("commands", [])
        if not isinstance(commands, list):
            raise GraphError(f"{path}: commands must be an array")
        for index, raw in enumerate(commands):
            location = f"{_rel(path, self.root)}:commands[{index}]"
            if not isinstance(raw, dict):
                raise GraphError(f"{location}: must be an object")
            command_path = raw.get("path")
            owner = raw.get("owner")
            if not isinstance(command_path, str) or not isinstance(owner, str):
                raise GraphError(f"{location}: path and owner are required")
            parts = Path(command_path).parts
            if len(parts) != 3 or parts[1] != "commands" or not parts[2].endswith(".md"):
                raise GraphError(f"{location}: path must be `<plugin>/commands/<name>.md`")
            source = f"command:{parts[0]}/{Path(parts[2]).stem}"
            target = f"skill:{owner}"
            self.add_edge(source, target, "routes-to", location, execution="sequential")

    def add_explicit_references(self) -> None:
        origin = _rel(self.contract_path, self.root)
        for raw in self.contract["references"]:
            self.add_edge(
                raw["from"],
                raw["to"],
                raw["relation"],
                origin,
                execution=raw["execution"],
            )

    def finish(self) -> dict[str, Any]:
        edges: list[dict[str, Any]] = []
        for (source, target, relation, execution), origins in sorted(self._edges.items()):
            if source not in self.nodes:
                raise GraphError(f"edge references unknown source `{source}`")
            if target not in self.nodes:
                raise GraphError(f"edge references unknown target `{target}`")
            edges.append(
                {
                    "from": source,
                    "to": target,
                    "relation": relation,
                    "execution": execution,
                    "origins": sorted(origins),
                }
            )
        return {
            "schema_version": SCHEMA_VERSION,
            "artifact_kind": "component-relationship-graph",
            "contract": _rel(self.contract_path, self.root),
            "semantics": {
                "relationships": "conditional-candidates-not-unconditional-execution",
                "activation": "host-selects-relevant-available-candidates",
            },
            "resolution": self.contract["resolution"],
            "nodes": [self.nodes[node_id] for node_id in sorted(self.nodes)],
            "edges": edges,
        }


def build_graph(root: Path, contract_path: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    resolved_contract, contract = load_contract(root, contract_path)
    builder = GraphBuilder(root, resolved_contract, contract)
    builder.scan_plugins()
    builder.scan_agent_declarations()
    builder.scan_rule_routes()
    builder.scan_external()
    builder.scan_chain_map()
    builder.scan_command_catalog()
    builder.add_explicit_references()
    return builder.finish()


def load_graph(path: Path) -> dict[str, Any]:
    """Load a generated graph, including installed-runtime availability flags."""

    graph = _read_json(path)
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise GraphError(f"{path}: generated graph must contain nodes and edges arrays")

    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        location = f"{path}:nodes[{index}]"
        if not isinstance(node, dict):
            raise GraphError(f"{location}: must be an object")
        node_id = _component_id(node.get("id"), f"{location}.id")
        if node_id in node_ids:
            raise GraphError(f"{location}: duplicate node `{node_id}`")
        installed = node.get("installed")
        if installed is not None and not isinstance(installed, bool):
            raise GraphError(f"{location}.installed: must be a boolean when present")
        node_ids.add(node_id)

    for index, edge in enumerate(edges):
        location = f"{path}:edges[{index}]"
        if not isinstance(edge, dict):
            raise GraphError(f"{location}: must be an object")
        source = _component_id(edge.get("from"), f"{location}.from")
        target = _component_id(edge.get("to"), f"{location}.to")
        if source not in node_ids or target not in node_ids:
            raise GraphError(f"{location}: edge endpoint is missing from nodes")
        if edge.get("relation") not in RELATIONS:
            raise GraphError(f"{location}.relation: unsupported relation")
        if edge.get("execution") not in EXECUTION_MODES:
            raise GraphError(f"{location}.execution: must be parallel or sequential")
    return graph


def _filtered_edges(graph: dict[str, Any], relations: set[str], node_ids: set[str] | None = None) -> list[dict[str, Any]]:
    result = []
    for edge in graph["edges"]:
        if edge["relation"] not in relations:
            continue
        if node_ids is not None and (edge["from"] not in node_ids or edge["to"] not in node_ids):
            continue
        result.append(edge)
    return result


def cycle_edges(
    graph: dict[str, Any],
    relations: Iterable[str] | None = None,
    node_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Return every edge that belongs to a directed cycle, without recursion."""
    allowed = set(relations or DEFAULT_TRAVERSE_RELATIONS)
    selected_nodes = (
        node_ids if node_ids is not None else {node["id"] for node in graph["nodes"]}
    )
    edges = _filtered_edges(graph, allowed, selected_nodes)
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in selected_nodes}
    reverse: dict[str, list[str]] = {node_id: [] for node_id in selected_nodes}
    for edge in edges:
        adjacency[edge["from"]].append(edge["to"])
        reverse[edge["to"]].append(edge["from"])
    for values in (*adjacency.values(), *reverse.values()):
        values[:] = sorted(set(values))

    seen: set[str] = set()
    finish_order: list[str] = []
    for start in sorted(selected_nodes):
        if start in seen:
            continue
        seen.add(start)
        stack: list[tuple[str, int]] = [(start, 0)]
        while stack:
            node, index = stack[-1]
            neighbors = adjacency[node]
            if index < len(neighbors):
                target = neighbors[index]
                stack[-1] = (node, index + 1)
                if target not in seen:
                    seen.add(target)
                    stack.append((target, 0))
                continue
            stack.pop()
            finish_order.append(node)

    component_by_node: dict[str, int] = {}
    component_sizes: dict[int, int] = {}
    for start in reversed(finish_order):
        if start in component_by_node:
            continue
        component_id = len(component_sizes)
        members: list[str] = []
        stack = [start]
        component_by_node[start] = component_id
        while stack:
            node = stack.pop()
            members.append(node)
            for target in reversed(reverse[node]):
                if target not in component_by_node:
                    component_by_node[target] = component_id
                    stack.append(target)
        component_sizes[component_id] = len(members)

    result = []
    for edge in edges:
        source_component = component_by_node[edge["from"]]
        if source_component != component_by_node[edge["to"]]:
            continue
        if component_sizes[source_component] > 1 or edge["from"] == edge["to"]:
            result.append(edge)
    return result


def resolve_graph(
    graph: dict[str, Any],
    root_id: str,
    relations: Iterable[str] | None = None,
    *,
    available_only: bool = False,
) -> dict[str, Any]:
    """Resolve a finite breadth-first candidate closure from a cyclic graph.

    Traversal has no depth limit. Each canonical node is considered once, nodes
    discovered at the same breadth are exposed as deterministic parallel or
    sequential *candidates*. Sequential edges within one breadth keep their
    targets out of that breadth's parallel group and are returned as ordered
    constraints. Cycle edges are reported rather than followed repeatedly. The
    host still decides which candidates are relevant to the current request.
    With ``available_only=True``, a node explicitly marked ``installed: false``
    is not admitted to the closure; the rejected node and incoming relationship
    are reported instead.
    """
    _component_id(root_id, "root")
    nodes_by_id = {node["id"]: node for node in graph["nodes"]}
    node_ids = set(nodes_by_id)
    if root_id not in node_ids:
        raise GraphError(f"unknown component `{root_id}`")
    allowed = set(relations or graph.get("resolution", {}).get("traverse_relations", DEFAULT_TRAVERSE_RELATIONS))
    unknown_relations = sorted(allowed - RELATIONS)
    if unknown_relations:
        raise GraphError(f"unsupported traversal relation(s): {', '.join(unknown_relations)}")

    adjacency: dict[str, list[dict[str, Any]]] = {node_id: [] for node_id in node_ids}
    for edge in _filtered_edges(graph, allowed):
        adjacency[edge["from"]].append(edge)
    for node_id in adjacency:
        adjacency[node_id].sort(
            key=lambda edge: (edge["to"], edge["relation"], edge["execution"])
        )

    root_unavailable = available_only and nodes_by_id[root_id].get("installed") is False
    visited: set[str] = set() if root_unavailable else {root_id}
    frontier = [] if root_unavailable else [root_id]
    frontier_modes = {} if root_unavailable else {root_id: "sequential"}
    levels: list[dict[str, Any]] = []
    considered_edges: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    ordered_constraints: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    blocked_edges: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    unavailable_ids: set[str] = {root_id} if root_unavailable else set()
    depth = 0
    while frontier:
        frontier_ids = set(frontier)
        for node in sorted(frontier):
            for edge in adjacency[node]:
                if edge["execution"] == "sequential" and edge["to"] in frontier_ids:
                    frontier_modes[edge["to"]] = "sequential"
        parallel = sorted(node for node in frontier if frontier_modes[node] == "parallel")
        sequential = sorted(node for node in frontier if frontier_modes[node] == "sequential")
        levels.append(
            {
                "depth": depth,
                "candidates": sorted(frontier),
                "parallel_candidates": parallel,
                "sequential_candidates": sequential,
            }
        )
        next_modes: dict[str, set[str]] = {}
        for node in sorted(frontier):
            for edge in adjacency[node]:
                key = (edge["from"], edge["to"], edge["relation"], edge["execution"])
                if available_only and nodes_by_id[edge["to"]].get("installed") is False:
                    unavailable_ids.add(edge["to"])
                    blocked_edges[key] = {
                        **edge,
                        "blocked_reason": "target-installed-false",
                    }
                    continue
                considered_edges[key] = edge
                if edge["execution"] == "sequential":
                    ordered_constraints[key] = edge
                if edge["to"] in visited:
                    continue
                next_modes.setdefault(edge["to"], set()).add(edge["execution"])
        frontier = sorted(next_modes)
        frontier_modes = {
            node: "sequential" if "sequential" in modes else "parallel"
            for node, modes in next_modes.items()
        }
        visited.update(frontier)
        depth += 1

    cycles = cycle_edges(graph, allowed, visited)
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "component-relationship-candidate-closure",
        "root": root_id,
        "candidate_semantics": (
            "relationships-require-host-relevance-selection-before-execution"
        ),
        "policy": "breadth-first-candidates-visit-once",
        "availability_filter": (
            "exclude-installed-false" if available_only else "include-all-nodes"
        ),
        "relations": sorted(allowed),
        "candidate_count": len(visited),
        "levels": levels,
        "cycle_edges": cycles,
        "considered_edges": [considered_edges[key] for key in sorted(considered_edges)],
        "ordered_constraints": [
            ordered_constraints[key] for key in sorted(ordered_constraints)
        ],
        "blocked_edges": [blocked_edges[key] for key in sorted(blocked_edges)],
        "unavailable_nodes": [nodes_by_id[node_id] for node_id in sorted(unavailable_ids)],
    }


def _render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=False) + "\n"


def _write_json(data: dict[str, Any], output: str | None) -> None:
    rendered = _render_json(data)
    if not output or output == "-":
        print(rendered, end="")
        return
    path = Path(output).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    print(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build and resolve the typed plugin-component graph.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="derive the complete graph from repository sources")
    build.add_argument("--root", default=".", help="repository root")
    build.add_argument("--contract", help=f"contract path (default: {DEFAULT_CONTRACT})")
    build.add_argument("--output", help="write generated graph JSON here; default is stdout")
    build.add_argument(
        "--check",
        action="store_true",
        help=(
            f"verify the checked-in full graph is current (default: {DEFAULT_GENERATED_GRAPH})"
        ),
    )

    resolve = subparsers.add_parser(
        "resolve", help="inspect one component's cycle-safe relationship candidate closure"
    )
    resolve.add_argument("component", help="canonical component id")
    resolve.add_argument("--root", default=".", help="repository root")
    resolve_source = resolve.add_mutually_exclusive_group()
    resolve_source.add_argument(
        "--contract", help=f"source overlay path (default: {DEFAULT_CONTRACT})"
    )
    resolve_source.add_argument(
        "--graph",
        help=(
            "existing full graph JSON to inspect; use a project's "
            ".agents/component-graph.json for installed flags"
        ),
    )
    resolve.add_argument("--relation", action="append", choices=sorted(RELATIONS), help="traverse only this relation; repeatable")
    resolve.add_argument(
        "--available-only",
        action="store_true",
        help="exclude nodes explicitly marked installed:false and report blocked relationships",
    )
    resolve.add_argument("--output", help="write resolution JSON here; default is stdout")
    return parser


def _contract_arg(root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def _output_arg(root: Path, value: str | None) -> Path:
    if value is None:
        return root / DEFAULT_GENERATED_GRAPH
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def _input_arg(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    try:
        if args.command == "build":
            graph = build_graph(root, _contract_arg(root, args.contract))
            if args.check:
                output = _output_arg(root, args.output)
                expected = _render_json(graph)
                if not output.is_file():
                    raise GraphError(
                        f"generated graph is missing: {output}; regenerate with "
                        f"`python3 scripts/component_graph.py build --root {root} "
                        f"--output {output}`"
                    )
                if output.read_text(encoding="utf-8") != expected:
                    raise GraphError(
                        f"generated graph is stale: {output}; regenerate with "
                        f"`python3 scripts/component_graph.py build --root {root} "
                        f"--output {output}`"
                    )
                cycles = cycle_edges(graph, graph["resolution"]["traverse_relations"])
                print(
                    f"Generated component graph is current with {len(graph['nodes'])} node(s), "
                    f"{len(graph['edges'])} edge(s), and {len(cycles)} preserved cycle edge(s)."
                )
                return 0
            output = args.output
            if output and output != "-":
                output = str(_output_arg(root, output))
            _write_json(graph, output)
            return 0
        graph = (
            load_graph(_input_arg(root, args.graph))
            if args.graph
            else build_graph(root, _contract_arg(root, args.contract))
        )
        result = resolve_graph(
            graph,
            args.component,
            args.relation,
            available_only=args.available_only,
        )
        _write_json(result, args.output)
        return 0
    except (GraphError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
