#!/usr/bin/env python3
from __future__ import annotations

import argparse
import configparser
import re
import subprocess
import sys
from pathlib import Path


class ExperimentError(Exception):
    pass


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), check=check, text=True, capture_output=True)


def read_config(path: Path) -> dict[str, str]:
    text = "[experiment]\n" + path.read_text(encoding="utf-8")
    parser = configparser.ConfigParser()
    parser.read_string(text)
    data = {key: value.strip() for key, value in parser["experiment"].items()}
    for required in ("target", "evaluate_cmd", "metric", "metric_direction"):
        if required not in data or not data[required]:
            raise ExperimentError(f"missing config value: {required}")
    if data["metric_direction"] not in {"lower", "higher"}:
        raise ExperimentError("metric_direction must be lower or higher")
    return data


def current_branch(root: Path) -> str:
    result = run(["git", "branch", "--show-current"], root)
    return result.stdout.strip()


def ensure_safe_branch(root: Path, experiment: str) -> None:
    branch = current_branch(root)
    expected = f"autoresearch/{experiment}"
    if branch != expected:
        raise ExperimentError(f"refusing to run on branch `{branch}`; expected `{expected}`")


def parse_metric(output: str, metric: str) -> float:
    match = re.search(rf"(^|\s){re.escape(metric)}\s*[:=]\s*(-?\d+(?:\.\d+)?)", output)
    if not match:
        raise ExperimentError(f"metric `{metric}` not found in evaluator output")
    return float(match.group(2))


def best_metric(results: Path, direction: str) -> float | None:
    if not results.exists():
        return None
    best: float | None = None
    for line in results.read_text(encoding="utf-8").splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) < 3 or parts[2] != "keep":
            continue
        try:
            metric = float(parts[1])
        except ValueError:
            continue
        if best is None:
            best = metric
        elif direction == "lower" and metric < best:
            best = metric
        elif direction == "higher" and metric > best:
            best = metric
    return best


def is_improvement(value: float, best: float | None, direction: str) -> bool:
    if best is None:
        return True
    return value < best if direction == "lower" else value > best


def append_result(results: Path, commit: str, metric: str, status: str, description: str) -> None:
    if not results.exists():
        results.write_text("commit\tmetric\tstatus\tdescription\n", encoding="utf-8")
    with results.open("a", encoding="utf-8") as handle:
        handle.write(f"{commit}\t{metric}\t{status}\t{description}\n")


def run_single(root: Path, experiment: str, description: str) -> int:
    exp_dir = root / ".autoresearch" / experiment
    config_path = exp_dir / "config.cfg"
    results = exp_dir / "results.tsv"
    if not config_path.exists():
        raise ExperimentError(f"experiment config not found: {config_path}")
    ensure_safe_branch(root, experiment)
    config = read_config(config_path)
    target = root / config["target"]
    if not target.exists():
        raise ExperimentError(f"target not found: {target}")

    diff = run(["git", "diff", "--name-only", "HEAD"], root).stdout.splitlines()
    if config["target"] not in diff:
        raise ExperimentError(f"target `{config['target']}` has no working-tree changes to evaluate")
    unsafe = [path for path in diff if path != config["target"]]
    if unsafe:
        raise ExperimentError(f"refusing to evaluate unrelated changed files: {', '.join(unsafe)}")

    run(["git", "add", config["target"]], root)
    run(["git", "commit", "-m", f"experiment: {description}"], root)
    commit = run(["git", "rev-parse", "--short", "HEAD"], root).stdout.strip()

    evaluator = subprocess.run(config["evaluate_cmd"], cwd=str(root), shell=True, text=True, capture_output=True)
    output = evaluator.stdout + "\n" + evaluator.stderr
    if evaluator.returncode != 0:
        run(["git", "reset", "--hard", "HEAD~1"], root)
        append_result(results, commit, "nan", "crash", description)
        print(output.strip())
        return 2

    value = parse_metric(output, config["metric"])
    best = best_metric(results, config["metric_direction"])
    if is_improvement(value, best, config["metric_direction"]):
        append_result(results, commit, str(value), "keep", description)
        print(f"KEEP {config['metric']}={value}")
        return 0

    run(["git", "reset", "--hard", "HEAD~1"], root)
    append_result(results, commit, str(value), "discard", description)
    print(f"DISCARD {config['metric']}={value}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one safe autoresearch experiment evaluation.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--single", action="store_true", help="Run one evaluation and keep/discard the last target change")
    parser.add_argument("--description", default="single change")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if not args.single:
            raise ExperimentError("only --single is currently supported")
        return run_single(Path(args.root).resolve(), args.experiment.strip("/"), args.description)
    except (ExperimentError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
