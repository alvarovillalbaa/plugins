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

from scripts import component_graph


class ComponentGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self._add_plugin(
            "alpha",
            skills=["root", "left", "right", "join"],
            commands=["run"],
            rules=["defaults"],
            agents=["worker"],
        )
        self._add_plugin(
            "beta",
            skills=["remote"],
            commands=[],
            rules=[],
            agents=["reviewer"],
        )
        (self.root / "alpha/agents/worker.md").write_text(
            "# worker\n\n"
            "## Commands\n\n"
            "- `run`\n",
            encoding="utf-8",
        )
        (self.root / "beta/agents/reviewer.md").write_text(
            "# reviewer\n\n"
            "## Primary Skills\n\n"
            "- `remote`\n"
            "- `alpha/root`\n",
            encoding="utf-8",
        )
        (self.root / "alpha/rules/defaults.md").write_text(
            "# defaults\n\n"
            "## Routing constraints\n\n"
            "Route through `root` and `beta/remote`, then hand off to `beta`.\n"
            "Ignore explanatory prose such as `not a skill reference`.\n\n"
            "## Operating defaults\n",
            encoding="utf-8",
        )
        references = self.root / "references"
        references.mkdir()
        (references / "external-skills.yaml").write_text(
            "skills:\n"
            "  ext-one:\n"
            "    owner: example\n"
            "    repo: https://example.com/ext.git\n"
            "    ref: main\n"
            "    path: skills/ext-one\n"
            "    install_name: ext-one\n"
            "    homepage: https://example.com/ext\n"
            "    domain: example\n",
            encoding="utf-8",
        )
        (references / "external-sources.yaml").write_text(
            "sources:\n"
            "  source-only:\n"
            "    owner: example\n"
            "    repo: https://example.com/source.git\n"
            "    ref: main\n"
            "    homepage: https://example.com/source\n"
            "    domain: example-reference\n",
            encoding="utf-8",
        )
        (references / "command-capabilities.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "commands": [
                        {
                            "path": "alpha/commands/run.md",
                            "owner": "beta/remote",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        (self.root / "skills-chaining-map.md").write_text(
            "# Skills Chaining Map\n\n"
            "## External Chains\n\n"
            "| Internal skill | External skills |\n"
            "| --- | --- |\n"
            "| `root` | `ext-one`, `source-only` |\n\n"
            "## Chains\n\n"
            "### Alpha\n\n"
            "| Parent | Children | Chains To |\n"
            "| --- | --- | --- |\n"
            "| `root` | `left`, `right` | `left`, `right` |\n"
            "| `left` | — | `join` |\n"
            "| `right` | — | `join` |\n"
            "| `join` | — | `root` |\n",
            encoding="utf-8",
        )
        self.contract = references / "component-graph.json"
        self.contract.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "sources": {
                        "profiles": "*/profile.yaml",
                        "chain_map": "skills-chaining-map.md",
                        "external_skills": "references/external-skills.yaml",
                        "external_sources": "references/external-sources.yaml",
                        "command_catalog": "references/command-capabilities.json",
                    },
                    "resolution": {
                        "strategy": "breadth-first",
                        "breadth_execution": "parallel",
                        "cycle_policy": "visit-once-report-edges",
                        "traverse_relations": sorted(component_graph.RELATIONS),
                    },
                    "references": [
                        {
                            "from": "rule:alpha/defaults",
                            "to": "agent:beta/reviewer",
                            "relation": "references",
                            "execution": "sequential",
                        },
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def _add_plugin(
        self,
        name: str,
        *,
        skills: list[str],
        commands: list[str],
        rules: list[str],
        agents: list[str],
    ) -> None:
        plugin = self.root / name
        plugin.mkdir()
        (plugin / "profile.yaml").write_text(f"slug: {name}\n", encoding="utf-8")
        for skill in skills:
            directory = plugin / "skills" / skill
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text(
                f"---\nname: {skill}\ndescription: Test skill.\n---\n",
                encoding="utf-8",
            )
        for kind, names in (("commands", commands), ("rules", rules), ("agents", agents)):
            directory = plugin / kind
            directory.mkdir(parents=True, exist_ok=True)
            for item in names:
                (directory / f"{item}.md").write_text(f"# {item}\n", encoding="utf-8")

    def build(self) -> dict:
        return component_graph.build_graph(self.root, self.contract)

    def test_build_scans_typed_nodes_containment_chains_and_explicit_references(self) -> None:
        graph = self.build()
        self.assertEqual(graph["artifact_kind"], "component-relationship-graph")
        self.assertEqual(
            graph["semantics"]["relationships"],
            "conditional-candidates-not-unconditional-execution",
        )
        node_ids = {node["id"] for node in graph["nodes"]}
        self.assertTrue(
            {
                "plugin:alpha",
                "skill:alpha/root",
                "command:alpha/run",
                "rule:alpha/defaults",
                "agent:alpha/worker",
                "external-skill:ext-one",
                "external-skill:source-only",
            }.issubset(node_ids)
        )
        edges = {
            (edge["from"], edge["to"], edge["relation"], edge["execution"])
            for edge in graph["edges"]
        }
        self.assertIn(("plugin:alpha", "skill:alpha/root", "contains", "parallel"), edges)
        self.assertIn(("skill:alpha/root", "skill:alpha/left", "owns", "parallel"), edges)
        self.assertIn(("skill:alpha/root", "external-skill:ext-one", "chains-to", "parallel"), edges)
        self.assertIn(("skill:alpha/root", "external-skill:source-only", "chains-to", "parallel"), edges)
        self.assertIn(("command:alpha/run", "skill:beta/remote", "routes-to", "sequential"), edges)
        self.assertIn(("agent:alpha/worker", "command:alpha/run", "invokes", "parallel"), edges)
        self.assertIn(("agent:beta/reviewer", "skill:beta/remote", "uses", "parallel"), edges)
        self.assertIn(("agent:beta/reviewer", "skill:alpha/root", "uses", "parallel"), edges)
        self.assertIn(("rule:alpha/defaults", "skill:alpha/root", "routes-to", "parallel"), edges)
        self.assertIn(("rule:alpha/defaults", "skill:beta/remote", "routes-to", "parallel"), edges)
        self.assertEqual(
            {
                edge["to"]
                for edge in graph["edges"]
                if edge["from"] == "rule:alpha/defaults"
                and edge["relation"] == "routes-to"
            },
            {"skill:alpha/root", "skill:beta/remote"},
        )
        declared = next(
            edge
            for edge in graph["edges"]
            if edge["from"] == "agent:alpha/worker"
            and edge["to"] == "command:alpha/run"
            and edge["relation"] == "invokes"
        )
        self.assertEqual(declared["origins"], ["alpha/agents/worker.md:5"])
        self.assertEqual(graph, self.build())

    def test_agent_declarations_prefer_same_plugin_and_accept_qualified_refs(self) -> None:
        for plugin in ("alpha", "beta"):
            path = self.root / plugin / "commands" / "task.md"
            path.write_text("# task\n", encoding="utf-8")
        (self.root / "alpha/agents/worker.md").write_text(
            "# worker\n\n"
            "## Commands\n\n"
            "- `task`\n"
            "- `beta/task`\n",
            encoding="utf-8",
        )

        graph = self.build()
        targets = {
            edge["to"]
            for edge in graph["edges"]
            if edge["from"] == "agent:alpha/worker" and edge["relation"] == "invokes"
        }
        self.assertEqual(targets, {"command:alpha/task", "command:beta/task"})

    def test_agent_declarations_reject_unknown_refs(self) -> None:
        (self.root / "beta/agents/reviewer.md").write_text(
            "# reviewer\n\n## Primary skills\n\n- `missing`\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(component_graph.GraphError, "unknown skill `missing`"):
            self.build()

    def test_agent_routing_boundaries_include_only_known_agent_handoffs(self) -> None:
        for plugin in ("alpha", "beta"):
            (self.root / plugin / "agents" / "lead.md").write_text(
                "# lead\n",
                encoding="utf-8",
            )
        (self.root / "alpha/agents/worker.md").write_text(
            "# worker\n\n"
            "## Routing boundaries\n\n"
            "Hand off locally to `lead`, cross-plugin to `beta/lead`, and ignore "
            "skill or prose refs such as `root` and `not an agent`.\n",
            encoding="utf-8",
        )

        graph = self.build()
        targets = {
            edge["to"]
            for edge in graph["edges"]
            if edge["from"] == "agent:alpha/worker"
            and edge["relation"] == "routes-to"
        }
        self.assertEqual(targets, {"agent:alpha/lead", "agent:beta/lead"})

    def test_rule_routes_reject_ambiguous_unqualified_refs(self) -> None:
        for plugin in ("gamma", "delta"):
            self._add_plugin(
                plugin,
                skills=["shared"],
                commands=[],
                rules=[],
                agents=[],
            )
        (self.root / "alpha/rules/defaults.md").write_text(
            "# defaults\n\n## Routing constraints\n\nRoute to `shared`.\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(component_graph.GraphError, "ambiguous skill `shared`"):
            self.build()

    def test_resolve_is_breadth_parallel_visit_once_and_reports_cycle_edges(self) -> None:
        result = component_graph.resolve_graph(self.build(), "skill:alpha/root", ["chains-to"])
        self.assertEqual(
            result["artifact_kind"],
            "component-relationship-candidate-closure",
        )
        self.assertIn("host-relevance-selection", result["candidate_semantics"])
        self.assertEqual(
            [level["candidates"] for level in result["levels"]],
            [
                ["skill:alpha/root"],
                [
                    "external-skill:ext-one",
                    "external-skill:source-only",
                    "skill:alpha/left",
                    "skill:alpha/right",
                ],
                ["skill:alpha/join"],
            ],
        )
        self.assertEqual(result["candidate_count"], 6)
        flattened = [node for level in result["levels"] for node in level["candidates"]]
        self.assertEqual(len(flattened), len(set(flattened)))
        self.assertEqual(
            result["levels"][1]["parallel_candidates"],
            result["levels"][1]["candidates"],
        )
        self.assertEqual(result["blocked_edges"], [])
        self.assertEqual(result["unavailable_nodes"], [])
        cycle_pairs = {(edge["from"], edge["to"]) for edge in result["cycle_edges"]}
        self.assertIn(("skill:alpha/join", "skill:alpha/root"), cycle_pairs)
        self.assertIn(("skill:alpha/root", "skill:alpha/left"), cycle_pairs)

    def test_default_resolution_follows_cross_element_references_deterministically(self) -> None:
        result = component_graph.resolve_graph(self.build(), "agent:alpha/worker")
        levels = [level["candidates"] for level in result["levels"]]
        self.assertEqual(levels[0], ["agent:alpha/worker"])
        self.assertEqual(levels[1], ["command:alpha/run"])
        self.assertEqual(levels[2], ["skill:beta/remote"])
        self.assertEqual(
            result["levels"][2]["sequential_candidates"],
            ["skill:beta/remote"],
        )

    def test_available_only_skips_explicitly_uninstalled_nodes_and_reports_blocks(self) -> None:
        graph = self.build()
        nodes = {node["id"]: node for node in graph["nodes"]}
        nodes["skill:alpha/root"]["installed"] = True
        nodes["skill:alpha/left"]["installed"] = True
        nodes["skill:alpha/right"]["installed"] = False
        nodes["skill:alpha/join"]["installed"] = True
        nodes["external-skill:ext-one"]["installed"] = False
        nodes["external-skill:source-only"]["installed"] = False

        result = component_graph.resolve_graph(
            graph,
            "skill:alpha/root",
            ["chains-to"],
            available_only=True,
        )

        self.assertEqual(
            [level["candidates"] for level in result["levels"]],
            [
                ["skill:alpha/root"],
                ["skill:alpha/left"],
                ["skill:alpha/join"],
            ],
        )
        self.assertEqual(result["candidate_count"], 3)
        self.assertEqual(
            [node["id"] for node in result["unavailable_nodes"]],
            [
                "external-skill:ext-one",
                "external-skill:source-only",
                "skill:alpha/right",
            ],
        )
        self.assertEqual(len(result["blocked_edges"]), 3)
        self.assertTrue(
            all(
                edge["blocked_reason"] == "target-installed-false"
                for edge in result["blocked_edges"]
            )
        )
        self.assertNotIn(
            "skill:alpha/right",
            {
                edge["from"]
                for edge in result["considered_edges"]
            },
        )
        cycle_pairs = {(edge["from"], edge["to"]) for edge in result["cycle_edges"]}
        self.assertIn(("skill:alpha/join", "skill:alpha/root"), cycle_pairs)

    def test_available_only_reports_an_unavailable_root_without_traversal(self) -> None:
        graph = self.build()
        root = next(node for node in graph["nodes"] if node["id"] == "skill:alpha/root")
        root["installed"] = False

        result = component_graph.resolve_graph(
            graph,
            "skill:alpha/root",
            available_only=True,
        )

        self.assertEqual(result["candidate_count"], 0)
        self.assertEqual(result["levels"], [])
        self.assertEqual(result["cycle_edges"], [])
        self.assertEqual(
            [node["id"] for node in result["unavailable_nodes"]],
            ["skill:alpha/root"],
        )

    def test_resolution_depth_is_not_limited_by_python_recursion(self) -> None:
        count = 1200
        graph = {
            "schema_version": "1.0",
            "resolution": {"traverse_relations": ["chains-to"]},
            "nodes": [{"id": f"skill:alpha/n{index}"} for index in range(count)],
            "edges": [
                {
                    "from": f"skill:alpha/n{index}",
                    "to": f"skill:alpha/n{index + 1}",
                    "relation": "chains-to",
                    "execution": "parallel",
                    "origins": ["test"],
                }
                for index in range(count - 1)
            ],
        }
        result = component_graph.resolve_graph(graph, "skill:alpha/n0")
        self.assertEqual(result["candidate_count"], count)
        self.assertEqual(len(result["levels"]), count)
        self.assertEqual(result["cycle_edges"], [])

    def test_same_breadth_sequential_dependency_is_not_grouped_as_parallel(self) -> None:
        graph = {
            "schema_version": "1.0",
            "resolution": {"traverse_relations": ["uses"]},
            "nodes": [
                {"id": "skill:alpha/root"},
                {"id": "skill:alpha/a"},
                {"id": "skill:alpha/b"},
            ],
            "edges": [
                {
                    "from": "skill:alpha/root",
                    "to": "skill:alpha/a",
                    "relation": "uses",
                    "execution": "parallel",
                    "origins": ["test"],
                },
                {
                    "from": "skill:alpha/root",
                    "to": "skill:alpha/b",
                    "relation": "uses",
                    "execution": "parallel",
                    "origins": ["test"],
                },
                {
                    "from": "skill:alpha/a",
                    "to": "skill:alpha/b",
                    "relation": "uses",
                    "execution": "sequential",
                    "origins": ["test"],
                },
            ],
        }

        result = component_graph.resolve_graph(graph, "skill:alpha/root")

        self.assertEqual(
            result["levels"][1]["candidates"],
            ["skill:alpha/a", "skill:alpha/b"],
        )
        self.assertEqual(result["levels"][1]["parallel_candidates"], ["skill:alpha/a"])
        self.assertEqual(result["levels"][1]["sequential_candidates"], ["skill:alpha/b"])
        self.assertEqual(
            [
                (edge["from"], edge["to"])
                for edge in result["ordered_constraints"]
            ],
            [("skill:alpha/a", "skill:alpha/b")],
        )

    def test_generated_full_graph_write_and_drift_check_accept_two_sided_cycles(self) -> None:
        stdout = StringIO()
        with redirect_stdout(stdout):
            generated = component_graph.main(
                [
                    "build",
                    "--root",
                    str(self.root),
                    "--contract",
                    str(self.contract),
                    "--output",
                    "component-graph.json",
                ]
            )
        self.assertEqual(generated, 0)
        output = self.root / "component-graph.json"
        self.assertTrue(output.is_file())
        first = output.read_bytes()

        with redirect_stdout(stdout):
            result = component_graph.main(
                ["build", "--check", "--root", str(self.root), "--contract", str(self.contract)]
            )
        self.assertEqual(result, 0)
        self.assertIn("Generated component graph is current", stdout.getvalue())
        self.assertIn("preserved cycle edge", stdout.getvalue())
        self.assertEqual(output.read_bytes(), first)

        output.write_text("{}\n", encoding="utf-8")
        stderr = StringIO()
        with redirect_stderr(stderr):
            stale = component_graph.main(
                ["build", "--check", "--root", str(self.root), "--contract", str(self.contract)]
            )
        self.assertEqual(stale, 1)
        self.assertIn("generated graph is stale", stderr.getvalue())

    def test_unknown_explicit_reference_fails_closed(self) -> None:
        data = json.loads(self.contract.read_text(encoding="utf-8"))
        data["references"].append(
            {
                "from": "skill:alpha/root",
                "to": "agent:beta/missing",
                "relation": "spawns",
            }
        )
        self.contract.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(component_graph.GraphError, "unknown target"):
            self.build()


class RepositoryGraphContractTests(unittest.TestCase):
    def test_seo_declares_its_external_runtime_chain(self) -> None:
        graph = component_graph.build_graph(
            ROOT,
            ROOT / "references/component-graph.json",
        )
        targets = {
            edge["to"]
            for edge in graph["edges"]
            if edge["from"] == "skill:marketing/seo"
            and edge["relation"] == "chains-to"
        }
        self.assertTrue(
            {
                "external-skill:browserbase-search",
                "external-skill:browserbase-fetch",
                "external-skill:browserbase-competitor-analysis",
                "external-skill:unslop",
                "external-skill:stop-slop",
            }.issubset(targets)
        )


if __name__ == "__main__":
    unittest.main()
