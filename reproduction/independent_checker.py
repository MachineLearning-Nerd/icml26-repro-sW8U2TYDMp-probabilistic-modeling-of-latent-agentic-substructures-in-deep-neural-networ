"""High-precision checkers that do not import the production math primitives."""

from __future__ import annotations

from decimal import Decimal, localcontext
from typing import Any


def claim2_decimal_certificate() -> dict[str, Any]:
    """Recompute the linear-pool certificate with Decimal arithmetic."""
    with localcontext() as context:
        context.prec = 70
        agents = [
            [Decimal("0.10"), Decimal("0.20"), Decimal("0.70")],
            [Decimal("0.60"), Decimal("0.25"), Decimal("0.15")],
            [Decimal("0.20"), Decimal("0.50"), Decimal("0.30")],
        ]
        weights = [Decimal("0.20"), Decimal("0.30"), Decimal("0.50")]
        pool = [
            sum(
                (weight * agent[outcome] for weight, agent in zip(weights, agents)),
                Decimal(0),
            )
            for outcome in range(3)
        ]
        gaps = [
            sum(
                (
                    (pool[outcome] - agent[outcome]) * agent[outcome].ln()
                    for outcome in range(3)
                ),
                Decimal(0),
            )
            for agent in agents
        ]
        weighted_gap = sum(
            (weight * gap for weight, gap in zip(weights, gaps)), Decimal(0)
        )
        forward = sum(
            (
                weight
                * sum(
                    (
                        agent[outcome]
                        * (agent[outcome] / pool[outcome]).ln()
                        for outcome in range(3)
                    ),
                    Decimal(0),
                )
                for weight, agent in zip(weights, agents)
            ),
            Decimal(0),
        )
        reverse = sum(
            (
                weight
                * sum(
                    (
                        pool[outcome]
                        * (pool[outcome] / agent[outcome]).ln()
                        for outcome in range(3)
                    ),
                    Decimal(0),
                )
                for weight, agent in zip(weights, agents)
            ),
            Decimal(0),
        )
        residual = weighted_gap + forward + reverse
        mutation_residual = weighted_gap + forward
        tolerance = Decimal("1e-60")
        passed = (
            weighted_gap < 0
            and forward > 0
            and reverse > 0
            and abs(residual) < tolerance
            and abs(mutation_residual) > Decimal("1e-6")
        )
        return {
            "checker": "independent Decimal implementation, precision=70",
            "pool": [str(value) for value in pool],
            "gaps": [str(value) for value in gaps],
            "weighted_gap": str(weighted_gap),
            "forward_kl": str(forward),
            "reverse_kl": str(reverse),
            "certificate_residual": str(residual),
            "omit_reverse_mutation_residual": str(mutation_residual),
            "tolerance": str(tolerance),
            "passed": passed,
        }


def claim3_decimal_witness() -> dict[str, Any]:
    """Independently check the paper's n=2, three-outcome construction."""
    with localcontext() as context:
        context.prec = 70
        epsilon = Decimal("0.00001")
        delta = epsilon**3
        base = Decimal(1) - epsilon - delta
        agents = [
            [base, epsilon, delta],
            [base, delta, epsilon],
        ]
        raw_pool = [
            (agents[0][outcome] * agents[1][outcome]).sqrt()
            for outcome in range(3)
        ]
        normalizer = sum(raw_pool, Decimal(0))
        pool = [value / normalizer for value in raw_pool]
        gaps = [
            sum(
                (
                    (pool[outcome] - agent[outcome]) * agent[outcome].ln()
                    for outcome in range(3)
                ),
                Decimal(0),
            )
            for agent in agents
        ]
        # Linear pooling is the named wrong-pool mutation.
        linear_pool = [
            (agents[0][outcome] + agents[1][outcome]) / Decimal(2)
            for outcome in range(3)
        ]
        linear_gaps = [
            sum(
                (
                    (linear_pool[outcome] - agent[outcome]) * agent[outcome].ln()
                    for outcome in range(3)
                ),
                Decimal(0),
            )
            for agent in agents
        ]
        passed = min(gaps) > 0 and min(linear_gaps) < 0
        return {
            "checker": "independent Decimal construction, precision=70",
            "epsilon": str(epsilon),
            "delta": str(delta),
            "agents": [[str(value) for value in agent] for agent in agents],
            "log_pool": [str(value) for value in pool],
            "log_pool_gaps": [str(value) for value in gaps],
            "wrong_linear_pool_gaps": [str(value) for value in linear_gaps],
            "passed": passed,
        }


def claim4_decimal_counterexample() -> dict[str, Any]:
    """Independently audit Theorem 19 and the broader claimed consequence."""
    with localcontext() as context:
        context.prec = 70
        zero = Decimal(0)
        profiles = [
            [Decimal(1), Decimal(-1), zero],   # H (Luigi)
            [Decimal(1), Decimal(-1), zero],   # aligned duplicate
            [Decimal(-1), Decimal(1), zero],   # W (anti-aligned)
        ]

        def softmax(profile: list[Decimal]) -> list[Decimal]:
            raw = [value.exp() for value in profile]
            total = sum(raw, zero)
            return [value / total for value in raw]

        def log_pool(
            agents: list[list[Decimal]], weights: list[Decimal]
        ) -> list[Decimal]:
            raw = [
                sum(
                    (
                        weight * agent[outcome].ln()
                        for weight, agent in zip(weights, agents)
                    ),
                    zero,
                ).exp()
                for outcome in range(3)
            ]
            total = sum(raw, zero)
            return [value / total for value in raw]

        agents = [softmax(profile) for profile in profiles]
        base_weights = [Decimal("0.25"), Decimal("0.25"), Decimal("0.50")]
        delta_weights = [Decimal("0.05"), Decimal("-0.05"), zero]
        new_weights = [
            value + change for value, change in zip(base_weights, delta_weights)
        ]
        base_pool = log_pool(agents, base_weights)
        new_pool = log_pool(agents, new_weights)

        def centered_profile(
            agent: list[Decimal], reference: list[Decimal]
        ) -> list[Decimal]:
            logs = [value.ln() for value in agent]
            center = sum(
                (probability * value for probability, value in zip(reference, logs)),
                zero,
            )
            return [value - center for value in logs]

        visible_profiles = [
            centered_profile(agent, base_pool) for agent in agents
        ]

        def inner(left: list[Decimal], right: list[Decimal]) -> Decimal:
            return sum(
                (
                    probability * left_value * right_value
                    for probability, left_value, right_value in zip(
                        base_pool, left, right
                    )
                ),
                zero,
            )

        h_profile = visible_profiles[0]
        inner_products = [inner(profile, h_profile) for profile in visible_profiles]
        h_norm_sq = inner(h_profile, h_profile)
        delta_log_profile = [
            sum(
                (
                    change * profile[outcome]
                    for change, profile in zip(delta_weights, visible_profiles)
                ),
                zero,
            )
            for outcome in range(3)
        ]
        epsilon = inner(delta_log_profile, delta_log_profile).sqrt()
        lhs = max(delta_weights[2], zero) * abs(inner_products[2])
        aligned_downweight = (
            max(-delta_weights[1], zero) * inner_products[1]
        )
        rhs = (
            delta_weights[0] * h_norm_sq
            - epsilon * h_norm_sq.sqrt()
            - aligned_downweight
        )
        mutated_rhs = (
            delta_weights[0] * h_norm_sq - epsilon * h_norm_sq.sqrt()
        )
        pool_shift = max(
            abs(left - right) for left, right in zip(base_pool, new_pool)
        )
        tolerance = Decimal("1e-60")
        passed = (
            inner_products[2] < 0
            and delta_weights[2] == 0
            and pool_shift < tolerance
            and lhs + tolerance >= rhs
            and lhs + tolerance < mutated_rhs
        )
        return {
            "checker": "independent Decimal log-pool audit, precision=70",
            "base_weights": [str(value) for value in base_weights],
            "delta_weights": [str(value) for value in delta_weights],
            "base_pool": [str(value) for value in base_pool],
            "new_pool": [str(value) for value in new_pool],
            "pool_shift_max": str(pool_shift),
            "inner_products_with_H": [str(value) for value in inner_products],
            "waluigi_weight_change": str(delta_weights[2]),
            "theorem_lhs": str(lhs),
            "theorem_rhs": str(rhs),
            "omit_aligned_downweight_term_rhs": str(mutated_rhs),
            "passed": passed,
        }


def claim5_decimal_geometry() -> dict[str, Any]:
    """Independently check the weighted projection identities for Claim 5."""
    with localcontext() as context:
        context.prec = 70
        quarter = Decimal("0.25")
        zero = Decimal(0)
        epsilon = Decimal("0.20")
        g = [Decimal("0.75"), Decimal("-0.25"), Decimal("-0.25"), Decimal("-0.25")]
        h = [Decimal(-1), Decimal(1), Decimal(-1), Decimal(1)]
        w = [Decimal(3), Decimal(-1), Decimal(-1), Decimal(-1)]

        def inner(left: list[Decimal], right: list[Decimal]) -> Decimal:
            return sum(
                (quarter * x * y for x, y in zip(left, right)),
                zero,
            )

        h_norm_sq = inner(h, h)
        projection_coefficient = inner(w, h) / h_norm_sq
        u = [
            value - projection_coefficient * direction
            for value, direction in zip(w, h)
        ]
        u_norm_sq = inner(u, u)
        g_u = inner(g, u)
        pure_projection_norm_sq = inner(g, h) ** 2 / h_norm_sq
        shatter_projection_norm_sq = (
            pure_projection_norm_sq + g_u**2 / u_norm_sq
        )
        pure = epsilon * pure_projection_norm_sq.sqrt()
        shatter = epsilon * shatter_projection_norm_sq.sqrt()
        proposition_residual = (
            shatter_projection_norm_sq
            - pure_projection_norm_sq
            - g_u**2 / u_norm_sq
        )
        inside_w = [Decimal(2) * value for value in h]
        inside_coefficient = inner(inside_w, h) / h_norm_sq
        inside_u = [
            value - inside_coefficient * direction
            for value, direction in zip(inside_w, h)
        ]
        inside_u_norm_sq = inner(inside_u, inside_u)
        orthogonal_u = [zero, Decimal(1), zero, Decimal(-1)]
        orthogonal_correlation = inner(g, orthogonal_u)
        passed = (
            u_norm_sq > 0
            and g_u != 0
            and shatter > pure
            and abs(proposition_residual) < Decimal("1e-60")
            and inside_u_norm_sq == 0
            and orthogonal_correlation == 0
        )
        return {
            "checker": "independent Decimal weighted geometry, precision=70",
            "epsilon": str(epsilon),
            "g_A": [str(value) for value in g],
            "baseline_H": [str(value) for value in h],
            "waluigi_w": [str(value) for value in w],
            "novel_u": [str(value) for value in u],
            "u_norm_sq": str(u_norm_sq),
            "g_u_inner": str(g_u),
            "pure_max_reduction": str(pure),
            "shatter_max_reduction": str(shatter),
            "strict_gain": str(shatter - pure),
            "pythagorean_residual": str(proposition_residual),
            "inside_span_u_norm_sq": str(inside_u_norm_sq),
            "orthogonal_novelty_correlation": str(orthogonal_correlation),
            "passed": passed,
        }
