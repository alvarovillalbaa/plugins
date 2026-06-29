#!/usr/bin/env python3
"""Estimate current-month Azure spend via the Cost Management query API.

Queries month-to-date actual cost for a subscription, grouped by service, and
projects an end-of-month total from the current daily run rate.

Auth: uses the az CLI token (must be logged in) and calls the Cost Management
REST API directly, so only `az` + `requests` are required — no azure-mgmt SDKs.

Usage:
    python estimate_azure_costs.py --subscription <sub-id>
    python estimate_azure_costs.py            # uses the active az subscription
    python estimate_azure_costs.py --json
"""

import argparse
import calendar
import datetime as dt
import json
import subprocess
import sys


API_VERSION = "2023-11-01"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Estimate current-month Azure costs.")
    p.add_argument("--subscription", help="Subscription ID (defaults to active az subscription)")
    p.add_argument("--top", type=int, default=8, help="Number of services to show")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    return p.parse_args()


def az(*args: str) -> str:
    return subprocess.check_output(["az", *args], text=True).strip()


def main() -> int:
    args = parse_args()
    try:
        import requests
    except ImportError:
        print("ERROR: requests is required. Install with: pip install requests", file=sys.stderr)
        return 1

    try:
        sub = args.subscription or az("account", "show", "--query", "id", "-o", "tsv")
        token = az("account", "get-access-token", "--query", "accessToken", "-o", "tsv")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: az CLI not available or not logged in. Run 'az login'.", file=sys.stderr)
        return 2

    today = dt.date.today()
    start = today.replace(day=1)
    url = (
        f"https://management.azure.com/subscriptions/{sub}"
        f"/providers/Microsoft.CostManagement/query?api-version={API_VERSION}"
    )
    body = {
        "type": "ActualCost",
        "timeframe": "Custom",
        "timePeriod": {
            "from": start.isoformat() + "T00:00:00Z",
            "to": today.isoformat() + "T23:59:59Z",
        },
        "dataset": {
            "granularity": "None",
            "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
            "grouping": [{"type": "Dimension", "name": "ServiceName"}],
        },
    }
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"ERROR {resp.status_code}: {resp.text}", file=sys.stderr)
        return 3

    payload = resp.json()
    cols = [c["name"] for c in payload["properties"]["columns"]]
    cost_i = cols.index("Cost")
    svc_i = cols.index("ServiceName")
    cur_i = cols.index("Currency") if "Currency" in cols else None

    rows, total, currency = [], 0.0, "USD"
    for r in payload["properties"]["rows"]:
        amount = float(r[cost_i])
        rows.append((str(r[svc_i]), amount))
        total += amount
        if cur_i is not None:
            currency = r[cur_i]
    rows.sort(key=lambda x: x[1], reverse=True)

    days_in_month = calendar.monthrange(today.year, today.month)[1]
    daily_rate = total / today.day if today.day else 0.0
    projected = daily_rate * days_in_month

    if args.json:
        print(json.dumps({
            "subscription": sub,
            "period": {"start": start.isoformat(), "end": today.isoformat()},
            "currency": currency,
            "month_to_date": round(total, 2),
            "daily_run_rate": round(daily_rate, 2),
            "projected_month_total": round(projected, 2),
            "by_service": [{"service": s, "cost": round(a, 2)} for s, a in rows],
        }, indent=2))
        return 0

    print(f"Azure cost {start.isoformat()} -> {today.isoformat()} ({currency})  sub={sub}")
    print("-" * 52)
    for service, amount in rows[: args.top]:
        print(f"  {service[:36]:<36} {amount:>12.2f}")
    if len(rows) > args.top:
        rest = sum(a for _, a in rows[args.top:])
        print(f"  {'(' + str(len(rows) - args.top) + ' more)':<36} {rest:>12.2f}")
    print("-" * 52)
    print(f"  {'Month to date':<36} {total:>12.2f}")
    print(f"  {'Daily run rate':<36} {daily_rate:>12.2f}")
    print(f"  {'Projected month total':<36} {projected:>12.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
