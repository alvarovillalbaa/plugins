from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import audit_agents


class AgentAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def add_department(self, name: str, skills: list[str], agents: dict[str, list[str]]) -> None:
        department = self.root / name
        (department / "agents").mkdir(parents=True)
        for skill in skills:
            skill_dir = department / "skills" / skill
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: {skill}\ndescription: Work.\n---\n", encoding="utf-8"
            )
        (department / "profile.yaml").write_text(
            f"slug: {name}\n"
            + "skills:\n"
            + "".join(f"  - {skill}\n" for skill in skills)
            + "agents:\n"
            + "".join(f"  - {agent}\n" for agent in agents),
            encoding="utf-8",
        )
        for agent, owned in agents.items():
            (department / "agents" / f"{agent}.md").write_text(
                f"""---
name: {agent}
description: Coordinates a reusable workflow.
---

# {agent}

## Scope

Own a bounded workflow.

## Primary skills

{''.join(f'- `{skill}`\n' for skill in owned)}
## Routing boundaries

Own the requested workflow and hand off adjacent work explicitly.
""",
                encoding="utf-8",
            )

    def test_accepts_complete_generalized_agent_coverage(self) -> None:
        self.add_department("alpha", ["plan", "execute"], {"operator": ["plan", "execute"]})

        failures, summaries, records = audit_agents.audit(self.root)

        self.assertEqual(failures, [])
        self.assertEqual(summaries[0].covered_skill_count, 2)
        self.assertEqual(records[0].name, "operator")

    def test_rejects_missing_skill_coverage_and_profile_drift(self) -> None:
        self.add_department("alpha", ["plan", "execute"], {"operator": ["plan"]})
        profile = self.root / "alpha" / "profile.yaml"
        profile.write_text(profile.read_text(encoding="utf-8").replace("  - operator\n", ""), encoding="utf-8")

        failures, _, _ = audit_agents.audit(self.root)

        self.assertTrue(any("local skills missing agent coverage: execute" in item for item in failures))
        self.assertTrue(any("agents missing from profile: operator" in item for item in failures))

    def test_rejects_specific_identity_and_absolute_user_path(self) -> None:
        self.add_department("alpha", ["plan"], {"operator": ["plan"]})
        agent = self.root / "alpha" / "agents" / "operator.md"
        agent.write_text(agent.read_text(encoding="utf-8") + "Run for CLOUS in /Users/alvaro/private/.\n", encoding="utf-8")

        failures, _, _ = audit_agents.audit(self.root)

        self.assertTrue(any("named organization" in item for item in failures))
        self.assertTrue(any("absolute macOS user path" in item for item in failures))

    def test_rejects_exact_duplicate_agent_capability_sets(self) -> None:
        self.add_department("alpha", ["plan", "execute"], {"planner": ["plan", "execute"], "operator": ["plan", "execute"]})

        failures, _, _ = audit_agents.audit(self.root)

        self.assertTrue(any("exact duplicate primary-skill coverage" in item for item in failures))

    def test_high_overlap_requires_mutual_routing_boundaries(self) -> None:
        self.add_department(
            "alpha",
            ["plan", "execute", "report"],
            {"planner": ["plan", "execute"], "operator": ["plan", "execute", "report"]},
        )

        failures, _, _ = audit_agents.audit(self.root)

        self.assertTrue(any("high-overlap agents" in item for item in failures))

        planner = self.root / "alpha" / "agents" / "planner.md"
        operator = self.root / "alpha" / "agents" / "operator.md"
        planner.write_text(planner.read_text(encoding="utf-8").replace("hand off adjacent work", "hand off execution to operator"), encoding="utf-8")
        operator.write_text(operator.read_text(encoding="utf-8").replace("hand off adjacent work", "hand off planning to planner"), encoding="utf-8")

        failures, _, _ = audit_agents.audit(self.root)

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
