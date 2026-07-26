# Evaluator-blind review — round 1

Candidate source: clean `git archive` of commit
`883ec79c9ad238a37bfbc5015acc65f37aec6ddd`, restricted to `space/`.
The review started at `logbook.json` and `pages/index.md` and used only
declared navigation and reachable local links.

Machine record: [red-team-round1.json](red-team-round1.json). It records all
66 files opened, claim conclusions, JSON validation, missing links, historical
subset checks, and secret-pattern results.

## Conclusions

- Every declared page and reachable local artifact existed.
- Five claims were discoverable as VERIFIED and Claim 4 as FALSIFIED.
- All 27 non-cache JSON files parsed.
- No token, cloud-key, or private-key pattern was detected.
- All 17 judged paths remained present at the candidate root.
- An exact hash-matched copy of all 17 judged files existed beneath
  `historical/judged-3d065680/`.

## Could not verify directly

1. `reproduction/run_all.py` was named but not a clickable reachable file.
2. Per-claim `method.md` and `EVAL.md` records were present but not directly
   linked from the canonical traversal.
3. Claims 3–6 source-audit files were present but not directly linked.
4. Claim 1's raw link exposed the immutable historical record rather than the
   current cumulative rerun.

All four findings are treated as missing evaluator evidence and are fixed in
the release-audit child before round 2.
