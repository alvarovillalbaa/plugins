from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "marketing/skills/coursify/scripts/validate_course_manifest.py"
ROUTER_PATH = ROOT / "marketing/skills/content/scripts/detect_content_type.py"
EXAMPLE_PATH = ROOT / "marketing/skills/coursify/examples/course-manifest.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("validate_course_manifest", VALIDATOR_PATH)
ROUTER = load_module("detect_content_type", ROUTER_PATH)


class CourseManifestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def test_complete_multimodal_example_is_valid(self) -> None:
        self.assertEqual(VALIDATOR.validate_manifest(self.manifest), [])

    def test_course_contract_fields_are_required(self) -> None:
        for field in ("entry_level", "desired_transformation", "source_map", "capstone", "production_plan"):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                del manifest[field]
                errors = VALIDATOR.validate_manifest(manifest)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_unknown_and_uncovered_outcomes_fail_closed(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["modules"][0]["aligned_outcomes"] = ["missing-outcome"]
        errors = VALIDATOR.validate_manifest(manifest)
        self.assertTrue(any("unknown 'missing-outcome'" in error for error in errors))
        self.assertTrue(any("'design-tool-contract' is not aligned" in error for error in errors))

    def test_malformed_alignment_returns_errors_instead_of_crashing(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["modules"][0]["aligned_outcomes"] = [{"not": "hashable"}]
        errors = VALIDATOR.validate_manifest(manifest)
        self.assertTrue(any("aligned_outcomes[0]" in error for error in errors), errors)

    def test_assessment_type_must_be_a_string(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["modules"][0]["lessons"][0]["assessment"]["type"] = 1
        errors = VALIDATOR.validate_manifest(manifest)
        self.assertTrue(any("assessment.type must be a non-empty string" in error for error in errors))

    def test_every_lesson_needs_a_production_artifact(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["production_plan"] = [
            artifact
            for artifact in manifest["production_plan"]
            if artifact["canonical_unit_id"] != "schema-first-tools"
        ]
        errors = VALIDATOR.validate_manifest(manifest)
        self.assertIn("lesson 'schema-first-tools' has no production-plan artifact", errors)

    def test_video_requires_an_accessible_alternative(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["modules"][0]["lessons"][0]["formats"] = ["text", "code", "video-based"]
        manifest["accessibility"]["provisions"] = ["Keyboard access for interactive labs"]
        errors = VALIDATOR.validate_manifest(manifest)
        self.assertTrue(any("captions or transcripts" in error for error in errors))


class ContentCourseRoutingTests(unittest.TestCase):
    def test_course_target_outranks_generic_repurposing(self) -> None:
        matches = ROUTER.classify("Turn this webinar into a course for new engineers")
        self.assertEqual(matches[0]["skill"], "coursify")

    def test_modality_qualified_course_target_routes_to_coursify(self) -> None:
        requests = (
            "Turn this webinar into an interactive course for new engineers",
            "Convert this documentation into a video-based course",
            "Transform these notes into a code-based self-paced course",
        )
        for request in requests:
            with self.subTest(request=request):
                matches = ROUTER.classify(request)
                self.assertEqual(matches[0]["skill"], "coursify")

    def test_course_source_with_post_target_stays_repurposing(self) -> None:
        matches = ROUTER.classify("Turn this course into five LinkedIn posts")
        self.assertEqual(matches[0]["skill"], "repurposing")


if __name__ == "__main__":
    unittest.main()
