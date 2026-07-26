# Current verification: Claim 5

**Verdict contract: VERIFIED** only under the Appendix's explicit novelty and
event-correlation assumptions, with visible projection code, an independent
checker, and controls that remove strictness.

## Exact theorem geometry

For base belief `P`, harmful event `A`, and
`g_A=1_A-P(A)`, Lemma 71 states

```text
M(S) = epsilon ||Proj_S(g_A)||_P.
```

Let `S0` be the baseline profile span, elicit Waluigi direction `w`, set
`u=w-Proj_S0(w)`, and `S1=span(S0,w)`. Proposition 72 gives

```text
||Proj_S1(g_A)||_P^2
 = ||Proj_S0(g_A)||_P^2 + <g_A,u>_P^2 / ||u||_P^2.
```

When `u!=0` and `<g_A,u>_P!=0`, Corollary 74 therefore yields
`M(S1)>M(S0)`. These conditions appear in Appendix J but are not stated in
the short main-text wording.

Source: Section 5.1, Theorem 21; Appendix J, Lemma 71, Proposition 72,
Corollary 74 and Theorem 75 in arXiv:2509.06701v2. Archived source SHA-256:
`013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

## Reproducible fixture

Use uniform `P` on four outcomes, `A={0}`, and

```text
g_A = ( 0.75,-0.25,-0.25,-0.25)
H   = (-1, 1,-1, 1)
w   = ( 3,-1,-1,-1)
u   = ( 2, 0,-2, 0).
```

The visible dependency-free Gram solver is
`reproduction/math_core.py::project_onto_span`; the current verifier is
`reproduction/verifier.py::claim5`. A separate 70-digit checker lives in
`reproduction/independent_checker.py::claim5_decimal_geometry`.

Fixed command:

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

The checker constructs both optimal directions and confirms they attain the
budgeted objectives. It also applies decreasing finite exponential tilts to
show actual event reduction converging toward the first-order prediction.

Controls put `w` inside the baseline span, then give it novelty orthogonal to
`g_A`; each removes strict gain for a different required assumption.

## Scope and source caveat

This is an exact first-order span result, not a ten-step neural training
trajectory. The general gain is
`epsilon(||Proj_S1 g_A||-||Proj_S0 g_A||)`. The compact equality for the
difference printed in Appendix Theorem 75 is not used as a general identity
when the baseline projection is nonzero; the strict result follows directly
from the preceding Pythagorean identity.

## Supervised cumulative evidence

At budget `0.2`, pure benevolence achieved first-order reduction `0.05`,
whereas the elicited span achieved `0.08660254037844387`, a strict gain of
`0.03660254037844386`. The Pythagorean residual was `0.0`. Finite exponential
tilt ratios approached the first-order result:
`0.941464, 0.970894, 0.988411, 0.994216`. The independent 70-digit checker
reproduced the strict gain. Both the inside-span and event-orthogonal controls
reduced it to exactly zero.

The cumulative run used Git SHA
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`, seed `42`, one local CPU
thread, `0.2946048330049962` verifier seconds, 5 orchestrated seconds, and
`$0`. Download [raw output](../../evidence/claim-5/raw.json),
[checker](../../evidence/claim-5/checker.json),
[controls](../../evidence/claim-5/negative_control.json),
[contract](../../evidence/claim-5/claim_contract.json),
[environment](../../evidence/claim-5/environment.md), and
[limitations](../../evidence/claim-5/limitations.md).
