from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import audit_rules


class RuleAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def add_department(self, name: str, skills: list[str], routes: str | None = None) -> None:
        department = self.root / name
        (department / "rules").mkdir(parents=True)
        for skill in skills:
            skill_dir = department / "skills" / skill
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(f"# {skill}\n", encoding="utf-8")
        profile = "slug: " + name + "\nskills:\n" + "".join(
            f"  - {skill}\n" for skill in skills
        ) + "commands:\n"
        (department / "profile.yaml").write_text(profile, encoding="utf-8")
        (department / "rules" / "README.md").write_text(
            f"# {name.title()} rules\n\nSee [`defaults.md`](defaults.md).\n",
            encoding="utf-8",
        )
        route_refs = routes or ", ".join(f"`{skill}`" for skill in skills)
        defaults = f"""# {name.title()} rules

## Department boundary

Owns its bounded domain.

## Routing constraints

| Request shape | Route to |
| --- | --- |
| Local work | {route_refs} |

## Operating defaults

- Use evidence.

## Authorization gates

- Confirm external actions.

## Quality bar

- Verify the result.
"""
        (department / "rules" / "defaults.md").write_text(defaults, encoding="utf-8")

    def test_accepts_complete_generalized_rules(self) -> None:
        self.add_department("alpha", ["one", "two"])

        failures, summaries = audit_rules.audit(self.root)

        self.assertEqual(failures, [])
        self.assertEqual(summaries[0].covered_skill_count, 2)

    def test_rejects_uncovered_profile_skill(self) -> None:
        self.add_department("alpha", ["one", "two"], routes="`one`")

        failures, _ = audit_rules.audit(self.root)

        self.assertTrue(any("local skills missing from routing coverage: two" in item for item in failures))

    def test_rejects_unqualified_cross_plugin_route(self) -> None:
        self.add_department("alpha", ["one"], routes="`one`, `two`")
        self.add_department("beta", ["two"])

        failures, _ = audit_rules.audit(self.root)

        self.assertTrue(any("must be qualified as beta/two" in item for item in failures))

    def test_accepts_qualified_cross_plugin_route(self) -> None:
        self.add_department("alpha", ["one"], routes="`one`, `beta/two`")
        self.add_department("beta", ["two"])

        failures, _ = audit_rules.audit(self.root)

        self.assertEqual(failures, [])

    def test_rejects_missing_contract_and_specific_identity(self) -> None:
        self.add_department("alpha", ["one"])
        readme = self.root / "alpha" / "rules" / "README.md"
        readme.write_text(
            "# Rules for CLOUS\n\nStored in /Users/alvaro/work/. Contact owner@example.com.\n",
            encoding="utf-8",
        )

        failures, _ = audit_rules.audit(self.root)

        self.assertTrue(any("must link to [defaults.md](defaults.md)" in item for item in failures))
        self.assertTrue(any("named repository or organization" in item for item in failures))
        self.assertTrue(any("absolute macOS user path" in item for item in failures))
        self.assertTrue(any("email address" in item for item in failures))

    def test_rejects_missing_or_reordered_contract_sections(self) -> None:
        self.add_department("alpha", ["one"])
        defaults = self.root / "alpha" / "rules" / "defaults.md"
        text = defaults.read_text(encoding="utf-8")
        text = text.replace("## Quality bar\n\n- Verify the result.\n", "")
        text = text.replace(
            "## Operating defaults\n\n- Use evidence.\n\n## Authorization gates",
            "## Authorization gates\n\n- Confirm external actions.\n\n## Operating defaults",
        )
        defaults.write_text(text, encoding="utf-8")

        failures, _ = audit_rules.audit(self.root)

        self.assertTrue(any("expected one `## Quality bar`" in item for item in failures))
        self.assertTrue(any("required sections are out of order" in item for item in failures))

    def test_rejects_profile_and_disk_inventory_drift(self) -> None:
        self.add_department("alpha", ["one"])
        profile = self.root / "alpha" / "profile.yaml"
        profile.write_text(
            profile.read_text(encoding="utf-8").replace(
                "commands:\n", "  - missing-on-disk\ncommands:\n"
            ),
            encoding="utf-8",
        )
        extra = self.root / "alpha" / "skills" / "missing-from-profile"
        extra.mkdir(parents=True)
        (extra / "SKILL.md").write_text("# extra\n", encoding="utf-8")

        failures, _ = audit_rules.audit(self.root)

        self.assertTrue(any("skills missing from profile: missing-from-profile" in item for item in failures))
        self.assertTrue(any("profiled skills missing on disk: missing-on-disk" in item for item in failures))

    def test_rejects_qualified_route_to_missing_skill(self) -> None:
        self.add_department("alpha", ["one"], routes="`one`, `beta/missing`")
        self.add_department("beta", ["two"])

        failures, _ = audit_rules.audit(self.root)

        self.assertTrue(any("route `beta/missing` names a missing skill" in item for item in failures))

    def test_rejects_duplicate_policy_statement(self) -> None:
        self.add_department("alpha", ["one"])
        defaults = self.root / "alpha" / "rules" / "defaults.md"
        defaults.write_text(
            defaults.read_text(encoding="utf-8") + "\n- Verify the result.\n",
            encoding="utf-8",
        )

        failures, _ = audit_rules.audit(self.root)

        self.assertTrue(any("duplicate policy statement" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
