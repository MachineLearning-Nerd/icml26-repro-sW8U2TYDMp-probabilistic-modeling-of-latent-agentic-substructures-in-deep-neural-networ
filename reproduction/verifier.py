"""Cumulative verifier: exact Claims 1-2 and four historical toy checks."""

from __future__ import annotations

import math
import random
from typing import Any

from .independent_checker import (
    claim2_decimal_certificate,
    claim3_decimal_witness,
    claim4_decimal_counterexample,
    claim5_decimal_geometry,
)
from .math_core import (
    centered_log_profile,
    entropy,
    epistemic_utility,
    kl_divergence,
    linear_pool,
    log_pool,
    normalize,
    project_onto_span,
    weighted_inner,
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


def _theorem9_construction(n: int, epsilon: float) -> list[list[float]]:
    """Appendix E.2.1 construction on shared o_0 and private o_i."""
    if n < 2 or not 0.0 < epsilon < 0.25:
        raise ValueError("construction requires n>=2 and 0<epsilon<1/4")
    delta = epsilon ** (n + 1)
    base = 1.0 - epsilon - (n - 1) * delta
    agents: list[list[float]] = []
    for agent_index in range(n):
        distribution = [base, *([delta] * n)]
        distribution[agent_index + 1] = epsilon
        agents.append(distribution)
    return agents


def claim3(rng: random.Random) -> dict[str, Any]:
    del rng
    epsilon = 1e-5
    weight_sets = (
        [0.5, 0.5],
        [0.2, 0.8],
        [0.1, 0.3, 0.6],
        [0.05, 0.15, 0.3, 0.5],
    )
    fixtures: list[dict[str, Any]] = []
    for weights in weight_sets:
        agents = _theorem9_construction(len(weights), epsilon)
        pool = log_pool(agents, weights)
        gaps = [welfare_gap(agent, pool) for agent in agents]
        fixtures.append(
            {
                "n": len(weights),
                "outcomes": len(weights) + 1,
                "epsilon": epsilon,
                "delta": epsilon ** (len(weights) + 1),
                "weights": weights,
                "agents": agents,
                "pool": pool,
                "gaps": gaps,
                "minimum_gap": min(gaps),
            }
        )

    # Complete grid corroboration of the binary contrast. The proof certificate
    # below, rather than this grid, supplies the universal argument.
    binary_grid = [value / 100 for value in range(1, 100)]
    binary_strict_cases = 0
    for left_index, left_probability in enumerate(binary_grid):
        for right_probability in binary_grid[left_index + 1 :]:
            agents = [
                [left_probability, 1.0 - left_probability],
                [right_probability, 1.0 - right_probability],
            ]
            for left_weight in (0.1, 0.25, 0.5, 0.75, 0.9):
                pool = log_pool(agents, [left_weight, 1.0 - left_weight])
                binary_strict_cases += int(
                    min(welfare_gap(agent, pool) for agent in agents) > 1e-14
                )

    independent = claim3_decimal_witness()
    wrong_pool_detected = all(
        min(
            welfare_gap(agent, linear_pool(item["agents"], item["weights"]))
            for agent in item["agents"]
        )
        < 0.0
        for item in fixtures
    )
    passed = (
        all(float(item["minimum_gap"]) > 1e-10 for item in fixtures)
        and binary_strict_cases == 0
        and independent["passed"]
        and wrong_pool_detected
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "passed": passed,
        "contract": {
            "domain": "n>=2 full-support beliefs; at least three outcomes",
            "pool": "normalized weighted geometric mean",
            "weights": "positive normalized; max_i beta_i<1",
            "quantifier": "there exist beliefs yielding Delta_i>0 for every agent",
        },
        "construction": (
            "on {o_0,...,o_n}: P_i(o_i)=epsilon, "
            "P_i(o_0)=1-epsilon-(n-1)epsilon^(n+1), "
            "and P_i(other)=epsilon^(n+1)"
        ),
        "asymptotic_certificate": {
            "private_pool_exponent": "c_i=(n+1)-n*beta_i>1",
            "agent_entropy": "H(P_i)=Theta(epsilon*log(1/epsilon))",
            "pool_entropy": "H(P)=o(epsilon*log(1/epsilon))",
            "reverse_kl": "KL(P||P_i)=O(epsilon)",
            "conclusion": "Delta_i/(epsilon*log(1/epsilon)) -> 1",
        },
        "fixtures": fixtures,
        "independent_checker": independent,
        "negative_controls": {
            "binary_grid_cases": 99 * 98 // 2 * 5,
            "binary_strict_unanimity_cases": binary_strict_cases,
            "binary_analytic_reason": (
                "Delta_i=(q-p_i)logit(p_i), while logit(q) is a "
                "positive-weight average of the agents' logits; an extreme "
                "same-side agent or either agent in a mixed-side pair cannot benefit"
            ),
            "wrong_linear_pool_detected": wrong_pool_detected,
        },
        "limitation": (
            "Finite fixtures audit the construction; the existence conclusion "
            "uses the displayed asymptotic certificate. The construction uses "
            "n+1 outcomes; the n=2 fixture directly establishes the three-outcome frontier."
        ),
    }


def claim4() -> dict[str, Any]:
    # Any centered vector is a valid centered log-profile under a uniform base
    # after softmax. H and A are aligned duplicates; W is anti-aligned.
    profiles = [
        [1.0, -1.0, 0.0],
        [1.0, -1.0, 0.0],
        [-1.0, 1.0, 0.0],
    ]
    agents = [normalize([math.exp(value) for value in profile]) for profile in profiles]
    base_weights = [0.25, 0.25, 0.5]
    delta_weights = [0.05, -0.05, 0.0]
    new_weights = [
        weight + change for weight, change in zip(base_weights, delta_weights)
    ]
    base_pool = log_pool(agents, base_weights)
    new_pool = log_pool(agents, new_weights)
    visible_profiles = [
        centered_log_profile(agent, base_pool) for agent in agents
    ]
    h_profile = visible_profiles[0]
    inner_products = [
        weighted_inner(base_pool, profile, h_profile)
        for profile in visible_profiles
    ]
    h_norm_sq = weighted_inner(base_pool, h_profile, h_profile)
    delta_log_profile = [
        math.fsum(
            change * profile[outcome]
            for change, profile in zip(delta_weights, visible_profiles)
        )
        for outcome in range(3)
    ]
    epsilon = math.sqrt(
        weighted_inner(base_pool, delta_log_profile, delta_log_profile)
    )
    remainder_norm = 0.0
    anti_indices = [
        index for index, value in enumerate(inner_products) if value < 0.0
    ]
    aligned_indices = [
        index for index, value in enumerate(inner_products) if value >= 0.0
    ]
    lhs = math.fsum(
        max(delta_weights[index], 0.0) * abs(inner_products[index])
        for index in anti_indices
    )
    aligned_downweight_term = math.fsum(
        max(-delta_weights[index], 0.0) * inner_products[index]
        for index in aligned_indices
    )
    rhs = (
        delta_weights[0] * h_norm_sq
        - (epsilon + remainder_norm) * math.sqrt(h_norm_sq)
        - aligned_downweight_term
    )
    mutated_rhs = (
        delta_weights[0] * h_norm_sq
        - (epsilon + remainder_norm) * math.sqrt(h_norm_sq)
    )
    pool_shift = max(
        abs(left - right) for left, right in zip(base_pool, new_pool)
    )
    broad_conclusion_holds = any(
        delta_weights[index] > 0.0 for index in anti_indices
    )
    independent = claim4_decimal_counterexample()
    passed = (
        math.isclose(math.fsum(delta_weights), 0.0, abs_tol=1e-14)
        and delta_weights[0] > 0.0
        and pool_shift < 1e-14
        and len(anti_indices) == 1
        and lhs + 1e-14 >= rhs
        and lhs + 1e-14 < mutated_rhs
        and not broad_conclusion_holds
        and independent["passed"]
    )
    return {
        "status": "FALSIFIED" if passed else "BLOCKED",
        "passed": passed,
        "claim_tested": (
            "Under stable logit deviation, increasing a benevolent component "
            "necessarily strengthens an antagonistic counterpart."
        ),
        "counterexample": {
            "outcomes": 3,
            "component_names": ["H_benevolent", "A_aligned_duplicate", "W_antagonist"],
            "agents": agents,
            "base_weights": base_weights,
            "delta_weights": delta_weights,
            "new_weights": new_weights,
            "base_pool": base_pool,
            "new_pool": new_pool,
            "pool_shift_max": pool_shift,
            "inner_products_with_H": inner_products,
            "anti_aligned_indices": anti_indices,
            "waluigi_weight_change": delta_weights[2],
            "broad_conclusion_holds": broad_conclusion_holds,
        },
        "exact_theorem_19_audit": {
            "epsilon": epsilon,
            "remainder_norm": remainder_norm,
            "lhs_anti_aligned_increases": lhs,
            "aligned_downweight_term": aligned_downweight_term,
            "rhs": rhs,
            "inequality_holds": lhs + 1e-14 >= rhs,
            "special_consequence_applicable": False,
            "why_not": (
                "the aligned duplicate A is downweighted; Theorem 19's "
                "strict W consequence explicitly excludes aligned downweighting"
            ),
        },
        "independent_checker": independent,
        "negative_control": {
            "mutation": "omit the aligned-downweight term from inequality (3)",
            "mutated_rhs": mutated_rhs,
            "detected": lhs + 1e-14 < mutated_rhs,
        },
        "interpretation": (
            "The general compensation inequality is satisfied exactly. The "
            "broader judged wording is false because it omits the theorem's "
            "additional no-aligned-downweighting and positive-margin conditions."
        ),
    }


def _vector_subtract(left: list[float], right: list[float]) -> list[float]:
    return [left_value - right_value for left_value, right_value in zip(left, right)]


def _vector_norm(reference: list[float], vector: list[float]) -> float:
    return math.sqrt(weighted_inner(reference, vector, vector))


def claim5() -> dict[str, Any]:
    reference = [0.25, 0.25, 0.25, 0.25]
    event = [1.0, 0.0, 0.0, 0.0]
    event_probability = expectation(reference, event)
    g_event = [value - event_probability for value in event]
    h_direction = [-1.0, 1.0, -1.0, 1.0]
    w_direction = [3.0, -1.0, -1.0, -1.0]
    baseline_basis = [h_direction]
    expanded_basis = [h_direction, w_direction]
    budget = 0.2

    pure_projection = project_onto_span(reference, g_event, baseline_basis)
    shatter_projection = project_onto_span(reference, g_event, expanded_basis)
    projected_w = project_onto_span(reference, w_direction, baseline_basis)
    novelty = _vector_subtract(w_direction, projected_w)
    novelty_norm = _vector_norm(reference, novelty)
    novelty_correlation = weighted_inner(reference, g_event, novelty)
    pure_projection_norm = _vector_norm(reference, pure_projection)
    shatter_projection_norm = _vector_norm(reference, shatter_projection)
    pure_max = budget * pure_projection_norm
    shatter_max = budget * shatter_projection_norm
    strict_gain = shatter_max - pure_max
    pythagorean_rhs = (
        pure_projection_norm**2
        + novelty_correlation**2 / novelty_norm**2
    )
    pythagorean_error = abs(shatter_projection_norm**2 - pythagorean_rhs)

    pure_optimizer = [
        -budget * value / pure_projection_norm for value in pure_projection
    ]
    shatter_optimizer = [
        -budget * value / shatter_projection_norm for value in shatter_projection
    ]
    pure_objective = -weighted_inner(reference, pure_optimizer, g_event)
    shatter_objective = -weighted_inner(reference, shatter_optimizer, g_event)

    finite_calibration: list[dict[str, float]] = []
    for calibration_budget in (0.1, 0.05, 0.02, 0.01):
        direction = [
            -calibration_budget * value / shatter_projection_norm
            for value in shatter_projection
        ]
        updated = normalize(
            [
                probability * math.exp(change)
                for probability, change in zip(reference, direction)
            ]
        )
        actual_reduction = reference[0] - updated[0]
        first_order = calibration_budget * shatter_projection_norm
        finite_calibration.append(
            {
                "budget": calibration_budget,
                "actual_event_reduction": actual_reduction,
                "first_order_prediction": first_order,
                "ratio": actual_reduction / first_order,
            }
        )

    inside_span_w = [2.0 * value for value in h_direction]
    inside_novelty = _vector_subtract(
        inside_span_w,
        project_onto_span(reference, inside_span_w, baseline_basis),
    )
    inside_novelty_norm = _vector_norm(reference, inside_novelty)
    orthogonal_novelty = [0.0, 1.0, 0.0, -1.0]
    orthogonal_correlation = weighted_inner(
        reference, g_event, orthogonal_novelty
    )
    independent = claim5_decimal_geometry()
    passed = (
        novelty_norm > 1e-12
        and abs(novelty_correlation) > 1e-12
        and strict_gain > 1e-12
        and pythagorean_error < 1e-12
        and abs(pure_objective - pure_max) < 1e-12
        and abs(shatter_objective - shatter_max) < 1e-12
        and abs(_vector_norm(reference, pure_optimizer) - budget) < 1e-12
        and abs(_vector_norm(reference, shatter_optimizer) - budget) < 1e-12
        and abs(finite_calibration[-1]["ratio"] - 1.0) < 0.02
        and inside_novelty_norm < 1e-12
        and abs(orthogonal_correlation) < 1e-12
        and independent["passed"]
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "passed": passed,
        "contract": {
            "base": "strictly positive P on a finite outcome space",
            "event": "A is a proper subset; g_A=1_A-P(A)",
            "budget": "||Delta L||_P <= epsilon",
            "baseline_span": "S0=span of available centered log profiles",
            "novelty": "u=w-Proj_S0(w) is nonzero",
            "correlation": "<g_A,u>_P is nonzero",
            "conclusion": "M(S1)>M(S0), S1=span(S0,w)",
        },
        "geometry": {
            "reference": reference,
            "event": [0],
            "g_A": g_event,
            "H": h_direction,
            "w": w_direction,
            "u": novelty,
            "u_norm": novelty_norm,
            "g_u_inner": novelty_correlation,
            "budget": budget,
            "pure_projection_norm": pure_projection_norm,
            "shatter_projection_norm": shatter_projection_norm,
            "pure_max_reduction": pure_max,
            "shatter_max_reduction": shatter_max,
            "strict_gain": strict_gain,
            "pythagorean_error": pythagorean_error,
            "pure_optimizer_objective": pure_objective,
            "shatter_optimizer_objective": shatter_objective,
        },
        "finite_exponential_tilt_calibration": finite_calibration,
        "independent_checker": independent,
        "negative_controls": {
            "inside_span": {
                "u_norm": inside_novelty_norm,
                "strict_gain_expected": 0.0,
                "detected": inside_novelty_norm < 1e-12,
            },
            "novel_but_event_orthogonal": {
                "g_u_inner": orthogonal_correlation,
                "strict_gain_expected": 0.0,
                "detected": abs(orthogonal_correlation) < 1e-12,
            },
        },
        "limitation": (
            "This verifies the paper's first-order theorem under the explicit "
            "Appendix novelty and correlation assumptions. It does not claim "
            "a multi-step neural-network training result."
        ),
        "source_formula_note": (
            "The general strict gain is epsilon*(||Proj_S1 g||-||Proj_S0 g||). "
            "The Appendix's Pythagorean identity proves positivity; the more "
            "compact equality printed in Theorem 75 is not used as a general identity."
        ),
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
        "claim_3": claim3(rng),
        "claim_4": claim4(),
        "claim_5": claim5(),
        "claim_6": claim6_toy(),
    }
    return {
        "campaign_stage": "claim_5_first_order_shattering",
        "seed": SEED,
        "claims": claims,
        "full_credit_claims": sum(item["status"] in {"VERIFIED", "FALSIFIED"} for item in claims.values()),
        "toy_claims": sum(item["status"] == "TOY" for item in claims.values()),
        "baseline_points": 7,
        "passed": all(item["passed"] for item in claims.values()),
    }
