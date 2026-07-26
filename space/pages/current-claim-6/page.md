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

## Supervised cumulative evidence

The parent gap was `0.1289745781560655`. Child-one gaps over
`lambda={0,1,2,4,8,12}` were
`{0.128975, 0.121525, -0.062208, -0.807044, -2.620105, -4.348108}`: the
first negative appeared at `lambda=2`. Maximum parent-reconstruction error
was `1.1102230246251565e-16`; maximum global-pool shift was
`5.551115123125783e-17`. The independent 70-digit checker found both
invariants within `2E-70`. The clone stayed positive and the incompatible
one-sided tilt moved the parent (`0.4197323`) and pool (`0.2274891`).

The cumulative run used Git SHA
`c2b9aefefc290d44097b4bdd18d5e8e7cf707ba4`, seed `42`, one local CPU
thread, `0.2946048330049962` verifier seconds, 5 orchestrated seconds, and
`$0`. Download [raw output](../../evidence/claim-6/raw.json),
[checker](../../evidence/claim-6/checker.json),
[controls](../../evidence/claim-6/negative_control.json),
[contract](../../evidence/claim-6/claim_contract.json),
[environment](../../evidence/claim-6/environment.md), and
[limitations](../../evidence/claim-6/limitations.md).

This verifies an existential compatible-split counterexample. It does not
assert that every recursive split harms a child.
