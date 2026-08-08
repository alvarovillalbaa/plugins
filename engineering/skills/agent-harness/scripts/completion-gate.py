#!/usr/bin/env python3
"""Claude Stop-hook completion gate with an optional bounded loop mode."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import deque
from pathlib import Path
from typing import Any


DEFAULT_REASON = """Before stopping, do each of these checks:

1. Re-read the original user message and account for every request and constraint.
2. Confirm repository instructions and any active plan or specification were followed.
3. Resolve pending steps, unchecked items, recent tool errors, and review or CI follow-ups.
4. Support completion claims with fresh verification evidence.
5. Confirm the worktree and any requested handoff state are intentional.

If the user explicitly asked to stop, defer work, or skip a check, respect that instruction.
Otherwise, continue working instead of narrating unfinished work."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate one Claude Stop-hook JSON event and emit a block decision when needed."
    )
    return parser.parse_args(argv)


def read_payload() -> dict[str, Any] | None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return None
    return payload if isinstance(payload, dict) else None


def safe_unlink(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def parse_int(value: object, default: int) -> int:
    try:
        parsed = int(str(value))
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def state_file() -> Path:
    configured = os.environ.get("AGENTIC_DEV_STATE_FILE", "").strip()
    if configured:
        return Path(configured).expanduser()
    state_dir = Path(os.environ.get("AGENTIC_DEV_STATE_DIR", ".agentic")).expanduser()
    current = state_dir / "agentic-dev-loop.local.md"
    legacy = Path(".claude/agentic-dev-loop.local.md")
    return legacy if not current.is_file() and legacy.is_file() else current


def parse_state(path: Path) -> tuple[dict[str, str], str] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---\n"):
        return None
    parts = text.split("---", 2)
    if len(parts) != 3:
        return None
    metadata: dict[str, str] = {}
    for raw in parts[1].splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, parts[2].lstrip("\n")


def transcript_tail(path: Path, lines: int = 80) -> str:
    try:
        with path.open(encoding="utf-8", errors="ignore") as handle:
            return "".join(deque(handle, maxlen=lines))
    except OSError:
        return ""


def last_assistant_text(path: Path) -> str:
    tail = transcript_tail(path, lines=400)
    for raw in reversed(tail.splitlines()):
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            continue
        message = record.get("message", record)
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        content = message.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "\n".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict) and item.get("type") == "text"
            )
    return ""


def emit_block(reason: str, system_message: str | None = None) -> None:
    payload: dict[str, str] = {"decision": "block", "reason": reason}
    if system_message:
        payload["systemMessage"] = system_message
    print(json.dumps(payload, ensure_ascii=False))


def run_loop_mode(path: Path, payload: dict[str, Any]) -> int:
    parsed = parse_state(path)
    if parsed is None:
        print(f"agent-harness: invalid loop state at {path}; stopping loop", file=sys.stderr)
        safe_unlink(path)
        return 0
    metadata, prompt = parsed
    iteration = parse_int(metadata.get("iteration"), -1)
    maximum = parse_int(metadata.get("max_iterations"), -1)
    if iteration < 0 or maximum < 0 or not prompt.strip():
        print(f"agent-harness: incomplete loop state at {path}; stopping loop", file=sys.stderr)
        safe_unlink(path)
        return 0
    if maximum > 0 and iteration >= maximum:
        print(f"agent-harness: maximum loop iterations ({maximum}) reached", file=sys.stderr)
        safe_unlink(path)
        return 0

    promise = metadata.get("completion_promise", "").strip()
    if promise and promise.lower() != "null":
        current_message = payload.get("last_assistant_message")
        if isinstance(current_message, str):
            output = current_message
        else:
            transcript_value = payload.get("transcript_path") or payload.get("transcriptPath")
            transcript = Path(str(transcript_value)).expanduser() if transcript_value else None
            output = last_assistant_text(transcript) if transcript and transcript.is_file() else ""
        matches = re.findall(r"<promise>(.*?)</promise>", output, flags=re.DOTALL)
        normalized = " ".join(matches[-1].split()) if matches else ""
        if normalized == " ".join(promise.split()):
            print("agent-harness: completion promise detected", file=sys.stderr)
            safe_unlink(path)
            return 0

    next_iteration = iteration + 1
    text = path.read_text(encoding="utf-8")
    updated = re.sub(
        r"(?m)^iteration:\s*.*$", f"iteration: {next_iteration}", text, count=1
    )
    path.write_text(updated, encoding="utf-8")

    label = (
        f"iteration {next_iteration}/{maximum}" if maximum > 0 else f"iteration {next_iteration}"
    )
    spec_file = metadata.get("spec_file", "").strip()
    spec_reminder = f" Re-read {spec_file} before this iteration." if spec_file and spec_file != "null" else ""
    if promise and promise.lower() != "null":
        message = (
            f"Dev loop {label}.{spec_reminder} Output <promise>{promise}</promise> only "
            "when the task and all gates are genuinely complete."
        )
    else:
        message = f"Dev loop {label}.{spec_reminder} No completion promise is configured."
    emit_block(prompt.strip(), message)
    return 0


def run_gate_mode(payload: dict[str, Any]) -> int:
    session_id = str(
        payload.get("session_id")
        or payload.get("sessionId")
        or payload.get("conversation_id")
        or payload.get("conversationId")
        or "unknown-session"
    )
    session_key = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id)[:120]
    counter_dir = Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "agent-harness"
    counter_dir.mkdir(parents=True, exist_ok=True)
    counter = counter_dir / session_key
    maximum = parse_int(os.environ.get("AGENTIC_DEV_MAX", "1"), 1)
    count = parse_int(counter.read_text(encoding="utf-8") if counter.is_file() else "0", 0)
    if maximum > 0 and count >= maximum:
        safe_unlink(counter)
        return 0

    transcript_value = payload.get("transcript_path") or payload.get("transcriptPath")
    transcript = Path(str(transcript_value)).expanduser() if transcript_value else None
    current_message = payload.get("last_assistant_message")
    tail = current_message if isinstance(current_message, str) else ""
    if transcript and transcript.is_file():
        tail = f"{transcript_tail(transcript)}\n{tail}"
    incomplete = any(
        pattern.search(tail)
        for pattern in (
            re.compile(r'"status"\s*:\s*"(?:in_progress|pending)"', re.IGNORECASE),
            re.compile(r'"is_error"\s*:\s*true', re.IGNORECASE),
            re.compile(r"- \[ \]"),
        )
    )
    stop_active = payload.get("stop_hook_active", payload.get("stopHookActive", False)) is True
    if stop_active and not incomplete:
        safe_unlink(counter)
        return 0

    next_count = count + 1
    counter.write_text(str(next_count), encoding="utf-8")
    preamble = (
        "Incomplete tasks, unchecked boxes, or recent tool errors were detected."
        if incomplete
        else "Verify the task is genuinely complete before stopping."
    )
    label = f"AGENT_HARNESS ({next_count}/{maximum})" if maximum > 0 else f"AGENT_HARNESS ({next_count})"
    emit_block(f"{label}: {preamble}\n\n{DEFAULT_REASON}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parse_args(argv)
    payload = read_payload()
    if payload is None:
        return 0
    path = state_file()
    return run_loop_mode(path, payload) if path.is_file() else run_gate_mode(payload)


if __name__ == "__main__":
    raise SystemExit(main())
