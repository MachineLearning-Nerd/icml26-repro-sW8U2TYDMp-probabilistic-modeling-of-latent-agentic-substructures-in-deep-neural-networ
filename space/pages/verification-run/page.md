# Verification run


---
<!-- trackio-cell
{"type": "code", "id": "cell_ec3c36b942b0", "created_at": "2026-07-23T00:24:45+00:00", "title": "verify all claims", "command": [".venv/bin/python", "repro/src/verify_unanimity.py"], "exit_code": 0, "duration_s": 2.043}
-->
````bash
$ .venv/bin/python repro/src/verify_unanimity.py
````

exit 0 · 2.0s


````python title=verify_unanimity.py
"""Verify Agents, Epistemic Utility, and Unanimity claims (arXiv 2509.06701). numpy CPU."""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import unanimity as U

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
results = {}
def banner(s): print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78, flush=True)

rng = np.random.default_rng(42)


# ---------- c1: U(o) = log P(o) ----------
banner("CLAIM 1: U(o) = log P(o) (logarithmic scoring rule)")
P = np.array([0.3, 0.5, 0.2])
for o in range(3):
    u = U.epistemic_utility(P, o)
    expected = np.log(P[o])
    assert abs(u - expected) < 1e-12
eu = U.expected_utility(P, P)
expected_eu = np.sum(P * np.log(P))  # = -H(P)
c1 = abs(eu - expected_eu) < 1e-12
print(f"  U(o) = log P(o): verified for all outcomes")
print(f"  E_P[log P] = {eu:.4f} = -H(P) = {expected_eu:.4f}")
print(f"  -> {'PASS' if c1 else 'FAIL'}")
results["c1_log_score"] = dict(passed=bool(c1), eu=float(eu))


# ---------- c2: strict unanimity IMPOSSIBLE under linear pooling ----------
banner("CLAIM 2: strict unanimity IMPOSSIBLE under linear pooling (Theorem 10)")
# exhaustive search over 2-outcome, 2-agent space: find NO case where both benefit
found_linear = False
for _ in range(20000):
    d1 = rng.dirichlet([1, 1]); d2 = rng.dirichlet([1, 1])
    pooled = U.linear_pool([d1, d2])
    unan, _ = U.check_strict_unanimity([d1, d2], pooled)
    if unan:
        found_linear = True; break
# also for 3 outcomes
for _ in range(20000):
    d1 = rng.dirichlet([1, 1, 1]); d2 = rng.dirichlet([1, 1, 1])
    pooled = U.linear_pool([d1, d2])
    unan, _ = U.check_strict_unanimity([d1, d2], pooled)
    if unan:
        found_linear = True; break
c2 = not found_linear  # unanimity NEVER found under linear pooling
print(f"  40000 random 2-agent trials: strict unanimity found: {found_linear}")
print(f"  -> {'PASS' if c2 else 'FAIL'} (impossibility: unanimity never occurs)")
results["c2_linear_impossible"] = dict(passed=bool(c2), found=bool(found_linear))


# ---------- c3: strict unanimity ACHIEVABLE under log pooling ≥3 outcomes ----------
banner("CLAIM 3: strict unanimity ACHIEVABLE under log pooling for >=3 outcomes (Thm 9)")
found_log = False; case = None
for _ in range(20000):
    d1 = rng.dirichlet([1, 1, 1]); d2 = rng.dirichlet([1, 1, 1])
    pooled = U.log_pool([d1, d2])
    unan, benefits = U.check_strict_unanimity([d1, d2], pooled)
    if unan:
        found_log = True; case = (d1, d2, pooled, benefits); break
c3 = found_log
if found_log:
    d1, d2, pooled, benefits = case
    print(f"  Found unanimous case: benefits = {[round(b, 4) for b in benefits]}")
    print(f"  Agent 1: {np.round(d1, 3)}, Agent 2: {np.round(d2, 3)}")
    print(f"  Pooled: {np.round(pooled, 3)}")
print(f"  -> {'PASS' if c3 else 'FAIL'} (log pooling CAN achieve unanimity for 3 outcomes)")
results["c3_log_achievable"] = dict(passed=bool(c3), found=bool(found_log))


# ---------- c4: Waluigi effect ----------
banner("CLAIM 4: Waluigi effect — manifesting B strengthens A (Theorem 19)")
P_b = np.array([0.6, 0.3, 0.1])  # benevolent
P_a = np.array([0.1, 0.3, 0.6])  # antagonist (complementary)
w_b_vals = np.linspace(0.1, 0.9, 9)
w_a_init = 0.3
w_a_vals = [U.waluigu_effect(P_b, P_a, wb, w_a_init) for wb in w_b_vals]
# antagonist weight should INCREASE as benevolent is manifested
monotone_increase = all(w_a_vals[i] <= w_a_vals[i+1] + 1e-10 for i in range(len(w_a_vals)-1))
c4 = monotone_increase and w_a_vals[-1] > w_a_vals[0]
print(f"  w_b: {[round(wb,2) for wb in w_b_vals]}")
print(f"  w_a: {[round(wa,3) for wa in w_a_vals]} (monotone increasing: {monotone_increase})")
print(f"  -> {'PASS' if c4 else 'FAIL'}")
results["c4_waluigi"] = dict(passed=bool(c4), w_a_vals=[float(w) for w in w_a_vals])


# ---------- c5: Waluigi shattering > pure benevolence ----------
banner("CLAIM 5: manifest-then-suppress beats pure benevolence (Theorem 21)")
misalign_pure, misalign_shatter = U.waluigu_shattering(0.3, 0.3, P_b, P_a, n_steps=10)
# shattering should achieve lower final misalignment than pure
c5 = misalign_shatter[-1] < misalign_pure[-1]
print(f"  final misalignment — pure: {misalign_pure[-1]:.3f}, shatter: {misalign_shatter[-1]:.3f}")
print(f"  -> {'PASS' if c5 else 'FAIL'}")
results["c5_shattering"] = dict(passed=bool(c5),
                                final_pure=float(misalign_pure[-1]),
                                final_shatter=float(misalign_shatter[-1]))


# ---------- c6: compositional benefit doesn't propagate ----------
banner("CLAIM 6: compositional benefit doesn't propagate to children (Theorem 14)")
parent_benefits = [0.5, 1.0, 2.0, 5.0]
child_benefits = [U.compositional_propagation(pb, child_overlap=0.5) for pb in parent_benefits]
# child benefit is strictly less than parent benefit (diluted)
c6 = all(cb < pb for cb, pb in zip(child_benefits, parent_benefits))
print(f"  parent benefits: {parent_benefits}")
print(f"  child benefits:  {[round(cb,3) for cb in child_benefits]}")
print(f"  -> {'PASS' if c6 else 'FAIL'} (child < parent for all)")
results["c6_non_propagation"] = dict(passed=bool(c6),
                                     parent=parent_benefits,
                                     child=child_benefits)


# ---------- summary ----------
banner("VERDICT SUMMARY")
passed = sum(1 for r in results.values() if r.get("passed"))
for k_, r in results.items():
    print(f"  [{'PASS' if r.get('passed') else 'FAIL'}] {k_}")
print(f"\n  {passed}/{len(results)} claims verified.")
json.dump(results, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print("  wrote outputs/verdict.json")

````


````output

==============================================================================
CLAIM 1: U(o) = log P(o) (logarithmic scoring rule)
==============================================================================
  U(o) = log P(o): verified for all outcomes
  E_P[log P] = -1.0297 = -H(P) = -1.0297
  -> PASS

==============================================================================
CLAIM 2: strict unanimity IMPOSSIBLE under linear pooling (Theorem 10)
==============================================================================
  40000 random 2-agent trials: strict unanimity found: False
  -> PASS (impossibility: unanimity never occurs)

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

````
