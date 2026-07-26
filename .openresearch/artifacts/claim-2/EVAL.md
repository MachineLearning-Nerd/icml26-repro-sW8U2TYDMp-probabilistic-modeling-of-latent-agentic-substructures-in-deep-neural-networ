# Claim 2 evaluation contract

Run the fixed project command:

`uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all`

The process exits nonzero unless:

- the direct and entropy/KL gap definitions agree;
- the weighted-gap certificate agrees numerically;
- every distinct fixture has a strictly negative weighted gap;
- both negative controls are detected; and
- the cumulative Claim 1 regression still passes.

Verdict: `VERIFIED` only when every condition passes. The fixture sweep is
explicitly not presented as exhaustive evidence for the universal theorem.
