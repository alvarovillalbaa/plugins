from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("completion-gate.py")


class CompletionGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def run_gate(self, payload: object, **environment: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update({"TMPDIR": str(self.tmp), "AGENTIC_DEV_MAX": "1"})
        env.update(environment)
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
            env=env,
            cwd=self.tmp,
        )

    def test_malformed_input_is_non_blocking(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="not-json",
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "TMPDIR": str(self.tmp)},
            cwd=self.tmp,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_default_gate_blocks_once_then_releases(self) -> None:
        payload = {"session_id": "session-one", "hook_event_name": "Stop"}

        first = self.run_gate(payload)
        second = self.run_gate(payload)

        self.assertEqual(first.returncode, 0)
        self.assertEqual(json.loads(first.stdout)["decision"], "block")
        self.assertIn("Verify the task", json.loads(first.stdout)["reason"])
        self.assertEqual(second.returncode, 0)
        self.assertEqual(second.stdout, "")

    def test_recursive_stop_without_incomplete_signal_is_non_blocking(self) -> None:
        payload = {
            "session_id": "session-two",
            "hook_event_name": "Stop",
            "stop_hook_active": True,
        }

        result = self.run_gate(payload)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_loop_completion_promise_removes_state(self) -> None:
        state = self.tmp / "loop.md"
        state.write_text(
            """---
iteration: 1
max_iterations: 3
completion_promise: DONE
spec_file: null
---
Finish the task.
""",
            encoding="utf-8",
        )
        result = self.run_gate(
            {"session_id": "loop", "last_assistant_message": "<promise>DONE</promise>"},
            AGENTIC_DEV_STATE_FILE=str(state),
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertFalse(state.exists())

    def test_loop_reinjects_prompt_and_increments_iteration(self) -> None:
        state = self.tmp / "loop.md"
        state.write_text(
            """---
iteration: 1
max_iterations: 3
completion_promise: DONE
spec_file: spec.md
---
Finish the task.
""",
            encoding="utf-8",
        )
        transcript = self.tmp / "transcript.jsonl"
        transcript.write_text(
            json.dumps({"message": {"role": "assistant", "content": "Still working"}}) + "\n",
            encoding="utf-8",
        )

        result = self.run_gate(
            {"session_id": "loop", "transcript_path": str(transcript)},
            AGENTIC_DEV_STATE_FILE=str(state),
        )

        output = json.loads(result.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertEqual(output["reason"], "Finish the task.")
        self.assertIn("iteration 2/3", output["systemMessage"])
        self.assertIn("iteration: 2", state.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
