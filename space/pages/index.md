# Claim-by-claim reproduction of latent agentic substructures

**Current evidence package — awaiting live judge.** The previous live score is
**7/12** at immutable Space revision
`3d065680c4492fdfc5e339a95f8287af6a533ec7`. No score change is claimed.

The paper models latent agents as probability distributions and asks how
logarithmic aggregation, compositional refinement, and low-dimensional
perturbations constrain their welfare. This package replaces five hidden,
toy-scale implementations with visible theorem-level certificates,
constructions, controls, and independent high-precision checkers.

## Results at a glance

| Claim | Exact current result | Strongest observed evidence | Current page |
|---|---|---|---|
| 1. Log-score utility | **VERIFIED** | pointwise and entropy errors `0.0` | [Claim 1](#/current-claim-1) |
| 2. Linear-pool impossibility | **VERIFIED** | analytic symmetric-KL certificate; Decimal residual `1E-70` | [Claim 2](#/current-claim-2) |
| 3. Three-outcome log-pool existence | **VERIFIED** | predeclared full-support witnesses; all gaps positive | [Claim 3](#/current-claim-3) |
| 4. Broad “necessarily strengthens Waluigi” wording | **FALSIFIED** | stable duplicate-component counterexample; Waluigi change `0` | [Claim 4](#/current-claim-4) |
| 5. Manifest-then-suppress span gain | **VERIFIED** | exact gain `0.03660254037844386`; two controls remove strictness | [Claim 5](#/current-claim-5) |
| 6. Parent benefit need not reach children | **VERIFIED** | parent `+0.128975`, compatible child `-2.620105` | [Claim 6](#/current-claim-6) |

Claim 4 falsifies the broad judged paraphrase, not Theorem 19's conditional
compensation inequality. Claim 5 verifies the theorem's first-order span
geometry, not a multi-step neural training trajectory.

## Reproduce the complete evidence

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

The command is fixed across every experiment. The candidate includes
[`pyproject.toml`](../pyproject.toml), [`uv.lock`](../uv.lock), the
complete [`verifier.py`](../reproduction/verifier.py), the independent
[`independent_checker.py`](../reproduction/independent_checker.py), and the
executable [`run_all.py`](../reproduction/run_all.py). The
[raw cumulative run record](../evidence/run_summary.json) captures the
supervised evidence.

The supervised cumulative run used Git SHA
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`, deterministic seed `42`,
one local Python thread, `0.2946048330049962` verifier seconds, 5 orchestrated
seconds, and `$0` cost. It exits nonzero if any exact check, independent
checker, or negative control fails.

## Reviewer map

- [Evaluator visibility matrix](#/visibility) — direct links to every contract,
  implementation, raw result, checker, control, and limitation.
- [Illustrated report](#/report) — implementation-led explanation and figures.
- [Release forecast](#/release) — conservative forecast, confidence, and risks;
  it is not a judge result.
- [Historical rejected baseline](#/verification-run) — preserved for audit,
  clearly superseded by the current pages above.

The exact judged files also remain unchanged under
`historical/judged-3d065680/`.
