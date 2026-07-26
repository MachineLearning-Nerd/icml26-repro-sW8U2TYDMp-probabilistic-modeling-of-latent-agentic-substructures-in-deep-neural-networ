# Claim 5 source audit

The main statement is Section 5.1, Theorem 21. Its strictness conditions are
made explicit in Appendix J: Proposition 72 and Corollary 74 require a novel
component `u=w-Proj_S0(w) != 0` and nonzero event correlation
`<g_A,u>_P != 0`. Theorem 75 repeats those conditions.

Lemma 71 states that the optimal first-order reduction under a norm budget is
`epsilon ||Proj_S(g_A)||_P`. Proposition 72 gives the Pythagorean identity

`||Proj_S1(g_A)||_P^2 = ||Proj_S0(g_A)||_P^2
+ <g_A,u>_P^2 / ||u||_P^2`.

Those identities directly imply the strict comparison. Source:
arXiv:2509.06701v2, archived SHA-256
`013a579947622a09d4375d4d4d4cb18aa8c61728ed3070c83f084c40140f0282`.

The compact equality for the *difference* printed in Appendix Theorem 75 is
not the general difference-of-projection-norms identity when the baseline
projection is nonzero. This reproduction verifies the strict inequality
through Lemma 71 and Proposition 72 and reports that source-formula caveat.
