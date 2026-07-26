# Claim 2 method

Let `P = sum_i beta_i P_i` and
`Delta_i = E_P[log P_i] - E_Pi[log P_i]`. Direct expansion gives

`Delta_i = H(P_i) - H(P) - KL(P || P_i)`.

The weighted Jensen gap has the exact KL form

`H(P) - sum_i beta_i H(P_i) = sum_i beta_i KL(P_i || P)`.

Combining them produces the certificate

`sum_i beta_i Delta_i =
-sum_i beta_i [KL(P_i || P) + KL(P || P_i)]`.

Gibbs' inequality makes every term nonnegative. Positive weights and any
non-identical agent make the forward sum strictly positive, so the weighted
gap is strictly negative. If every gap were nonnegative, its positive-weighted
sum would be nonnegative, a contradiction.

The verifier independently evaluates gaps from expectations and from the
entropy/KL identity. It checks four deterministic fixtures spanning two to
four agents and two to five outcomes. These fixtures are implementation
audits, not the basis for the universal conclusion.

Negative controls:

1. Delete the reverse-KL term from the certificate. The checker must reject it.
2. Make all agents identical. Strictness must disappear while strict benefit
   remains impossible.
