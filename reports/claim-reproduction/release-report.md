# Release report

- Previous live judged score: `7/12`
- Conservative projected score range after the proposed change: **10–12/12**
- Best-supported possible new score: **12/12 (forecast, not a judge result)**

The current total remains **7/12**. The existing Hugging Face Head and Judge
Head are both `3d065680c4492fdfc5e339a95f8287af6a533ec7`. Only the live
judge can change that score.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 2 | 2 | HIGH | VERIFIED | Accepted definition rerun exactly; pointwise and entropy errors are zero and the destructive mutation is detected. |
| 2 | 1 | 2 | HIGH | VERIFIED | Visible universal symmetric-KL certificate with independent Decimal residual `1E-70`; residual risk is reviewer acceptance of the displayed derivation as proof-level evidence. |
| 3 | 1 | 2 | HIGH | VERIFIED | Paper's predeclared full-support construction gives positive gaps; high-precision, wrong-pool, and binary controls pass. |
| 4 | 1 | 2 | MEDIUM | FALSIFIED | Assumption-audited duplicate-component counterexample contradicts the broad wording while satisfying the exact inequality; interpretation risk remains because conditional Theorem 19 is not falsified. |
| 5 | 1 | 2 | MEDIUM | VERIFIED | Exact Appendix projection geometry, independent checker, finite-tilt calibration, and two strictness controls pass; risk remains if the short wording is read as broader training dynamics. |
| 6 | 1 | 2 | HIGH | VERIFIED | Compatible child split preserves parent/global pool and makes one child strictly worse; high-precision and incompatible-split controls pass. |

Claims 2–6 changed from historical toy checks to current proof- or
construction-level evidence. No claim is BLOCKED. No confidence is LOW, so the
mandatory three-route/fourth-falsification sequence is not triggered.

## Experiment tree and winning evidence

The stacked lineage is baseline → Claim 2 analytic certificate → Claim 3
construction → Claim 4 compensation audit → Claim 5 projection geometry →
Claim 6 compatible split → evaluator-visible package → release audit. A Claim
2 exhaustive finite sibling was retained as correctly scoped BLOCKED
corroboration and was not promoted.

The scientific winning branch is
`orx/claim-6-compatible-recursive-split` at
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`. The evaluator-visible package
ran at `883ec79c9ad238a37bfbc5015acc65f37aec6ddd`; release-audit fixes were
reviewed from `362bdf129240ed0eb3df009905e982c12063d19c`. The final release
commit is reported after creation because a Git commit cannot contain its own
hash.

| Node / run | Result | Verifier runtime | Allocated compute | Cost |
|---|---|---:|---|---:|
| judged baseline / `1d3c37f0…` | 1 full, 5 toy | 0.029235 s | local, 1 Python thread | $0 |
| Claim 2 analytic / `e32a50a7…` | Claim 2 VERIFIED | 0.007180 s | local, 1 Python thread | $0 |
| Claim 2 exhaustive sibling / `dc4949e7…` | finite corroboration BLOCKED | 0.108574 s | local, 1 Python thread | $0 |
| Claim 3 / `b7ed9d7d…` | Claim 3 VERIFIED | 0.135315 s | local, 1 Python thread | $0 |
| Claim 4 / `f59f6939…` | broad wording FALSIFIED | 0.128624 s | local, 1 Python thread | $0 |
| Claim 5 first attempt / `259174c8…` | environmental code failure: missing import | — | local, 1 Python thread | $0 |
| Claim 5 fixed / `3593a899…` | Claim 5 VERIFIED | 0.146212 s | local, 1 Python thread | $0 |
| Claim 6 / `685055a4…` | cumulative 6/6, 0 toy | 0.294605 s | local, 1 Python thread | $0 |
| evaluator package / `0582e75c…` | cumulative 6/6, 0 toy | 0.219140 s | local, 1 Python thread | $0 |

All nine orchestrated runs occupied 5 seconds each: 45 seconds total, all on
local CPU with one Python thread. Hugging Face cpu-upgrade was not used because
every task was confidently below one core and five minutes. Total compute
cost: **$0**.

## Release gates

- Every claim is exactly VERIFIED or FALSIFIED; none is toy or vacuous.
- Claim 1 still passes in the cumulative regression suite.
- Every historical judge criticism is answered by visible implementation,
  proof/construction-level evidence, or the explicit Claim 4 falsification.
- The fixed command regenerates all raw numerical results and exits nonzero on
  failure.
- Independent checkers and negative controls pass.
- `logbook.json`, all raw JSON, strict marimo validation, and all SVG XML pass.
- The visibility matrix has no missing cells.
- Blind round 1 recorded four inaccessible items; all were fixed.
- Blind round 2 opened 83 reachable files and passed with no unverifiable
  conclusion.
- All 17 judged paths remain present. All 17 exact judged hashes also match the
  protected copy beneath `historical/judged-3d065680/`.
- Secret scanning reports zero credential-like paths.
- The exact [text upload allowlist](../../space/release/upload-allowlist.txt)
  contains 112 UTF-8 paths. The
  [SHA-256 manifest](../../space/release/upload-manifest.sha256) covers the
  other 111 files; as standard, the manifest excludes its own hash. Binary
  PNGs and cache metadata are not uploaded.

## Commands

The fixed experiment command, copied verbatim from every `orx exp status`, is:

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

Substantive orchestration and audit commands executed:

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 380a0684-e737-431b-aeeb-90b23f8d50cd
orx project view 380a0684-e737-431b-aeeb-90b23f8d50cd
orx project edit 380a0684-e737-431b-aeeb-90b23f8d50cd --run-command "uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all"
curl -L -A "OpenResearch-Reproduction/1.0" https://ar5iv.labs.arxiv.org/html/2509.06701v2
hf download DineshAI/sW8U2TYDMp --repo-type space --revision 3d065680c4492fdfc5e339a95f8287af6a533ec7
uv lock
uv sync --locked
orx exp run <experiment-id> --backend local
orx exp wait <experiment-id> --timeout 480
orx logs <run-id> --bytes 50000
marimo check --strict notebooks/latent_agentic_claims.py
.venv/bin/python -m reproduction.run_all
.venv/bin/python tools/audit_candidate.py <fresh-candidate>/space --historical-manifest <protected-manifest>
xmllint --noout reports/claim-reproduction/images/*.svg
rsvg-convert -o <preview.png> <figure.svg>
git diff --check
git push origin <experiment-branch>
```

Experiment creation used `orx create-experiment ... --parent <winner>` for
each named node. Routine read-only inspection (`git status`, `git rev-parse`,
`git branch -a`, `git ls-remote`, `find`, `rg`, `sed`, `df`, and environment
name enumeration) supported the startup and release audits.

## Publication action

After the final candidate manifest and fresh-copy audit pass, upload only the
allowlisted UTF-8/text files through the Hugging Face commit API to the
existing Space `DineshAI/sW8U2TYDMp`; do not create a second Space. Then
download the exact returned revision, verify every uploaded hash, repeat the
canonical traversal, mark the paper awaiting judge, and mirror the same
reader-facing files to GitHub `main`. The exact published Space revision and
remote Git SHA are recorded after those actions.
