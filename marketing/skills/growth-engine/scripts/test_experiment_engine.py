#!/usr/bin/env python3
"""Contract tests for generalized experiment configuration."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("experiment-engine.py")
SPEC = importlib.util.spec_from_file_location("experiment_engine", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExperimentConfigurationTests(unittest.TestCase):
    def test_two_variants_are_valid_without_batch_mode(self) -> None:
        self.assertEqual(
            MODULE.parse_variants('["control", "variant"]', False),
            ["control", "variant"],
        )

    def test_more_than_two_variants_requires_batch_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "--batch-mode"):
            MODULE.parse_variants('["a", "b", "c"]', False)

    def test_duplicate_variants_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicates"):
            MODULE.parse_variants('["same", "same"]', False)

    def test_sample_floor_is_explicit_and_positive(self) -> None:
        self.assertEqual(MODULE.get_min_samples(27), 27)
        with self.assertRaisesRegex(ValueError, "at least 2"):
            MODULE.get_min_samples(1)


if __name__ == "__main__":
    unittest.main()
