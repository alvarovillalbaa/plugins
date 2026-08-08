from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import generate_discovery_catalog as discovery


class DiscoveryCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.add_department("alpha")

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def add_department(self, name: str) -> None:
        department = self.root / name
        (department / "skills" / "routing").mkdir(parents=True)
        (department / "commands").mkdir()
        (department / "agents").mkdir()
        (department / "rules").mkdir()
        for manifest_dir in (".claude-plugin", ".codex-plugin", ".cursor-plugin"):
            path = department / manifest_dir
            path.mkdir()
            (path / "plugin.json").write_text(
                json.dumps({"name": name, "version": "1.2.3"}) + "\n",
                encoding="utf-8",
            )

        (department / "profile.yaml").write_text(
            f"""slug: {name}
version: 1.2.3
mission: Route bounded work to the narrowest source capability.
platforms:
  - claude
  - codex
skills:
  - routing
commands:
  - do-work
agents:
  - reviewer
team:
  - Maintainer
""",
            encoding="utf-8",
        )
        (department / "skills" / "routing" / "SKILL.md").write_text(
            """---
name: routing
description: >-
  Route requests to the narrowest capability while preserving source
  ownership and verification requirements.
hooks:
  Stop:
    - hooks:
        - type: command
---

# Routing
""",
            encoding="utf-8",
        )
        (department / "commands" / "do-work.md").write_text(
            """---
name: "do:work"
description: "Run one bounded workflow: inspect, act, and verify."
allowed-tools: [Read, Skill]
---

Use skill: **routing**.
""",
            encoding="utf-8",
        )
        (department / "agents" / "reviewer.md").write_text(
            """---
name: reviewer
description: Review one supplied artifact and return evidence-backed corrections.
---

# Reviewer
""",
            encoding="utf-8",
        )
        (department / "rules" / "defaults.md").write_text(
            f"""# {name.title()} defaults

Runtime-neutral defaults for the {name} plugin and all of its components.
""",
            encoding="utf-8",
        )

    def test_builds_inventory_from_profiles_and_frontmatter(self) -> None:
        catalog = discovery.build_catalog(self.root)

        self.assertEqual(
            catalog["counts"],
            {"plugins": 1, "skills": 1, "commands": 1, "agents": 1, "rules": 1},
        )
        plugin = catalog["plugins"][0]
        self.assertEqual(plugin["name"], "alpha")
        self.assertEqual(plugin["platforms"], ["claude", "codex"])
        self.assertEqual(plugin["skills"][0]["install_name"], "routing")
        self.assertEqual(
            plugin["skills"][0]["description"],
            "Route requests to the narrowest capability while preserving source ownership and verification requirements.",
        )
        self.assertEqual(plugin["commands"][0]["name"], "do:work")
        self.assertEqual(plugin["commands"][0]["install_name"], "do-work")
        self.assertEqual(
            plugin["commands"][0]["url"],
            "https://github.com/alvarovillalbaa/plugins/blob/main/alpha/commands/do-work.md",
        )
        self.assertEqual(plugin["rules"][0]["qualified_name"], "alpha/defaults")

    def test_outputs_are_deterministic_and_do_not_advertise_endpoints(self) -> None:
        first = discovery.render_outputs(self.root)
        second = discovery.render_outputs(self.root)

        self.assertEqual(first, second)
        self.assertEqual(tuple(first), discovery.OUTPUT_FILES)
        self.assertNotIn("agent-card.json", "".join(first.values()))
        catalog = json.loads(first["catalog.json"])
        self.assertNotIn("api_url", catalog)
        self.assertNotIn("endpoint", catalog)
        self.assertIn("public name `do:work`", first["llms-full.txt"])
        self.assertIn(discovery.raw_url("catalog.json"), first["llms.txt"])

    def test_check_reports_missing_and_stale_outputs(self) -> None:
        outputs = discovery.render_outputs(self.root)
        self.assertEqual(discovery.stale_outputs(self.root, outputs), list(discovery.OUTPUT_FILES))

        discovery.write_outputs(self.root, outputs)
        self.assertEqual(discovery.stale_outputs(self.root, outputs), [])

        (self.root / "llms.txt").write_text("stale\n", encoding="utf-8")
        self.assertEqual(discovery.stale_outputs(self.root, outputs), ["llms.txt"])
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            self.assertEqual(discovery.main(["--root", str(self.root), "--check"]), 1)

    def test_rejects_profile_inventory_drift(self) -> None:
        extra = self.root / "alpha" / "skills" / "unlisted"
        extra.mkdir()
        (extra / "SKILL.md").write_text(
            "---\nname: unlisted\ndescription: Unlisted capability.\n---\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(discovery.DiscoveryError, "missing from profile: unlisted"):
            discovery.build_catalog(self.root)

    def test_checked_in_outputs_are_current(self) -> None:
        outputs = discovery.render_outputs(ROOT)
        self.assertEqual(discovery.stale_outputs(ROOT, outputs), [])


if __name__ == "__main__":
    unittest.main()
