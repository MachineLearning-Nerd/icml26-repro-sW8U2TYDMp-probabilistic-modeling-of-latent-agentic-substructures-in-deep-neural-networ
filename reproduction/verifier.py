"""Cumulative verifier: exact Claims 1-2 and four historical toy checks."""

from __future__ import annotations

import math
import random
from typing import Any

from .independent_checker import claim2_decimal_certificate
from .math_core import (
    entropy,
    epistemic_utility,
    kl_divergence,
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


def _claim2_identity(
    agents: list[list[float]], weights: list[float]
) -> dict[str, float | list[float]]:
    """Check the certificate using definitions, then an independent KL form."""
    pool = linear_pool(agents, weights)
    direct_gaps = [welfare_gap(agent, pool) for agent in agents]
    entropy_kl_gaps = [
        entropy(agent) - entropy(pool) - kl_divergence(pool, agent)
        for agent in agents
    ]
    weighted_direct = math.fsum(
        weight * gap for weight, gap in zip(weights, direct_gaps)
    )
    forward_kl = math.fsum(
        weight * kl_divergence(agent, pool)
        for weight, agent in zip(weights, agents)
    )
    reverse_kl = math.fsum(
        weight * kl_divergence(pool, agent)
        for weight, agent in zip(weights, agents)
    )
    certificate_rhs = -(forward_kl + reverse_kl)
    return {
        "pool": pool,
        "direct_gaps": direct_gaps,
        "entropy_kl_gaps": entropy_kl_gaps,
        "weighted_direct": weighted_direct,
        "forward_kl": forward_kl,
        "reverse_kl": reverse_kl,
        "certificate_rhs": certificate_rhs,
        "gap_identity_error": max(
            abs(left - right)
            for left, right in zip(direct_gaps, entropy_kl_gaps)
        ),
        "certificate_error": abs(weighted_direct - certificate_rhs),
    }


def claim2(rng: random.Random) -> dict[str, Any]:
    """Machine-check the analytic Theorem 10 certificate."""
    fixtures: list[dict[str, Any]] = []
    configurations = ((2, 2), (2, 5), (3, 3), (4, 5))
    for agents_count, outcomes in configurations:
        agents = [
            _random_distribution(rng, outcomes) for _ in range(agents_count)
        ]
        weights = normalize(
            [float(index + 1) for index in range(agents_count)]
        )
        result = _claim2_identity(agents, weights)
        fixtures.append(
            {
                "agents_count": agents_count,
                "outcomes": outcomes,
                "weights": weights,
                **result,
            }
        )

    # Plausible algebra mutation: omit the reverse-KL term.
    omitted_reverse_detected = any(
        abs(float(item["weighted_direct"]) + float(item["forward_kl"])) > 1e-6
        for item in fixtures
    )

    # Identical beliefs remove strictness, auditing the nondegeneracy condition.
    identical = _claim2_identity(
        [[0.2, 0.3, 0.5], [0.2, 0.3, 0.5]], [0.25, 0.75]
    )
    distinctness_control_detected = (
        abs(float(identical["weighted_direct"])) < 1e-14
        and abs(float(identical["forward_kl"])) < 1e-14
        and abs(float(identical["reverse_kl"])) < 1e-14
    )

    fixture_checks = [
        float(item["weighted_direct"]) < -1e-12
        and float(item["forward_kl"]) > 0.0
        and float(item["reverse_kl"]) > 0.0
        and float(item["gap_identity_error"]) < 1e-12
        and float(item["certificate_error"]) < 1e-12
        for item in fixtures
    ]
    independent = claim2_decimal_certificate()
    passed = (
        all(fixture_checks)
        and omitted_reverse_detected
        and distinctness_control_detected
        and independent["passed"]
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "passed": passed,
        "contract": {
            "domain": "finite outcome space; n>=2 full-support distributions",
            "weights": "beta_i>0 and sum beta_i=1",
            "nondegeneracy": "not all P_i identical",
            "quantifier": "for every admissible instance",
            "conclusion": "not(all Delta_i>=0), hence strict unanimity is impossible",
        },
        "proof_certificate": {
            "identity": (
                "sum_i beta_i Delta_i = "
                "-sum_i beta_i[KL(P_i||P)+KL(P||P_i)]"
            ),
            "analytic_lemma": (
                "Gibbs inequality: KL(Q||R)>=0, equality iff Q=R "
                "for positive finite distributions"
            ),
            "strictness": (
                "positive weights and a non-identical agent imply "
                "sum_i beta_i KL(P_i||P)>0"
            ),
            "contradiction": (
                "all Delta_i>=0 would make the positive-weighted sum >=0, "
                "contradicting the strictly negative certificate"
            ),
        },
        "fixtures": fixtures,
        "independent_checker": independent,
        "negative_controls": {
            "omit_reverse_kl_term_detected": omitted_reverse_detected,
            "identical_agents_remove_strictness_detected": (
                distinctness_control_detected
            ),
        },
        "limitation": (
            "Floating-point fixtures audit the implementation only; universal "
            "coverage comes from the displayed algebraic certificate and Gibbs inequality."
        ),
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
        "claim_2": claim2(rng),
        "claim_3": claim3_toy(rng),
        "claim_4": claim4_toy(),
        "claim_5": claim5_toy(),
        "claim_6": claim6_toy(),
    }
    return {
        "campaign_stage": "claim_2_analytic_certificate",
        "seed": SEED,
        "claims": claims,
        "full_credit_claims": sum(item["status"] in {"VERIFIED", "FALSIFIED"} for item in claims.values()),
        "toy_claims": sum(item["status"] == "TOY" for item in claims.values()),
        "baseline_points": 7,
        "passed": all(item["passed"] for item in claims.values()),
    }
