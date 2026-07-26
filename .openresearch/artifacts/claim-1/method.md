# Claim 1 method

The public implementation is `reproduction/math_core.py`; the baseline check is `reproduction/verifier.py::claim1`. It uses one fixed three-outcome full-support distribution, evaluates every coordinate, verifies the entropy identity, and injects a destructive mutation that substitutes `P[o]` for `log(P[o])`.

Fixed command:

```bash
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

Expected compute: one CPU core, under five minutes, local backend.
