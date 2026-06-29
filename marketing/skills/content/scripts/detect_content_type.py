#!/usr/bin/env python3
"""Classify a free-text content request and suggest the child skill to route to.

Heuristic keyword classifier — no network, no deps. Returns the best-matching
content type and the skill that owns it, plus runner-up matches so the router
can disambiguate.

Usage:
    python detect_content_type.py "turn this webinar into 5 linkedin posts"
    python detect_content_type.py --json "rewrite this AI-sounding intro"
    echo "find keywords for our pricing page" | python detect_content_type.py -
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# type -> (owning skill, keyword patterns)
RULES: dict[str, tuple[str, list[str]]] = {
    "keyword-research": ("keywords", [
        r"\bkeyword", r"\bsearch volume", r"\bsearch intent", r"\bserp",
        r"\btopic cluster", r"\brank for\b",
    ]),
    "humanize": ("humanizing", [
        r"\bhumaniz", r"sounds? like ai", r"ai[- ]sounding", r"too robotic",
        r"\bstiff\b", r"de-?slop", r"remove ai tells",
    ]),
    "repurpose": ("repurposing", [
        r"\brepurpos", r"turn .* into", r"break .* into", r"atomi[sz]e",
        r"into \d+ (posts|tweets|threads)", r"distribution pack",
    ]),
    "syndicate": ("syndication", [
        r"\bsyndicat", r"\bcross-?post", r"\brepost", r"dev\.to|hashnode|medium",
        r"\bcanonical\b", r"newsletter distribution",
    ]),
    "context-to-content": ("context-to-content", [
        r"support ticket", r"customer question", r"sales objection",
        r"\bfaq\b", r"help article", r"\bknowledge base\b",
    ]),
    "copywrite": ("copywrite", [
        r"\bcopy\b", r"\bcopywrit", r"headline", r"\btagline", r"hero copy",
        r"landing page copy", r"\bcta\b", r"value prop",
    ]),
}


def classify(text: str) -> list[dict]:
    t = text.lower()
    scored = []
    for ctype, (skill, patterns) in RULES.items():
        hits = sum(1 for p in patterns if re.search(p, t))
        if hits:
            scored.append({"type": ctype, "skill": skill, "score": hits})
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("request", help="the content request, or '-' to read stdin")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    text = sys.stdin.read() if args.request == "-" else args.request
    results = classify(text)

    if args.json:
        print(json.dumps({"matches": results}, indent=2))
        return 0

    if not results:
        print("No clear match. Route to the content router for manual triage, "
              "or default to `copywrite` for general writing.")
        return 1

    best = results[0]
    print(f"Best match : {best['type']}  ->  skill: {best['skill']}")
    if len(results) > 1:
        print("Runner-ups :")
        for r in results[1:]:
            print(f"  - {r['type']} ({r['skill']}), score {r['score']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
