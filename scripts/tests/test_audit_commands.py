from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import audit_commands


class CommandAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        (self.root / "references").mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def add_department(self, name: str, command: str = "do-work", skill: str = "worker") -> None:
        department = self.root / name
        (department / "commands").mkdir(parents=True)
        skill_dir = department / "skills" / skill
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"---\nname: {skill}\ndescription: Work.\n---\n", encoding="utf-8")
        (department / "profile.yaml").write_text(
            f"slug: {name}\nskills:\n  - {skill}\ncommands:\n  - {command}\n",
            encoding="utf-8",
        )
        (department / "commands" / f"{command}.md").write_text(
            f"""---
name: {command}
description: Perform one bounded reusable workflow and report verified evidence.
argument-hint: "[scope]"
allowed-tools: [Read, Skill]
---

Use skill: **{skill}**.

1. Read the supplied scope.
2. Return verified evidence.
""",
            encoding="utf-8",
        )

    def write_catalog(
        self,
        commands: list[dict[str, str]],
        retired: list[dict[str, str]] | None = None,
    ) -> None:
        (self.root / "references" / "command-capabilities.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "selection_rule": "Keep only distinct stable workflows.",
                    "commands": commands,
                    "retired": retired or [],
                }
            ),
            encoding="utf-8",
        )

    def record(self, department: str = "alpha", command: str = "do-work", owner: str = "alpha/worker") -> dict[str, str]:
        return {
            "path": f"{department}/commands/{command}.md",
            "capability": f"{department}.{command}",
            "owner": owner,
            "boundary": "Owns one bounded workflow and excludes adjacent work.",
        }

    def test_accepts_complete_generalized_command_contract(self) -> None:
        self.add_department("alpha")
        self.write_catalog([self.record()])

        failures, summaries, records, _ = audit_commands.audit(self.root)

        self.assertEqual(failures, [])
        self.assertEqual(summaries[0].cataloged_count, 1)
        self.assertEqual(records[0].owner, "alpha/worker")

    def test_rejects_profile_and_catalog_inventory_drift(self) -> None:
        self.add_department("alpha")
        profile = self.root / "alpha" / "profile.yaml"
        profile.write_text(profile.read_text(encoding="utf-8").replace("  - do-work\n", ""), encoding="utf-8")
        self.write_catalog([])

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("commands missing from capability registry" in item for item in failures))
        self.assertTrue(any("commands missing from profile" in item for item in failures))

    def test_rejects_same_plugin_skill_command_name(self) -> None:
        self.add_department("alpha", command="worker", skill="worker")
        self.write_catalog([self.record(command="worker")])

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("conflicts with same-plugin skill" in item for item in failures))

    def test_rejects_duplicate_capability_and_missing_owner(self) -> None:
        self.add_department("alpha")
        self.add_department("beta")
        first = self.record()
        second = self.record("beta", owner="beta/missing")
        second["capability"] = first["capability"]
        self.write_catalog([first, second])

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("duplicate capability" in item for item in failures))
        self.assertTrue(any("canonical owner `beta/missing` does not exist" in item for item in failures))

    def test_rejects_command_that_does_not_route_to_cataloged_owner(self) -> None:
        self.add_department("alpha")
        command = self.root / "alpha" / "commands" / "do-work.md"
        command.write_text(
            command.read_text(encoding="utf-8").replace("Use skill: **worker**.\n\n", ""),
            encoding="utf-8",
        )
        self.write_catalog([self.record()])

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("does not route to canonical owner `alpha/worker`" in item for item in failures))

    def test_rejects_routed_command_without_skill_tool(self) -> None:
        self.add_department("alpha")
        command = self.root / "alpha" / "commands" / "do-work.md"
        command.write_text(
            command.read_text(encoding="utf-8").replace("[Read, Skill]", "[Read]"),
            encoding="utf-8",
        )
        self.write_catalog([self.record()])

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("must allow the `Skill` tool" in item for item in failures))

    def test_rejects_specific_identity_and_oversized_command(self) -> None:
        self.add_department("alpha")
        command = self.root / "alpha" / "commands" / "do-work.md"
        command.write_text(
            command.read_text(encoding="utf-8")
            + "Run for CLOUS at /Users/alvaro/private/.\n"
            + "\n".join("extra" for _ in range(audit_commands.MAX_COMMAND_LINES)),
            encoding="utf-8",
        )
        self.write_catalog([self.record()])

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("named organization" in item for item in failures))
        self.assertTrue(any("absolute macOS user path" in item for item in failures))
        self.assertTrue(any("exceeds the" in item for item in failures))

    def test_rejects_retired_command_that_reappears(self) -> None:
        self.add_department("alpha")
        self.write_catalog(
            [self.record()],
            [
                {
                    "path": "alpha/commands/do-work.md",
                    "replacement": "alpha/worker",
                    "reason": "A skill owns this invocation.",
                }
            ],
        )

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("retired command must remain absent" in item for item in failures))

    def test_rejects_retired_command_without_live_replacement(self) -> None:
        self.add_department("alpha")
        self.write_catalog(
            [self.record()],
            [
                {
                    "path": "alpha/commands/old.md",
                    "replacement": "alpha/missing",
                    "reason": "The old workflow was redundant.",
                }
            ],
        )

        failures, _, _, _ = audit_commands.audit(self.root)

        self.assertTrue(any("replacement target `alpha/missing` does not exist" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
