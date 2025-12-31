# Bug Hunting Plan - Systematic Codebase Investigation

**Created**: December 31, 2025
**Based on**: Successful discovery of 6 critical bugs in Phase 2 investigation
**Multi-AI Strategy**: Claude + ChatGPT + Gemini collaboration patterns

---

## Executive Summary

This plan provides a systematic methodology for hunting bugs in the DIP-SMC-PSO codebase. It's based on successful discovery of 6 critical bugs during Phase 2:
- 1 bug found by Claude (emergency reset threshold)
- 5 bugs found by Gemini (parameter passing, state indexing, damping sign, gradient, gain naming)

**Key Principle**: Bugs often hide at interfaces, in implicit assumptions, and where multiple components interact.

---

## Bug Categories (Priority Order)

### Category 1: Critical - Controller Safety & Correctness
**Impact**: System stability, physical safety, mathematical correctness
**Examples from Phase 2**:
- Emergency reset threshold (0.9×k_max vs k_max clip)
- Damping sign (amplifying vs opposing)
- Gain naming (velocity vs position swapped)

### Category 2: High - Parameter Propagation
**Impact**: Optimization ineffective, wrong configurations used
**Examples from Phase 2**:
- Parameter passing (hardcoded gains instead of PSO-optimized)
- Gradient calculation (wrong gains used)

### Category 3: Medium - State Management
**Impact**: Incorrect calculations, instability
**Examples from Phase 2**:
- State indexing (wrong vector format)

### Category 4: Low - Documentation & Consistency
**Impact**: Confusion, maintenance issues
**Examples**: Misleading comments, inconsistent naming

---

## Systematic Search Strategies

### Strategy 1: Interface Boundary Analysis

**What to Look For**: Bugs at component boundaries where data passes between systems

**Steps**:
1. Identify all interfaces (controller factory, config objects, function calls)
2. Check parameter mapping at each boundary
3. Verify units/formats match expectations
4. Trace data flow end-to-end

**Commands**:
```bash
# Find all factory creation functions
grep -n "def create_" src/controllers/factory/

# Find all config class definitions
grep -n "class.*Config" src/ -r

# Find parameter extraction patterns
grep -n "get\(" src/ -r | grep "params"
```

**Checklist**:
- [ ] Are parameters passed through or recreated?
- [ ] Are defaults consistent across boundaries?
- [ ] Are units/scales preserved?
- [ ] Are array indices consistent?

**Phase 2 Success**: Found parameter passing bug (hardcoded gains)

---

### Strategy 2: Sign Convention Audit

**What to Look For**: Negative signs that should be positive (or vice versa)

**Steps**:
1. Find all control law implementations
2. Check damping/derivative terms (should oppose motion)
3. Check feedback signs (should stabilize, not amplify)
4. Verify mathematical derivations match code

**Commands**:
```bash
# Find all derivative control calculations
grep -n "derivative" src/controllers/ -r -i

# Find damping implementations
grep -n "damp" src/controllers/ -r -i

# Find negative sign patterns
grep -n "\-.*\*" src/controllers/ -r | grep -v "^\s*#"
```

**Checklist**:
- [ ] Does damping oppose velocity? (should be negative)
- [ ] Does feedback stabilize? (check sign of error)
- [ ] Are gradients computed correctly? (chain rule)
- [ ] Do surface derivatives match theory?

**Phase 2 Success**: Found damping sign bug (amplifying instead of opposing)

---

### Strategy 3: Array Indexing & State Vector Format

**What to Look For**: Mismatches in array access patterns

**Steps**:
1. Document canonical state vector format
2. Find all state[i] accesses
3. Verify each access matches documented format
4. Check for off-by-one errors

**Commands**:
```bash
# Find all state vector accesses
grep -n "state\[" src/controllers/ -r

# Find state format documentation
grep -n "state.*format\|state vector" src/ -r -i

# Find array slicing
grep -n "state\[.*:" src/controllers/ -r
```

**Canonical Format** (document this!):
```python
# Full DIP state vector (6 elements)
state = [x, theta1, theta2, x_dot, theta1_dot, theta2_dot]

# Simplified state vector (4 elements)
state = [theta1, theta1_dot, theta2, theta2_dot]
```

**Checklist**:
- [ ] Is format documented in each controller?
- [ ] Are indices consistent across files?
- [ ] Are bounds checked before access?
- [ ] Are velocity/position pairs adjacent?

**Phase 2 Success**: Found state indexing bug (wrong format assumption)

---

### Strategy 4: Mathematical Correctness Verification

**What to Look For**: Code that doesn't match mathematical derivations

**Steps**:
1. Find all sliding surface implementations
2. Compare code to theory (papers, textbooks)
3. Check gain/coefficient assignments
4. Verify gradient calculations

**Commands**:
```bash
# Find sliding surface implementations
grep -n "sliding.*surface\|surface.*compute" src/ -r -i

# Find gain assignments
grep -n "self\.k1\|self\.k2\|self\.lam" src/controllers/ -r

# Find gradient calculations
grep -n "gradient" src/controllers/ -r -i
```

**Theory Reference**:
```
Standard SMC sliding surface:
s = λ₁e₁ + ė₁ + λ₂e₂ + ė₂

Where:
- λ₁, λ₂ = position gains (damping coefficients)
- e₁, e₂ = position errors
- ė₁, ė₂ = velocity errors
```

**Checklist**:
- [ ] Do variable names match theory?
- [ ] Are gains applied to correct terms?
- [ ] Are derivatives computed correctly?
- [ ] Does code match paper equations?

**Phase 2 Success**: Found gain naming bug (k/λ swapped) + gradient calculation bug

---

### Strategy 5: Emergency/Safety Condition Analysis

**What to Look For**: Safety thresholds that conflict with operational limits

**Steps**:
1. Find all reset/safety conditions
2. Compare thresholds to operational limits
3. Check for contradictory conditions
4. Verify recovery mechanisms exist

**Commands**:
```bash
# Find emergency reset conditions
grep -n "emergency\|reset" src/controllers/ -r -i

# Find threshold comparisons
grep -n "if.*>.*max\|if.*<.*min" src/controllers/ -r

# Find safety limits
grep -n "max_force\|min_force\|max_gain\|min_gain" src/ -r
```

**Checklist**:
- [ ] Are thresholds reachable under normal operation?
- [ ] Are thresholds consistent with clipping limits?
- [ ] Can system recover from emergency state?
- [ ] Are all safety conditions logged?

**Phase 2 Success**: Found emergency reset threshold bug (0.9×k_max vs k_max)

---

## Multi-AI Collaboration Strategy

### When to Use Each AI

**Claude (Code Review Approach)**:
- Finding safety/threshold bugs
- Analyzing control flow logic
- Checking boundary conditions
- Documentation review

**Gemini (Systematic Investigation)**:
- Mathematical correctness verification
- State vector format analysis
- Sign convention audits
- Parameter propagation tracing

**ChatGPT (High-Level Architecture)**:
- Interface design issues
- Configuration management
- Factory pattern bugs
- Dependency injection

### Collaboration Workflow

1. **Planning Phase** (Claude)
   - Define bug categories
   - Prioritize search areas
   - Create systematic checklist

2. **Parallel Search** (All 3 AIs)
   - Claude: Focus on safety conditions
   - Gemini: Focus on mathematical correctness
   - ChatGPT: Focus on interfaces

3. **Cross-Validation** (All 3 AIs)
   - Each AI reviews others' findings
   - Check for false positives
   - Verify fixes don't introduce new bugs

4. **Testing Phase** (Claude)
   - Run comprehensive tests
   - Validate with PSO optimization
   - Measure impact on metrics

---

## High-Priority Search Areas

### 1. Controller Factory (`src/controllers/factory/base.py`)
**Why**: Central point where all controllers are created
**What to Check**:
- Parameter mapping from config to controllers
- Default value consistency
- Gain propagation to sub-controllers

**Commands**:
```bash
grep -n "def create_controller" src/controllers/factory/base.py
grep -n "Config" src/controllers/factory/base.py
grep -n "gains\s*=" src/controllers/factory/base.py
```

### 2. Sliding Surface Implementations
**Why**: Mathematical correctness critical for stability
**What to Check**:
- Gain naming conventions (k vs λ)
- Position vs velocity terms
- Derivative calculations

**Files**:
- `src/controllers/smc/core/sliding_surface.py`
- `src/controllers/smc/algorithms/*/controller.py`

### 3. Adaptive Gain Logic
**Why**: Complex state-dependent behavior
**What to Check**:
- Adaptation bounds vs clipping limits
- Emergency reset conditions
- Leak rate signs
- Saturation handling

**Files**:
- `src/controllers/smc/algorithms/adaptive/adaptation_law.py`
- `src/controllers/smc/algorithms/hybrid/controller.py`

### 4. State Vector Access
**Why**: Easy to get wrong, hard to debug
**What to Check**:
- Index consistency across files
- Format assumptions documented
- Bounds checking present

**Command**:
```bash
grep -n "state\[[0-9]\]" src/controllers/ -r
```

### 5. Equivalent Control Calculations
**Why**: Affects all controllers
**What to Check**:
- Gradient calculations
- Gain selection (position vs velocity)
- Matrix operations

**File**: `src/controllers/smc/core/equivalent_control.py`

---

## Bug Hunting Checklist (Weekly Audit)

### Week 1: Interface Boundaries
- [ ] Review all `create_*` functions
- [ ] Check parameter passing in factory
- [ ] Verify config object propagation
- [ ] Test with multiple configurations

### Week 2: Mathematical Correctness
- [ ] Audit sliding surface implementations
- [ ] Compare code to theory papers
- [ ] Check gain naming conventions
- [ ] Verify derivative calculations

### Week 3: Safety & Thresholds
- [ ] Review all emergency conditions
- [ ] Check threshold consistency
- [ ] Verify saturation limits
- [ ] Test recovery mechanisms

### Week 4: State Management
- [ ] Document state vector formats
- [ ] Audit all state[i] accesses
- [ ] Check array bounds
- [ ] Verify velocity/position pairing

---

## Validation Protocol (After Finding Bugs)

### 1. Unit Test (Immediate)
```bash
# Test specific controller with bug fix
python -m pytest tests/test_controllers/test_<controller>.py -v
```

### 2. Integration Test (Same Day)
```bash
# Run simulation with fixed controller
python simulate.py --ctrl <controller> --plot
```

### 3. PSO Optimization (1-2 Days)
```bash
# Re-run optimization to measure impact
python simulate.py --ctrl <controller> --run-pso --seed 42 --save gains_fixed.json
```

### 4. Comparative Analysis (3-4 Days)
- Compare before/after metrics
- Check if bug fix improves performance
- Document impact (chattering, settling time, overshoot)

---

## Bug Documentation Template

When you find a bug, document it with this template:

```markdown
## Bug #N: <Short Description>

**Date Discovered**: YYYY-MM-DD
**Discovered By**: Claude/Gemini/ChatGPT
**Severity**: Critical/High/Medium/Low
**Category**: Safety/Math/Interface/State/Documentation

### Description
[Clear explanation of what's wrong]

### Location
- **File**: path/to/file.py
- **Line**: XXX
- **Function**: function_name()

### Root Cause
[Why the bug exists - design flaw, typo, assumption violation, etc.]

### Evidence
```python
# BEFORE (buggy code)
old_code_here
```

### Fix
```python
# AFTER (fixed code)
new_code_here
```

### Impact
- **Before Fix**: [metrics/behavior]
- **After Fix**: [metrics/behavior]
- **Improvement**: [quantitative change]

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] PSO optimization shows improvement
- [ ] No new bugs introduced

### Related Bugs
[Links to related bugs or issues]
```

---

## Known Bug Patterns (Learn from Phase 2)

### Pattern 1: "Hardcoded Defaults"
**Symptom**: Optimization has no effect
**Location**: Factory functions, config initialization
**Fix**: Extract values from parameters, don't recreate

### Pattern 2: "Sign Flip"
**Symptom**: Instability, amplification instead of damping
**Location**: Control law implementations, derivative terms
**Fix**: Check mathematical derivation, verify feedback sign

### Pattern 3: "Index Offset"
**Symptom**: Wrong state values, unexpected behavior
**Location**: state[i] accesses
**Fix**: Document state format, verify all accesses

### Pattern 4: "Threshold Mismatch"
**Symptom**: Safety conditions trigger unexpectedly
**Location**: Emergency resets, saturation checks
**Fix**: Ensure thresholds > operational limits

### Pattern 5: "Variable Name Confusion"
**Symptom**: Code doesn't match theory
**Location**: Gain assignments, coefficient naming
**Fix**: Use consistent naming from literature

---

## Tools & Commands Reference

### Finding Specific Patterns
```bash
# Find all TODO/FIXME comments
grep -n "TODO\|FIXME" src/ -r

# Find all hardcoded numbers
grep -n "[^a-zA-Z_][0-9]\+\.[0-9]\+" src/controllers/ -r

# Find all state vector accesses
grep -n "state\[" src/controllers/ -r

# Find all config defaults
grep -n "default\s*=" src/ -r

# Find all emergency/safety conditions
grep -n "if.*emergency\|if.*reset" src/controllers/ -r
```

### Cross-File Consistency Checks
```bash
# Find all definitions of a variable
grep -n "self\.k1\s*=" src/controllers/ -r

# Find all uses of a variable
grep -n "self\.k1" src/controllers/ -r

# Compare implementations across controllers
diff -y <(grep "surface" src/controllers/smc/algorithms/classical/controller.py) \
        <(grep "surface" src/controllers/smc/algorithms/adaptive/controller.py)
```

### Test Coverage Analysis
```bash
# Check which files lack tests
for file in src/controllers/**/*.py; do
    test_file="tests/test_controllers/test_$(basename $file)"
    if [ ! -f "$test_file" ]; then
        echo "Missing test: $test_file"
    fi
done
```

---

## Success Metrics

### Bug Hunt Effectiveness
- **Critical Bugs Found**: >0 per week (initially)
- **False Positive Rate**: <20%
- **Fix Validation**: 100% (all fixes tested)
- **Regression Rate**: <5% (new bugs introduced by fixes)

### Code Quality Improvement
- **Test Coverage**: +5% per month
- **Documentation Coverage**: +10% per month
- **Consistent Naming**: 95%+ (automated checks)
- **Mathematical Correctness**: 100% (verified against theory)

### Performance Impact
- **Chattering Reduction**: Measure before/after each bug fix
- **Stability Improvement**: Count emergency resets
- **PSO Effectiveness**: Check if optimization works after fixes

---

## Monthly Bug Hunt Schedule

### Week 1: Factory & Interfaces
- Monday: Parameter passing audit
- Wednesday: Config object review
- Friday: Factory function testing

### Week 2: Mathematical Correctness
- Monday: Sliding surface audit
- Wednesday: Derivative calculation review
- Friday: Gain naming verification

### Week 3: Safety & Thresholds
- Monday: Emergency condition review
- Wednesday: Saturation limit checks
- Friday: Recovery mechanism testing

### Week 4: State Management
- Monday: State format documentation
- Wednesday: Index access audit
- Friday: Bounds checking implementation

---

## Emergency Bug Response Protocol

### If Production System Fails

1. **Immediate** (< 1 hour)
   - Roll back to last known good version
   - Document failure symptoms
   - Preserve logs/data

2. **Investigation** (1-4 hours)
   - Run systematic bug hunt (all strategies)
   - Involve all 3 AIs (parallel search)
   - Identify root cause

3. **Fix & Test** (4-8 hours)
   - Implement minimal fix
   - Run full test suite
   - Validate with real data

4. **Deploy & Monitor** (8-24 hours)
   - Deploy fix to production
   - Monitor for 24 hours
   - Document lessons learned

---

## Lessons from Phase 2

### What Worked Well

1. **Multi-AI Collaboration**
   - Claude found emergency reset bug through code review
   - Gemini found 5 bugs through systematic investigation
   - Cross-validation caught false positives

2. **Systematic Testing**
   - PSO optimization revealed parameter passing bug
   - Set 3 validation confirmed bug fixes (or lack thereof)
   - Statistical analysis showed impact

3. **Documentation**
   - Comprehensive bug tracking in markdown
   - Clear before/after comparisons
   - Publication-ready analysis

### What to Improve

1. **Earlier Detection**
   - Should have found bugs before 4 failed optimizations
   - Weekly audits could catch issues sooner
   - Automated checks for known patterns

2. **Automated Validation**
   - Run PSO after every major change
   - Continuous integration with full test suite
   - Regression test suite for bug fixes

3. **Theory Verification**
   - Compare code to papers during implementation
   - Peer review by multiple AIs before committing
   - Mathematical correctness checklist

---

## Quick Start Guide

### For Next Bug Hunt Session

1. **Pick a Strategy** (from Strategies 1-5 above)
2. **Run Search Commands** (copy-paste from checklist)
3. **Review Results** (manually inspect suspicious patterns)
4. **Document Findings** (use bug documentation template)
5. **Validate Fix** (run tests, PSO, compare metrics)
6. **Commit** (with clear commit message)

### Example: Finding Hardcoded Values

```bash
# 1. Search for hardcoded gains
grep -n "\[20.*15.*12.*8\]" src/controllers/ -r

# 2. Check if they should be parameters
grep -n "controller_gains\|params" src/controllers/factory/base.py

# 3. Document the bug
# (use template above)

# 4. Implement fix
# (extract from parameters instead of hardcoding)

# 5. Test
python -m pytest tests/test_controllers/test_hybrid.py -v

# 6. Validate with PSO
python simulate.py --ctrl hybrid_adaptive_sta_smc --run-pso --seed 42
```

---

## Conclusion

This bug hunting plan is a living document based on successful discovery of 6 critical bugs. Update it as you find new patterns and develop better search strategies.

**Remember**: Bugs often hide where:
- Multiple components interact (interfaces)
- Implicit assumptions are made (formats, units)
- Mathematical theory meets code (sign conventions)
- Safety meets performance (thresholds)

**Key Principle**: Systematic search + multi-AI collaboration + rigorous testing = Bug-free code

---

**Status**: READY FOR USE
**Next Bug Hunt**: Week of January 6, 2026
**Target**: Find and fix 2-3 medium/high severity bugs
**Success Metric**: Improved test coverage + better PSO performance

**Last Updated**: December 31, 2025
