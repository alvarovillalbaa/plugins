#!/usr/bin/env python3
"""Verify a site's AI-discovery files exist and are valid.

Checks for the artifacts that make a site discoverable by AI agents and answer
engines:
  - /llms.txt           (valid markdown, has H1 + summary)
  - /llms-full.txt      (optional, full-content variant)
  - /.well-known/agent-card.json  (valid JSON, required fields)
  - /robots.txt         (does not block AI crawlers wholesale)

Works against a live base URL or a local directory of built files.

Usage:
    python check_ai_discovery.py https://example.com
    python check_ai_discovery.py ./public          # local build dir
    python check_ai_discovery.py https://example.com --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

AGENT_CARD_REQUIRED = ["name", "description", "url"]
CARD_PATHS = [".well-known/agent-card.json", "agent-card.json"]


def get(base: str, path: str) -> tuple[bool, str]:
    if base.startswith(("http://", "https://")):
        url = base.rstrip("/") + "/" + path
        try:
            req = Request(url, headers={"User-Agent": "ai-discovery-check/1.0"})
            with urlopen(req, timeout=15) as resp:  # noqa: S310
                return True, resp.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError):
            return False, ""
    local = os.path.join(base, path)
    if os.path.isfile(local):
        with open(local, encoding="utf-8", errors="replace") as fh:
            return True, fh.read()
    return False, ""


def check_llms_txt(content: str) -> list[str]:
    issues = []
    if not content.lstrip().startswith("#"):
        issues.append("missing H1 title line")
    if ">" not in content:
        issues.append("missing '>' summary blockquote")
    if len(content.strip()) < 40:
        issues.append("suspiciously short")
    return issues


def check_agent_card(content: str) -> list[str]:
    issues = []
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    for field in AGENT_CARD_REQUIRED:
        if field not in data:
            issues.append(f"missing required field '{field}'")
    return issues


def run(base: str) -> dict:
    result: dict = {"base": base, "checks": {}}

    ok, content = get(base, "llms.txt")
    result["checks"]["llms.txt"] = {
        "present": ok,
        "issues": check_llms_txt(content) if ok else ["not found"],
    }

    ok_full, _ = get(base, "llms-full.txt")
    result["checks"]["llms-full.txt"] = {"present": ok_full, "issues": [] if ok_full else ["optional: not found"]}

    card_found = False
    for p in CARD_PATHS:
        ok_card, card = get(base, p)
        if ok_card:
            card_found = True
            result["checks"]["agent-card.json"] = {
                "present": True, "path": p, "issues": check_agent_card(card),
            }
            break
    if not card_found:
        result["checks"]["agent-card.json"] = {"present": False, "issues": ["not found"]}

    ok_robots, robots = get(base, "robots.txt")
    robots_issues = []
    if ok_robots:
        low = robots.lower()
        if "user-agent: *" in low and "disallow: /" in low.split("user-agent: *", 1)[1][:80]:
            robots_issues.append("robots.txt may block all crawlers (Disallow: /)")
    else:
        robots_issues.append("not found")
    result["checks"]["robots.txt"] = {"present": ok_robots, "issues": robots_issues}

    blocking = []
    for name, c in result["checks"].items():
        if name in ("llms.txt", "agent-card.json") and (not c["present"] or c["issues"]):
            blocking.append(name)
    result["ok"] = not blocking
    result["blocking"] = blocking
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("base", help="base URL or local build directory")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    result = run(args.base)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name, c in result["checks"].items():
            mark = "ok " if c["present"] and not c["issues"] else "FAIL"
            issues = f"  ({'; '.join(c['issues'])})" if c["issues"] else ""
            print(f"[{mark}] {name}{issues}")
        print(f"\nOverall: {'PASS' if result['ok'] else 'NEEDS WORK -> ' + ', '.join(result['blocking'])}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
