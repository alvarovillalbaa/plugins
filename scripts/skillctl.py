#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_REPO = "alvarovillalbaa/plugins"
RUNTIME_MARKERS = (
    ".codex/skills",
    ".cursor",
    ".openclaw",
    ".claude/plugins",
    ".claude/cache",
    "claude/plugins/cache",
)
DEPARTMENT_REQUIRED_DIRS = ("skills", "agents", "commands", "rules")
DEPARTMENT_REQUIRED_FILES = (
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    "TEAM.md",
    "profile.yaml",
    "mcp.json",
)
RETIRED_SKILL_PATH_ROOTS = {"agent-suite", "business-ops", "learning-system"}
VALID_TOOL_NAMES = {
    "Agent",
    "AskUserQuestion",
    "Bash",
    "Edit",
    "Glob",
    "Grep",
    "Read",
    "Skill",
    "WebFetch",
    "WebSearch",
    "Write",
}
PRIVATE_PATTERNS = (
    r"(?i)(api[_-]?key|apikey|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}",
    r"(?i)bearer\s+[A-Za-z0-9_./+=-]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
)
INLINE_SKILL_REF_RE = re.compile(r"\*\*([a-z0-9][a-z0-9-]*)\*\*")
LOCAL_SKILL_PATH_RE = re.compile(r"(?:\./)?[a-z][a-z0-9-]*/skills/[a-z0-9-]+")
COMMAND_SKILL_REF_RE = re.compile(r"(?:`([a-z0-9][a-z0-9-]*)`\s+skill|skill\s+`([a-z0-9][a-z0-9-]*)`)")
BACKTICK_REF_RE = re.compile(r"`([^`]+)`")
DOLLAR_SKILL_REF_RE = re.compile(r"\$([a-z0-9][a-z0-9-]*)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
EXTERNAL_INSTALL_REF_RE = re.compile(r"--skill\s+([a-z0-9-]+)")
OPTIONAL_EXTERNAL_REF_RE = re.compile(r"optional external(?: chain)?:?\s+\*\*([a-z0-9-]+)\*\*", re.IGNORECASE)
SKILL_REF_TOKEN_RE = re.compile(r"^[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)?$")
COMMAND_AGENT_TOOL_RE = re.compile(
    r"(Use agent:|Spawn(?:\s+the)?\s+.+?\s+agent|Invoke\s+.+?\s+agent|using\s+.+?\s+agent|agent\s+at\s+`[^`]+/agents/|Agent\s+tool)",
    re.IGNORECASE,
)
EXTERNAL_SKILL_REQUIRED_FIELDS = {"owner", "repo", "ref", "path", "install_name", "homepage", "domain"}
EXTERNAL_SOURCE_REQUIRED_FIELDS = {"owner", "repo", "ref", "homepage", "domain"}
ROOT_ALLOWED_PATTERNS = (
    ".claude-plugin/**",
    ".github/workflows/**",
    ".gitignore",
    "CHANGELOG.md",
    "COMPANY.md",
    "CONTRIBUTING.md",
    "QUICK_START.md",
    "README.md",
    "TESTING.md",
    "assets/**",
    "docs/**",
    "publish_targets.yml",
    "references/**",
    "schemas/**",
    "scripts/**",
    "*/.claude-plugin/**",
    "*/.codex-plugin/**",
    "*/.cursor-plugin/**",
    "*/TEAM.md",
    "*/README.md",
    "*/agents/**",
    "*/commands/**",
    "*/mcp.json",
    "*/profile.yaml",
    "*/rules/**",
)
LOCAL_ONLY_PATTERNS = (
    "*.local.yml",
    "personalize.local.yml",
    ".overlays/**",
    ".generated/**",
    ".company/**",
    ".user/**",
    ".skill-improvements/**",
    ".skill-lock.yml",
    ".skill-lock.json",
    ".worktrees/**",
)


class SkillctlError(Exception):
    pass


@dataclass(frozen=True)
class Classification:
    path: str
    kind: str
    reason: str


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), check=check, text=True, capture_output=True)


def bool_value(value: str) -> object:
    if value == "true":
        return True
    if value == "false":
        return False
    return value.strip('"').strip("'")


def parse_simple_yaml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    section: str | None = None
    list_key: str | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))

        if indent == 0:
            section = None
            list_key = None
            if ":" not in stripped:
                raise SkillctlError(f"{path}: expected key/value line: {raw}")
            key, value = stripped.split(":", 1)
            value = value.strip()
            if value:
                data[key] = bool_value(value)
            else:
                data[key] = {}
                section = key
            continue

        if indent == 2 and section:
            if ":" not in stripped:
                raise SkillctlError(f"{path}: expected nested key/value line: {raw}")
            key, value = stripped.split(":", 1)
            value = value.strip()
            if value:
                assert isinstance(data[section], dict)
                data[section][key] = bool_value(value)
                list_key = None
            else:
                assert isinstance(data[section], dict)
                data[section][key] = []
                list_key = key
            continue

        if indent == 4 and section and list_key and stripped.startswith("- "):
            assert isinstance(data[section], dict)
            values = data[section][list_key]
            assert isinstance(values, list)
            values.append(stripped[2:].strip('"').strip("'"))
            continue

        raise SkillctlError(f"{path}: unsupported YAML shape: {raw}")

    return data


def parse_profile_list(path: Path, key: str) -> list[str]:
    items: list[str] = []
    active = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            active = stripped == f"{key}:"
            continue
        if active and indent == 2 and stripped.startswith("- "):
            items.append(stripped[2:].strip().strip('"').strip("'"))
    return items


def frontmatter_field(path: Path, key: str) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index] == "---":
            break
        stripped = lines[index].strip()
        if not stripped.startswith(f"{key}:"):
            continue
        return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def profile_scalar(path: Path, key: str) -> str:
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped.startswith(f"{key}:"):
            return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def read_json(path: Path, failures: list[str], root: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        failures.append(f"{relative_to_root(path, root)}: invalid JSON: {exc}")
        return {}


def public_name_slug(name: str) -> str:
    return name.replace(":", "-")


def clean_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def external_skill_names(root: Path, failures: list[str] | None = None) -> set[str]:
    registry = root / "references" / "external-skills.yaml"
    names: set[str] = set()
    if not registry.exists():
        return names
    registry_entries: dict[str, dict[str, str]] = {}
    install_names: dict[str, str] = {}
    current_name: str | None = None
    current_fields: dict[str, str] = {}
    in_skills = False

    def finish_current() -> None:
        nonlocal current_name, current_fields
        if current_name is None:
            return
        if current_name in registry_entries:
            if failures is not None:
                failures.append(f"{relative_to_root(registry, root)}: duplicate external skill `{current_name}`")
        registry_entries[current_name] = current_fields
        names.add(current_name)
        missing = sorted(EXTERNAL_SKILL_REQUIRED_FIELDS - set(current_fields))
        if failures is not None and missing:
            failures.append(
                f"{relative_to_root(registry, root)}: external skill `{current_name}` missing required field(s): {', '.join(missing)}"
            )
        install_name = current_fields.get("install_name", "")
        if install_name:
            if failures is not None and install_name in install_names and install_names[install_name] != current_name:
                failures.append(
                    f"{relative_to_root(registry, root)}: duplicate external install_name `{install_name}`"
                )
            install_names[install_name] = current_name
            names.add(install_name)
        current_name = None
        current_fields = {}

    for line_number, raw in enumerate(registry.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "skills:":
            finish_current()
            in_skills = True
            continue
        if not in_skills:
            continue
        if re.fullmatch(r"  [a-z0-9-]+:", line):
            finish_current()
            current_name = stripped[:-1]
            current_fields = {}
            continue
        if current_name and line.startswith("    ") and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            if failures is not None and key in current_fields:
                failures.append(
                    f"{relative_to_root(registry, root)}:{line_number}: external skill `{current_name}` repeats field `{key}`"
                )
            current_fields[key] = clean_yaml_scalar(value)
            continue
        if failures is not None:
            failures.append(f"{relative_to_root(registry, root)}:{line_number}: unsupported external skill registry line")
    finish_current()
    return names


def external_source_names(root: Path, failures: list[str] | None = None) -> set[str]:
    registry = root / "references" / "external-sources.yaml"
    names: set[str] = set()
    if not registry.exists():
        return names
    registry_entries: dict[str, dict[str, str]] = {}
    current_name: str | None = None
    current_fields: dict[str, str] = {}
    in_sources = False

    def finish_current() -> None:
        nonlocal current_name, current_fields
        if current_name is None:
            return
        if current_name in registry_entries and failures is not None:
            failures.append(f"{relative_to_root(registry, root)}: duplicate external source `{current_name}`")
        registry_entries[current_name] = current_fields
        names.add(current_name)
        missing = sorted(EXTERNAL_SOURCE_REQUIRED_FIELDS - set(current_fields))
        if failures is not None and missing:
            failures.append(
                f"{relative_to_root(registry, root)}: external source `{current_name}` missing required field(s): {', '.join(missing)}"
            )
        current_name = None
        current_fields = {}

    for line_number, raw in enumerate(registry.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "sources:":
            finish_current()
            in_sources = True
            continue
        if not in_sources:
            continue
        if re.fullmatch(r"  [a-z0-9-]+:", line):
            finish_current()
            current_name = stripped[:-1]
            current_fields = {}
            continue
        if current_name and line.startswith("    ") and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            if failures is not None and key in current_fields:
                failures.append(
                    f"{relative_to_root(registry, root)}:{line_number}: external source `{current_name}` repeats field `{key}`"
                )
            current_fields[key] = clean_yaml_scalar(value)
            continue
        if failures is not None:
            failures.append(f"{relative_to_root(registry, root)}:{line_number}: unsupported external source registry line")
    finish_current()
    return names


def command_skill_refs(path: Path) -> set[str]:
    refs: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Use skill"):
            refs.update(INLINE_SKILL_REF_RE.findall(line))
        for match in COMMAND_SKILL_REF_RE.finditer(line):
            refs.update(value for value in match.groups() if value)
    return refs


def explicit_external_skill_refs(path: Path) -> list[tuple[int, str]]:
    refs: list[tuple[int, str]] = []
    seen: set[tuple[int, str]] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for pattern in (EXTERNAL_INSTALL_REF_RE, OPTIONAL_EXTERNAL_REF_RE):
            for name in pattern.findall(line):
                item = (line_number, name)
                if item in seen:
                    continue
                seen.add(item)
                refs.append(item)
    return refs


def agent_primary_skill_refs(path: Path) -> set[str]:
    refs: set[str] = set()
    in_section = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped.lower() == "## primary skills":
            in_section = True
            continue
        if in_section and raw.startswith("## "):
            in_section = False
            continue
        if not in_section:
            continue
        match = re.match(r"- `([^`]+)`", stripped)
        if match:
            refs.add(match.group(1))
    return refs


def agent_command_refs(path: Path) -> set[str]:
    refs: set[str] = set()
    in_section = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped.lower() in {"## commands", "## relevant commands"}:
            in_section = True
            continue
        if in_section and raw.startswith("## "):
            in_section = False
            continue
        if not in_section:
            continue
        refs.update(ref.lstrip("/") for ref in BACKTICK_REF_RE.findall(stripped))
    return refs


def agent_spawned_by_command_refs(path: Path) -> set[str]:
    refs: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if "spawned by" not in line.lower():
            continue
        refs.update(ref.strip() for ref in re.findall(r"`/([^`]+)`", line))
    return refs


def frontmatter_tool_names(value: str) -> set[str]:
    names: set[str] = set()
    for raw in value.split(","):
        token = raw.strip().strip("[]").strip().strip('"').strip("'")
        if not token:
            continue
        names.add(token.split("(", 1)[0].strip())
    return names


def local_skill_path_refs(path: Path, skill_path_roots: set[str] | None = None) -> set[str]:
    refs = {
        match[2:] if match.startswith("./") else match
        for match in LOCAL_SKILL_PATH_RE.findall(path.read_text(encoding="utf-8"))
    }
    if skill_path_roots is None:
        return refs
    return {ref for ref in refs if ref.split("/", 1)[0] in skill_path_roots}


def is_skill_ref_token(ref: str) -> bool:
    return bool(SKILL_REF_TOKEN_RE.fullmatch(ref))


def parse_internal_chain_rows(path: Path) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    in_internal = False
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if raw.startswith("## Chains"):
            in_internal = True
            continue
        if not in_internal or not raw.startswith("| `"):
            continue
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        parent_refs = BACKTICK_REF_RE.findall(cells[0])
        if not parent_refs:
            continue
        parent = parent_refs[0]
        rows[parent] = {
            "line": line_number,
            "children": [] if cells[1] == "—" else BACKTICK_REF_RE.findall(cells[1]),
            "chains": BACKTICK_REF_RE.findall(cells[2]),
        }
    return rows


def skill_children_section(path: Path) -> list[str]:
    children: list[str] = []
    in_section = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped == "## Children":
            in_section = True
            continue
        if in_section and raw.startswith("## "):
            break
        if not in_section:
            continue
        match = re.search(r"\[`([^`]+)`\]\(\.\./([^/]+)/SKILL\.md\)", raw)
        if match:
            children.append(match.group(1))
    return children


def direct_chain_rule_list(path: Path) -> list[str]:
    refs: list[str] = []
    in_section = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped == "## Chain Rules":
            in_section = True
            continue
        if in_section and raw.startswith("## "):
            break
        if not in_section:
            continue
        match = re.fullmatch(r"- `([^`]+)`", stripped)
        if match and is_skill_ref_token(match.group(1)):
            refs.append(match.group(1))
    return refs


def chain_rule_refs(path: Path) -> list[tuple[int, str]]:
    refs: list[tuple[int, str]] = []
    in_section = False
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw.strip()
        if stripped == "## Chain Rules":
            in_section = True
            continue
        if in_section and raw.startswith("## "):
            break
        if not in_section:
            continue
        for ref in BACKTICK_REF_RE.findall(raw):
            if is_skill_ref_token(ref):
                refs.append((line_number, ref))
    return refs


def local_markdown_links(path: Path) -> list[tuple[int, str, Path]]:
    links: list[tuple[int, str, Path]] = []
    in_fence = False
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in MARKDOWN_LINK_RE.finditer(line):
            raw = match.group(1).strip()
            if not raw or raw.startswith("#"):
                continue
            target = unquote(raw.split()[0].strip("<>"))
            if target.startswith(("http://", "https://", "mailto:", "app://")):
                continue
            target = target.split("#", 1)[0]
            if not target or target.startswith("/"):
                continue
            links.append((line_number, raw, path.parent / target))
    return links


def active_markdown_link_files(root: Path, skill_files: list[Path]) -> list[Path]:
    files = set(skill_files)
    files.update(root.glob("*/skills/*/references/**/*.md"))
    files.update(root.glob("*/commands/*.md"))
    files.update(root.glob("*/agents/*.md"))
    files.update(root.glob("*/README.md"))
    files.update(root.glob("docs/**/*.md"))
    for name in ("README.md", "QUICK_START.md", "CHANGELOG.md", "COMPANY.md", "CONTRIBUTING.md", "TESTING.md"):
        path = root / name
        if path.exists():
            files.add(path)
    chain_map = root / "skills-chaining-map.md"
    if chain_map.exists():
        files.add(chain_map)
    files.update(root.glob("references/docs/*.md"))
    return sorted(files)


def append_duplicate_failures(failures: list[str], label: str, paths_by_name: dict[str, list[Path]], root: Path) -> None:
    for name, paths in sorted(paths_by_name.items()):
        if len(paths) < 2:
            continue
        rendered = ", ".join(relative_to_root(path, root) for path in paths)
        failures.append(f"duplicate {label} name `{name}`: {rendered}")


def department_display_name(department: Path) -> str:
    return " ".join(part.capitalize() for part in department.name.split("-"))


def root_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.expanduser().as_posix()


def skill_dirs(root: Path) -> list[Path]:
    return sorted(path.parent for path in root.rglob("SKILL.md") if "skills" in path.parts)


def department_dirs(root: Path) -> list[Path]:
    return sorted(
        path.parent
        for path in root.glob("*/profile.yaml")
        if path.parent.is_dir() and (path.parent / ".claude-plugin" / "plugin.json").exists()
    )


def department_for_skill(skill_dir: Path) -> str:
    parts = skill_dir.parts
    if "skills" not in parts:
        raise SkillctlError(f"not a skill path: {skill_dir}")
    index = parts.index("skills")
    if index == 0:
        raise SkillctlError(f"skill path has no department: {skill_dir}")
    return parts[index - 1]


def default_meta_text(skill_dir: Path, root: Path) -> str:
    rel = relative_to_root(skill_dir, root)
    department = department_for_skill(Path(rel))
    name = skill_dir.name
    require_eval = "true" if name in {"auto-improve", "skill-eval-loop", "agent-harness"} else "false"
    return f"""id: {department}.{name}
name: {name}
origin:
  repo: {CANONICAL_REPO}
  branch: main
  path: {rel}
install:
  mode: symlink-preferred
  agents:
    - codex
    - cursor
    - openclaw
    - claude-code
personalization:
  policy: overlay-only
  local_files:
    - personalize.local.yml
    - "*.local.yml"
    - .overlays/**
    - .generated/**
    - .company/**
    - .user/**
upstream_contribution:
  allowed_paths:
    - .skillmeta.yml
    - SKILL.md
    - README.md
    - agents/**
    - scripts/**
    - references/**
    - templates/**
    - examples/**
    - hooks/**
    - personalization.schema.json
    - personalize.example.yml
    - evals/**
  forbidden_paths:
    - personalize.local.yml
    - "*.local.yml"
    - .overlays/**
    - .generated/**
    - .company/**
    - .user/**
    - generated/**
    - private/**
quality_gates:
  require_eval: {require_eval}
  require_diff_classification: true
  require_human_review: true
"""


def nearest_skill_dir(path: Path, root: Path) -> Path | None:
    current = path if path.is_dir() else path.parent
    root = root.resolve()
    while True:
        if (current / "SKILL.md").exists() or (current / ".skillmeta.yml").exists():
            return current
        if current == root or current.parent == current:
            return None
        current = current.parent


def nearest_meta(path: Path, root: Path) -> tuple[Path | None, dict[str, object] | None]:
    skill_dir = nearest_skill_dir(path, root)
    if not skill_dir:
        return None, None
    meta = skill_dir / ".skillmeta.yml"
    if not meta.exists():
        return skill_dir, None
    return skill_dir, parse_simple_yaml(meta)


def list_value(meta: dict[str, object], section: str, key: str) -> list[str]:
    value = meta.get(section, {})
    if not isinstance(value, dict):
        return []
    items = value.get(key, [])
    return [str(item) for item in items] if isinstance(items, list) else []


def scalar_value(meta: dict[str, object], section: str, key: str) -> str:
    value = meta.get(section, {})
    if not isinstance(value, dict):
        return ""
    item = value.get(key, "")
    return str(item)


def is_runtime_path(path: Path) -> bool:
    text = path.expanduser().as_posix()
    return any(marker in text for marker in RUNTIME_MARKERS)


def matches_any(rel: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel, pattern) for pattern in patterns)


def has_private_signal(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return any(re.search(pattern, text) for pattern in PRIVATE_PATTERNS)


def classify_path(path: Path, root: Path) -> Classification:
    path = path.expanduser()
    if is_runtime_path(path):
        return Classification(path.as_posix(), "generated-runtime", "runtime install or cache path")

    resolved = path.resolve() if path.exists() else (root / path).resolve()
    root_rel = relative_to_root(resolved, root)
    if matches_any(root_rel, list(LOCAL_ONLY_PATTERNS)):
        return Classification(root_rel, "local-private", "matches local-only path")
    if matches_any(root_rel, list(ROOT_ALLOWED_PATTERNS)):
        if has_private_signal(resolved):
            return Classification(root_rel, "local-private", "likely secret or private data")
        return Classification(root_rel, "upstream-safe", "allowed repo source path")

    skill_dir, meta = nearest_meta(resolved, root)
    if not meta or not skill_dir:
        return Classification(relative_to_root(resolved, root), "local-private", "no .skillmeta.yml provenance")

    origin_repo = scalar_value(meta, "origin", "repo")
    origin_path = scalar_value(meta, "origin", "path")
    skill_rel = relative_to_root(skill_dir, root)
    if resolved == skill_dir:
        return Classification(relative_to_root(resolved, root), "upstream-safe", "source-tracked skill root")
    rel_to_skill = resolved.relative_to(skill_dir).as_posix() if resolved.is_relative_to(skill_dir) else resolved.name

    forbidden = list_value(meta, "upstream_contribution", "forbidden_paths")
    allowed = list_value(meta, "upstream_contribution", "allowed_paths")
    if matches_any(rel_to_skill, forbidden):
        return Classification(relative_to_root(resolved, root), "local-private", "matches forbidden local/private path")
    if rel_to_skill.startswith(".generated/") or rel_to_skill.startswith("generated/"):
        return Classification(relative_to_root(resolved, root), "generated-runtime", "generated output")
    if has_private_signal(resolved):
        return Classification(relative_to_root(resolved, root), "local-private", "likely secret or private data")
    if origin_repo == CANONICAL_REPO and origin_path == skill_rel and matches_any(rel_to_skill, allowed):
        if rel_to_skill in {"personalization.schema.json", "personalize.example.yml"} or rel_to_skill.startswith("left-to-personalize/"):
            return Classification(relative_to_root(resolved, root), "personalization-template", "allowed personalization template")
        return Classification(relative_to_root(resolved, root), "upstream-safe", "allowed source-tracked path")
    return Classification(relative_to_root(resolved, root), "local-private", "origin metadata does not match source path")


def meta_generate(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    written = 0
    skipped = 0
    for skill_dir in skill_dirs(root):
        meta_path = skill_dir / ".skillmeta.yml"
        if meta_path.exists() and not args.force:
            skipped += 1
            continue
        text = default_meta_text(skill_dir, root)
        if args.dry_run:
            print(f"would write {relative_to_root(meta_path, root)}")
            continue
        meta_path.write_text(text, encoding="utf-8")
        written += 1
    if args.dry_run:
        print(f"Would write metadata for {len(skill_dirs(root)) - skipped} skill(s); skipped {skipped}.")
    else:
        print(f"Wrote {written} skill metadata file(s); skipped {skipped}.")
    return 0


def meta_check(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    failures: list[str] = []
    metas = sorted(root.rglob(".skillmeta.yml"))
    if args.require_pilot and not metas:
        raise SkillctlError("no .skillmeta.yml files found")

    if getattr(args, "require_all", False):
        for skill_dir in skill_dirs(root):
            meta_path = skill_dir / ".skillmeta.yml"
            if not meta_path.exists():
                failures.append(f"{meta_path}: missing .skillmeta.yml")

    for meta_path in metas:
        meta = parse_simple_yaml(meta_path)
        required = {"id", "name", "origin", "install", "personalization", "upstream_contribution", "quality_gates"}
        missing = sorted(required - set(meta))
        if missing:
            failures.append(f"{meta_path}: missing {', '.join(missing)}")
            continue
        skill_dir = meta_path.parent
        if not (skill_dir / "SKILL.md").exists():
            failures.append(f"{meta_path}: sibling SKILL.md not found")
        if str(meta.get("name")) != skill_dir.name:
            failures.append(f"{meta_path}: name must match directory `{skill_dir.name}`")
        origin_path = scalar_value(meta, "origin", "path")
        if origin_path != relative_to_root(skill_dir, root):
            failures.append(f"{meta_path}: origin.path `{origin_path}` does not match `{relative_to_root(skill_dir, root)}`")
        if scalar_value(meta, "personalization", "policy") != "overlay-only":
            failures.append(f"{meta_path}: personalization.policy must be overlay-only")
        if not list_value(meta, "upstream_contribution", "allowed_paths"):
            failures.append(f"{meta_path}: allowed_paths must not be empty")
        if not list_value(meta, "upstream_contribution", "forbidden_paths"):
            failures.append(f"{meta_path}: forbidden_paths must not be empty")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print(f"Validated {len(metas)} skill metadata file(s).")
    return 0


def trace_origin(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    for raw in args.paths:
        classification = classify_path(root_path(raw) if Path(raw).is_absolute() else root / raw, root)
        print(f"{classification.path}: {classification.kind} ({classification.reason})")
    return 0


def git_changed_files(root: Path, base: str, head: str) -> list[str]:
    if base == head:
        return []
    result = run(["git", "diff", "--name-only", base, head], cwd=root)
    return [line for line in result.stdout.splitlines() if line.strip()]


def patch_changed_files(root: Path, base: str, head: str) -> list[str]:
    if base == head:
        result = run(["git", "diff", "--name-only"], cwd=root, check=False)
    else:
        result = run(["git", "diff", "--name-only", base, head], cwd=root, check=False)
    return [line for line in result.stdout.splitlines() if line.strip()]


def diff_classify(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    files = list(args.file or [])
    files.extend(git_changed_files(root, args.base, args.head))
    files = sorted(dict.fromkeys(files))

    classifications = [classify_path(root / file, root) for file in files]
    for item in classifications:
        print(f"{item.path}\t{item.kind}\t{item.reason}")

    blocked = [item for item in classifications if item.kind in {"local-private", "generated-runtime"}]
    if args.fail_on_private and blocked:
        print(f"Blocked {len(blocked)} private/runtime file(s).", file=sys.stderr)
        return 1
    if not classifications:
        print("No changed files to classify.")
    return 0


def parse_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    stack: list[tuple[int, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        indent = len(line) - len(line.lstrip(" "))
        while stack and stack[-1][0] >= indent:
            stack.pop()
        key, value = stripped.split(":", 1)
        clean_key = key.strip()
        clean = value.strip().strip('"').strip("'")
        if not clean:
            stack.append((indent, clean_key))
            continue
        if clean.startswith("{{"):
            continue
        path_key = "_".join([item[1] for item in stack] + [clean_key]).upper().replace(".", "_").replace("-", "_")
        values[path_key] = clean
        values[clean_key.upper().replace(".", "_").replace("-", "_")] = clean
    return values


PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def render_overlays(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    skill = root_path(args.skill) if Path(args.skill).is_absolute() else root / args.skill
    source = skill / "left-to-personalize"
    if not source.exists():
        print(f"No left-to-personalize directory at {source}")
        return 0
    values = parse_values(root_path(args.values))
    out = root_path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rendered = 0
    for path in sorted(source.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(source)
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            return values.get(match.group(1), match.group(0))

        target.write_text(PLACEHOLDER_RE.sub(replace, text), encoding="utf-8")
        rendered += 1
    print(f"Rendered {rendered} file(s) to {out}.")
    return 0


def default_overlay_path(skill: Path, root: Path) -> Path:
    rel = skill.relative_to(root)
    department = rel.parts[0]
    return root / ".overlays" / department / f"{skill.name}.local.yml"


def load_local_overlay(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data: dict[str, object] = {}
    current: dict[str, object] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0 and stripped.endswith(":"):
            key = stripped[:-1].strip()
            current = {}
            data[key] = current
            continue
        if indent == 0 and ":" in stripped:
            key, value = stripped.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
            current = None
            continue
        if indent == 2 and current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip().strip('"').strip("'")
            continue
        raise SkillctlError(f"{path}: unsupported overlay YAML shape: {raw}")
    return data


def dump_local_overlay(data: dict[str, object]) -> str:
    lines: list[str] = []
    for key in sorted(data):
        value = data[key]
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for nested_key in sorted(value):
                lines.append(f"  {nested_key}: {json.dumps(str(value[nested_key]))}")
        else:
            lines.append(f"{key}: {json.dumps(str(value))}")
    return "\n".join(lines) + ("\n" if lines else "")


def set_overlay_value(data: dict[str, object], dotted_key: str, value: str) -> None:
    parts = dotted_key.split(".")
    if len(parts) == 1:
        data[parts[0]] = value
        return
    if len(parts) != 2:
        raise SkillctlError("--set currently supports one or two key levels, for example company.name=value")
    current = data.setdefault(parts[0], {})
    if not isinstance(current, dict):
        current = {}
        data[parts[0]] = current
    current[parts[1]] = value


def personalize_init(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    skill = root_path(args.skill) if Path(args.skill).is_absolute() else root / args.skill
    if not (skill / "SKILL.md").exists():
        raise SkillctlError(f"skill not found: {skill}")
    out = root_path(args.out) if args.out else default_overlay_path(skill, root)
    source = skill / "personalize.example.yml"
    if source.exists():
        content = source.read_text(encoding="utf-8")
    else:
        content = (
            "company:\n"
            "  name: \"{{COMPANY_NAME}}\"\n"
            "  website: \"{{COMPANY_WEBSITE}}\"\n"
            "  tone: \"{{COMPANY_TONE}}\"\n"
            "user:\n"
            "  name: \"{{USER_NAME}}\"\n"
            "  role: \"{{USER_ROLE}}\"\n"
        )
    if args.dry_run:
        print(f"would write {relative_to_root(out, root)}")
        print(content, end="" if content.endswith("\n") else "\n")
        return 0
    if out.exists() and not args.force:
        raise SkillctlError(f"overlay already exists: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(f"initialized {relative_to_root(out, root)}")
    return 0


def personalize_update(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    skill = root_path(args.skill) if Path(args.skill).is_absolute() else root / args.skill
    if not (skill / "SKILL.md").exists():
        raise SkillctlError(f"skill not found: {skill}")
    overlay = root_path(args.overlay) if args.overlay else default_overlay_path(skill, root)
    data = load_local_overlay(overlay)
    for item in args.set:
        if "=" not in item:
            raise SkillctlError(f"expected key=value for --set: {item}")
        key, value = item.split("=", 1)
        set_overlay_value(data, key.strip(), value.strip())
    rendered = dump_local_overlay(data)
    if args.dry_run:
        print(f"would write {relative_to_root(overlay, root)}")
        print(rendered, end="")
        return 0
    overlay.parent.mkdir(parents=True, exist_ok=True)
    overlay.write_text(rendered, encoding="utf-8")
    print(f"updated {relative_to_root(overlay, root)}")
    return 0


def write_patch_report(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    changed_files = patch_changed_files(root, args.base, args.head)
    classifications = [classify_path(root / file, root) for file in changed_files]
    blocked = [item for item in classifications if item.kind in {"local-private", "generated-runtime"}]
    if blocked:
        for item in blocked:
            print(f"blocked: {item.path}\t{item.kind}\t{item.reason}", file=sys.stderr)
        raise SkillctlError("refusing to propose upstream bundle with private/runtime files")

    out_dir = root / ".skill-improvements"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")[:60] or "skill-improvement"
    base = out_dir / f"{stamp}-{slug}"
    base.mkdir(parents=True, exist_ok=True)

    diff = run(["git", "diff", args.base, args.head], cwd=root, check=False).stdout if args.base != args.head else run(["git", "diff"], cwd=root, check=False).stdout
    (base / "changes.patch").write_text(diff, encoding="utf-8")
    kinds = {item.kind for item in classifications}
    if not kinds:
        overall = "upstream-safe"
    elif len(kinds) == 1:
        overall = next(iter(kinds))
    else:
        overall = "mixed"
    report = {
        "title": args.title,
        "target": args.target or "",
        "summary": args.summary or "Generated upstream improvement patch bundle.",
        "classification": overall,
        "private_data_detected": False,
        "changed_files": changed_files,
        "validation": ["skillctl diff classification passed"],
        "risk": args.risk,
    }
    (base / "improvement-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (base / "README.md").write_text(
        f"# {args.title}\n\nReview `changes.patch` and `improvement-report.json` before opening an upstream PR.\n",
        encoding="utf-8",
    )
    print(base.relative_to(root).as_posix())
    return 0


def propose_upstream(args: argparse.Namespace) -> int:
    if args.mode == "patch":
        return write_patch_report(args)
    if not shutil.which("gh"):
        raise SkillctlError("gh is required for --mode pr; use --mode patch instead")
    branch = args.branch or f"auto-improve/{re.sub(r'[^a-z0-9]+', '-', args.title.lower()).strip('-')[:50]}"
    run(["git", "switch", "-c", branch], cwd=root_path(args.root))
    run(["gh", "pr", "create", "--repo", CANONICAL_REPO, "--base", "main", "--head", branch, "--title", args.title, "--body", args.summary or args.title], cwd=root_path(args.root))
    return 0


def target_root(agent: str) -> Path:
    home = Path.home()
    if agent == "codex":
        return Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser() / "skills"
    if agent == "cursor":
        return home / ".cursor" / "skills"
    if agent == "openclaw":
        return home / ".openclaw" / "skills"
    if agent == "claude-code":
        return home / ".claude" / "skills"
    raise SkillctlError(f"unsupported agent: {agent}")


def install_skill(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    skill = root / args.skill
    if not (skill / "SKILL.md").exists():
        raise SkillctlError(f"skill not found: {skill}")
    destination = root_path(args.dest) if args.dest else target_root(args.agent) / skill.name
    if args.mode == "symlink":
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            if not args.force:
                raise SkillctlError(f"destination exists: {destination}")
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()
        destination.symlink_to(skill.resolve(), target_is_directory=True)
    else:
        if destination.exists():
            if not args.force:
                raise SkillctlError(f"destination exists: {destination}")
            shutil.rmtree(destination)
        shutil.copytree(skill, destination)

    lock = destination.parent / ".skill-lock.yml"
    lock.write_text(
        f"skills:\n  {skill.name}:\n    repo: {CANONICAL_REPO}\n    path: {relative_to_root(skill, root)}\n    install_mode: {args.mode}\n    agent: {args.agent}\n",
        encoding="utf-8",
    )
    print(f"installed {relative_to_root(skill, root)} -> {destination}")
    return 0


def update_installs(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    run(["git", "pull", "--ff-only"], cwd=root)
    print("Updated canonical clone. Re-render overlays and reload runtime agents as needed.")
    return 0


def structure_init(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    departments = department_dirs(root)
    for department in departments:
        mcp = department / "mcp.json"
        rules = department / "rules"
        if args.dry_run:
            if not mcp.exists():
                print(f"would write {relative_to_root(mcp, root)}")
            if not rules.exists():
                print(f"would create {relative_to_root(rules / 'README.md', root)}")
            continue
        if not mcp.exists() or args.force:
            mcp.write_text('{\n  "mcpServers": {}\n}\n', encoding="utf-8")
        rules.mkdir(parents=True, exist_ok=True)
        readme = rules / "README.md"
        if not readme.exists() or args.force:
            readme.write_text(
                f"# {department.name} rules\n\n"
                "Runtime-neutral policy and routing rules for this department plugin.\n",
                encoding="utf-8",
            )
    print(f"Initialized structure files for {len(departments)} department plugin(s).")
    return 0


def structure_check(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    failures: list[str] = []

    for path in (".claude-plugin/marketplace.json", "COMPANY.md", "assets", "scripts", "references"):
        if not (root / path).exists():
            failures.append(f"missing root path: {path}")
    if (root / "hooks").exists():
        failures.append("root hooks/ is forbidden; hook entrypoints must live inside skills")

    departments = department_dirs(root)
    if not departments:
        failures.append("no department plugins found")

    for department in departments:
        rel = relative_to_root(department, root)
        for file_path in DEPARTMENT_REQUIRED_FILES:
            if not (department / file_path).exists():
                failures.append(f"{rel}: missing {file_path}")
        for dir_path in DEPARTMENT_REQUIRED_DIRS:
            if not (department / dir_path).is_dir():
                failures.append(f"{rel}: missing {dir_path}/")
        for forbidden in ("hooks", "scripts"):
            if (department / forbidden).exists():
                failures.append(f"{rel}: {forbidden}/ is forbidden at department plugin root")

    for path in root.glob("*/.claude-plugin/*"):
        if path.name != "plugin.json":
            failures.append(f"{relative_to_root(path, root)}: unexpected file inside department .claude-plugin")
    for path in (root / ".claude-plugin").glob("*") if (root / ".claude-plugin").exists() else []:
        if path.name != "marketplace.json":
            failures.append(f"{relative_to_root(path, root)}: unexpected file inside root .claude-plugin")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print(f"Validated structure for {len(departments)} department plugin(s).")
    return 0


def conflicts_check(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    failures: list[str] = []

    skill_files = sorted(root.glob("*/skills/*/SKILL.md"))
    command_files = sorted(path for path in root.glob("*/commands/*.md") if path.name != "README.md")
    agent_files = sorted(path for path in root.glob("*/agents/*.md") if path.name != "README.md")

    skill_paths_by_name: dict[str, list[Path]] = {}
    for skill_file in skill_files:
        name = frontmatter_field(skill_file, "name") or skill_file.parent.name
        skill_paths_by_name.setdefault(name, []).append(skill_file.parent)
    skill_names = set(skill_paths_by_name)

    command_paths_by_slug: dict[str, list[Path]] = {}
    command_paths_by_name: dict[str, list[Path]] = {}
    for command_file in command_files:
        command_text = command_file.read_text(encoding="utf-8")
        name = frontmatter_field(command_file, "name")
        if not name:
            failures.append(f"{relative_to_root(command_file, root)}: missing command frontmatter name")
            continue
        if public_name_slug(name) != command_file.stem:
            failures.append(
                f"{relative_to_root(command_file, root)}: command name `{name}` must normalize to file stem `{command_file.stem}`"
            )
        allowed_tools = frontmatter_field(command_file, "allowed-tools")
        if allowed_tools and not (allowed_tools.startswith("[") and allowed_tools.endswith("]")):
            failures.append(f"{relative_to_root(command_file, root)}: allowed-tools must use bracketed list syntax")
        if "Task" in allowed_tools:
            failures.append(f"{relative_to_root(command_file, root)}: allowed-tools must use `Agent`, not stale `Task`")
        command_body = command_text.split("---", 2)[2] if command_text.startswith("---\n") else command_text
        if COMMAND_AGENT_TOOL_RE.search(command_body) and "Agent" not in allowed_tools:
            failures.append(f"{relative_to_root(command_file, root)}: command references agents but allowed-tools does not include `Agent`")
        command_paths_by_slug.setdefault(command_file.stem, []).append(command_file)
        command_paths_by_name.setdefault(name, []).append(command_file)

    agent_paths_by_slug: dict[str, list[Path]] = {}
    agent_paths_by_name: dict[str, list[Path]] = {}
    for agent_file in agent_files:
        name = frontmatter_field(agent_file, "name")
        if not name:
            failures.append(f"{relative_to_root(agent_file, root)}: missing agent frontmatter name")
            continue
        if public_name_slug(name) != agent_file.stem:
            failures.append(
                f"{relative_to_root(agent_file, root)}: agent name `{name}` must normalize to file stem `{agent_file.stem}`"
            )
        for key in ("tools", "disallowedTools"):
            for tool in sorted(frontmatter_tool_names(frontmatter_field(agent_file, key))):
                if tool not in VALID_TOOL_NAMES:
                    failures.append(f"{relative_to_root(agent_file, root)}: {key} references unknown tool `{tool}`")
        agent_paths_by_slug.setdefault(agent_file.stem, []).append(agent_file)
        agent_paths_by_name.setdefault(name, []).append(agent_file)

    append_duplicate_failures(failures, "skill install", skill_paths_by_name, root)
    append_duplicate_failures(failures, "command file", command_paths_by_slug, root)
    append_duplicate_failures(failures, "command public", command_paths_by_name, root)
    append_duplicate_failures(failures, "agent file", agent_paths_by_slug, root)
    append_duplicate_failures(failures, "agent public", agent_paths_by_name, root)

    departments = department_dirs(root)
    department_names = {department.name for department in departments}

    marketplace = root / ".claude-plugin" / "marketplace.json"
    if marketplace.exists():
        marketplace_data = read_json(marketplace, failures, root)
        plugins = marketplace_data.get("plugins", []) if isinstance(marketplace_data, dict) else []
        if not isinstance(plugins, list):
            failures.append(f"{relative_to_root(marketplace, root)}: plugins must be a list")
            plugins = []
        marketplace_names: dict[str, Path] = {}
        for plugin in plugins:
            if not isinstance(plugin, dict):
                failures.append(f"{relative_to_root(marketplace, root)}: plugin entries must be objects")
                continue
            name = str(plugin.get("name", ""))
            source = str(plugin.get("source", ""))
            if not name:
                failures.append(f"{relative_to_root(marketplace, root)}: plugin entry is missing name")
                continue
            if name in marketplace_names:
                failures.append(f"{relative_to_root(marketplace, root)}: duplicate marketplace plugin `{name}`")
            marketplace_names[name] = root / name
            if name not in department_names:
                failures.append(f"{relative_to_root(marketplace, root)}: marketplace plugin `{name}` has no department directory")
            if source != f"./{name}":
                failures.append(f"{relative_to_root(marketplace, root)}: marketplace plugin `{name}` source must be `./{name}`")
            profile = root / name / "profile.yaml"
            if profile.exists():
                profile_version = profile_scalar(profile, "version")
                if profile_version and str(plugin.get("version", "")) != profile_version:
                    failures.append(
                        f"{relative_to_root(marketplace, root)}: marketplace plugin `{name}` version must match {relative_to_root(profile, root)}"
                    )
        for department in sorted(department_names - set(marketplace_names)):
            failures.append(f"{relative_to_root(marketplace, root)}: missing marketplace entry for department `{department}`")

    for department in departments:
        profile = department / "profile.yaml"
        rel_department = relative_to_root(department, root)
        profile_slug = profile_scalar(profile, "slug")
        profile_version = profile_scalar(profile, "version")
        if profile_slug != department.name:
            failures.append(f"{relative_to_root(profile, root)}: slug `{profile_slug}` must match department `{department.name}`")

        team_file = department / "TEAM.md"
        if team_file.exists():
            team_lines = team_file.read_text(encoding="utf-8").splitlines()
            expected_heading = f"# {department_display_name(department)} Team"
            actual_heading = next((line.strip() for line in team_lines if line.strip()), "")
            if actual_heading != expected_heading:
                failures.append(
                    f"{relative_to_root(team_file, root)}: first heading must be `{expected_heading}`"
                )
            team_text = "\n".join(team_lines)
            for member in parse_profile_list(profile, "team"):
                if member not in team_text:
                    failures.append(
                        f"{relative_to_root(team_file, root)}: missing profile team member `{member}`"
                    )

        claude_plugin = department / ".claude-plugin" / "plugin.json"
        if claude_plugin.exists():
            data = read_json(claude_plugin, failures, root)
            if isinstance(data, dict):
                if data.get("name") != department.name:
                    failures.append(f"{relative_to_root(claude_plugin, root)}: name must match department `{department.name}`")
                if profile_version and data.get("version") != profile_version:
                    failures.append(f"{relative_to_root(claude_plugin, root)}: version must match {relative_to_root(profile, root)}")

        codex_plugin = department / ".codex-plugin" / "plugin.json"
        if codex_plugin.exists():
            data = read_json(codex_plugin, failures, root)
            if isinstance(data, dict):
                if data.get("name") != department.name:
                    failures.append(f"{relative_to_root(codex_plugin, root)}: name must match department `{department.name}`")
                if profile_version and data.get("version") != profile_version:
                    failures.append(f"{relative_to_root(codex_plugin, root)}: version must match {relative_to_root(profile, root)}")
                if data.get("skills") != "./skills/":
                    failures.append(f"{relative_to_root(codex_plugin, root)}: skills must be `./skills/`")

        cursor_plugin = department / ".cursor-plugin" / "plugin.json"
        if cursor_plugin.exists():
            data = read_json(cursor_plugin, failures, root)
            if isinstance(data, dict):
                if data.get("name") != department.name:
                    failures.append(f"{relative_to_root(cursor_plugin, root)}: name must match department `{department.name}`")
                if profile_version and data.get("version") != profile_version:
                    failures.append(f"{relative_to_root(cursor_plugin, root)}: version must match {relative_to_root(profile, root)}")

        mcp = department / "mcp.json"
        if mcp.exists():
            data = read_json(mcp, failures, root)
            if isinstance(data, dict) and not isinstance(data.get("mcpServers", {}), dict):
                failures.append(f"{relative_to_root(mcp, root)}: mcpServers must be an object")

        skill_entries = set(parse_profile_list(profile, "skills"))
        skill_dirs_in_department = {
            path.name for path in (department / "skills").iterdir() if path.is_dir() and (path / "SKILL.md").exists()
        }
        for name in sorted(skill_entries - skill_dirs_in_department):
            failures.append(f"{relative_to_root(profile, root)}: skill `{name}` is listed but {rel_department}/skills/{name}/SKILL.md is missing")
        for name in sorted(skill_dirs_in_department - skill_entries):
            failures.append(f"{relative_to_root(profile, root)}: skill `{name}` exists but is not listed")

        command_entries = set(parse_profile_list(profile, "commands"))
        command_stems = {path.stem for path in (department / "commands").glob("*.md") if path.name != "README.md"}
        for name in sorted(command_entries - command_stems):
            failures.append(f"{relative_to_root(profile, root)}: command `{name}` is listed but {rel_department}/commands/{name}.md is missing")
        for name in sorted(command_stems - command_entries):
            failures.append(f"{relative_to_root(profile, root)}: command `{name}` exists but is not listed")

        agent_entries = set(parse_profile_list(profile, "agents"))
        agent_stems = {path.stem for path in (department / "agents").glob("*.md") if path.name != "README.md"}
        for name in sorted(agent_entries - agent_stems):
            failures.append(f"{relative_to_root(profile, root)}: agent `{name}` is listed but {rel_department}/agents/{name}.md is missing")
        for name in sorted(agent_stems - agent_entries):
            failures.append(f"{relative_to_root(profile, root)}: agent `{name}` exists but is not listed")

    installable_external_names = external_skill_names(root, failures)
    reference_external_names = external_source_names(root, failures)
    for name in sorted(installable_external_names & reference_external_names):
        failures.append(f"external source `{name}` conflicts with an installable external skill")
    external_names = installable_external_names | reference_external_names
    for command_file in command_files:
        for name in sorted(command_skill_refs(command_file)):
            if name not in skill_names and name not in external_names:
                failures.append(f"{relative_to_root(command_file, root)}: command references unknown skill `{name}`")

    for markdown_file in [*skill_files, *command_files]:
        for line, name in explicit_external_skill_refs(markdown_file):
            if name not in external_names:
                failures.append(
                    f"{relative_to_root(markdown_file, root)}:{line}: references unknown external skill `{name}`"
                )

    for agent_file in agent_files:
        for name in sorted(agent_primary_skill_refs(agent_file)):
            if name not in skill_names:
                failures.append(f"{relative_to_root(agent_file, root)}: agent references unknown primary skill `{name}`")
        known_commands = set(command_paths_by_slug) | set(command_paths_by_name)
        for name in sorted(agent_command_refs(agent_file)):
            if name not in known_commands:
                failures.append(f"{relative_to_root(agent_file, root)}: agent references unknown command `{name}`")
        for name in sorted(agent_spawned_by_command_refs(agent_file)):
            if name not in known_commands:
                failures.append(f"{relative_to_root(agent_file, root)}: agent spawned-by reference points at unknown command `{name}`")

    skill_paths = {relative_to_root(skill_file.parent, root) for skill_file in skill_files}
    discovered_skill_roots = {path.split("/", 1)[0] for path in skill_paths}
    skill_path_roots = department_names | discovered_skill_roots | RETIRED_SKILL_PATH_ROOTS
    for readme in sorted(root.glob("*/skills/*/README.md")):
        for ref in sorted(local_skill_path_refs(readme, skill_path_roots)):
            if ref not in skill_paths:
                failures.append(f"{relative_to_root(readme, root)}: README references missing skill path `{ref}`")

    for markdown_file in active_markdown_link_files(root, skill_files):
        for ref in sorted(local_skill_path_refs(markdown_file, skill_path_roots)):
            if ref not in skill_paths:
                failures.append(
                    f"{relative_to_root(markdown_file, root)}: Markdown references missing skill path `{ref}`"
                )
        for line, raw, target in local_markdown_links(markdown_file):
            if not target.exists():
                failures.append(
                    f"{relative_to_root(markdown_file, root)}:{line}: Markdown references missing local link `{raw}`"
                )

    for skill_file in skill_files:
        skill_name = frontmatter_field(skill_file, "name") or skill_file.parent.name
        direct_agents = skill_file.parent / "agents"
        if not direct_agents.exists():
            continue
        for agent_meta in sorted(path for path in direct_agents.iterdir() if path.is_file()):
            try:
                tokens = set(DOLLAR_SKILL_REF_RE.findall(agent_meta.read_text(encoding="utf-8")))
            except OSError:
                continue
            for token in sorted(tokens):
                if token != skill_name:
                    failures.append(
                        f"{relative_to_root(agent_meta, root)}: direct skill agent prompt references `${token}` instead of `${skill_name}`"
                    )

    chain_map = root / "skills-chaining-map.md"
    if chain_map.exists():
        internal_rows = parse_internal_chain_rows(chain_map)
        owner_by_child: dict[str, str] = {}
        for parent, row in sorted(internal_rows.items()):
            line_number = int(row["line"])
            if parent not in skill_names:
                failures.append(f"{relative_to_root(chain_map, root)}:{line_number}: chain map references unknown parent skill `{parent}`")
            for child in row["children"]:
                if not isinstance(child, str):
                    continue
                if child not in skill_names:
                    failures.append(f"{relative_to_root(chain_map, root)}:{line_number}: chain map references unknown child skill `{child}`")
                    continue
                existing_parent = owner_by_child.get(child)
                if existing_parent and existing_parent != parent:
                    failures.append(
                        f"{relative_to_root(chain_map, root)}:{line_number}: child skill `{child}` is owned by both `{existing_parent}` and `{parent}`"
                    )
                    continue
                owner_by_child[child] = parent

        def validate_internal_ref(ref: str, location: str) -> None:
            if not is_skill_ref_token(ref):
                return
            parts = ref.split("/")
            for name in parts:
                if name not in skill_names:
                    failures.append(f"{location}: references unknown skill `{name}`")
                    return
            if len(parts) == 2:
                parent, child = parts
                if owner_by_child.get(child) != parent:
                    failures.append(
                        f"{location}: invalid parent/child chain `{ref}`; `{child}` is owned by `{owner_by_child.get(child, 'no parent')}`"
                    )

        for parent, row in sorted(internal_rows.items()):
            line_number = int(row["line"])
            for ref in row["chains"]:
                if isinstance(ref, str):
                    validate_internal_ref(ref, f"{relative_to_root(chain_map, root)}:{line_number}")

            parent_paths = skill_paths_by_name.get(parent, [])
            if not parent_paths:
                continue
            skill_file = parent_paths[0] / "SKILL.md"
            expected_children = list(row["children"])
            actual_children = skill_children_section(skill_file)
            if actual_children != expected_children:
                failures.append(
                    f"{relative_to_root(skill_file, root)}: Children section {actual_children} does not match {relative_to_root(chain_map, root)} row {expected_children}"
                )
            expected_chains = list(row["chains"])
            actual_chains = direct_chain_rule_list(skill_file)
            if actual_chains != expected_chains:
                failures.append(
                    f"{relative_to_root(skill_file, root)}: Chain Rules {actual_chains} do not match {relative_to_root(chain_map, root)} row {expected_chains}"
                )

        for skill_file in skill_files:
            for line_number, ref in chain_rule_refs(skill_file):
                if "/" in ref:
                    validate_internal_ref(ref, f"{relative_to_root(skill_file, root)}:{line_number}")
                elif ref not in skill_names and ref not in external_names:
                    failures.append(f"{relative_to_root(skill_file, root)}:{line_number}: references unknown skill `{ref}`")

        in_external = False
        in_internal = False
        for raw in chain_map.read_text(encoding="utf-8").splitlines():
            if raw.startswith("## External Chains"):
                in_external = True
                in_internal = False
                continue
            if raw.startswith("## Chains"):
                in_external = False
                in_internal = True
                continue
            if raw.startswith("## ") and not raw.startswith("## External Chains") and not raw.startswith("## Chains"):
                in_external = False
                in_internal = False
            if not raw.startswith("| `"):
                continue
            cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
            if in_external and len(cells) >= 2:
                for name in BACKTICK_REF_RE.findall(cells[0]):
                    if name not in skill_names:
                        failures.append(f"{relative_to_root(chain_map, root)}: external chain references unknown internal skill `{name}`")
                for name in BACKTICK_REF_RE.findall(cells[1]):
                    if name not in external_names:
                        failures.append(f"{relative_to_root(chain_map, root)}: external chain references unknown external skill `{name}`")
            elif in_internal:
                for ref in BACKTICK_REF_RE.findall(raw):
                    if is_skill_ref_token(ref):
                        validate_internal_ref(ref, relative_to_root(chain_map, root))

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print(f"Validated conflicts for {len(skill_files)} skill(s), {len(command_files)} command(s), and {len(agent_files)} agent(s).")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Agent Company skill provenance, overlays, and improvement proposals.")
    sub = parser.add_subparsers(dest="command", required=True)

    meta = sub.add_parser("meta")
    meta_sub = meta.add_subparsers(dest="meta_command", required=True)
    meta_generate_parser = meta_sub.add_parser("generate")
    meta_generate_parser.add_argument("--root", default=".")
    meta_generate_parser.add_argument("--force", action="store_true")
    meta_generate_parser.add_argument("--dry-run", action="store_true")
    meta_generate_parser.set_defaults(func=meta_generate)
    meta_check_parser = meta_sub.add_parser("check")
    meta_check_parser.add_argument("--root", default=".")
    meta_check_parser.add_argument("--require-pilot", action="store_true")
    meta_check_parser.add_argument("--require-all", action="store_true")
    meta_check_parser.set_defaults(func=meta_check)

    structure = sub.add_parser("structure")
    structure_sub = structure.add_subparsers(dest="structure_command", required=True)
    structure_init_parser = structure_sub.add_parser("init")
    structure_init_parser.add_argument("--root", default=".")
    structure_init_parser.add_argument("--force", action="store_true")
    structure_init_parser.add_argument("--dry-run", action="store_true")
    structure_init_parser.set_defaults(func=structure_init)
    structure_check_parser = structure_sub.add_parser("check")
    structure_check_parser.add_argument("--root", default=".")
    structure_check_parser.set_defaults(func=structure_check)

    conflicts = sub.add_parser("conflicts")
    conflicts_sub = conflicts.add_subparsers(dest="conflicts_command", required=True)
    conflicts_check_parser = conflicts_sub.add_parser("check")
    conflicts_check_parser.add_argument("--root", default=".")
    conflicts_check_parser.set_defaults(func=conflicts_check)

    trace = sub.add_parser("trace-origin")
    trace.add_argument("paths", nargs="+")
    trace.add_argument("--root", default=".")
    trace.set_defaults(func=trace_origin)

    diff = sub.add_parser("diff-classify")
    diff.add_argument("--root", default=".")
    diff.add_argument("--base", default="origin/main")
    diff.add_argument("--head", default="HEAD")
    diff.add_argument("--file", action="append")
    diff.add_argument("--fail-on-private", action="store_true")
    diff.set_defaults(func=diff_classify)

    render = sub.add_parser("render-overlays")
    render.add_argument("--root", default=".")
    render.add_argument("--skill", required=True)
    render.add_argument("--values", required=True)
    render.add_argument("--out", required=True)
    render.set_defaults(func=render_overlays)

    personalize = sub.add_parser("personalize")
    personalize_sub = personalize.add_subparsers(dest="personalize_command", required=True)
    personalize_init_parser = personalize_sub.add_parser("init")
    personalize_init_parser.add_argument("--root", default=".")
    personalize_init_parser.add_argument("--skill", required=True)
    personalize_init_parser.add_argument("--out")
    personalize_init_parser.add_argument("--force", action="store_true")
    personalize_init_parser.add_argument("--dry-run", action="store_true")
    personalize_init_parser.set_defaults(func=personalize_init)
    personalize_update_parser = personalize_sub.add_parser("update")
    personalize_update_parser.add_argument("--root", default=".")
    personalize_update_parser.add_argument("--skill", required=True)
    personalize_update_parser.add_argument("--overlay")
    personalize_update_parser.add_argument("--set", action="append", default=[])
    personalize_update_parser.add_argument("--dry-run", action="store_true")
    personalize_update_parser.set_defaults(func=personalize_update)
    personalize_render_parser = personalize_sub.add_parser("render")
    personalize_render_parser.add_argument("--root", default=".")
    personalize_render_parser.add_argument("--skill", required=True)
    personalize_render_parser.add_argument("--values", required=True)
    personalize_render_parser.add_argument("--out", required=True)
    personalize_render_parser.set_defaults(func=render_overlays)

    propose = sub.add_parser("propose-upstream")
    propose.add_argument("--root", default=".")
    propose.add_argument("--mode", choices=["patch", "pr"], default="patch")
    propose.add_argument("--title", required=True)
    propose.add_argument("--summary")
    propose.add_argument("--target")
    propose.add_argument("--risk", choices=["low", "medium", "high"], default="low")
    propose.add_argument("--base", default="origin/main")
    propose.add_argument("--head", default="HEAD")
    propose.add_argument("--branch")
    propose.set_defaults(func=propose_upstream)

    install = sub.add_parser("install")
    install.add_argument("skill")
    install.add_argument("--root", default=".")
    install.add_argument("--agent", choices=["codex", "cursor", "openclaw", "claude-code"], default="codex")
    install.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    install.add_argument("--dest")
    install.add_argument("--force", action="store_true")
    install.set_defaults(func=install_skill)

    update = sub.add_parser("update")
    update.add_argument("--root", default=".")
    update.set_defaults(func=update_installs)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (SkillctlError, subprocess.CalledProcessError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
