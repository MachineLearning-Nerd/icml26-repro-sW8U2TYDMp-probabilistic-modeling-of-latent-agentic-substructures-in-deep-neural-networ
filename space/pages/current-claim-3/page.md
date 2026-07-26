# Current verification: Claim 3

**Verdict contract:** `VERIFIED` only if a visible full-support construction
produces strict benefit under the paper's logarithmic pool, an independent
checker agrees, and binary and wrong-pool controls behave as predicted.

## Source contract

Section 3.1, Theorem 9 states existence for `n>=2` once there are at least
three outcomes, with epistemic welfare `log P_i`. Appendix E.2, Theorems
34–36 give the construction and arbitrary-weight extension. The archived
arXiv:2509.06701v2 source has SHA-256
`013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

For `n` agents use outcomes `{o_0,...,o_n}`, a fixed
`0<epsilon<1/4`, and `delta=epsilon^(n+1)`:

```text
P_i(o_i) = epsilon
P_i(o_0) = 1 - epsilon - (n-1) delta
P_i(o_j) = delta                    for j != i
```

All probabilities are strictly positive. For weights with
`max_i beta_i<1`, raw log-pool mass on `o_i` is
`epsilon^c_i`, where `c_i=(n+1)-n beta_i>1`.
Consequently

```text
H(P_i) = Theta(epsilon log(1/epsilon))
H(P) = o(epsilon log(1/epsilon))
KL(P || P_i) = O(epsilon)
Delta_i / (epsilon log(1/epsilon)) -> 1.
```

Thus every gap is positive for sufficiently small epsilon. The `n=2`
construction is an explicit three-outcome witness.

## Executable audit and controls

The visible verifier is `reproduction/verifier.py::claim3`; the independent
70-digit implementation is
`reproduction/independent_checker.py::claim3_decimal_witness`.
The fixed command is:

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

Fixtures use the predeclared `epsilon=1e-5` and four equal/nonuniform weight
vectors; there is no witness search. Replacing the log pool with the linear
pool must make at least one agent worse off in every fixture.

The binary control uses the exact identity
`Delta_i=(q-p_i)logit(p_i)`. Since `logit(q)` is a convex combination of
the agents' logits, an extreme same-side agent cannot improve, while
mixed-side requirements are incompatible. A complete 0.01-grid check is
printed only as checker calibration.

Exact supervised output and raw JSON will be attached before release.
