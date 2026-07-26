# Release forecast and claim summary

- Previous live judged score: `7/12`
- Conservative projected score range after this change: **10–12/12**
- Best-supported possible new score: **12/12 (forecast, not a judge result)**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 2 | 2 | HIGH | VERIFIED | Already accepted; cumulative exact rerun and destructive control pass. |
| 2 | 1 | 2 | HIGH | VERIFIED | Universal symmetric-KL proof certificate is visible and independently checked; reviewer must accept the displayed derivation as proof-level evidence. |
| 3 | 1 | 2 | HIGH | VERIFIED | Paper construction is predeclared, full-support, positive, high-precision checked, and contrasted with binary and linear-pool controls. |
| 4 | 1 | 2 | MEDIUM | FALSIFIED | Exact counterexample satisfies the displayed theorem inequality while contradicting the broad judged wording; interpretation risk remains because the paper's conditional theorem itself is not falsified. |
| 5 | 1 | 2 | MEDIUM | VERIFIED | Exact Appendix span geometry and finite-tilt calibration pass; the short main-text wording may be read as a broader training-dynamics statement. |
| 6 | 1 | 2 | HIGH | VERIFIED | Explicit compatible child split preserves parent and global pool while one child becomes strictly worse. |

Current total score remains **7/12** until a live judge evaluates the new
revision. Claims 2–6 changed from historical toy evidence to current
proof/construction-level evidence. No claim is BLOCKED. The principal residual
risk is interpretation of the broad Claim 4 wording and Claim 5's
first-order scope.

Publication action after every release gate passes: upload the exact
UTF-8/text allowlist to the existing Space `DineshAI/sW8U2TYDMp` through the
Hugging Face commit API, verify the returned revision by fresh download, mark
the paper awaiting judge, and mirror the same reader-facing text to GitHub
`main`.
