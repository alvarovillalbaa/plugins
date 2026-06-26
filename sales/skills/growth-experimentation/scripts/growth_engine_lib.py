#!/usr/bin/env python3
"""Shared helpers for the go-to-market growth engine scripts."""

from __future__ import annotations

import json
import math
import os
import random
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import NormalDist, fmean
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_DATA_DIR = SKILL_DIR / "data" / "experiments"
UTC = timezone.utc


def now_utc() -> datetime:
    return datetime.now(UTC)


def iso_now() -> str:
    return now_utc().isoformat()


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def coerce_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_csv(value: str | None, default: str) -> list[str]:
    raw = value if value is not None else default
    return [item.strip() for item in raw.split(",") if item.strip()]


def parse_json_env(name: str, default: dict[str, Any] | None = None) -> dict[str, Any]:
    raw = os.environ.get(name)
    if not raw:
        return dict(default or {})
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return dict(default or {})
    return parsed if isinstance(parsed, dict) else dict(default or {})


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True))


def average_ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    current = 0
    while current < len(indexed):
        start = current
        target = indexed[current][1]
        while current < len(indexed) and indexed[current][1] == target:
            current += 1
        avg_rank = (start + 1 + current) / 2
        for idx in range(start, current):
            original_index = indexed[idx][0]
            ranks[original_index] = avg_rank
    return ranks


def mann_whitney_p_value(sample_a: list[float], sample_b: list[float], alternative: str = "two-sided") -> float:
    """Approximate Mann-Whitney U p-value with tie correction using the normal approximation."""
    if not sample_a or not sample_b:
        return 1.0

    combined = sample_a + sample_b
    ranks = average_ranks(combined)
    n1 = len(sample_a)
    n2 = len(sample_b)
    rank_sum_a = sum(ranks[:n1])
    u1 = rank_sum_a - n1 * (n1 + 1) / 2
    mean_u = n1 * n2 / 2

    counts = Counter(combined)
    total = n1 + n2
    tie_term = sum(count**3 - count for count in counts.values())
    denom = total**3 - total
    tie_correction = 1.0 - (tie_term / denom) if denom else 1.0
    variance = n1 * n2 * (total + 1) * tie_correction / 12
    if variance <= 0:
        return 1.0

    stddev = math.sqrt(variance)
    continuity = 0.5 if u1 != mean_u else 0.0
    if alternative == "less":
        z_score = (u1 - mean_u + continuity) / stddev
        return NormalDist().cdf(z_score)
    if alternative == "greater":
        z_score = (u1 - mean_u - continuity) / stddev
        return 1 - NormalDist().cdf(z_score)

    z_score = (u1 - mean_u - math.copysign(continuity, u1 - mean_u)) / stddev
    tail = NormalDist().cdf(z_score)
    return max(0.0, min(1.0, 2 * min(tail, 1 - tail)))


def bootstrap_lift_ci(
    baseline_values: list[float],
    variant_values: list[float],
    iterations: int,
    confidence: int = 95,
) -> tuple[float | None, float | None]:
    if not baseline_values or not variant_values:
        return None, None

    rng = random.Random(42)
    lifts: list[float] = []
    for _ in range(max(iterations, 1)):
        sample_a = [rng.choice(baseline_values) for _ in range(len(baseline_values))]
        sample_b = [rng.choice(variant_values) for _ in range(len(variant_values))]
        baseline_mean = fmean(sample_a)
        if baseline_mean == 0:
            continue
        variant_mean = fmean(sample_b)
        lifts.append((variant_mean - baseline_mean) / baseline_mean * 100)

    if not lifts:
        return None, None

    lifts.sort()
    lower_idx = int((100 - confidence) / 2 / 100 * (len(lifts) - 1))
    upper_idx = int((1 - (100 - confidence) / 2 / 100) * (len(lifts) - 1))
    return round(lifts[lower_idx], 1), round(lifts[upper_idx], 1)


@dataclass(frozen=True)
class GrowthEngineConfig:
    data_dir: Path
    agents: list[str]
    high_volume_agents: set[str]
    low_volume_agents: set[str]
    batch_mode_max_variants: int
    bootstrap_iterations: int
    p_winner: float
    p_trend: float
    lift_win: float
    daily_lead_target: int
    weekly_candidate_target: int
    pipeline_api_url: str
    pipeline_auth_token: str
    recruiting_api_url: str
    recruiting_auth_token: str
    email_api_url: str
    email_auth_token: str
    outbound_campaigns: dict[str, str]
    recruiting_campaigns: dict[str, str]
    timezone_offset: int
    timezone_label: str

    @property
    def local_timezone(self) -> timezone:
        return timezone(timedelta(hours=self.timezone_offset))

    def agent_dir(self, agent: str) -> Path:
        path = self.data_dir / agent
        path.mkdir(parents=True, exist_ok=True)
        return path

    def experiments_path(self, agent: str) -> Path:
        return self.agent_dir(agent) / "experiments.json"

    def active_path(self, agent: str) -> Path:
        return self.agent_dir(agent) / "active.json"

    def playbook_path(self, agent: str) -> Path:
        return self.agent_dir(agent) / "playbook.json"

    def get_min_samples(self, agent: str, override: int | None = None) -> int:
        if override is not None and override > 3:
            return override
        if agent in self.high_volume_agents:
            return 10
        return 30

    def channel_for_agent(self, agent: str) -> str:
        mapping = {
            "content": "social",
            "email": "email",
            "linkedin": "linkedin",
            "seo": "seo",
            "blog": "blog",
            "paid": "paid",
            "outbound": "outbound",
        }
        return mapping.get(agent, agent)


def load_config() -> GrowthEngineConfig:
    data_dir = Path(os.environ.get("GROWTH_ENGINE_DATA_DIR", str(DEFAULT_DATA_DIR))).expanduser()
    data_dir.mkdir(parents=True, exist_ok=True)
    return GrowthEngineConfig(
        data_dir=data_dir,
        agents=parse_csv(os.environ.get("GROWTH_ENGINE_AGENTS"), "content,email,linkedin,seo,blog"),
        high_volume_agents=set(parse_csv(os.environ.get("HIGH_VOLUME_AGENTS"), "content,email")),
        low_volume_agents=set(parse_csv(os.environ.get("LOW_VOLUME_AGENTS"), "seo,linkedin,blog")),
        batch_mode_max_variants=coerce_int(os.environ.get("BATCH_MODE_MAX_VARIANTS"), 10),
        bootstrap_iterations=coerce_int(os.environ.get("BOOTSTRAP_ITERATIONS"), 1000),
        p_winner=coerce_float(os.environ.get("P_WINNER"), 0.05),
        p_trend=coerce_float(os.environ.get("P_TREND"), 0.10),
        lift_win=coerce_float(os.environ.get("LIFT_WIN"), 15.0),
        daily_lead_target=coerce_int(os.environ.get("DAILY_LEAD_TARGET"), 10),
        weekly_candidate_target=coerce_int(os.environ.get("WEEKLY_CANDIDATE_TARGET"), 400),
        pipeline_api_url=os.environ.get("PIPELINE_API_URL", "").strip(),
        pipeline_auth_token=os.environ.get("PIPELINE_AUTH_TOKEN", "").strip(),
        recruiting_api_url=os.environ.get("RECRUITING_API_URL", "").strip(),
        recruiting_auth_token=os.environ.get("RECRUITING_AUTH_TOKEN", "").strip(),
        email_api_url=os.environ.get("EMAIL_API_URL", "").strip(),
        email_auth_token=os.environ.get("EMAIL_AUTH_TOKEN", "").strip(),
        outbound_campaigns=parse_json_env("OUTBOUND_CAMPAIGNS"),
        recruiting_campaigns=parse_json_env("RECRUITING_CAMPAIGNS"),
        timezone_offset=coerce_int(os.environ.get("TZ_OFFSET"), 0),
        timezone_label=os.environ.get("TZ_LABEL", "UTC").strip() or "UTC",
    )


DEFAULT_CATEGORIES = {
    "content": [
        "hook_style",
        "post_format",
        "cta_type",
        "post_time",
        "thread_length",
        "emoji_usage",
        "data_vs_narrative",
        "question_vs_statement",
    ],
    "email": [
        "subject_line_style",
        "opener_type",
        "email_length",
        "personalization_depth",
        "cta_style",
        "send_time",
        "follow_up_timing",
        "social_proof_type",
    ],
    "linkedin": [
        "inmail_opener",
        "role_framing",
        "company_pitch",
        "personalization_level",
        "subject_line",
        "follow_up_cadence",
    ],
    "blog": [
        "headline_style",
        "content_format",
        "platform_priority",
        "visual_style",
        "posting_time",
        "content_length",
    ],
    "seo": [
        "title_tag_format",
        "meta_description_style",
        "content_structure",
        "internal_linking",
        "heading_format",
    ],
    "paid": [
        "offer_angle",
        "creative_style",
        "audience_segment",
        "landing_page_variant",
        "cta_style",
    ],
    "outbound": [
        "targeting_rule",
        "email_opening",
        "social_proof_type",
        "sequence_length",
        "cta_style",
    ],
}
