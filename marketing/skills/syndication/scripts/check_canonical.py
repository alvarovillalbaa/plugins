#!/usr/bin/env python3
"""
Check that a URL has a canonical tag set before syndicating.

Usage:
    python check_canonical.py https://example.com/blog/my-post
"""

import sys
import urllib.request
import urllib.error
import re


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "canonical-checker/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="replace")


def find_canonical(html: str) -> str | None:
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    )
    if not match:
        match = re.search(
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
            html,
            re.IGNORECASE,
        )
    return match.group(1) if match else None


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python check_canonical.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    print(f"Checking: {url}")

    try:
        html = fetch_html(url)
    except urllib.error.URLError as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)

    canonical = find_canonical(html)

    if canonical:
        print(f"✓ Canonical tag found: {canonical}")
        if canonical == url:
            print("✓ Canonical points to itself — safe to syndicate.")
        else:
            print(f"⚠ Canonical points to a different URL: {canonical}")
            print("  Verify this is intentional before syndicating.")
    else:
        print("✗ No canonical tag found.")
        print("  Add <link rel='canonical' href='...'> before syndicating.")
        sys.exit(1)


if __name__ == "__main__":
    main()
