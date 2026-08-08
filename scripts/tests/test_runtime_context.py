from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import runtime_context


class RuntimeContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        agents = self.project / ".agents"
        agents.mkdir()
        self.contract = json.loads(
            (runtime_context.ROOT / "references" / "runtime-contract.json").read_text(encoding="utf-8")
        )
        (agents / "runtime-contract.json").write_text(
            json.dumps(self.contract), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_configure_persists_only_project_values(self) -> None:
        out = runtime_context.configure_project(
            project=self.project,
            assignments=["project.name=Atlas", "output.language=Spanish"],
        )
        stored = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(stored["project"]["name"], "Atlas")
        self.assertEqual(stored["output"]["language"], "Spanish")

        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "invocation-scoped"):
            runtime_context.configure_project(
                project=self.project, assignments=["content.topic=Agents"]
            )

    def test_contract_top_level_fields_are_declared_by_its_schema(self) -> None:
        schema = json.loads(
            (runtime_context.ROOT / "schemas" / "runtime-contract.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(set(self.contract).issubset(schema["properties"]))
        self.assertTrue(set(schema["required"]).issubset(self.contract))

    def test_resolve_uses_invocation_session_project_default_order(self) -> None:
        runtime_context.configure_project(
            project=self.project,
            assignments=["project.name=Atlas", "output.language=Spanish"],
        )
        result = runtime_context.resolve_context(
            project=self.project,
            component="skill:marketing/content",
            invocation={"content.topic": "Agent workflows", "output.language": "English"},
            session={"audience.primary": "Developers"},
        )
        self.assertEqual(result["values"]["project.name"], "Atlas")
        self.assertEqual(result["values"]["content.topic"], "Agent workflows")
        self.assertEqual(result["values"]["audience.primary"], "Developers")
        self.assertEqual(result["values"]["output.language"], "English")
        self.assertEqual(result["sources"]["output.language"], "invocation")
        self.assertEqual(result["missing_required"], [])

    def test_required_invocation_value_fails_closed(self) -> None:
        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "content.topic"):
            runtime_context.resolve_context(
                project=self.project,
                component="skill:marketing/content",
            )
        result = runtime_context.resolve_context(
            project=self.project,
            component="skill:marketing/content",
            allow_missing=True,
        )
        self.assertEqual(result["missing_required"], ["content.topic"])

    def test_personalization_policy_can_disable_inherited_variables(self) -> None:
        self.contract["components"]["skill:marketing/content"]["personalization"] = "disabled"
        (self.project / ".agents" / "runtime-contract.json").write_text(
            json.dumps(self.contract), encoding="utf-8"
        )

        result = runtime_context.resolve_context(
            project=self.project,
            component="skill:marketing/content",
        )

        self.assertEqual(result["values"], {})
        self.assertEqual(result["missing_required"], [])

    def test_required_values_can_be_prompted_without_persistence(self) -> None:
        values = runtime_context.prompt_missing_values(
            ["content.topic"],
            self.contract["variables"]["definitions"],
            input_fn=lambda _prompt: "Agent workflows",
        )

        self.assertEqual(values, {"content.topic": "Agent workflows"})
        self.assertFalse((self.project / ".agents" / "personalization.local.json").exists())

    def test_resolution_uses_contract_order(self) -> None:
        self.contract["variables"]["resolution_order"] = [
            "session",
            "invocation",
            "project",
            "default",
        ]
        (self.project / ".agents" / "runtime-contract.json").write_text(
            json.dumps(self.contract), encoding="utf-8"
        )

        result = runtime_context.resolve_context(
            project=self.project,
            component="skill:marketing/content",
            invocation={"content.topic": "Invocation topic"},
            session={"content.topic": "Session topic"},
        )

        self.assertEqual(result["values"]["content.topic"], "Session topic")
        self.assertEqual(result["sources"]["content.topic"], "session")

    def test_invocation_scoped_value_is_never_loaded_from_project_store(self) -> None:
        (self.project / ".agents" / "personalization.local.json").write_text(
            json.dumps({"content": {"topic": "Persisted topic"}}),
            encoding="utf-8",
        )

        result = runtime_context.resolve_context(
            project=self.project,
            component="skill:marketing/content",
            allow_missing=True,
        )

        self.assertNotIn("content.topic", result["values"])
        self.assertEqual(result["missing_required"], ["content.topic"])

    def test_render_placeholders_supports_named_values_and_raw_arguments(self) -> None:
        rendered = runtime_context.render_placeholders(
            "Project {{project.name}}: $ARGUMENTS\n",
            {"project.name": "Atlas"},
            arguments="ship the release",
        )

        self.assertEqual(rendered, "Project Atlas: ship the release\n")
        with self.assertRaisesRegex(
            runtime_context.RuntimeContextError, "unresolved runtime placeholder"
        ):
            runtime_context.render_placeholders(
                "Missing {{organization.name}}", {"project.name": "Atlas"}
            )

    def test_sensitive_values_cannot_be_persisted(self) -> None:
        self.contract["variables"]["definitions"]["secret.token"] = {
            "scope": "project",
            "type": "string",
            "prompt": "Token?",
            "required": False,
            "sensitive": True,
        }
        (self.project / ".agents" / "runtime-contract.json").write_text(
            json.dumps(self.contract), encoding="utf-8"
        )
        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "refusing to persist"):
            runtime_context.configure_project(
                project=self.project, assignments=["secret.token=do-not-store"]
            )

    def test_project_store_cannot_escape_the_project(self) -> None:
        outside = self.project.parent / "outside.json"
        self.contract["personalization"]["project_store"] = "../outside.json"
        (self.project / ".agents" / "runtime-contract.json").write_text(
            json.dumps(self.contract), encoding="utf-8"
        )

        with self.assertRaisesRegex(runtime_context.RuntimeContextError, "under .agents"):
            runtime_context.configure_project(
                project=self.project, assignments=["project.name=Atlas"]
            )
        self.assertFalse(outside.exists())


if __name__ == "__main__":
    unittest.main()
