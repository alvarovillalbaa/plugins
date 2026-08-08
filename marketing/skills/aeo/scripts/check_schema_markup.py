#!/usr/bin/env python3
"""Check a URL (or local HTML file) for Schema.org JSON-LD structured data.

Reports which @type blocks are present, flags AEO-relevant types (FAQPage,
HowTo, QAPage, Article, Product), and exits non-zero when none are found so it
can gate an AEO audit.

Usage:
    python check_schema_markup.py https://example.com/faq
    python check_schema_markup.py ./page.html
    python check_schema_markup.py https://example.com/faq --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.request import Request, urlopen

AEO_TYPES = {"FAQPage", "QAPage", "HowTo", "Article", "Product", "BreadcrumbList"}
JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


def load_html(source: str) -> str:
    if source.startswith(("http://", "https://")):
        req = Request(source, headers={"User-Agent": "aeo-schema-check/1.0"})
        with urlopen(req, timeout=20) as resp:  # noqa: S310 (trusted CLI input)
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    with open(source, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def extract_types(payload: object, found: list[str]) -> None:
    if isinstance(payload, dict):
        t = payload.get("@type")
        if isinstance(t, str):
            found.append(t)
        elif isinstance(t, list):
            found.extend(str(x) for x in t)
        for value in payload.values():
            extract_types(value, found)
    elif isinstance(payload, list):
        for item in payload:
            extract_types(item, found)


def analyze(html: str) -> dict:
    blocks = JSONLD_RE.findall(html)
    types: list[str] = []
    invalid = 0
    for raw in blocks:
        try:
            extract_types(json.loads(raw.strip()), types)
        except json.JSONDecodeError:
            invalid += 1
    unique = sorted(set(types))
    return {
        "jsonld_blocks": len(blocks),
        "invalid_blocks": invalid,
        "types_found": unique,
        "aeo_types": sorted(set(unique) & AEO_TYPES),
        "has_structured_data": bool(blocks) and invalid < len(blocks),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="URL or local HTML file path")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    try:
        html = load_html(args.source)
    except Exception as exc:  # noqa: BLE001 - surface any fetch/read error to CLI
        print(f"error: could not load {args.source}: {exc}", file=sys.stderr)
        return 2

    result = analyze(html)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"JSON-LD blocks found : {result['jsonld_blocks']}")
        print(f"Invalid blocks       : {result['invalid_blocks']}")
        print(f"Types                : {', '.join(result['types_found']) or '(none)'}")
        print(f"AEO-relevant types   : {', '.join(result['aeo_types']) or '(none)'}")
        if not result["aeo_types"]:
            print("\nNo AEO-relevant structured data. Add FAQPage/HowTo/Article "
                  "JSON-LD before relying on snippet capture.")

    return 0 if result["aeo_types"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
