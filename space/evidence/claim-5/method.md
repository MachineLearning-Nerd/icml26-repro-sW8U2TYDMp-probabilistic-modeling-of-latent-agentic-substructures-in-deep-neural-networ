# Claim 5 method

Use a uniform four-outcome base, event `A={0}`, and centered directions

```text
g_A = ( 0.75,-0.25,-0.25,-0.25)
H   = (-1, 1,-1, 1)
w   = ( 3,-1,-1,-1)
```

The baseline span is `S0=span(H)`. The Waluigi novelty is
`u=w-Proj_S0(w)=(2,0,-2,0)`, which has nonzero norm and nonzero correlation
with `g_A`. An explicit weighted Gram solve computes both projections. The
verifier constructs the Cauchy–Schwarz optimizers, checks their budgets and
objectives, and checks Proposition 72's squared-norm identity.

An independent 70-digit Decimal calculation reconstructs the geometry.
Finite exponential tilts at four decreasing budgets confirm that actual event
reduction approaches the first-order prediction.

Controls:

1. `w=2H` lies inside `S0`, so novelty and strict gain vanish.
2. A nonzero novelty orthogonal to `g_A` adds a direction but no suppression
   leverage, so strict gain again vanishes.
