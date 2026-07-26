# Current verification: Claim 6

**Verdict contract: VERIFIED** only with a full-support parent that strictly
benefits, an exact compatible child split that preserves the global pool, and
a child with a strictly negative welfare gap.

## Exact construction

Section 4.1, Theorem 14 is existential. Appendix G, Theorem 46 starts from a
nonuniform `P1` and `t>1`, defines

```text
P2 proportional to P1^(2t-1),
Pt proportional to P1^t,
```

and pools `P1,P2` with equal weights. The power-family log-partition has
second derivative `Var_Pt(log P1)>0`, so `Delta_P1(Pt)>0`.

For `alpha in (0,1)` split the parent by

```text
log P11 = log P1 + (1-alpha)g - c1
log P12 = log P1 - alpha*g - c2.
```

Then `alpha log P11+(1-alpha)log P12` equals `log P1` up to a constant.
With global child weights `alpha*beta1` and `(1-alpha)*beta1`, the global log
pool is unchanged.

Choose `g_lambda=(-lambda,0,0)`. As `lambda` grows,
`P11(0)->0` while `Pt(0)>0`; therefore `KL(Pt||P11)->infinity`.
Since child entropy is bounded by `log|O|`,
`Delta_P11(Pt)->-infinity`.

Source: Section 4.1, Lemma 13 and Theorem 14; Appendix G, Lemma 44 and
Theorem 46 in arXiv:2509.06701v2. Archived SHA-256:
`013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

## Executable audit

The fixture uses `P1=(0.6,0.3,0.1)`, `t=1.5`, `alpha=0.4`, and the fixed
sweep `lambda={0,1,2,4,8,12}`. The visible verifier is
`reproduction/verifier.py::claim6`; a separate 70-digit implementation is
`reproduction/independent_checker.py::claim6_decimal_split`.

Fixed command:

```text
uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
```

At every sweep point the checker recomputes parent reconstruction and global
pool invariance. The clone control at `lambda=0` must keep both child gaps
positive. A one-sided tilt is deliberately incompatible and must move both
the reconstructed parent and global pool.

This verifies an existential compatible-split counterexample. It does not
assert that every recursive split harms a child. Exact supervised output and
raw JSON will be attached before release.
