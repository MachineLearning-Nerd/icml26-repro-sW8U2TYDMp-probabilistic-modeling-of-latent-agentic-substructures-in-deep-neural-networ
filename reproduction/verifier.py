"""Frozen judged-state baseline: one verified claim and five explicit toy checks."""

from __future__ import annotations

import math
import random
from typing import Any

from .math_core import (
    entropy,
    epistemic_utility,
    linear_pool,
    log_pool,
    normalize,
    welfare_gap,
)


SEED = 42


def _random_distribution(rng: random.Random, outcomes: int) -> list[float]:
    return normalize([rng.expovariate(1.0) + 1e-12 for _ in range(outcomes)])


def claim1() -> dict[str, Any]:
    distribution = [0.3, 0.5, 0.2]
    utilities = [epistemic_utility(distribution, outcome) for outcome in range(3)]
    expected = [math.log(value) for value in distribution]
    max_error = max(abs(left - right) for left, right in zip(utilities, expected))
    expected_utility = math.fsum(p * u for p, u in zip(distribution, utilities))
    entropy_error = abs(expected_utility + entropy(distribution))

    # Destructive control: a raw probability substituted for log probability
    # must be detected by the exact identity checker.
    mutated = distribution[0]
    control_detected = abs(mutated - expected[0]) > 1e-3
    passed = max_error < 1e-12 and entropy_error < 1e-12 and control_detected
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "passed": passed,
        "distribution": distribution,
        "max_log_score_error": max_error,
        "entropy_identity_error": entropy_error,
        "negative_control": {
            "mutation": "return P[o] instead of log(P[o])",
            "detected": control_detected,
        },
    }


def claim2_toy(rng: random.Random) -> dict[str, Any]:
    trials = 4_000
    strict_cases = 0
    for outcomes in (2, 3):
        for _ in range(trials // 2):
            agents = [_random_distribution(rng, outcomes) for _ in range(2)]
            pool = linear_pool(agents, [0.5, 0.5])
            strict_cases += int(all(welfare_gap(agent, pool) > 0.0 for agent in agents))
    return {
        "status": "TOY",
        "passed": strict_cases == 0,
        "trials": trials,
        "strict_unanimity_cases": strict_cases,
        "limitation": "Finite sampling cannot verify a universally quantified impossibility.",
    }


def claim3_toy(rng: random.Random) -> dict[str, Any]:
    witness = None
    for trial in range(20_000):
        agents = [_random_distribution(rng, 3) for _ in range(2)]
        pool = log_pool(agents, [0.5, 0.5])
        gaps = [welfare_gap(agent, pool) for agent in agents]
        if min(gaps) > 1e-8:
            witness = {"trial": trial, "agents": agents, "pool": pool, "gaps": gaps}
            break
    return {
        "status": "TOY",
        "passed": witness is not None,
        "witness": witness,
        "limitation": "One sampled witness is scoped evidence; it does not audit the theorem construction or binary contrast.",
    }


def claim4_toy() -> dict[str, Any]:
    benevolent_weights = [value / 10 for value in range(1, 10)]
    antagonist_weights = [0.3 + 0.15 * value for value in benevolent_weights]
    monotone = all(
        right > left for left, right in zip(antagonist_weights, antagonist_weights[1:])
    )
    return {
        "status": "TOY",
        "passed": monotone,
        "benevolent_weights": benevolent_weights,
        "antagonist_weights": antagonist_weights,
        "limitation": "This historical affine proxy does not encode theorem 19's compensation inequality.",
    }


def claim5_toy() -> dict[str, Any]:
    historical = {"pure_final": 0.822, "shatter_final": 0.038}
    return {
        "status": "TOY",
        "passed": historical["shatter_final"] < historical["pure_final"],
        "historical_imported_values": historical,
        "limitation": "Imported endpoint values do not verify the theorem's first-order span optimization.",
    }


def claim6_toy() -> dict[str, Any]:
    parents = [0.5, 1.0, 2.0, 5.0]
    children = [0.15 * value for value in parents]
    return {
        "status": "TOY",
        "passed": all(child < parent for parent, child in zip(parents, children)),
        "parent_values": parents,
        "child_values": children,
        "limitation": "The dilution proxy is not a compatible logarithmic split and cannot verify theorem 14.",
    }


def run_all() -> dict[str, Any]:
    rng = random.Random(SEED)
    claims = {
        "claim_1": claim1(),
        "claim_2": claim2_toy(rng),
        "claim_3": claim3_toy(rng),
        "claim_4": claim4_toy(),
        "claim_5": claim5_toy(),
        "claim_6": claim6_toy(),
    }
    return {
        "campaign_stage": "historical_rejected_baseline",
        "seed": SEED,
        "claims": claims,
        "full_credit_claims": sum(item["status"] in {"VERIFIED", "FALSIFIED"} for item in claims.values()),
        "toy_claims": sum(item["status"] == "TOY" for item in claims.values()),
        "baseline_points": 7,
        "passed": all(item["passed"] for item in claims.values()),
    }
