#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "references" / "external-skills.yaml"


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


def selected_entries(
    registry: dict[str, ExternalSkill], all_skills: bool, skill_ids: list[str]
) -> list[ExternalSkill]:
    if all_skills:
        if skill_ids:
            raise ValueError("use either --all or --skill, not both")
        return [registry[key] for key in sorted(registry)]
    if not skill_ids:
        raise ValueError("select at least one skill with --skill or use --all")

    unknown = [skill_id for skill_id in skill_ids if skill_id not in registry]
    if unknown:
        known = ", ".join(sorted(registry))
        raise ValueError(f"unknown external skill(s): {', '.join(unknown)}\nknown: {known}")
    return [registry[skill_id] for skill_id in skill_ids]


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


def cache_root() -> Path:
    configured = os.environ.get("AGENT_COMPANY_EXTERNAL_SKILLS_CACHE")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".cache" / "agent-company" / "external-skills").resolve()


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
    parser.add_argument(
        "--agent",
        choices=["codex", "claude", "cursor", "project"],
        default="codex",
        help="Destination agent layout",
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
        skills = selected_entries(registry, args.all, args.skill)
        root = target_root(args.agent, args.dest)
        for skill in skills:
            print(install_skill(skill, root, dry_run=args.dry_run, force=args.force))
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
