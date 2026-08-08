#!/usr/bin/env python3
"""Project-local installer for the plugin bundle.

The module is intentionally independent from ``skillctl.py`` so the existing CLI
can use it through a thin adapter.  It installs source components into the
runtime-neutral ``.agents`` project tree, records ownership and upstream bases,
and performs conservative three-way updates that never silently replace local
work.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Sequence
from urllib.parse import quote, unquote


KINDS = ("skill", "command", "rule", "agent")
KIND_DIRECTORIES = {
    "skill": "skills",
    "command": "commands",
    "rule": "rules",
    "agent": "agents",
}
LOCK_VERSION = 1
LOCK_NAME = ".plugin-lock.json"
STATE_DIRECTORY = ".plugin-state"
UPDATE_DIRECTORY = ".updates"
CONFLICT_BASE_DIRECTORY = ".plugin-state/conflict-bases"
SINGLE_FILE_KEY = "__component_file__"
COMMAND_CAPABILITY_REGISTRY = Path("references/command-capabilities.json")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
QUALIFIED_TARGET_SEPARATOR = "__"
SOURCE_IGNORED_DIRECTORIES = {
    ".git",
    ".overlays",
    ".generated",
    ".company",
    ".user",
    ".skill-improvements",
    ".worktrees",
    "__pycache__",
    "node_modules",
}
SOURCE_IGNORED_FILES = {
    ".DS_Store",
    ".skill-lock.yml",
    ".skill-lock.json",
    LOCK_NAME,
}
COMPONENT_RENAMES = {
    "skill:system/skills-management": "skill:system/plugins-management",
    "skill:engineering/computer-vision-systems": "skill:engineering/computer-vision",
    "skill:engineering/context-memory-rag": "skill:engineering/context-engineering",
    "skill:engineering/prompt-tool-design": "skill:engineering/prompt-engineering",
    "skill:marketing/seo-and-geo": "skill:marketing/seo",
}
SOURCE_EXTERNAL_INSTALLER_RE = re.compile(
    r"\bpython(?:3)? scripts/install-external-skills\.py"
)
PROJECT_EXTERNAL_INSTALLER = (
    "python3 .agents/runtime-support/install-external-skills.py"
)
PROJECT_EXTERNAL_INSTALL_RE = re.compile(
    r"python(?:3)? \.agents/runtime-support/install-external-skills\.py[^`\r\n]*"
)
PORTABLE_COMPONENT_SKILL_PATH_RE = re.compile(
    r"(?P<claude>\$\{CLAUDE_PLUGIN_ROOT\}/skills/"
    r"(?P<claude_name>[a-z0-9][a-z0-9-]*))"
    r"|(?<![A-Za-z0-9_./-])(?P<qualified_plugin>[a-z0-9][a-z0-9-]*)/skills/"
    r"(?P<qualified_name>[a-z0-9][a-z0-9-]*)"
    r"|(?<![A-Za-z0-9_./-])(?P<parent>\.\./skills/"
    r"(?P<parent_name>[a-z0-9][a-z0-9-]*))"
    r"|(?<![A-Za-z0-9_./-])(?P<bare>skills/"
    r"(?P<bare_name>[a-z0-9][a-z0-9-]*))"
)
MARKDOWN_DESTINATION_RE = re.compile(r"\]\(\s*<?(?P<target>[^\s)>]+)")
INLINE_CODE_RE = re.compile(r"(?<!`)`(?P<code>[^`\r\n]+)`(?!`)")
SHARED_RUNTIME_TARGETS = {
    "skills-chaining-map.md": Path("runtime-support/skills-chaining-map.md"),
    "references/external-skills.yaml": Path(
        "runtime-support/external-skills.yaml"
    ),
    "references/external-sources.yaml": Path(
        "runtime-support/external-sources.yaml"
    ),
    "references/docs/promotion-matrix.md": Path(
        "runtime-support/promotion-matrix.md"
    ),
    "references/docs/INSTALLATION.md": Path("runtime-support/INSTALLATION.md"),
    "references/component-graph.json": Path("component-graph.json"),
    "references/runtime-contract.json": Path("runtime-contract.json"),
}


class InstallerError(Exception):
    """Base error for project installer failures."""


class SelectorError(InstallerError):
    """A typed selector is malformed or cannot be resolved."""


class UnmanagedTargetError(InstallerError):
    """An install would overwrite a path not owned by the lock."""


class OwnershipConflictError(InstallerError):
    """Two managed components claim the same flat target."""


class UnsafePathError(InstallerError):
    """A source, target, or saved base contains an unsafe path type."""


@dataclass(frozen=True)
class FileValue:
    kind: str
    data: bytes
    mode: int

    @property
    def digest(self) -> str:
        digest = hashlib.sha256()
        digest.update(self.kind.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(self.mode).encode("ascii"))
        digest.update(b"\0")
        digest.update(self.data)
        return digest.hexdigest()


@dataclass(frozen=True)
class Snapshot:
    entries: dict[str, FileValue]


@dataclass(frozen=True)
class Component:
    kind: str
    plugin: str
    name: str
    source_path: Path
    source_relative: Path
    target_relative: Path
    is_directory: bool

    @property
    def identity(self) -> str:
        return f"{self.kind}:{self.plugin}/{self.name}"

    @property
    def state_tag(self) -> str:
        return _state_tag(self.identity)


@dataclass(frozen=True)
class Catalog:
    source_root: Path
    components: dict[str, Component]
    plugins: dict[str, tuple[str, ...]]
    dependencies: dict[str, tuple[str, ...]]

    def resolve(
        self,
        selectors: Sequence[str],
        *,
        include_dependencies: bool = True,
    ) -> list[Component]:
        if not selectors:
            raise SelectorError("at least one typed selector is required")

        identities: list[str] = []
        seen: set[str] = set()
        for raw_selector in selectors:
            selector = raw_selector.strip()
            if selector.startswith("plugin:"):
                plugin = selector.removeprefix("plugin:")
                if plugin not in self.plugins:
                    raise SelectorError(f"unknown plugin selector: {selector}")
                for identity in self.plugins[plugin]:
                    if identity not in seen:
                        identities.append(identity)
                        seen.add(identity)
                continue

            match = re.fullmatch(r"(skill|command|rule|agent):([^/]+)/([^/]+)", selector)
            if not match:
                raise SelectorError(
                    f"invalid selector `{selector}`; expected plugin:<slug> or "
                    "skill|command|rule|agent:<plugin>/<name>"
                )
            kind, plugin, name = match.groups()
            identity = f"{kind}:{plugin}/{name}"
            if identity not in self.components:
                raise SelectorError(f"unknown component selector: {selector}")
            if identity not in seen:
                identities.append(identity)
                seen.add(identity)

        resolved = [self.components[identity] for identity in identities]
        return self.expand_dependencies(resolved) if include_dependencies else resolved

    def expand_dependencies(self, components: Sequence[Component]) -> list[Component]:
        """Add declared hard dependencies once, preserving deterministic request order."""

        expanded = list(components)
        seen = {component.identity for component in expanded}
        for component in tuple(expanded):
            for identity in self.dependencies.get(component.identity, ()):
                if identity in seen:
                    continue
                expanded.append(self.components[identity])
                seen.add(identity)
        return expanded


@dataclass(frozen=True)
class MergeDecision:
    value: FileValue | None
    conflict: bool = False
    stage_incoming: bool = False
    note: str = ""


@dataclass
class ComponentPlan:
    component: Component
    target: Path
    local_path: Path | None
    previous_target: Path | None
    incoming: Snapshot
    local: Snapshot
    base: Snapshot
    had_lock_entry: bool
    existing_conflicts: list[dict[str, str]] = field(default_factory=list)
    conflict_records: list[dict[str, str]] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class InstallResult:
    selected: tuple[str, ...]
    actions: tuple[str, ...]
    conflicts: tuple[str, ...]
    dry_run: bool

    @property
    def changed(self) -> bool:
        return any(not action.startswith("plan ") for action in self.actions)


@dataclass(frozen=True)
class ConflictAdoption:
    conflict_id: str
    identity: str
    path: str
    local_state: str
    local_sha256: str | None


@dataclass(frozen=True)
class ConflictAdoptionResult:
    items: tuple[ConflictAdoption, ...]
    dry_run: bool


def _lexists(path: Path) -> bool:
    return os.path.lexists(path)


def _assert_safe_container(agents_root: Path, target: Path) -> None:
    """Reject any project-control parent that could redirect writes elsewhere."""

    if _lexists(agents_root) and (agents_root.is_symlink() or not agents_root.is_dir()):
        raise UnsafePathError(f"project .agents path is not a real directory: {agents_root}")
    try:
        relative = target.relative_to(agents_root)
    except ValueError as exc:
        raise UnsafePathError(f"managed path escapes .agents: {target}") from exc
    current = agents_root
    for part in relative.parts[:-1]:
        current = current / part
        if _lexists(current) and (current.is_symlink() or not current.is_dir()):
            raise UnsafePathError(f"managed parent is not a real directory: {current}")


def _validate_name(value: str, label: str) -> None:
    if not NAME_RE.fullmatch(value):
        raise InstallerError(f"invalid {label} `{value}`; expected lower-case hyphen-case")


def _component_target(kind: str, plugin: str, name: str, suffix: str, collides: bool) -> Path:
    target_name = (
        f"{plugin}{QUALIFIED_TARGET_SEPARATOR}{name}"
        if collides or (kind == "rule" and name == "defaults")
        else name
    )
    if kind != "skill":
        target_name += suffix or ".md"
    return Path(KIND_DIRECTORIES[kind]) / target_name


def _legacy_qualified_component_target(
    kind: str, plugin: str, name: str, suffix: str
) -> Path:
    """Return the pre-safe-separator target accepted for lock migration only."""

    target_name = f"{plugin}-{name}"
    if kind != "skill":
        target_name += suffix or ".md"
    return Path(KIND_DIRECTORIES[kind]) / target_name


def _lock_identity_parts(identity: str) -> tuple[str, str, str]:
    match = re.fullmatch(r"(skill|command|rule|agent):([^/]+)/([^/]+)", identity)
    if not match:
        raise InstallerError(f"invalid component identity in lock: {identity!r}")
    kind, plugin, name = match.groups()
    _validate_name(plugin, "locked plugin name")
    _validate_name(name, "locked component name")
    return kind, plugin, name


def _state_tag(identity: str) -> str:
    readable = re.sub(r"[^a-z0-9-]+", "--", identity.lower()).strip("-")
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    return f"{readable}--{digest}"


def conflict_id(identity: str, displayed_path: str) -> str:
    """Return the stable public identifier for one component conflict."""

    _lock_identity_parts(identity)
    relative = _safe_relative(displayed_path, "conflict path").as_posix()
    digest = hashlib.sha256(f"{identity}\0{relative}".encode("utf-8")).hexdigest()
    return digest[:16]


def _expected_lock_source(identity: str) -> str:
    kind, plugin, name = _lock_identity_parts(identity)
    source = Path(plugin) / KIND_DIRECTORIES[kind]
    return (source / name if kind == "skill" else source / f"{name}.md").as_posix()


def _allowed_lock_targets(identity: str) -> set[str]:
    """Return current/historical flat targets that can belong to one identity."""

    kind, plugin, name = _lock_identity_parts(identity)
    suffix = "" if kind == "skill" else ".md"
    return {
        _component_target(kind, plugin, name, suffix, collides=False).as_posix(),
        _component_target(kind, plugin, name, suffix, collides=True).as_posix(),
        _legacy_qualified_component_target(kind, plugin, name, suffix).as_posix(),
    }


def _assert_real_source_directory(path: Path, label: str) -> bool:
    """Return whether an optional source directory exists, rejecting redirections."""

    if not _lexists(path):
        return False
    if path.is_symlink() or not path.is_dir():
        raise UnsafePathError(f"{label} must be a real directory: {path}")
    return True


def _assert_component_source(component: Component, source_root: Path) -> None:
    """Recheck source ancestors immediately before capture to close symlink races."""

    current = component.source_path
    while current != source_root:
        if current.is_symlink():
            raise UnsafePathError(f"source component ancestor cannot be a symlink: {current}")
        if current.parent == current or not current.is_relative_to(source_root):
            raise UnsafePathError(f"source component escapes source root: {component.source_path}")
        current = current.parent
    if component.is_directory:
        if not component.source_path.is_dir():
            raise UnsafePathError(f"source directory component is missing: {component.source_path}")
    elif not component.source_path.is_file():
        raise UnsafePathError(f"source file component is missing: {component.source_path}")


def _command_owner_dependencies(
    root: Path,
    components: dict[str, Component],
) -> dict[str, tuple[str, ...]]:
    """Load the canonical command-to-owner-skill hard dependency map."""

    registry = root / COMMAND_CAPABILITY_REGISTRY
    if not _lexists(registry):
        return {}
    if registry.parent.is_symlink() or registry.is_symlink() or not registry.is_file():
        raise UnsafePathError(f"command capability registry must be a real file: {registry}")
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallerError(f"invalid command capability registry {registry}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise InstallerError(f"unsupported command capability registry schema in {registry}")
    records = data.get("commands")
    if not isinstance(records, list):
        raise InstallerError(f"command capability registry commands must be an array: {registry}")

    command_by_path = {
        component.source_relative.as_posix(): component.identity
        for component in components.values()
        if component.kind == "command"
    }
    dependencies: dict[str, tuple[str, ...]] = {}
    seen_paths: set[str] = set()
    for index, raw in enumerate(records):
        location = f"{COMMAND_CAPABILITY_REGISTRY.as_posix()}:commands[{index}]"
        if not isinstance(raw, dict):
            raise InstallerError(f"{location}: must be an object")
        command_path = raw.get("path")
        if not isinstance(command_path, str) or not command_path.strip():
            raise InstallerError(f"{location}: command path is required")
        command_path = command_path.strip()
        if command_path in seen_paths:
            raise InstallerError(f"{location}: duplicate command path `{command_path}`")
        seen_paths.add(command_path)
        command_identity = command_by_path.get(command_path)
        if command_identity is None:
            raise InstallerError(f"{location}: unknown command path `{command_path}`")

        owner = raw.get("owner")
        if not isinstance(owner, str) or not owner.strip():
            raise InstallerError(f"{location}: command owner is required")
        owner_parts = owner.strip().split("/")
        if len(owner_parts) != 2 or any(not NAME_RE.fullmatch(part) for part in owner_parts):
            raise InstallerError(f"{location}: invalid command owner `{owner}`")
        dependency = f"skill:{owner_parts[0]}/{owner_parts[1]}"
        if dependency not in components:
            raise InstallerError(
                f"{location}: command owner `{owner.strip()}` does not resolve to a local skill"
            )
        dependencies[command_identity] = (dependency,)

    missing = sorted(set(command_by_path.values()) - set(dependencies))
    if missing:
        raise InstallerError(
            "command capability registry is missing owner entries for: "
            + ", ".join(missing)
        )
    return dependencies


def scan_catalog(source_root: str | Path) -> Catalog:
    """Discover department plugins and compute deterministic flat targets."""

    root = Path(source_root).expanduser().resolve()
    if not root.is_dir():
        raise InstallerError(f"source root is not a directory: {root}")

    raw: list[tuple[str, str, str, Path, Path, bool, str]] = []
    plugins_seen: set[str] = set()
    for plugin_dir in sorted(root.iterdir(), key=lambda path: path.name):
        profile = plugin_dir / "profile.yaml"
        if not plugin_dir.is_dir() or plugin_dir.is_symlink():
            continue
        if profile.is_symlink():
            raise UnsafePathError(f"plugin profile cannot be a symlink: {profile}")
        if not profile.is_file():
            continue
        plugin = plugin_dir.name
        _validate_name(plugin, "plugin name")
        plugins_seen.add(plugin)

        skills_dir = plugin_dir / "skills"
        if _assert_real_source_directory(skills_dir, "source skills category"):
            for skill_dir in sorted(skills_dir.iterdir(), key=lambda path: path.name):
                if skill_dir.is_symlink():
                    raise UnsafePathError(f"source component cannot be a symlink: {skill_dir}")
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file():
                    _validate_name(skill_dir.name, "skill name")
                    raw.append(
                        (
                            "skill",
                            plugin,
                            skill_dir.name,
                            skill_dir,
                            skill_dir.relative_to(root),
                            True,
                            "",
                        )
                    )

        for kind in ("command", "rule", "agent"):
            component_dir = plugin_dir / KIND_DIRECTORIES[kind]
            if not _assert_real_source_directory(
                component_dir, f"source {KIND_DIRECTORIES[kind]} category"
            ):
                continue
            for source_file in sorted(component_dir.iterdir(), key=lambda path: path.name):
                if source_file.name == "README.md" or source_file.suffix.lower() != ".md":
                    continue
                if source_file.is_symlink():
                    raise UnsafePathError(f"source component cannot be a symlink: {source_file}")
                if not source_file.is_file():
                    continue
                _validate_name(source_file.stem, f"{kind} name")
                raw.append(
                    (
                        kind,
                        plugin,
                        source_file.stem,
                        source_file,
                        source_file.relative_to(root),
                        False,
                        source_file.suffix,
                    )
                )

    if not plugins_seen:
        raise InstallerError(f"no department plugins found under {root}")

    identity_counts = Counter((kind, plugin, name) for kind, plugin, name, *_ in raw)
    duplicates = [item for item, count in identity_counts.items() if count > 1]
    if duplicates:
        rendered = ", ".join(f"{kind}:{plugin}/{name}" for kind, plugin, name in sorted(duplicates))
        raise InstallerError(f"duplicate source component identities: {rendered}")

    name_counts = Counter((kind, name) for kind, _plugin, name, *_ in raw)
    components: dict[str, Component] = {}
    target_owners: dict[Path, str] = {}
    plugin_components: dict[str, list[str]] = {plugin: [] for plugin in plugins_seen}
    for kind, plugin, name, source_path, source_relative, is_directory, suffix in raw:
        target_relative = _component_target(kind, plugin, name, suffix, name_counts[(kind, name)] > 1)
        component = Component(
            kind=kind,
            plugin=plugin,
            name=name,
            source_path=source_path,
            source_relative=source_relative,
            target_relative=target_relative,
            is_directory=is_directory,
        )
        if target_relative in target_owners:
            raise InstallerError(
                f"deterministic flat target collision: {target_relative} is claimed by "
                f"{target_owners[target_relative]} and {component.identity}"
            )
        target_owners[target_relative] = component.identity
        components[component.identity] = component
        plugin_components[plugin].append(component.identity)

    kind_order = {kind: index for index, kind in enumerate(KINDS)}
    plugins = {
        plugin: tuple(
            sorted(
                identities,
                key=lambda identity: (
                    kind_order[components[identity].kind],
                    components[identity].name,
                ),
            )
        )
        for plugin, identities in sorted(plugin_components.items())
    }
    dependencies = _command_owner_dependencies(root, components)
    return Catalog(root, components, plugins, dependencies)


def prompt_selectors(
    catalog: Catalog,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> list[str]:
    """Guide a human through whole-plugin or individual-component selection."""

    plugins = sorted(catalog.plugins)
    output_fn("Available plugins:")
    for index, plugin in enumerate(plugins, 1):
        output_fn(f"  {index}. {plugin} ({len(catalog.plugins[plugin])} components)")
    output_fn(
        "Choose plugin numbers or names. You may also paste typed selectors such as "
        "skill:marketing/seo."
    )
    response = input_fn("Plugins or selectors (comma-separated): ").strip()
    if not response:
        raise SelectorError("select at least one plugin or component")

    requested_plugins: list[str] = []
    direct_selectors: list[str] = []
    for raw in (item.strip() for item in response.split(",")):
        if not raw:
            continue
        if raw.lower() == "all":
            requested_plugins.extend(plugins)
            continue
        if raw.isdigit():
            position = int(raw)
            if position < 1 or position > len(plugins):
                raise SelectorError(f"plugin number out of range: {raw}")
            requested_plugins.append(plugins[position - 1])
            continue
        plugin = raw.removeprefix("plugin:")
        if plugin in catalog.plugins:
            requested_plugins.append(plugin)
            continue
        direct_selectors.append(raw)

    selectors = list(direct_selectors)
    for plugin in dict.fromkeys(requested_plugins):
        mode = input_fn(
            f"{plugin}: install [a]ll components or [s]elect individually? [a]: "
        ).strip().lower()
        if mode in {"", "a", "all"}:
            selectors.append(f"plugin:{plugin}")
            continue
        if mode not in {"s", "select"}:
            raise SelectorError(f"invalid selection mode for {plugin}: {mode}")

        identities = catalog.plugins[plugin]
        output_fn(f"Components in {plugin}:")
        for index, identity in enumerate(identities, 1):
            component = catalog.components[identity]
            output_fn(
                f"  {index}. {identity} -> .agents/{component.target_relative.as_posix()}"
            )
        component_response = input_fn(
            f"{plugin} component numbers or typed selectors (comma-separated): "
        ).strip()
        if not component_response:
            raise SelectorError(f"select at least one component from {plugin}")
        for raw in (item.strip() for item in component_response.split(",")):
            if not raw:
                continue
            if raw.lower() == "all":
                selectors.append(f"plugin:{plugin}")
                continue
            if raw.isdigit():
                position = int(raw)
                if position < 1 or position > len(identities):
                    raise SelectorError(
                        f"component number out of range for {plugin}: {raw}"
                    )
                selectors.append(identities[position - 1])
                continue
            if raw not in identities:
                raise SelectorError(
                    f"component selector does not belong to {plugin}: {raw}"
                )
            selectors.append(raw)

    resolved = catalog.resolve(selectors)
    output_fn(f"Selected {len(resolved)} component(s).")
    return selectors


def _capture_entry(path: Path, *, reject_symlinks: bool) -> FileValue:
    metadata = path.lstat()
    mode = stat.S_IMODE(metadata.st_mode)
    if stat.S_ISLNK(metadata.st_mode):
        if reject_symlinks:
            raise UnsafePathError(f"symlinks are not allowed in managed source/base content: {path}")
        return FileValue("symlink", os.readlink(path).encode("utf-8", errors="surrogateescape"), mode)
    if stat.S_ISDIR(metadata.st_mode):
        return FileValue("directory", b"", mode)
    if stat.S_ISREG(metadata.st_mode):
        return FileValue("file", path.read_bytes(), mode)
    raise UnsafePathError(f"unsupported filesystem entry: {path}")


def _ignore_source_path(relative: str, *, is_directory: bool) -> bool:
    path = Path(relative)
    if any(part in SOURCE_IGNORED_DIRECTORIES for part in path.parts):
        return True
    if is_directory:
        return False
    return (
        path.name in SOURCE_IGNORED_FILES
        or path.suffix == ".pyc"
        or _is_personalization_path(relative)
    )


def _capture_directory(root: Path, *, reject_symlinks: bool, source_content: bool = False) -> Snapshot:
    if root.is_symlink():
        if reject_symlinks:
            raise UnsafePathError(f"directory cannot be a symlink: {root}")
        return Snapshot({SINGLE_FILE_KEY: _capture_entry(root, reject_symlinks=False)})
    if not root.is_dir():
        raise UnsafePathError(f"expected directory component: {root}")

    entries: dict[str, FileValue] = {}
    for current_raw, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current = Path(current_raw)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            path = current / name
            relative = path.relative_to(root).as_posix()
            if source_content and _ignore_source_path(relative, is_directory=True):
                continue
            value = _capture_entry(path, reject_symlinks=reject_symlinks)
            entries[relative] = value
            if value.kind == "directory":
                retained_directories.append(name)
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            path = current / name
            relative = path.relative_to(root).as_posix()
            if source_content and _ignore_source_path(relative, is_directory=False):
                continue
            entries[relative] = _capture_entry(path, reject_symlinks=reject_symlinks)
    return Snapshot(entries)


def _capture_component(
    path: Path,
    is_directory: bool,
    *,
    reject_symlinks: bool,
    source_content: bool = False,
) -> Snapshot:
    if not _lexists(path):
        return Snapshot({})
    if is_directory:
        return _capture_directory(
            path,
            reject_symlinks=reject_symlinks,
            source_content=source_content,
        )
    return Snapshot({SINGLE_FILE_KEY: _capture_entry(path, reject_symlinks=reject_symlinks)})


def _resolve_flat_skill(
    catalog: Catalog,
    owner_plugin: str,
    name: str,
    *,
    explicit_plugin: str | None = None,
) -> Component:
    if explicit_plugin is not None:
        identity = f"skill:{explicit_plugin}/{name}"
        selected = catalog.components.get(identity)
        if selected is None or selected.kind != "skill":
            raise InstallerError(
                "portable component reference points to unknown skill "
                f"`{explicit_plugin}/{name}`"
            )
        return selected

    candidates = [
        candidate
        for candidate in catalog.components.values()
        if candidate.kind == "skill" and candidate.name == name
    ]
    same_plugin = [candidate for candidate in candidates if candidate.plugin == owner_plugin]
    if len(same_plugin) == 1:
        selected = same_plugin[0]
    elif len(candidates) == 1:
        selected = candidates[0]
    elif not candidates:
        raise InstallerError(
            f"portable plugin-root reference points to unknown skill `{name}`"
        )
    else:
        owners = ", ".join(sorted(candidate.identity for candidate in candidates))
        raise InstallerError(
            f"portable plugin-root reference to `{name}` is ambiguous: {owners}"
        )
    return selected


def _installed_entry_parent(component: Component, relative: str) -> Path:
    if component.is_directory:
        if relative == SINGLE_FILE_KEY:
            raise InstallerError(
                f"unexpected single-file entry for {component.identity}"
            )
        return (component.target_relative / relative).parent
    if relative != SINGLE_FILE_KEY:
        raise InstallerError(f"unexpected component entry for {component.identity}: {relative}")
    return component.target_relative.parent


def _source_entry_path(component: Component, relative: str) -> Path:
    if component.is_directory:
        if relative == SINGLE_FILE_KEY:
            raise InstallerError(
                f"unexpected single-file source entry for {component.identity}"
            )
        return component.source_path / relative
    if relative != SINGLE_FILE_KEY:
        raise InstallerError(
            f"unexpected source entry for {component.identity}: {relative}"
        )
    return component.source_path


def _canonical_blob_base(source_root: Path) -> str:
    """Read the canonical repository URL from portable source metadata."""

    metadata_path = source_root / "codemeta.json"
    if metadata_path.is_symlink() or not metadata_path.is_file():
        raise InstallerError(
            f"canonical repository metadata is missing or unsafe: {metadata_path}"
        )
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallerError(
            f"invalid canonical repository metadata {metadata_path}: {exc}"
        ) from exc
    repository = metadata.get("codeRepository") if isinstance(metadata, dict) else None
    if not isinstance(repository, str) or not re.fullmatch(
        r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?/?",
        repository,
    ):
        raise InstallerError(
            f"invalid canonical codeRepository in {metadata_path}: {repository!r}"
        )
    return repository.rstrip("/").removesuffix(".git") + "/blob/main"


def _component_installed_target(
    catalog: Catalog, source_target: Path
) -> Path | None:
    candidates: list[tuple[int, Component, Path]] = []
    for candidate in catalog.components.values():
        if candidate.is_directory and source_target.is_relative_to(
            candidate.source_path
        ):
            inner = source_target.relative_to(candidate.source_path)
            candidates.append((len(candidate.source_path.parts), candidate, inner))
        elif not candidate.is_directory and source_target == candidate.source_path:
            candidates.append(
                (len(candidate.source_path.parts), candidate, Path())
            )
    if not candidates:
        return None
    _depth, selected, inner = max(candidates, key=lambda item: item[0])
    return selected.target_relative / inner


def _relative_installed_target(
    component: Component, relative: str, installed_target: Path
) -> str:
    installed_parent = _installed_entry_parent(component, relative)
    return (Path(*([".."] * len(installed_parent.parts))) / installed_target).as_posix()


def _rewrite_markdown_links(
    text: str,
    catalog: Catalog,
    component: Component,
    relative: str,
) -> str:
    source_file = _source_entry_path(component, relative)

    def rewrite_line(line: str) -> str:
        inline_code_spans = [
            (code_match.start(), code_match.end())
            for code_match in INLINE_CODE_RE.finditer(line)
        ]

        def portable_destination(match: re.Match[str]) -> str:
            if any(
                start <= match.start("target") < end
                for start, end in inline_code_spans
            ):
                return match.group(0)
            raw_target = match.group("target")
            if raw_target.startswith(
                ("#", "/", "http://", "https://", "mailto:", "app://")
            ):
                return match.group(0)
            if any(character in raw_target for character in ('"', "'", "{", "}")):
                return match.group(0)
            path_text, separator, fragment = raw_target.partition("#")
            if not path_text:
                return match.group(0)
            source_target = (source_file.parent / unquote(path_text)).resolve()
            if not source_target.exists():
                raise InstallerError(
                    f"portable Markdown link is missing for {component.identity}: "
                    f"{source_file}:{raw_target}"
                )
            try:
                source_relative = source_target.relative_to(catalog.source_root)
            except ValueError as exc:
                raise InstallerError(
                    f"portable Markdown link escapes source root for "
                    f"{component.identity}: {source_file}:{raw_target}"
                ) from exc

            installed_target = _component_installed_target(catalog, source_target)
            if installed_target is None:
                installed_target = SHARED_RUNTIME_TARGETS.get(
                    source_relative.as_posix()
                )
            if installed_target is not None:
                rewritten = _relative_installed_target(
                    component, relative, installed_target
                )
            else:
                rewritten = (
                    f"{_canonical_blob_base(catalog.source_root)}/"
                    f"{quote(source_relative.as_posix(), safe='/')}"
                )
            if separator:
                rewritten = f"{rewritten}#{fragment}"
            start = match.start("target") - match.start()
            end = match.end("target") - match.start()
            return match.group(0)[:start] + rewritten + match.group(0)[end:]

        return MARKDOWN_DESTINATION_RE.sub(portable_destination, line)

    rendered: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            rendered.append(line)
        elif in_fence:
            rendered.append(line)
        else:
            rendered.append(rewrite_line(line))
    return "".join(rendered)


def _rewrite_inline_repo_paths(
    text: str,
    catalog: Catalog,
    component: Component,
    relative: str,
) -> str:
    source_file = _source_entry_path(component, relative)

    def portable_code(match: re.Match[str]) -> str:
        raw = match.group("code")
        if any(character.isspace() for character in raw) or raw.startswith(
            ("/", "http://", "https://", "app://")
        ):
            return match.group(0)
        path_text, separator, fragment = raw.partition("#")
        if not (
            path_text.startswith(("./", "../"))
            or re.match(r"^[a-z0-9][a-z0-9-]*/", path_text)
        ):
            return match.group(0)
        source_target = (source_file.parent / unquote(path_text)).resolve()
        if not source_target.exists():
            return match.group(0)
        try:
            source_target.relative_to(catalog.source_root)
        except ValueError:
            return match.group(0)
        installed_target = _component_installed_target(catalog, source_target)
        if installed_target is None:
            return match.group(0)
        rewritten = f".agents/{installed_target.as_posix()}"
        if separator:
            rewritten = f"{rewritten}#{fragment}"
        return f"`{rewritten}`"

    return INLINE_CODE_RE.sub(portable_code, text)


def _rewrite_shared_source_paths(
    text: str,
    catalog: Catalog,
    component: Component,
    relative: str,
) -> str:
    source_file = _source_entry_path(component, relative)
    rendered = text
    for source_relative, installed_target in SHARED_RUNTIME_TARGETS.items():
        source_path = catalog.source_root / source_relative
        source_reference = os.path.relpath(
            source_path, start=source_file.parent
        ).replace(os.sep, "/")
        installed_reference = _relative_installed_target(
            component, relative, installed_target
        )
        rendered = rendered.replace(source_reference, installed_reference)
    return rendered


def _markdown_destination_spans(text: str) -> list[tuple[int, int]]:
    return [
        (match.start("target"), match.end("target"))
        for match in MARKDOWN_DESTINATION_RE.finditer(text)
    ]


def _rewrite_component_skill_paths(
    text: str,
    catalog: Catalog,
    component: Component,
    relative: str,
) -> str:
    destination_spans = _markdown_destination_spans(text)

    def portable_path(match: re.Match[str]) -> str:
        if any(
            start <= match.start() < end for start, end in destination_spans
        ):
            # Markdown destinations were resolved by _rewrite_markdown_links.
            # In particular, a collision-safe target such as
            # `../skills/engineering__craft` must not be reinterpreted as the
            # valid-looking `../skills/engineering` source-path prefix.
            return match.group(0)
        explicit_plugin = match.group("qualified_plugin")
        name = (
            match.group("claude_name")
            or match.group("qualified_name")
            or match.group("parent_name")
            or match.group("bare_name")
        )
        selected = _resolve_flat_skill(
            catalog,
            component.plugin,
            name,
            explicit_plugin=explicit_plugin,
        )
        return f".agents/{selected.target_relative.as_posix()}"

    return PORTABLE_COMPONENT_SKILL_PATH_RE.sub(portable_path, text)


def _project_portable_snapshot(
    catalog: Catalog, component: Component, snapshot: Snapshot
) -> Snapshot:
    """Rewrite native source references only in the project-runtime snapshot."""

    entries = dict(snapshot.entries)
    changed = False
    for relative, value in snapshot.entries.items():
        if value.kind != "file":
            continue
        installable_markdown = (
            relative == SINGLE_FILE_KEY or Path(relative).suffix.lower() == ".md"
        )
        if not installable_markdown:
            continue
        try:
            text = value.data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise InstallerError(
                f"portable text reference is not UTF-8 in {component.identity}: {relative}"
            ) from exc
        rendered = _rewrite_markdown_links(
            text, catalog, component, relative
        )
        rendered = _rewrite_shared_source_paths(
            rendered, catalog, component, relative
        )
        rendered = _rewrite_inline_repo_paths(
            rendered, catalog, component, relative
        )
        rendered = SOURCE_EXTERNAL_INSTALLER_RE.sub(
            PROJECT_EXTERNAL_INSTALLER, rendered
        )

        def project_agent(match: re.Match[str]) -> str:
            return match.group(0).replace("--agent codex", "--agent project")

        rendered = PROJECT_EXTERNAL_INSTALL_RE.sub(project_agent, rendered)
        rendered = _rewrite_component_skill_paths(
            rendered, catalog, component, relative
        )
        if rendered == text:
            continue
        entries[relative] = FileValue(
            value.kind,
            rendered.encode("utf-8"),
            value.mode,
        )
        changed = True
    return Snapshot(entries) if changed else snapshot


def _safe_relative(value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise InstallerError(f"unsafe {label} in lock: {value!r}")
    return path


def _empty_lock() -> dict[str, object]:
    return {"schema_version": LOCK_VERSION, "components": {}}


def load_lock(project_root: str | Path) -> dict[str, object]:
    project = Path(project_root).expanduser().resolve()
    agents_root = project / ".agents"
    _assert_safe_container(agents_root, agents_root / LOCK_NAME)
    lock_path = agents_root / LOCK_NAME
    if not lock_path.exists():
        return _empty_lock()
    try:
        data = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallerError(f"invalid plugin lock {lock_path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != LOCK_VERSION:
        raise InstallerError(f"unsupported plugin lock schema in {lock_path}")
    components = data.get("components")
    if not isinstance(components, dict):
        raise InstallerError(f"plugin lock components must be an object: {lock_path}")

    owners: dict[str, str] = {}
    for identity, raw_entry in components.items():
        if not isinstance(identity, str) or not isinstance(raw_entry, dict):
            raise InstallerError(f"invalid component entry in {lock_path}")
        kind, plugin, name = _lock_identity_parts(identity)
        for field_name, expected in (("kind", kind), ("plugin", plugin), ("name", name)):
            if raw_entry.get(field_name) != expected:
                raise OwnershipConflictError(
                    f"lock metadata mismatch for {identity}: {field_name} is "
                    f"{raw_entry.get(field_name)!r}, expected {expected!r}"
                )
        target = raw_entry.get("target")
        snapshot = raw_entry.get("base_snapshot")
        if not isinstance(target, str) or not isinstance(snapshot, str):
            raise InstallerError(f"incomplete lock entry for {identity}")
        files = raw_entry.get("files")
        if not isinstance(files, dict):
            raise InstallerError(f"lock files must be an object for {identity}")
        for displayed_path, digest in files.items():
            if not isinstance(displayed_path, str) or not isinstance(digest, str):
                raise InstallerError(f"invalid lock file record for {identity}")
            _safe_relative(displayed_path, "locked component file")
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise InstallerError(
                    f"invalid lock file digest for {identity}: {displayed_path}"
                )
        source_repository = raw_entry.get("source_repository")
        if not isinstance(source_repository, str) or not source_repository:
            raise InstallerError(f"lock source repository is missing for {identity}")
        expected_source = _expected_lock_source(identity)
        if raw_entry.get("source") != expected_source:
            raise OwnershipConflictError(
                f"lock source mismatch for {identity}: {raw_entry.get('source')!r} "
                f"does not equal {expected_source!r}"
            )
        _safe_relative(target, "component target")
        _safe_relative(snapshot, "base snapshot")
        allowed_targets = _allowed_lock_targets(identity)
        if target not in allowed_targets:
            raise OwnershipConflictError(
                f"lock target mismatch for {identity}: {target!r} is not one of "
                f"{', '.join(sorted(allowed_targets))}"
            )
        expected_snapshot = (
            Path(STATE_DIRECTORY) / "bases" / _state_tag(identity)
        ).as_posix()
        if snapshot != expected_snapshot:
            raise OwnershipConflictError(
                f"lock base snapshot mismatch for {identity}: {snapshot!r} "
                f"does not equal {expected_snapshot!r}"
            )
        conflicts = raw_entry.get("conflicts", [])
        if not isinstance(conflicts, list):
            raise InstallerError(f"lock conflicts must be a list for {identity}")
        seen_conflict_paths: set[str] = set()
        seen_conflict_ids: set[str] = set()
        for conflict in conflicts:
            if not isinstance(conflict, dict):
                raise InstallerError(f"invalid lock conflict for {identity}")
            for field_name in ("path", "staged", "reason", "incoming_sha256"):
                if not isinstance(conflict.get(field_name), str):
                    raise InstallerError(f"lock conflict for {identity} is missing {field_name}")
            if not re.fullmatch(r"[0-9a-f]{64}", str(conflict["incoming_sha256"])):
                raise InstallerError(
                    f"lock conflict for {identity} has an invalid incoming_sha256"
                )
            _safe_relative(str(conflict["path"]), "conflict path")
            _safe_relative(str(conflict["staged"]), "staged conflict path")
            expected_conflict_id = conflict_id(identity, str(conflict["path"]))
            if str(conflict["path"]) in seen_conflict_paths:
                raise InstallerError(
                    f"lock conflict path is duplicated for {identity}: {conflict['path']}"
                )
            if expected_conflict_id in seen_conflict_ids:
                raise InstallerError(
                    f"lock conflict id is duplicated for {identity}: {expected_conflict_id}"
                )
            seen_conflict_paths.add(str(conflict["path"]))
            seen_conflict_ids.add(expected_conflict_id)
            recorded_conflict_id = conflict.get("id")
            if recorded_conflict_id is not None and recorded_conflict_id != expected_conflict_id:
                raise InstallerError(
                    f"lock conflict for {identity} has an invalid id"
                )
            base_state = conflict.get("base_state")
            base_sha256 = conflict.get("base_sha256")
            base_path = conflict.get("base")
            if base_state is not None:
                if base_state not in {"present", "missing"}:
                    raise InstallerError(
                        f"lock conflict for {identity} has an invalid base_state"
                    )
                if base_state == "present":
                    if not isinstance(base_sha256, str) or not re.fullmatch(
                        r"[0-9a-f]{64}", base_sha256
                    ):
                        raise InstallerError(
                            f"lock conflict for {identity} has an invalid base_sha256"
                        )
                    expected_base = (
                        Path(CONFLICT_BASE_DIRECTORY)
                        / _state_tag(identity)
                        / expected_conflict_id
                        / "content"
                    ).as_posix()
                    if base_path != expected_base:
                        raise InstallerError(
                            f"lock conflict for {identity} has an invalid base path"
                        )
                    _safe_relative(str(base_path), "conflict base path")
                elif base_sha256 is not None or base_path is not None:
                    raise InstallerError(
                        f"lock conflict for {identity} cannot hash a missing base"
                    )
            elif base_sha256 is not None or base_path is not None:
                raise InstallerError(
                    f"lock conflict for {identity} has base metadata without base_state"
                )
        if target in owners and owners[target] != identity:
            raise OwnershipConflictError(
                f"lock ownership conflict for {target}: {owners[target]} and {identity}"
            )
        owners[target] = identity
    return data


def _repository_identity(source_root: Path) -> str:
    config = source_root / ".git" / "config"
    if config.is_file():
        try:
            text = config.read_text(encoding="utf-8")
            match = re.search(r'\[remote "origin"\][^\[]*?\n\s*url\s*=\s*(\S+)', text, re.MULTILINE)
            if match:
                remote = match.group(1).removesuffix(".git")
                remote = re.sub(r"^git@[^:]+:", "", remote)
                remote = re.sub(r"^https?://[^/]+/", "", remote)
                return remote.strip("/")
        except OSError:
            pass
    return source_root.name


def _snapshot_path(agents_root: Path, component: Component) -> Path:
    return agents_root / STATE_DIRECTORY / "bases" / component.state_tag


def _updates_path(agents_root: Path, component: Component) -> Path:
    return agents_root / UPDATE_DIRECTORY / component.state_tag


def _conflict_bases_path(agents_root: Path, component: Component) -> Path:
    return agents_root / CONFLICT_BASE_DIRECTORY / component.state_tag


def _preflight(
    catalog: Catalog,
    project_root: Path,
    components: Sequence[Component],
    lock: dict[str, object],
) -> list[ComponentPlan]:
    agents_root = project_root / ".agents"
    source_repository = _repository_identity(catalog.source_root)
    lock_components = lock["components"]
    assert isinstance(lock_components, dict)

    target_owners: dict[str, str] = {}
    for identity, raw_entry in lock_components.items():
        assert isinstance(raw_entry, dict)
        target = str(raw_entry["target"])
        target_owners[target] = str(identity)

    vacating_target_owners: dict[str, str] = {}
    for component in components:
        raw_entry = lock_components.get(component.identity)
        if not isinstance(raw_entry, dict):
            continue
        recorded_target = str(raw_entry.get("target", ""))
        if recorded_target != component.target_relative.as_posix():
            vacating_target_owners[recorded_target] = component.identity

    requested_targets: dict[str, str] = {}
    plans: list[ComponentPlan] = []
    for component in components:
        target_text = component.target_relative.as_posix()
        if target_text in requested_targets and requested_targets[target_text] != component.identity:
            raise OwnershipConflictError(
                f"install plan target conflict for {target_text}: "
                f"{requested_targets[target_text]} and {component.identity}"
            )
        requested_targets[target_text] = component.identity

        owner = target_owners.get(target_text)
        if (
            owner is not None
            and owner != component.identity
            and vacating_target_owners.get(target_text) != owner
        ):
            raise OwnershipConflictError(
                f"managed target {target_text} is owned by {owner}, not {component.identity}"
            )

        target = agents_root / component.target_relative
        _assert_safe_container(agents_root, target)
        _assert_safe_container(agents_root, _snapshot_path(agents_root, component))
        _assert_safe_container(agents_root, _updates_path(agents_root, component))
        _assert_safe_container(
            agents_root, _conflict_bases_path(agents_root, component)
        )
        local_path = target
        previous_target: Path | None = None
        existing_conflicts: list[dict[str, str]] = []
        raw_lock_entry = lock_components.get(component.identity)
        if raw_lock_entry is None:
            if _lexists(target):
                displaced_owner = target_owners.get(target_text)
                if displaced_owner is None:
                    raise UnmanagedTargetError(
                        f"refusing to overwrite unmanaged target {target}; "
                        "adopt or move it explicitly"
                    )
                if vacating_target_owners.get(target_text) != displaced_owner:
                    raise OwnershipConflictError(
                        f"managed target {target_text} is owned by "
                        f"{displaced_owner}, not {component.identity}"
                    )
                # The old owner is captured by its own migration plan. Treat
                # this target as empty for the incoming component so their
                # contents are never merged together.
                local_path = None
            base = Snapshot({})
            had_lock_entry = False
        else:
            if not isinstance(raw_lock_entry, dict):
                raise InstallerError(f"invalid lock entry for {component.identity}")
            recorded_repository = raw_lock_entry.get("source_repository")
            if not isinstance(recorded_repository, str) or recorded_repository != source_repository:
                raise OwnershipConflictError(
                    f"source ownership changed for {component.identity}: lock has "
                    f"{recorded_repository!r}, current source is {source_repository!r}"
                )
            recorded_source = raw_lock_entry.get("source")
            expected_source = component.source_relative.as_posix()
            if recorded_source != expected_source:
                raise OwnershipConflictError(
                    f"source path changed for {component.identity}: lock has "
                    f"{recorded_source!r}, expected {expected_source!r}"
                )
            recorded_target = str(raw_lock_entry.get("target", ""))
            if recorded_target != target_text:
                recorded_relative = _safe_relative(recorded_target, "component target")
                previous_target = agents_root / recorded_relative
                _assert_safe_container(agents_root, previous_target)
                local_path = previous_target
                if _lexists(target):
                    new_owner = target_owners.get(target_text)
                    if new_owner is None:
                        raise UnmanagedTargetError(
                            f"cannot migrate {component.identity} to unmanaged target {target}"
                        )
                    if (
                        new_owner != component.identity
                        and vacating_target_owners.get(target_text) != new_owner
                    ):
                        raise OwnershipConflictError(
                            f"cannot migrate {component.identity}; {target_text} is owned by {new_owner}"
                        )
            base_relative = _safe_relative(str(raw_lock_entry["base_snapshot"]), "base snapshot")
            expected_base = Path(STATE_DIRECTORY) / "bases" / component.state_tag
            if base_relative != expected_base:
                raise OwnershipConflictError(
                    f"base snapshot mapping changed for {component.identity}: lock has "
                    f"{base_relative}, expected {expected_base}"
                )
            base_path = agents_root / base_relative
            if not base_path.is_dir() or base_path.is_symlink():
                raise InstallerError(f"saved base is missing or unsafe for {component.identity}: {base_path}")
            base = _capture_component(base_path, True, reject_symlinks=True)
            if not component.is_directory:
                base = Snapshot(
                    {SINGLE_FILE_KEY: base.entries[SINGLE_FILE_KEY]}
                    if SINGLE_FILE_KEY in base.entries
                    else {}
                )
            recorded_files = raw_lock_entry.get("files")
            assert isinstance(recorded_files, dict)
            actual_base_files = {
                (
                    relative
                    if component.is_directory
                    else Path(recorded_target).name
                ): value.digest
                for relative, value in sorted(base.entries.items())
            }
            if actual_base_files != recorded_files:
                raise OwnershipConflictError(
                    f"saved upstream base was modified for {component.identity}; "
                    "preserve it and restore the lock-owned snapshot"
                )
            had_lock_entry = True
            raw_conflicts = raw_lock_entry.get("conflicts", [])
            assert isinstance(raw_conflicts, list)
            existing_conflicts = [
                {str(key): str(value) for key, value in conflict.items()}
                for conflict in raw_conflicts
                if isinstance(conflict, dict)
            ]

        _assert_component_source(component, catalog.source_root)
        incoming = _capture_component(
            component.source_path,
            component.is_directory,
            reject_symlinks=True,
            source_content=True,
        )
        incoming = _project_portable_snapshot(catalog, component, incoming)
        local = (
            Snapshot({})
            if local_path is None
            else _capture_component(
                local_path,
                component.is_directory,
                reject_symlinks=False,
            )
        )
        plans.append(
            ComponentPlan(
                component=component,
                target=target,
                local_path=local_path,
                previous_target=previous_target,
                incoming=incoming,
                local=local,
                base=base,
                had_lock_entry=had_lock_entry,
                existing_conflicts=existing_conflicts,
            )
        )
        if previous_target is not None:
            plans[-1].actions.append(
                f"{component.identity}: migrate .agents/{recorded_target} -> "
                f".agents/{target_text}"
            )

    return plans


def _is_personalization_path(relative: str) -> bool:
    if relative == SINGLE_FILE_KEY:
        return False
    path = Path(relative)
    lowered_parts = [part.lower() for part in path.parts]
    name = path.name.lower()
    return (
        name == "personalize.local.yml"
        or ".local." in name
        or any(part in {".overlays", ".company", ".user", ".generated"} for part in lowered_parts)
    )


@dataclass(frozen=True)
class _Edit:
    start: int
    end: int
    replacement: tuple[str, ...]
    side: str


def _line_edits(base: list[str], variant: list[str], side: str) -> list[_Edit]:
    matcher = difflib.SequenceMatcher(a=base, b=variant, autojunk=False)
    return [
        _Edit(i1, i2, tuple(variant[j1:j2]), side)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    ]


def _edits_conflict(left: _Edit, right: _Edit) -> bool:
    if left.start == right.start and left.end == right.end and left.replacement == right.replacement:
        return False
    left_insert = left.start == left.end
    right_insert = right.start == right.end
    if left_insert and right_insert:
        return left.start == right.start
    if left_insert:
        return right.start < left.start < right.end
    if right_insert:
        return left.start < right.start < left.end
    return max(left.start, right.start) < min(left.end, right.end)


def _three_way_text(base: bytes, local: bytes, incoming: bytes) -> bytes | None:
    try:
        base_text = base.decode("utf-8")
        local_text = local.decode("utf-8")
        incoming_text = incoming.decode("utf-8")
    except UnicodeDecodeError:
        return None

    base_lines = base_text.splitlines(keepends=True)
    local_edits = _line_edits(base_lines, local_text.splitlines(keepends=True), "local")
    incoming_edits = _line_edits(base_lines, incoming_text.splitlines(keepends=True), "incoming")
    for local_edit in local_edits:
        for incoming_edit in incoming_edits:
            if _edits_conflict(local_edit, incoming_edit):
                return None

    edits: list[_Edit] = []
    seen: set[tuple[int, int, tuple[str, ...]]] = set()
    for edit in local_edits + incoming_edits:
        key = (edit.start, edit.end, edit.replacement)
        if key not in seen:
            edits.append(edit)
            seen.add(key)
    edits.sort(key=lambda edit: (edit.start, edit.end, 0 if edit.side == "local" else 1), reverse=True)
    merged = list(base_lines)
    for edit in edits:
        merged[edit.start : edit.end] = list(edit.replacement)
    return "".join(merged).encode("utf-8")


def _merge_value(
    relative: str,
    base: FileValue | None,
    local: FileValue | None,
    incoming: FileValue | None,
) -> MergeDecision:
    personalized = _is_personalization_path(relative)

    if base is None:
        if incoming is None:
            return MergeDecision(local)
        if local is None:
            return MergeDecision(incoming, note="added upstream")
        if local == incoming:
            return MergeDecision(local)
        return MergeDecision(
            local,
            conflict=True,
            stage_incoming=True,
            note="local addition conflicts with new upstream path",
        )

    if incoming is None:
        if local is None:
            return MergeDecision(None)
        if personalized:
            return MergeDecision(local, note="preserved personalization after upstream deletion")
        if local == base:
            return MergeDecision(None, note="removed unchanged upstream path")
        return MergeDecision(local, note="preserved locally changed upstream deletion")

    if local is None:
        if incoming == base:
            return MergeDecision(None, note="preserved local deletion")
        return MergeDecision(
            None,
            conflict=True,
            stage_incoming=True,
            note="local deletion conflicts with upstream change",
        )

    if local == incoming:
        return MergeDecision(local)
    if local == base:
        return MergeDecision(incoming, note="updated from upstream")
    if incoming == base:
        return MergeDecision(local, note="preserved local change")
    if personalized:
        return MergeDecision(
            local,
            conflict=True,
            stage_incoming=True,
            note="preserved personalized path",
        )

    if base.kind == local.kind == incoming.kind == "file":
        merged = _three_way_text(base.data, local.data, incoming.data)
        if merged is not None:
            return MergeDecision(
                FileValue("file", merged, local.mode),
                note="merged disjoint local and upstream changes",
            )

    return MergeDecision(
        local,
        conflict=True,
        stage_incoming=True,
        note="overlapping or non-text local/upstream changes",
    )


def _is_descendant(relative: str, ancestor: str) -> bool:
    if relative == SINGLE_FILE_KEY or ancestor == SINGLE_FILE_KEY:
        return False
    relative_parts = Path(relative).parts
    ancestor_parts = Path(ancestor).parts
    return (
        len(relative_parts) > len(ancestor_parts)
        and relative_parts[: len(ancestor_parts)] == ancestor_parts
    )


def _snapshot_digest(snapshot: Snapshot, relative: str) -> str | None:
    """Hash one entry, including its complete subtree when it is a directory."""

    value = snapshot.entries.get(relative)
    if value is None:
        return None
    if value.kind != "directory":
        return value.digest
    digest = hashlib.sha256()
    digest.update(b"directory-subtree\0")
    for child in sorted(
        key
        for key in snapshot.entries
        if key == relative or _is_descendant(key, relative)
    ):
        digest.update(child.encode("utf-8"))
        digest.update(b"\0")
        digest.update(snapshot.entries[child].digest.encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def _staged_artifact_digest(root: Path, displayed_path: str) -> str | None:
    """Hash a staged incoming artifact using the lock's subtree digest format."""

    if not _lexists(root):
        return None
    if root.is_symlink() or not root.is_dir():
        raise UnsafePathError(f"staged update root is unsafe: {root}")
    relative = _safe_relative(displayed_path, "staged conflict path")
    path = root / relative
    _assert_safe_parents(root, path, root_is_file=False)
    if not _lexists(path):
        return None
    root_value = _capture_entry(path, reject_symlinks=True)
    if root_value.kind != "directory":
        return root_value.digest
    captured = _capture_directory(path, reject_symlinks=True)
    entries = {displayed_path: root_value}
    for relative, value in captured.entries.items():
        entries[(Path(displayed_path) / relative).as_posix()] = value
    return _snapshot_digest(Snapshot(entries), displayed_path)


def _merge_decisions(plan: ComponentPlan) -> dict[str, MergeDecision]:
    """Plan entry merges while treating file/directory transitions as subtrees."""

    all_keys = set(plan.base.entries) | set(plan.local.entries) | set(plan.incoming.entries)
    decisions = {
        relative: _merge_value(
            relative,
            plan.base.entries.get(relative),
            plan.local.entries.get(relative),
            plan.incoming.entries.get(relative),
        )
        for relative in all_keys
    }

    transition_roots: list[str] = []
    for relative in sorted(
        all_keys,
        key=lambda item: (0 if item == SINGLE_FILE_KEY else len(Path(item).parts), item),
    ):
        if any(_is_descendant(relative, root) for root in transition_roots):
            continue
        incoming = plan.incoming.entries.get(relative)
        local = plan.local.entries.get(relative)
        decision = decisions[relative]
        transition_conflict = False

        if incoming is not None and incoming.kind == "directory":
            if local is not None and local.kind != "directory" and decision.value != incoming:
                transition_conflict = True
            elif (
                local is None
                and decision.value != incoming
                and _snapshot_digest(plan.base, relative)
                != _snapshot_digest(plan.incoming, relative)
            ):
                transition_conflict = True
        elif incoming is not None and incoming.kind != "directory":
            if local is not None and local.kind == "directory":
                preserved_descendant = any(
                    _is_descendant(child, relative) and child_decision.value is not None
                    for child, child_decision in decisions.items()
                )
                transition_conflict = decision.value != incoming or preserved_descendant

        if transition_conflict:
            decisions[relative] = MergeDecision(
                local,
                conflict=True,
                stage_incoming=True,
                note="local subtree conflicts with upstream path type change",
            )
            transition_roots.append(relative)

    for root in transition_roots:
        for relative in all_keys:
            if not _is_descendant(relative, root):
                continue
            decisions[relative] = MergeDecision(
                plan.local.entries.get(relative),
                stage_incoming=plan.incoming.entries.get(relative) is not None,
            )
    return decisions


def _stage_relative(component: Component, relative: str) -> str:
    if relative != SINGLE_FILE_KEY:
        return relative
    return component.target_relative.name


def _internal_conflict_relative(component: Component, displayed_path: str) -> str:
    display_relative = _safe_relative(displayed_path, "conflict path")
    if component.is_directory:
        return display_relative.as_posix()
    if display_relative.as_posix() == component.target_relative.name:
        return SINGLE_FILE_KEY
    raise InstallerError(
        f"invalid file-component conflict path for {component.identity}: {displayed_path}"
    )


def _validate_existing_conflict_artifacts(
    plan: ComponentPlan, existing_updates: Path
) -> None:
    """Fail closed before a refresh could overwrite a user-edited staged artifact."""

    component = plan.component
    for conflict in plan.existing_conflicts:
        displayed_path = conflict.get("path", "")
        display_relative = _safe_relative(displayed_path, "conflict path")
        expected_staged = Path(UPDATE_DIRECTORY) / component.state_tag / display_relative
        staged_relative = _safe_relative(
            conflict.get("staged", ""), "staged conflict path"
        )
        if staged_relative != expected_staged:
            raise OwnershipConflictError(
                f"staged conflict mapping changed for {component.identity}: "
                f"lock has {staged_relative}, expected {expected_staged}"
            )
        staged_digest = _staged_artifact_digest(
            existing_updates, displayed_path
        )
        if staged_digest is None:
            raise OwnershipConflictError(
                f"staged update is missing for {component.identity}: {displayed_path}"
            )
        if (
            staged_digest != conflict.get("incoming_sha256")
        ):
            raise OwnershipConflictError(
                f"staged update was locally modified for {component.identity}: "
                f"{displayed_path}; preserve it and resolve the conflict explicitly"
            )
        base_state = conflict.get("base_state")
        if base_state is not None:
            agents_root = existing_updates.parent.parent
            base_relative = conflict.get("base")
            base_digest = None
            if isinstance(base_relative, str):
                base_path = agents_root / _safe_relative(
                    base_relative, "conflict base path"
                )
                base_digest = _staged_artifact_digest(
                    base_path.parent, base_path.name
                )
            if base_state == "present" and base_digest != conflict.get("base_sha256"):
                raise OwnershipConflictError(
                    f"saved conflict base was modified for {component.identity}: "
                    f"{displayed_path}"
                )
            if base_state == "missing" and base_digest is not None:
                raise OwnershipConflictError(
                    f"saved conflict base unexpectedly exists for {component.identity}: "
                    f"{displayed_path}"
                )


def _path_for_entry(root: Path, relative: str, *, single_file: bool) -> Path:
    if single_file:
        if relative != SINGLE_FILE_KEY:
            raise InstallerError(f"unexpected file-component entry: {relative}")
        return root
    path = Path(relative)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise UnsafePathError(f"unsafe component-relative path: {relative}")
    return root / path


def _assert_safe_parents(root: Path, target: Path, *, root_is_file: bool) -> None:
    boundary = root.parent if root_is_file else root
    current = target.parent
    parents: list[Path] = []
    while current != boundary:
        if current.parent == current or not current.is_relative_to(boundary):
            raise UnsafePathError(f"path escapes staging root: {target}")
        parents.append(current)
        current = current.parent
    for parent in reversed(parents):
        if _lexists(parent) and parent.is_symlink():
            raise UnsafePathError(f"refusing to traverse local symlink while merging: {parent}")


def _remove_any(path: Path) -> None:
    if not _lexists(path):
        return
    if path.is_symlink() or not path.is_dir():
        path.unlink()
    else:
        shutil.rmtree(path)


def _remove_merged_entry(path: Path) -> None:
    """Remove one merged entry without deleting preserved descendants."""

    if not _lexists(path):
        return
    if path.is_symlink() or not path.is_dir():
        path.unlink()
        return
    try:
        path.rmdir()
    except OSError:
        # The directory contains a local addition or another preserved child.
        # Leaving it in place is the conservative no-loss outcome.
        return


def _write_value(root: Path, relative: str, value: FileValue | None, *, single_file: bool) -> None:
    target = _path_for_entry(root, relative, single_file=single_file)
    _assert_safe_parents(root, target, root_is_file=single_file)
    if value is None:
        _remove_merged_entry(target)
        return

    if value.kind == "directory":
        if _lexists(target) and (target.is_symlink() or not target.is_dir()):
            _remove_any(target)
        target.mkdir(parents=True, exist_ok=True)
        target.chmod(value.mode)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    if _lexists(target):
        _remove_any(target)
    if value.kind == "file":
        target.write_bytes(value.data)
        target.chmod(value.mode)
        return
    if value.kind == "symlink":
        os.symlink(value.data.decode("utf-8", errors="surrogateescape"), target)
        return
    raise UnsafePathError(f"unsupported staged entry kind: {value.kind}")


def _write_snapshot_artifact(
    snapshot: Snapshot,
    relative: str,
    destination: Path,
) -> bool:
    """Materialize one snapshot entry and its subtree at a stable artifact path."""

    value = snapshot.entries.get(relative)
    if value is None:
        return False
    _write_value(destination, SINGLE_FILE_KEY, value, single_file=True)
    if value.kind != "directory":
        return True
    for child in sorted(
        (
            key
            for key in snapshot.entries
            if _is_descendant(key, relative)
        ),
        key=lambda item: _entry_order(item, snapshot.entries[item]),
    ):
        child_relative = Path(child).relative_to(relative).as_posix()
        _write_value(
            destination,
            child_relative,
            snapshot.entries[child],
            single_file=False,
        )
    return True


def _copy_existing(source: Path, destination: Path, *, is_directory: bool) -> None:
    if not _lexists(source):
        return
    if is_directory:
        if source.is_symlink() or not source.is_dir():
            raise UnsafePathError(f"managed directory target is not a real directory: {source}")
        shutil.copytree(source, destination, symlinks=True)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        os.symlink(os.readlink(source), destination)
    else:
        shutil.copy2(source, destination)


def _entry_order(relative: str, incoming: FileValue | None) -> tuple[int, int, str]:
    depth = 0 if relative == SINGLE_FILE_KEY else len(Path(relative).parts)
    if incoming is None:
        return (0, -depth, relative)
    return (1, depth, relative)


def _prepare_component(
    plan: ComponentPlan,
    stage_target: Path,
    stage_base: Path,
    stage_updates: Path,
    existing_updates: Path,
    stage_conflict_bases: Path,
    existing_conflict_bases: Path,
) -> tuple[bool, bool]:
    component = plan.component
    _validate_existing_conflict_artifacts(plan, existing_updates)
    if plan.local_path is not None:
        _copy_existing(plan.local_path, stage_target, is_directory=component.is_directory)

    decisions = _merge_decisions(plan)

    ordered = sorted(
        decisions,
        key=lambda relative: _entry_order(relative, plan.incoming.entries.get(relative)),
    )
    if _lexists(existing_updates):
        if existing_updates.is_symlink() or not existing_updates.is_dir():
            raise UnsafePathError(f"staged update root is unsafe: {existing_updates}")
        _capture_directory(existing_updates, reject_symlinks=True)
        shutil.copytree(existing_updates, stage_updates, symlinks=True)
        has_staged_updates = True
    else:
        has_staged_updates = False
    if _lexists(existing_conflict_bases):
        if existing_conflict_bases.is_symlink() or not existing_conflict_bases.is_dir():
            raise UnsafePathError(
                f"saved conflict base root is unsafe: {existing_conflict_bases}"
            )
        _capture_directory(existing_conflict_bases, reject_symlinks=True)
        shutil.copytree(
            existing_conflict_bases,
            stage_conflict_bases,
            symlinks=True,
        )
        has_conflict_bases = True
    else:
        has_conflict_bases = False
    new_conflict_paths: set[str] = set()
    for relative in ordered:
        decision = decisions[relative]
        local = plan.local.entries.get(relative)
        if decision.value != local:
            _write_value(
                stage_target,
                relative,
                decision.value,
                single_file=not component.is_directory,
            )
            if decision.note:
                plan.actions.append(f"{component.identity}: {_stage_relative(component, relative)}: {decision.note}")
        elif decision.note and decision.note not in {"preserved local change", "preserved local deletion"}:
            plan.actions.append(f"{component.identity}: {_stage_relative(component, relative)}: {decision.note}")

        if decision.conflict:
            displayed_path = _stage_relative(component, relative)
            rendered = f"{component.identity}: {displayed_path}: {decision.note}"
            plan.conflicts.append(rendered)
            new_conflict_paths.add(displayed_path)
        incoming = plan.incoming.entries.get(relative)
        if decision.stage_incoming and incoming is not None:
            if not has_staged_updates:
                stage_updates.mkdir(parents=True, exist_ok=True)
                has_staged_updates = True
            update_relative = _stage_relative(component, relative)
            _write_value(stage_updates, update_relative, incoming, single_file=False)
            if decision.conflict:
                incoming_digest = _snapshot_digest(plan.incoming, relative)
                assert incoming_digest is not None
                existing_record = next(
                    (
                        existing
                        for existing in plan.existing_conflicts
                        if existing.get("path") == update_relative
                    ),
                    None,
                )
                record = {
                    "id": conflict_id(component.identity, update_relative),
                    "path": update_relative,
                    "staged": (
                        Path(UPDATE_DIRECTORY) / component.state_tag / update_relative
                    ).as_posix(),
                    "reason": decision.note,
                    "incoming_sha256": incoming_digest,
                }
                if existing_record is not None and "base_state" in existing_record:
                    record["base_state"] = existing_record["base_state"]
                    if "base_sha256" in existing_record:
                        record["base_sha256"] = existing_record["base_sha256"]
                    if "base" in existing_record:
                        record["base"] = existing_record["base"]
                elif existing_record is None:
                    record["base_state"] = (
                        "present"
                        if plan.base.entries.get(relative) is not None
                        else "missing"
                    )
                    if record["base_state"] == "present":
                        base_id = str(record["id"])
                        artifact_root = stage_conflict_bases / base_id
                        artifact_path = artifact_root / "content"
                        _remove_any(artifact_root)
                        if not _write_snapshot_artifact(
                            plan.base,
                            relative,
                            artifact_path,
                        ):
                            raise InstallerError(
                                f"failed to preserve conflict base for {component.identity}: "
                                f"{displayed_path}"
                            )
                        base_digest = _staged_artifact_digest(
                            artifact_root,
                            "content",
                        )
                        assert base_digest is not None
                        record["base_sha256"] = base_digest
                        record["base"] = (
                            Path(CONFLICT_BASE_DIRECTORY)
                            / component.state_tag
                            / base_id
                            / "content"
                        ).as_posix()
                        has_conflict_bases = True
                plan.conflict_records.append(record)

    for existing in plan.existing_conflicts:
        displayed_path = existing.get("path", "")
        if displayed_path in new_conflict_paths:
            continue
        display_relative = _safe_relative(displayed_path, "conflict path")
        expected_staged = Path(UPDATE_DIRECTORY) / component.state_tag / display_relative
        staged_relative = _safe_relative(existing.get("staged", ""), "staged conflict path")
        if staged_relative != expected_staged:
            raise OwnershipConflictError(
                f"staged conflict mapping changed for {component.identity}: "
                f"lock has {staged_relative}, expected {expected_staged}"
            )
        internal_relative = _internal_conflict_relative(component, displayed_path)
        local = plan.local.entries.get(internal_relative)
        incoming = plan.incoming.entries.get(internal_relative)
        current_incoming_digest = _snapshot_digest(plan.incoming, internal_relative)
        staged_digest = _staged_artifact_digest(existing_updates, displayed_path)
        recorded_digest = existing.get("incoming_sha256")
        if staged_digest is None:
            raise OwnershipConflictError(
                f"staged update is missing for {component.identity}: {displayed_path}"
            )
        if staged_digest != recorded_digest:
            raise OwnershipConflictError(
                f"staged update was locally modified for {component.identity}: "
                f"{displayed_path}; preserve it and resolve the conflict explicitly"
            )
        if (
            local != incoming
            and current_incoming_digest == recorded_digest
        ):
            retained = dict(existing)
            retained.setdefault(
                "id", conflict_id(component.identity, displayed_path)
            )
            plan.conflict_records.append(retained)
            plan.conflicts.append(
                f"{component.identity}: {displayed_path}: unresolved staged update"
            )
            continue
        if has_staged_updates:
            other_paths = {
                str(conflict.get("path", ""))
                for conflict in [*plan.existing_conflicts, *plan.conflict_records]
                if conflict is not existing
            } | new_conflict_paths
            if any(_is_descendant(path, displayed_path) for path in other_paths):
                _write_value(stage_updates, display_relative.as_posix(), None, single_file=False)
            else:
                _remove_any(stage_updates / display_relative)
        resolution = (
            "resolved staged update"
            if current_incoming_digest == recorded_digest
            else "removed stale staged update"
        )
        plan.actions.append(f"{component.identity}: {displayed_path}: {resolution}")

    active_base_ids = {
        str(record["id"])
        for record in plan.conflict_records
        if record.get("base_state") == "present" and "id" in record
    }
    if _lexists(stage_conflict_bases):
        for child in stage_conflict_bases.iterdir():
            if child.name not in active_base_ids:
                _remove_any(child)
        if not any(stage_conflict_bases.iterdir()):
            stage_conflict_bases.rmdir()
            has_conflict_bases = False

    # The normal saved base always advances to the latest upstream snapshot so
    # subsequent updates compare against the version that was actually staged.
    # Each unresolved conflict keeps its original ancestor independently under
    # ``conflict-bases`` for exact three-way review.
    stage_base.mkdir(parents=True, exist_ok=True)
    for relative in sorted(
        plan.incoming.entries,
        key=lambda item: _entry_order(item, plan.incoming.entries[item]),
    ):
        _write_value(stage_base, relative, plan.incoming.entries[relative], single_file=False)
    return has_staged_updates, has_conflict_bases


def _lock_entry(
    component: Component,
    incoming: Snapshot,
    source_root: Path,
    conflicts: Sequence[dict[str, str]],
) -> dict[str, object]:
    displayed_files = {
        _stage_relative(component, relative): value.digest
        for relative, value in sorted(incoming.entries.items())
    }
    return {
        "kind": component.kind,
        "plugin": component.plugin,
        "name": component.name,
        "source_repository": _repository_identity(source_root),
        "source": component.source_relative.as_posix(),
        "target": component.target_relative.as_posix(),
        "base_snapshot": (
            Path(STATE_DIRECTORY) / "bases" / component.state_tag
        ).as_posix(),
        "files": displayed_files,
        "conflicts": list(conflicts),
    }


@dataclass
class _Swap:
    target: Path
    backup: Path | None


def _swap_into_place(prepared: Path, target: Path, backup_root: Path, index: int) -> _Swap:
    target.parent.mkdir(parents=True, exist_ok=True)
    backup: Path | None = None
    try:
        if _lexists(target):
            backup = backup_root / f"{index:04d}"
            backup.parent.mkdir(parents=True, exist_ok=True)
            os.replace(target, backup)
        os.replace(prepared, target)
    except BaseException:
        try:
            if backup is not None and _lexists(backup):
                _remove_any(target)
                os.replace(backup, target)
            elif backup is None and not _lexists(prepared):
                _remove_any(target)
        except BaseException:
            # The outer transaction handler preserves remaining backups for
            # explicit recovery when an interrupted local repair also fails.
            pass
        raise
    return _Swap(target, backup)


def _remove_into_backup(target: Path, backup_root: Path, index: int) -> _Swap | None:
    if not _lexists(target):
        return None
    backup = backup_root / f"{index:04d}"
    backup.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(target, backup)
    except BaseException:
        try:
            if _lexists(backup):
                _remove_any(target)
                os.replace(backup, target)
        except BaseException:
            pass
        raise
    return _Swap(target, backup)


def _rollback(swaps: Sequence[_Swap]) -> list[str]:
    failures: list[str] = []
    for swap in reversed(swaps):
        try:
            _remove_any(swap.target)
            if swap.backup is not None and _lexists(swap.backup):
                swap.target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(swap.backup, swap.target)
        except OSError as exc:
            failures.append(f"{swap.target}: {exc}")
    return failures


def _preview_merge(plans: Sequence[ComponentPlan]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    actions: list[str] = []
    conflicts: list[str] = []
    for plan in plans:
        actions.extend(plan.actions)
        component = plan.component
        agents_root = plan.target.parent.parent
        _validate_existing_conflict_artifacts(
            plan, _updates_path(agents_root, component)
        )
        decisions = _merge_decisions(plan)
        current_conflicts: set[str] = set()
        for relative in sorted(decisions):
            decision = decisions[relative]
            local = plan.local.entries.get(relative)
            rendered_path = _stage_relative(component, relative)
            if decision.value != local and decision.note:
                actions.append(f"{component.identity}: {rendered_path}: {decision.note}")
            if decision.conflict:
                conflicts.append(f"{component.identity}: {rendered_path}: {decision.note}")
                current_conflicts.add(rendered_path)
        for existing in plan.existing_conflicts:
            displayed_path = existing.get("path", "")
            if displayed_path in current_conflicts:
                continue
            internal_relative = _internal_conflict_relative(component, displayed_path)
            staged_relative = _safe_relative(existing.get("staged", ""), "staged conflict path")
            local = plan.local.entries.get(internal_relative)
            incoming = plan.incoming.entries.get(internal_relative)
            current_incoming_digest = _snapshot_digest(plan.incoming, internal_relative)
            staged_digest = _staged_artifact_digest(
                agents_root / UPDATE_DIRECTORY / component.state_tag,
                displayed_path,
            )
            if staged_digest is None:
                raise OwnershipConflictError(
                    f"staged update is missing for {component.identity}: {displayed_path}"
                )
            recorded_digest = existing.get("incoming_sha256")
            if staged_digest != recorded_digest:
                raise OwnershipConflictError(
                    f"staged update was locally modified for {component.identity}: "
                    f"{displayed_path}; preserve it and resolve the conflict explicitly"
                )
            if (
                staged_digest is not None
                and local != incoming
                and current_incoming_digest == recorded_digest
            ):
                conflicts.append(
                    f"{component.identity}: {displayed_path}: unresolved staged update"
                )
            else:
                verb = (
                    "resolve staged update"
                    if current_incoming_digest == recorded_digest
                    else "remove stale staged update"
                )
                actions.append(f"{component.identity}: {displayed_path}: {verb}")
    return tuple(actions), tuple(conflicts)


def install_project(
    source_root: str | Path,
    project_root: str | Path,
    selectors: Sequence[str],
    *,
    dry_run: bool = False,
) -> InstallResult:
    """Install or update selected components in a project's flat ``.agents`` tree."""

    catalog = scan_catalog(source_root)
    requested = catalog.resolve(selectors, include_dependencies=False)
    selected = catalog.expand_dependencies(requested)
    project = Path(project_root).expanduser().resolve()
    if not project.is_dir():
        raise InstallerError(f"project root is not a directory: {project}")

    lock = load_lock(project)
    lock_components = lock["components"]
    assert isinstance(lock_components, dict)
    current_locked: list[Component] = []
    moving_locked: list[Component] = []
    for identity, raw_entry in sorted(lock_components.items()):
        if identity not in catalog.components:
            continue
        assert isinstance(raw_entry, dict)
        component = catalog.components[identity]
        current_locked.append(component)
        expected_source = component.source_relative.as_posix()
        if raw_entry.get("source") != expected_source:
            raise OwnershipConflictError(
                f"source path changed for {identity}: lock has "
                f"{raw_entry.get('source')!r}, expected {expected_source!r}"
            )
        if str(raw_entry.get("target", "")) != component.target_relative.as_posix():
            moving_locked.append(component)

    if moving_locked:
        # A topology change can alter portable links embedded in any locked
        # component, even when that component's own target is stable. Refresh
        # the complete still-current lock cohort and order movers first so old
        # targets are vacated before a newly requested component claims them.
        reordered: list[Component] = []
        seen: set[str] = set()
        for component in (*moving_locked, *current_locked, *selected):
            if component.identity in seen:
                continue
            reordered.append(component)
            seen.add(component.identity)
        selected = reordered
    selected = catalog.expand_dependencies(selected)
    requested_id_set = {component.identity for component in requested}
    dependency_reasons: dict[str, list[str]] = {}
    for component in selected:
        for dependency in catalog.dependencies.get(component.identity, ()):
            if dependency not in requested_id_set:
                dependency_reasons.setdefault(dependency, []).append(component.identity)
    plans = _preflight(catalog, project, selected, lock)
    selected_identities = tuple(component.identity for component in selected)
    preview_actions = tuple(
        (
            f"plan {component.identity} -> .agents/{component.target_relative.as_posix()}"
            + (
                " (required by "
                + ", ".join(sorted(dependency_reasons[component.identity]))
                + ")"
                if component.identity in dependency_reasons
                else ""
            )
        )
        for component in selected
    )
    if dry_run:
        merge_actions, merge_conflicts = _preview_merge(plans)
        return InstallResult(
            selected_identities,
            preview_actions + merge_actions,
            merge_conflicts,
            True,
        )

    transaction = Path(tempfile.mkdtemp(prefix=".plugin-install-", dir=project))
    agents_root = project / ".agents"
    prepared_targets = transaction / "prepared-targets"
    prepared_bases = transaction / "prepared-bases"
    prepared_updates = transaction / "prepared-updates"
    prepared_conflict_bases = transaction / "prepared-conflict-bases"
    backup_root = transaction / "backups"
    swaps: list[_Swap] = []
    update_stages: list[tuple[Path, Path]] = []
    conflict_base_stages: list[tuple[Path | None, Path]] = []

    preserve_transaction = False
    try:
        for index, plan in enumerate(plans):
            component = plan.component
            stage_target = prepared_targets / f"{index:04d}"
            stage_base = prepared_bases / component.state_tag
            stage_updates = prepared_updates / component.state_tag
            existing_updates = _updates_path(agents_root, component)
            stage_conflict_bases = prepared_conflict_bases / component.state_tag
            existing_conflict_bases = _conflict_bases_path(agents_root, component)
            has_updates, has_conflict_bases = _prepare_component(
                plan,
                stage_target,
                stage_base,
                stage_updates,
                existing_updates,
                stage_conflict_bases,
                existing_conflict_bases,
            )
            if has_updates:
                update_stages.append((stage_updates, existing_updates))
            if has_conflict_bases:
                conflict_base_stages.append(
                    (stage_conflict_bases, existing_conflict_bases)
                )
            elif _lexists(existing_conflict_bases):
                conflict_base_stages.append((None, existing_conflict_bases))

        lock_components = lock["components"]
        assert isinstance(lock_components, dict)
        new_lock = json.loads(json.dumps(lock))
        new_components = new_lock["components"]
        assert isinstance(new_components, dict)
        for plan in plans:
            new_components[plan.component.identity] = _lock_entry(
                plan.component,
                plan.incoming,
                catalog.source_root,
                plan.conflict_records,
            )
        staged_lock = transaction / LOCK_NAME
        staged_lock.write_text(
            json.dumps(new_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        # Keep the transaction (and its backups) until the complete commit has
        # either succeeded or been rolled back, including on Ctrl-C/SystemExit.
        preserve_transaction = True
        swap_index = 0
        for index, plan in enumerate(plans):
            if plan.previous_target is not None and plan.previous_target != plan.target:
                migration_swap = _remove_into_backup(
                    plan.previous_target,
                    backup_root,
                    swap_index,
                )
                if migration_swap is not None:
                    swaps.append(migration_swap)
                    swap_index += 1
            prepared_target = prepared_targets / f"{index:04d}"
            if _lexists(prepared_target):
                swaps.append(
                    _swap_into_place(
                        prepared_target,
                        plan.target,
                        backup_root,
                        swap_index,
                    )
                )
            else:
                removal_swap = _remove_into_backup(
                    plan.target,
                    backup_root,
                    swap_index,
                )
                if removal_swap is not None:
                    swaps.append(removal_swap)
            swap_index += 1
        for plan in plans:
            swaps.append(
                _swap_into_place(
                    prepared_bases / plan.component.state_tag,
                    _snapshot_path(agents_root, plan.component),
                    backup_root,
                    swap_index,
                )
            )
            swap_index += 1
        for prepared, target in update_stages:
            swaps.append(_swap_into_place(prepared, target, backup_root, swap_index))
            swap_index += 1
        for prepared, target in conflict_base_stages:
            if prepared is not None:
                swaps.append(
                    _swap_into_place(prepared, target, backup_root, swap_index)
                )
            else:
                removal_swap = _remove_into_backup(target, backup_root, swap_index)
                if removal_swap is not None:
                    swaps.append(removal_swap)
            swap_index += 1
        swaps.append(
            _swap_into_place(
                staged_lock,
                agents_root / LOCK_NAME,
                backup_root,
                swap_index,
            )
        )

        actions = preview_actions + tuple(action for plan in plans for action in plan.actions)
        conflicts = tuple(conflict for plan in plans for conflict in plan.conflicts)
        preserve_transaction = False
        return InstallResult(selected_identities, actions, conflicts, False)
    except BaseException as exc:
        rollback_failures = _rollback(swaps)
        remaining_backups = (
            sorted(path.name for path in backup_root.iterdir())
            if backup_root.is_dir()
            else []
        )
        if rollback_failures or remaining_backups:
            details = "; ".join(
                [
                    *rollback_failures,
                    *(
                        ["unreconciled backups: " + ", ".join(remaining_backups)]
                        if remaining_backups
                        else []
                    ),
                ]
            )
            raise InstallerError(
                f"install failed and rollback needs manual recovery at {transaction}: {details}"
            ) from exc
        preserve_transaction = False
        raise
    finally:
        if not preserve_transaction:
            shutil.rmtree(transaction, ignore_errors=True)


def _prune_empty_staged_parents(path: Path, boundary: Path) -> None:
    current = path
    while current != boundary:
        if not current.is_relative_to(boundary):
            raise UnsafePathError(f"staged cleanup escapes its boundary: {current}")
        try:
            current.rmdir()
        except (FileNotFoundError, OSError):
            return
        current = current.parent


def _locked_local_conflict_digest(
    agents_root: Path,
    identity: str,
    entry: dict[str, object],
    displayed_path: str,
) -> str | None:
    target = agents_root / _safe_relative(str(entry["target"]), "component target")
    _assert_safe_container(agents_root, target)
    if entry.get("kind") == "skill":
        if _lexists(target) and (target.is_symlink() or not target.is_dir()):
            raise UnsafePathError(
                f"managed skill target is not a real directory for {identity}: {target}"
            )
        return _staged_artifact_digest(target, displayed_path)
    expected_name = target.name
    if _safe_relative(displayed_path, "conflict path").as_posix() != expected_name:
        raise OwnershipConflictError(
            f"invalid file-component conflict path for {identity}: {displayed_path}"
        )
    return _staged_artifact_digest(target.parent, expected_name)


def accept_local_conflicts(
    project_root: str | Path,
    conflict_ids: Sequence[str],
    *,
    dry_run: bool = False,
    expected_local_digests: dict[str, str | None] | None = None,
) -> ConflictAdoptionResult:
    """Adopt current local component values as explicit conflict resolutions.

    This action never writes a component target. It validates the recorded
    incoming/base artifacts, removes only the selected staged conflict state,
    and atomically updates the component lock.
    """

    project = Path(project_root).expanduser().resolve()
    if not project.is_dir():
        raise InstallerError(f"project root is not a directory: {project}")
    requested = tuple(conflict_ids)
    if not requested:
        raise InstallerError("at least one conflict id is required")
    if len(set(requested)) != len(requested):
        raise InstallerError("conflict ids must not be repeated")
    for requested_id in requested:
        if not re.fullmatch(r"[0-9a-f]{16}", requested_id):
            raise InstallerError(f"invalid conflict id: {requested_id!r}")
    if expected_local_digests is not None and set(expected_local_digests) != set(
        requested
    ):
        raise InstallerError(
            "expected local digests must match the requested conflict ids"
        )

    lock = load_lock(project)
    components = lock["components"]
    assert isinstance(components, dict)
    agents_root = project / ".agents"
    indexed: dict[
        str, tuple[str, dict[str, object], dict[str, object]]
    ] = {}
    for identity, raw_entry in sorted(components.items()):
        if not isinstance(raw_entry, dict):
            continue
        raw_conflicts = raw_entry.get("conflicts", [])
        assert isinstance(raw_conflicts, list)
        displayed_paths = [
            str(raw_conflict["path"])
            for raw_conflict in raw_conflicts
            if isinstance(raw_conflict, dict)
        ]
        for index, left in enumerate(displayed_paths):
            for right in displayed_paths[index + 1 :]:
                if (
                    left == right
                    or _is_descendant(left, right)
                    or _is_descendant(right, left)
                ):
                    raise OwnershipConflictError(
                        f"overlapping lock conflict paths for {identity}: {left}, {right}"
                    )
        for raw_conflict in raw_conflicts:
            assert isinstance(raw_conflict, dict)
            displayed_path = str(raw_conflict["path"])
            item_id = conflict_id(str(identity), displayed_path)
            if item_id in indexed:
                raise OwnershipConflictError(
                    f"conflict id collision between {indexed[item_id][0]} and {identity}: "
                    f"{item_id}"
                )
            indexed[item_id] = (
                str(identity),
                raw_entry,
                raw_conflict,
            )

    missing_ids = sorted(set(requested) - set(indexed))
    if missing_ids:
        raise InstallerError(
            "unknown unresolved conflict id(s): " + ", ".join(missing_ids)
        )

    selected: dict[str, list[tuple[str, dict[str, object]]]] = {}
    adoption_items: list[ConflictAdoption] = []
    for item_id in requested:
        identity, entry, conflict = indexed[item_id]
        displayed_path = str(conflict["path"])
        internal_relative = (
            displayed_path
            if entry.get("kind") == "skill"
            else SINGLE_FILE_KEY
        )
        if _is_personalization_path(internal_relative):
            raise InstallerError(
                f"personalization conflict cannot be adopted into managed state: "
                f"{identity}: {displayed_path}"
            )
        state_tag = _state_tag(identity)
        expected_staged = (
            Path(UPDATE_DIRECTORY) / state_tag / displayed_path
        ).as_posix()
        if str(conflict["staged"]) != expected_staged:
            raise OwnershipConflictError(
                f"staged conflict mapping changed for {identity}: {displayed_path}"
            )
        update_root = agents_root / UPDATE_DIRECTORY / state_tag
        _capture_directory(update_root, reject_symlinks=True)
        incoming_digest = _staged_artifact_digest(update_root, displayed_path)
        if incoming_digest is None or incoming_digest != conflict.get("incoming_sha256"):
            raise OwnershipConflictError(
                f"staged update is missing or modified for {identity}: {displayed_path}"
            )
        operational_base_root = agents_root / _safe_relative(
            str(entry["base_snapshot"]), "base snapshot"
        )
        operational_base = _capture_directory(
            operational_base_root, reject_symlinks=True
        )
        if entry.get("kind") == "skill":
            operational_files = {
                relative: value.digest
                for relative, value in sorted(operational_base.entries.items())
            }
        else:
            if set(operational_base.entries) - {SINGLE_FILE_KEY}:
                raise OwnershipConflictError(
                    f"saved upstream base has unexpected entries for {identity}"
                )
            operational_value = operational_base.entries.get(SINGLE_FILE_KEY)
            operational_files = (
                {Path(str(entry["target"])).name: operational_value.digest}
                if operational_value is not None
                else {}
            )
        if operational_files != entry.get("files"):
            raise OwnershipConflictError(
                f"saved upstream base was modified for {identity}"
            )
        operational_digest = _snapshot_digest(
            operational_base, internal_relative
        )
        if operational_digest != incoming_digest:
            raise OwnershipConflictError(
                f"latest upstream base does not match the staged update for {identity}: "
                f"{displayed_path}"
            )

        expected_base_root = agents_root / CONFLICT_BASE_DIRECTORY / state_tag / item_id
        base_state = conflict.get("base_state")
        if base_state == "present":
            recorded_base = conflict.get("base")
            assert isinstance(recorded_base, str)
            base_path = agents_root / _safe_relative(
                recorded_base, "conflict base path"
            )
            _capture_directory(base_path.parent.parent, reject_symlinks=True)
            base_digest = _staged_artifact_digest(base_path.parent, base_path.name)
            if base_digest != conflict.get("base_sha256"):
                raise OwnershipConflictError(
                    f"saved conflict base is missing or modified for {identity}: "
                    f"{displayed_path}"
                )
        elif base_state == "missing" and _lexists(expected_base_root):
            raise OwnershipConflictError(
                f"saved conflict base unexpectedly exists for {identity}: {displayed_path}"
            )

        local_digest = _locked_local_conflict_digest(
            agents_root, identity, entry, displayed_path
        )
        if (
            expected_local_digests is not None
            and local_digest != expected_local_digests[item_id]
        ):
            raise OwnershipConflictError(
                f"current local value changed after review for {identity}: "
                f"{displayed_path}"
            )
        adoption_items.append(
            ConflictAdoption(
                item_id,
                identity,
                displayed_path,
                "missing" if local_digest is None else "present",
                local_digest,
            )
        )
        selected.setdefault(identity, []).append((item_id, conflict))

    result = ConflictAdoptionResult(tuple(adoption_items), dry_run)
    if dry_run:
        return result

    transaction = Path(tempfile.mkdtemp(prefix=".plugin-accept-", dir=project))
    prepared_updates = transaction / "prepared-updates"
    prepared_conflict_bases = transaction / "prepared-conflict-bases"
    backup_root = transaction / "backups"
    state_swaps: list[tuple[Path | None, Path]] = []
    base_swaps: list[tuple[Path | None, Path]] = []
    swaps: list[_Swap] = []
    preserve_transaction = False
    try:
        new_lock = json.loads(json.dumps(lock))
        new_components = new_lock["components"]
        assert isinstance(new_components, dict)
        for identity, accepted in sorted(selected.items()):
            entry = components[identity]
            assert isinstance(entry, dict)
            state_tag = _state_tag(identity)
            update_root = agents_root / UPDATE_DIRECTORY / state_tag
            stage_updates = prepared_updates / state_tag
            _capture_directory(update_root, reject_symlinks=True)
            shutil.copytree(update_root, stage_updates, symlinks=True)
            for _item_id, conflict in accepted:
                relative = _safe_relative(
                    str(conflict["path"]), "conflict path"
                )
                copied_digest = _staged_artifact_digest(
                    stage_updates, relative.as_posix()
                )
                if copied_digest != conflict.get("incoming_sha256"):
                    raise OwnershipConflictError(
                        f"staged update changed while adopting {identity}: "
                        f"{relative.as_posix()}"
                    )
                staged_path = stage_updates / relative
                _remove_any(staged_path)
                _prune_empty_staged_parents(staged_path.parent, stage_updates)
            if stage_updates.is_dir() and not any(stage_updates.iterdir()):
                stage_updates.rmdir()
            state_swaps.append(
                (stage_updates if _lexists(stage_updates) else None, update_root)
            )

            accepted_present_bases = [
                (item_id, conflict)
                for item_id, conflict in accepted
                if conflict.get("base_state") == "present"
            ]
            conflict_base_root = agents_root / CONFLICT_BASE_DIRECTORY / state_tag
            if accepted_present_bases:
                stage_bases = prepared_conflict_bases / state_tag
                if not _lexists(conflict_base_root):
                    raise OwnershipConflictError(
                        f"saved conflict base root is missing for {identity}"
                    )
                _capture_directory(conflict_base_root, reject_symlinks=True)
                shutil.copytree(conflict_base_root, stage_bases, symlinks=True)
                for item_id, conflict in accepted_present_bases:
                    copied_base = stage_bases / item_id / "content"
                    copied_base_digest = _staged_artifact_digest(
                        copied_base.parent, copied_base.name
                    )
                    if copied_base_digest != conflict.get("base_sha256"):
                        raise OwnershipConflictError(
                            f"saved conflict base changed while adopting {identity}: "
                            f"{conflict['path']}"
                        )
                    _remove_any(stage_bases / item_id)
                if stage_bases.is_dir() and not any(stage_bases.iterdir()):
                    stage_bases.rmdir()
                base_swaps.append(
                    (
                        stage_bases if _lexists(stage_bases) else None,
                        conflict_base_root,
                    )
                )

            accepted_ids = {item_id for item_id, _conflict in accepted}
            new_entry = new_components[identity]
            assert isinstance(new_entry, dict)
            new_entry["conflicts"] = [
                conflict
                for conflict in new_entry.get("conflicts", [])
                if (
                    conflict_id(identity, str(conflict["path"]))
                    not in accepted_ids
                )
            ]

        staged_lock = transaction / LOCK_NAME
        staged_lock.write_text(
            json.dumps(new_lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        for item in adoption_items:
            entry = components[item.identity]
            assert isinstance(entry, dict)
            current_digest = _locked_local_conflict_digest(
                agents_root,
                item.identity,
                entry,
                item.path,
            )
            if current_digest != item.local_sha256:
                raise OwnershipConflictError(
                    f"current local value changed while adopting {item.identity}: "
                    f"{item.path}"
                )

        preserve_transaction = True
        swap_index = 0
        for prepared, target in [*state_swaps, *base_swaps]:
            if prepared is not None:
                swaps.append(
                    _swap_into_place(prepared, target, backup_root, swap_index)
                )
            else:
                removal_swap = _remove_into_backup(target, backup_root, swap_index)
                if removal_swap is not None:
                    swaps.append(removal_swap)
            swap_index += 1
        swaps.append(
            _swap_into_place(
                staged_lock,
                agents_root / LOCK_NAME,
                backup_root,
                swap_index,
            )
        )
        preserve_transaction = False
        return result
    except BaseException as exc:
        rollback_failures = _rollback(swaps)
        remaining_backups = (
            sorted(path.name for path in backup_root.iterdir())
            if backup_root.is_dir()
            else []
        )
        if rollback_failures or remaining_backups:
            details = "; ".join(
                [
                    *rollback_failures,
                    *(
                        ["unreconciled backups: " + ", ".join(remaining_backups)]
                        if remaining_backups
                        else []
                    ),
                ]
            )
            raise InstallerError(
                "conflict adoption failed and rollback needs manual recovery at "
                f"{transaction}: {details}"
            ) from exc
        preserve_transaction = False
        raise
    finally:
        if not preserve_transaction:
            shutil.rmtree(transaction, ignore_errors=True)


def update_project(
    source_root: str | Path,
    project_root: str | Path,
    *,
    selectors: Sequence[str] | None = None,
    dry_run: bool = False,
) -> InstallResult:
    """Refresh locked components, or a typed subset, through the same merge engine."""

    project = Path(project_root).expanduser().resolve()
    catalog = scan_catalog(source_root)
    if selectors:
        resolved_selectors = list(selectors)
    else:
        lock = load_lock(project)
        components = lock["components"]
        assert isinstance(components, dict)
        if not components:
            raise InstallerError(f"no project-local plugin installs found under {project / '.agents'}")
        missing = sorted(identity for identity in components if identity not in catalog.components)
        replacements = {
            identity: COMPONENT_RENAMES[identity]
            for identity in missing
            if (
                identity in COMPONENT_RENAMES
                and COMPONENT_RENAMES[identity] in catalog.components
            )
        }
        resolved_selectors = sorted(
            {
                *(identity for identity in components if identity in catalog.components),
                *replacements.values(),
            }
        )
        orphan_actions = tuple(
            (
                f"preserved renamed predecessor {identity}; installed current replacement "
                f"{replacements[identity]}"
                if identity in replacements
                else f"preserved orphaned locked component {identity}: no longer present upstream"
            )
            for identity in missing
        )
        if not resolved_selectors:
            return InstallResult((), orphan_actions, (), dry_run)
        result = install_project(
            source_root, project, resolved_selectors, dry_run=dry_run
        )
        return InstallResult(
            result.selected,
            orphan_actions + result.actions,
            result.conflicts,
            result.dry_run,
        )
    return install_project(source_root, project, resolved_selectors, dry_run=dry_run)


def _print_catalog(catalog: Catalog) -> None:
    for plugin in sorted(catalog.plugins):
        print(f"plugin:{plugin}")
        for identity in catalog.plugins[plugin]:
            component = catalog.components[identity]
            print(f"  {identity} -> .agents/{component.target_relative.as_posix()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install plugin components into a project's flat .agents tree.")
    parser.add_argument("--source-root", default=".", help="Plugin bundle source root")
    parser.add_argument("--project-root", default=".", help="Target project root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List typed selectors and targets")
    list_parser.set_defaults(action="list")

    install_parser = subparsers.add_parser("install", help="Install plugins or individual components")
    install_parser.add_argument("selectors", nargs="*")
    install_parser.add_argument("--dry-run", action="store_true")
    install_parser.set_defaults(action="install")

    update_parser = subparsers.add_parser("update", help="Update locked components")
    update_parser.add_argument("selectors", nargs="*")
    update_parser.add_argument("--dry-run", action="store_true")
    update_parser.set_defaults(action="update")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        catalog = scan_catalog(args.source_root)
        if args.action == "list":
            _print_catalog(catalog)
            return 0
        selectors = list(args.selectors)
        if args.action == "install" and not selectors:
            if not sys.stdin.isatty():
                raise SelectorError("selectors are required in non-interactive mode")
            selectors = prompt_selectors(catalog)
        if args.action == "install":
            result = install_project(
                args.source_root,
                args.project_root,
                selectors,
                dry_run=args.dry_run,
            )
        else:
            result = update_project(
                args.source_root,
                args.project_root,
                selectors=selectors or None,
                dry_run=args.dry_run,
            )
        for action in result.actions:
            print(action)
        for conflict in result.conflicts:
            print(f"conflict: {conflict}", file=sys.stderr)
        return 0
    except InstallerError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
