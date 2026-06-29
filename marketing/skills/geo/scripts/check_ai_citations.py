#!/usr/bin/env python3
"""Check whether a brand/domain shows GEO (generative-engine) citation signals.

This is a baseline harness. It does NOT call a paid SERP/AI API by default;
instead it scores the *citation-readiness* of a page and, when an API key is
present in the environment, can query a live AI-answer endpoint.

Citation-readiness heuristics (what makes LLMs quote a page):
  - quotable statistics (numbers with units / %)
  - explicit definitions ("X is ...")
  - named, attributable claims
  - freshness (visible date)
  - author / organization attribution
  - outbound source citations

Usage:
    python check_ai_citations.py https://example.com/post
    python check_ai_citations.py https://example.com/post --json
    # Optional live check (if you wire one up):
    AI_SEARCH_API_KEY=... python check_ai_citations.py "BrandName" --live
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.request import Request, urlopen

STAT_RE = re.compile(r"\b\d+(\.\d+)?\s?(%|percent|x|ms|s|gb|mb|k|m|bn|billion|million)\b", re.I)
DEFINITION_RE = re.compile(r"\b[A-Z][A-Za-z0-9 ]{2,40}\s+(is|are|refers to|means)\s+", re.I)
DATE_RE = re.compile(r"\b(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b|"
                     r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+20\d{2}\b")
AUTHOR_RE = re.compile(r'(rel=["\']author["\']|"author"|by\s+[A-Z][a-z]+\s+[A-Z][a-z]+)')
CITATION_RE = re.compile(r"<a\b[^>]*href=[\"']https?://", re.I)
TAG_RE = re.compile(r"<[^>]+>")


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "geo-citation-check/1.0"})
    with urlopen(req, timeout=20) as resp:  # noqa: S310 (trusted CLI input)
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def readiness(html: str) -> dict:
    text = TAG_RE.sub(" ", html)
    signals = {
        "quotable_stats": len(STAT_RE.findall(text)),
        "definitions": len(DEFINITION_RE.findall(text)),
        "has_date": bool(DATE_RE.search(html)),
        "has_author": bool(AUTHOR_RE.search(html)),
        "outbound_citations": len(CITATION_RE.findall(html)),
    }
    score = 0
    score += min(signals["quotable_stats"], 5) * 2      # up to 10
    score += min(signals["definitions"], 5) * 2         # up to 10
    score += 5 if signals["has_date"] else 0
    score += 5 if signals["has_author"] else 0
    score += min(signals["outbound_citations"], 10)     # up to 10
    signals["citation_readiness_score"] = score  # out of ~40
    signals["grade"] = (
        "strong" if score >= 28 else "moderate" if score >= 16 else "weak"
    )
    return signals


def live_check(query: str) -> dict:
    key = os.environ.get("AI_SEARCH_API_KEY")
    if not key:
        return {"live": "skipped", "reason": "AI_SEARCH_API_KEY not set"}
    # Wire your provider here (Perplexity, Brave, SerpAPI AI Overviews, etc.).
    return {"live": "not_implemented",
            "reason": "Add provider call for query: " + query}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", help="URL to score, or brand/query for --live")
    ap.add_argument("--live", action="store_true", help="query a live AI endpoint")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    out: dict = {"target": args.target}

    if args.target.startswith(("http://", "https://")):
        try:
            out["readiness"] = readiness(fetch(args.target))
        except Exception as exc:  # noqa: BLE001
            print(f"error: {exc}", file=sys.stderr)
            return 2
    if args.live:
        out["live_result"] = live_check(args.target)

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        r = out.get("readiness")
        if r:
            print(f"Citation readiness : {r['citation_readiness_score']}/40 ({r['grade']})")
            print(f"  quotable stats   : {r['quotable_stats']}")
            print(f"  definitions      : {r['definitions']}")
            print(f"  visible date     : {r['has_date']}")
            print(f"  author signal    : {r['has_author']}")
            print(f"  outbound cites   : {r['outbound_citations']}")
        if "live_result" in out:
            print(f"Live check         : {out['live_result']}")

    grade = out.get("readiness", {}).get("grade")
    return 0 if grade in {"strong", "moderate"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
