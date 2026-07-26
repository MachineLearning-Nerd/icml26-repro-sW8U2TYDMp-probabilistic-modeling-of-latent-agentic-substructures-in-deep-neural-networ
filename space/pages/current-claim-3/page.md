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

## Supervised cumulative evidence

With the predeclared `epsilon=1e-5`, the minimum strict gaps were:

| Agents / weights | Minimum gap |
|---|---:|
| 2 / `(0.5,0.5)` | `0.00011512454946950386` |
| 2 / `(0.2,0.8)` | `0.00011167524269923514` |
| 3 / `(0.1,0.3,0.6)` | `0.0001151286941131128` |
| 4 / `(0.05,0.15,0.3,0.5)` | `0.00011512915459163134` |

The independent 70-digit checker reproduced both two-agent gaps as
`0.0001151245494695038378…`. The wrong linear pool made both gaps negative
(`-0.0001151292546381893587…`), and the complete binary calibration grid had
0 strict cases among 24,255.

The cumulative run used Git SHA
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`, seed `42`, one local CPU
thread, `0.2946048330049962` verifier seconds, 5 orchestrated seconds, and
`$0`. Download [raw output](../../evidence/claim-3/raw.json),
[checker](../../evidence/claim-3/checker.json),
[controls](../../evidence/claim-3/negative_control.json),
[contract](../../evidence/claim-3/claim_contract.json),
[environment](../../evidence/claim-3/environment.md), and
[limitations](../../evidence/claim-3/limitations.md).
