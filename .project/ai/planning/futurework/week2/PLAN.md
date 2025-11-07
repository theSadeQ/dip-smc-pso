# Week 2 Detailed Execution Plan

**Duration**: 18 hours (MT-1: 10h, MT-2: 8h)
**Tasks**: MT-1 (Terminal SMC), MT-2 (Integral SMC)
**Prerequisites**: ✅ All met (QW-1 complete, theory documented)
**Confidence**: **MEDIUM-HIGH** (75%)
**Created**: October 17, 2025
**Status**: In Progress

---

## Executive Summary

Week 2 implements two advanced SMC variants with finite-time convergence (Terminal SMC) and disturbance rejection (Integral SMC). Both controllers are fully planned in the theory documentation with mathematical formulations ready for implementation.

**Terminal SMC** (MT-1, 10 hours) introduces a **nonlinear sliding surface** that accelerates convergence near equilibrium, achieving 30-50% faster settling times than classical SMC.

**Integral SMC** (MT-2, 8 hours) **eliminates the reaching phase** by constructing a sliding surface that passes through the initial condition, providing 40-60% better disturbance rejection through integral action.

Week 1's 40% time efficiency (6h actual vs 10h planned) provides a 4-hour buffer for unexpected stability tuning challenges.

**Success Metrics**: 2 new controllers operational, 20+ tests passing (≥95% coverage), performance validated, factory integration clean, Week 3 unblocked.

---

## Quick Reference

### Daily Schedule

**Day 1** (6h): MT-1 Theory + Implementation
- 09:00-11:00: MT-1.1 Theory & Design
- 11:00-13:00: MT-1.2 Implementation Part 1
- 14:00-16:00: MT-1.2 Implementation Part 2

**Day 2** (6h): MT-1 Complete + MT-2 Start
- 09:00-11:00: MT-1.3 Testing
- 11:00-12:00: MT-1.4 Factory Integration
- 13:00-14:00: MT-1.5 Validation
- 14:00-17:00: MT-2.1 Theory + MT-2.2 Start

**Day 3** (6h): MT-2 Complete + Validation
- 09:00-11:00: MT-2.2 Implementation Complete
- 11:00-12:30: MT-2.3 Testing
- 13:00-13:30: MT-2.4 Factory Integration
- 13:30-17:00: MT-2.5 Validation + Final Wrap-up

### Success Criteria Checklist

- [ ] 1. Controllers implemented (2 files, ~580 lines)
- [ ] 2. Test coverage ≥95%
- [ ] 3. Tests passing (18+)
- [ ] 4. Terminal convergence 30-50% faster
- [ ] 5. Integral disturbance rejection 40-60% better
- [ ] 6. Reaching phase eliminated (s(0) = 0)
- [ ] 7. Documentation updated (+100 lines)
- [ ] 8. Factory integration clean
- [ ] 9. Config valid
- [ ] 10. Week 3 unblocked

**Pass Threshold**: ≥9/10 criteria met

---

## MT-1: Terminal SMC (10 hours)

### Mathematical Specifications

**Nonlinear Sliding Surface**:
```
s = (k1·θ̇1 + λ1·θ1) + (k2·θ̇2 + λ2·θ2) + β·sign(s_linear)|e|^α
where 0 < α < 1, e = sqrt(θ1² + θ2²)
```

**Control Law**:
```
u = u_eq - K·sat(s/ε)
```

**7 Gains**: [k1, k2, λ1, λ2, α, β, K]
- Position gains: k1, k2 ∈ [2.0, 30.0]
- Velocity gains: λ1, λ2 ∈ [0.2, 10.0]
- Convergence exponent: α ∈ (0.5, 0.95) **must satisfy 0 < α < 1**
- Terminal gain: β ∈ [1.0, 20.0]
- Switching gain: K ∈ [5.0, 50.0]

**Default Gains**: [20.0, 15.0, 12.0, 8.0, 0.7, 10.0, 35.0]

### Subtasks

**MT-1.1: Theory & Design** (2h)
- Read theory docs (lines 267-324)
- Validate equations
- Design sliding surface computation
- Document design decisions

**MT-1.2: Implementation** (4h)
- Create `src/controllers/tsmc_smc.py` (~300 lines)
- Implement class skeleton + __init__
- Implement _compute_sliding_surface() with nonlinear term
- Implement compute_control(), _compute_equivalent_control()
- Add utilities: validate_gains(), properties, cleanup()

**MT-1.3: Testing** (2h)
- Create `tests/test_controllers/test_tsmc_smc.py` (~250 lines)
- 10+ tests: initialization, α constraint, sliding surface, control computation, convergence vs classical
- Target coverage: ≥95%

**MT-1.4: Factory Integration** (1h)
- Update factory.py CONTROLLER_REGISTRY
- Update config.yaml (defaults + PSO bounds)
- Test create_controller('tsmc_smc')

**MT-1.5: Validation** (1h)
- Run simulation: python simulate.py --ctrl tsmc_smc --plot
- Measure convergence time vs classical (verify 30-50% speedup)
- Update theory docs (line 267: [PLAN] → [IMPLEMENTED])

### Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Nonlinear stability tuning difficult | Use literature values (α=0.7, β=10.0), incremental tuning |
| Terminal term numerical instability | Add epsilon guard: if e_norm > 1e-6 |
| Convergence test fails | Manual gain tuning, use PSO if needed |

---

## MT-2: Integral SMC (8 hours)

### Mathematical Specifications

**Integral Sliding Surface**:
```
s = σ + ∫₀ᵗ σ(τ) dτ
where σ = (k1·θ̇1 + λ1·θ1) + (k2·θ̇2 + λ2·θ2)
```

**Initial Condition**: s(0) = 0 by construction (no reaching phase)

**Control Law**:
```
u = u_eq - K·sat(s/ε) - kd·σ - ki·integral_state
```

**7 Gains**: [k1, k2, λ1, λ2, K, kd, ki]
- Position/velocity: Same as classical SMC
- Switching gain: K ∈ [5.0, 50.0]
- Derivative gain: kd ∈ [0.05, 3.0]
- Integral gain: ki ∈ [0.1, 5.0] **must be moderate to avoid windup**

**Default Gains**: [20.0, 15.0, 12.0, 8.0, 35.0, 2.0, 1.0]

### Subtasks

**MT-2.1: Theory & Design** (1.5h)
- Read theory docs (lines 326-400)
- Design integral surface + anti-windup mechanism
- Document design

**MT-2.2: Implementation** (3.5h)
- Create `src/controllers/ismc_smc.py` (~280 lines)
- Implement with integral state management
- Add anti-windup: freeze integral during saturation, clamp ±10.0

**MT-2.3: Testing** (1.5h)
- Create `tests/test_controllers/test_ismc_smc.py` (~200 lines)
- 8+ tests: initialization, s(0) = 0, anti-windup, disturbance rejection

**MT-2.4: Factory Integration** (0.5h)
- Update factory + config (same pattern as MT-1)

**MT-2.5: Validation** (1h)
- Run simulation with disturbance injection
- Measure disturbance rejection (verify 40-60% better)
- Update theory docs

### Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Integral windup under saturation | Anti-windup logic (freeze + clamp), reduce ki if needed |
| Disturbance test fails | Increase ki, tune kd for damping |
| Overshoot excessive | Reduce ki, increase kd |

---

## Risk Register

| ID | Risk | Prob | Impact | Mitigation |
|----|------|------|--------|------------|
| R-1 | Nonlinear stability tuning | M | H | Use literature values, incremental tuning |
| R-2 | Integral windup | M | M | Anti-windup back-calculation |
| R-3 | Time overrun (18h → 22h) | M | M | Use Week 1 buffer (4h saved) |

---

## Quality Gates

### QG-1: After MT-1.1 (Design)
- [ ] Sliding surface equation validated
- [ ] Gain bounds defined
- [ ] Design document created

### QG-2: After MT-1.2 (Implementation)
- [ ] Controller instantiates without errors
- [ ] compute_control() returns valid output
- [ ] Sliding surface includes nonlinear term

### QG-3: After MT-1.3 (Testing)
- [ ] 10+ tests passing
- [ ] Coverage ≥95%
- [ ] Convergence test shows speedup

### QG-4: After MT-1.4 (Integration)
- [ ] create_controller('tsmc_smc') works
- [ ] No regressions in existing controllers

### QG-5: After MT-1.5 (Validation)
- [ ] Simulation successful
- [ ] Performance validated (30-50% speedup)
- [ ] Theory docs updated

---

## Files to Read (Before Starting)

- [ ] docs/theory/smc_theory_complete.md (lines 267-400)
- [ ] src/controllers/classic_smc.py (implementation pattern)
- [ ] src/controllers/sta_smc.py (advanced SMC pattern)
- [ ] src/controllers/factory.py (registry structure)
- [ ] config.yaml (controller configs)
- [ ] tests/test_controllers/test_controller_basics.py (test patterns)

## External References

- [ ] Feng et al. (2002): "Terminal sliding mode control"
- [ ] Yu & Man (1998): "Fast terminal sliding-mode control"
- [ ] Utkin & Shi (1996): "Integral sliding mode"

---

## Progress Tracking

**Current Status**: Week 2 started
**Date**: October 17, 2025
**Completed**: 0/12 tasks
**Time Spent**: 0h / 18h planned
**Buffer Available**: 4h (from Week 1)

**Daily Updates**: See .project/ai/planning/research/week2/DAILY_LOG.md

---

## Week 3 Preview

**What Week 2 Unblocks**:
- MT-5: Controller Performance Benchmark (9 controllers: 7 existing + Terminal + Integral)
- Comprehensive comparison study with statistical analysis
- Expected Week 3 start: MT-4 (Particle Diversity PSO) + MT-5 (Benchmark)

---

## Sign-Off Checklist

**Before starting**:
- [x] Week 2 plan created
- [x] Todo list updated
- [x] Directory structure created
- [ ] Theory docs reviewed
- [ ] Reference implementations analyzed
- [ ] External papers acquired (or available)

**Upon completion**:
- [ ] All success criteria met (≥9/10)
- [ ] No blockers for Week 3
- [ ] Final summary written

---

**Review Status**: ✅ APPROVED by user
**Next Step**: Begin MT-1.1 (Theory & Design Analysis)
