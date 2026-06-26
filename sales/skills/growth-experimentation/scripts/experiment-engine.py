#!/usr/bin/env python3
"""Local growth experiment engine for the go-to-market skill."""

from __future__ import annotations

import argparse
import json
import sys
from statistics import fmean

from growth_engine_lib import (
    DEFAULT_CATEGORIES,
    bootstrap_lift_ci,
    iso_now,
    load_config,
    load_json,
    mann_whitney_p_value,
    save_json,
)


def next_experiment_id(agent: str, experiments: list[dict]) -> str:
    return f"EXP-{agent.upper()}-{len(experiments) + 1:03d}"


def cmd_create(args: argparse.Namespace) -> int:
    config = load_config()
    experiments_path = config.experiments_path(args.agent)
    active_path = config.active_path(args.agent)
    experiments = load_json(experiments_path, [])

    try:
        variants = json.loads(args.variants)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON for --variants: {exc}", file=sys.stderr)
        return 1

    if not isinstance(variants, list) or len(variants) < 2:
        print("--variants must be a JSON array with at least two values", file=sys.stderr)
        return 1

    batch_mode = bool(args.batch_mode)
    if batch_mode and len(variants) > config.batch_mode_max_variants:
        print(
            f"Warning: capping batch-mode variants at {config.batch_mode_max_variants} "
            f"(received {len(variants)})",
            file=sys.stderr,
        )
        variants = variants[: config.batch_mode_max_variants]

    experiment_id = next_experiment_id(args.agent, experiments)
    min_samples = config.get_min_samples(args.agent, args.min_samples if args.min_samples != 3 else None)
    experiment = {
        "id": experiment_id,
        "agent": args.agent,
        "channel": config.channel_for_agent(args.agent),
        "hypothesis": args.hypothesis,
        "variable": args.variable,
        "variants": variants,
        "primary_metric": args.metric,
        "guardrail_metrics": args.guardrails or [],
        "cycle_hours": args.cycle_hours,
        "min_samples": min_samples,
        "batch_mode": batch_mode,
        "created_at": iso_now(),
        "owner": args.owner or "",
        "launch_window": args.launch_window or "",
        "status": "running",
        "baseline_variant": variants[0],
        "data_points": [],
        "result": None,
        "winner": None,
    }
    experiments.append(experiment)
    save_json(experiments_path, experiments)

    active = load_json(active_path, [])
    active.append(
        {
            "id": experiment_id,
            "variable": args.variable,
            "variants": variants,
            "status": "running",
            "created_at": experiment["created_at"],
        }
    )
    save_json(active_path, active)

    mode = f"BATCH ({len(variants)} variants)" if batch_mode else "A/B"
    print(f"Created {experiment_id}")
    print(f"  Agent: {args.agent} ({experiment['channel']})")
    print(f"  Variable: {args.variable} | Mode: {mode}")
    print(f"  Metric: {args.metric} | Min samples/variant: {min_samples}")
    print(f"  Variants: {variants}")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    config = load_config()
    experiments_path = config.experiments_path(args.agent)
    experiments = load_json(experiments_path, [])

    try:
        metrics = json.loads(args.metrics)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON for --metrics: {exc}", file=sys.stderr)
        return 1

    if not isinstance(metrics, dict):
        print("--metrics must be a JSON object", file=sys.stderr)
        return 1

    for experiment in experiments:
        if experiment["id"] != args.experiment_id:
            continue
        if args.variant not in experiment["variants"]:
            print(f"Variant '{args.variant}' is not part of {args.experiment_id}", file=sys.stderr)
            return 1
        data_point = {
            "variant": args.variant,
            "metrics": metrics,
            "logged_at": iso_now(),
            "notes": args.notes or "",
            "source": args.source or "",
        }
        experiment.setdefault("data_points", []).append(data_point)
        save_json(experiments_path, experiments)
        print(f"Logged data point for {args.experiment_id} / {args.variant}: {metrics}")
        return 0

    print(f"Experiment {args.experiment_id} not found", file=sys.stderr)
    return 1


def build_result(experiment: dict, config) -> dict:
    primary_metric = experiment["primary_metric"]
    baseline_variant = experiment["baseline_variant"]
    grouped: dict[str, list[float]] = {variant: [] for variant in experiment["variants"]}
    for data_point in experiment.get("data_points", []):
        value = data_point.get("metrics", {}).get(primary_metric)
        if value is None:
            continue
        grouped.setdefault(data_point["variant"], []).append(float(value))

    baseline_values = grouped.get(baseline_variant, [])
    results: list[dict] = []
    for variant, values in grouped.items():
        if variant == baseline_variant:
            continue
        if not values or not baseline_values:
            results.append(
                {
                    "variant": variant,
                    "mean": round(fmean(values), 2) if values else 0.0,
                    "lift_pct": 0.0,
                    "p_value": 1.0,
                    "ci_95": [None, None],
                    "n": len(values),
                    "status": "running",
                }
            )
            continue

        baseline_mean = fmean(baseline_values)
        variant_mean = fmean(values)
        lift_pct = ((variant_mean - baseline_mean) / baseline_mean * 100) if baseline_mean else 0.0
        p_two_sided = mann_whitney_p_value(baseline_values, values, alternative="two-sided")
        p_less = mann_whitney_p_value(baseline_values, values, alternative="less")
        ci_low, ci_high = bootstrap_lift_ci(
            baseline_values,
            values,
            iterations=config.bootstrap_iterations,
        )

        if p_less < config.p_winner and lift_pct >= config.lift_win:
            status = "keep"
        elif p_less < config.p_trend and len(values) >= min(15, experiment["min_samples"]):
            status = "trending"
        elif p_two_sided < config.p_winner and lift_pct < 0:
            status = "discard"
        else:
            status = "running"

        results.append(
            {
                "variant": variant,
                "mean": round(variant_mean, 2),
                "lift_pct": round(lift_pct, 1),
                "p_value": round(p_less, 4),
                "ci_95": [ci_low, ci_high],
                "n": len(values),
                "status": status,
            }
        )

    return {
        "baseline": baseline_variant,
        "baseline_mean": round(fmean(baseline_values), 2) if baseline_values else 0.0,
        "baseline_n": len(baseline_values),
        "variants": results,
        "scored_at": iso_now(),
        "thresholds": {
            "p_winner": config.p_winner,
            "p_trend": config.p_trend,
            "lift_win": config.lift_win,
        },
    }


def update_playbook(config, experiment: dict, winning_variant: dict) -> None:
    playbook_path = config.playbook_path(experiment["agent"])
    playbook = load_json(playbook_path, {})
    playbook[experiment["variable"]] = {
        "best": winning_variant["variant"],
        "metric": experiment["primary_metric"],
        "avg": winning_variant["mean"],
        "improvement": winning_variant["lift_pct"],
        "p_value": winning_variant["p_value"],
        "ci_95": winning_variant["ci_95"],
        "experiment_id": experiment["id"],
        "promoted_at": iso_now(),
        "channel": experiment["channel"],
        "usage_note": experiment.get("hypothesis", ""),
    }
    save_json(playbook_path, playbook)


def update_active_index(config, agent: str, experiment_id: str, status: str) -> None:
    active_path = config.active_path(agent)
    active = load_json(active_path, [])
    updated = []
    for item in active:
        if item.get("id") == experiment_id:
            if status in {"keep", "discard"}:
                continue
            item["status"] = status
        updated.append(item)
    save_json(active_path, updated)


def cmd_score(args: argparse.Namespace) -> int:
    config = load_config()
    experiments_path = config.experiments_path(args.agent)
    experiments = load_json(experiments_path, [])

    for experiment in experiments:
        if experiment["id"] != args.experiment_id:
            continue

        grouped_counts = {}
        for data_point in experiment.get("data_points", []):
            grouped_counts[data_point["variant"]] = grouped_counts.get(data_point["variant"], 0) + 1

        if not grouped_counts:
            print(f"{args.experiment_id}: no data points yet")
            return 0

        min_samples = experiment["min_samples"]
        insufficient = [f"{variant}={count}/{min_samples}" for variant, count in grouped_counts.items() if count < min_samples]
        result = build_result(experiment, config)

        winners = [item for item in result["variants"] if item["status"] == "keep"]
        trending = [item for item in result["variants"] if item["status"] == "trending"]
        discards = [item for item in result["variants"] if item["status"] == "discard"]

        if winners:
            winner = max(winners, key=lambda item: item["lift_pct"])
            experiment["status"] = "keep"
            experiment["winner"] = winner["variant"]
            experiment["result"] = result
            update_playbook(config, experiment, winner)
            update_active_index(config, args.agent, args.experiment_id, "keep")
            save_json(experiments_path, experiments)
            print(
                f"{args.experiment_id}: KEEP '{winner['variant']}' "
                f"(lift {winner['lift_pct']}%, p={winner['p_value']}, CI={winner['ci_95']})"
            )
            return 0

        if insufficient:
            if trending:
                best_trend = max(trending, key=lambda item: item["lift_pct"])
                experiment["status"] = "trending"
                experiment["result"] = result
                update_active_index(config, args.agent, args.experiment_id, "trending")
                save_json(experiments_path, experiments)
                print(
                    f"{args.experiment_id}: TRENDING '{best_trend['variant']}' "
                    f"(lift {best_trend['lift_pct']}%, p={best_trend['p_value']})"
                )
            else:
                experiment["status"] = "running"
                experiment["result"] = result
                update_active_index(config, args.agent, args.experiment_id, "running")
                save_json(experiments_path, experiments)
                print(f"{args.experiment_id}: needs more data ({', '.join(insufficient)})")
            return 0

        if discards and len(discards) == len(result["variants"]):
            experiment["status"] = "discard"
            experiment["result"] = result
            update_active_index(config, args.agent, args.experiment_id, "discard")
            save_json(experiments_path, experiments)
            print(f"{args.experiment_id}: DISCARD (baseline still wins)")
            return 0

        if trending:
            best_trend = max(trending, key=lambda item: item["lift_pct"])
            experiment["status"] = "trending"
            experiment["result"] = result
            update_active_index(config, args.agent, args.experiment_id, "trending")
            save_json(experiments_path, experiments)
            print(
                f"{args.experiment_id}: TRENDING '{best_trend['variant']}' "
                f"(lift {best_trend['lift_pct']}%, p={best_trend['p_value']})"
            )
            return 0

        experiment["status"] = "running"
        experiment["result"] = result
        update_active_index(config, args.agent, args.experiment_id, "running")
        save_json(experiments_path, experiments)
        for variant in result["variants"]:
            print(
                f"{args.experiment_id}: {variant['variant']} "
                f"{variant['lift_pct']:+.1f}% lift, p={variant['p_value']} -> {variant['status']}"
            )
        return 0

    print(f"Experiment {args.experiment_id} not found", file=sys.stderr)
    return 1


def cmd_list(args: argparse.Namespace) -> int:
    config = load_config()
    experiments = load_json(config.experiments_path(args.agent), [])
    aliases = {"active": "running", "promoted": "keep", "killed": "discard"}
    status_filter = aliases.get(args.status, args.status)

    for experiment in experiments:
        status = aliases.get(experiment["status"], experiment["status"])
        if status_filter != "all" and status != status_filter:
            continue
        data_points = len(experiment.get("data_points", []))
        print(f"{experiment['id']}: {experiment['hypothesis']}")
        print(
            f"  Variable: {experiment['variable']} | Status: {experiment['status']} | "
            f"Data points: {data_points}"
        )
        if experiment.get("winner"):
            print(f"  Winner: {experiment['winner']}")
        print()
    return 0


def cmd_playbook(args: argparse.Namespace) -> int:
    config = load_config()
    playbook = load_json(config.playbook_path(args.agent), {})
    if not playbook:
        print(f"No playbook entries for {args.agent} yet.")
        return 0
    print(f"{args.agent.upper()} PLAYBOOK")
    print()
    for variable, entry in playbook.items():
        print(
            f"{variable}: '{entry['best']}' "
            f"(+{entry['improvement']}% on {entry['metric']}, p={entry['p_value']})"
        )
        print(f"  Source: {entry['experiment_id']} | Promoted: {entry['promoted_at'][:10]}")
        print()
    return 0


def cmd_suggest(args: argparse.Namespace) -> int:
    config = load_config()
    experiments = load_json(config.experiments_path(args.agent), [])
    playbook = load_json(config.playbook_path(args.agent), {})
    tested = set(playbook.keys())
    tested.update(
        experiment["variable"]
        for experiment in experiments
        if experiment.get("status") in {"running", "trending"}
    )
    categories = DEFAULT_CATEGORIES.get(args.agent, [])
    untested = [category for category in categories if category not in tested]
    if not untested:
        print(f"{args.agent}: all standard categories are already covered. Try a packaging or segment test next.")
        return 0
    print(f"Suggested next experiments for {args.agent}:")
    for category in untested[: args.limit]:
        print(f"  - {category}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local growth experiment engine")
    subparsers = parser.add_subparsers(dest="command")

    create = subparsers.add_parser("create", help="Create a new experiment")
    create.add_argument("--agent", required=True)
    create.add_argument("--hypothesis", required=True)
    create.add_argument("--variable", required=True)
    create.add_argument("--variants", required=True, help='JSON array, e.g. ["a","b"]')
    create.add_argument("--metric", required=True)
    create.add_argument("--cycle-hours", type=int, default=24)
    create.add_argument("--min-samples", type=int, default=3)
    create.add_argument("--batch-mode", action="store_true")
    create.add_argument("--owner")
    create.add_argument("--launch-window")
    create.add_argument("--guardrails", nargs="*")

    log = subparsers.add_parser("log", help="Log a data point")
    log.add_argument("--agent", required=True)
    log.add_argument("--experiment-id", required=True)
    log.add_argument("--variant", required=True)
    log.add_argument("--metrics", required=True, help='JSON object, e.g. {"clicks": 42}')
    log.add_argument("--notes")
    log.add_argument("--source")

    score = subparsers.add_parser("score", help="Score an experiment")
    score.add_argument("--agent", required=True)
    score.add_argument("--experiment-id", required=True)

    listing = subparsers.add_parser("list", help="List experiments")
    listing.add_argument("--agent", required=True)
    listing.add_argument("--status", default="all")

    playbook = subparsers.add_parser("playbook", help="Show promoted winners")
    playbook.add_argument("--agent", required=True)

    suggest = subparsers.add_parser("suggest", help="Suggest next experiments")
    suggest.add_argument("--agent", required=True)
    suggest.add_argument("--limit", type=int, default=3)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    handlers = {
        "create": cmd_create,
        "log": cmd_log,
        "score": cmd_score,
        "list": cmd_list,
        "playbook": cmd_playbook,
        "suggest": cmd_suggest,
    }
    if not args.command:
        parser.print_help()
        return 0
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
