from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SKILLCTL_PATH = ROOT / "scripts" / "skillctl.py"
SPEC = importlib.util.spec_from_file_location("skillctl_project_runtime", SKILLCTL_PATH)
assert SPEC and SPEC.loader
skillctl = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = skillctl
SPEC.loader.exec_module(skillctl)


class SkillctlProjectRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = Path(tempfile.mkdtemp(prefix="skillctl-runtime-test-"))
        self.project = self.temporary / "project"
        self.project.mkdir()
        (self.project / "README.md").write_text("# User project\n\nKeep this text.\n", encoding="utf-8")
        (self.project / "AGENTS.md").write_text("# User instructions\n", encoding="utf-8")
        (self.project / ".gitignore").write_text("dist/\n", encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.temporary)

    def _install_args(self) -> SimpleNamespace:
        return SimpleNamespace(
            root=str(ROOT),
            project=str(self.project),
            selectors=[
                "skill:marketing/seo",
                "command:marketing/content-brief",
                "rule:marketing/defaults",
                "agent:marketing/growth-lead",
            ],
            yes=True,
            dry_run=False,
            verbose=False,
            no_sync_docs=False,
        )

    def _component_source(self) -> tuple[Path, Path]:
        source = self.temporary / "component-source"
        command = source / "engineering" / "commands" / "review.md"
        command.parent.mkdir(parents=True)
        (source / "engineering" / "profile.yaml").write_text(
            "slug: engineering\n", encoding="utf-8"
        )
        command.write_text("alpha\nmiddle\nomega\n", encoding="utf-8")
        references = source / "references"
        references.mkdir()
        (references / "agent-runtime-rule.md").write_text(
            "Use installed runtime components safely.\n", encoding="utf-8"
        )
        return source, command

    def _component_conflict(
        self,
        *,
        local: str = "local\nmiddle\nomega\n",
        incoming: str = "upstream\nmiddle\nomega\n",
    ) -> tuple[Path, Path, Path, dict[str, object]]:
        source, source_command = self._component_source()
        selector = ["command:engineering/review"]
        skillctl.project_installer.install_project(source, self.project, selector)
        target = self.project / ".agents" / "commands" / "review.md"
        target.write_text(local, encoding="utf-8")
        source_command.write_text(incoming, encoding="utf-8")
        result = skillctl.project_installer.install_project(
            source, self.project, selector
        )
        self.assertEqual(len(result.conflicts), 1)
        lock = json.loads(
            (self.project / ".agents" / ".plugin-lock.json").read_text(
                encoding="utf-8"
            )
        )
        conflict = lock["components"]["command:engineering/review"]["conflicts"][0]
        return source, source_command, target, conflict

    def _skill_source(self) -> tuple[Path, Path]:
        source = self.temporary / "skill-source"
        skill = source / "engineering" / "skills" / "craft"
        skill.mkdir(parents=True)
        (source / "engineering" / "profile.yaml").write_text(
            "slug: engineering\n", encoding="utf-8"
        )
        (skill / "SKILL.md").write_text(
            "---\nname: craft\ndescription: Engineering craft.\n---\n",
            encoding="utf-8",
        )
        references = source / "references"
        references.mkdir()
        (references / "agent-runtime-rule.md").write_text(
            "Use installed runtime components safely.\n", encoding="utf-8"
        )
        return source, skill

    def _reconcile_args(
        self, source: Path, output: str | None
    ) -> SimpleNamespace:
        return SimpleNamespace(
            root=str(source),
            project=str(self.project),
            selectors=[],
            output=output,
        )

    def _synthetic_root_conflict(
        self,
    ) -> tuple[str, str, Path, Path, Path, bytes]:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        agents = self.project / ".agents"
        lock_path = agents / ".plugin-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        identity = "command:marketing/content-brief"
        entry = lock["components"][identity]
        target = agents / entry["target"]
        local = target.read_bytes() + b"\nReviewed semantic local resolution.\n"
        target.write_bytes(local)
        displayed_path = target.name
        item_id = skillctl.project_installer.conflict_id(identity, displayed_path)
        state_tag = skillctl.project_installer._state_tag(identity)
        staged_relative = (
            Path(skillctl.project_installer.UPDATE_DIRECTORY)
            / state_tag
            / displayed_path
        )
        staged = agents / staged_relative
        staged.parent.mkdir(parents=True)
        staged.write_text("synthetic incoming update\n", encoding="utf-8")
        incoming_digest = skillctl.project_installer._staged_artifact_digest(
            staged.parent, staged.name
        )
        base_relative = (
            Path(skillctl.project_installer.CONFLICT_BASE_DIRECTORY)
            / state_tag
            / item_id
            / "content"
        )
        saved_base = agents / base_relative
        saved_base.parent.mkdir(parents=True)
        shutil.copy2(
            agents
            / entry["base_snapshot"]
            / skillctl.project_installer.SINGLE_FILE_KEY,
            saved_base,
        )
        base_digest = skillctl.project_installer._staged_artifact_digest(
            saved_base.parent, saved_base.name
        )
        operational_base = (
            agents
            / entry["base_snapshot"]
            / skillctl.project_installer.SINGLE_FILE_KEY
        )
        operational_base.write_bytes(staged.read_bytes())
        entry["files"] = {displayed_path: incoming_digest}
        entry["conflicts"] = [
            {
                "id": item_id,
                "path": displayed_path,
                "staged": staged_relative.as_posix(),
                "reason": "synthetic integration conflict",
                "incoming_sha256": incoming_digest,
                "base_state": "present",
                "base_sha256": base_digest,
                "base": base_relative.as_posix(),
            }
        ]
        lock_path.write_text(
            json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        skillctl._sync_project_runtime(
            ROOT, self.project, sync_docs=False, dry_run=False
        )
        return identity, item_id, target, staged, saved_base, local

    @staticmethod
    def _file_tree(root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    @staticmethod
    def _bundle_value(
        bundle: Path, entry: dict[str, object], variant: str
    ) -> bytes:
        record = entry[variant]
        assert isinstance(record, dict)
        relative = record["bundle_path"]
        assert isinstance(relative, str)
        return (bundle / relative).read_bytes()

    def test_install_syncs_flat_runtime_and_preserves_project_docs(self) -> None:
        stdout = StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)

        agents = self.project / ".agents"
        self.assertTrue((agents / "skills" / "seo" / "SKILL.md").is_file())
        self.assertTrue(
            (agents / "skills" / "context-to-content" / "SKILL.md").is_file()
        )
        self.assertTrue((agents / "commands" / "content-brief.md").is_file())
        self.assertTrue((agents / "rules" / "marketing__defaults.md").is_file())
        self.assertTrue((agents / "agents" / "growth-lead.md").is_file())
        self.assertFalse((agents / "marketing").exists())
        for relative in (
            ".plugin-lock.json",
            ".plugin-support-lock.json",
            "component-graph.json",
            "registry.json",
            "runtime-contract.json",
            "personalization.example.json",
            "runtime-support/install-external-skills.py",
            "runtime-support/external-skills.yaml",
            "runtime-support/external-sources.yaml",
            "runtime-support/skills-chaining-map.md",
            "runtime-support/INSTALLATION.md",
            "runtime-support/promotion-matrix.md",
            "README.md",
        ):
            self.assertTrue((agents / relative).is_file(), relative)

        support_lock = json.loads(
            (agents / ".plugin-support-lock.json").read_text(encoding="utf-8")
        )
        self.assertIn(
            "runtime-support/install-external-skills.py", support_lock["files"]
        )
        installed_chain_map = (
            agents / "runtime-support" / "skills-chaining-map.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "[`external-skills.yaml`](external-skills.yaml)", installed_chain_map
        )
        self.assertIn(
            "[`external-sources.yaml`](external-sources.yaml)", installed_chain_map
        )
        self.assertNotIn(
            "](references/external-skills.yaml)", installed_chain_map
        )
        self.assertNotIn(
            "](references/external-sources.yaml)", installed_chain_map
        )
        for registry_name in ("external-skills.yaml", "external-sources.yaml"):
            self.assertTrue(
                (agents / "runtime-support" / registry_name).is_file(),
                registry_name,
            )

        installed_installation = (
            agents / "runtime-support" / "INSTALLATION.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "python3 .agents/runtime-support/install-external-skills.py",
            installed_installation,
        )
        self.assertNotIn(
            "python .agents/runtime-support/install-external-skills.py",
            installed_installation,
        )

        readme = (self.project / "README.md").read_text(encoding="utf-8")
        self.assertIn("Keep this text.", readme)
        self.assertIn("agent-plugins:installed-components:start", readme)
        gitignore = (self.project / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("dist/", gitignore)
        self.assertIn("# agent-plugins:local-runtime-files:start", gitignore)
        self.assertNotIn("<!--", gitignore)

        registry = json.loads((agents / "registry.json").read_text(encoding="utf-8"))
        seo = next(item for item in registry["components"] if item["id"] == "skill:marketing/seo")
        self.assertNotEqual(seo["description"], ">-")
        self.assertEqual(seo["status"], "current")

        output = stdout.getvalue()
        self.assertIn("Plan: 5 components", output)
        self.assertIn(
            "(required by command:marketing/content-brief)",
            output,
        )
        self.assertNotIn(": added upstream", output)

    def test_unmanaged_support_file_is_not_overwritten_or_partially_installed(self) -> None:
        agents = self.project / ".agents"
        agents.mkdir()
        unmanaged = agents / "runtime-contract.json"
        unmanaged.write_text('{"owner":"another-runtime"}\n', encoding="utf-8")

        with redirect_stdout(StringIO()):
            with self.assertRaisesRegex(skillctl.SkillctlError, "unmanaged support file"):
                skillctl.install_components(self._install_args())

        self.assertEqual(
            unmanaged.read_text(encoding="utf-8"),
            '{"owner":"another-runtime"}\n',
        )
        self.assertFalse((agents / ".plugin-lock.json").exists())

    def test_lockless_marker_shaped_support_edit_is_preserved_and_rejected(self) -> None:
        agents = self.project / ".agents"
        agents.mkdir()
        unmanaged = agents / "runtime-contract.json"
        content = json.dumps(
            {
                "$schema": "https://example.test/schemas/runtime-contract.schema.json",
                "user_edit": "keep me",
            },
            indent=2,
        ) + "\n"
        unmanaged.write_text(content, encoding="utf-8")

        with redirect_stdout(StringIO()):
            with self.assertRaisesRegex(skillctl.SkillctlError, "unmanaged support file"):
                skillctl.install_components(self._install_args())

        self.assertEqual(unmanaged.read_text(encoding="utf-8"), content)
        self.assertFalse((agents / ".plugin-lock.json").exists())

    def test_locally_modified_managed_support_file_is_preserved(self) -> None:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        contract = self.project / ".agents" / "runtime-contract.json"
        contract.write_text('{"local":"custom contract"}\n', encoding="utf-8")

        with redirect_stdout(StringIO()):
            with self.assertRaisesRegex(
                skillctl.SkillctlError, "locally modified managed support file"
            ):
                skillctl.install_components(self._install_args())

        self.assertEqual(
            contract.read_text(encoding="utf-8"),
            '{"local":"custom contract"}\n',
        )

    def test_ai_edit_inside_managed_project_block_is_preserved_and_blocks_update(self) -> None:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        readme = self.project / "README.md"
        edited = readme.read_text(encoding="utf-8").replace(
            "## Agent components", "## Agent components\n\nAI-maintained project note."
        )
        readme.write_text(edited, encoding="utf-8")

        with redirect_stdout(StringIO()):
            with self.assertRaisesRegex(
                skillctl.SkillctlError, "locally modified managed.*block"
            ):
                skillctl.install_components(self._install_args())

        self.assertIn("AI-maintained project note.", readme.read_text(encoding="utf-8"))

    def test_reinstall_preserves_personalization_local_edits_and_conflict_status(self) -> None:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        agents = self.project / ".agents"
        local_values = agents / "personalization.local.json"
        local_values.write_text(
            json.dumps({"project": {"name": "Atlas"}}, indent=2) + "\n",
            encoding="utf-8",
        )
        before_values = local_values.read_bytes()
        installed_skill = agents / "skills" / "seo" / "SKILL.md"
        installed_skill.write_text(
            installed_skill.read_text(encoding="utf-8") + "\nLocal project note.\n",
            encoding="utf-8",
        )

        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)

        self.assertEqual(local_values.read_bytes(), before_values)
        self.assertIn("Local project note.", installed_skill.read_text(encoding="utf-8"))
        self.assertIn("Keep this text.", (self.project / "README.md").read_text(encoding="utf-8"))

        lock_path = agents / ".plugin-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["components"]["skill:marketing/seo"]["conflicts"] = [
            {
                "path": "SKILL.md",
                "staged": ".updates/example/SKILL.md",
                "reason": "test conflict",
                "incoming_sha256": "0" * 64,
            }
        ]
        lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
        skillctl._sync_project_runtime(ROOT, self.project, sync_docs=True, dry_run=False)
        registry = json.loads((agents / "registry.json").read_text(encoding="utf-8"))
        seo = next(item for item in registry["components"] if item["id"] == "skill:marketing/seo")
        self.assertEqual(seo["status"], "conflicted")

    def test_count_summary_uses_singular_labels(self) -> None:
        self.assertEqual(
            skillctl._count_summary({"skill": 1, "command": 1, "rule": 1, "agent": 1}),
            "1 skill, 1 command, 1 rule, and 1 agent",
        )

    def test_deleted_component_is_marked_missing_and_not_available(self) -> None:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        agents = self.project / ".agents"
        shutil.rmtree(agents / "skills" / "seo")

        skillctl._sync_project_runtime(ROOT, self.project, sync_docs=True, dry_run=False)

        graph = json.loads((agents / "component-graph.json").read_text(encoding="utf-8"))
        seo_node = next(node for node in graph["nodes"] if node["id"] == "skill:marketing/seo")
        self.assertFalse(seo_node["installed"])
        registry = json.loads((agents / "registry.json").read_text(encoding="utf-8"))
        seo_entry = next(
            item for item in registry["components"] if item["id"] == "skill:marketing/seo"
        )
        self.assertEqual(seo_entry["status"], "missing")

        args = SimpleNamespace(
            project=str(self.project),
            component="skill:marketing/seo",
            set=[],
            session=[],
            allow_missing=True,
        )
        with self.assertRaisesRegex(skillctl.SkillctlError, "not installed"):
            skillctl.resolve_runtime_context(args)

    def test_installed_graph_resolution_filters_unavailable_candidates(self) -> None:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        args = SimpleNamespace(
            project=str(self.project),
            root=str(ROOT),
            component="skill:marketing/seo",
            relation=["chains-to"],
            available_only=True,
        )

        stdout = StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(skillctl.graph_resolve(args), 0)
        result = json.loads(stdout.getvalue())

        self.assertEqual(result["availability_filter"], "exclude-installed-false")
        self.assertEqual(result["levels"][0]["candidates"], ["skill:marketing/seo"])
        self.assertTrue(result["blocked_edges"])
        self.assertTrue(result["unavailable_nodes"])

    def test_context_cli_renders_dynamic_values_and_raw_arguments(self) -> None:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        (self.project / "prompt.txt").write_text(
            "Audit {{site.url}} for $ARGUMENTS.\n", encoding="utf-8"
        )
        args = SimpleNamespace(
            project=str(self.project),
            component="skill:marketing/seo",
            set=["site.url=https://example.test"],
            session=[],
            allow_missing=False,
            render="prompt.txt",
            output="rendered.txt",
            arguments="AI search visibility",
        )

        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.resolve_runtime_context(args), 0)

        self.assertEqual(
            (self.project / "rendered.txt").read_text(encoding="utf-8"),
            "Audit https://example.test for AI search visibility.\n",
        )

    def test_support_preflight_rejects_project_doc_symlink_before_install(self) -> None:
        sentinel = self.temporary / "outside-readme.md"
        sentinel.write_text("Outside content.\n", encoding="utf-8")
        project_readme = self.project / "README.md"
        project_readme.unlink()
        project_readme.symlink_to(sentinel)

        with redirect_stdout(StringIO()):
            with self.assertRaisesRegex(
                skillctl.SkillctlError, "managed path cannot traverse a symlink"
            ):
                skillctl.install_components(self._install_args())

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "Outside content.\n")
        self.assertFalse((self.project / ".agents" / ".plugin-lock.json").exists())

    def test_reconcile_exports_exact_component_triplet_without_mutating_runtime(self) -> None:
        source, _source_command, target, conflict = self._component_conflict()
        agents = self.project / ".agents"
        personalization = agents / "personalization.local.json"
        personalization.write_text(
            json.dumps({"project": {"name": "Atlas"}}, indent=2) + "\n",
            encoding="utf-8",
        )
        staged = agents / str(conflict["staged"])
        before = {
            "target": target.read_bytes(),
            "lock": (agents / ".plugin-lock.json").read_bytes(),
            "personalization": personalization.read_bytes(),
            "staged": staged.read_bytes(),
            "state": self._file_tree(agents / ".plugin-state"),
        }

        first = self.project / "reconcile-one"
        second = self.project / "reconcile-two"
        with redirect_stdout(StringIO()):
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(source, first.name)
                ),
                0,
            )
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(source, second.name)
                ),
                0,
            )

        manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["review_sha256"],
            skillctl._text_sha256((first / "REVIEW.md").read_text(encoding="utf-8")),
        )
        component_entries = [
            entry for entry in manifest["entries"] if entry["scope"] == "component"
        ]
        self.assertEqual(len(component_entries), 1)
        entry = component_entries[0]
        self.assertEqual(entry["identity"], "command:engineering/review")
        self.assertEqual(
            self._bundle_value(first, entry, "base"),
            b"alpha\nmiddle\nomega\n",
        )
        self.assertEqual(
            self._bundle_value(first, entry, "local"),
            b"local\nmiddle\nomega\n",
        )
        self.assertEqual(
            self._bundle_value(first, entry, "incoming"),
            b"upstream\nmiddle\nomega\n",
        )
        self.assertEqual(self._file_tree(first), self._file_tree(second))
        self.assertFalse((first / "suggested.patch").exists())
        self.assertEqual(target.read_bytes(), before["target"])
        self.assertEqual((agents / ".plugin-lock.json").read_bytes(), before["lock"])
        self.assertEqual(personalization.read_bytes(), before["personalization"])
        self.assertEqual(staged.read_bytes(), before["staged"])
        self.assertEqual(self._file_tree(agents / ".plugin-state"), before["state"])

    def test_reconcile_default_output_uses_content_addressed_updates_path(self) -> None:
        source, _source_command, _target, _conflict = self._component_conflict()
        output = StringIO()

        with redirect_stdout(output):
            self.assertEqual(
                skillctl.reconcile_installs(self._reconcile_args(source, None)),
                0,
            )

        relative = output.getvalue().strip()
        self.assertTrue(relative.startswith(".agents/.updates/reconcile/"), relative)
        bundle = self.project / relative
        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(bundle.parent, self.project / ".agents/.updates/reconcile")
        self.assertEqual(bundle.name, manifest["bundle_id"])
        self.assertTrue((bundle / "REVIEW.md").is_file())

    def test_reconcile_exports_skill_subtree_conflict_losslessly(self) -> None:
        source, source_skill = self._skill_source()
        source_shape = source_skill / "shape"
        source_shape.mkdir()
        (source_shape / "tracked.md").write_text("tracked\n", encoding="utf-8")
        selector = ["skill:engineering/craft"]
        skillctl.project_installer.install_project(source, self.project, selector)
        local_shape = self.project / ".agents" / "skills" / "craft" / "shape"
        (local_shape / "local.md").write_text("local addition\n", encoding="utf-8")
        shutil.rmtree(source_shape)
        source_shape.write_text("incoming file\n", encoding="utf-8")
        result = skillctl.project_installer.install_project(
            source, self.project, selector
        )
        self.assertEqual(len(result.conflicts), 1)

        bundle = self.project / "subtree-reconcile"
        with redirect_stdout(StringIO()):
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(source, bundle.name)
                ),
                0,
            )

        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        entry = next(item for item in manifest["entries"] if item["scope"] == "component")
        self.assertEqual(entry["target"], ".agents/skills/craft/shape")
        self.assertEqual(entry["base"]["state"], "directory")
        self.assertEqual(entry["local"]["state"], "directory")
        self.assertEqual(entry["incoming"]["state"], "file")
        base = bundle / entry["base"]["bundle_path"]
        local = bundle / entry["local"]["bundle_path"]
        self.assertEqual(self._file_tree(base), {"tracked.md": b"tracked\n"})
        self.assertEqual(
            self._file_tree(local),
            {
                "local.md": b"local addition\n",
                "tracked.md": b"tracked\n",
            },
        )
        self.assertEqual(
            self._bundle_value(bundle, entry, "incoming"), b"incoming file\n"
        )

    def test_reconcile_marks_genuinely_missing_base_without_artifact(self) -> None:
        source, source_skill = self._skill_source()
        selector = ["skill:engineering/craft"]
        skillctl.project_installer.install_project(source, self.project, selector)
        local = self.project / ".agents" / "skills" / "craft" / "new.md"
        local.write_text("local addition\n", encoding="utf-8")
        (source_skill / "new.md").write_text("upstream addition\n", encoding="utf-8")
        result = skillctl.project_installer.install_project(
            source, self.project, selector
        )
        self.assertEqual(len(result.conflicts), 1)

        bundle = self.project / "missing-base-reconcile"
        with redirect_stdout(StringIO()):
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(source, bundle.name)
                ),
                0,
            )

        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        entry = next(item for item in manifest["entries"] if item["scope"] == "component")
        self.assertEqual(
            entry["base"],
            {
                "state": "missing",
                "sha256": None,
                "bundle_path": None,
                "utf8_text": True,
            },
        )
        self.assertEqual(
            self._bundle_value(bundle, entry, "local"), b"local addition\n"
        )
        self.assertEqual(
            self._bundle_value(bundle, entry, "incoming"), b"upstream addition\n"
        )

    def test_reconcile_marks_legacy_conflict_base_unavailable(self) -> None:
        source, _source_command, _target, _conflict = self._component_conflict()
        lock_path = self.project / ".agents" / ".plugin-lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        conflict = lock["components"]["command:engineering/review"]["conflicts"][0]
        for field in ("id", "base_state", "base_sha256", "base"):
            conflict.pop(field, None)
        lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

        bundle = self.project / "legacy-reconcile"
        with redirect_stdout(StringIO()):
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(source, bundle.name)
                ),
                0,
            )

        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        entry = next(item for item in manifest["entries"] if item["scope"] == "component")
        self.assertEqual(
            entry["base"],
            {
                "state": "unavailable",
                "sha256": None,
                "bundle_path": None,
                "utf8_text": False,
            },
        )
        self.assertEqual(
            self._bundle_value(bundle, entry, "local"),
            b"local\nmiddle\nomega\n",
        )
        self.assertEqual(
            self._bundle_value(bundle, entry, "incoming"),
            b"upstream\nmiddle\nomega\n",
        )

    def test_reconcile_marks_binary_variants_non_text_and_preserves_bytes(self) -> None:
        source, source_skill = self._skill_source()
        source_binary = source_skill / "payload.bin"
        source_binary.write_bytes(b"\xffbase\x00")
        selector = ["skill:engineering/craft"]
        skillctl.project_installer.install_project(source, self.project, selector)
        local_binary = self.project / ".agents" / "skills" / "craft" / "payload.bin"
        local_binary.write_bytes(b"\xfflocal\x00")
        source_binary.write_bytes(b"\xffincoming\x00")
        result = skillctl.project_installer.install_project(
            source, self.project, selector
        )
        self.assertEqual(len(result.conflicts), 1)

        bundle = self.project / "binary-reconcile"
        with redirect_stdout(StringIO()):
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(source, bundle.name)
                ),
                0,
            )

        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        entry = next(item for item in manifest["entries"] if item["scope"] == "component")
        for variant, expected in (
            ("base", b"\xffbase\x00"),
            ("local", b"\xfflocal\x00"),
            ("incoming", b"\xffincoming\x00"),
        ):
            self.assertFalse(entry[variant]["utf8_text"])
            self.assertEqual(self._bundle_value(bundle, entry, variant), expected)

    def test_reconcile_exports_only_bounded_agents_and_readme_blocks(self) -> None:
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.install_components(self._install_args()), 0)
        agents = self.project / ".agents"
        agents_doc = self.project / "AGENTS.md"
        readme = self.project / "README.md"
        outside_sentinel = "outside-project-context-must-not-be-exported"
        agents_doc.write_text(
            agents_doc.read_text(encoding="utf-8").replace(
                "# User instructions",
                f"# User instructions\n\n{outside_sentinel}",
            ).replace(
                "## Installed agent runtime",
                "## Installed agent runtime\n\nLocal AGENTS reconciliation note.",
            ),
            encoding="utf-8",
        )
        readme.write_text(
            readme.read_text(encoding="utf-8").replace(
                "## Agent components",
                "## Agent components\n\nLocal README reconciliation note.",
            ),
            encoding="utf-8",
        )
        personalization = agents / "personalization.local.json"
        personalization_secret = "api_key=personalization-secret-123456"
        personalization.write_text(personalization_secret + "\n", encoding="utf-8")
        before = {
            "agents": agents_doc.read_bytes(),
            "readme": readme.read_bytes(),
            "component_lock": (agents / ".plugin-lock.json").read_bytes(),
            "support_lock": (agents / ".plugin-support-lock.json").read_bytes(),
            "personalization": personalization.read_bytes(),
        }

        bundle = self.project / "doc-reconcile"
        with redirect_stdout(StringIO()):
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(ROOT, bundle.name)
                ),
                0,
            )

        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        entries = {
            entry["identity"]: entry
            for entry in manifest["entries"]
            if entry["scope"] == "managed-block"
        }
        self.assertEqual(
            set(entries),
            {"AGENTS.md#installed-runtime", "README.md#installed-components"},
        )
        agents_entry = entries["AGENTS.md#installed-runtime"]
        readme_entry = entries["README.md#installed-components"]
        self.assertIn(
            b"Local AGENTS reconciliation note.",
            self._bundle_value(bundle, agents_entry, "local"),
        )
        self.assertIn(
            b"Local README reconciliation note.",
            self._bundle_value(bundle, readme_entry, "local"),
        )
        self.assertEqual(
            self._bundle_value(bundle, agents_entry, "base"),
            self._bundle_value(bundle, agents_entry, "incoming"),
        )
        self.assertEqual(
            self._bundle_value(bundle, readme_entry, "base"),
            self._bundle_value(bundle, readme_entry, "incoming"),
        )
        exported = b"\n".join(self._file_tree(bundle).values())
        self.assertNotIn(outside_sentinel.encode("utf-8"), exported)
        self.assertNotIn(personalization_secret.encode("utf-8"), exported)
        self.assertEqual(agents_doc.read_bytes(), before["agents"])
        self.assertEqual(readme.read_bytes(), before["readme"])
        self.assertEqual((agents / ".plugin-lock.json").read_bytes(), before["component_lock"])
        self.assertEqual((agents / ".plugin-support-lock.json").read_bytes(), before["support_lock"])
        self.assertEqual(personalization.read_bytes(), before["personalization"])

        with self.assertRaisesRegex(
            skillctl.project_installer.InstallerError,
            "unknown unresolved conflict id",
        ):
            skillctl.reconcile_installs(
                SimpleNamespace(
                    root=str(ROOT),
                    project=str(self.project),
                    selectors=[],
                    output=None,
                    accept_local=[str(agents_entry["id"])],
                    dry_run=False,
                    yes=True,
                )
            )
        self.assertEqual(agents_doc.read_bytes(), before["agents"])
        self.assertEqual(readme.read_bytes(), before["readme"])

    def test_reconcile_with_no_conflicts_creates_no_bundle(self) -> None:
        source, _source_command = self._component_source()
        skillctl.project_installer.install_project(
            source, self.project, ["command:engineering/review"]
        )
        output = StringIO()
        destination = self.project / "no-conflicts"

        with redirect_stdout(output):
            self.assertEqual(
                skillctl.reconcile_installs(
                    self._reconcile_args(source, destination.name)
                ),
                0,
            )

        self.assertIn("No unresolved", output.getvalue())
        self.assertFalse(destination.exists())

    def test_reconcile_rejects_tampered_staged_incoming_without_output(self) -> None:
        source, _source_command, target, conflict = self._component_conflict()
        agents = self.project / ".agents"
        lock = (agents / ".plugin-lock.json").read_bytes()
        staged = agents / str(conflict["staged"])
        staged.write_text("tampered incoming\n", encoding="utf-8")
        destination = self.project / "tampered-reconcile"

        with self.assertRaisesRegex(
            skillctl.SkillctlError, "staged incoming artifact is missing or modified"
        ):
            skillctl.reconcile_installs(
                self._reconcile_args(source, destination.name)
            )

        self.assertFalse(destination.exists())
        self.assertEqual(target.read_text(encoding="utf-8"), "local\nmiddle\nomega\n")
        self.assertEqual((agents / ".plugin-lock.json").read_bytes(), lock)
        self.assertEqual(staged.read_text(encoding="utf-8"), "tampered incoming\n")

    def test_reconcile_rejects_tampered_saved_base_without_output(self) -> None:
        source, _source_command, target, conflict = self._component_conflict()
        agents = self.project / ".agents"
        lock = (agents / ".plugin-lock.json").read_bytes()
        saved_base = agents / str(conflict["base"])
        saved_base.write_text("tampered ancestor\n", encoding="utf-8")
        destination = self.project / "tampered-base-reconcile"

        with self.assertRaisesRegex(
            skillctl.SkillctlError, "saved base artifact is missing or modified"
        ):
            skillctl.reconcile_installs(
                self._reconcile_args(source, destination.name)
            )

        self.assertFalse(destination.exists())
        self.assertEqual(target.read_text(encoding="utf-8"), "local\nmiddle\nomega\n")
        self.assertEqual((agents / ".plugin-lock.json").read_bytes(), lock)
        self.assertEqual(saved_base.read_text(encoding="utf-8"), "tampered ancestor\n")

    def test_reconcile_rejects_output_inside_managed_agents_namespace(self) -> None:
        source, _source_command, _target, _conflict = self._component_conflict()
        args = self._reconcile_args(source, ".agents/skills/reconcile-output")

        with self.assertRaisesRegex(
            skillctl.SkillctlError, "inside .agents must remain under"
        ):
            skillctl.reconcile_installs(args)

        self.assertFalse(self.project.joinpath(args.output).exists())

    def test_reconcile_rejects_output_symlink_without_writing_outside(self) -> None:
        source, _source_command, _target, _conflict = self._component_conflict()
        outside = self.temporary / "outside-reconcile"
        outside.mkdir()
        (self.project / "bundle-link").symlink_to(outside, target_is_directory=True)

        with self.assertRaisesRegex(
            skillctl.SkillctlError, "reconciliation output cannot traverse a symlink"
        ):
            skillctl.reconcile_installs(
                self._reconcile_args(source, "bundle-link/reconcile")
            )

        self.assertEqual(list(outside.iterdir()), [])

    def test_reconcile_accept_local_updates_registry_without_touching_target(self) -> None:
        identity, item_id, target, staged, saved_base, local = (
            self._synthetic_root_conflict()
        )
        agents = self.project / ".agents"
        lock_path = agents / ".plugin-lock.json"
        before_lock = lock_path.read_bytes()
        registry_path = agents / "registry.json"
        unchanged_runtime = {
            path: path.read_bytes()
            for path in (
                self.project / "AGENTS.md",
                self.project / "README.md",
                self.project / ".gitignore",
                agents / "runtime-contract.json",
                agents / "component-graph.json",
                agents / "README.md",
                agents / "rules" / "agent-runtime.md",
                agents / "runtime-support" / "INSTALLATION.md",
            )
        }
        conflicted_registry = json.loads(registry_path.read_text(encoding="utf-8"))
        conflicted_entry = next(
            entry for entry in conflicted_registry["components"] if entry["id"] == identity
        )
        self.assertEqual(conflicted_entry["status"], "conflicted")
        args = SimpleNamespace(
            root=str(ROOT),
            project=str(self.project),
            selectors=[],
            output=None,
            accept_local=[item_id],
            dry_run=False,
            yes=False,
        )
        before_dry_run = {
            "target": target.read_bytes(),
            "lock": lock_path.read_bytes(),
            "registry": registry_path.read_bytes(),
            "support_lock": (agents / ".plugin-support-lock.json").read_bytes(),
            "staged": staged.read_bytes(),
            "base": saved_base.read_bytes(),
        }
        args.dry_run = True
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.reconcile_installs(args), 0)
        self.assertEqual(target.read_bytes(), before_dry_run["target"])
        self.assertEqual(lock_path.read_bytes(), before_dry_run["lock"])
        self.assertEqual(registry_path.read_bytes(), before_dry_run["registry"])
        self.assertEqual(
            (agents / ".plugin-support-lock.json").read_bytes(),
            before_dry_run["support_lock"],
        )
        self.assertEqual(staged.read_bytes(), before_dry_run["staged"])
        self.assertEqual(saved_base.read_bytes(), before_dry_run["base"])
        args.dry_run = False

        with mock.patch.object(
            skillctl.sys, "stdin", SimpleNamespace(isatty=lambda: False)
        ), redirect_stdout(StringIO()):
            with self.assertRaisesRegex(
                skillctl.SkillctlError,
                "non-interactive conflict adoption requires --yes",
            ):
                skillctl.reconcile_installs(args)
        self.assertEqual(target.read_bytes(), local)
        self.assertEqual(lock_path.read_bytes(), before_lock)
        self.assertTrue(staged.is_file())
        self.assertTrue(saved_base.is_file())

        args.yes = True
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(skillctl.reconcile_installs(args), 0)

        self.assertIn("Plan: 1 current local conflict resolution", output.getvalue())
        self.assertIn("Adopted: 1 current local conflict resolution", output.getvalue())
        self.assertEqual(target.read_bytes(), local)
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(lock["components"][identity]["conflicts"], [])
        self.assertFalse(staged.exists())
        self.assertFalse(saved_base.parent.exists())
        for path, content in unchanged_runtime.items():
            self.assertEqual(path.read_bytes(), content)
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        current_entry = next(
            entry for entry in registry["components"] if entry["id"] == identity
        )
        self.assertEqual(current_entry["status"], "current")

    def test_reconcile_accept_local_rejects_incompatible_flags(self) -> None:
        base = {
            "root": str(ROOT),
            "project": str(self.project),
            "selectors": [],
            "output": None,
            "accept_local": ["0" * 16],
            "dry_run": False,
            "yes": True,
        }
        cases = (
            (
                {**base, "selectors": ["command:marketing/content-brief"]},
                "selectors cannot be combined",
            ),
            ({**base, "output": "bundle"}, "--output cannot be combined"),
            (
                {**base, "accept_local": [], "yes": True},
                "--dry-run and --yes require --accept-local",
            ),
        )

        for values, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(skillctl.SkillctlError, message):
                    skillctl.reconcile_installs(SimpleNamespace(**values))
        self.assertFalse((self.project / ".agents").exists())

    def test_reconcile_fails_closed_on_likely_secret_without_output(self) -> None:
        secret = "api_key=local-secret-1234567890"
        source, _source_command, target, _conflict = self._component_conflict(
            local=f"{secret}\nmiddle\nomega\n"
        )
        agents = self.project / ".agents"
        lock = (agents / ".plugin-lock.json").read_bytes()
        destination = self.project / "private-reconcile"

        with self.assertRaisesRegex(
            skillctl.SkillctlError, "likely private or credential-bearing"
        ):
            skillctl.reconcile_installs(
                self._reconcile_args(source, destination.name)
            )

        self.assertFalse(destination.exists())
        self.assertIn(secret, target.read_text(encoding="utf-8"))
        self.assertEqual((agents / ".plugin-lock.json").read_bytes(), lock)


if __name__ == "__main__":
    unittest.main()
