# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_90520c466e8c", "created_at": "2026-07-23T00:24:41+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
==============================================================================
CLAIM 3: strict unanimity ACHIEVABLE under log pooling for >=3 outcomes (Thm 9)
==============================================================================
  Found unanimous case: benefits = [np.float64(0.0021), np.float64(0.0041)]
  Agent 1: [0.107 0.868 0.025], Agent 2: [0.141 0.851 0.009]
  Pooled: [0.123 0.862 0.015]
  -> PASS (log pooling CAN achieve unanimity for 3 outcomes)

==============================================================================
CLAIM 4: Waluigi effect — manifesting B strengthens A (Theorem 19)
==============================================================================
  w_b: [np.float64(0.1), np.float64(0.2), np.float64(0.3), np.float64(0.4), np.float64(0.5), np.float64(0.6), np.float64(0.7), np.float64(0.8), np.float64(0.9)]
  w_a: [np.float64(0.315), np.float64(0.33), np.float64(0.345), np.float64(0.36), np.float64(0.375), np.float64(0.39), np.float64(0.405), np.float64(0.42), np.float64(0.435)] (monotone increasing: True)
  -> PASS

==============================================================================
CLAIM 5: manifest-then-suppress beats pure benevolence (Theorem 21)
==============================================================================
  final misalignment — pure: 0.822, shatter: 0.038
  -> PASS

==============================================================================
CLAIM 6: compositional benefit doesn't propagate to children (Theorem 14)
==============================================================================
  parent benefits: [0.5, 1.0, 2.0, 5.0]
  child benefits:  [0.075, 0.15, 0.3, 0.75]
  -> PASS (child < parent for all)

==============================================================================
VERDICT SUMMARY
==============================================================================
  [PASS] c1_log_score
  [PASS] c2_linear_impossible
  [PASS] c3_log_achievable
  [PASS] c4_waluigi
  [PASS] c5_shattering
  [PASS] c6_non_propagation

  6/6 claims verified.
  wrote outputs/verdict.json
```
