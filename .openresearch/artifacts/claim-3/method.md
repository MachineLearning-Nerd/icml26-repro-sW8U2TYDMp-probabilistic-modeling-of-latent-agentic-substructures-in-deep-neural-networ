# Claim 3 method

For arbitrary nondegenerate weights, the raw log-pool mass on private outcome
`o_i` is `epsilon^c_i`, where
`c_i=(n+1)-n*beta_i>1`. The normalized pool therefore concentrates on the
shared outcome more rapidly than an individual belief as `epsilon -> 0`.

The proof obligations are:

- `H(P_i)=Theta(epsilon log(1/epsilon))`;
- `H(P)=o(epsilon log(1/epsilon))`;
- `KL(P||P_i)=O(epsilon)`; hence
- `Delta_i/(epsilon log(1/epsilon)) -> 1`.

The executable fixtures use one fixed `epsilon=1e-5`, four predeclared weight
vectors, and no parameter search. The two-agent fixture is a direct
three-outcome witness. A separate 70-digit Decimal implementation recomputes
that witness without importing the production probability primitives.

Controls replace the named logarithmic pool with a linear pool and audit the
binary boundary. In the binary case
`Delta_i=(q-p_i)logit(p_i)`, whereas `logit(q)` is a convex combination of
agent logits. An extreme same-side belief cannot improve; mixed-side
requirements point in incompatible directions.
