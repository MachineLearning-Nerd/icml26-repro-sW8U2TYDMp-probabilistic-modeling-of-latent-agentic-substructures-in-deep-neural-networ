# Current verification: Claim 1

Status: **VERIFIED**. The cumulative verifier reran the accepted identity and
its destructive control successfully.

This page supersedes the old combined verifier for Claim 1. The old page remains reachable as **Historical rejected baseline**.

## Exact claim contract

For a finite, strictly positive probability distribution \(P\) on outcomes \(\mathcal O\), the epistemic utility of every outcome \(o\) is

\[
U(o)=\log P(o),
\]

and therefore \(\mathbb E_P[U]=-H(P)\).

Source: arXiv:2509.06701v2, Section 2, Definitions 1–3. Retrieved 2026-07-26 from `https://ar5iv.labs.arxiv.org/html/2509.06701v2`; SHA-256 `013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

## Visible implementation and fixed command

The complete implementation is
[`reproduction/math_core.py`](../../reproduction/math_core.py); the verifier
is [`reproduction/verifier.py`](../../reproduction/verifier.py), function
`claim1`.

```bash
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

The environment is pinned by `pyproject.toml` and `uv.lock`. Expected compute is one local CPU core and less than five minutes.

## Evidence already accepted

The immutable judged revision evaluated \(P=(0.3,0.5,0.2)\) at every outcome and reported

```text
U(o) = log P(o): verified for all outcomes
E_P[log P] = -1.0297 = -H(P) = -1.0297
```

Raw historical record: [raw.json](../../evidence/claim-1/raw.json).

The current verifier additionally injects a destructive control that returns \(P(o)\) instead of \(\log P(o)\); the identity check must detect that mutation. It exits nonzero if the exact check or the control fails.

## Supervised cumulative evidence

The fixed command ran at Git SHA
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`, seed `42`, on one local CPU
thread. The verifier took `0.2946048330049962` seconds; the orchestrated run
took 5 seconds and cost `$0`.

| Audit | Observed |
|---|---:|
| maximum pointwise log-score error | `0.0` |
| entropy identity error | `0.0` |
| mutation `P[o]` in place of `log(P[o])` detected | `true` |

Download the [current checker output](../../evidence/claim-1/checker.json),
[negative-control output](../../evidence/claim-1/negative_control.json),
[claim contract](../../evidence/claim-1/claim_contract.json), and
[environment record](../../evidence/claim-1/environment.md). The complete
[cumulative run summary](../../evidence/run_summary.json) records the command,
commit, seed, allocation, and runtime. `run_all.py` exits nonzero if any claim
or control fails.

## Limitations

This verifies the mathematical definition. It does not identify a latent
agent inside a trained neural network. See the
[full limitations](../../evidence/claim-1/limitations.md) and
[source audit](../../evidence/claim-1/source_audit.md).
