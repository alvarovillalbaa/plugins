#!/usr/bin/env python3
"""Generate a weekly markdown scorecard from the local growth engine JSON data."""

from __future__ import annotations

import argparse
from datetime import timedelta
from pathlib import Path

from growth_engine_lib import DEFAULT_CATEGORIES, load_config, load_json, now_utc, parse_iso


def week_window(weeks_back: int) -> tuple:
    now = now_utc()
    this_monday = now - timedelta(days=now.weekday())
    start = (this_monday - timedelta(weeks=max(weeks_back - 1, 0))).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start + timedelta(days=7)
    return start, end


def in_window(value: str | None, start, end) -> bool:
    parsed = parse_iso(value)
    return bool(parsed and start <= parsed < end)


def load_all(config):
    experiments_by_agent: dict[str, list[dict]] = {}
    playbook_by_agent: dict[str, dict] = {}
    for agent in config.agents:
        experiments_by_agent[agent] = load_json(config.experiments_path(agent), [])
        playbook_by_agent[agent] = load_json(config.playbook_path(agent), {})
    return experiments_by_agent, playbook_by_agent


def top_playbook_rules(playbook_by_agent: dict[str, dict]) -> list[tuple[str, str, dict]]:
    rules = []
    for agent, entries in playbook_by_agent.items():
        for variable, entry in entries.items():
            rules.append((agent, variable, entry))
    rules.sort(key=lambda item: item[2].get("improvement", 0), reverse=True)
    return rules


def next_queue(agent: str, experiments: list[dict], playbook: dict) -> list[str]:
    tested = set(playbook.keys())
    tested.update(
        experiment.get("variable")
        for experiment in experiments
        if experiment.get("status") in {"running", "trending"}
    )
    defaults = DEFAULT_CATEGORIES.get(agent, [])
    return [category for category in defaults if category not in tested][:3]


def generate_scorecard(weeks_back: int) -> str:
    config = load_config()
    experiments_by_agent, playbook_by_agent = load_all(config)
    start, end = week_window(weeks_back)
    label = f"{start.strftime('%b %d')} - {(end - timedelta(days=1)).strftime('%b %d, %Y')}"

    new_experiments = []
    active_experiments = []
    completed_experiments = []
    winners = []
    trending = []
    discards = []
    data_points_count = 0

    for agent, experiments in experiments_by_agent.items():
        for experiment in experiments:
            if in_window(experiment.get("created_at"), start, end):
                new_experiments.append((agent, experiment))
            if experiment.get("status") in {"running", "trending"}:
                active_experiments.append((agent, experiment))
            result = experiment.get("result") or {}
            if in_window(result.get("scored_at"), start, end) and experiment.get("status") in {"keep", "discard", "trending"}:
                completed_experiments.append((agent, experiment))
            if experiment.get("status") == "keep":
                winners.append((agent, experiment))
            elif experiment.get("status") == "trending":
                trending.append((agent, experiment))
            elif experiment.get("status") == "discard":
                discards.append((agent, experiment))

            for point in experiment.get("data_points", []):
                if in_window(point.get("logged_at"), start, end):
                    data_points_count += 1

    lines = [
        f"# AutoGrowth Weekly Scorecard - Week of {label}",
        "",
        "## Summary",
        f"- Total experiments active: {len(active_experiments)}",
        f"- New experiments launched: {len(new_experiments)}",
        f"- Experiments completed: {len(completed_experiments)}",
        f"- Winners promoted: {sum(1 for _, experiment in completed_experiments if experiment.get('status') == 'keep')}",
        f"- Discards confirmed: {sum(1 for _, experiment in completed_experiments if experiment.get('status') == 'discard')}",
        f"- Data points logged this week: {data_points_count}",
        "",
        "## Big Wins",
    ]

    if not winners:
        lines.append("No promoted winners yet.")
    else:
        for agent, experiment in winners[:5]:
            result = experiment.get("result") or {}
            winner_variant = experiment.get("winner")
            winning_row = next(
                (row for row in result.get("variants", []) if row.get("variant") == winner_variant),
                {},
            )
            lines.append(
                f"- `{experiment['id']}` ({agent}) -> `{experiment['variable']}` winner `{winner_variant}` "
                f"at {winning_row.get('lift_pct', 0)}% lift"
            )

    lines.extend(["", "## Trending"])
    if not trending:
        lines.append("No trending experiments right now.")
    else:
        for agent, experiment in trending[:5]:
            result = experiment.get("result") or {}
            best = max(result.get("variants", []) or [{}], key=lambda row: row.get("lift_pct", 0))
            lines.append(
                f"- `{experiment['id']}` ({agent}) -> `{best.get('variant', '?')}` "
                f"{best.get('lift_pct', 0)}% lift, p={best.get('p_value', 1)}"
            )

    lines.extend(["", "## Running"])
    if not active_experiments:
        lines.append("No active experiments.")
    else:
        for agent, experiment in active_experiments[:8]:
            counts = {}
            for point in experiment.get("data_points", []):
                counts[point["variant"]] = counts.get(point["variant"], 0) + 1
            count_str = ", ".join(f"{variant}={count}" for variant, count in counts.items()) or "no samples"
            lines.append(
                f"- `{experiment['id']}` ({agent}) testing `{experiment['variable']}` "
                f"[{count_str}]"
            )

    lines.extend(["", "## Discarded"])
    if not discards:
        lines.append("No discards yet.")
    else:
        for agent, experiment in discards[:5]:
            lines.append(
                f"- `{experiment['id']}` ({agent}) -> `{experiment['variable']}` did not beat baseline"
            )

    lines.extend(["", "## Cumulative Playbook"])
    all_rules = top_playbook_rules(playbook_by_agent)
    lines.append(f"- Total rules in playbook: {len(all_rules)}")
    if all_rules:
        lines.append("")
        lines.append("Top 3 lifts ever promoted:")
        for idx, (agent, variable, entry) in enumerate(all_rules[:3], start=1):
            lines.append(
                f"{idx}. ({agent}) `{variable}` -> `{entry['best']}` at {entry['improvement']}% lift"
            )

    lines.extend(["", "## Next Queue"])
    queue_lines = []
    for agent in config.agents:
        queue = next_queue(agent, experiments_by_agent.get(agent, []), playbook_by_agent.get(agent, {}))
        if queue:
            queue_lines.append(f"- {agent}: {', '.join(queue)}")
    if queue_lines:
        lines.extend(queue_lines)
    else:
        lines.append("No default queue gaps detected. Consider new segment, offer, or packaging tests.")

    lines.extend(["", "---", f"*Generated {now_utc().strftime('%Y-%m-%d %H:%M UTC')}*"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a weekly growth scorecard")
    parser.add_argument("--weeks", type=int, default=1, help="1 = current week, 2 = previous week, etc.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    output = generate_scorecard(args.weeks)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
        print(f"Wrote scorecard to {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
