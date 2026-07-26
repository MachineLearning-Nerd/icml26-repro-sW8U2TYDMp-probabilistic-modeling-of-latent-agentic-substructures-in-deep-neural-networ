# Current verification: Claim 4

**Verdict contract: FALSIFIED** if a full-support, stable perturbation increases
Luigi without increasing any anti-aligned weight, while still satisfying
Theorem 19's exact inequality.

## What Theorem 19 actually says

Section 5, Theorem 19 (Appendix I.2, Theorem 69) gives

```text
sum_anti (Delta beta_i)+ |<v_i,v_H>_P|
 >= delta ||v_H||_P^2
    - (epsilon + ||r||_P)||v_H||_P
    - sum_aligned (Delta beta_j)- <v_j,v_H>_P.
```

A distinguished Waluigi must strictly increase only if W is the sole
anti-aligned component, aligned components are not downweighted, and
`epsilon+||r||_P < delta||v_H||_P`. The broad Claim 4 wording omits the last
two restrictions.

Source: arXiv:2509.06701v2, archived SHA-256
`013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

## Assumption-satisfying counterexample

On three outcomes, use centered log profiles

```text
H = ( 1,-1,0)   benevolent
A = ( 1,-1,0)   aligned duplicate
W = (-1, 1,0)   unique antagonist
```

Softmax makes each a full-support probability distribution. At base weights
`(0.25,0.25,0.50)`, the log pool is uniform. Apply
`Delta beta=(+0.05,-0.05,0)`. The weights remain nonnegative and normalized;
Luigi rises; the aligned duplicate falls; Waluigi is unchanged. Because
`Delta beta_H v_H + Delta beta_A v_A = 0`, the new pool is exactly the old
pool and `epsilon=0`.

The exact theorem inequality holds at equality: the Luigi term is cancelled
by the aligned-downweight term. Omitting that essential term makes the seeded
mutation fail.

## Executable and independent checks

The visible implementation is `reproduction/verifier.py::claim4`; centered
profiles and weighted inner products are in `reproduction/math_core.py`.
`reproduction/independent_checker.py::claim4_decimal_counterexample`
recomputes everything at 70-digit precision.

Fixed command:

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

The process exits nonzero unless the counterexample satisfies every listed
assumption, the exact inequality passes, the broad conclusion is contradicted,
and the mutated inequality is rejected. Raw supervised output will be linked
before release.

This falsifies the broad judged wording, not Theorem 19's conditional
compensation inequality.
