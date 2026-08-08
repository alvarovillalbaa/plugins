from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import importlib.util


ROOT = Path(__file__).resolve().parents[2]
SKILLCTL = ROOT / "scripts" / "skillctl.py"


spec = importlib.util.spec_from_file_location("skillctl", SKILLCTL)
assert spec and spec.loader
skillctl = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = skillctl
spec.loader.exec_module(skillctl)


class SkillctlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        skill = self.tmp / "system" / "skills" / "demo"
        (skill / "references").mkdir(parents=True)
        (skill / "left-to-personalize").mkdir()
        (skill / "SKILL.md").write_text("---\nname: demo\ndescription: Demo skill.\n---\n", encoding="utf-8")
        (skill / ".skillmeta.yml").write_text(
            f"""id: system.demo
name: demo
origin:
  repo: {skillctl.CANONICAL_REPO}
  branch: main
  path: system/skills/demo
install:
  mode: project-managed-copy
  agents:
    - codex
personalization:
  policy: overlay-only
  local_files:
    - personalize.local.yml
upstream_contribution:
  allowed_paths:
    - SKILL.md
    - references/**
    - left-to-personalize/**
    - personalization.schema.json
    - personalize.example.yml
  forbidden_paths:
    - personalize.local.yml
    - .overlays/**
quality_gates:
  require_eval: false
  require_diff_classification: true
  require_human_review: true
""",
            encoding="utf-8",
        )
        self.skill = skill

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def write_external_registry(self, text: str) -> None:
        registry = self.tmp / "references"
        registry.mkdir(exist_ok=True)
        (registry / "external-skills.yaml").write_text(text, encoding="utf-8")

    def test_classifies_source_and_private_files(self) -> None:
        public = self.skill / "references" / "guide.md"
        private = self.skill / "personalize.local.yml"
        public.write_text("guide", encoding="utf-8")
        private.write_text("company: secret", encoding="utf-8")

        source = skillctl.classify_path(public, self.tmp)
        local = skillctl.classify_path(private, self.tmp)

        self.assertEqual(source.kind, "upstream-safe")
        self.assertEqual(local.kind, "local-private")

    def test_public_safety_guidance_about_secrets_is_not_private(self) -> None:
        public = self.skill / "references" / "secret-safety.md"
        public.write_text("Storing credentials or secrets in any memory file - never.", encoding="utf-8")

        source = skillctl.classify_path(public, self.tmp)

        self.assertEqual(source.kind, "upstream-safe")

    def test_root_discovery_and_agent_guidance_are_upstream_safe(self) -> None:
        for name in (
            "AGENTS.md",
            "CITATION.cff",
            "catalog.json",
            "codemeta.json",
            "context7.json",
            "llms.txt",
            "llms-full.txt",
        ):
            with self.subTest(name=name):
                classification = skillctl.classify_path(self.tmp / name, self.tmp)
                self.assertEqual(classification.kind, "upstream-safe")

    def test_render_overlays_replaces_known_placeholders(self) -> None:
        template = self.skill / "left-to-personalize" / "voice.md"
        values = self.tmp / "values.yml"
        out = self.tmp / "out"
        template.write_text("Hello {{COMPANY_NAME}} and {{MISSING}}", encoding="utf-8")
        values.write_text("company_name: ExampleCo\n", encoding="utf-8")

        args = type("Args", (), {"root": str(self.tmp), "skill": "system/skills/demo", "values": str(values), "out": str(out)})
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.render_overlays(args), 0)
        self.assertEqual((out / "voice.md").read_text(encoding="utf-8"), "Hello ExampleCo and {{MISSING}}")

    def test_patch_bundle_requires_upstream_safe_diff(self) -> None:
        subprocess.run(["git", "init"], cwd=self.tmp, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.tmp, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.tmp, check=True)
        guide = self.skill / "references" / "guide.md"
        guide.write_text("before", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.tmp, check=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=self.tmp, check=True, capture_output=True)
        guide.write_text("after", encoding="utf-8")

        args = type(
            "Args",
            (),
            {
                "root": str(self.tmp),
                "base": "HEAD",
                "head": "HEAD",
                "title": "Improve demo guide",
                "target": "system/skills/demo",
                "summary": None,
                "risk": "low",
            },
        )
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.write_patch_report(args), 0)
        bundles = list((self.tmp / ".skill-improvements").glob("*/improvement-report.json"))
        self.assertEqual(len(bundles), 1)

    def test_conflicts_check_allows_colon_public_command_names(self) -> None:
        system = self.tmp / "system"
        (system / ".claude-plugin").mkdir()
        (system / ".codex-plugin").mkdir()
        (system / ".cursor-plugin").mkdir()
        (system / "commands").mkdir()
        (system / "agents").mkdir()
        (system / "mcp.json").write_text('{"mcpServers": {}}\n', encoding="utf-8")
        (system / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "system", "version": "3.0.0"}\n',
            encoding="utf-8",
        )
        (system / ".codex-plugin" / "plugin.json").write_text(
            '{"name": "system", "version": "3.0.0", "skills": "./skills/"}\n',
            encoding="utf-8",
        )
        (system / ".cursor-plugin" / "plugin.json").write_text(
            '{"name": "system", "version": "3.0.0"}\n',
            encoding="utf-8",
        )
        (system / "profile.yaml").write_text(
            "slug: system\n"
            "version: 3.0.0\n"
            "skills:\n"
            "  - demo\n"
            "commands:\n"
            "  - si-review\n"
            "agents:\n",
            encoding="utf-8",
        )
        (system / "commands" / "si-review.md").write_text(
            "---\nname: si:review\ndescription: Review memory.\n---\n\nUse skill: **demo**.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})
        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 0)

    def test_conflicts_check_rejects_same_plugin_skill_command_name(self) -> None:
        system = self.tmp / "system"
        (system / ".claude-plugin").mkdir()
        (system / "commands").mkdir()
        (system / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "system", "version": "3.0.0"}\n',
            encoding="utf-8",
        )
        (system / "profile.yaml").write_text(
            "slug: system\n"
            "version: 3.0.0\n"
            "skills:\n"
            "  - demo\n"
            "commands:\n"
            "  - demo\n"
            "agents:\n",
            encoding="utf-8",
        )
        (system / "commands" / "demo.md").write_text(
            "---\nname: demo\ndescription: Duplicate public surface.\n---\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})
        stderr = StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(skillctl.conflicts_check(args), 1)
        self.assertIn("conflicts with same-plugin skill `system/demo`", stderr.getvalue())

    def test_conflicts_check_rejects_manifest_name_mismatch(self) -> None:
        system = self.tmp / "system"
        (system / ".claude-plugin").mkdir()
        (system / "profile.yaml").write_text(
            "slug: system\n"
            "version: 3.0.0\n"
            "skills:\n"
            "  - demo\n"
            "commands:\n"
            "agents:\n",
            encoding="utf-8",
        )
        (system / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "wrong", "version": "3.0.0"}\n',
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_stale_team_heading(self) -> None:
        system = self.tmp / "system"
        (system / ".claude-plugin").mkdir()
        (system / "profile.yaml").write_text(
            "slug: system\n"
            "version: 3.0.0\n"
            "skills:\n"
            "  - demo\n"
            "commands:\n"
            "agents:\n"
            "team:\n"
            "  - CEO\n",
            encoding="utf-8",
        )
        (system / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "system", "version": "3.0.0"}\n',
            encoding="utf-8",
        )
        (system / "TEAM.md").write_text("# Learning System Team\n\n- CEO\n", encoding="utf-8")

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_missing_profile_team_member(self) -> None:
        system = self.tmp / "system"
        (system / ".claude-plugin").mkdir()
        (system / "profile.yaml").write_text(
            "slug: system\n"
            "version: 3.0.0\n"
            "skills:\n"
            "  - demo\n"
            "commands:\n"
            "agents:\n"
            "team:\n"
            "  - CEO\n",
            encoding="utf-8",
        )
        (system / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "system", "version": "3.0.0"}\n',
            encoding="utf-8",
        )
        (system / "TEAM.md").write_text("# System Team\n\n- CTO\n", encoding="utf-8")

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_stale_readme_skill_paths(self) -> None:
        readme = self.skill / "README.md"
        readme.write_text(
            "```bash\nnpx -y skills add ./system/skills/missing-demo\n```\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_unknown_command_skill_refs(self) -> None:
        system = self.tmp / "system"
        (system / "commands").mkdir(exist_ok=True)
        (system / "commands" / "bad.md").write_text(
            "---\nname: bad\ndescription: Bad command.\n---\n\nUse skill: **missing-skill**.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_external_registry_missing_required_fields(self) -> None:
        self.write_external_registry(
            "skills:\n"
            "  known-external:\n"
            "    owner: example\n"
            "    repo: https://example.com/repo.git\n"
            "    ref: main\n"
            "    path: skills/known-external\n"
            "    install_name: known-external\n"
            "    homepage: https://example.com/repo\n"
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_duplicate_external_install_names(self) -> None:
        self.write_external_registry(
            "skills:\n"
            "  first-external:\n"
            "    owner: example\n"
            "    repo: https://example.com/first.git\n"
            "    ref: main\n"
            "    path: skills/first\n"
            "    install_name: shared-external\n"
            "    homepage: https://example.com/first\n"
            "    domain: quality\n"
            "  second-external:\n"
            "    owner: example\n"
            "    repo: https://example.com/second.git\n"
            "    ref: main\n"
            "    path: skills/second\n"
            "    install_name: shared-external\n"
            "    homepage: https://example.com/second\n"
            "    domain: quality\n"
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_unknown_explicit_external_skill_refs(self) -> None:
        self.write_external_registry(
            "skills:\n"
            "  known-external:\n"
            "    owner: example\n"
            "    repo: https://example.com/repo.git\n"
            "    ref: main\n"
            "    path: skills/known-external\n"
            "    install_name: known-external\n"
            "    homepage: https://example.com/repo\n"
            "    domain: quality\n"
        )
        system = self.tmp / "system"
        (system / "commands").mkdir(exist_ok=True)
        (system / "commands" / "demo.md").write_text(
            "---\n"
            "name: demo\n"
            "description: Demo command.\n"
            "---\n\n"
            "Optional external chain: **missing-external** if installed.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_allows_registered_external_install_refs(self) -> None:
        self.write_external_registry(
            "skills:\n"
            "  known-external:\n"
            "    owner: example\n"
            "    repo: https://example.com/repo.git\n"
            "    ref: main\n"
            "    path: skills/known-external\n"
            "    install_name: known-external\n"
            "    homepage: https://example.com/repo\n"
            "    domain: quality\n"
        )
        (self.skill / "SKILL.md").write_text(
            "---\n"
            "name: demo\n"
            "description: Demo skill.\n"
            "---\n\n"
            "Install optional chain with `python scripts/install-external-skills.py --skill known-external --agent codex`.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stdout(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 0)

    def test_conflicts_check_rejects_unknown_agent_command_refs(self) -> None:
        agents = self.tmp / "system" / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        (agents / "demo-agent.md").write_text(
            "---\n"
            "name: demo-agent\n"
            "description: Demo agent.\n"
            "---\n\n"
            "## Primary skills\n\n"
            "- `demo`\n\n"
            "## Commands\n\n"
            "- `missing-command`\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_unknown_agent_frontmatter_tools(self) -> None:
        agents = self.tmp / "system" / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        (agents / "demo-agent.md").write_text(
            "---\n"
            "name: demo-agent\n"
            "description: Demo agent.\n"
            "tools: Read, UnknownTool\n"
            "---\n\n"
            "## Primary skills\n\n"
            "- `demo`\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_unknown_agent_spawned_by_refs(self) -> None:
        agents = self.tmp / "system" / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        (agents / "demo-agent.md").write_text(
            "---\n"
            "name: demo-agent\n"
            "description: Demo agent. Spawned by `/missing-command`.\n"
            "tools: Read, Bash(git status *)\n"
            "disallowedTools: Bash(git push *)\n"
            "---\n\n"
            "## Primary skills\n\n"
            "- `demo`\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_unbracketed_allowed_tools(self) -> None:
        system = self.tmp / "system"
        (system / "commands").mkdir(exist_ok=True)
        (system / "commands" / "bad-tools.md").write_text(
            "---\n"
            "name: bad-tools\n"
            "description: Bad command tools.\n"
            "allowed-tools: Read, Write\n"
            "---\n\n"
            "Use skill: **demo**.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_stale_direct_agent_skill_token(self) -> None:
        agents = self.skill / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text(
            'interface:\n  default_prompt: "Use $old-demo to do the work."\n',
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_missing_skill_markdown_links(self) -> None:
        (self.skill / "SKILL.md").write_text(
            "---\n"
            "name: demo\n"
            "description: Demo skill.\n"
            "---\n\n"
            "See [`../missing-parent/SKILL.md`](../missing-parent/SKILL.md).\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_missing_reference_markdown_links(self) -> None:
        (self.skill / "references" / "guide.md").write_text(
            "See [missing](missing.md).\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_ignores_markdown_like_code_fences(self) -> None:
        (self.skill / "references" / "guide.md").write_text(
            "```python\n"
            "result = tools[action.name](action.argument)\n"
            "```\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 0)

    def test_conflicts_check_rejects_missing_command_markdown_links(self) -> None:
        commands = self.tmp / "system" / "commands"
        commands.mkdir(parents=True, exist_ok=True)
        (commands / "demo.md").write_text(
            "---\n"
            "name: demo\n"
            "description: Demo command.\n"
            "---\n\n"
            "See [missing](missing.md).\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_missing_command_backtick_skill_refs(self) -> None:
        commands = self.tmp / "system" / "commands"
        commands.mkdir(parents=True, exist_ok=True)
        (commands / "demo.md").write_text(
            "---\n"
            "name: demo\n"
            "description: Demo command.\n"
            "---\n\n"
            "Invoke the `missing-skill` skill.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_stale_task_allowed_tool(self) -> None:
        commands = self.tmp / "system" / "commands"
        commands.mkdir(parents=True, exist_ok=True)
        (commands / "demo.md").write_text(
            "---\n"
            "name: demo\n"
            "description: Demo command.\n"
            'allowed-tools: ["Read", "Task"]\n'
            "---\n\n"
            "Use agent: **memory-analyst**.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_agent_command_without_agent_tool(self) -> None:
        commands = self.tmp / "system" / "commands"
        commands.mkdir(parents=True, exist_ok=True)
        (commands / "demo.md").write_text(
            "---\n"
            "name: demo\n"
            "description: Demo command.\n"
            "allowed-tools: [Read]\n"
            "---\n\n"
            "Spawn the memory analyst agent.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_rejects_missing_active_doc_skill_paths(self) -> None:
        docs = self.tmp / "docs" / "audits"
        docs.mkdir(parents=True)
        (docs / "notes.md").write_text(
            "Route to system/skills/missing-skill for this workflow.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 1)

    def test_conflicts_check_ignores_non_plugin_skill_path_fragments(self) -> None:
        docs = self.tmp / "docs" / "audits" / "skills"
        docs.mkdir(parents=True)
        (docs / "notes.md").write_text(
            "See docs/audits/skills/2026-06-22-skill-plugin-maintenance.md.\n",
            encoding="utf-8",
        )

        args = type("Args", (), {"root": str(self.tmp)})

        with redirect_stderr(StringIO()):
            self.assertEqual(skillctl.conflicts_check(args), 0)


class ExperimentRunnerTests(unittest.TestCase):
    def test_runner_keeps_improvement_on_safe_branch(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            (root / "target.txt").write_text("old", encoding="utf-8")
            (root / "eval.py").write_text("print('score: 1')\n", encoding="utf-8")
            exp = root / ".autoresearch" / "demo" / "case"
            exp.mkdir(parents=True)
            (exp / "config.cfg").write_text(
                "target = target.txt\nevaluate_cmd = python3 eval.py\nmetric = score\nmetric_direction = lower\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "initial"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "checkout", "-b", "autoresearch/demo/case"], cwd=root, check=True, capture_output=True)
            (root / "target.txt").write_text("new", encoding="utf-8")
            runner = ROOT / "system" / "skills" / "loops" / "scripts" / "run_experiment.py"
            result = subprocess.run(
                ["python3", str(runner), "--root", str(root), "--experiment", "demo/case", "--single", "--description", "test"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("KEEP", result.stdout)


if __name__ == "__main__":
    unittest.main()
