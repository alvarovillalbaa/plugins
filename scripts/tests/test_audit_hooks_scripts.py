from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import audit_hooks_scripts


class HookScriptAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        (self.root / "references" / "docs").mkdir(parents=True)
        (self.root / "references" / "docs" / "hooks-and-scripts.md").write_text(
            "# Hooks and Scripts\n", encoding="utf-8"
        )
        self.department = self.root / "engineering"
        (self.department / ".claude-plugin").mkdir(parents=True)
        (self.department / ".claude-plugin" / "plugin.json").write_text(
            '{"name":"engineering"}\n', encoding="utf-8"
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def add_skill(
        self, name: str, frontmatter_extra: str = "", *, document_scripts: bool = True
    ) -> Path:
        skill = self.department / "skills" / name
        skill.mkdir(parents=True)
        scripts_note = "\nUse `scripts/` for owned executable assets.\n" if document_scripts else ""
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Test skill.\n{frontmatter_extra}---\n\n# {name}\n{scripts_note}",
            encoding="utf-8",
        )
        return skill

    def add_script(self, skill: Path, name: str, body: str) -> Path:
        path = skill / "scripts" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        path.chmod(0o755)
        return path

    def test_accepts_registered_skill_hook_and_on_demand_script(self) -> None:
        extra = """hooks:
  Stop:
    - hooks:
        - type: command
          command: bash
          args:
            - "${CLAUDE_SKILL_DIR}/scripts/completion-gate.sh"
          timeout: 10
"""
        skill = self.add_skill("demo", extra)
        self.add_script(skill, "completion-gate.sh", "#!/usr/bin/env bash\nexit 0\n")
        self.add_script(skill, "render.py", "#!/usr/bin/env python3\nprint('ok')\n")

        failures, departments, skills, assets, registrations = audit_hooks_scripts.audit(self.root)

        self.assertEqual(failures, [])
        self.assertEqual(len(departments), 1)
        self.assertEqual(len(skills), 1)
        self.assertEqual(len(assets), 2)
        self.assertEqual(len(registrations), 1)
        report = audit_hooks_scripts.render_report(
            self.root, departments, skills, assets, registrations
        )
        self.assertIn("hook-handler", report)
        self.assertIn("automatic lifecycle behavior registered", report)

    def test_rejects_files_in_skill_hooks_directory_and_placeholders(self) -> None:
        skill = self.add_skill("demo")
        hook = skill / "hooks" / "pre-tool.sh"
        hook.parent.mkdir()
        hook.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        readme = skill / "scripts" / "README.md"
        readme.parent.mkdir()
        readme.write_text("# scripts\n\nPlaceholder for `demo` scripts.\n", encoding="utf-8")

        failures, *_ = audit_hooks_scripts.audit(self.root)

        self.assertTrue(any("skill hooks belong in SKILL.md frontmatter" in item for item in failures))
        self.assertTrue(any("placeholder hook/script README" in item for item in failures))

    def test_rejects_duplicate_capability_owners(self) -> None:
        first = self.add_skill("first")
        second = self.add_skill("second")
        body = "#!/usr/bin/env python3\nprint('same')\n"
        self.add_script(first, "analyze.py", body)
        self.add_script(second, "analyze.py", body)

        failures, *_ = audit_hooks_scripts.audit(self.root)

        self.assertTrue(any("ambiguous script name `analyze.py`" in item for item in failures))
        self.assertTrue(any("exact duplicate script implementations" in item for item in failures))

    def test_rejects_unregistered_hook_like_and_private_path(self) -> None:
        skill = self.add_skill("demo")
        self.add_script(
            skill,
            "completion-gate.sh",
            "#!/usr/bin/env bash\nprintf '%s\\n' '/Users/someone/private'\n",
        )

        failures, *_ = audit_hooks_scripts.audit(self.root)

        self.assertTrue(any("hook-like script is not referenced" in item for item in failures))
        self.assertTrue(any("absolute macOS user path" in item for item in failures))

    def test_requires_documented_script_ownership(self) -> None:
        skill = self.add_skill("demo", document_scripts=False)
        self.add_script(skill, "tool.py", "#!/usr/bin/env python3\nprint('ok')\n")

        failures, *_ = audit_hooks_scripts.audit(self.root)

        self.assertTrue(any("does not document its scripts boundary" in item for item in failures))

    def test_rejects_stale_script_asset_claim(self) -> None:
        skill = self.add_skill("demo", document_scripts=False)
        skill_file = skill / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8")
            + "\n- `scripts/` contains executable helpers owned by this lane.\n",
            encoding="utf-8",
        )

        failures, *_ = audit_hooks_scripts.audit(self.root)

        self.assertTrue(any("claims executable helpers" in item for item in failures))

    def test_rejects_stale_generic_script_claim(self) -> None:
        skill = self.add_skill("demo", document_scripts=False)
        skill_file = skill / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8")
            + "\nThe work needs this lane's references, scripts, examples, or templates.\n",
            encoding="utf-8",
        )

        failures, *_ = audit_hooks_scripts.audit(self.root)

        self.assertTrue(any("claims executable helpers" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
