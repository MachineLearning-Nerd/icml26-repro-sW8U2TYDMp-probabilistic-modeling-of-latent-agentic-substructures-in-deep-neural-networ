# Claim 6 source audit

Section 4.1, Lemma 13 defines a compatible split and proves distributional
pooling invariance. Theorem 14 is existential: a parent may benefit while a
child in a compatible split is harmed. Appendix G, Lemma 44 and Theorem 46
give the construction.

Choose a nonuniform full-support `P1`, `t>1`,
`P2 proportional to P1^(2t-1)`, and equal parent weights. Their log pool is
`Pt proportional to P1^t`; monotonicity of the power-family log partition
gives `Delta_P1(Pt)>0`.

For `alpha in (0,1)` and any tilt `g`, set

```text
log P11 = log P1 + (1-alpha)g - c1
log P12 = log P1 - alpha g - c2.
```

The relative child log pool reconstructs `P1`, so child global weights
`alpha*beta1` and `(1-alpha)*beta1` preserve the original pool. A large
negative single-outcome tilt sends `KL(Pt||P11)` to infinity while child
entropy remains bounded, forcing its welfare gap to negative infinity.

Source: arXiv:2509.06701v2, archived SHA-256
`013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.
