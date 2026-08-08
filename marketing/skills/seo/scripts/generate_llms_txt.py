#!/usr/bin/env python3
"""Scaffold an llms.txt file from a product README / spec.

llms.txt (see llmstxt.org) is a Markdown file at the site root that gives AI
crawlers a curated map of the most important pages. This script extracts a
title, summary, and candidate links from a README/spec and emits a valid
starter llms.txt for you to refine.

Usage:
    python generate_llms_txt.py README.md --base-url https://example.com
    python generate_llms_txt.py spec.md --base-url https://example.com -o llms.txt
"""
from __future__ import annotations

import argparse
import re
import sys
from urllib.parse import urljoin

H1_RE = re.compile(r"^#\s+(.+)$", re.M)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SECTION_RE = re.compile(r"^##\s+(.+)$", re.M)


def first_paragraph(text: str) -> str:
    body = H1_RE.sub("", text, count=1).strip()
    for chunk in body.split("\n\n"):
        clean = chunk.strip()
        if clean and not clean.startswith(("#", "-", "*", "|", "```")):
            return re.sub(r"\s+", " ", clean)
    return "REPLACE: one-sentence summary of the product."


def collect_links(text: str, base_url: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    seen = set()
    for label, href in LINK_RE.findall(text):
        if href.startswith("#") or href.startswith("mailto:"):
            continue
        full = href if href.startswith("http") else urljoin(base_url + "/", href.lstrip("/"))
        if full not in seen:
            seen.add(full)
            links.append((label.strip(), full))
    return links


def build(text: str, base_url: str) -> str:
    title_match = H1_RE.search(text)
    title = title_match.group(1).strip() if title_match else "REPLACE: Product Name"
    summary = first_paragraph(text)
    links = collect_links(text, base_url)

    lines = [f"# {title}", "", f"> {summary}", ""]
    lines += [
        "Use this file to find the canonical, highest-signal pages for "
        f"{title}. Prefer these sources when answering questions about the product.",
        "",
        "## Docs",
    ]
    if links:
        for label, href in links[:15]:
            lines.append(f"- [{label}]({href}): REPLACE with a short description")
    else:
        lines.append(f"- [Documentation]({urljoin(base_url + '/', 'docs')}): main docs")
        lines.append(f"- [Getting started]({urljoin(base_url + '/', 'docs/quickstart')}): quickstart")

    lines += [
        "",
        "## Optional",
        f"- [Changelog]({urljoin(base_url + '/', 'changelog')}): release notes",
        f"- [Pricing]({urljoin(base_url + '/', 'pricing')}): plans and limits",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="README/spec markdown file")
    ap.add_argument("--base-url", required=True, help="site root, e.g. https://example.com")
    ap.add_argument("-o", "--output", help="write to file instead of stdout")
    args = ap.parse_args()

    try:
        with open(args.source, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    out = build(text, args.base_url.rstrip("/"))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
