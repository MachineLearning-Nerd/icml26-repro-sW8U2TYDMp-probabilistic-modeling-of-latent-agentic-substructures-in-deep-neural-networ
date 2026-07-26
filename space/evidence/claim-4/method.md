# Claim 4 method

Use a uniform three-outcome base pool and centered profiles

```text
v_H = ( 1, -1, 0)
v_A = ( 1, -1, 0)   aligned duplicate
v_W = (-1,  1, 0)   unique anti-aligned component
```

Each profile corresponds to a full-support agent through softmax. Base weights
`(0.25,0.25,0.50)` pool to the uniform distribution. Perturb them by
`(+0.05,-0.05,0)`: Luigi increases, the aligned duplicate decreases, Waluigi
does not change, and the pooled distribution remains exactly uniform. Thus
the logit deviation is zero and every general stability assumption is met.

Theorem 19's inequality still holds: its positive Luigi term is cancelled by
the aligned-downweight term. Removing that term is the negative-control
mutation and makes the inequality falsely reject the valid counterexample.
A separate 70-digit Decimal implementation reconstructs the distributions,
pools, profiles, and both sides.
