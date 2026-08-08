#!/usr/bin/env python3
"""Regression tests for the local-only auto-improve contract."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import component_graph  # noqa: E402


class AutoImproveContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = ROOT / "system" / "skills" / "auto-improve"

    def test_skill_focuses_local_context_markdown_and_first_use(self) -> None:
        text = (self.skill / "SKILL.md").read_text(encoding="utf-8")

        for expected in (
            "agent context",
            "Markdown",
            "first relevant workflow",
            ".agents/{skills,commands,rules,agents}",
            "canonical `alvarovillalbaa/plugins` checkout",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_auto_improve_exposes_no_upstream_commands(self) -> None:
        paths = (
            self.skill / "SKILL.md",
            self.skill / "references" / "routing-guide.md",
            ROOT / "engineering" / "skills" / "agent-harness" / "references" / "autoimprove.md",
        )
        commands: list[str] = []
        for path in paths:
            in_fence = False
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    commands.append(line.strip())

        rendered = "\n".join(commands)
        for forbidden in ("propose-upstream", "diff-classify", "git push", "gh pr"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, rendered)

    def test_personalization_schema_allows_only_installed_copy_scope(self) -> None:
        schema = json.loads(
            (self.skill / "personalization.schema.json").read_text(encoding="utf-8")
        )
        workflow = schema["properties"]["workflow"]

        self.assertEqual(workflow["required"], ["plugin_improvement_scope"])
        self.assertEqual(
            workflow["properties"]["plugin_improvement_scope"],
            {"const": "installed-copy"},
        )
        example = (self.skill / "personalize.example.yml").read_text(encoding="utf-8")
        self.assertIn('plugin_improvement_scope: "installed-copy"', example)
        self.assertNotIn("default_contribution_mode", example)

    def test_relationships_are_narrowed_to_local_improvement_owners(self) -> None:
        graph = component_graph.build_graph(ROOT)
        outgoing = {
            edge["to"]
            for edge in graph["edges"]
            if edge["from"] == "skill:system/auto-improve"
        }

        self.assertEqual(
            outgoing,
            {
                "external-skill:teach",
                "external-skill:use-afs",
                "external-skill:writing-great-skills",
                "skill:engineering/code-documentation",
                "skill:engineering/quality-assurance",
                "skill:system/ingestion",
                "skill:system/loops",
                "skill:system/memory",
                "skill:system/personalize",
                "skill:system/plugins-management",
                "skill:system/skill-eval-loop",
            },
        )

    def test_installed_runtime_routes_first_use_through_auto_improve(self) -> None:
        rule = (ROOT / "references" / "agent-runtime-rule.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("route initialization through the", rule)
        self.assertIn("installed `auto-improve` skill", rule)
        self.assertIn("canonical plugin source checkout as read-only", rule)


if __name__ == "__main__":
    unittest.main()
