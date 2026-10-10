#!/usr/bin/env python3
"""Protect explicit workspace selection and the limit of local intake proof."""

import tempfile
import unittest
from pathlib import Path

import brain_inventory


class WorkspaceInventoryTests(unittest.TestCase):
    def test_nested_guidance_keeps_explicit_workspace_and_root_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("This repo uses partial AFS mode.\n")
            child = root / "subsystem"
            child.mkdir()
            (child / "AGENTS.md").write_text("Use a native company standard here.\n")
            data = brain_inventory.build_inventory(root, include_memory=False)
            self.assertEqual(data["workspace_root"], str(root.resolve()))
            self.assertEqual(data["mode"], "partial-afs")
            self.assertEqual(len(data["instruction_files"]), 2)
            self.assertNotIn("brain_count", data)

    def test_local_empty_queue_does_not_claim_remote_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            data = brain_inventory.build_inventory(Path(directory), include_memory=False)
            self.assertEqual(data["local_legacy_intake"]["total_files"], 0)
            self.assertEqual(data["drive_intake"]["status"], "not_inspected")
            self.assertEqual(data["mode"], "missing")

    def test_explicit_subdirectory_is_not_replaced_by_nested_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            child = root / "selected"
            child.mkdir()
            nested = child / "nested"
            nested.mkdir()
            (nested / "AGENTS.md").write_text("Strict AFS mode\n")
            data = brain_inventory.build_inventory(child, include_memory=False)
            self.assertEqual(data["workspace_root"], str(child.resolve()))
            self.assertEqual(data["mode"], "missing")


if __name__ == "__main__":
    unittest.main()
