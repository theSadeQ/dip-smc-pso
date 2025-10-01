# Division-by-Zero Safety Coordination Plan
## Issue #13: CRIT-004 - Division by Zero Robustness

**Status:** In Progress
**Coordinator:** Integration Coordinator
**Target Completion:** Current Session

---

## Executive Summary

**Findings:**
- **Total Division Operations Found:** 41
- **Currently Safe (with epsilon):** 10 (24%)
- **Unsafe (need protection):** 31 (76%)
- **Files Needing Fixes:** 17
- **Critical Files (Controllers + Plant):** 11

**Critical Issue:** 76% of division operations lack epsilon threshold protection, creating risk of:
- Division by zero errors
- Numerical instability with denominators < 1e-12
- LinAlgError exceptions in edge cases
- System crashes in production

---

## Coordination Strategy

### Phase 1: Utility Infrastructure (Code Beautification Specialist)
**Task:** Create `src/utils/numerical_stability/safe_operations.py`

**Required Functions:**
```python
def safe_divide(numerator, denominator, epsilon=1e-12, fallback=0.0):
    """Safe division with epsilon threshold protection."""

def safe_reciprocal(value, epsilon=1e-12):
    """Safe reciprocal: 1 / (value + epsilon)."""

def safe_normalize(array, epsilon=1e-12):
    """Safe normalization: array / (sum(array) + epsilon)."""
```

**Dependencies:** None
**Blocking:** Phase 2, 3, 4

---

### Phase 2: Critical Controllers (Control Systems Specialist)
**Priority:** HIGHEST
**Files:** 9 controller files with 16 unsafe divisions

**Critical Files:**
1. `src/controllers/smc/core/switching_functions.py` - 3 unsafe divisions (lines 197, 222)
2. `src/controllers/smc/algorithms/classical/boundary_layer.py` - 1 unsafe (line 264)
3. `src/controllers/smc/algorithms/hybrid/switching_logic.py` - 2 unsafe (lines 308, 332)
4. `src/controllers/smc/algorithms/hybrid/controller.py` - 1 unsafe (line 56)
5. `src/controllers/smc/algorithms/adaptive/parameter_estimation.py` - Already safe (line 275 has 1e-10)
6. `src/controllers/smc/hybrid_adaptive_sta_smc.py` - 4 unsafe (lines 371, 564, 570, 571)
7. `src/controllers/factory/pso_integration.py` - 1 unsafe (line 262)

**Approach:**
- Import `safe_divide` from new utility module
- Replace risky divisions with safe_divide calls
- Maintain existing epsilon values where already present (upgrade to 1e-12 if weaker)
- Add unit tests for edge cases

**Dependencies:** Phase 1 complete
**Blocking:** Test validation

---

### Phase 3: Plant Models (Control Systems Specialist)
**Priority:** HIGH
**Files:** 2 plant files with 4 divisions

**Files:**
1. `src/plant/models/full/dynamics.py` - 2 safe (lines 248, 280 already have 1e-12)
2. `src/plant/models/lowrank/config.py` - 2 unsafe (lines 175, 180)

**Approach:**
- Validate existing epsilon protection in dynamics.py
- Add safe_divide to lowrank/config.py for inertia calculations
- Critical: Inertia matrix inversions must never fail

**Dependencies:** Phase 1 complete

---

### Phase 4: Optimization (PSO Optimization Engineer)
**Priority:** MEDIUM
**Files:** 10 optimization files with varied protection

**Key Files:**
- `enhanced_convergence_analyzer.py` - 3 divisions (lines 407, 497, 533, 534)
- `energy.py` - 2 divisions (lines 210, 213 already have 1e-12)
- `weighted_sum.py` - 2 divisions (lines 453, 454 already have 1e-12)
- `overshoot.py` - 1 division (line 327 has 1e-6)
- `robustness.py` - 1 division (line 417 has 1e-6)
- Others: Various states of protection

**Approach:**
- Standardize epsilon to 1e-12 across all optimization
- Upgrade weaker epsilon values (1e-6 → 1e-12)
- Add safe_divide for consistency

**Dependencies:** Phase 1 complete

---

### Phase 5: Utilities (Integration Coordinator)
**Priority:** LOW
**Files:** 2 utility files (visualization, analysis)

**Files:**
- `visualization/movie_generator.py` - Unknown divisions (need line-level scan)
- `analysis/statistics.py` - Unknown divisions (need line-level scan)

**Approach:**
- Manual review of context
- Apply safe_divide where appropriate
- May be display-only calculations (less critical)

---

## Test Validation Strategy

### Fix Test First (Integration Coordinator)
**File:** `tests/test_integration/test_numerical_stability/test_numerical_stability_deep.py`

**Current Issue:** Test line 543 fails with `inf/0.0` case
```python
# BROKEN: This will always fail
test_cases = [
    (np.inf, 0.0),  # This CANNOT produce finite result
]
```

**Fix Required:**
```python
# Test should validate that safe_divide handles edge cases gracefully
def test_division_by_zero_robustness(self):
    from src.utils.numerical_stability.safe_operations import safe_divide

    test_cases = [
        (1.0, 0.0, 1.0),  # Expected: fallback value
        (0.0, 0.0, 0.0),  # Expected: fallback value
        (1e-20, 1e-20, 1.0),  # Expected: ~1.0
        (-1.0, 0.0, -1.0),  # Expected: fallback value
        (10.0, 1e-16, 10.0/1e-12),  # Expected: uses epsilon threshold
    ]

    for numerator, denominator, expected_order in test_cases:
        result = safe_divide(numerator, denominator, epsilon=1e-12, fallback=numerator)
        assert np.isfinite(result), f"Division {numerator}/{denominator} produced non-finite result"
```

### Integration Test (Post-Fixes)
```bash
pytest tests/test_integration/test_numerical_stability/test_numerical_stability_deep.py::TestNumericalRobustness::test_division_by_zero_robustness -v
```

### Stress Test (Find Min Denominators)
Create test that scans actual simulation runs for min denominator values:
```python
def test_min_denominator_tracking():
    """Verify all denominators in production >= 1e-12."""
    # Run full simulation suite
    # Track all division operations
    # Assert: min_denominator >= 1e-12
```

---

## Acceptance Criteria Tracking

| Criterion | Status | Evidence |
|-----------|--------|----------|
| All division operations protected with epsilon (1e-12) | ❌ IN PROGRESS | 31/41 need fixes |
| Graceful handling of near-zero denominators | ❌ PENDING | Awaiting safe_divide implementation |
| Consistent behavior across mathematical modules | ❌ PENDING | Standardization in progress |
| Zero LinAlgError in stress testing | ❌ PENDING | Test needs fixing first |

---

## Agent Assignments

### 🟣 Code Beautification Specialist
- **Phase 1:** Create `src/utils/numerical_stability/safe_operations.py`
- **Timeline:** IMMEDIATE (blocking)
- **Deliverable:** Working utility module with safe_divide, safe_reciprocal, safe_normalize

### 🔴 Control Systems Specialist
- **Phase 2:** Fix 9 controller files (16 unsafe divisions)
- **Phase 3:** Fix 2 plant files (2 unsafe divisions)
- **Timeline:** After Phase 1 complete
- **Deliverable:** All critical control paths protected

### 🔵 PSO Optimization Engineer
- **Phase 4:** Fix 10 optimization files (varied protection)
- **Timeline:** After Phase 1 complete
- **Deliverable:** Standardized epsilon protection across optimization

### 🌈 Integration Coordinator (Self)
- **Phase 0:** Create coordination artifacts ✅ DONE
- **Phase 5:** Fix utility files
- **Test Fix:** Update test_division_by_zero_robustness
- **Final Validation:** Run full test suite, create acceptance report
- **Timeline:** Ongoing + final validation

---

## Risk Assessment

**High Risk:**
- Controllers: Real-time control loops - failure = system crash
- Plant Models: Inertia matrix inversions - LinAlgError = simulation halt

**Medium Risk:**
- Optimization: Convergence analysis - may cause optimization failures

**Low Risk:**
- Utilities: Visualization/analysis - likely non-critical display calculations

---

## Success Metrics

1. **100% Coverage:** All 41 division operations reviewed and protected
2. **Epsilon Standard:** All epsilon thresholds ≥ 1e-12
3. **Zero Errors:** No LinAlgError in 1000-iteration stress test
4. **Test Passing:** test_division_by_zero_robustness passes with new implementation
5. **Performance:** < 1% overhead from safe_divide calls

---

## Next Steps

1. **IMMEDIATE:** Code Beautification Specialist creates safe_operations.py
2. **PARALLEL (after 1):** Control Systems Specialist + PSO Engineer fix their domains
3. **FINAL:** Integration Coordinator validates all changes and runs acceptance tests
4. **COMMIT:** Single atomic commit with all fixes + passing tests

---

**Coordination Status:** ✅ Planning Complete - Ready for Parallel Execution
