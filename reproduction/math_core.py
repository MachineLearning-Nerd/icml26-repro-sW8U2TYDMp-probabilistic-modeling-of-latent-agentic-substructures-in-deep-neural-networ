"""Visible finite-probability definitions used by every verifier."""

from __future__ import annotations

import math
from collections.abc import Sequence


Vector = Sequence[float]


def normalize(values: Vector) -> list[float]:
    total = math.fsum(values)
    if not math.isfinite(total) or total <= 0.0:
        raise ValueError("normalization requires a positive finite total")
    result = [float(value) / total for value in values]
    if any(value <= 0.0 or not math.isfinite(value) for value in result):
        raise ValueError("paper domain requires strictly positive probabilities")
    return result


def validate_distribution(values: Vector, *, atol: float = 1e-12) -> None:
    if not values or any(value <= 0.0 or not math.isfinite(value) for value in values):
        raise ValueError("distribution must have finite full support")
    if not math.isclose(math.fsum(values), 1.0, abs_tol=atol):
        raise ValueError("distribution must sum to one")


def epistemic_utility(agent: Vector, outcome: int) -> float:
    validate_distribution(agent)
    return math.log(agent[outcome])


def expectation(distribution: Vector, values: Vector) -> float:
    validate_distribution(distribution)
    if len(distribution) != len(values):
        raise ValueError("dimension mismatch")
    return math.fsum(probability * value for probability, value in zip(distribution, values))


def entropy(distribution: Vector) -> float:
    validate_distribution(distribution)
    return -math.fsum(value * math.log(value) for value in distribution)


def kl_divergence(left: Vector, right: Vector) -> float:
    validate_distribution(left)
    validate_distribution(right)
    if len(left) != len(right):
        raise ValueError("dimension mismatch")
    return math.fsum(p * math.log(p / q) for p, q in zip(left, right))


def welfare_gap(agent: Vector, pool: Vector) -> float:
    """E_pool[log(agent)] - E_agent[log(agent)]."""
    utilities = [math.log(value) for value in agent]
    return expectation(pool, utilities) - expectation(agent, utilities)


def centered_log_profile(agent: Vector, reference: Vector) -> list[float]:
    """The paper's v_i = log P_i - E_reference[log P_i]."""
    validate_distribution(agent)
    validate_distribution(reference)
    if len(agent) != len(reference):
        raise ValueError("dimension mismatch")
    log_values = [math.log(value) for value in agent]
    center = expectation(reference, log_values)
    return [value - center for value in log_values]


def weighted_inner(reference: Vector, left: Vector, right: Vector) -> float:
    validate_distribution(reference)
    if len(reference) != len(left) or len(left) != len(right):
        raise ValueError("dimension mismatch")
    return math.fsum(
        probability * left_value * right_value
        for probability, left_value, right_value in zip(reference, left, right)
    )


def linear_pool(agents: Sequence[Vector], weights: Vector) -> list[float]:
    _validate_pool_inputs(agents, weights)
    result = [
        math.fsum(weight * agent[outcome] for weight, agent in zip(weights, agents))
        for outcome in range(len(agents[0]))
    ]
    validate_distribution(result)
    return result


def log_pool(agents: Sequence[Vector], weights: Vector) -> list[float]:
    _validate_pool_inputs(agents, weights)
    logits = [
        math.fsum(weight * math.log(agent[outcome]) for weight, agent in zip(weights, agents))
        for outcome in range(len(agents[0]))
    ]
    shift = max(logits)
    return normalize([math.exp(value - shift) for value in logits])


def _validate_pool_inputs(agents: Sequence[Vector], weights: Vector) -> None:
    if len(agents) < 2 or len(agents) != len(weights):
        raise ValueError("pool needs matching agents and weights")
    for agent in agents:
        validate_distribution(agent)
    if len({len(agent) for agent in agents}) != 1:
        raise ValueError("agent dimensions differ")
    if any(weight <= 0.0 for weight in weights):
        raise ValueError("the theorem contract uses positive weights")
    if not math.isclose(math.fsum(weights), 1.0, abs_tol=1e-12):
        raise ValueError("weights must sum to one")
