# Reproduction campaign: latent agentic substructures

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/blob/main/notebooks/latent_agentic_claims.py)

This repository reproduces six judged theoretical claims from
[Probabilistic Modeling of Latent Agentic Substructures in Deep Neural
Networks](https://arxiv.org/abs/2509.06701). It replaces five hidden toy
checks with visible analytic certificates or assumption-audited constructions,
independent 70-digit checkers, and negative controls.

The strongest cumulative run reports Claims 1, 2, 3, 5, and 6 as **VERIFIED**
and **FALSIFIES the broad Claim 4 paraphrase** with a stable counterexample.
The exact Theorem 19 compensation inequality remains valid. The live judged
score remains **7/12** until a new Hugging Face revision is evaluated; no score
increase is claimed here.

| Claim | Paper result | Observed result | Assessment |
|---|---|---|---|
| 1 | `U(o)=log P(o)` and `E[U]=-H(P)` | both errors `0.0` | VERIFIED |
| 2 | strict unanimity impossible under linear pooling | symmetric-KL certificate; Decimal residual `1E-70` | VERIFIED |
| 3 | strict unanimity exists for log pooling with ≥3 outcomes | minimum predeclared-witness gap `1.11675e-4` | VERIFIED |
| 4 | broad wording: Luigi necessarily strengthens Waluigi | valid counterexample has `ΔW=0`, pool shift `0` | FALSIFIED |
| 5 | eliciting then suppressing adds a useful direction | first-order suppression gain `0.03660254` | VERIFIED |
| 6 | parent benefit need not propagate to children | parent `+0.128975`, compatible child `-2.620105` | VERIFIED |

The work is mathematical and CPU-only: one local Python thread, deterministic
seed 42, 0.295 seconds for the strongest verifier, 5 seconds of orchestrated
runtime, and $0 cost. No neural model was trained. Claim 5 is a first-order
span result rather than a ten-step training trajectory, and the existence
claims use explicit paper constructions rather than random search.

- [Illustrated technical report](reports/claim-reproduction/report.md)
- [Self-contained tutorial notebook](notebooks/latent_agentic_claims.py)
- [Existing Hugging Face logbook](https://huggingface.co/spaces/DineshAI/sW8U2TYDMp)

Run the complete fixed verifier with:

```bash
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Reader-facing report, notebook, and release mirror | — |
| [`orx/judged-7-of-12-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/tree/orx/judged-7-of-12-baseline) | Freeze and rerun exact judged baseline | `uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all` | Claim 1 VERIFIED; Claims 2–6 historical TOY | local CPU, 1 thread, 0.029 s |
| [`orx/claim-2-analytic-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/tree/orx/claim-2-analytic-certificate) | Replace sampling with universal proof certificate | `uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all` | Claim 2 VERIFIED; residual `1E-70` | local CPU, 1 thread, 0.007 s |
| [`orx/claim-3-constructive-log-pooling`](https://github.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/tree/orx/claim-3-constructive-log-pooling) | Implement paper's full-support existence witness | `uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all` | Claim 3 VERIFIED; wrong-pool control flips sign | local CPU, 1 thread, <1 s |
| [`orx/claim-4-exact-compensation-law-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/tree/orx/claim-4-exact-compensation-law-audit) | Audit exact Theorem 19 assumptions | `uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all` | Broad Claim 4 FALSIFIED; exact inequality preserved | local CPU, 1 thread, 0.129 s |
| [`orx/claim-5-first-order-shattering-geometry`](https://github.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/tree/orx/claim-5-first-order-shattering-geometry) | Verify exact projection gain and two controls | `uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all` | Claim 5 VERIFIED after one recorded import-fix rerun | local CPU, 1 thread, 0.146 s |
| [`orx/claim-6-compatible-recursive-split`](https://github.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/tree/orx/claim-6-compatible-recursive-split) | Preserve parent/global pool while harming a child | `uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all` | Cumulative: 5 VERIFIED, 1 FALSIFIED, 0 TOY | local CPU, 1 thread, 0.295 s |

## Historical upstream workspace

ICML 2026 agent reproduction workspace for `sW8U2TYDMp`.
