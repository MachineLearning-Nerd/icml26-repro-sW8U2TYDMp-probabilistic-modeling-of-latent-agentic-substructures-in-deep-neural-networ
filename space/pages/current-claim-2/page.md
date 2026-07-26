# Current verification: Claim 2

**Verdict contract:** `VERIFIED` only if the universal linear-pooling
impossibility follows from a visible analytic certificate and the executable
checker detects its seeded mutations. This supersedes the page labeled
**Historical rejected baseline**, whose random sampling was only toy evidence.

## Exact claim and assumptions

For every finite outcome space, every `n >= 2` full-support agent beliefs
`P_i`, and positive normalized weights `beta_i`, let the linear pool be
`P = sum_i beta_i P_i` and the epistemic utility be `log P_i(o)`.
If the beliefs are not all identical, all welfare gaps cannot be nonnegative.
The identical case has every gap equal to zero and therefore also cannot
provide strict unanimity.

Source anchors: Section 3.1, Theorem 10; Appendix C.3, Theorem 37 in
arXiv:2509.06701v2. Archived source SHA-256:
`013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

## Proof certificate

Define

`Delta_i = E_P[log P_i] - E_Pi[log P_i]`.

Expanding the definitions gives

`Delta_i = H(P_i) - H(P) - KL(P || P_i)`.

The weighted entropy gap is exactly

`H(P) - sum_i beta_i H(P_i) = sum_i beta_i KL(P_i || P)`.

Therefore

`sum_i beta_i Delta_i =
-sum_i beta_i [KL(P_i || P) + KL(P || P_i)] < 0`.

Gibbs' inequality gives `KL(Q || R) >= 0`, with equality exactly when
`Q = R`. Positive weights and at least one non-identical belief make the
forward-KL sum strict. If every `Delta_i >= 0`, the left side would be
nonnegative, a contradiction.

## Executable implementation and controls

The current visible implementation is
[`reproduction/verifier.py`](../../reproduction/verifier.py), function
`claim2`; its only probability primitives are visible in
[`reproduction/math_core.py`](../../reproduction/math_core.py).

Fixed command:

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

The checker computes each gap twice—directly from expectations and through
entropy/KL—and compares the weighted sum with the certificate. Four seeded
fixtures cover 2–4 agents and 2–5 outcomes only to audit the implementation.
They are not substituted for the proof.

The negative controls (1) remove the reverse-KL term, which must break the
identity, and (2) make all agents identical, which must remove strictness.
The process exits nonzero if either mutation is not detected.

## Limitations

Floating-point fixtures cannot establish a universal theorem. Universal
coverage here comes from the displayed symbolic derivation plus Gibbs'
inequality; execution checks that the public implementation and arithmetic
match that derivation.

## Supervised cumulative evidence

At Git SHA `c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`, the four fixture
weighted gaps were `-0.3190425358`, `-0.1371885935`, `-0.1541939779`, and
`-0.4318456062`; the maximum certificate residual was
`1.1102230246251565e-16`. The independent 70-digit Decimal checker obtained a
residual of `1E-70`. Both mutations were detected.

The fixed command used seed `42`, one local CPU thread, `0.2946048330049962`
seconds of verifier runtime, 5 seconds orchestrated runtime, and `$0` cost.
Download [raw output](../../evidence/claim-2/raw.json),
[independent checker](../../evidence/claim-2/checker.json),
[negative controls](../../evidence/claim-2/negative_control.json),
[contract](../../evidence/claim-2/claim_contract.json),
[environment](../../evidence/claim-2/environment.md), and
[full limitations](../../evidence/claim-2/limitations.md).
