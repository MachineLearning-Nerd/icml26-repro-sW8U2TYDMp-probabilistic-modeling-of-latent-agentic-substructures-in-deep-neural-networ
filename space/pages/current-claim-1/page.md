# Current verification: Claim 1

Status: **VERIFIED by the live judge; cumulative rerun pending**.

This page supersedes the old combined verifier for Claim 1. The old page remains reachable as **Historical rejected baseline**.

## Exact claim contract

For a finite, strictly positive probability distribution \(P\) on outcomes \(\mathcal O\), the epistemic utility of every outcome \(o\) is

\[
U(o)=\log P(o),
\]

and therefore \(\mathbb E_P[U]=-H(P)\).

Source: arXiv:2509.06701v2, Section 2, Definitions 1–3. Retrieved 2026-07-26 from `https://ar5iv.labs.arxiv.org/html/2509.06701v2`; SHA-256 `013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

## Visible implementation and fixed command

The complete implementation is in `reproduction/math_core.py`; the verifier is `reproduction/verifier.py::claim1`.

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

Raw historical record: `.openresearch/artifacts/claim-1/raw.json`.

The current verifier additionally injects a destructive control that returns \(P(o)\) instead of \(\log P(o)\); the identity check must detect that mutation. It exits nonzero if the exact check or the control fails.

## Limitations

This verifies the mathematical definition. It does not identify a latent agent inside a trained neural network. The accepted Claim 1 check will be rerun unchanged in every cumulative experiment.
