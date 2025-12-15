# MT-8 Reproducibility Test Protocol

**Test Date:** December 15, 2025
**Test Type:** Reproducibility Validation
**Test ID:** MT8-REPRO-2025-12-15

---

## Objective

Validate the reproducibility of MT-8 disturbance rejection optimization by re-running the complete robust PSO workflow from baseline gains with explicit random seeds.

**Research Question:** Do multiple PSO runs with different random seeds converge to similar optimal gains and fitness values?

**Success Criteria:**
- Coefficient of variation (CV) of final fitness < 5% across seeds
- Mean improvement within ±10% of original MT-8 improvement
- Relative standard deviation (RSD) of gain parameters < 20%

---

## Background

### Original MT-8 Optimization (November 8, 2025)

**Results:**
- **Classical SMC:** 2.15% improvement
- **STA SMC:** 1.38% improvement
- **Adaptive SMC:** 0.47% improvement
- **Hybrid Adaptive STA SMC:** 21.39% improvement (best)
- **Average:** 6.35% improvement

**Configuration:**
- Algorithm: PySwarms GlobalBestPSO
- Particles: 30
- Iterations: 50
- Evaluations per controller: ~4,500
- Runtime: ~70 minutes (all 4 controllers)
- **Random seed:** Not explicitly documented (likely system time or PySwarms default)

**Problem:** Original run did not control random seed, making it impossible to reproduce exact results.

---

## Test Design

### Seed Strategy

Run optimization with **3 different explicit random seeds**:
1. **Seed 42** - Standard reproducibility seed
2. **Seed 123** - Alternative seed
3. **Seed 456** - Third independent seed

**Rationale:**
- 3 seeds provides statistical confidence (N=3 for mean, std, CV)
- Keeps runtime manageable (~3.5 hours total)
- More seeds can be added if CV > 5%

### Baseline Gains (Pre-MT-8)

Starting point for all optimization runs (nominal-only tuning, NO disturbance rejection):

| Controller | Baseline Gains | Source | Performance Under Disturbances |
|-----------|----------------|--------|-------------------------------|
| Classical SMC | [5.0, 5.0, 5.0, 0.5, 0.5, 0.5] | Pre-MT-8 nominal tuning | 0% convergence, 236° overshoot |
| STA SMC | [8.0, 4.0, 12.0, 6.0, 4.85, 3.43] | Issue #2 resolution | 0% convergence, 241° overshoot |
| Adaptive SMC | [10.0, 8.0, 5.0, 4.0, 1.0] | Pre-MT-8 nominal tuning | 0% convergence, 187° overshoot |
| Hybrid Adaptive STA SMC | [5.0, 5.0, 5.0, 0.5] | Pre-MT-8 nominal tuning | 0% convergence, 667° overshoot (CATASTROPHIC) |

**Note:** These gains are restored to `config.yaml` during testing and reverted to MT-8 robust gains afterward.

---

## PSO Configuration

**Algorithm:** PySwarms GlobalBestPSO

**Parameters (Identical to Original MT-8):**
- **n_particles:** 30
- **n_iterations:** 50
- **Options:** `{'c1': 2.0, 'c2': 2.0, 'w': 0.7}` (cognitive, social, inertia)
- **Bounds:** Controller-specific from `config.yaml pso.bounds` section

**Fitness Function:**
```
robust_fitness = 0.5 * cost_nominal + 0.5 * cost_disturbed
```

Where:
- `cost_nominal`: Performance with no external disturbances
- `cost_disturbed`: Average performance over 2 disturbance scenarios:
  - **Step disturbance:** 10.0 N at t=2.0s
  - **Impulse disturbance:** 30.0 N pulse at t=2.0s (0.1s duration)

**Cost Metric:**
```
cost = 0.7 * settling_time + 0.2 * (overshoot/30.0) + 0.1 * (energy/50.0)
```

---

## Test Execution

### Phase 1: Setup (Complete)

**Tasks:**
- [OK] Created `optimization_results/mt8_baseline_gains.json` with baseline gains
- [OK] Backed up current MT-8 robust gains to `optimization_results/mt8_robust_gains_backup.json`
- [OK] Restored baseline gains to `config.yaml` (lines 74-154)
- [OK] Created `scripts/mt8_reproducibility_test.py` with seed parameter
- [OK] Created this protocol document

### Phase 2: Run Optimization (Pending)

**Execution Commands:**

```bash
# Seed 42 (~70 minutes)
python scripts/mt8_reproducibility_test.py --seed 42 --save-prefix mt8_repro_seed42

# Seed 123 (~70 minutes)
python scripts/mt8_reproducibility_test.py --seed 123 --save-prefix mt8_repro_seed123

# Seed 456 (~70 minutes)
python scripts/mt8_reproducibility_test.py --seed 456 --save-prefix mt8_repro_seed456
```

**Expected Output Files:**

Per seed (4 controllers × 3 seeds = 12 JSON files):
- `optimization_results/mt8_repro_seed42_classical_smc.json`
- `optimization_results/mt8_repro_seed42_sta_smc.json`
- `optimization_results/mt8_repro_seed42_adaptive_smc.json`
- `optimization_results/mt8_repro_seed42_hybrid_adaptive_sta_smc.json`
- (Same pattern for seeds 123 and 456)

Summary files (3 total):
- `optimization_results/mt8_repro_seed42_summary.json`
- `optimization_results/mt8_repro_seed123_summary.json`
- `optimization_results/mt8_repro_seed456_summary.json`

**Runtime Estimate:**
- Per seed: ~70 minutes (4 controllers)
- Total: ~210 minutes (~3.5 hours)
- Can be run overnight or in background

### Phase 3: Statistical Analysis (Pending)

**Script:** `scripts/mt8_analyze_reproducibility.py` (to be created)

**Metrics to Compute:**

#### A. Fitness Reproducibility
For each controller, across 3 seeds:
- Mean final fitness: `μ_fitness = mean(fitness_seed42, fitness_seed123, fitness_seed456)`
- Standard deviation: `σ_fitness`
- Coefficient of variation: `CV = σ_fitness / μ_fitness × 100%`
- Comparison with original MT-8 fitness

**Success Criterion:** CV < 5%

#### B. Gain Reproducibility
For each controller, for each gain parameter, across 3 seeds:
- Mean gain value: `μ_k = mean(k_seed42, k_seed123, k_seed456)`
- Standard deviation: `σ_k`
- Relative standard deviation: `RSD = σ_k / μ_k × 100%`

**Success Criterion:** RSD < 20% for all gain parameters

#### C. Improvement Reproducibility
For each controller, across 3 seeds:
- Fitness improvement: `improvement = 100 × (baseline_cost - optimized_cost) / baseline_cost`
- Mean improvement across seeds
- Comparison with original MT-8 improvement

**Success Criterion:** Mean improvement within ±10% of original MT-8 improvement

#### D. Convergence Rate
- Count how many runs successfully converged (expected: 12/12 = 100%)
- Check for any PSO failures or diverged simulations

### Phase 4: Reporting (Pending)

**Report File:** `benchmarks/MT8_REPRODUCIBILITY_REPORT.md`

**Contents:**
1. Executive summary (pass/fail, key findings)
2. Statistical analysis results (tables with mean, std, CV, RSD)
3. Comparison with original MT-8 results
4. Fitness convergence plots (optional, if time permits)
5. Recommendations (e.g., ensemble methods if CV > 5%)

### Phase 5: Cleanup and Archival (Pending)

**Tasks:**
- Restore MT-8 robust gains to `config.yaml` from backup
- Archive reproducibility test results to `benchmarks/reproducibility/mt8/`
- Update `benchmarks/MT8_COMPLETE_REPORT.md` with reproducibility validation section
- Commit results to git repository

---

## Success Criteria

### Primary Criteria

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| CV of final fitness | < 5% | Acceptable variation for stochastic optimization |
| Mean improvement vs. original MT-8 | Within ±10% | Validates original results are reproducible |
| RSD of gain parameters | < 20% | PSO stochasticity expected, but gains should cluster |
| Convergence rate | 100% (12/12 runs) | All optimizations should succeed |

### Secondary Criteria

| Metric | Threshold | Note |
|--------|-----------|------|
| Runtime per seed | 60-80 minutes | Should match original MT-8 runtime |
| No simulation divergences | 0 failures | Controllers should be stable during optimization |
| Gain bounds respected | 100% compliance | All optimized gains within specified bounds |

---

## Interpretation Guidelines

### If CV < 5% (GOOD Reproducibility)

**Interpretation:** MT-8 methodology is robust and reproducible despite PSO stochasticity

**Actions:**
1. Document reproducibility as research strength in LT-7 paper
2. Use mean gains across seeds as "ensemble" production gains (optional)
3. Cite reproducibility validation as evidence of methodological rigor

### If 5% ≤ CV < 10% (MODERATE Reproducibility)

**Interpretation:** PSO shows some sensitivity to random seed but results are reasonably consistent

**Actions:**
1. Document CV in research paper with confidence intervals
2. Consider running additional seeds (4-5 total) for tighter confidence bounds
3. Recommend ensemble approach: run multiple seeds, select best or average

### If CV ≥ 10% (POOR Reproducibility)

**Interpretation:** PSO is highly sensitive to random seed, indicating potential local optima issues

**Actions:**
1. Document PSO stochasticity as research finding
2. Investigate PSO parameter tuning:
   - Increase particles (e.g., 50-100)
   - Increase iterations (e.g., 100-200)
   - Adjust cognitive/social parameters (c1, c2)
3. Consider alternative optimization methods:
   - Multi-start PSO (run N seeds, take best)
   - Ensemble PSO (average top K results)
   - Alternative algorithms (CMA-ES, Bayesian optimization)
4. Still valuable research contribution (documents optimization challenges)

---

## Data Management

### File Organization

```
optimization_results/
├── mt8_baseline_gains.json                    # Baseline gains reference
├── mt8_robust_gains_backup.json               # MT-8 robust gains backup
├── mt8_repro_seed42_classical_smc.json        # Seed 42 results
├── mt8_repro_seed42_sta_smc.json
├── mt8_repro_seed42_adaptive_smc.json
├── mt8_repro_seed42_hybrid_adaptive_sta_smc.json
├── mt8_repro_seed42_summary.json
├── mt8_repro_seed123_*.json                   # Seed 123 results (5 files)
├── mt8_repro_seed456_*.json                   # Seed 456 results (5 files)
└── ...

benchmarks/
├── MT8_REPRODUCIBILITY_TEST_PROTOCOL.md       # This file
├── MT8_REPRODUCIBILITY_REPORT.md              # Final report (after analysis)
└── mt8_reproducibility_test.log               # Execution log

scripts/
├── mt8_reproducibility_test.py                # Test execution script
└── mt8_analyze_reproducibility.py             # Statistical analysis script
```

### After Completion: Archive Structure

```
benchmarks/reproducibility/mt8/
├── protocol.md                                # This protocol
├── report.md                                  # Final report
├── results/
│   ├── seed42_*.json                         # 5 files
│   ├── seed123_*.json                        # 5 files
│   └── seed456_*.json                        # 5 files
├── scripts/
│   ├── mt8_reproducibility_test.py
│   └── mt8_analyze_reproducibility.py
└── logs/
    └── mt8_reproducibility_test.log
```

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Setup | 25 min | [OK] Complete (2025-12-15) |
| Phase 2: Run Optimization | 210 min | [PENDING] Ready to execute |
| Phase 3: Statistical Analysis | 30 min | [PENDING] After Phase 2 |
| Phase 4: Reporting | 15 min | [PENDING] After Phase 3 |
| Phase 5: Cleanup | 5 min | [PENDING] After Phase 4 |
| **Total** | **~4.5 hours** | |

---

## Risk Assessment

### Low Risk
- Baseline restoration (fully documented, easily reversible)
- Statistical analysis (read-only operations)
- Production restoration (backed up gains)

### Medium Risk
- Long runtime (3.5 hours) - **Mitigation:** Run overnight or in background
- PSO may converge to different local optima - **Expected:** This is what we're measuring

### No Risk
- No changes to controller code
- No changes to simulation logic
- No changes to PSO algorithm (same parameters as MT-8)

---

## References

**Original MT-8 Documentation:**
- Complete Report: `benchmarks/MT8_COMPLETE_REPORT.md`
- Optimization Script: `scripts/mt8_robust_pso.py`
- Result Files: `optimization_results/mt8_robust_*.json`
- Summary: `optimization_results/mt8_robust_pso_summary.json`

**Configuration:**
- Baseline Gains: `config.yaml` lines 38-73 (`controller_defaults`)
- MT-8 Robust Gains: `config.yaml` lines 74-154 (`controllers`)
- PSO Bounds: `config.yaml` `pso.bounds` section

**Research Paper:**
- LT-7: `.artifacts/mt8_disturbance_rejection_paper_v2.1.pdf`
- Section 8.2: Disturbance Rejection Analysis (will include reproducibility validation)

---

## Contact

**Reproducibility Test Lead:** Claude Code MT-8 Team
**Test Date:** December 15, 2025
**Protocol Version:** 1.0

---

**Status:** Phase 1 Complete | Phase 2 Ready to Execute
