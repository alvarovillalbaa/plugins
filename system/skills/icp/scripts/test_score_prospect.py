#!/usr/bin/env python3
"""Contract tests for the configuration-driven ICP scorer."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("score_prospect.py")
SPEC = importlib.util.spec_from_file_location("score_prospect", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ScoreProspectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = {
            "name": "Example account model",
            "criteria": [
                {
                    "id": "size",
                    "path": "company.employees",
                    "operator": "between",
                    "value": [10, 100],
                    "weight": 3,
                },
                {
                    "id": "regions",
                    "path": "region",
                    "operator": "in",
                    "value": ["EU", "US"],
                    "weight": 1,
                },
            ],
            "disqualifiers": [
                {"id": "blocked", "path": "blocked", "operator": "truthy"}
            ],
            "thresholds": [
                {"min": 75, "label": "Strong fit"},
                {"min": 0, "label": "Needs review"},
            ],
        }

    def test_scores_nested_and_weighted_criteria(self) -> None:
        result = MODULE.score_prospect(
            self.model,
            {"name": "Example", "company": {"employees": 25}, "region": "APAC"},
        )
        self.assertEqual(result["score"], 75.0)
        self.assertEqual(result["status"], "Strong fit")

    def test_disqualifier_zeros_score_but_preserves_raw_score(self) -> None:
        result = MODULE.score_prospect(
            self.model,
            {
                "company": {"employees": 25},
                "region": "EU",
                "blocked": True,
            },
        )
        self.assertEqual(result["raw_score"], 100.0)
        self.assertEqual(result["score"], 0.0)
        self.assertTrue(result["disqualified"])

    def test_missing_fields_are_unmatched_by_default(self) -> None:
        result = MODULE.score_prospect(self.model, {})
        self.assertEqual(result["score"], 0.0)

    def test_strict_missing_rejects_absent_fields(self) -> None:
        with self.assertRaisesRegex(MODULE.ModelError, "company.employees"):
            MODULE.score_prospect(self.model, {}, strict_missing=True)


if __name__ == "__main__":
    unittest.main()
