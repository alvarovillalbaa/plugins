from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
INSTALLER_PATH = ROOT / "scripts" / "install-external-skills.py"
SPEC = importlib.util.spec_from_file_location(
    "install_external_skills", INSTALLER_PATH
)
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class InstallExternalSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = Path(
            tempfile.mkdtemp(prefix="install-external-skills-test-")
        )
        self.project = self.temporary / "project"
        self.skills_root = self.project / ".agents" / "skills"
        self.skills_root.mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.temporary)

    def _write_runtime(self, nodes: list[dict[str, object]]) -> tuple[Path, Path]:
        agents = self.project / ".agents"
        graph_path = agents / "component-graph.json"
        graph = {
            "schema_version": "1.0",
            "artifact_kind": "component-relationship-graph",
            "contract": "references/component-graph.json",
            "nodes": nodes,
            "edges": [],
        }
        graph_text = json.dumps(graph, indent=2) + "\n"
        graph_path.write_text(graph_text, encoding="utf-8")
        lock_path = agents / ".plugin-support-lock.json"
        lock = {
            "schema_version": 1,
            "files": {
                "component-graph.json": hashlib.sha256(
                    graph_text.encode("utf-8")
                ).hexdigest(),
                "runtime-support/external-skills.yaml": "1" * 64,
            },
            "blocks": {"README.md#installed-components": "2" * 64},
        }
        lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
        return graph_path, lock_path

    def _write_registry(self) -> Path:
        registry = self.temporary / "external-skills.yaml"
        registry.write_text(
            "skills:\n"
            "  alpha:\n"
            "    owner: example\n"
            "    repo: https://example.invalid/skills.git\n"
            "    ref: main\n"
            "    path: skills/alpha\n"
            "    install_name: alpha\n"
            "    homepage: https://example.invalid/alpha\n"
            "    domain: testing\n",
            encoding="utf-8",
        )
        return registry

    def _write_upstream(self, content: str = "# Alpha\n") -> Path:
        repository = self.temporary / "upstream"
        skill = repository / "skills" / "alpha"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(content, encoding="utf-8")
        return repository

    def test_refresh_updates_all_external_flags_and_support_lock_digest(self) -> None:
        graph_path, lock_path = self._write_runtime(
            [
                {
                    "id": "external-skill:alpha",
                    "kind": "external-skill",
                    "install_name": "alpha",
                    "installed": False,
                },
                {
                    "id": "external-skill:beta",
                    "kind": "external-skill",
                    "install_name": "beta",
                    "installed": True,
                },
                {
                    "id": "external-skill:fluid-functionalism",
                    "kind": "external-skill",
                    "installable": False,
                    "installed": True,
                },
                {"id": "skill:engineering/testing", "installed": True},
            ]
        )
        alpha = self.skills_root / "alpha"
        alpha.mkdir()
        (alpha / "SKILL.md").write_text("# Alpha\n", encoding="utf-8")

        self.assertTrue(installer.refresh_project_runtime(self.skills_root))

        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        flags = {
            node["id"]: node.get("installed") for node in graph["nodes"]
        }
        self.assertTrue(flags["external-skill:alpha"])
        self.assertFalse(flags["external-skill:beta"])
        self.assertFalse(flags["external-skill:fluid-functionalism"])
        self.assertTrue(flags["skill:engineering/testing"])
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(
            lock["files"]["component-graph.json"],
            hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            lock["files"]["runtime-support/external-skills.yaml"], "1" * 64
        )
        self.assertEqual(
            lock["blocks"]["README.md#installed-components"], "2" * 64
        )

        graph_before = graph_path.read_bytes()
        lock_before = lock_path.read_bytes()
        self.assertFalse(installer.refresh_project_runtime(self.skills_root))
        self.assertEqual(graph_path.read_bytes(), graph_before)
        self.assertEqual(lock_path.read_bytes(), lock_before)

    def test_refresh_rolls_back_graph_when_support_lock_replace_fails(self) -> None:
        graph_path, lock_path = self._write_runtime(
            [
                {
                    "id": "external-skill:alpha",
                    "kind": "external-skill",
                    "install_name": "alpha",
                    "installed": True,
                }
            ]
        )
        graph_before = graph_path.read_bytes()
        lock_before = lock_path.read_bytes()
        real_replace = os.replace
        calls = 0

        def fail_second_replace(source: str | Path, destination: str | Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated support-lock replace failure")
            real_replace(source, destination)

        with mock.patch.object(installer.os, "replace", side_effect=fail_second_replace):
            with self.assertRaisesRegex(OSError, "simulated"):
                installer.refresh_project_runtime(self.skills_root)

        self.assertEqual(graph_path.read_bytes(), graph_before)
        self.assertEqual(lock_path.read_bytes(), lock_before)

    def test_project_install_refreshes_mixed_graph_and_preserves_existing_by_default(self) -> None:
        graph_path, lock_path = self._write_runtime(
            [
                {
                    "id": "external-skill:alpha",
                    "kind": "external-skill",
                    "installable": True,
                    "install_name": "alpha",
                    "installed": False,
                },
                {
                    "id": "external-skill:fluid-functionalism",
                    "kind": "external-skill",
                    "name": "fluid-functionalism",
                    "path": "references/external-sources.yaml",
                    "installable": False,
                    "owner": "mickadesign",
                    "repo": "https://github.com/mickadesign/fluid-functionalism",
                    "ref": "main",
                    "domain": "ui-design-reference",
                    "installed": False,
                },
            ]
        )
        registry = self._write_registry()
        repository = self._write_upstream("# Upstream alpha\n")
        previous_cwd = Path.cwd()
        stdout = StringIO()
        try:
            os.chdir(self.project)
            with mock.patch.object(installer, "sync_repo", return_value=repository):
                with redirect_stdout(stdout):
                    self.assertEqual(
                        installer.main(
                            [
                                "--registry",
                                str(registry),
                                "--skill",
                                "alpha",
                                "--agent",
                                "project",
                            ]
                        ),
                        0,
                    )
        finally:
            os.chdir(previous_cwd)

        installed = self.skills_root / "alpha" / "SKILL.md"
        self.assertEqual(installed.read_text(encoding="utf-8"), "# Upstream alpha\n")
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        flags = {
            node["id"]: node.get("installed") for node in graph["nodes"]
        }
        self.assertTrue(flags["external-skill:alpha"])
        self.assertFalse(flags["external-skill:fluid-functionalism"])
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(
            lock["files"]["component-graph.json"],
            hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        )
        self.assertIn("refreshed external install state", stdout.getvalue())

        installed.write_text("# Local alpha\n", encoding="utf-8")
        (repository / "skills" / "alpha" / "SKILL.md").write_text(
            "# New upstream alpha\n", encoding="utf-8"
        )
        previous_cwd = Path.cwd()
        try:
            os.chdir(self.project)
            with mock.patch.object(installer, "sync_repo", return_value=repository):
                with redirect_stdout(StringIO()):
                    self.assertEqual(
                        installer.main(
                            [
                                "--registry",
                                str(registry),
                                "--skill",
                                "alpha",
                                "--agent",
                                "project",
                            ]
                        ),
                        0,
                    )
        finally:
            os.chdir(previous_cwd)
        self.assertEqual(installed.read_text(encoding="utf-8"), "# Local alpha\n")

    def test_modified_managed_graph_fails_before_external_copy(self) -> None:
        graph_path, _lock_path = self._write_runtime(
            [
                {
                    "id": "external-skill:alpha",
                    "kind": "external-skill",
                    "install_name": "alpha",
                    "installed": False,
                }
            ]
        )
        graph_path.write_text(
            graph_path.read_text(encoding="utf-8") + "\n", encoding="utf-8"
        )
        registry = self._write_registry()
        stderr = StringIO()
        previous_cwd = Path.cwd()
        try:
            os.chdir(self.project)
            with mock.patch.object(installer, "sync_repo") as sync_repo:
                with redirect_stderr(stderr):
                    self.assertEqual(
                        installer.main(
                            [
                                "--registry",
                                str(registry),
                                "--skill",
                                "alpha",
                                "--agent",
                                "project",
                            ]
                        ),
                        1,
                    )
                sync_repo.assert_not_called()
        finally:
            os.chdir(previous_cwd)
        self.assertFalse((self.skills_root / "alpha").exists())
        self.assertIn("locally modified managed support file", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
