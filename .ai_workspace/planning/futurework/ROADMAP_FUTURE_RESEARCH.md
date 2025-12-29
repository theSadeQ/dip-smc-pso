# Research Roadmap: Future Research & Experimental Work

**Generated**: October 18, 2025 (Split from original ROADMAP.md)
**Focus**: New controllers and new PSO algorithms (NOT necessary right now)
**Goal**: Experimental research for novel contributions and advanced optimization
**Time Horizon**: 12+ weeks (120+ hours total)
**Priority**: LOW - Defer until existing work complete (see ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/))

---

## Executive Summary

This roadmap contains **experimental and future research work** that is **NOT necessary for current system validation**. These are novel controllers and advanced optimization algorithms that could be explored AFTER the existing 7 controllers are validated, documented, and benchmarked.

**⚠️ IMPORTANT**: This work should be **DEFERRED** until ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/) is complete. You cannot publish research on new controllers without first validating the existing ones.

**New Controllers (Experimental)**:
1. Terminal Sliding Mode Control (TSMC) - Finite-time convergence
2. Integral Sliding Mode Control (ISMC) - No reaching phase
3. Higher-Order SMC (HOSM) - Beyond super-twisting

**New PSO Algorithms (Experimental)**:
1. Adaptive Inertia PSO - Time-varying inertia weight
2. Particle Diversity Maintenance - Repulsion mechanism
3. Hybrid PSO (PSO + Gradient Descent) - Local refinement
4. Multi-Objective PSO - Pareto fronts
5. Genetic Algorithm (GA) - Alternative optimization
6. Simulated Annealing (SA) - Alternative optimization

**Why Deferred**:
- Existing 7 controllers not yet validated
- Lyapunov proofs for existing controllers not complete
- Benchmarking for current system not done
- Cannot justify new controllers without understanding current ones

---

## 1. New Controllers (Experimental)

### 1.1 Terminal Sliding Mode Control (TSMC)

**Priority**: Medium (after existing work complete)
**Effort**: 10-12 hours
**Value**: High (finite-time convergence)

**Why This Is New**:
- Finite-time convergence (faster than asymptotic SMC)
- Nonlinear sliding surface (vs linear in Classical SMC)

**Implementation Details**:
- **File**: `src/controllers/tsmc_smc.py`
- **Gains**: 7 total [k1, k2, λ1, λ2, α, β, K]
- **Sliding Surface**: `s = x + β·sign(x)|x|^α` where 0 < α < 1
- **Control Law**: `u = -K·sign(s)` or `u = -K·tanh(s/ε)`
- **Key Property**: Finite-time convergence (vs asymptotic in Classical SMC)

**References**:
- Feng et al. (2002) - Terminal sliding mode control
- Yu & Man (1998) - Terminal sliding mode with fast response

**Tasks**:
1. Implement controller following factory pattern
2. Add to `src/controllers/factory.py` (CONTROLLER_REGISTRY)
3. Create `tests/test_controllers/test_tsmc_smc.py`
4. Add to `config.yaml` with gain bounds
5. PSO tuning for gain optimization
6. Document in `docs/theory/smc_theory_complete.md`

**Success Criteria**:
- Controller passes validation tests
- Converges faster than Classical SMC
- PSO tunes gains successfully

**Deliverables**:
- `src/controllers/tsmc_smc.py` (~300-400 lines)
- `tests/test_controllers/test_tsmc_smc.py` (~200 lines)
- Theory documentation update (~150 lines)

---

### 1.2 Integral Sliding Mode Control (ISMC)

**Priority**: Medium (after existing work complete)
**Effort**: 8-10 hours
**Value**: High (no reaching phase, better disturbance rejection)

**Why This Is New**:
- Eliminates reaching phase (system on sliding surface from t=0)
- Better disturbance rejection than Classical SMC

**Implementation Details**:
- **File**: `src/controllers/ismc_smc.py`
- **Gains**: 7 total [k1, k2, λ1, λ2, K, kd, ki]
- **Sliding Surface**: `s = x + ∫σ(x)dt` (integral term)
- **Control Law**: `u = -K·sign(s) - kd·ẋ - ki·∫s·dt`
- **Key Property**: No reaching phase (system starts on sliding surface)

**References**:
- Utkin & Shi (1996) - Integral sliding mode control
- Cao & Xu (2004) - Integral sliding mode for uncertain systems

**Tasks**:
1. Implement controller with integral term
2. Add to factory pattern
3. Create tests with disturbance rejection validation
4. PSO tuning
5. Document theory

**Success Criteria**:
- No reaching phase observed
- Better disturbance rejection than Classical SMC (>20% improvement)
- Stable under parameter variations

**Deliverables**:
- `src/controllers/ismc_smc.py` (~300-400 lines)
- `tests/test_controllers/test_ismc_smc.py` (~200 lines)
- Theory documentation update (~150 lines)

---

### 1.3 Higher-Order Sliding Mode Control (HOSM)

**Priority**: Low (advanced research, complex theory)
**Effort**: 14-16 hours
**Value**: Medium (generalization, academic contribution)

**Why This Is New**:
- Generalization beyond super-twisting (order 2 → order 3+)
- Arbitrary-order sliding mode differentiator

**Implementation Details**:
- **File**: `src/controllers/hosm_smc.py`
- **Gains**: 8-10 gains (depends on order)
- **Order**: 3 or higher (super-twisting is order 2)
- **Control Law**: Arbitrary-order differentiator, twisting algorithm
- **Key Property**: Higher-order chattering reduction

**References**:
- Levant (2003) - Higher-order sliding modes
- Levant (2005) - Homogeneity approach to HOSM

**Tasks**:
1. Study HOSM theory (complex mathematics)
2. Implement arbitrary-order differentiator
3. Add to factory pattern
4. Create property-based tests
5. PSO tuning (challenging)
6. Extensive documentation (theory is complex)

**Success Criteria**:
- HOSM controller operational (order 3+)
- Chattering reduced vs super-twisting
- Formal stability proof

**Deliverables**:
- `src/controllers/hosm_smc.py` (~500-600 lines, complex)
- `tests/test_controllers/test_hosm_smc.py` (~300 lines)
- Theory documentation update (~400-500 lines, extensive math)

**Warning**: This is academically interesting but may not provide significant practical value over existing STA SMC.

---

## 2. New PSO Algorithms (Experimental)

### 2.1 Adaptive Inertia PSO

**Priority**: Medium (good ROI if PSO improvements needed)
**Effort**: 3-4 hours
**Value**: High (20-30% faster convergence expected)

**Why This Is New**:
- Current PSO uses fixed inertia w = 0.729
- Time-varying inertia improves convergence speed

**Implementation Details**:
- **File**: Modify `src/optimizer/pso_optimizer.py`
- **Parameters**: w_min = 0.4, w_max = 0.9
- **Formula**: `w(t) = w_max - (w_max - w_min) * t / T`
- **Effect**: High inertia early (exploration), low inertia late (exploitation)

**References**:
- Shi & Eberhart (1998) - Inertia weight strategy
- Clerc & Kennedy (2002) - Constriction factor

**Tasks**:
1. Add adaptive inertia parameters to `__init__`
2. Modify `optimize()` loop to update w each iteration
3. Add flag `adaptive_inertia = True/False`
4. Validate on Classical SMC (compare fixed vs adaptive)
5. Create `tests/test_optimizer/test_pso_optimizer.py` (currently missing!)

**Success Criteria**:
- PSO converges in 35 generations (vs 50 baseline)
- 20-30% speedup validated across multiple controllers
- No loss in final fitness quality

**Deliverables**:
- Updated `src/optimizer/pso_optimizer.py` (~20-30 lines modified)
- `tests/test_optimizer/test_pso_optimizer.py` (~200 lines NEW)
- Documentation update in Tutorial 03

**Note**: This should be tested AFTER existing system is validated (ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/) QW-3 complete).

---

### 2.2 Particle Diversity Maintenance

**Priority**: Medium (avoid premature convergence)
**Effort**: 4-5 hours
**Value**: Medium (prevents premature convergence)

**Why This Is New**:
- Current PSO has no diversity maintenance
- Particles can cluster prematurely (local minima)

**Implementation Details**:
- **File**: Modify `src/optimizer/pso_optimizer.py`
- **Mechanism**: Repulsion force when particles cluster
- **Formula**: If distance between particles < threshold, add repulsion term
- **Effect**: Maintains exploration, avoids premature convergence

**References**:
- Parsopoulos & Vrahatis (2004) - Particle diversity
- Blackwell & Branke (2004) - Multi-swarm optimization

**Tasks**:
1. Add diversity metric calculation (std of particle positions)
2. Add repulsion mechanism when diversity < threshold
3. Validate maintains diversity score > 0.5 throughout run
4. Compare performance with/without diversity maintenance

**Success Criteria**:
- Diversity score > 0.5 throughout optimization
- No significant slowdown (< 10% more generations)
- Better global optimum found (vs premature convergence)

**Deliverables**:
- Updated `src/optimizer/pso_optimizer.py` (~40-50 lines modified)
- Tests in `tests/test_optimizer/test_pso_optimizer.py`

**Note**: Depends on MT-3 (Adaptive Inertia PSO) being implemented first.

---

### 2.3 Hybrid PSO (PSO + Gradient Descent)

**Priority**: Low (complex, marginal value)
**Effort**: 10-12 hours
**Value**: Medium (50% faster convergence, but complex)

**Why This Is New**:
- Combines global search (PSO) + local refinement (gradient descent)
- Current PSO is global search only

**Implementation Details**:
- **File**: New file `src/optimizer/hybrid_pso_optimizer.py`
- **Strategy**: PSO for first 70% of budget, gradient descent for last 30%
- **Gradient**: Numerical gradient (finite differences) for controller fitness
- **Effect**: Fast global search + precise local refinement

**References**:
- Angeline (1998) - Evolutionary optimization in continuous spaces
- Shi & Eberhart (2001) - Hybrid optimization methods

**Tasks**:
1. Implement numerical gradient computation
2. Create hybrid optimizer class (extends PSOTuner)
3. Add switching logic (PSO → gradient descent)
4. Validate on multiple controllers
5. Compare with pure PSO

**Success Criteria**:
- Hybrid PSO converges in 25 generations (vs 35 adaptive PSO)
- Better final fitness (local optimum refinement)
- Stable across controllers

**Deliverables**:
- `src/optimizer/hybrid_pso_optimizer.py` (~400-500 lines NEW)
- Tests in `tests/test_optimizer/test_hybrid_pso.py`

**Warning**: Complex implementation, may not provide sufficient value over adaptive PSO. Defer unless convergence speed critical.

---

### 2.4 Multi-Objective PSO (MOPSO)

**Priority**: Low (advanced research, niche application)
**Effort**: 15-18 hours
**Value**: High (research contribution, Pareto analysis)

**Why This Is New**:
- Current PSO optimizes single objective (weighted sum)
- Multi-objective explores trade-offs (stability vs chattering vs energy)

**Implementation Details**:
- **File**: New file `src/optimizer/mopso_optimizer.py`
- **Objectives**:
  1. Stability (minimize settling time)
  2. Chattering (minimize chattering frequency)
  3. Energy (minimize ∫u²dt)
- **Output**: Pareto front (set of non-dominated solutions)
- **Algorithm**: NSGA-II style Pareto ranking + crowding distance

**References**:
- Coello Coello et al. (2004) - Multi-objective evolutionary algorithms
- Reyes-Sierra & Coello (2006) - Multi-objective PSO

**Tasks**:
1. Implement multi-objective fitness evaluation
2. Implement Pareto dominance ranking
3. Implement crowding distance for diversity
4. Create Pareto front visualization
5. Analyze trade-offs (stability vs chattering vs energy)
6. Generate trade-off plots

**Success Criteria**:
- Pareto front generated (20-50 non-dominated solutions)
- Trade-offs clearly visible (e.g., low chattering requires high energy)
- Visualization shows Pareto front in 2D/3D

**Deliverables**:
- `src/optimizer/mopso_optimizer.py` (~600-800 lines NEW)
- Pareto front visualization in `src/utils/visualization/pareto_plots.py`
- Tutorial update with trade-off analysis

**Note**: This is a significant research contribution but NOT necessary for validating existing controllers. Defer until after research paper on existing work.

---

### 2.5 Genetic Algorithm (GA)

**Priority**: Low (alternative optimization, marginal value)
**Effort**: 12-14 hours
**Value**: Low (PSO already works well)

**Why This Is New**:
- Alternative population-based optimization
- Comparison: GA vs PSO

**Implementation Details**:
- **File**: New file `src/optimizer/ga_optimizer.py`
- **Operations**: Selection, crossover, mutation
- **Encoding**: Real-valued (not binary)
- **Selection**: Tournament or roulette wheel
- **Crossover**: Single-point or uniform
- **Mutation**: Gaussian noise

**References**:
- Goldberg (1989) - Genetic algorithms in search and optimization
- Deb (2001) - Multi-objective optimization using evolutionary algorithms

**Tasks**:
1. Implement GA optimizer class
2. Implement selection, crossover, mutation operators
3. Integrate with controller factory
4. Validate on Classical SMC
5. Compare with PSO (convergence speed, final fitness)

**Success Criteria**:
- GA converges to similar fitness as PSO
- Comparison study shows GA vs PSO trade-offs

**Deliverables**:
- `src/optimizer/ga_optimizer.py` (~500-600 lines NEW)
- Tests in `tests/test_optimizer/test_ga_optimizer.py`
- Comparison tutorial update

**Warning**: Marginal value - PSO already works well. Only implement if academic comparison needed.

---

### 2.6 Simulated Annealing (SA)

**Priority**: Very Low (sequential, slow, not recommended)
**Effort**: 6-8 hours
**Value**: Very Low (not suitable for controller tuning)

**Why This Is New**:
- Alternative optimization (stochastic local search)
- Avoids local minima via probabilistic acceptance

**Implementation Details**:
- **File**: New file `src/optimizer/sa_optimizer.py`
- **Algorithm**: Metropolis-Hastings acceptance
- **Cooling Schedule**: Exponential or logarithmic
- **Effect**: Slow convergence, sequential (not parallel like PSO)

**Warning**: **NOT RECOMMENDED** for controller tuning. Simulated Annealing is:
- Sequential (cannot parallelize like PSO)
- Slow (requires many iterations)
- Worse than PSO for continuous optimization

**Recommendation**: **SKIP** unless academic comparison absolutely required.

---

## 3. Task Dependencies & Execution Order

### 3.1 Dependency Graph (Future Work Only)

```
NEW CONTROLLERS:
  MT-1 (Terminal SMC, 10h)
    └─> MT-7 (Reaching time analysis, 9h)

  MT-2 (Integral SMC, 8h)
    └─> MT-7 (Reaching time analysis, 9h)

  LT-1 (HOSM, 14h)
    └─> (Advanced theory work)

NEW PSO:
  MT-3 (Adaptive inertia PSO, 3h)
    └─> MT-4 (Particle diversity PSO, 4h)
        └─> LT-2 (Hybrid PSO, 10h)
        └─> LT-5 (Multi-objective PSO, 15h)

  LT-3 (Genetic Algorithm, 12h)
    └─> (Independent, comparison study)

THEORY:
  MT-7 (Reaching time analysis for NEW controllers, 9h)
    └─> (Depends on MT-1, MT-2)
```

### 3.2 Critical Path (Future Work)

**If you decide to pursue this work AFTER existing work complete**:

1. **Controllers First**: MT-1 (10h) + MT-2 (8h) = 18 hours
2. **PSO Improvements**: MT-3 (3h) + MT-4 (4h) = 7 hours
3. **Advanced PSO**: LT-2 (10h) OR LT-5 (15h)
4. **Theory**: MT-7 (9h) for new controllers
5. **HOSM**: LT-1 (14h) if academically motivated

**Total**: 58-73 hours for new controllers + basic PSO improvements

**MOPSO + GA**: Additional 27-32 hours if needed

---

## 4. Execution Strategy (IF Pursued)

### 4.1 Recommendation: DEFER Until Existing Work Complete

**⚠️ DO NOT START THIS WORK UNTIL**:
- ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/) is complete
- Research paper on existing 7 controllers is drafted
- Existing controllers validated, benchmarked, Lyapunov proofs complete

**Reason**:
- Cannot justify new controllers without validating existing ones
- Reviewers will ask "why not improve existing controllers first?"
- Benchmarking methodology must be established on existing system

---

### 4.2 IF You Decide to Pursue (After Existing Work)

**Phase 1: New Controllers** (4-5 weeks, 36 hours)
1. MT-1: Terminal SMC (10h)
2. MT-2: Integral SMC (8h)
3. MT-7: Reaching time analysis (9h)
4. Benchmark new controllers vs existing 7 (6h)
5. Update research paper with new controllers (3h)

**Phase 2: PSO Improvements** (2-3 weeks, 17 hours)
1. MT-3: Adaptive inertia PSO (3h)
2. MT-4: Particle diversity PSO (4h)
3. Validate PSO improvements on all controllers (6h)
4. Update Tutorial 03 with PSO improvements (4h)

**Phase 3: Advanced Work** (4-6 weeks, 39-53 hours) - **OPTIONAL**
1. LT-1: HOSM controller (14h) - if academically motivated
2. LT-2: Hybrid PSO (10h) - if convergence speed critical
3. LT-5: Multi-objective PSO (15h) - if trade-off analysis needed
4. Update research paper with advanced contributions (variable)

**Phase 4: Alternative Optimizers** (3-4 weeks, 12-26 hours) - **LOW PRIORITY**
1. LT-3: Genetic Algorithm (12h) - only if comparison needed
2. SA: Simulated Annealing (6-8h) - **NOT RECOMMENDED**

---

### 4.3 Recommended Priority (IF Pursued)

**HIGH PRIORITY** (good ROI, practical value):
1. MT-1: Terminal SMC - Finite-time convergence (practical)
2. MT-2: Integral SMC - Disturbance rejection (practical)
3. MT-3: Adaptive inertia PSO - 30% faster convergence

**MEDIUM PRIORITY** (research value, moderate effort):
1. MT-4: Particle diversity PSO - Avoid premature convergence
2. LT-5: Multi-objective PSO - Research contribution (Pareto analysis)

**LOW PRIORITY** (academic niche, high effort):
1. LT-1: HOSM - Complex theory, marginal practical value
2. LT-2: Hybrid PSO - Complex, marginal value over adaptive PSO
3. LT-3: Genetic Algorithm - Only for comparison study

**NOT RECOMMENDED**:
1. Simulated Annealing - Slow, sequential, not suitable

---

## 5. Success Criteria (IF Pursued)

### 5.1 New Controllers Success

- ✅ Terminal SMC converges faster than Classical SMC (finite-time property)
- ✅ Integral SMC shows no reaching phase
- ✅ All new controllers pass validation tests
- ✅ PSO successfully tunes gains for new controllers
- ✅ Benchmarking shows performance improvement over existing controllers

### 5.2 New PSO Success

- ✅ Adaptive inertia PSO: 20-30% faster convergence
- ✅ Particle diversity PSO: Diversity score > 0.5 throughout
- ✅ Hybrid PSO: 50% faster convergence (if implemented)
- ✅ Multi-objective PSO: Clear Pareto fronts, trade-off analysis

### 5.3 Research Output Success

- ✅ Research paper updated with new controllers (if added)
- ✅ Performance comparison: 9-10 controllers (7 existing + 2-3 new)
- ✅ Trade-off analysis (if MOPSO implemented)
- ✅ Novel contributions clearly articulated

---

## 6. Risk Assessment (IF Pursued)

### 6.1 Technical Risks

**Terminal SMC Stability**:
- Risk: Finite-time singularity near origin (α < 1)
- Mitigation: Boundary layer, saturation function
- Impact: High (controller may be unstable)

**HOSM Complexity**:
- Risk: Theory is very complex, implementation challenging
- Mitigation: Use existing literature, start with order 3
- Impact: Medium (may take 16-20 hours instead of 14)

**Hybrid PSO Gradient Computation**:
- Risk: Numerical gradient expensive (many fitness evaluations)
- Mitigation: Use analytical gradient if possible
- Impact: Medium (may negate convergence speedup)

### 6.2 Research Risks

**Novelty Concern**:
- Risk: Terminal SMC, Integral SMC already well-known
- Mitigation: Focus on application to DIP, comparison with existing
- Impact: Low (application still publishable)

**Incremental Contribution**:
- Risk: Adding 2-3 controllers may not be significant contribution
- Mitigation: Focus on comprehensive comparison, Lyapunov proofs, robustness
- Impact: Medium (reviewers may ask for more novelty)

**Time Investment vs Payoff**:
- Risk: 60-120 hours for marginal improvement over existing work
- Mitigation: Prioritize high-value tasks (Terminal, Integral, Adaptive PSO)
- Impact: High (opportunity cost - could spend time on other research)

---

## 7. Resource Requirements (IF Pursued)

### 7.1 Tools

- ✅ Python 3.9+ (already installed)
- ✅ NumPy, SciPy, Matplotlib (already installed)
- ❌ **cvxpy** - May be needed for advanced optimization (MOPSO, Hybrid PSO)
- ❌ **DEAP** - Genetic algorithm library (if GA implemented)

### 7.2 Documentation

- ⚠️ **Terminal SMC references** - Feng et al. (2002), Yu & Man (1998) - NEED TO ACQUIRE
- ⚠️ **Integral SMC references** - Utkin & Shi (1996) - NEED TO ACQUIRE
- ⚠️ **HOSM references** - Levant (2003, 2005) - NEED TO ACQUIRE
- ⚠️ **MOPSO references** - Coello Coello et al. (2004) - NEED TO ACQUIRE

### 7.3 Time Allocation (IF Pursued)

**Minimum (High-priority only)**:
- New controllers (Terminal + Integral): 18 hours
- Adaptive inertia PSO: 3 hours
- Reaching time analysis: 9 hours
- **Total**: 30 hours

**Medium (High + Medium priority)**:
- Above + Particle diversity PSO: 4 hours
- Above + Multi-objective PSO: 15 hours
- **Total**: 49 hours

**Maximum (All tasks)**:
- Above + HOSM: 14 hours
- Above + Hybrid PSO: 10 hours
- Above + GA: 12 hours
- **Total**: 85 hours

---

## 8. Integration with Existing Work

### 8.1 Handoff from ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/)

**PREREQUISITE**: ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/) must be complete BEFORE starting this work.

**Handoff Checklist**:
- ✅ Existing 7 controllers validated, benchmarked
- ✅ Lyapunov proofs complete for existing controllers
- ✅ Disturbance rejection analysis complete
- ✅ Model uncertainty analysis complete
- ✅ Research paper draft complete (existing work)

**What Carries Forward**:
- Benchmarking methodology (apply to new controllers)
- Lyapunov proof techniques (apply to Terminal, Integral SMC)
- PSO tuning workflow (use for new controllers)
- Chattering metrics (apply to new controllers)

---

### 8.2 Research Continuity

**If new controllers added**:
1. Benchmark Terminal, Integral, HOSM same way as existing 7
2. Add to performance comparison matrix (7 → 9-10 controllers)
3. Derive Lyapunov proofs for new controllers
4. Update research paper with new contributions

**If new PSO added**:
1. Validate adaptive inertia PSO on existing 7 controllers first
2. Then apply to new controllers (if implemented)
3. Update Tutorial 03 with PSO improvements
4. Add convergence comparison (fixed vs adaptive vs hybrid)

---

## 9. Summary & Recommendation

### 9.1 Recommendation: DEFER

**⚠️ This work is NOT NECESSARY RIGHT NOW**

**Priority Order**:
1. **FIRST**: Complete ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/) (72 hours, 8-10 weeks)
   - Validate, benchmark, document existing 7 controllers
   - Lyapunov proofs, disturbance rejection, model uncertainty
   - Research paper on existing work

2. **SECOND (OPTIONAL)**: If research needs expansion, start with:
   - MT-1: Terminal SMC (10h) - High practical value
   - MT-2: Integral SMC (8h) - High practical value
   - MT-3: Adaptive inertia PSO (3h) - High ROI

3. **THIRD (OPTIONAL)**: Advanced work if needed:
   - LT-5: Multi-objective PSO (15h) - Research contribution
   - MT-7: Reaching time analysis (9h) - Theoretical validation

4. **DEFER INDEFINITELY**:
   - LT-1: HOSM (14h) - Complex, marginal value
   - LT-2: Hybrid PSO (10h) - Marginal value over adaptive PSO
   - LT-3: Genetic Algorithm (12h) - Marginal value
   - SA: Simulated Annealing - **NOT RECOMMENDED**

---

### 9.2 Effort Summary (IF Pursued)

**High-Priority Tasks** (if pursued after existing work):
- New controllers (Terminal + Integral): 18 hours
- PSO improvements (Adaptive + Diversity): 7 hours
- Reaching time analysis: 9 hours
- **Subtotal**: 34 hours

**Medium-Priority Tasks** (optional research contributions):
- Multi-objective PSO: 15 hours
- HOSM controller: 14 hours
- **Subtotal**: 29 hours

**Low-Priority Tasks** (not recommended):
- Hybrid PSO: 10 hours
- Genetic Algorithm: 12 hours
- **Subtotal**: 22 hours

**Total**: 85 hours if ALL tasks pursued (NOT RECOMMENDED)

---

### 9.3 Decision Framework

**Ask yourself**:

1. **Are existing 7 controllers validated?**
   - ❌ NO → Focus on ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/)
   - ✅ YES → Consider new controllers

2. **Is research paper on existing work complete?**
   - ❌ NO → Focus on ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/)
   - ✅ YES → Consider new controllers

3. **Do you need more novelty for publication?**
   - ❌ NO → Focus on existing work quality
   - ✅ YES → Consider Terminal SMC + Integral SMC (high value)

4. **Is PSO convergence too slow?**
   - ❌ NO → Skip PSO improvements
   - ✅ YES → Consider Adaptive inertia PSO (3 hours, high ROI)

5. **Do you need trade-off analysis?**
   - ❌ NO → Skip MOPSO
   - ✅ YES → Consider Multi-objective PSO (15 hours)

**Most likely answer**: Focus on ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/) first.

---

## 10. Files That Would Be Created (IF Pursued)

### 10.1 New Controllers

- `src/controllers/tsmc_smc.py` (~300-400 lines)
- `src/controllers/ismc_smc.py` (~300-400 lines)
- `src/controllers/hosm_smc.py` (~500-600 lines)
- `tests/test_controllers/test_tsmc_smc.py` (~200 lines)
- `tests/test_controllers/test_ismc_smc.py` (~200 lines)
- `tests/test_controllers/test_hosm_smc.py` (~300 lines)

### 10.2 New PSO Algorithms

- Modified `src/optimizer/pso_optimizer.py` (adaptive inertia, diversity)
- `src/optimizer/hybrid_pso_optimizer.py` (~400-500 lines)
- `src/optimizer/mopso_optimizer.py` (~600-800 lines)
- `src/optimizer/ga_optimizer.py` (~500-600 lines)
- `tests/test_optimizer/test_pso_optimizer.py` (~200 lines NEW)
- `tests/test_optimizer/test_hybrid_pso.py` (~200 lines)
- `tests/test_optimizer/test_mopso.py` (~300 lines)
- `tests/test_optimizer/test_ga.py` (~200 lines)

### 10.3 Visualization & Analysis

- `src/utils/visualization/pareto_plots.py` (~200 lines)
- `docs/theory/terminal_smc_theory.md` (~200 lines)
- `docs/theory/integral_smc_theory.md` (~200 lines)
- `docs/theory/hosm_theory.md` (~400 lines)

---

**End of Future Research Roadmap**

**⚠️ REMEMBER**: This work is DEFERRED until ROADMAP_EXISTING_PROJECT.md (archived in academic/archive/planning/) is complete.
