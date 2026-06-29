#!/usr/bin/env python3
"""
Score a prospect against a simple ICP definition.

Usage:
    python score_prospect.py --company "Acme" --employees 45 --stage "Series B" --has-github --has-slack
    python score_prospect.py --help
"""

import argparse


def score(args: argparse.Namespace) -> dict:
    points = 0
    max_points = 0
    signals = []

    def add(condition: bool, weight: int, label: str) -> None:
        nonlocal points, max_points
        max_points += weight
        if condition:
            points += weight
            signals.append(f"  ✓ (+{weight}) {label}")
        else:
            signals.append(f"  ✗ (  0) {label}")

    # Firmographic
    add(10 <= args.employees <= 200, 3, f"Employees {args.employees} in 10–200 range")
    add(args.stage in ["Series A", "Series B", "Series C"], 3, f"Stage: {args.stage}")
    add(args.revenue_m is not None and 2 <= args.revenue_m <= 50, 2, f"Revenue ${'?' if args.revenue_m is None else str(args.revenue_m)}M ARR in $2–50M range")

    # Technographic
    add(args.has_github, 2, "Uses GitHub/GitLab")
    add(args.has_slack, 1, "Uses Slack")
    add(args.has_linear, 1, "Uses Linear/Jira")
    add(args.uses_ai_coding, 2, "Already uses AI coding tools")

    # Trigger signals
    add(args.recently_hired, 2, "Recently hired 3+ engineers")
    add(args.recently_raised, 2, "Recently raised funding")
    add(args.posted_about_pain, 3, "Posted about engineering velocity pain")
    add(args.using_competitor, 2, "Currently using a competitor")

    # Disqualifiers (auto-zero the score)
    disqualified = False
    if args.air_gapped:
        disqualified = True
        signals.append("  ✗ DISQUALIFIED: Air-gapped infrastructure")
    if args.employees < 5:
        disqualified = True
        signals.append("  ✗ DISQUALIFIED: Too small (<5 engineers)")

    pct = int(100 * points / max_points) if max_points > 0 and not disqualified else 0
    return {
        "company": args.company,
        "score": pct,
        "points": points,
        "max_points": max_points,
        "disqualified": disqualified,
        "signals": signals,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Score a prospect against ICP criteria")
    p.add_argument("--company", default="Unknown")
    p.add_argument("--employees", type=int, default=0)
    p.add_argument("--stage", default="", help="Seed/Series A/Series B/Series C/Public")
    p.add_argument("--revenue-m", type=float, default=None)
    p.add_argument("--has-github", action="store_true")
    p.add_argument("--has-slack", action="store_true")
    p.add_argument("--has-linear", action="store_true")
    p.add_argument("--uses-ai-coding", action="store_true")
    p.add_argument("--recently-hired", action="store_true")
    p.add_argument("--recently-raised", action="store_true")
    p.add_argument("--posted-about-pain", action="store_true")
    p.add_argument("--using-competitor", action="store_true")
    p.add_argument("--air-gapped", action="store_true")
    args = p.parse_args()

    result = score(args)
    print(f"\nICP Score: {result['company']}")
    print(f"  Score: {result['score']}% ({result['points']}/{result['max_points']} points)")
    if result["disqualified"]:
        print("  Status: DISQUALIFIED")
    elif result["score"] >= 70:
        print("  Status: Strong ICP fit")
    elif result["score"] >= 40:
        print("  Status: Partial fit — investigate further")
    else:
        print("  Status: Weak fit — deprioritize")
    print("\nSignals:")
    for s in result["signals"]:
        print(s)


if __name__ == "__main__":
    main()
