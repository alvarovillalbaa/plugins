#!/usr/bin/env python3
"""Check pacing for the local growth engine, with optional external API checks."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import timedelta

from growth_engine_lib import load_config, load_json, now_utc, parse_iso


def api_get(url: str, token: str) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = token if token.startswith("Bearer ") else f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return {"error": f"HTTP {exc.code}"}
    except Exception as exc:  # pragma: no cover - defensive
        return {"error": str(exc)}


def pace_status(score: int) -> str:
    if score <= 0:
        return "on pace"
    if score == 1:
        return "watch"
    return "alert"


def local_summary(config) -> dict:
    start = (now_utc() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    active = 0
    overdue = []
    logged_this_week = 0
    tracked_agents = 0

    for agent in config.agents:
        experiments = load_json(config.experiments_path(agent), [])
        if experiments:
            tracked_agents += 1
        for experiment in experiments:
            if experiment.get("status") in {"running", "trending"}:
                active += 1
                created_at = parse_iso(experiment.get("created_at"))
                cycle_hours = experiment.get("cycle_hours") or 24
                if created_at and now_utc() - created_at > timedelta(hours=cycle_hours * 2):
                    overdue.append(
                        {
                            "agent": agent,
                            "experiment_id": experiment["id"],
                            "variable": experiment["variable"],
                            "age_hours": round((now_utc() - created_at).total_seconds() / 3600, 1),
                        }
                    )
            for point in experiment.get("data_points", []):
                logged_at = parse_iso(point.get("logged_at"))
                if logged_at and logged_at >= start:
                    logged_this_week += 1

    issues = 0
    if active == 0:
        issues += 2
    elif active < max(1, tracked_agents // 2):
        issues += 1
    if logged_this_week == 0:
        issues += 2
    elif logged_this_week < tracked_agents:
        issues += 1
    if overdue:
        issues += 1

    return {
        "status": pace_status(issues),
        "active_experiments": active,
        "data_points_last_7d": logged_this_week,
        "overdue_experiments": overdue,
        "tracked_agents": tracked_agents,
    }


def external_summary(config) -> dict:
    sections = {}

    if config.pipeline_api_url:
        sections["pipeline"] = api_get(config.pipeline_api_url, config.pipeline_auth_token)
    if config.recruiting_api_url:
        sections["recruiting"] = api_get(config.recruiting_api_url, config.recruiting_auth_token)
    if config.email_api_url and config.outbound_campaigns:
        campaign_results = {}
        for name, campaign_id in config.outbound_campaigns.items():
            campaign_results[name] = api_get(
                f"{config.email_api_url.rstrip('/')}/{campaign_id}",
                config.email_auth_token,
            )
        sections["outbound_campaigns"] = campaign_results
    if config.email_api_url and config.recruiting_campaigns:
        campaign_results = {}
        for name, campaign_id in config.recruiting_campaigns.items():
            campaign_results[name] = api_get(
                f"{config.email_api_url.rstrip('/')}/{campaign_id}",
                config.email_auth_token,
            )
        sections["recruiting_campaigns"] = campaign_results

    return sections


def render_text(local: dict, external: dict) -> str:
    lines = [
        f"Pacing Alert - {now_utc().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "Local growth engine",
        f"- status: {local['status']}",
        f"- active experiments: {local['active_experiments']}",
        f"- data points last 7d: {local['data_points_last_7d']}",
        f"- tracked agents: {local['tracked_agents']}",
    ]
    if local["overdue_experiments"]:
        lines.append("- overdue experiments:")
        for item in local["overdue_experiments"][:5]:
            lines.append(
                f"  - {item['experiment_id']} ({item['agent']}) "
                f"{item['variable']} age={item['age_hours']}h"
            )
    else:
        lines.append("- overdue experiments: none")

    if external:
        lines.extend(["", "External checks"])
        for name, payload in external.items():
            has_error = False
            if isinstance(payload, dict) and payload.get("error"):
                has_error = True
            elif isinstance(payload, dict):
                has_error = any(
                    isinstance(item, dict) and item.get("error")
                    for item in payload.values()
                )
            status = "alert" if has_error else "configured"
            lines.append(f"- {name}: {status}")
    else:
        lines.extend(["", "External checks", "- none configured"])

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check experiment pacing")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()

    config = load_config()
    local = local_summary(config)
    external = external_summary(config)
    payload = {
        "timestamp": now_utc().isoformat(),
        "local": local,
        "external": external,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(render_text(local, external))

    external_error = any(
        isinstance(section, dict)
        and (
            section.get("error")
            or any(isinstance(item, dict) and item.get("error") for item in section.values())
        )
        for section in external.values()
    )
    return 1 if local["status"] == "alert" or external_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
