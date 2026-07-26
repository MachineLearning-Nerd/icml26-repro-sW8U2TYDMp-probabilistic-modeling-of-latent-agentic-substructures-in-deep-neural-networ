# Release report

- Previous live judged score: `7/12`
- Conservative projected score range after the proposed change: **10–12/12**
- Best-supported possible new score: **12/12 (forecast, not a judge result)**

The current total remains **7/12**. The existing Hugging Face Head and Judge
Head are both `3d065680c4492fdfc5e339a95f8287af6a533ec7`. Only the live
judge can change that score.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 2 | 2 | HIGH | VERIFIED | Accepted definition rerun exactly; errors are zero and the destructive mutation is detected. |
| 2 | 1 | 2 | HIGH | VERIFIED | Universal symmetric-KL certificate with Decimal residual `1E-70`; reviewer must accept the displayed derivation as proof-level evidence. |
| 3 | 1 | 2 | HIGH | VERIFIED | Paper construction, high-precision checker, wrong-pool, and binary controls pass. |
| 4 | 1 | 2 | MEDIUM | FALSIFIED | Valid counterexample contradicts the broad wording while satisfying the exact theorem inequality; conditional Theorem 19 is not falsified. |
| 5 | 1 | 2 | MEDIUM | VERIFIED | Exact projection geometry, finite-tilt calibration, and two controls pass; risk remains around broader training-dynamics interpretations. |
| 6 | 1 | 2 | HIGH | VERIFIED | Compatible child split preserves parent/global pool and makes one child strictly worse. |

Claims 2–6 changed from historical toy evidence. No claim is BLOCKED and no
confidence is LOW. The scientific winning SHA is
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`; the evaluator-visible package
ran at `883ec79c9ad238a37bfbc5015acc65f37aec6ddd`.

All nine OpenResearch runs used local CPU, one Python thread, 5 orchestrated
seconds each (45 seconds total), and `$0`. The strongest verifier used
0.294605 seconds. Hugging Face cpu-upgrade was not needed because each task
was confidently below one core and five minutes.

The fixed command on every node was:

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

Blind round 1 identified four visibility gaps. [Round 1](red-team-round1.md)
records them. [Round 2](red-team-round2.md) opened 83 canonical-reachable
files and passed with none missing. All 17 judged paths remain present. Exact
text/SVG copies are in the protected historical subtree; the three judged PNGs
remain hash-identical at their root paths because publication is text-only.
Secret scanning found no credential-like paths.

The exact [text upload allowlist](upload-allowlist.txt) contains 112 UTF-8
paths. The [SHA-256 manifest](upload-manifest.sha256) covers the other 111
files; as standard, the manifest excludes its own hash. No binary PNG or cache
metadata is uploaded.

Publication action after final gates: upload the exact text allowlist to the
existing `DineshAI/sW8U2TYDMp` Space with the Hugging Face commit API, verify
the returned revision by fresh download, mark awaiting judge, and mirror the
same reader-facing content to GitHub `main`.
