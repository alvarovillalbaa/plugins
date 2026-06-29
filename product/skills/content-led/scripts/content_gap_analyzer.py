#!/usr/bin/env python3
"""Compare existing content topics against ICP search intent to find gaps.

Inputs are two newline-delimited text files:
  --have   topics you already cover (one per line; titles or slugs)
  --want   intent topics your ICP searches for (one per line)

Matching is fuzzy by shared keyword tokens (stopwords removed). Reports covered
topics, uncovered intent (the gaps), and weakly-covered intent.

Usage:
    python content_gap_analyzer.py --have existing.txt --want intent.txt
"""
import argparse
import re

STOP = set("the a an of to for and or in on with how do i my your we our is are "
           "what why when guide tutorial best vs using use".split())


def tokens(line):
    words = re.findall(r"[a-z0-9]+", line.lower())
    return {w for w in words if w not in STOP and len(w) > 2}


def load(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def overlap(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--have", required=True, help="File of existing content topics")
    ap.add_argument("--want", required=True, help="File of ICP intent topics")
    ap.add_argument("--strong", type=float, default=0.34, help="Strong-match threshold")
    ap.add_argument("--weak", type=float, default=0.18, help="Weak-match threshold")
    args = ap.parse_args()

    have = [(t, tokens(t)) for t in load(args.have)]
    want = load(args.want)

    gaps, weak, covered = [], [], []
    for w in want:
        wt = tokens(w)
        best = max((overlap(wt, ht) for _, ht in have), default=0.0)
        if best >= args.strong:
            covered.append((w, round(best, 2)))
        elif best >= args.weak:
            weak.append((w, round(best, 2)))
        else:
            gaps.append(w)

    print("# Content Gap Analysis\n")
    print(f"## Gaps — uncovered intent ({len(gaps)})  [priority]\n")
    for g in gaps:
        print(f"- {g}")
    print(f"\n## Weakly covered ({len(weak)})  [refresh/expand]\n")
    for w, s in weak:
        print(f"- {w}  (best match {s})")
    print(f"\n## Covered ({len(covered)})\n")
    for c, s in covered:
        print(f"- {c}  (match {s})")


if __name__ == "__main__":
    main()
