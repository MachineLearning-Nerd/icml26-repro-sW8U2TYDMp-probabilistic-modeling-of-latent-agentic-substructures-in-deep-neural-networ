# Evaluator visibility matrix

This audit starts from [the canonical page](#/index) and uses only reachable
candidate files. Every claim page contains the exact statement, assumptions,
quantifiers, numerical results, command, commit, seed, CPU/runtime record, and
limitations. Every raw link below is downloadable.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | [Claim 1](#/current-claim-1) | [verifier](../../reproduction/verifier.py), [core](../../reproduction/math_core.py) | yes | [raw](../../evidence/claim-1/raw.json) | [output](../../evidence/claim-1/checker.json) | [mutation](../../evidence/claim-1/negative_control.json) | [contract](../../evidence/claim-1/claim_contract.json) | VERIFIED |
| 2 | [Claim 2](#/current-claim-2) | [verifier](../../reproduction/verifier.py), [checker source](../../reproduction/independent_checker.py) | yes | [raw](../../evidence/claim-2/raw.json) | [output](../../evidence/claim-2/checker.json) | [mutations](../../evidence/claim-2/negative_control.json) | [contract](../../evidence/claim-2/claim_contract.json) | VERIFIED |
| 3 | [Claim 3](#/current-claim-3) | [verifier](../../reproduction/verifier.py), [checker source](../../reproduction/independent_checker.py) | yes | [raw](../../evidence/claim-3/raw.json) | [output](../../evidence/claim-3/checker.json) | [wrong pool/binary](../../evidence/claim-3/negative_control.json) | [contract](../../evidence/claim-3/claim_contract.json) | VERIFIED |
| 4 | [Claim 4](#/current-claim-4) | [verifier](../../reproduction/verifier.py), [checker source](../../reproduction/independent_checker.py) | yes | [raw](../../evidence/claim-4/raw.json) | [output](../../evidence/claim-4/checker.json) | [missing-term mutation](../../evidence/claim-4/negative_control.json) | [contract](../../evidence/claim-4/claim_contract.json) | FALSIFIED |
| 5 | [Claim 5](#/current-claim-5) | [verifier](../../reproduction/verifier.py), [projection core](../../reproduction/math_core.py) | yes | [raw](../../evidence/claim-5/raw.json) | [output](../../evidence/claim-5/checker.json) | [two controls](../../evidence/claim-5/negative_control.json) | [contract](../../evidence/claim-5/claim_contract.json) | VERIFIED |
| 6 | [Claim 6](#/current-claim-6) | [verifier](../../reproduction/verifier.py), [checker source](../../reproduction/independent_checker.py) | yes | [raw](../../evidence/claim-6/raw.json) | [output](../../evidence/claim-6/checker.json) | [clone/incompatible split](../../evidence/claim-6/negative_control.json) | [contract](../../evidence/claim-6/claim_contract.json) | VERIFIED |

Per-claim [source audits](../../evidence/claim-2/source_audit.md), methods,
environment records, `EVAL.md` files, and limitations live beside each linked
raw file. The pinned environment is
[`pyproject.toml`](../../pyproject.toml) plus [`uv.lock`](../../uv.lock).

Direct evidence-bundle links:

- Claim 1: [source](../../evidence/claim-1/source_audit.md),
  [method](../../evidence/claim-1/method.md),
  [EVAL](../../evidence/claim-1/EVAL.md),
  [limitations](../../evidence/claim-1/limitations.md).
- Claim 2: [source](../../evidence/claim-2/source_audit.md),
  [method](../../evidence/claim-2/method.md),
  [EVAL](../../evidence/claim-2/EVAL.md),
  [limitations](../../evidence/claim-2/limitations.md).
- Claim 3: [source](../../evidence/claim-3/source_audit.md),
  [method](../../evidence/claim-3/method.md),
  [EVAL](../../evidence/claim-3/EVAL.md),
  [limitations](../../evidence/claim-3/limitations.md).
- Claim 4: [source](../../evidence/claim-4/source_audit.md),
  [method](../../evidence/claim-4/method.md),
  [EVAL](../../evidence/claim-4/EVAL.md),
  [limitations](../../evidence/claim-4/limitations.md).
- Claim 5: [source](../../evidence/claim-5/source_audit.md),
  [method](../../evidence/claim-5/method.md),
  [EVAL](../../evidence/claim-5/EVAL.md),
  [limitations](../../evidence/claim-5/limitations.md).
- Claim 6: [source](../../evidence/claim-6/source_audit.md),
  [method](../../evidence/claim-6/method.md),
  [EVAL](../../evidence/claim-6/EVAL.md),
  [limitations](../../evidence/claim-6/limitations.md).

The current verifier is
[`reproduction/run_all.py`](../../reproduction/run_all.py); the combined verifier on
the page titled **Historical rejected baseline** is preserved evidence, not
the current verification.
