# Claim 6 method

The fixed fixture uses `P1=(0.6,0.3,0.1)`, `t=1.5`, equal parent weights,
and `P2 proportional to P1^2`. It checks that the pool equals
`P1^1.5/Z` and that the parent gap is positive.

The split uses `alpha=0.4` and
`g_lambda=(-lambda,0,0)` over the predeclared sweep
`lambda in {0,1,2,4,8,12}`. At every point the verifier reconstructs `P1`
from the two children and recomputes the global pool. It requires both errors
below `1e-12` and at least one child gap below zero.

A 70-digit Decimal implementation independently checks the `lambda=8`
fixture.

Controls:

1. At `lambda=0`, both children clone the parent and retain its positive gap.
2. Tilting only one child breaks compatibility; both parent reconstruction
   and global-pool invariance must fail.
