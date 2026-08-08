#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-external-skills.py"
DEFAULT_REGISTRY = ROOT / "references" / "external-skills.yaml"
DEFAULT_CHAIN_MAP = ROOT / "skills-chaining-map.md"


def load_installer():
    spec = importlib.util.spec_from_file_location("external_skill_installer", INSTALLER)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load installer module: {INSTALLER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check external Agent Skill availability.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="Path to external-skills.yaml")
    parser.add_argument("--all", action="store_true", help="Check every registry entry")
    parser.add_argument("--skill", action="append", default=[], help="External skill id to check")
    parser.add_argument("--chain", action="append", default=[], help="Internal skill id whose external chain should be checked")
    parser.add_argument("--chain-map", default=str(DEFAULT_CHAIN_MAP), help="Path to skills-chaining-map.md")
    parser.add_argument(
        "--agent",
        choices=["codex", "claude", "cursor", "project"],
        default="codex",
        help="Destination agent layout",
    )
    parser.add_argument("--dest", help="Override destination skill directory")
    parser.add_argument("--offline", action="store_true", help="Only check local install state")
    parser.add_argument("--network", action="store_true", help="Also verify upstream refs and skill paths")
    return parser


def verify_network(installer, skill) -> tuple[bool, str]:
    try:
        repo_dir = installer.sync_repo(skill, dry_run=False)
        skill_file = repo_dir / skill.path / "SKILL.md"
        if not skill_file.exists():
            return False, f"upstream missing SKILL.md at {skill.path}"
        return True, "upstream ok"
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        return False, f"upstream failed: {exc}"


def install_missing(skill_ids: list[str], agent: str, dest: str | None) -> int:
    cmd = [sys.executable, str(INSTALLER), "--agent", agent]
    if dest:
        cmd.extend(["--dest", dest])
    for skill_id in skill_ids:
        cmd.extend(["--skill", skill_id])
    return subprocess.run(cmd, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.offline and args.network:
        parser.error("use either --offline or --network, not both")

    installer = load_installer()
    registry = installer.load_registry(Path(args.registry).expanduser().resolve())
    check_all = args.all or (not args.skill and not args.chain)
    skills = installer.selected_entries(
        registry,
        check_all,
        args.skill,
        args.chain,
        Path(args.chain_map).expanduser().resolve(),
    )
    root = installer.target_root(args.agent, args.dest)

    missing: list[str] = []
    failures = 0

    for skill in skills:
        installed = root / skill.install_name / "SKILL.md"
        local_ok = installed.exists()
        status = "installed" if local_ok else "missing"
        details = [status]
        if not local_ok:
            missing.append(skill.skill_id)
        if args.network:
            ok, message = verify_network(installer, skill)
            details.append(message)
            if not ok:
                failures += 1
        print(f"{skill.skill_id}: {', '.join(details)}")

    if missing:
        print()
        print("Install missing skills with:")
        for skill_id in missing:
            command = f"python3 scripts/install-external-skills.py --skill {skill_id} --agent {args.agent}"
            if args.dest:
                command += f" --dest {args.dest}"
            print(f"  {command}")

        if os.environ.get("PLUGIN_BUNDLE_AUTO_INSTALL_EXTERNAL_SKILLS") == "1":
            print()
            print("PLUGIN_BUNDLE_AUTO_INSTALL_EXTERNAL_SKILLS=1 set; installing missing skills.")
            failures += install_missing(missing, args.agent, args.dest)

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
