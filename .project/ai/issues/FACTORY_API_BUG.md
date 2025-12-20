# Factory API Inconsistency - Production Blocking Bug

**Issue ID**: FACTORY-001
**Severity**: CRITICAL (blocks production deployment)
**Status**: OPEN
**Discovered**: December 20, 2025 (Week 3 Session 3)
**Discovered By**: Integration tests with real config.yaml

---

## Summary

Factory `create_controller()` passes `gains` as a keyword argument to controller constructors, but modular controllers expect `gains` to be in `config.gains` (not as a separate parameter). This causes 4 out of 5 controllers to fail initialization with `TypeError`.

**Impact**: Only 1/5 controllers (hybrid_adaptive_sta_smc) works correctly. System cannot create most controllers.

---

## Evidence

### Test Results

From `tests/test_integration/test_factory_integration.py::TestFactoryControllerCreation::test_create_controller_from_config`:

```
❌ classical_smc: TypeError: ModularClassicalSMC.__init__() got an unexpected keyword argument 'gains'
❌ sta_smc: TypeError: ModularSuperTwistingSMC.__init__() missing 1 required positional argument: 'config'
❌ adaptive_smc: TypeError (similar to classical_smc)
✅ hybrid_adaptive_sta_smc: PASSED (only working controller)
❌ swing_up_smc: TypeError (API mismatch)
```

**Pass Rate**: 1/5 (20%)

### Error Details

**classical_smc failure**:
```python
# Factory code (src/controllers/factory/base.py:656)
controller_params = {
    'gains': [23.068, 12.853, ...],  # Passed as keyword arg
    'boundary_layer': 0.3,
    'dynamics_model': <DIPDynamics>,
    # ...
}
controller = controller_class(**controller_params)  # FAILS HERE

# ModularClassicalSMC signature (expected)
class ModularClassicalSMC:
    def __init__(self, config, dynamics_model, **kwargs):
        # Expects config.gains, NOT gains as separate kwarg
```

**sta_smc failure**:
```python
# Factory tries to pass individual params, but STA-SMC expects config object
TypeError: ModularSuperTwistingSMC.__init__() missing 1 required positional argument: 'config'
```

---

## Root Cause

**Inconsistent controller initialization patterns**:

1. **Factory assumption**: Controllers accept `gains` as keyword argument
2. **Modular controller reality**: Controllers expect `config` object with `config.gains`
3. **Exception**: `hybrid_adaptive_sta_smc` happens to accept both patterns (why it passes)

**Location**: `src/controllers/factory/base.py:656`

```python
# PROBLEMATIC CODE
controller = controller_class(**controller_params)  # Line 656
```

---

## Reproduction Steps

1. Clone repository
2. Run integration tests:
   ```bash
   python -m pytest tests/test_integration/test_factory_integration.py::TestFactoryControllerCreation::test_create_controller_from_config -v
   ```
3. Observe 4/5 controllers failing with TypeError

**Expected**: All 5 controllers should initialize successfully
**Actual**: Only hybrid_adaptive_sta_smc works

---

## Proposed Fix Options

### Option 1: Config-Driven (RECOMMENDED)

**Change factory to pass config object instead of individual params**:

```python
# Factory (base.py:656)
controller = controller_class(
    config=controller_config,  # Pass config object
    dynamics_model=dynamics_model,
    **other_params  # Other kwargs (not gains)
)

# All controllers must accept:
class ModularXXXSMC:
    def __init__(self, config, dynamics_model, **kwargs):
        self.gains = config.gains  # Extract from config
```

**Pros**:
- Clean, config-driven design
- Consistent across all controllers
- Easier to extend with new parameters

**Cons**:
- Requires updating all controller constructors
- Larger changeset

### Option 2: Parameter-Based

**Update all controllers to accept gains as kwarg**:

```python
# Factory (no change)
controller = controller_class(**controller_params)  # Includes 'gains'

# All controllers must accept:
class ModularXXXSMC:
    def __init__(self, gains, dynamics_model, **kwargs):
        self.gains = gains  # Direct parameter
```

**Pros**:
- Minimal factory changes
- Explicit parameter passing

**Cons**:
- Breaks config-driven pattern
- Inconsistent with design philosophy

### Option 3: Hybrid (NOT RECOMMENDED)

Keep current inconsistent pattern, fix each controller individually.

**Cons**:
- Maintains technical debt
- Future controllers will be confused
- No standardization

---

## Recommended Action

**Choose Option 1 (Config-Driven)**:

1. **Update factory** (`src/controllers/factory/base.py:656`):
   - Remove `gains` from `controller_params`
   - Ensure `gains` are in `controller_config.gains`
   - Pass `config` object to controller constructor

2. **Standardize controller constructors**:
   - All modular controllers: `__init__(self, config, dynamics_model, **kwargs)`
   - Extract gains from `config.gains` in constructor
   - Update 4 broken controllers (classical, sta, adaptive, swing_up)

3. **Validation**:
   - Re-run integration tests
   - Verify all 5 controllers pass
   - Check coverage improvement

---

## Affected Files

**Factory**:
- `src/controllers/factory/base.py` (line 656)
- `src/controllers/factory/registry.py` (controller metadata)

**Controllers** (need constructor updates):
- `src/controllers/smc/algorithms/classical/controller.py`
- `src/controllers/smc/algorithms/super_twisting/controller.py`
- `src/controllers/smc/algorithms/adaptive/controller.py`
- `src/controllers/swing_up/controller.py` (if exists)

**Working Controller** (reference implementation):
- `src/controllers/smc/algorithms/hybrid/controller.py` (use as template)

---

## Testing Requirements

**Before Fix**:
- [x] Integration tests fail (4/5 controllers)
- [x] Test pass rate: 20% (1/5)

**After Fix**:
- [ ] All integration tests pass (5/5 controllers)
- [ ] Test pass rate: 100% (5/5)
- [ ] No regressions in existing unit tests
- [ ] Factory coverage >40%

**Test Commands**:
```bash
# Run integration tests
python -m pytest tests/test_integration/test_factory_integration.py -v

# Run factory unit tests
python -m pytest tests/test_controllers/factory/ -v

# Check coverage
python -m pytest tests/ --cov=src/controllers/factory --cov-report=html
```

---

## Impact Assessment

**Production Impact**: CRITICAL
- System cannot create 4/5 controllers
- Blocks all production deployments
- Prevents Week 3 coverage work continuation

**User Impact**: HIGH
- Users cannot use classical_smc, sta_smc, adaptive_smc, swing_up_smc
- Only hybrid_adaptive_sta_smc works
- Simulations will fail for most controller types

**Development Impact**: HIGH
- Blocks Week 3 coverage improvement (PAUSED)
- Blocks PSO integration tests
- Blocks end-to-end workflow tests

---

## Discovery Context

**Why Mock Tests Missed This**:
- Sessions 1-2 used mock-based unit tests
- Mocks created fake config objects matching mock expectations
- 20% pass rate attributed to "incomplete mocks"
- Real factory API bug was hidden

**Why Integration Tests Found This**:
- Session 3 switched to integration tests with real config.yaml
- Used actual factory code paths
- Used actual controller classes
- **Immediately revealed API inconsistency on first run**

**Value**: Integration tests prevented this bug from shipping to production!

---

## References

**Documentation**:
- `.project/ai/planning/WEEK3_SESSION3_FINDINGS.md` (detailed analysis)
- `.project/ai/planning/WEEK3_PROGRESS.md` (progress tracker)

**Tests**:
- `tests/test_integration/test_factory_integration.py` (reproduction)
- `tests/test_controllers/factory/test_base_create_controller.py` (unit tests)

**Code**:
- `src/controllers/factory/base.py:656` (bug location)
- `src/controllers/smc/algorithms/hybrid/controller.py` (working example)

---

## Timeline

**Discovered**: December 20, 2025, 8:00-9:00pm (Session 3)
**Documented**: December 20, 2025, 9:00pm
**Status**: OPEN (pending fix)
**Priority**: P0 (blocks Week 3 continuation)

---

## Next Steps

1. **Assign Owner**: Factory team to implement Option 1
2. **Estimate**: 2-4 hours (4 controller updates + factory fix + tests)
3. **Validate**: Run integration tests after fix
4. **Resume Work**: Week 3 Session 4 after factory fix complete

---

**Issue Status**: OPEN - Awaiting factory fix
**Blocking**: Week 3 Coverage Improvement
**Priority**: CRITICAL (P0)
