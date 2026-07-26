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
