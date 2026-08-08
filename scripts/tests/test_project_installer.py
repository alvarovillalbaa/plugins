from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
INSTALLER_PATH = ROOT / "scripts" / "project_installer.py"
SPEC = importlib.util.spec_from_file_location("project_installer", INSTALLER_PATH)
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class ProjectInstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = Path(tempfile.mkdtemp(prefix="project-installer-test-"))
        self.source = self.temporary / "source"
        self.project = self.temporary / "project"
        self.source.mkdir()
        self.project.mkdir()
        self._write_plugin(
            "engineering",
            skills={
                "craft": {
                    "SKILL.md": "---\nname: craft\ndescription: Engineering craft.\n---\n",
                    "remove.md": "remove upstream\n",
                    "keep.md": "keep upstream\n",
                }
            },
            commands={"review": "alpha\nmiddle\nomega\n"},
            rules={"defaults": "engineering defaults\n"},
            agents={"reviewer": "engineering reviewer\n"},
        )
        self._write_plugin(
            "marketing",
            skills={"craft": {"SKILL.md": "---\nname: craft\ndescription: Marketing craft.\n---\n"}},
            commands={"publish": "publish\n"},
            rules={"defaults": "marketing defaults\n"},
            agents={"reviewer": "marketing reviewer\n"},
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temporary)

    def _write_plugin(
        self,
        plugin: str,
        *,
        skills: dict[str, dict[str, str]],
        commands: dict[str, str],
        rules: dict[str, str],
        agents: dict[str, str],
    ) -> None:
        root = self.source / plugin
        root.mkdir()
        (root / "profile.yaml").write_text(f"slug: {plugin}\n", encoding="utf-8")
        for directory in ("skills", "commands", "rules", "agents"):
            (root / directory).mkdir()
        (root / "rules" / "README.md").write_text("not installable\n", encoding="utf-8")
        for name, files in skills.items():
            skill = root / "skills" / name
            skill.mkdir()
            for relative, content in files.items():
                path = skill / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        for name, content in commands.items():
            (root / "commands" / f"{name}.md").write_text(content, encoding="utf-8")
        for name, content in rules.items():
            (root / "rules" / f"{name}.md").write_text(content, encoding="utf-8")
        for name, content in agents.items():
            (root / "agents" / f"{name}.md").write_text(content, encoding="utf-8")

    def _lock(self) -> dict[str, object]:
        return json.loads(
            (self.project / ".agents" / ".plugin-lock.json").read_text(encoding="utf-8")
        )

    @staticmethod
    def _file_tree(root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def _write_command_registry(self, owners: dict[str, str]) -> None:
        references = self.source / "references"
        references.mkdir(exist_ok=True)
        records = [
            {
                "path": f"{identity.split('/', 1)[0]}/commands/"
                f"{identity.split('/', 1)[1]}.md",
                "owner": owner,
            }
            for identity, owner in owners.items()
        ]
        (references / "command-capabilities.json").write_text(
            json.dumps({"schema_version": 1, "commands": records}, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_typed_selectors_install_all_four_component_types(self) -> None:
        result = installer.install_project(
            self.source,
            self.project,
            [
                "skill:engineering/craft",
                "command:engineering/review",
                "rule:engineering/defaults",
                "agent:engineering/reviewer",
            ],
        )

        agents = self.project / ".agents"
        self.assertTrue((agents / "skills" / "engineering__craft" / "SKILL.md").is_file())
        self.assertTrue((agents / "commands" / "review.md").is_file())
        self.assertTrue((agents / "rules" / "engineering__defaults.md").is_file())
        self.assertTrue((agents / "agents" / "engineering__reviewer.md").is_file())
        self.assertEqual(len(result.selected), 4)
        self.assertEqual(len(self._lock()["components"]), 4)

    def test_interactive_selector_supports_whole_plugin_by_number(self) -> None:
        catalog = installer.scan_catalog(self.source)
        answers = iter(["1", ""])
        output: list[str] = []

        selectors = installer.prompt_selectors(
            catalog,
            input_fn=lambda _prompt: next(answers),
            output_fn=output.append,
        )

        self.assertEqual(selectors, ["plugin:engineering"])
        self.assertIn("Selected 4 component(s).", output)

    def test_interactive_selector_supports_individual_components(self) -> None:
        catalog = installer.scan_catalog(self.source)
        answers = iter(["marketing", "select", "1, 4"])
        output: list[str] = []

        selectors = installer.prompt_selectors(
            catalog,
            input_fn=lambda _prompt: next(answers),
            output_fn=output.append,
        )

        self.assertEqual(
            selectors,
            ["skill:marketing/craft", "agent:marketing/reviewer"],
        )
        self.assertTrue(any("Components in marketing" in line for line in output))
        self.assertIn("Selected 2 component(s).", output)

    def test_whole_plugin_expands_into_flat_tree_without_plugin_folder(self) -> None:
        self._write_command_registry(
            {
                "engineering/review": "engineering/craft",
                "marketing/publish": "marketing/craft",
            }
        )
        result = installer.install_project(
            self.source, self.project, ["plugin:engineering"]
        )

        agents = self.project / ".agents"
        expected = {
            "skills/engineering__craft/SKILL.md",
            "commands/review.md",
            "rules/engineering__defaults.md",
            "agents/engineering__reviewer.md",
        }
        for relative in expected:
            self.assertTrue((agents / relative).exists(), relative)
        self.assertFalse((agents / "engineering").exists())
        self.assertFalse((agents / "rules" / "README.md").exists())
        self.assertEqual(result.selected.count("skill:engineering/craft"), 1)
        self.assertEqual(len(self._lock()["components"]), 4)

    def test_command_dependency_uses_collision_qualified_flat_skill_target(self) -> None:
        self._write_command_registry(
            {
                "engineering/review": "marketing/craft",
                "marketing/publish": "marketing/craft",
            }
        )

        preview = installer.install_project(
            self.source,
            self.project,
            ["command:engineering/review"],
            dry_run=True,
        )
        result = installer.install_project(
            self.source,
            self.project,
            ["command:engineering/review"],
        )

        self.assertEqual(
            result.selected,
            ("command:engineering/review", "skill:marketing/craft"),
        )
        self.assertTrue(
            (self.project / ".agents/skills/marketing__craft/SKILL.md").is_file()
        )
        self.assertTrue(
            any(
                action.endswith("(required by command:engineering/review)")
                for action in preview.actions
            )
        )

    def test_canonical_command_installs_include_required_owner_skills(self) -> None:
        selectors = [
            "command:engineering/dev-loop",
            "command:engineering/browser-trace",
            "command:sales/account-brief",
        ]

        result = installer.install_project(ROOT, self.project, selectors)

        self.assertEqual(
            set(result.selected),
            {
                *selectors,
                "skill:engineering/agent-harness",
                "skill:engineering/frontend-e2e",
                "skill:productivity/prospect",
            },
        )
        for relative in (
            ".agents/skills/agent-harness/scripts/setup-dev-loop.sh",
            ".agents/skills/frontend-e2e/scripts/browser_trace.py",
            ".agents/skills/prospect/SKILL.md",
        ):
            self.assertTrue((self.project / relative).is_file(), relative)

        dev_loop = (self.project / ".agents/commands/dev-loop.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            ".agents/skills/agent-harness/scripts/setup-dev-loop.sh", dev_loop
        )
        self.assertIn(".agents/skills/agent-harness/SKILL.md", dev_loop)
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", dev_loop)

        browser_trace = (
            self.project / ".agents/commands/browser-trace.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            ".agents/skills/frontend-e2e/scripts/browser_trace.py",
            browser_trace,
        )
        self.assertIn(".agents/skills/frontend-e2e/SKILL.md", browser_trace)
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", browser_trace)

        agent_harness = (
            self.project / ".agents/skills/agent-harness/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            ".agents/skills/agent-harness/scripts/completion-gate.py",
            agent_harness,
        )
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", agent_harness)

    def test_all_canonical_installed_markdown_links_stay_in_agents_and_exist(self) -> None:
        agents = self.project / ".agents"
        runtime_support = agents / "runtime-support"
        runtime_support.mkdir(parents=True)
        support_sources = {
            "install-external-skills.py": ROOT
            / "scripts"
            / "install-external-skills.py",
            "external-skills.yaml": ROOT / "references" / "external-skills.yaml",
            "external-sources.yaml": ROOT / "references" / "external-sources.yaml",
            "skills-chaining-map.md": ROOT / "skills-chaining-map.md",
            "promotion-matrix.md": ROOT
            / "references"
            / "docs"
            / "promotion-matrix.md",
            "INSTALLATION.md": ROOT
            / "references"
            / "docs"
            / "INSTALLATION.md",
        }
        for name, source in support_sources.items():
            shutil.copy2(source, runtime_support / name)
        shutil.copy2(ROOT / "component-graph.json", agents / "component-graph.json")
        shutil.copy2(
            ROOT / "references" / "runtime-contract.json",
            agents / "runtime-contract.json",
        )

        catalog = installer.scan_catalog(ROOT)
        installer.install_project(
            ROOT,
            self.project,
            [f"plugin:{plugin}" for plugin in sorted(catalog.plugins)],
        )

        instruction_design = (
            agents
            / "skills"
            / "agent-harness"
            / "references"
            / "instruction-file-design.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "python3 .agents/runtime-support/install-external-skills.py",
            instruction_design,
        )
        self.assertNotIn("--agent codex", instruction_design)
        self_improvement = (
            agents
            / "skills"
            / "agent-harness"
            / "references"
            / "self-improvement.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "https://github.com/alvarovillalbaa/plugins/blob/main/"
            "references/docs/hooks-and-scripts.md",
            self_improvement,
        )
        brain_contract = (
            agents / "skills" / "brain" / "references" / "brain_contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "../../../runtime-support/promotion-matrix.md", brain_contract
        )

        markdown_files: list[Path] = []
        for directory in ("skills", "commands", "rules", "agents"):
            markdown_files.extend((agents / directory).rglob("*.md"))
        self.assertTrue(markdown_files)
        for markdown in sorted(markdown_files):
            text = markdown.read_text(encoding="utf-8")
            self.assertNotIn(
                "python scripts/install-external-skills.py",
                text,
                str(markdown),
            )
            self.assertNotIn("${CLAUDE_PLUGIN_ROOT}/skills/", text, str(markdown))
            in_fence = False
            for line in text.splitlines():
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                inline_code_spans = [
                    (code_match.start(), code_match.end())
                    for code_match in installer.INLINE_CODE_RE.finditer(line)
                ]
                for match in installer.MARKDOWN_DESTINATION_RE.finditer(line):
                    target = match.group("target")
                    if any(
                        start <= match.start("target") < end
                        for start, end in inline_code_spans
                    ):
                        continue
                    if target.startswith(
                        ("#", "/", "http://", "https://", "mailto:", "app://")
                    ):
                        continue
                    if any(character in target for character in ('"', "'", "{", "}")):
                        continue
                    local_target = target.split("#", 1)[0]
                    resolved = (markdown.parent / local_target).resolve()
                    self.assertTrue(
                        resolved.is_relative_to(agents.resolve()),
                        f"{markdown}: link escapes .agents: {target}",
                    )
                    self.assertTrue(
                        resolved.exists(),
                        f"{markdown}: installed link is missing: {target}",
                    )

    def test_command_registry_missing_or_invalid_owner_fails_closed(self) -> None:
        references = self.source / "references"
        references.mkdir()
        registry = references / "command-capabilities.json"
        valid_publish = {
            "path": "marketing/commands/publish.md",
            "owner": "marketing/craft",
        }
        cases = (
            (
                [
                    {"path": "engineering/commands/review.md"},
                    valid_publish,
                ],
                "command owner is required",
            ),
            (
                [
                    {
                        "path": "engineering/commands/review.md",
                        "owner": "engineering/missing",
                    },
                    valid_publish,
                ],
                "does not resolve to a local skill",
            ),
            (
                [valid_publish],
                "missing owner entries for: command:engineering/review",
            ),
        )
        for records, message in cases:
            with self.subTest(message=message):
                registry.write_text(
                    json.dumps({"schema_version": 1, "commands": records}) + "\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(installer.InstallerError, message):
                    installer.install_project(
                        self.source,
                        self.project,
                        ["command:engineering/review"],
                    )
                self.assertFalse((self.project / ".agents").exists())

    def test_flat_skill_rewrites_external_support_without_mutating_source(self) -> None:
        references = self.source / "references"
        references.mkdir()
        (references / "external-skills.yaml").write_text(
            "skills:\n", encoding="utf-8"
        )
        (references / "external-sources.yaml").write_text(
            "sources:\n", encoding="utf-8"
        )
        docs = references / "docs"
        docs.mkdir()
        (docs / "promotion-matrix.md").write_text(
            "# Promotion matrix\n", encoding="utf-8"
        )
        (docs / "INSTALLATION.md").write_text(
            "# Installation\n", encoding="utf-8"
        )
        (references / "component-graph.json").write_text("{}\n", encoding="utf-8")
        (references / "runtime-contract.json").write_text("{}\n", encoding="utf-8")
        (self.source / "skills-chaining-map.md").write_text(
            "# Skill chaining\n", encoding="utf-8"
        )
        source_skill = self.source / "engineering" / "skills" / "craft" / "SKILL.md"
        native = (
            "---\nname: craft\ndescription: Engineering craft.\n---\n\n"
            "Install: `python scripts/install-external-skills.py --skill tdd --agent codex`.\n\n"
            "Registry: [`../../../references/external-skills.yaml`]"
            "(../../../references/external-skills.yaml).\n\n"
            "Sources: [`../../../references/external-sources.yaml`]"
            "(../../../references/external-sources.yaml).\n\n"
            "See [`../../../skills-chaining-map.md`]"
            "(../../../skills-chaining-map.md).\n\n"
            "Promotion: [`../../../references/docs/promotion-matrix.md`]"
            "(../../../references/docs/promotion-matrix.md).\n\n"
            "Install guide: [`../../../references/docs/INSTALLATION.md`]"
            "(../../../references/docs/INSTALLATION.md).\n\n"
            "Graph: [`../../../references/component-graph.json`]"
            "(../../../references/component-graph.json).\n\n"
            "Contract: [`../../../references/runtime-contract.json`]"
            "(../../../references/runtime-contract.json).\n\n"
            "Related: [`../../../marketing/skills/craft/SKILL.md`]"
            "(../../../marketing/skills/craft/SKILL.md).\n"
        )
        source_skill.write_text(native, encoding="utf-8")
        self.assertTrue(
            (source_skill.parent / "../../../references/external-skills.yaml").is_file()
        )
        self.assertTrue(
            (source_skill.parent / "../../../skills-chaining-map.md").is_file()
        )

        runtime_support = self.project / ".agents" / "runtime-support"
        runtime_support.mkdir(parents=True)
        for name in (
            "install-external-skills.py",
            "external-skills.yaml",
            "external-sources.yaml",
            "skills-chaining-map.md",
            "promotion-matrix.md",
            "INSTALLATION.md",
        ):
            (runtime_support / name).write_text("runtime support\n", encoding="utf-8")
        (self.project / ".agents" / "component-graph.json").write_text(
            "{}\n", encoding="utf-8"
        )
        (self.project / ".agents" / "runtime-contract.json").write_text(
            "{}\n", encoding="utf-8"
        )

        installer.install_project(
            self.source,
            self.project,
            ["skill:engineering/craft", "skill:marketing/craft"],
        )

        installed_skill = (
            self.project
            / ".agents"
            / "skills"
            / "engineering__craft"
            / "SKILL.md"
        )
        installed = installed_skill.read_text(encoding="utf-8")
        self.assertIn(
            "python3 .agents/runtime-support/install-external-skills.py "
            "--skill tdd --agent project",
            installed,
        )
        self.assertIn("../../runtime-support/external-skills.yaml", installed)
        self.assertIn("../../runtime-support/external-sources.yaml", installed)
        self.assertIn("../../runtime-support/skills-chaining-map.md", installed)
        self.assertIn("../../runtime-support/promotion-matrix.md", installed)
        self.assertIn("../../runtime-support/INSTALLATION.md", installed)
        self.assertIn("../../component-graph.json", installed)
        self.assertIn("../../runtime-contract.json", installed)
        self.assertIn("../../skills/marketing__craft/SKILL.md", installed)
        self.assertNotIn("python scripts/install-external-skills.py", installed)
        self.assertNotIn("--agent codex", installed)
        self.assertTrue(
            (installed_skill.parent / "../../runtime-support/external-skills.yaml").is_file()
        )
        self.assertTrue(
            (installed_skill.parent / "../../runtime-support/skills-chaining-map.md").is_file()
        )
        self.assertTrue(
            (installed_skill.parent / "../../skills/marketing__craft/SKILL.md").is_file()
        )
        self.assertEqual(source_skill.read_text(encoding="utf-8"), native)

    def test_multi_plugin_installs_keep_all_lock_entries_and_prefix_collisions(self) -> None:
        installer.install_project(self.source, self.project, ["plugin:engineering"])
        installer.install_project(self.source, self.project, ["plugin:marketing"])

        agents = self.project / ".agents"
        for relative in (
            "skills/engineering__craft/SKILL.md",
            "skills/marketing__craft/SKILL.md",
            "rules/engineering__defaults.md",
            "rules/marketing__defaults.md",
            "agents/engineering__reviewer.md",
            "agents/marketing__reviewer.md",
        ):
            self.assertTrue((agents / relative).exists(), relative)
        self.assertEqual(len(self._lock()["components"]), 8)

    def test_unknown_and_unmanaged_conflicts_are_preflighted_without_partial_plan(self) -> None:
        with self.assertRaises(installer.SelectorError):
            installer.install_project(self.source, self.project, ["command:engineering/missing"])
        self.assertFalse((self.project / ".agents").exists())

        unmanaged = self.project / ".agents" / "commands" / "review.md"
        unmanaged.parent.mkdir(parents=True)
        unmanaged.write_text("user-owned\n", encoding="utf-8")
        with self.assertRaises(installer.UnmanagedTargetError):
            installer.install_project(self.source, self.project, ["plugin:engineering"])
        self.assertEqual(unmanaged.read_text(encoding="utf-8"), "user-owned\n")
        self.assertFalse((self.project / ".agents" / "skills").exists())
        self.assertFalse((self.project / ".agents" / ".plugin-lock.json").exists())

    def test_lock_ownership_conflict_is_rejected_before_target_changes(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        before = target.read_bytes()
        lock_path = self.project / ".agents" / ".plugin-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        entry = lock["components"].pop("command:engineering/review")
        lock["components"]["command:other/review"] = entry
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

        with self.assertRaises(installer.OwnershipConflictError):
            installer.install_project(self.source, self.project, selector)
        self.assertEqual(target.read_bytes(), before)

    def test_source_repository_ownership_change_is_rejected(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        before = target.read_bytes()
        lock_path = self.project / ".agents" / ".plugin-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["components"]["command:engineering/review"]["source_repository"] = "other/repo"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

        with self.assertRaises(installer.OwnershipConflictError):
            installer.install_project(self.source, self.project, selector)
        self.assertEqual(target.read_bytes(), before)

    def test_reinstall_is_idempotent_and_preserves_complete_lock(self) -> None:
        installer.install_project(self.source, self.project, ["plugin:engineering"])
        lock_path = self.project / ".agents" / ".plugin-lock.json"
        before_lock = lock_path.read_bytes()
        before_command = (self.project / ".agents" / "commands" / "review.md").read_bytes()

        result = installer.install_project(self.source, self.project, ["plugin:engineering"])

        self.assertEqual(lock_path.read_bytes(), before_lock)
        self.assertEqual(
            (self.project / ".agents" / "commands" / "review.md").read_bytes(),
            before_command,
        )
        self.assertEqual(len(self._lock()["components"]), 4)
        self.assertFalse(result.changed)

    def test_fresh_install_reports_changed(self) -> None:
        result = installer.install_project(
            self.source,
            self.project,
            ["command:engineering/review"],
        )
        self.assertTrue(result.changed)

    def test_new_global_collision_atomically_migrates_existing_managed_target(self) -> None:
        shutil.rmtree(self.source / "marketing")
        installer.install_project(self.source, self.project, ["plugin:engineering"])
        old_skill = self.project / ".agents" / "skills" / "craft"
        (old_skill / "local.md").write_text("preserve me\n", encoding="utf-8")
        self._write_plugin(
            "marketing",
            skills={"craft": {"SKILL.md": "---\nname: craft\ndescription: Marketing craft.\n---\n"}},
            commands={"publish": "publish\n"},
            rules={"defaults": "marketing defaults\n"},
            agents={"reviewer": "marketing reviewer\n"},
        )

        result = installer.install_project(self.source, self.project, ["plugin:marketing"])

        agents = self.project / ".agents"
        migrated = agents / "skills" / "engineering__craft"
        self.assertFalse(old_skill.exists())
        self.assertEqual((migrated / "local.md").read_text(encoding="utf-8"), "preserve me\n")
        self.assertTrue((agents / "skills" / "marketing__craft" / "SKILL.md").is_file())
        self.assertFalse((agents / "agents" / "reviewer.md").exists())
        self.assertTrue((agents / "agents" / "engineering__reviewer.md").is_file())
        self.assertTrue((agents / "agents" / "marketing__reviewer.md").is_file())
        lock = self._lock()["components"]
        self.assertEqual(lock["skill:engineering/craft"]["target"], "skills/engineering__craft")
        self.assertEqual(len(lock), 8)
        self.assertTrue(any("migrate" in action for action in result.actions))

    def test_topology_migration_rerenders_stable_locked_component_links(self) -> None:
        shutil.rmtree(self.source / "marketing")
        source_command = self.source / "engineering" / "commands" / "review.md"
        native_command = "Run [craft](../skills/craft/SKILL.md)\nbase command\n"
        source_command.write_text(native_command, encoding="utf-8")
        installer.install_project(self.source, self.project, ["plugin:engineering"])

        installed_command = self.project / ".agents" / "commands" / "review.md"
        self.assertIn(
            "../skills/craft/SKILL.md",
            installed_command.read_text(encoding="utf-8"),
        )
        installed_command.write_text(
            installed_command.read_text(encoding="utf-8") + "local note\n",
            encoding="utf-8",
        )
        self._write_plugin(
            "marketing",
            skills={
                "craft": {
                    "SKILL.md": "---\nname: craft\ndescription: Marketing craft.\n---\n"
                }
            },
            commands={"publish": "publish\n"},
            rules={"defaults": "marketing defaults\n"},
            agents={"reviewer": "marketing reviewer\n"},
        )

        result = installer.install_project(
            self.source,
            self.project,
            ["plugin:marketing"],
        )

        rendered_command = installed_command.read_text(encoding="utf-8")
        self.assertIn(
            "../skills/engineering__craft/SKILL.md",
            rendered_command,
        )
        self.assertNotIn("../skills/craft/SKILL.md", rendered_command)
        self.assertIn("local note\n", rendered_command)
        self.assertIn("command:engineering/review", result.selected)
        self.assertFalse(result.conflicts)
        self.assertEqual(source_command.read_text(encoding="utf-8"), native_command)

    def test_safe_qualification_is_closed_under_future_topology(self) -> None:
        shutil.rmtree(self.source / "engineering")
        shutil.rmtree(self.source / "marketing")
        for plugin in ("a", "b"):
            self._write_plugin(
                plugin,
                skills={
                    "foo": {
                        "SKILL.md": f"---\nname: foo\ndescription: {plugin} foo.\n---\n"
                    }
                },
                commands={},
                rules={},
                agents={},
            )
        installer.install_project(self.source, self.project, ["plugin:a", "plugin:b"])

        agents = self.project / ".agents"
        current_a = agents / "skills" / "a__foo"
        legacy_a = agents / "skills" / "a-foo"
        current_a.rename(legacy_a)
        (legacy_a / "local.md").write_text("preserve a\n", encoding="utf-8")
        lock_path = agents / ".plugin-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["components"]["skill:a/foo"]["target"] = "skills/a-foo"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

        self._write_plugin(
            "c",
            skills={
                "a-foo": {
                    "SKILL.md": "---\nname: a-foo\ndescription: c a-foo.\n---\n"
                }
            },
            commands={},
            rules={},
            agents={},
        )
        catalog = installer.scan_catalog(self.source)
        self.assertEqual(
            {
                identity: component.target_relative.as_posix()
                for identity, component in catalog.components.items()
            },
            {
                "skill:a/foo": "skills/a__foo",
                "skill:b/foo": "skills/b__foo",
                "skill:c/a-foo": "skills/a-foo",
            },
        )

        result = installer.install_project(self.source, self.project, ["plugin:c"])

        self.assertEqual(
            (agents / "skills" / "a__foo" / "local.md").read_text(
                encoding="utf-8"
            ),
            "preserve a\n",
        )
        self.assertIn(
            "description: c a-foo.",
            (agents / "skills" / "a-foo" / "SKILL.md").read_text(
                encoding="utf-8"
            ),
        )
        self.assertFalse((agents / "skills" / "a-foo" / "local.md").exists())
        targets = {
            identity: entry["target"]
            for identity, entry in self._lock()["components"].items()
        }
        self.assertEqual(
            targets,
            {
                "skill:a/foo": "skills/a__foo",
                "skill:b/foo": "skills/b__foo",
                "skill:c/a-foo": "skills/a-foo",
            },
        )
        self.assertEqual(
            result.selected,
            ("skill:a/foo", "skill:b/foo", "skill:c/a-foo"),
        )
        self.assertTrue(any("migrate" in action for action in result.actions))

    def test_collision_migration_stops_if_new_target_is_unmanaged(self) -> None:
        shutil.rmtree(self.source / "marketing")
        installer.install_project(self.source, self.project, ["plugin:engineering"])
        old_skill = self.project / ".agents" / "skills" / "craft"
        self._write_plugin(
            "marketing",
            skills={"craft": {"SKILL.md": "---\nname: craft\ndescription: Marketing craft.\n---\n"}},
            commands={"publish": "publish\n"},
            rules={"defaults": "marketing defaults\n"},
            agents={"reviewer": "marketing reviewer\n"},
        )
        unmanaged = self.project / ".agents" / "skills" / "engineering__craft"
        unmanaged.mkdir()
        (unmanaged / "SKILL.md").write_text("unmanaged\n", encoding="utf-8")

        with self.assertRaises(installer.UnmanagedTargetError):
            installer.install_project(self.source, self.project, ["plugin:marketing"])

        self.assertTrue((old_skill / "SKILL.md").is_file())
        self.assertEqual((unmanaged / "SKILL.md").read_text(encoding="utf-8"), "unmanaged\n")
        self.assertFalse((self.project / ".agents" / "skills" / "marketing__craft").exists())

    def test_disjoint_local_and_upstream_changes_merge(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        target.write_text("alpha local\nmiddle\nomega\n", encoding="utf-8")
        (self.source / "engineering" / "commands" / "review.md").write_text(
            "alpha\nmiddle\nomega upstream\n",
            encoding="utf-8",
        )

        result = installer.install_project(self.source, self.project, selector)

        self.assertEqual(target.read_text(encoding="utf-8"), "alpha local\nmiddle\nomega upstream\n")
        self.assertFalse(result.conflicts)
        self.assertTrue(any("merged disjoint" in action for action in result.actions))

    def test_same_line_conflict_keeps_local_and_stages_incoming(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        target.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        incoming = self.source / "engineering" / "commands" / "review.md"
        incoming.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")

        preview = installer.install_project(self.source, self.project, selector, dry_run=True)
        self.assertEqual(target.read_text(encoding="utf-8"), "local\nmiddle\nomega\n")
        self.assertEqual(len(preview.conflicts), 1)
        self.assertFalse((self.project / ".agents" / ".updates").exists())

        result = installer.install_project(self.source, self.project, selector)

        self.assertEqual(target.read_text(encoding="utf-8"), "local\nmiddle\nomega\n")
        staged = (
            self.project
            / ".agents"
            / ".updates"
            / installer.scan_catalog(self.source).components[
                "command:engineering/review"
            ].state_tag
            / "review.md"
        )
        self.assertEqual(staged.read_text(encoding="utf-8"), incoming.read_text(encoding="utf-8"))
        self.assertEqual(len(result.conflicts), 1)
        lock_entry = self._lock()["components"]["command:engineering/review"]
        self.assertEqual(len(lock_entry["conflicts"]), 1)
        conflict = lock_entry["conflicts"][0]
        self.assertEqual(conflict["base_state"], "present")
        self.assertEqual(
            conflict["id"],
            installer.conflict_id("command:engineering/review", "review.md"),
        )
        conflict_base = self.project / ".agents" / conflict["base"]
        self.assertEqual(
            conflict_base.read_text(encoding="utf-8"),
            "alpha\nmiddle\nomega\n",
        )
        self.assertEqual(
            installer._staged_artifact_digest(  # type: ignore[attr-defined]
                conflict_base.parent, conflict_base.name
            ),
            conflict["base_sha256"],
        )
        saved_base = (
            self.project / ".agents" / lock_entry["base_snapshot"] / installer.SINGLE_FILE_KEY
        )
        self.assertEqual(saved_base.read_text(encoding="utf-8"), "upstream\nmiddle\nomega\n")

        unresolved = installer.install_project(self.source, self.project, selector)
        self.assertEqual(len(unresolved.conflicts), 1)
        self.assertEqual(
            len(self._lock()["components"]["command:engineering/review"]["conflicts"]),
            1,
        )

        target.write_text(incoming.read_text(encoding="utf-8"), encoding="utf-8")
        resolved = installer.install_project(self.source, self.project, selector)
        self.assertFalse(resolved.conflicts)
        self.assertEqual(
            self._lock()["components"]["command:engineering/review"]["conflicts"],
            [],
        )
        self.assertFalse(staged.exists())
        self.assertFalse(conflict_base.exists())

    def test_accept_local_conflict_is_selective_and_preserves_semantic_merge(self) -> None:
        source_skill = self.source / "engineering" / "skills" / "craft"
        source_first = source_skill / "first.md"
        source_second = source_skill / "second.md"
        source_first.write_text("alpha\nmiddle\nomega\n", encoding="utf-8")
        source_second.write_text("one\ntwo\nthree\n", encoding="utf-8")
        selector = ["skill:engineering/craft"]
        installer.install_project(self.source, self.project, selector)
        agents = self.project / ".agents"
        target = agents / "skills" / "engineering__craft"
        target_first = target / "first.md"
        target_second = target / "second.md"
        target_first.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        target_second.write_text("local two\ntwo\nthree\n", encoding="utf-8")
        source_first.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")
        source_second.write_text("upstream two\ntwo\nthree\n", encoding="utf-8")
        conflicted = installer.install_project(self.source, self.project, selector)
        self.assertEqual(len(conflicted.conflicts), 2)

        lock_path = agents / ".plugin-lock.json"
        identity = "skill:engineering/craft"
        entry = self._lock()["components"][identity]
        by_path = {conflict["path"]: conflict for conflict in entry["conflicts"]}
        selected = by_path["first.md"]
        remaining = by_path["second.md"]
        target_first.write_text(
            "semantic local and upstream\nmiddle\nomega\n", encoding="utf-8"
        )
        updates = agents / installer.UPDATE_DIRECTORY
        conflict_bases = agents / installer.CONFLICT_BASE_DIRECTORY
        base_snapshot = agents / entry["base_snapshot"]

        def adoption_state() -> dict[str, object]:
            return {
                "target": self._file_tree(target),
                "lock": lock_path.read_bytes(),
                "updates": self._file_tree(updates),
                "conflict_bases": self._file_tree(conflict_bases),
                "base_snapshot": self._file_tree(base_snapshot),
            }

        before = adoption_state()
        preview = installer.accept_local_conflicts(
            self.project, [selected["id"]], dry_run=True
        )
        self.assertTrue(preview.dry_run)
        self.assertEqual(preview.items[0].conflict_id, selected["id"])
        self.assertEqual(preview.items[0].local_state, "present")
        self.assertEqual(adoption_state(), before)

        adopted = installer.accept_local_conflicts(
            self.project, [selected["id"]]
        )
        self.assertFalse(adopted.dry_run)
        self.assertEqual(target_first.read_bytes(), before["target"]["first.md"])
        self.assertEqual(target_second.read_bytes(), before["target"]["second.md"])
        self.assertEqual(self._file_tree(base_snapshot), before["base_snapshot"])
        remaining_conflicts = self._lock()["components"][identity]["conflicts"]
        self.assertEqual(remaining_conflicts, [remaining])
        self.assertFalse((agents / selected["staged"]).exists())
        self.assertTrue((agents / remaining["staged"]).is_file())
        self.assertFalse((agents / selected["base"]).parent.exists())
        self.assertTrue((agents / remaining["base"]).is_file())

        source_first.write_text(
            "upstream\nmiddle\nomega newer\n", encoding="utf-8"
        )
        refreshed = installer.install_project(self.source, self.project, selector)
        self.assertEqual(
            target_first.read_text(encoding="utf-8"),
            "semantic local and upstream\nmiddle\nomega newer\n",
        )
        self.assertEqual(len(refreshed.conflicts), 1)
        self.assertIn("second.md", refreshed.conflicts[0])

    def test_accept_local_conflict_rejects_unknown_and_tampered_state(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        agents = self.project / ".agents"
        target = agents / "commands" / "review.md"
        target.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        incoming = self.source / "engineering" / "commands" / "review.md"
        incoming.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")
        installer.install_project(self.source, self.project, selector)
        conflict = self._lock()["components"]["command:engineering/review"]["conflicts"][0]
        lock_path = agents / ".plugin-lock.json"
        staged = agents / conflict["staged"]
        saved_base = agents / conflict["base"]

        base_snapshot = agents / self._lock()["components"][
            "command:engineering/review"
        ]["base_snapshot"]

        def state() -> tuple[
            bytes,
            bytes,
            dict[str, bytes],
            dict[str, bytes],
            dict[str, bytes],
        ]:
            return (
                target.read_bytes(),
                lock_path.read_bytes(),
                self._file_tree(agents / installer.UPDATE_DIRECTORY),
                self._file_tree(agents / installer.CONFLICT_BASE_DIRECTORY),
                self._file_tree(base_snapshot),
            )

        before = state()
        unknown = "0" * 16 if conflict["id"] != "0" * 16 else "1" * 16
        with self.assertRaisesRegex(installer.InstallerError, "unknown unresolved"):
            installer.accept_local_conflicts(self.project, [unknown])
        self.assertEqual(state(), before)
        with self.assertRaisesRegex(installer.InstallerError, "must not be repeated"):
            installer.accept_local_conflicts(
                self.project, [conflict["id"], conflict["id"]]
            )
        self.assertEqual(state(), before)

        staged_original = staged.read_bytes()
        staged.write_text("tampered incoming\n", encoding="utf-8")
        tampered_staged = state()
        with self.assertRaisesRegex(
            installer.OwnershipConflictError, "staged update is missing or modified"
        ):
            installer.accept_local_conflicts(self.project, [conflict["id"]])
        self.assertEqual(state(), tampered_staged)
        staged.write_bytes(staged_original)

        saved_base_original = saved_base.read_bytes()
        saved_base.write_text("tampered base\n", encoding="utf-8")
        tampered_base = state()
        with self.assertRaisesRegex(
            installer.OwnershipConflictError,
            "saved conflict base is missing or modified",
        ):
            installer.accept_local_conflicts(self.project, [conflict["id"]])
        self.assertEqual(state(), tampered_base)
        saved_base.write_bytes(saved_base_original)

        operational_base = base_snapshot / installer.SINGLE_FILE_KEY
        operational_base.write_text("tampered operational base\n", encoding="utf-8")
        tampered_operational_base = state()
        with self.assertRaisesRegex(
            installer.OwnershipConflictError,
            "saved upstream base was modified",
        ):
            installer.accept_local_conflicts(self.project, [conflict["id"]])
        self.assertEqual(state(), tampered_operational_base)

    def test_accept_local_conflict_rolls_back_partial_state_swap(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        agents = self.project / ".agents"
        target = agents / "commands" / "review.md"
        target.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        incoming = self.source / "engineering" / "commands" / "review.md"
        incoming.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")
        installer.install_project(self.source, self.project, selector)

        identity = "command:engineering/review"
        conflict = self._lock()["components"][identity]["conflicts"][0]
        lock_path = agents / ".plugin-lock.json"
        updates = agents / installer.UPDATE_DIRECTORY
        conflict_bases = agents / installer.CONFLICT_BASE_DIRECTORY
        update_root = updates / installer._state_tag(identity)
        before = {
            "target": target.read_bytes(),
            "lock": lock_path.read_bytes(),
            "updates": self._file_tree(updates),
            "conflict_bases": self._file_tree(conflict_bases),
        }
        real_replace = os.replace
        successful_replaces: list[tuple[Path, Path]] = []
        injected_failure = False

        def fail_after_state_swap(source: object, destination: object) -> None:
            nonlocal injected_failure
            source_path = Path(source)
            destination_path = Path(destination)
            if successful_replaces and not injected_failure:
                injected_failure = True
                raise OSError("injected conflict-base swap failure")
            real_replace(source, destination)
            successful_replaces.append((source_path, destination_path))

        with mock.patch.object(
            installer.os, "replace", side_effect=fail_after_state_swap
        ):
            with self.assertRaisesRegex(OSError, "injected conflict-base swap failure"):
                installer.accept_local_conflicts(self.project, [conflict["id"]])

        self.assertEqual(successful_replaces[0][0], update_root.resolve())
        self.assertTrue(injected_failure)
        self.assertEqual(target.read_bytes(), before["target"])
        self.assertEqual(lock_path.read_bytes(), before["lock"])
        self.assertEqual(self._file_tree(updates), before["updates"])
        self.assertEqual(
            self._file_tree(conflict_bases), before["conflict_bases"]
        )
        self.assertEqual(list(self.project.glob(".plugin-accept-*")), [])

    def test_accept_local_conflict_rejects_local_change_after_preview(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        agents = self.project / ".agents"
        target = agents / "commands" / "review.md"
        target.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        incoming = self.source / "engineering" / "commands" / "review.md"
        incoming.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")
        installer.install_project(self.source, self.project, selector)

        conflict = self._lock()["components"][
            "command:engineering/review"
        ]["conflicts"][0]
        preview = installer.accept_local_conflicts(
            self.project, [conflict["id"]], dry_run=True
        )
        self.assertEqual(len(preview.items), 1)
        target.write_text("changed after review\nmiddle\nomega\n", encoding="utf-8")

        lock_path = agents / ".plugin-lock.json"
        updates = agents / installer.UPDATE_DIRECTORY
        conflict_bases = agents / installer.CONFLICT_BASE_DIRECTORY
        after_change = {
            "target": target.read_bytes(),
            "lock": lock_path.read_bytes(),
            "updates": self._file_tree(updates),
            "conflict_bases": self._file_tree(conflict_bases),
        }
        with self.assertRaisesRegex(
            installer.OwnershipConflictError, "changed after review"
        ):
            installer.accept_local_conflicts(
                self.project,
                [conflict["id"]],
                expected_local_digests={
                    conflict["id"]: preview.items[0].local_sha256
                },
            )

        self.assertEqual(target.read_bytes(), after_change["target"])
        self.assertEqual(lock_path.read_bytes(), after_change["lock"])
        self.assertEqual(self._file_tree(updates), after_change["updates"])
        self.assertEqual(
            self._file_tree(conflict_bases), after_change["conflict_bases"]
        )

    def test_accept_local_conflicts_adopts_multiple_components_atomically(self) -> None:
        selectors = [
            "command:engineering/review",
            "command:marketing/publish",
        ]
        installer.install_project(self.source, self.project, selectors)
        agents = self.project / ".agents"
        targets = {
            "command:engineering/review": agents / "commands" / "review.md",
            "command:marketing/publish": agents / "commands" / "publish.md",
        }
        sources = {
            "command:engineering/review": self.source
            / "engineering"
            / "commands"
            / "review.md",
            "command:marketing/publish": self.source
            / "marketing"
            / "commands"
            / "publish.md",
        }
        for identity, target in targets.items():
            target.write_text(f"local {identity}\n", encoding="utf-8")
            sources[identity].write_text(
                f"upstream {identity}\n", encoding="utf-8"
            )
        conflicted = installer.install_project(self.source, self.project, selectors)
        self.assertEqual(len(conflicted.conflicts), 2)
        lock = self._lock()["components"]
        conflicts = {
            identity: lock[identity]["conflicts"][0] for identity in targets
        }
        before_targets = {
            identity: target.read_bytes() for identity, target in targets.items()
        }

        result = installer.accept_local_conflicts(
            self.project,
            [conflicts[identity]["id"] for identity in sorted(conflicts)],
        )

        self.assertEqual(len(result.items), 2)
        final_lock = self._lock()["components"]
        for identity, target in targets.items():
            self.assertEqual(target.read_bytes(), before_targets[identity])
            self.assertEqual(final_lock[identity]["conflicts"], [])
            self.assertFalse((agents / conflicts[identity]["staged"]).exists())
            self.assertFalse(
                (agents / conflicts[identity]["base"]).parent.exists()
            )

    def test_personalization_and_local_additions_survive_reinstall(self) -> None:
        selector = ["skill:engineering/craft"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "skills" / "engineering__craft"
        (target / "personalize.local.yml").write_text("user: Ada\n", encoding="utf-8")
        (target / "settings.local.json").write_text('{"tone":"direct"}\n', encoding="utf-8")
        (target / "notes.md").write_text("local notes\n", encoding="utf-8")
        source_skill = self.source / "engineering" / "skills" / "craft"
        (source_skill / "SKILL.md").write_text(
            "---\nname: craft\ndescription: Updated engineering craft.\n---\n",
            encoding="utf-8",
        )
        (source_skill / "settings.local.json").write_text('{"tone":"upstream"}\n', encoding="utf-8")
        (source_skill / "notes.md").write_text("upstream notes\n", encoding="utf-8")

        result = installer.install_project(self.source, self.project, selector)

        self.assertEqual((target / "personalize.local.yml").read_text(encoding="utf-8"), "user: Ada\n")
        self.assertEqual((target / "settings.local.json").read_text(encoding="utf-8"), '{"tone":"direct"}\n')
        self.assertEqual((target / "notes.md").read_text(encoding="utf-8"), "local notes\n")
        self.assertIn("Updated engineering craft", (target / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(len(result.conflicts), 1)

    def test_source_caches_and_source_local_overlays_are_not_distributed(self) -> None:
        source_skill = self.source / "engineering" / "skills" / "craft"
        cache = source_skill / "scripts" / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "helper.pyc").write_bytes(b"cache")
        (source_skill / "personalize.local.yml").write_text("private: true\n", encoding="utf-8")
        (source_skill / "settings.local.json").write_text("{}\n", encoding="utf-8")

        installer.install_project(
            self.source,
            self.project,
            ["skill:engineering/craft"],
        )

        target = self.project / ".agents" / "skills" / "engineering__craft"
        self.assertFalse((target / "scripts" / "__pycache__").exists())
        self.assertFalse((target / "personalize.local.yml").exists())
        self.assertFalse((target / "settings.local.json").exists())

    def test_upstream_deletions_remove_only_unchanged_files(self) -> None:
        selector = ["skill:engineering/craft"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "skills" / "engineering__craft"
        (target / "keep.md").write_text("locally changed\n", encoding="utf-8")
        source_skill = self.source / "engineering" / "skills" / "craft"
        (source_skill / "remove.md").unlink()
        (source_skill / "keep.md").unlink()

        installer.install_project(self.source, self.project, selector)

        self.assertFalse((target / "remove.md").exists())
        self.assertEqual((target / "keep.md").read_text(encoding="utf-8"), "locally changed\n")

    def test_upstream_directory_deletion_preserves_local_additions_below_it(self) -> None:
        source_skill = self.source / "engineering" / "skills" / "craft"
        obsolete = source_skill / "obsolete"
        obsolete.mkdir()
        (obsolete / "tracked.md").write_text("tracked\n", encoding="utf-8")
        selector = ["skill:engineering/craft"]
        installer.install_project(self.source, self.project, selector)
        target_obsolete = (
            self.project / ".agents" / "skills" / "engineering__craft" / "obsolete"
        )
        (target_obsolete / "local.md").write_text("local addition\n", encoding="utf-8")
        shutil.rmtree(obsolete)

        installer.install_project(self.source, self.project, selector)

        self.assertFalse((target_obsolete / "tracked.md").exists())
        self.assertEqual((target_obsolete / "local.md").read_text(encoding="utf-8"), "local addition\n")

    def test_directory_to_file_transition_preserves_local_subtree_and_stages_incoming(self) -> None:
        source_skill = self.source / "engineering" / "skills" / "craft"
        shape = source_skill / "shape"
        shape.mkdir()
        (shape / "tracked.md").write_text("tracked\n", encoding="utf-8")
        selector = ["skill:engineering/craft"]
        installer.install_project(self.source, self.project, selector)
        target_shape = self.project / ".agents" / "skills" / "engineering__craft" / "shape"
        (target_shape / "local.md").write_text("preserve me\n", encoding="utf-8")
        shutil.rmtree(shape)
        shape.write_text("incoming file\n", encoding="utf-8")

        preview = installer.install_project(self.source, self.project, selector, dry_run=True)
        self.assertEqual(len(preview.conflicts), 1)
        self.assertEqual((target_shape / "local.md").read_text(encoding="utf-8"), "preserve me\n")

        result = installer.install_project(self.source, self.project, selector)
        self.assertEqual(len(result.conflicts), 1)
        self.assertTrue(target_shape.is_dir())
        self.assertEqual((target_shape / "local.md").read_text(encoding="utf-8"), "preserve me\n")
        component = installer.scan_catalog(self.source).components["skill:engineering/craft"]
        staged = self.project / ".agents" / ".updates" / component.state_tag / "shape"
        self.assertEqual(staged.read_text(encoding="utf-8"), "incoming file\n")

    def test_file_to_directory_transition_preserves_local_file_and_stages_tree(self) -> None:
        source_skill = self.source / "engineering" / "skills" / "craft"
        shape = source_skill / "shape"
        shape.write_text("base file\n", encoding="utf-8")
        selector = ["skill:engineering/craft"]
        installer.install_project(self.source, self.project, selector)
        target_shape = self.project / ".agents" / "skills" / "engineering__craft" / "shape"
        target_shape.write_text("local file\n", encoding="utf-8")
        shape.unlink()
        shape.mkdir()
        (shape / "incoming.md").write_text("incoming child\n", encoding="utf-8")

        result = installer.install_project(self.source, self.project, selector)

        self.assertEqual(len(result.conflicts), 1)
        self.assertEqual(target_shape.read_text(encoding="utf-8"), "local file\n")
        component = installer.scan_catalog(self.source).components["skill:engineering/craft"]
        staged_child = (
            self.project
            / ".agents"
            / ".updates"
            / component.state_tag
            / "shape"
            / "incoming.md"
        )
        self.assertEqual(staged_child.read_text(encoding="utf-8"), "incoming child\n")

    def test_dry_run_writes_nothing_and_update_uses_full_lock(self) -> None:
        dry = installer.install_project(
            self.source,
            self.project,
            ["plugin:engineering"],
            dry_run=True,
        )
        self.assertTrue(dry.dry_run)
        self.assertFalse((self.project / ".agents").exists())

        installer.install_project(self.source, self.project, ["plugin:engineering"])
        installer.install_project(self.source, self.project, ["plugin:marketing"])
        target = self.project / ".agents" / "commands" / "publish.md"
        (self.source / "marketing" / "commands" / "publish.md").write_text(
            "publish updated\n",
            encoding="utf-8",
        )
        before_lock = (self.project / ".agents" / ".plugin-lock.json").read_bytes()
        installer.update_project(self.source, self.project, dry_run=True)
        self.assertEqual(target.read_text(encoding="utf-8"), "publish\n")
        self.assertEqual((self.project / ".agents" / ".plugin-lock.json").read_bytes(), before_lock)

        installer.update_project(self.source, self.project)
        self.assertEqual(target.read_text(encoding="utf-8"), "publish updated\n")
        self.assertEqual(len(self._lock()["components"]), 8)

    def test_default_update_preserves_removed_upstream_component_and_updates_rest(self) -> None:
        selectors = ["command:engineering/review", "command:marketing/publish"]
        installer.install_project(self.source, self.project, selectors)
        review = self.project / ".agents" / "commands" / "review.md"
        publish = self.project / ".agents" / "commands" / "publish.md"
        (self.source / "engineering" / "commands" / "review.md").unlink()
        (self.source / "marketing" / "commands" / "publish.md").write_text(
            "publish updated\n", encoding="utf-8"
        )

        result = installer.update_project(self.source, self.project)

        self.assertEqual(review.read_text(encoding="utf-8"), "alpha\nmiddle\nomega\n")
        self.assertEqual(publish.read_text(encoding="utf-8"), "publish updated\n")
        self.assertIn("command:engineering/review", self._lock()["components"])
        self.assertTrue(any("preserved orphaned" in action for action in result.actions))

    def test_default_update_installs_known_rename_and_preserves_predecessor(self) -> None:
        old_identity = "command:engineering/review"
        new_identity = "command:engineering/review-next"
        installer.install_project(self.source, self.project, [old_identity])
        old_target = self.project / ".agents" / "commands" / "review.md"
        source_old = self.source / "engineering" / "commands" / "review.md"
        source_new = source_old.with_name("review-next.md")
        source_old.rename(source_new)
        source_new.write_text("current replacement\n", encoding="utf-8")

        with mock.patch.dict(
            installer.COMPONENT_RENAMES, {old_identity: new_identity}, clear=False
        ):
            result = installer.update_project(self.source, self.project)

        new_target = self.project / ".agents" / "commands" / "review-next.md"
        self.assertEqual(old_target.read_text(encoding="utf-8"), "alpha\nmiddle\nomega\n")
        self.assertEqual(new_target.read_text(encoding="utf-8"), "current replacement\n")
        self.assertTrue(
            {old_identity, new_identity}.issubset(self._lock()["components"])
        )
        self.assertTrue(any("installed current replacement" in action for action in result.actions))

    def test_deleted_single_file_and_skill_directory_remain_absent(self) -> None:
        selectors = ["command:engineering/review", "skill:engineering/craft"]
        installer.install_project(self.source, self.project, selectors)
        command = self.project / ".agents" / "commands" / "review.md"
        skill = self.project / ".agents" / "skills" / "engineering__craft"
        command.unlink()
        shutil.rmtree(skill)

        result = installer.install_project(self.source, self.project, selectors)

        self.assertFalse(result.conflicts)
        self.assertFalse(command.exists())
        self.assertFalse(skill.exists())
        self.assertEqual(len(self._lock()["components"]), 2)

        (self.source / "engineering" / "commands" / "review.md").write_text(
            "upstream changed\n", encoding="utf-8"
        )
        conflicted = installer.install_project(
            self.source, self.project, ["command:engineering/review"]
        )
        self.assertEqual(len(conflicted.conflicts), 1)
        self.assertFalse(command.exists())

    def test_keyboard_interrupt_rolls_back_all_completed_swaps(self) -> None:
        selectors = ["command:engineering/review", "command:marketing/publish"]
        installer.install_project(self.source, self.project, selectors)
        review = self.project / ".agents" / "commands" / "review.md"
        publish = self.project / ".agents" / "commands" / "publish.md"
        lock_path = self.project / ".agents" / ".plugin-lock.json"
        before = (review.read_bytes(), publish.read_bytes(), lock_path.read_bytes())
        (self.source / "engineering" / "commands" / "review.md").write_text(
            "review changed\n", encoding="utf-8"
        )
        (self.source / "marketing" / "commands" / "publish.md").write_text(
            "publish changed\n", encoding="utf-8"
        )
        real_replace = installer.os.replace
        calls = 0

        def interrupt_fourth(source: object, target: object) -> None:
            nonlocal calls
            calls += 1
            if calls == 4:
                raise KeyboardInterrupt()
            real_replace(source, target)

        with mock.patch.object(installer.os, "replace", side_effect=interrupt_fourth):
            with self.assertRaises(KeyboardInterrupt):
                installer.install_project(self.source, self.project, selectors)

        self.assertEqual(
            (review.read_bytes(), publish.read_bytes(), lock_path.read_bytes()), before
        )
        self.assertEqual(list(self.project.glob(".plugin-install-*")), [])

    def test_corrupted_lock_target_and_source_are_rejected_without_mutation(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        readme = self.project / ".agents" / "README.md"
        readme.write_text("user runtime notes\n", encoding="utf-8")
        lock_path = self.project / ".agents" / ".plugin-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["components"]["command:engineering/review"]["target"] = "README.md"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

        with self.assertRaises(installer.OwnershipConflictError):
            installer.install_project(self.source, self.project, selector)
        self.assertEqual(readme.read_text(encoding="utf-8"), "user runtime notes\n")
        self.assertEqual(target.read_text(encoding="utf-8"), "alpha\nmiddle\nomega\n")

        lock["components"]["command:engineering/review"]["target"] = "commands/review.md"
        lock["components"]["command:engineering/review"]["source"] = "marketing/commands/publish.md"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        with self.assertRaises(installer.OwnershipConflictError):
            installer.install_project(
                self.source, self.project, ["command:marketing/publish"]
            )
        self.assertEqual(target.read_text(encoding="utf-8"), "alpha\nmiddle\nomega\n")
        self.assertFalse((self.project / ".agents" / "commands" / "publish.md").exists())

    def test_stale_conflict_is_cleared_after_disjoint_upstream_change(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        incoming = self.source / "engineering" / "commands" / "review.md"
        target.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        incoming.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")
        first = installer.install_project(self.source, self.project, selector)
        self.assertEqual(len(first.conflicts), 1)
        staged_relative = self._lock()["components"]["command:engineering/review"]["conflicts"][0]["staged"]
        staged = self.project / ".agents" / staged_relative
        incoming.write_text("upstream\nmiddle\nomega newer\n", encoding="utf-8")

        second = installer.install_project(self.source, self.project, selector)

        self.assertFalse(second.conflicts)
        self.assertEqual(target.read_text(encoding="utf-8"), "local\nmiddle\nomega newer\n")
        self.assertEqual(self._lock()["components"]["command:engineering/review"]["conflicts"], [])
        self.assertFalse(staged.exists())

    def test_locally_modified_staged_conflict_fails_closed(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        incoming = self.source / "engineering" / "commands" / "review.md"
        target.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        incoming.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")
        installer.install_project(self.source, self.project, selector)
        conflict = self._lock()["components"]["command:engineering/review"]["conflicts"][0]
        staged = self.project / ".agents" / conflict["staged"]
        staged.write_text("reviewed but not applied\n", encoding="utf-8")
        incoming.write_text("new upstream\nmiddle\nomega\n", encoding="utf-8")

        with self.assertRaisesRegex(installer.OwnershipConflictError, "locally modified"):
            installer.install_project(self.source, self.project, selector)

        self.assertEqual(staged.read_text(encoding="utf-8"), "reviewed but not applied\n")
        self.assertEqual(target.read_text(encoding="utf-8"), "local\nmiddle\nomega\n")

    def test_locally_modified_saved_conflict_base_fails_closed(self) -> None:
        selector = ["command:engineering/review"]
        installer.install_project(self.source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        incoming = self.source / "engineering" / "commands" / "review.md"
        target.write_text("local\nmiddle\nomega\n", encoding="utf-8")
        incoming.write_text("upstream\nmiddle\nomega\n", encoding="utf-8")
        installer.install_project(self.source, self.project, selector)
        conflict = self._lock()["components"]["command:engineering/review"]["conflicts"][0]
        saved_base = self.project / ".agents" / conflict["base"]
        saved_base.write_text("tampered ancestor\n", encoding="utf-8")
        incoming.write_text("new upstream\nmiddle\nomega\n", encoding="utf-8")

        with self.assertRaisesRegex(
            installer.OwnershipConflictError, "saved conflict base was modified"
        ):
            installer.install_project(self.source, self.project, selector)

        self.assertEqual(saved_base.read_text(encoding="utf-8"), "tampered ancestor\n")
        self.assertEqual(target.read_text(encoding="utf-8"), "local\nmiddle\nomega\n")

    def test_staged_conflict_symlink_ancestor_cannot_escape_updates_root(self) -> None:
        source_skill = self.source / "engineering" / "skills" / "craft"
        nested = source_skill / "nested"
        nested.mkdir()
        incoming = nested / "artifact.md"
        incoming.write_text("base\n", encoding="utf-8")
        selector = ["skill:engineering/craft"]
        installer.install_project(self.source, self.project, selector)
        target = (
            self.project
            / ".agents"
            / "skills"
            / "engineering__craft"
            / "nested"
            / "artifact.md"
        )
        target.write_text("local\n", encoding="utf-8")
        incoming.write_text("upstream\n", encoding="utf-8")
        installer.install_project(self.source, self.project, selector)
        conflict = self._lock()["components"]["skill:engineering/craft"]["conflicts"][0]
        staged = self.project / ".agents" / conflict["staged"]
        outside = self.temporary / "outside-updates"
        outside.mkdir()
        sentinel = outside / "artifact.md"
        sentinel.write_text("outside sentinel\n", encoding="utf-8")
        shutil.rmtree(staged.parent)
        os.symlink(outside, staged.parent)

        with self.assertRaisesRegex(
            installer.UnsafePathError, "symlink|staged update root"
        ):
            installer.install_project(self.source, self.project, selector)

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "outside sentinel\n")
        self.assertEqual(target.read_text(encoding="utf-8"), "local\n")

    def test_source_category_symlinks_are_rejected(self) -> None:
        for category in ("skills", "commands", "rules", "agents"):
            with self.subTest(category=category):
                source_category = self.source / "engineering" / category
                outside = self.temporary / f"outside-{category}"
                shutil.copytree(source_category, outside)
                shutil.rmtree(source_category)
                os.symlink(outside, source_category)
                try:
                    with self.assertRaises(installer.UnsafePathError):
                        installer.scan_catalog(self.source)
                    self.assertFalse((self.project / ".agents").exists())
                finally:
                    source_category.unlink()
                    shutil.copytree(outside, source_category)

    def test_source_symlink_is_rejected_without_following_cycle(self) -> None:
        source_skill = self.source / "engineering" / "skills" / "craft"
        os.symlink(source_skill, source_skill / "cycle")
        with self.assertRaises(installer.UnsafePathError):
            installer.install_project(self.source, self.project, ["skill:engineering/craft"])
        self.assertFalse((self.project / ".agents").exists())

    def test_project_category_symlink_cannot_redirect_install_writes(self) -> None:
        outside = self.temporary / "outside"
        outside.mkdir()
        agents = self.project / ".agents"
        agents.mkdir()
        os.symlink(outside, agents / "skills")

        with self.assertRaises(installer.UnsafePathError):
            installer.install_project(self.source, self.project, ["skill:engineering/craft"])

        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((agents / ".plugin-lock.json").exists())


if __name__ == "__main__":
    unittest.main()
