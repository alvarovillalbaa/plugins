#!/usr/bin/env python3
"""Extract buyer objections and motivators from a sales-call transcript.

Reads a plain-text transcript (file path or stdin) and surfaces sentences that
signal objections (risk, doubt, cost concern) versus motivators (desire, gain,
intent). Heuristic and dependency-free: meant as a first pass for a human to
refine, not a classifier.

Usage:
    python extract_objections.py transcript.txt
    cat transcript.txt | python extract_objections.py -
"""
import argparse
import re
import sys

OBJECTION_CUES = [
    "too expensive", "expensive", "budget", "cost", "pricey", "afford",
    "not sure", "worried", "concern", "risk", "but ", "however", "problem",
    "difficult", "hard to", "lock-in", "lock in", "migrate", "migration",
    "already use", "already have", "competitor", "security", "compliance",
    "don't think", "do not think", "hesitant", "skeptical", "what about",
]
MOTIVATOR_CUES = [
    "we need", "we want", "looking for", "hoping to", "goal is", "trying to",
    "would love", "ideally", "save time", "save money", "faster", "easier",
    "scale", "grow", "reduce", "improve", "frustrated with", "tired of",
    "pain", "wish", "if only", "must have", "deadline", "priority",
]


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in parts if p.strip()]


def classify(sentence):
    low = sentence.lower()
    obj = [c for c in OBJECTION_CUES if c in low]
    mot = [c for c in MOTIVATOR_CUES if c in low]
    return obj, mot


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="Transcript file path, or - for stdin")
    args = ap.parse_args()

    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()

    objections, motivators = [], []
    for s in split_sentences(text):
        obj, mot = classify(s)
        if obj:
            objections.append((s, sorted(set(obj))))
        if mot:
            motivators.append((s, sorted(set(mot))))

    print("# Extracted Buyer Signals\n")
    print(f"## Objections / Risks ({len(objections)})\n")
    for s, cues in objections:
        print(f"- {s}\n  - cues: {', '.join(cues)}")
    print(f"\n## Motivators / Desired Gains ({len(motivators)})\n")
    for s, cues in motivators:
        print(f"- {s}\n  - cues: {', '.join(cues)}")

    if not objections and not motivators:
        print("No clear signals found. Review the transcript manually.", file=sys.stderr)


if __name__ == "__main__":
    main()
