#!/usr/bin/env python3
"""Audit hook/script coverage, boundaries, conflicts, excess, and portability."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from validate_skills import ParseError, parse_frontmatter
except ModuleNotFoundError:  # Imported as scripts.audit_hooks_scripts in tests.
    from scripts.validate_skills import ParseError, parse_frontmatter


CODE_SUFFIXES = {".py", ".sh", ".js", ".mjs", ".cjs", ".ts", ".ps1"}
HOOK_EVENTS = {
    "ConfigChange",
    "CwdChanged",
    "DirectoryAdded",
    "Elicitation",
    "ElicitationResult",
    "FileChanged",
    "InstructionsLoaded",
    "MessageDisplay",
    "Notification",
    "PermissionDenied",
    "PermissionRequest",
    "PostCompact",
    "PostToolBatch",
    "PostToolUse",
    "PostToolUseFailure",
    "PreCompact",
    "PreToolUse",
    "SessionEnd",
    "SessionStart",
    "Setup",
    "Stop",
    "StopFailure",
    "SubagentStart",
    "SubagentStop",
    "TaskCompleted",
    "TaskCreated",
    "TeammateIdle",
    "UserPromptExpansion",
    "UserPromptSubmit",
    "WorktreeCreate",
    "WorktreeRemove",
}
PLACEHOLDER_PATTERNS = (
    re.compile(r"Placeholder for .+ (?:hooks|scripts)\.", re.IGNORECASE),
    re.compile(r"Leave empty unless the skill owns hook behavior", re.IGNORECASE),
    re.compile(r"^Executable helper scripts owned by this skill\.$", re.MULTILINE),
    re.compile(r"No deterministic script is required", re.IGNORECASE),
    re.compile(r"instead of adding .+ scripts", re.IGNORECASE),
)
PORTABILITY_PATTERNS = (
    ("absolute macOS user path", re.compile(r"/Users/[A-Za-z0-9._-]+/")),
    ("absolute Windows user path", re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\]+\\\\", re.IGNORECASE)),
    ("repository owner identity", re.compile("alvaro" + "villalbaa", re.IGNORECASE)),
    ("company identity", re.compile(r"\bcl" + r"ous\b", re.IGNORECASE)),
    ("legacy company-specific namespace", re.compile(r"agent[-_]" + r"company", re.IGNORECASE)),
)
EMAIL_ADDRESS_RE = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
RESERVED_EMAIL_DOMAINS = {"example.com", "example.net", "example.org", "example.co.uk"}
HOOKISH_NAME = re.compile(r"(?:^|[-_])(hook|pre[-_]?tool|post[-_]?tool|session[-_]?(?:start|end)|completion[-_]?gate)(?:[-_.]|$)", re.IGNORECASE)
SCRIPT_ASSET_CLAIM = "`scripts/` contains executable helpers owned by this lane."
GENERIC_SCRIPT_ASSET_CLAIM = "The work needs this lane's references, scripts, examples, or templates."
OWNERSHIP_DECISIONS = (
    ("Agent orchestration", "engineering/skills/multi-agent", "Removed the agent-system-architecture copy."),
    ("Agentic development Stop loop", "engineering/skills/agent-harness", "Removed the unused agentic-development workspace scaffold."),
    ("Prompt optimization", "engineering/skills/prompt-engineering", "Removed architecture and prompt-tool-design copies."),
    ("RAG evaluation", "engineering/skills/ai-evals-observability", "Removed the architecture copy."),
    ("Test coverage analysis and reporting", "engineering/skills/testing", "Removed architecture, backend-testing, and test-strategy-coverage copies."),
    ("CI/CD pipeline generation", "engineering/skills/cicd", "Removed the release-landing copy."),
    ("Passive source and secret scanning", "engineering/skills/security", "Removed the overlapping web-vuln-validation scanner; kept a dedicated secrets scanner and removed secret rules from the broad source scanner."),
    ("Dependency vulnerability intelligence", "current external advisory data", "Removed two overlapping scripts with frozen miniature CVE tables; use current ecosystem or advisory-backed tools."),
    ("Marketing experiment lifecycle", "marketing/skills/growth-engine", "Removed the sales/growth fork and made experiment thresholds explicit."),
    ("Two-proportion experiment sample sizing", "product/skills/experiments", "Removed the CRO calculator and chained CRO to this owner."),
)
REMOVAL_DECISIONS = (
    ("Skill-level hook folders and placeholder READMEs", "Removed; registrations belong in SKILL.md frontmatter and handlers in scripts/."),
    ("Advisory post-run Markdown files", "Moved to references/ as on-demand checklists."),
    ("Unregistered root hook-like scripts", "Removed because no runtime invoked them."),
    ("Hard-coded user-story demo generator", "Removed because it invented a canned epic and universal acceptance criteria."),
    ("Marketing pacing/recruiting monitor", "Removed because it assumed private API schemas, placeholder endpoints, and cross-department recruiting ownership."),
    ("Unfed agent trace summarizer", "Removed with its unregistered trace hook; no runtime produced the claimed input."),
    ("Overlapping security and dependency scanners", "Consolidated passive source and secret scanning under security; removed frozen CVE snapshots and the duplicate web-validation scanner."),
)


@dataclass(frozen=True)
class ScriptAsset:
    path: Path
    owner: str
    kind: str


@dataclass(frozen=True)
class HookRegistration:
    source: Path
    owner: str
    event: str
    matcher: str
    handler_type: str
    handler: Path | None


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def department_dirs(root: Path) -> list[Path]:
    return sorted(
        manifest.parent.parent
        for manifest in root.glob("*/.claude-plugin/plugin.json")
        if manifest.is_file()
    )


def skill_dirs(departments: Iterable[Path]) -> list[Path]:
    return sorted(
        skill
        for department in departments
        for skill in (department / "skills").glob("*")
        if skill.is_dir() and (skill / "SKILL.md").is_file()
    )


def is_code(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in CODE_SUFFIXES


def classify_script(path: Path, root: Path, departments: list[Path], skills: list[Path]) -> ScriptAsset:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.name.startswith("test_") or path.name.endswith("_test.py"):
        kind = "test"
        owning_skill = next((skill for skill in skills if skill in path.parents), None)
        owner = rel(owning_skill, root) if owning_skill else "repository"
    elif path.parent == root / "scripts" or (root / "scripts") in path.parents:
        kind = "repository-tool"
        owner = "repository"
    else:
        owning_skill = next((skill for skill in skills if skill == path or skill in path.parents), None)
        if owning_skill is not None:
            owner = rel(owning_skill, root)
            if path.stem.endswith("_lib") or path.name in {"credential.py", "dataforseo_api.py"}:
                kind = "support-module"
            elif path.suffix == ".py" and not text.startswith("#!") and "if __name__" not in text:
                kind = "support-module"
            else:
                kind = "on-demand"
        else:
            department = next((item for item in departments if item in path.parents), None)
            owner = rel(department, root) if department else "repository"
            kind = "plugin-handler"
    return ScriptAsset(path=path, owner=owner, kind=kind)


def discover_scripts(root: Path, departments: list[Path], skills: list[Path]) -> list[ScriptAsset]:
    candidates: set[Path] = set()
    root_scripts = root / "scripts"
    if root_scripts.is_dir():
        candidates.update(path for path in root_scripts.rglob("*") if is_code(path))
    for department in departments:
        plugin_scripts = department / "scripts"
        if plugin_scripts.is_dir():
            candidates.update(path for path in plugin_scripts.rglob("*") if is_code(path))
    for skill in skills:
        candidates.update(
            path
            for path in skill.rglob("*")
            if is_code(path) and "scripts" in path.relative_to(skill).parts
        )
    return [classify_script(path, root, departments, skills) for path in sorted(candidates)]


def hook_groups(value: object, source: Path, owner: str, root: Path, skill: Path | None, plugin: Path) -> tuple[list[HookRegistration], list[str]]:
    registrations: list[HookRegistration] = []
    failures: list[str] = []
    if not isinstance(value, dict):
        return registrations, [f"{rel(source, root)}: hooks must be a mapping"]

    for event, groups in value.items():
        if event not in HOOK_EVENTS:
            failures.append(f"{rel(source, root)}: unsupported hook event `{event}`")
            continue
        if not isinstance(groups, list):
            failures.append(f"{rel(source, root)}: hook event `{event}` must contain a list")
            continue
        for group in groups:
            if not isinstance(group, dict):
                failures.append(f"{rel(source, root)}: `{event}` matcher group must be a mapping")
                continue
            matcher = str(group.get("matcher", ""))
            handlers = group.get("hooks")
            if not isinstance(handlers, list) or not handlers:
                failures.append(f"{rel(source, root)}: `{event}` matcher group has no handlers")
                continue
            for handler in handlers:
                if not isinstance(handler, dict):
                    failures.append(f"{rel(source, root)}: `{event}` handler must be a mapping")
                    continue
                handler_type = str(handler.get("type", ""))
                resolved: Path | None = None
                if handler_type == "command":
                    command = handler.get("command")
                    args = handler.get("args", [])
                    if not isinstance(command, str) or not command:
                        failures.append(f"{rel(source, root)}: `{event}` command handler has no command")
                    elif not isinstance(args, list) or any(not isinstance(item, str) for item in args):
                        failures.append(f"{rel(source, root)}: `{event}` command args must be strings")
                    else:
                        tokens = [command, *args]
                        candidates = [token for token in tokens if "/scripts/" in token or token.startswith("scripts/")]
                        if candidates:
                            candidate = candidates[0]
                            if skill is not None:
                                candidate = candidate.replace("${CLAUDE_SKILL_DIR}", str(skill))
                            candidate = candidate.replace("${CLAUDE_PLUGIN_ROOT}", str(plugin))
                            path = Path(candidate).expanduser()
                            if not path.is_absolute():
                                path = source.parent / path
                            resolved = path.resolve()
                            if not resolved.is_file():
                                failures.append(
                                    f"{rel(source, root)}: `{event}` handler does not resolve: {candidates[0]}"
                                )
                            elif root.resolve() not in resolved.parents:
                                failures.append(
                                    f"{rel(source, root)}: `{event}` handler escapes the repository: {resolved}"
                                )
                        elif command not in {"bash", "python3", "node", "sh"}:
                            failures.append(
                                f"{rel(source, root)}: `{event}` command handler must reference an owned script"
                            )
                elif handler_type not in {"agent", "http", "mcp_tool", "prompt"}:
                    failures.append(f"{rel(source, root)}: `{event}` has unsupported handler type `{handler_type}`")

                registrations.append(
                    HookRegistration(
                        source=source,
                        owner=owner,
                        event=event,
                        matcher=matcher,
                        handler_type=handler_type,
                        handler=resolved,
                    )
                )
    return registrations, failures


def discover_hooks(root: Path, departments: list[Path], skills: list[Path]) -> tuple[list[HookRegistration], list[str]]:
    registrations: list[HookRegistration] = []
    failures: list[str] = []

    for department in departments:
        hook_dir = department / "hooks"
        if hook_dir.exists():
            for path in sorted(hook_dir.rglob("*")):
                if path.is_file() and path.suffix != ".json":
                    failures.append(f"{rel(path, root)}: hooks/ may contain registration JSON only")
            for config in sorted(hook_dir.glob("*.json")):
                try:
                    payload = json.loads(config.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    failures.append(f"{rel(config, root)}: invalid hook JSON: {exc}")
                    continue
                value = payload.get("hooks") if isinstance(payload, dict) else None
                found, errors = hook_groups(value, config, rel(department, root), root, None, department)
                registrations.extend(found)
                failures.extend(errors)

    for skill in skills:
        for hook_dir in (path for path in skill.rglob("hooks") if path.is_dir()):
            for path in sorted(hook_dir.rglob("*")):
                if path.is_file():
                    failures.append(
                        f"{rel(path, root)}: skill hooks belong in SKILL.md frontmatter; handler code belongs in scripts/"
                    )
        skill_file = skill / "SKILL.md"
        try:
            frontmatter = parse_frontmatter(skill_file)
        except ParseError as exc:
            failures.append(f"{rel(skill_file, root)}: cannot inspect hooks: {exc}")
            continue
        if "hooks" not in frontmatter:
            continue
        department = next(item for item in departments if item in skill.parents)
        found, errors = hook_groups(
            frontmatter["hooks"], skill_file, rel(skill, root), root, skill, department
        )
        registrations.extend(found)
        failures.extend(errors)

    return registrations, failures


def placeholder_failures(root: Path, departments: list[Path]) -> list[str]:
    failures: list[str] = []
    for department in departments:
        for path in department.rglob("README.md"):
            if "hooks" not in path.parts and "scripts" not in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern.search(text) for pattern in PLACEHOLDER_PATTERNS):
                failures.append(f"{rel(path, root)}: placeholder hook/script README is not allowed")
    return failures


def conflict_failures(assets: list[ScriptAsset], root: Path) -> list[str]:
    failures: list[str] = []
    by_name: dict[str, list[ScriptAsset]] = defaultdict(list)
    by_digest: dict[str, list[ScriptAsset]] = defaultdict(list)
    for asset in assets:
        if asset.kind == "test":
            continue
        by_name[asset.path.name].append(asset)
        digest = hashlib.sha256(asset.path.read_bytes()).hexdigest()
        by_digest[digest].append(asset)

    for name, matches in sorted(by_name.items()):
        owners = {item.owner for item in matches}
        if len(matches) > 1 and len(owners) > 1:
            rendered = ", ".join(rel(item.path, root) for item in matches)
            failures.append(f"ambiguous script name `{name}` has multiple owners: {rendered}")
    for matches in by_digest.values():
        if len(matches) > 1:
            rendered = ", ".join(rel(item.path, root) for item in matches)
            failures.append(f"exact duplicate script implementations: {rendered}")
    return failures


def portability_failures(assets: list[ScriptAsset], root: Path) -> list[str]:
    failures: list[str] = []
    for asset in assets:
        if asset.kind == "test":
            continue
        text = asset.path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PORTABILITY_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{rel(asset.path, root)}:{line}: {label} is not portable")
        for match in EMAIL_ADDRESS_RE.finditer(text):
            if match.group(1).lower() in RESERVED_EMAIL_DOMAINS:
                continue
            line = text.count("\n", 0, match.start()) + 1
            failures.append(f"{rel(asset.path, root)}:{line}: hard-coded email address is not portable")
    return failures


def registration_failures(registrations: list[HookRegistration], assets: list[ScriptAsset], root: Path) -> list[str]:
    failures: list[str] = []
    registered_paths = {item.handler for item in registrations if item.handler is not None}
    asset_paths = {asset.path.resolve() for asset in assets}
    seen: set[tuple[str, str, str, str]] = set()
    for registration in registrations:
        handler = rel(registration.handler, root) if registration.handler else registration.handler_type
        key = (registration.owner, registration.event, registration.matcher, str(handler))
        if key in seen:
            failures.append(
                f"{rel(registration.source, root)}: duplicate hook registration for "
                f"{registration.event}/{registration.matcher or '*'} -> {handler}"
            )
        seen.add(key)

    for asset in assets:
        if (
            HOOKISH_NAME.search(asset.path.name)
            and asset.kind != "test"
            and asset.path.resolve() not in registered_paths
        ):
            failures.append(f"{rel(asset.path, root)}: hook-like script is not referenced by a hook registration")
    for path in sorted(registered_paths):
        if path not in asset_paths:
            failures.append(f"{rel(path, root)}: registered hook handler is not an inventoried script")
    return failures


def script_contract_failures(assets: list[ScriptAsset], root: Path) -> list[str]:
    failures: list[str] = []
    runnable_kinds = {"on-demand", "plugin-handler", "repository-tool"}
    shebang_suffixes = {".py", ".sh", ".js", ".mjs", ".cjs"}
    for asset in assets:
        if asset.kind not in runnable_kinds or asset.path.suffix not in shebang_suffixes:
            continue
        first_line = asset.path.read_text(encoding="utf-8", errors="ignore").splitlines()[:1]
        if not first_line or not first_line[0].startswith("#!"):
            failures.append(f"{rel(asset.path, root)}: runnable script is missing a portable shebang")
            continue
        if not os.access(asset.path, os.X_OK) or not (asset.path.stat().st_mode & stat.S_IXUSR):
            failures.append(f"{rel(asset.path, root)}: runnable script is not executable")
    return failures


def documentation_failures(
    skills: list[Path], assets: list[ScriptAsset], root: Path
) -> list[str]:
    failures: list[str] = []
    executable_by_owner: dict[str, list[ScriptAsset]] = defaultdict(list)
    for asset in assets:
        if asset.kind != "test":
            executable_by_owner[asset.owner].append(asset)

    for skill in skills:
        owner = rel(skill, root)
        skill_file = skill / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8", errors="ignore")
        owned = executable_by_owner.get(owner, [])
        if owned and "scripts/" not in text and "`scripts`" not in text:
            failures.append(
                f"{rel(skill_file, root)}: owns executable assets but does not document its scripts boundary"
            )
        if not owned and (SCRIPT_ASSET_CLAIM in text or GENERIC_SCRIPT_ASSET_CLAIM in text):
            failures.append(
                f"{rel(skill_file, root)}: claims executable helpers but owns no non-test script assets"
            )
    return failures


def render_report(
    root: Path,
    departments: list[Path],
    skills: list[Path],
    assets: list[ScriptAsset],
    registrations: list[HookRegistration],
) -> str:
    assets_by_owner: dict[str, list[ScriptAsset]] = defaultdict(list)
    hooks_by_owner: dict[str, list[HookRegistration]] = defaultdict(list)
    for asset in assets:
        assets_by_owner[asset.owner].append(asset)
    for registration in registrations:
        hooks_by_owner[registration.owner].append(registration)

    lines = [
        "# Hook and Script Coverage",
        "",
        "Generated by `python3 scripts/audit_hooks_scripts.py . --report <path>`.",
        "",
        "## Summary",
        "",
        f"- Department plugins: {len(departments)}",
        f"- Skills reviewed: {len(skills)}",
        f"- Hook registrations: {len(registrations)}",
        f"- Script assets: {len(assets)}",
        f"- Registered hook handlers: {len({item.handler for item in registrations if item.handler})}",
        "",
        "Every discovered department plugin and every skill with a `SKILL.md` is included below.",
        "A zero in both capability columns is intentional: the skill remains an",
        "instruction/reference workflow and does not gain placeholder automation.",
        "",
        "## Decision rules applied",
        "",
        "- Hooks are automatic runtime lifecycle behavior and must be registered; handler code lives in `scripts/`.",
        "- Scripts are on-demand deterministic tools. Checklists, reminders, and judgment stay in skill instructions or references.",
        "- One capability has one canonical implementation owner. Exact duplicate implementations and ambiguous cross-owner filenames fail validation.",
        "- Runnable assets must be portable and executable; company identities, private user paths, and unregistered hook-like files fail validation.",
        "- A skill without deterministic automation remains instruction/reference-only instead of receiving placeholder files.",
        "",
        "See `references/docs/hooks-and-scripts.md` for the normative boundary and creation criteria.",
        "",
        "## Canonical capability ownership",
        "",
        "| Capability | Canonical owner | Resolution |",
        "| --- | --- | --- |",
    ]
    lines.extend(
        f"| {capability} | `{owner}` | {resolution} |"
        for capability, owner, resolution in OWNERSHIP_DECISIONS
    )
    lines.extend(
        [
            "",
            "## Excess removed or reclassified",
            "",
            "| Surface | Decision |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| {surface} | {decision} |" for surface, decision in REMOVAL_DECISIONS)
    lines.extend(
        [
        "",
        "## Plugin and skill matrix",
        "",
        "| Plugin | Skill | Hooks | Scripts | Decision |",
        "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for skill in skills:
        owner = rel(skill, root)
        plugin, _, name = owner.partition("/skills/")
        hooks = hooks_by_owner.get(owner, [])
        script_assets = assets_by_owner.get(owner, [])
        if hooks:
            decision = "automatic lifecycle behavior registered"
        elif script_assets:
            decision = "on-demand deterministic tooling only"
        else:
            decision = "instruction/reference-only; no executable needed"
        lines.append(f"| `{plugin}` | `{name}` | {len(hooks)} | {len(script_assets)} | {decision} |")

    lines.extend(["", "## Hook registrations", ""])
    if not registrations:
        lines.append("No automatic lifecycle behavior is registered.")
    else:
        lines.extend(
            [
                "| Owner | Event | Matcher | Type | Handler |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in registrations:
            handler = rel(item.handler, root) if item.handler else "runtime-native"
            lines.append(
                f"| `{item.owner}` | `{item.event}` | `{item.matcher or '*'}` | "
                f"`{item.handler_type}` | `{handler}` |"
            )

    lines.extend(["", "## Script inventory", ""])
    lines.extend(["| Owner | Kind | Path |", "| --- | --- | --- |"])
    registered_paths = {item.handler for item in registrations if item.handler}
    for asset in assets:
        kind = "hook-handler" if asset.path.resolve() in registered_paths else asset.kind
        lines.append(f"| `{asset.owner}` | `{kind}` | `{rel(asset.path, root)}` |")
    lines.append("")
    return "\n".join(lines)


def audit(root: Path) -> tuple[list[str], list[Path], list[Path], list[ScriptAsset], list[HookRegistration]]:
    failures: list[str] = []
    departments = department_dirs(root)
    skills = skill_dirs(departments)
    if not departments:
        failures.append("no department plugins found")
    policy = root / "references" / "docs" / "hooks-and-scripts.md"
    if not policy.is_file():
        failures.append("references/docs/hooks-and-scripts.md: missing boundary policy")

    assets = discover_scripts(root, departments, skills)
    registrations, hook_errors = discover_hooks(root, departments, skills)
    failures.extend(hook_errors)
    failures.extend(placeholder_failures(root, departments))
    failures.extend(conflict_failures(assets, root))
    failures.extend(portability_failures(assets, root))
    failures.extend(registration_failures(registrations, assets, root))
    failures.extend(script_contract_failures(assets, root))
    failures.extend(documentation_failures(skills, assets, root))
    return failures, departments, skills, assets, registrations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit plugin hooks/scripts for coverage, boundaries, conflicts, excess, and portability."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument("--report", help="Write the complete Markdown coverage matrix")
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    failures, departments, skills, assets, registrations = audit(root)
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        print(f"Hook/script audit failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1

    if args.report:
        report_path = Path(args.report).expanduser()
        if not report_path.is_absolute():
            report_path = root / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_report(root, departments, skills, assets, registrations), encoding="utf-8"
        )
        print(f"Wrote {rel(report_path, root)}")

    print(
        f"Audited {len(departments)} plugin(s), {len(skills)} skill(s), "
        f"{len(registrations)} hook registration(s), and {len(assets)} script asset(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
