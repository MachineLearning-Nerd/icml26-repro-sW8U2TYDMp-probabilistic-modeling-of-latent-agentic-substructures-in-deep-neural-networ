# Claim 1 execution environment

Command: `uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all`

Lock inputs: `pyproject.toml`, `uv.lock`; Python 3.12.11; seed 42.
Run `685055a4-365c-4743-b4d5-41957d21bc9d`, Git
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`.

Estimated one CPU core and under five minutes. Selected local CPU; HF
`cpu-upgrade` was not applicable. Actual Python threads: 1; verifier runtime:
0.294605 seconds; orchestrated duration: 5 seconds; cost: $0.
