#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent


def _default_asset(name: str, source_path: Path) -> Path:
    """Prefer assets shipped beside the project-local runtime helper."""

    runtime_asset = SCRIPT_DIR / name
    return runtime_asset if runtime_asset.exists() else source_path


DEFAULT_REGISTRY = _default_asset(
    "external-skills.yaml", ROOT / "references" / "external-skills.yaml"
)
DEFAULT_CHAIN_MAP = _default_asset(
    "skills-chaining-map.md", ROOT / "skills-chaining-map.md"
)
BACKTICK_REF_RE = re.compile(r"`([^`]+)`")
HEX_DIGEST_RE = re.compile(r"[0-9a-f]{64}")
COMPONENT_GRAPH_NAME = "component-graph.json"
SUPPORT_LOCK_NAME = ".plugin-support-lock.json"


@dataclass(frozen=True)
class ExternalSkill:
    skill_id: str
    owner: str
    repo: str
    ref: str
    path: str
    install_name: str
    homepage: str
    domain: str


@dataclass(frozen=True)
class ProjectRuntimeState:
    agents_root: Path
    graph_path: Path
    support_lock_path: Path
    graph_text: str
    support_lock_text: str
    graph: dict[str, object]
    support_lock: dict[str, object]


def _clean_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, ExternalSkill]:
    """Parse the constrained YAML shape used by references/external-skills.yaml."""
    if not path.exists():
        raise FileNotFoundError(f"registry not found: {path}")

    skills: dict[str, dict[str, str]] = {}
    current: str | None = None
    in_skills = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "skills:":
            in_skills = True
            continue
        if not in_skills:
            continue
        if line.startswith("  ") and not line.startswith("    ") and stripped.endswith(":"):
            current = stripped[:-1]
            skills[current] = {}
            continue
        if line.startswith("    ") and current and ":" in stripped:
            key, value = stripped.split(":", 1)
            skills[current][key] = _clean_value(value)
            continue
        raise ValueError(f"unsupported registry line: {raw_line}")

    required = {"owner", "repo", "ref", "path", "install_name", "homepage", "domain"}
    parsed: dict[str, ExternalSkill] = {}
    for skill_id, data in skills.items():
        missing = sorted(required - set(data))
        if missing:
            raise ValueError(f"{skill_id}: missing required field(s): {', '.join(missing)}")
        parsed[skill_id] = ExternalSkill(skill_id=skill_id, **data)
    return parsed


def chain_skill_ids(path: Path, chain_ids: list[str]) -> list[str]:
    """Return installable ids named by the External Chains table for internal skills."""
    if not chain_ids:
        return []
    if not path.exists():
        raise FileNotFoundError(f"chain map not found: {path}")

    wanted = set(chain_ids)
    found: set[str] = set()
    selected: list[str] = []
    in_external = False

    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## External Chains"):
            in_external = True
            continue
        if raw.startswith("## ") and not raw.startswith("## External Chains"):
            if in_external:
                break
            continue
        if not in_external or not raw.startswith("| `"):
            continue

        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        internal_names = BACKTICK_REF_RE.findall(cells[0])
        if not any(name in wanted for name in internal_names):
            continue
        found.update(name for name in internal_names if name in wanted)
        selected.extend(BACKTICK_REF_RE.findall(cells[1]))

    missing = sorted(wanted - found)
    if missing:
        raise ValueError(f"unknown internal chain(s): {', '.join(missing)}")
    return list(dict.fromkeys(selected))


def selected_entries(
    registry: dict[str, ExternalSkill],
    all_skills: bool,
    skill_ids: list[str],
    chain_ids: list[str] | None = None,
    chain_map: Path = DEFAULT_CHAIN_MAP,
) -> list[ExternalSkill]:
    if all_skills:
        if skill_ids or chain_ids:
            raise ValueError("use --all without --skill or --chain")
        return [registry[key] for key in sorted(registry)]

    selected_ids = list(skill_ids)
    selected_ids.extend(
        skill_id
        for skill_id in chain_skill_ids(chain_map, chain_ids or [])
        if skill_id in registry
    )
    selected_ids = list(dict.fromkeys(selected_ids))
    if not selected_ids:
        raise ValueError("select at least one skill with --skill, --chain, or use --all")

    unknown = [skill_id for skill_id in selected_ids if skill_id not in registry]
    if unknown:
        known = ", ".join(sorted(registry))
        raise ValueError(f"unknown external skill(s): {', '.join(unknown)}\nknown: {known}")
    return [registry[skill_id] for skill_id in selected_ids]


def target_root(agent: str, dest: str | None) -> Path:
    if dest:
        return Path(dest).expanduser().resolve()

    home = Path.home()
    if agent == "codex":
        base = Path(os.environ.get("CODEX_HOME", home / ".codex"))
        return (base / "skills").expanduser().resolve()
    if agent == "claude":
        return (home / ".claude" / "skills").resolve()
    if agent == "cursor":
        return (home / ".cursor" / "skills").resolve()
    if agent == "project":
        return (Path.cwd() / ".agents" / "skills").resolve()
    raise ValueError(f"unsupported agent: {agent}")


def _sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _project_agents_root(skill_root: Path) -> Path:
    root = skill_root.expanduser().resolve()
    if root.name != "skills" or root.parent.name != ".agents":
        raise ValueError(
            "--agent project must target a project's .agents/skills directory "
            "so component-graph.json can be refreshed"
        )
    return root.parent


def _read_project_runtime_state(skill_root: Path) -> ProjectRuntimeState:
    agents_root = _project_agents_root(skill_root)
    graph_path = agents_root / COMPONENT_GRAPH_NAME
    support_lock_path = agents_root / SUPPORT_LOCK_NAME
    for label, path in (
        ("component graph", graph_path),
        ("managed support lock", support_lock_path),
    ):
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"project {label} is missing or unsafe: {path}")

    try:
        graph_text = graph_path.read_text(encoding="utf-8")
        graph = json.loads(graph_text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid project component graph {graph_path}: {exc}") from exc
    if (
        not isinstance(graph, dict)
        or graph.get("artifact_kind") != "component-relationship-graph"
        or graph.get("contract") != "references/component-graph.json"
        or not isinstance(graph.get("nodes"), list)
    ):
        raise ValueError(f"unsupported project component graph: {graph_path}")

    try:
        support_lock_text = support_lock_path.read_text(encoding="utf-8")
        support_lock = json.loads(support_lock_text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"invalid managed support lock {support_lock_path}: {exc}"
        ) from exc
    files = support_lock.get("files") if isinstance(support_lock, dict) else None
    if (
        not isinstance(support_lock, dict)
        or support_lock.get("schema_version") != 1
        or not isinstance(files, dict)
    ):
        raise ValueError(f"unsupported managed support lock: {support_lock_path}")
    recorded_digest = files.get(COMPONENT_GRAPH_NAME)
    if not isinstance(recorded_digest, str) or not HEX_DIGEST_RE.fullmatch(
        recorded_digest
    ):
        raise ValueError(
            f"managed support lock has no valid {COMPONENT_GRAPH_NAME} digest: "
            f"{support_lock_path}"
        )
    if _sha256_text(graph_text) != recorded_digest:
        raise ValueError(
            f"refusing to overwrite locally modified managed support file: {graph_path}"
        )

    return ProjectRuntimeState(
        agents_root=agents_root,
        graph_path=graph_path,
        support_lock_path=support_lock_path,
        graph_text=graph_text,
        support_lock_text=support_lock_text,
        graph=graph,
        support_lock=support_lock,
    )


def _stage_text(path: Path, content: str) -> Path:
    descriptor, raw_temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=str(path.parent)
    )
    temporary = Path(raw_temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.chmod(path.stat().st_mode & 0o777)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise
    return temporary


def _replace_runtime_pair(
    state: ProjectRuntimeState, graph_text: str, support_lock_text: str
) -> None:
    graph_temporary = _stage_text(state.graph_path, graph_text)
    lock_temporary = _stage_text(state.support_lock_path, support_lock_text)
    graph_backup = _stage_text(state.graph_path, state.graph_text)
    lock_backup = _stage_text(state.support_lock_path, state.support_lock_text)
    graph_replaced = False
    lock_replaced = False
    try:
        os.replace(graph_temporary, state.graph_path)
        graph_replaced = True
        os.replace(lock_temporary, state.support_lock_path)
        lock_replaced = True
    except OSError:
        if lock_replaced:
            os.replace(lock_backup, state.support_lock_path)
        if graph_replaced:
            os.replace(graph_backup, state.graph_path)
        raise
    finally:
        for temporary in (
            graph_temporary,
            lock_temporary,
            graph_backup,
            lock_backup,
        ):
            if temporary and temporary.exists():
                temporary.unlink()


def refresh_project_runtime(skill_root: Path) -> bool:
    """Refresh external availability and the graph's managed-support digest."""

    state = _read_project_runtime_state(skill_root)
    skill_root = state.agents_root / "skills"
    nodes = state.graph["nodes"]
    assert isinstance(nodes, list)
    changed = False
    for raw_node in nodes:
        if not isinstance(raw_node, dict):
            raise ValueError(f"invalid node in project component graph: {state.graph_path}")
        node_id = raw_node.get("id")
        if not isinstance(node_id, str) or not node_id.startswith("external-skill:"):
            continue
        install_name = raw_node.get("install_name")
        installable = raw_node.get("installable") is not False
        if not installable or not isinstance(install_name, str) or not install_name:
            # Reference-only external sources are graph relationships, not
            # install targets. They intentionally have no install_name and
            # must never become available from an unrelated local directory.
            installed = False
        else:
            installed = (skill_root / install_name / "SKILL.md").is_file()
        if raw_node.get("installed") is not installed:
            raw_node["installed"] = installed
            changed = True

    if not changed:
        return False

    graph_text = json.dumps(
        state.graph, indent=2, sort_keys=False, ensure_ascii=False
    ) + "\n"
    files = state.support_lock["files"]
    assert isinstance(files, dict)
    files[COMPONENT_GRAPH_NAME] = _sha256_text(graph_text)
    support_lock_text = json.dumps(
        state.support_lock, indent=2, sort_keys=False, ensure_ascii=False
    ) + "\n"
    _replace_runtime_pair(state, graph_text, support_lock_text)
    return True


def cache_root() -> Path:
    configured = os.environ.get("PLUGIN_BUNDLE_EXTERNAL_SKILLS_CACHE")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".cache" / "plugin-bundle" / "external-skills").resolve()


def cache_dir_for(skill: ExternalSkill) -> Path:
    safe = "".join(ch if ch.isalnum() else "-" for ch in skill.repo)
    return cache_root() / safe.strip("-")


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def sync_repo(skill: ExternalSkill, *, dry_run: bool) -> Path:
    destination = cache_dir_for(skill)
    if dry_run:
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    if not (destination / ".git").exists():
        run(["git", "clone", "--quiet", "--depth", "1", "--branch", skill.ref, skill.repo, str(destination)])
        return destination

    run(["git", "remote", "set-url", "origin", skill.repo], cwd=destination)
    run(["git", "fetch", "--quiet", "--depth", "1", "origin", skill.ref], cwd=destination)
    run(["git", "-c", "advice.detachedHead=false", "checkout", "--quiet", "--force", "FETCH_HEAD"], cwd=destination)
    return destination


def install_skill(skill: ExternalSkill, root: Path, *, dry_run: bool, force: bool) -> str:
    repo_dir = sync_repo(skill, dry_run=dry_run)
    source = repo_dir / skill.path
    destination = root / skill.install_name

    if dry_run:
        return f"would install {skill.skill_id}: {source} -> {destination}"

    if not (source / "SKILL.md").exists():
        raise FileNotFoundError(f"{skill.skill_id}: SKILL.md not found at {source}")

    root.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not force:
            return f"exists, skipped {skill.skill_id}: {destination} (use --force to refresh)"
        if destination.resolve() == root.resolve() or destination.name != skill.install_name:
            raise ValueError(f"refusing unsafe delete: {destination}")
        shutil.rmtree(destination)

    shutil.copytree(source, destination)
    return f"installed {skill.skill_id}: {destination}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install live external Agent Skills.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="Path to external-skills.yaml")
    parser.add_argument("--all", action="store_true", help="Install every registry entry")
    parser.add_argument("--skill", action="append", default=[], help="External skill id to install")
    parser.add_argument("--chain", action="append", default=[], help="Internal skill id whose external chain should be installed")
    parser.add_argument("--chain-map", default=str(DEFAULT_CHAIN_MAP), help="Path to skills-chaining-map.md")
    parser.add_argument(
        "--agent",
        choices=["codex", "claude", "cursor", "project"],
        default="project",
        help="Destination agent layout (default: project-local .agents/skills)",
    )
    parser.add_argument("--dest", help="Override destination skill directory")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without installing")
    parser.add_argument("--force", action="store_true", help="Replace an existing installed skill")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        registry = load_registry(Path(args.registry).expanduser().resolve())
        skills = selected_entries(
            registry,
            args.all,
            args.skill,
            args.chain,
            Path(args.chain_map).expanduser().resolve(),
        )
        root = target_root(args.agent, args.dest)
        project_install = args.agent == "project" and not args.dry_run
        if project_install:
            _read_project_runtime_state(root)
        runtime_changed = False
        for skill in skills:
            print(install_skill(skill, root, dry_run=args.dry_run, force=args.force))
            if project_install:
                runtime_changed = refresh_project_runtime(root) or runtime_changed
        if runtime_changed:
            print(
                "refreshed external install state: "
                f"{root.parent / COMPONENT_GRAPH_NAME}"
            )
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
