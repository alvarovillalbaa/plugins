#!/usr/bin/env python3
"""Estimate current-month AWS spend via the Cost Explorer API.

Reports month-to-date unblended cost, grouped by service, and projects a simple
end-of-month total from the current daily run rate.

Requires boto3 and credentials with `ce:GetCostAndUsage`. Cost Explorer charges
a small per-request fee.

Usage:
    python list_running_costs.py
    python list_running_costs.py --profile my-dev --top 10
    python list_running_costs.py --json
"""

import argparse
import calendar
import datetime as dt
import json
import sys


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Estimate current-month AWS costs.")
    p.add_argument("--profile", help="AWS profile name")
    p.add_argument("--region", default="us-east-1",
                   help="Region for the Cost Explorer endpoint (default us-east-1)")
    p.add_argument("--top", type=int, default=8, help="Number of services to show")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        import boto3
    except ImportError:
        print("ERROR: boto3 is required. Install with: pip install boto3", file=sys.stderr)
        return 1

    session = boto3.Session(profile_name=args.profile) if args.profile else boto3.Session()
    client = session.client("ce", region_name=args.region)

    today = dt.date.today()
    start = today.replace(day=1)
    # Cost Explorer's End is exclusive; use tomorrow to include today's partial data.
    end = today + dt.timedelta(days=1)

    try:
        resp = client.get_cost_and_usage(
            TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
    except Exception as exc:  # noqa: BLE001 - surface the API/auth error verbatim
        print(f"ERROR calling Cost Explorer: {exc}", file=sys.stderr)
        return 2

    groups = resp["ResultsByTime"][0]["Groups"]
    rows = []
    total = 0.0
    currency = "USD"
    for g in groups:
        amount = float(g["Metrics"]["UnblendedCost"]["Amount"])
        currency = g["Metrics"]["UnblendedCost"]["Unit"]
        rows.append((g["Keys"][0], amount))
        total += amount
    rows.sort(key=lambda r: r[1], reverse=True)

    days_elapsed = today.day
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    daily_rate = total / days_elapsed if days_elapsed else 0.0
    projected = daily_rate * days_in_month

    if args.json:
        print(json.dumps({
            "period": {"start": start.isoformat(), "end": today.isoformat()},
            "currency": currency,
            "month_to_date": round(total, 2),
            "daily_run_rate": round(daily_rate, 2),
            "projected_month_total": round(projected, 2),
            "by_service": [{"service": s, "cost": round(a, 2)} for s, a in rows],
        }, indent=2))
        return 0

    print(f"AWS cost {start.isoformat()} -> {today.isoformat()} ({currency})")
    print("-" * 48)
    for service, amount in rows[: args.top]:
        print(f"  {service[:34]:<34} {amount:>10.2f}")
    if len(rows) > args.top:
        rest = sum(a for _, a in rows[args.top:])
        print(f"  {'(' + str(len(rows) - args.top) + ' more)':<34} {rest:>10.2f}")
    print("-" * 48)
    print(f"  {'Month to date':<34} {total:>10.2f}")
    print(f"  {'Daily run rate':<34} {daily_rate:>10.2f}")
    print(f"  {'Projected month total':<34} {projected:>10.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
