# Framework 1: Gap Closure Plan

**Framework**: By Purpose/Objective
**Plan Date**: 2025-12-30
**Current Status**: 70% Complete (75/133 files)
**Target**: 100% Complete (133/133 files)
**Total Effort**: 22-32 hours (or 10-15 hours optimized with parallelization)

---

## Executive Summary

**Current State**: Framework 1 implemented with 75 files categorized (70% complete)
**Gaps**: 58 files missing across 5 categories
**Critical Gaps**: 4 files (block usability) - 1-3 hours
**Enhancement Gaps**: 54 files (reduce value) - 21-29 hours

**Recommended Approach**:
1. **Phase 1** (Immediate): Close critical gaps in Category 1 (1-3 hours)
2. **Phase 2** (Short-term): Expand Category 2 Safety (6-8 hours)
3. **Phase 3** (Medium-term): Complete Categories 3-5 (15-21 hours)

**Total Time to 100%**: 22-32 hours (sequential) or 10-15 hours (parallel)

---

## Gap Summary by Priority

| Priority | Gaps | Files | Effort | Impact | Categories |
|----------|------|-------|--------|--------|------------|
| **HIGH** | 2 | 4 | 1-3 hours | Block usability | Cat 1 |
| **MEDIUM** | 4 | 16 | 7-10 hours | Reduce value | Cat 1, 2 |
| **LOW** | 4 | 38 | 14-19 hours | Enhancement | Cat 3, 4, 5 |
| **TOTAL** | **10** | **58** | **22-32 hours** | - | **All** |

---

## Phase 1: Critical Gap Closure (1-3 hours) [HIGH PRIORITY]

**Goal**: Bring Category 1 (Performance) to 100% operational status

**Status**: [RECOMMENDED] - Immediate action required
**Impact**: HIGH - Blocks Category 1 usability for publication
**Dependencies**: None

### Task 1.1: Locate Convergence Plots (1-2 hours)

**Gap ID**: GAP 1.1
**Missing Files**: 3-4 convergence plots
**Expected**:
- `pso_convergence_classical_smc.png`
- `pso_convergence_sta_smc.png`
- `pso_convergence_adaptive_smc.png`
- `pso_convergence_hybrid_adaptive_sta.png` (optional)

**Action Plan**:

**Step 1: Search for Existing Plots (15 min)**
```bash
# Search experiments directories
find experiments/ -name "*convergence*.png" -type f

# Search figures directory
find experiments/figures/ -name "*pso*.png" -type f

# Search benchmarks
find benchmarks/figures/ -name "*convergence*.png" -type f

# Search archives
find academic/logs/archive/ -name "*pso*.png" -type f
find .logs/ -name "*convergence*.png" -type f
```

**Step 2: Check Alternative Names (15 min)**
```bash
# PSO may be saved with different naming patterns
find experiments/ -name "*fitness*.png" -o -name "*optimization*.png"
find experiments/ -name "*evolution*.png" -o -name "*swarm*.png"
```

**Step 3: Regenerate from Logs if Missing (1 hour)**
```python
# If plots not found, regenerate from PSO logs
python scripts/visualization/regenerate_pso_plots.py \
    --logs academic/logs/pso/*phase53*.log \
    --output experiments/figures/ \
    --controllers classical_smc sta_smc adaptive_smc hybrid_adaptive_sta_smc
```

**Step 4: Update Framework 1 (15 min)**
```bash
# After finding/generating plots
cd .ai_workspace/pso/by_purpose

# Update create_shortcuts.py to add convergence plots
# Re-run script
python create_shortcuts.py

# Update Category 1 README
# Update FRAMEWORK_1_FILE_MAPPING.csv
# Commit changes
```

**Success Criteria**:
- ✓ 3-4 convergence plots found or regenerated
- ✓ Shortcuts created in `1_performance/convergence_plots/`
- ✓ README updated with plot descriptions
- ✓ File mapping CSV updated

**Effort**: 1-2 hours
**Risk**: LOW (plots likely exist, just need to locate)

---

### Task 1.2: Verify Classical SMC Phase 2 Gains (30 min)

**Gap ID**: GAP 1.2
**Missing File**: 1 file (`pso_classical_smc_standard.json`)
**Expected**: `experiments/classical_smc/optimization/phases/phase2/gains/standard/pso_classical_smc_standard.json`

**Action Plan**:

**Step 1: Search for File (10 min)**
```bash
# Search Phase 2 directories
find experiments/classical_smc/optimization/phases/phase2/ -name "*.json" -type f

# Search optimization_results (old structure)
find optimization_results/ -name "*classical*phase2*.json" -type f

# Search archives
find experiments/classical_smc/optimization/archive/ -name "*phase2*.json" -type f
```

**Step 2: Verify Intentional Gap (10 min)**
```bash
# Check if Classical SMC only has robust Phase 2 (not standard)
ls -la experiments/classical_smc/optimization/phases/phase2/gains/

# Check logs for Phase 2 classical runs
grep -r "classical_smc" academic/logs/pso/*phase2*.log

# Check research documentation
grep -r "Classical.*Phase 2" .ai_workspace/planning/
```

**Step 3: Document Finding (10 min)**

**If file found**:
- Create shortcut in `1_performance/phase2_standard/`
- Update README
- Update file mapping CSV

**If intentional gap**:
- Document in README: "Classical SMC has only robust Phase 2 gains (not standard)"
- Update coverage to 20/21 files (95%)
- Update gap analysis: GAP 1.2 → RESOLVED (intentional)

**Success Criteria**:
- ✓ File found OR gap confirmed as intentional
- ✓ Documentation updated accordingly
- ✓ No ambiguity about missing file

**Effort**: 30 min
**Risk**: VERY LOW (quick verification)

---

### Phase 1 Deliverables

**Upon Completion**:
- Category 1: 95-100% complete (20-21 files)
- Documentation: Updated README, file mapping, gap analysis
- Usability: Category 1 fully operational for publication

**Next Action**: Commit and push Phase 1 changes

---

## Phase 2: Safety Expansion (6-8 hours) [MEDIUM PRIORITY]

**Goal**: Expand Category 2 (Safety) from 40% to 100% coverage

**Status**: [RECOMMENDED] - Expand chattering optimization to all controllers
**Impact**: MEDIUM - Enables comprehensive safety analysis
**Dependencies**: None (can run in parallel with Phase 1)

### Task 2.1: Chattering Optimization for Classical SMC (2-3 hours)

**Gap ID**: GAP 2.1
**Missing Files**: 5 files
**Expected**:
- `classical_smc_chattering.csv` (optimization dataset)
- `classical_smc_chattering_convergence.png` (PSO convergence)
- `classical_smc_chattering_log.log` (execution log)
- `classical_smc_optimized_chattering_gains.json` (best gains)
- `classical_smc_chattering_report.md` (summary)

**Action Plan**:

**Step 1: Configure Chattering PSO (30 min)**
```python
# Create chattering-focused fitness configuration
# File: config_chattering_classical.yaml

pso:
  algorithm: "standard"
  n_particles: 30
  n_iterations: 100
  fitness:
    primary: "chattering"
    weights:
      chattering: 0.7
      rmse: 0.3
  boundary_layer:
    adaptive: true
    epsilon_range: [0.001, 0.010]
    alpha_range: [0.5, 2.0]
```

**Step 2: Run PSO Optimization (1.5-2 hours)**
```bash
# Run chattering-focused PSO for Classical SMC
python simulate.py \
    --ctrl classical_smc \
    --run-pso \
    --config config_chattering_classical.yaml \
    --fitness chattering \
    --boundary-layer-adaptive \
    --save experiments/classical_smc/boundary_layer/chattering_optimized.json \
    --log academic/logs/pso/classical_smc_chattering.log \
    --plot experiments/classical_smc/boundary_layer/chattering_convergence.png
```

**Step 3: Generate Report (30 min)**
```python
# Analyze results and create report
python scripts/analysis/generate_chattering_report.py \
    --input experiments/classical_smc/boundary_layer/ \
    --output experiments/classical_smc/boundary_layer/CHATTERING_REPORT.md \
    --baseline experiments/classical_smc/optimization/phases/phase53/optimized_gains_classical_smc_phase53.json
```

**Step 4: Update Framework 1 (15 min)**
```bash
# Create shortcuts for new files
python .ai_workspace/pso/by_purpose/create_shortcuts.py

# Update Category 2 README
# Update file mapping CSV
```

**Success Criteria**:
- ✓ PSO optimization completes (30-100 iterations)
- ✓ Chattering reduced by ≥3% vs baseline
- ✓ 5 files created (CSV, PNG, log, JSON, MD)
- ✓ Report documents optimal ε_min and α values

**Effort**: 2-3 hours
**Risk**: LOW (MT-6 validated this approach)

---

### Task 2.2: Chattering Optimization for Adaptive SMC (2-3 hours)

**Gap ID**: GAP 2.2
**Action Plan**: Same as Task 2.1, replace `classical_smc` with `adaptive_smc`

**Expected Outcomes**:
- Chattering reduction: ≥5% (Adaptive has better baseline)
- Optimal boundary layer parameters specific to Adaptive SMC
- 5 files created

**Effort**: 2-3 hours

---

### Task 2.3: Chattering Optimization for Hybrid (2-3 hours)

**Gap ID**: GAP 2.3
**Action Plan**: Same as Task 2.1, replace `classical_smc` with `hybrid_adaptive_sta_smc`

**Expected Outcomes**:
- Chattering reduction: ≥4% (Hybrid has moderate baseline)
- Optimal boundary layer parameters for hybrid architecture
- 5 files created

**Effort**: 2-3 hours

---

### Task 2.4: Comparative Chattering Analysis (30 min)

**Action Plan**:

**Step 1: Create Comparison Report (30 min)**
```python
# Compare chattering results across all 4 controllers
python scripts/analysis/compare_chattering_across_controllers.py \
    --input experiments/*/boundary_layer/ \
    --output experiments/comparative/CHATTERING_COMPARISON.md \
    --figures experiments/figures/chattering_comparison.png
```

**Report Contents**:
- Table: Controller × Chattering (baseline vs optimized)
- Table: Optimal boundary layer parameters per controller
- Plot: Chattering reduction bar chart
- Analysis: Trade-offs (chattering vs RMSE)

**Success Criteria**:
- ✓ Comparative report created
- ✓ Cross-controller insights documented
- ✓ Publication-ready figure generated

**Effort**: 30 min

---

### Phase 2 Deliverables

**Upon Completion**:
- Category 2: 100% complete (18/18 files)
- Chattering optimization: All 4 controllers
- Comparative analysis: Cross-controller insights
- Documentation: Updated README, file mapping

**Parallelization**:
- Run Tasks 2.1, 2.2, 2.3 in parallel → 3 hours total (instead of 6-8 hours)

---

## Phase 3: Robustness Cleanup (30 min) [LOW PRIORITY]

**Goal**: Bring Category 3 (Robustness) to 100% coverage

**Status**: [OPTIONAL] - Minor cleanup
**Impact**: LOW - Category already 95% complete
**Dependencies**: None

### Task 3.1: Locate Missing Robust Logs (30 min)

**Gap ID**: GAP 3.1
**Missing Files**: 1-2 log files
**Expected**:
- `2025-11-XX_classical_smc_robust.log`
- `2025-11-XX_sta_smc_robust.log`

**Action Plan**:

**Step 1: Search Archives (15 min)**
```bash
# Search log archives
find academic/logs/archive/ -name "*robust*.log" -o -name "*robust*.tar.gz"
find academic/logs/pso/archive/ -name "*.log"
find .logs/benchmarks/ -name "*robust*.log"

# Extract if compressed
tar -xzf academic/logs/archive/robust_logs_2025-11.tar.gz -C academic/logs/pso/
```

**Step 2: Verify Log Dates (10 min)**
```bash
# Check existing logs for date patterns
ls -lah academic/logs/pso/*robust*.log

# If missing, check if logs were never created (optimization ran without logging)
grep -r "robust" academic/logs/pso/*.log | grep "classical\|sta"
```

**Step 3: Update Framework 1 (5 min)**
- If found: Create shortcuts, update README
- If not found: Document as "logs not generated" in gap analysis

**Success Criteria**:
- ✓ Logs found OR confirmed missing
- ✓ Documentation updated

**Effort**: 30 min
**Risk**: VERY LOW (archival task only)

---

## Phase 4: Efficiency Optimization (8-10 hours) [LOW PRIORITY]

**Goal**: Complete Category 4 (Efficiency) from 15% to 100%

**Status**: [OPTIONAL] - Research extension
**Impact**: LOW - New research direction (not required for current work)
**Dependencies**: None

### Task 4.1: Energy-Focused PSO for All Controllers (8 hours)

**Gap ID**: GAP 4.1
**Missing Files**: 15 files (4 controllers × 3.75 files each + 1 report)
**Expected** (per controller):
- `<controller>_energy_optimized.json` (gains)
- `<controller>_energy_pso.log` (log)
- `<controller>_energy_convergence.png` (plot)
- `<controller>_energy_vs_performance.png` (trade-off plot)

**Plus**:
- `ENERGY_OPTIMIZATION_REPORT.md` (comparative report)

**Action Plan**:

**Step 1: Configure Energy PSO (30 min)**
```python
# Create energy-focused fitness configuration
# File: config_energy.yaml

pso:
  fitness:
    primary: "energy"
    weights:
      energy: 0.7        # Control effort (∫u²dt)
      rmse: 0.3          # Maintain reasonable tracking
  constraints:
    max_rmse: 0.05       # Don't sacrifice too much performance
    max_control: 50.0    # Physical actuator limits
```

**Step 2: Run Energy PSO (8 hours total, 2 hours per controller)**

**Parallelizable**: Run all 4 controllers simultaneously

```bash
# Classical SMC (2 hours)
python simulate.py --ctrl classical_smc --run-pso \
    --config config_energy.yaml \
    --fitness energy \
    --save experiments/classical_smc/optimization/energy_optimized.json \
    --log academic/logs/pso/classical_smc_energy.log \
    --plot experiments/classical_smc/optimization/energy_convergence.png

# STA SMC (2 hours)
python simulate.py --ctrl sta_smc --run-pso \
    --config config_energy.yaml \
    --fitness energy \
    --save experiments/sta_smc/optimization/energy_optimized.json \
    --log academic/logs/pso/sta_smc_energy.log \
    --plot experiments/sta_smc/optimization/energy_convergence.png

# Adaptive SMC (2 hours)
python simulate.py --ctrl adaptive_smc --run-pso \
    --config config_energy.yaml \
    --fitness energy \
    --save experiments/adaptive_smc/optimization/energy_optimized.json \
    --log academic/logs/pso/adaptive_smc_energy.log \
    --plot experiments/adaptive_smc/optimization/energy_convergence.png

# Hybrid (2 hours)
python simulate.py --ctrl hybrid_adaptive_sta_smc --run-pso \
    --config config_energy.yaml \
    --fitness energy \
    --save experiments/hybrid_adaptive_sta/optimization/energy_optimized.json \
    --log academic/logs/pso/hybrid_adaptive_sta_smc_energy.log \
    --plot experiments/hybrid_adaptive_sta/optimization/energy_convergence.png
```

**Step 3: Generate Trade-off Plots (1 hour)**
```python
# Energy vs RMSE trade-off for each controller
python scripts/analysis/generate_energy_tradeoff_plots.py \
    --baseline experiments/*/optimization/phases/phase53/*.json \
    --energy experiments/*/optimization/energy_optimized.json \
    --output experiments/figures/energy_vs_performance_*.png
```

**Step 4: Create Comparative Report (1 hour)**
```python
# Compare energy efficiency across all controllers
python scripts/analysis/generate_energy_report.py \
    --input experiments/*/optimization/energy_optimized.json \
    --output experiments/comparative/ENERGY_OPTIMIZATION_REPORT.md
```

**Step 5: Update Framework 1 (30 min)**
```bash
# Create shortcuts, update Category 4 README, update file mapping
python .ai_workspace/pso/by_purpose/create_shortcuts.py
```

**Success Criteria**:
- ✓ PSO optimization completes for all 4 controllers
- ✓ Energy reduced by ≥20% vs baseline (target: 30-40%)
- ✓ RMSE increase ≤10% (acceptable trade-off)
- ✓ 16 files created (4 × 4 + 1 report)
- ✓ Trade-off analysis documented

**Effort**: 8-10 hours (2-3 hours with parallelization)
**Risk**: MEDIUM (new fitness function, may need tuning)

---

## Phase 5: Multi-Objective Optimization (6-10 hours) [LOW PRIORITY]

**Goal**: Complete Category 5 (Multi-Objective) from 25% to 100%

**Status**: [OPTIONAL] - Research extension
**Impact**: LOW - Advanced research (Pareto fronts)
**Dependencies**: None (MOPSO infrastructure ready)

### Task 5.1: MOPSO for All Controllers (8 hours)

**Gap ID**: GAP 5.1
**Missing Files**: 22 files (4 controllers × 5.5 files each + 2 reports)
**Expected** (per controller):
- `<controller>_pareto_front.json` (Pareto archive)
- `<controller>_mopso_log.log` (execution log)
- `<controller>_chattering_vs_performance.png` (2D Pareto plot)
- `<controller>_hypervolume.json` (hypervolume metric)
- `<controller>_mopso_convergence.png` (convergence plot)
- `<controller>_selected_solution.json` (best compromise)

**Plus**:
- `PARETO_OPTIMIZATION_REPORT.md` (comparative report)
- `HYPERVOLUME_COMPARISON.md` (cross-controller analysis)

**Action Plan**:

**Step 1: Configure MOPSO (30 min)**
```python
# Create multi-objective PSO configuration
# File: config_mopso.yaml

pso:
  algorithm: "mopso"
  n_particles: 50         # Higher for multi-objective
  n_iterations: 200       # More iterations for convergence
  objectives:
    - name: "chattering"
      weight: 1.0
      minimize: true
    - name: "rmse"
      weight: 1.0
      minimize: true
  pareto:
    archive_size: 100
    mutation_rate: 0.1
    selection: "crowding_distance"
```

**Step 2: Run MOPSO (8 hours total, 2 hours per controller)**

**Parallelizable**: Run all 4 controllers simultaneously

```bash
# Classical SMC (2 hours)
python simulate.py --ctrl classical_smc --run-mopso \
    --config config_mopso.yaml \
    --objectives chattering rmse \
    --save experiments/classical_smc/optimization/pareto_front.json \
    --log academic/logs/pso/classical_smc_mopso.log

# Repeat for STA, Adaptive, Hybrid
```

**Step 3: Generate Pareto Plots (1 hour)**
```python
# 2D Pareto fronts for each controller
python scripts/analysis/plot_pareto_fronts.py \
    --input experiments/*/optimization/pareto_front.json \
    --output experiments/figures/*_chattering_vs_performance.png
```

**Step 4: Compute Hypervolume (30 min)**
```python
# Hypervolume indicator for multi-objective performance
python scripts/analysis/compute_hypervolume.py \
    --pareto experiments/*/optimization/pareto_front.json \
    --reference [5.0, 0.1]  # Worst-case reference point
    --output experiments/*/optimization/*_hypervolume.json
```

**Step 5: Select Best Compromise Solutions (30 min)**
```python
# Select knee point from Pareto front (best trade-off)
python scripts/analysis/select_pareto_solution.py \
    --pareto experiments/*/optimization/pareto_front.json \
    --method knee_point \
    --output experiments/*/optimization/*_selected_solution.json
```

**Step 6: Create Reports (1 hour)**
```python
# Pareto optimization report
python scripts/analysis/generate_pareto_report.py \
    --input experiments/*/optimization/pareto_front.json \
    --output experiments/comparative/PARETO_OPTIMIZATION_REPORT.md

# Hypervolume comparison
python scripts/analysis/compare_hypervolume.py \
    --input experiments/*/optimization/*_hypervolume.json \
    --output experiments/comparative/HYPERVOLUME_COMPARISON.md
```

**Step 7: Update Framework 1 (30 min)**
```bash
# Create shortcuts, update Category 5 README
python .ai_workspace/pso/by_purpose/create_shortcuts.py
```

**Success Criteria**:
- ✓ MOPSO converges for all 4 controllers
- ✓ Pareto fronts contain ≥50 non-dominated solutions
- ✓ Hypervolume metric computed
- ✓ Best compromise solutions selected
- ✓ 24 files created (4 × 6 + 2 reports)
- ✓ Trade-off analysis documented

**Effort**: 6-10 hours (2-3 hours with parallelization)
**Risk**: MEDIUM (MOPSO convergence may need tuning)

---

## Implementation Timeline

### Option A: Sequential Execution (22-32 hours)

| Phase | Tasks | Effort | Dependencies | ETA |
|-------|-------|--------|--------------|-----|
| Phase 1 | Critical gaps (Cat 1) | 1-3 hours | None | Day 1 |
| Phase 2 | Safety expansion (Cat 2) | 6-8 hours | None | Day 2-3 |
| Phase 3 | Robustness cleanup (Cat 3) | 30 min | None | Day 3 |
| Phase 4 | Efficiency optimization (Cat 4) | 8-10 hours | None | Day 4-5 |
| Phase 5 | Multi-objective (Cat 5) | 6-10 hours | None | Day 6-7 |
| **TOTAL** | **All gaps closed** | **22-32 hours** | - | **7 days** |

**Total Days**: 7 working days (or 2-3 weeks calendar time)

---

### Option B: Parallel Execution (10-15 hours) [RECOMMENDED]

| Phase | Tasks | Sequential | Parallel | Speedup |
|-------|-------|-----------|----------|---------|
| Phase 1 | Critical gaps | 1-3 hours | 1-3 hours | 1x (can't parallelize) |
| Phase 2 | Safety (3 PSO runs) | 6-8 hours | 2-3 hours | 3x (run simultaneously) |
| Phase 3 | Robustness | 30 min | 30 min | 1x (archival search) |
| Phase 4 | Efficiency (4 PSO runs) | 8-10 hours | 2-3 hours | 4x (run simultaneously) |
| Phase 5 | Multi-obj (4 MOPSO runs) | 6-10 hours | 2-3 hours | 4x (run simultaneously) |
| **TOTAL** | **All gaps closed** | **22-32 hours** | **10-15 hours** | **2-3x** |

**Total Days**: 2-3 working days (or 1 week calendar time)

**Parallelization Strategy**:
- Use GNU parallel or tmux to run multiple PSO optimizations simultaneously
- Requires: Multi-core CPU (4+ cores recommended) + adequate RAM (8GB+ per PSO)

```bash
# Example: Run Phase 2 (Safety) in parallel
parallel python simulate.py --ctrl {} --run-pso --fitness chattering \
    --save experiments/{}/boundary_layer/chattering_optimized.json \
    --log academic/logs/pso/{}_chattering.log ::: \
    classical_smc adaptive_smc hybrid_adaptive_sta_smc
```

---

## Resource Requirements

### Computational Resources

| Phase | CPU Cores | RAM | Disk | Duration |
|-------|-----------|-----|------|----------|
| Phase 1 | 1 | 2GB | 500MB | 1-3 hours |
| Phase 2 (parallel) | 3 | 6GB | 1GB | 2-3 hours |
| Phase 3 | 1 | 1GB | 0MB | 30 min |
| Phase 4 (parallel) | 4 | 8GB | 2GB | 2-3 hours |
| Phase 5 (parallel) | 4 | 12GB | 3GB | 2-3 hours |

**Recommended Setup**:
- CPU: 4+ cores (for parallel execution)
- RAM: 12GB+ (for parallel PSO)
- Disk: 10GB free space (for datasets, logs, plots)

---

### Human Resources

| Phase | Skill Level | Involvement | Effort |
|-------|-------------|-------------|--------|
| Phase 1 | Junior | File search, validation | 1-2 hours active |
| Phase 2 | Intermediate | PSO configuration, monitoring | 3-4 hours active |
| Phase 3 | Junior | Archive search | 15 min active |
| Phase 4 | Intermediate | PSO tuning, analysis | 3-4 hours active |
| Phase 5 | Advanced | MOPSO tuning, Pareto analysis | 4-5 hours active |

**Total Active Time**: 11-15 hours (rest is automated PSO execution)

---

## Risk Assessment

| Phase | Risk Level | Risk Description | Mitigation |
|-------|-----------|------------------|------------|
| Phase 1 | LOW | Files may not exist | Regenerate from logs, document gaps |
| Phase 2 | LOW | PSO may not converge | Use MT-6 validated config, monitor progress |
| Phase 3 | VERY LOW | Logs in archive | Extract from compressed files |
| Phase 4 | MEDIUM | Energy PSO untested | Start with 1 controller, tune config |
| Phase 5 | MEDIUM | MOPSO convergence | Use validated NSGA-II, increase iterations |

**Overall Risk**: LOW-MEDIUM (Phases 1-3 are low-risk, Phases 4-5 may need tuning)

---

## Success Criteria

### Phase 1: Critical Gaps (HIGH PRIORITY)
- ✓ Convergence plots found or regenerated (3-4 files)
- ✓ Classical Phase 2 verified (found or confirmed intentional gap)
- ✓ Category 1 → 95-100% complete
- ✓ Documentation updated

### Phase 2: Safety Expansion (MEDIUM PRIORITY)
- ✓ Chattering PSO completes for Classical, Adaptive, Hybrid (15 files)
- ✓ Chattering reduced by ≥3% per controller
- ✓ Comparative analysis complete
- ✓ Category 2 → 100% complete

### Phase 3: Robustness Cleanup (LOW PRIORITY)
- ✓ Missing logs located or confirmed absent (1-2 files)
- ✓ Category 3 → 100% complete

### Phase 4: Efficiency Optimization (LOW PRIORITY)
- ✓ Energy PSO completes for all 4 controllers (16 files)
- ✓ Energy reduced by ≥20% with RMSE increase ≤10%
- ✓ Trade-off analysis complete
- ✓ Category 4 → 100% complete

### Phase 5: Multi-Objective Optimization (LOW PRIORITY)
- ✓ MOPSO converges for all 4 controllers (24 files)
- ✓ Pareto fronts contain ≥50 non-dominated solutions
- ✓ Hypervolume computed, best solutions selected
- ✓ Category 5 → 100% complete

### Overall Success
- ✓ Framework 1 → 100% complete (133/133 files)
- ✓ All 5 categories operational
- ✓ Documentation comprehensive and accurate
- ✓ All gaps closed or documented

---

## Decision Points

### After Phase 1 (1-3 hours invested)
**Question**: Continue to Phase 2 or stop?

**Decision Criteria**:
- **Continue** if: Need comprehensive safety analysis (chattering across controllers)
- **Stop** if: Category 1 sufficient for current publication/research needs

**Recommendation**: Continue if planning PSO-focused research, otherwise defer Phases 2-5

---

### After Phase 2 (7-11 hours invested)
**Question**: Continue to Phases 4-5 or stop at Phase 3?

**Decision Criteria**:
- **Continue** if: Planning energy/multi-objective research (new directions)
- **Stop** if: Current work focused on performance/safety/robustness only

**Recommendation**: Stop after Phase 3 unless new research directions planned

---

### After Phase 3 (7.5-11.5 hours invested)
**Question**: Implement Phases 4-5 now or defer?

**Decision Criteria**:
- **Implement now** if:
  - Energy optimization is research priority
  - Need Pareto fronts for publication
  - Have computational resources available
- **Defer** if:
  - Categories 1-3 sufficient for current work
  - Computational resources limited
  - Time-sensitive deadline approaching

**Recommendation**: Defer Phases 4-5 unless explicitly needed for research

---

## Cost-Benefit Analysis

| Phase | Effort | Benefit | Value Score | Recommendation |
|-------|--------|---------|-------------|----------------|
| Phase 1 | 1-3 hours | High (Category 1 complete) | 9/10 | **DO NOW** |
| Phase 2 | 6-8 hours | Medium (comprehensive safety) | 6/10 | **RECOMMENDED** |
| Phase 3 | 30 min | Low (archival cleanup) | 4/10 | **OPTIONAL** |
| Phase 4 | 8-10 hours | Low (new research) | 3/10 | **DEFER** |
| Phase 5 | 6-10 hours | Low (advanced research) | 3/10 | **DEFER** |

**Best Value Path**: Phase 1 + Phase 2 = 7-11 hours for 85% of value

---

## Maintenance After Completion

### Update Procedures

**When New PSO Results Added**:
1. Save to appropriate `experiments/<controller>/optimization/` directory
2. Run `create_shortcuts.py` to regenerate shortcuts
3. Update category README with new file details
4. Update `FRAMEWORK_1_FILE_MAPPING.csv`
5. Commit with `[PSO Framework 1]` tag

**When Files Moved/Renamed**:
1. Update target paths in actual locations
2. Re-run `create_shortcuts.py` (auto-detects new paths)
3. Update documentation if file purpose changed
4. Commit changes

**When New Research Task Completed**:
1. Map new files to categories using Framework 1 logic
2. Create shortcuts in appropriate category directories
3. Update cross-reference files (file mapping, gap analysis)
4. Document research provenance in category README

---

## Next Steps

### Immediate Action (Today)
1. Review this plan with stakeholders
2. Decide: Full implementation (Phases 1-5) or partial (Phases 1-2)?
3. If approved, start Phase 1 (1-3 hours)

### Short-term (This Week)
4. Complete Phase 1 (critical gaps)
5. Evaluate need for Phase 2 (safety expansion)
6. If needed, execute Phase 2 (6-8 hours or 2-3 hours parallel)

### Medium-term (This Month)
7. Evaluate need for Phases 4-5 (efficiency, multi-objective)
8. If needed, schedule computational resources
9. Execute Phases 4-5 (14-20 hours or 4-6 hours parallel)

### Long-term (Next Quarter)
10. Maintain Framework 1 as PSO research continues
11. Consider implementing Frameworks 2-6 (by controller, by phase, etc.)
12. Publish research leveraging categorized PSO datasets

---

## Appendix A: Quick Reference Commands

### Phase 1: Critical Gaps
```bash
# Search convergence plots
find experiments/ -name "*convergence*.png" -type f

# Regenerate plots
python scripts/visualization/regenerate_pso_plots.py --logs academic/logs/pso/*phase53*.log

# Verify Classical Phase 2
find experiments/classical_smc/optimization/phases/phase2/ -name "*.json"
```

### Phase 2: Safety Expansion
```bash
# Run chattering PSO (single controller)
python simulate.py --ctrl classical_smc --run-pso --fitness chattering \
    --save experiments/classical_smc/boundary_layer/chattering_optimized.json

# Run chattering PSO (all 3 controllers in parallel)
parallel python simulate.py --ctrl {} --run-pso --fitness chattering \
    --save experiments/{}/boundary_layer/chattering_optimized.json ::: \
    classical_smc adaptive_smc hybrid_adaptive_sta_smc
```

### Phase 3: Robustness Cleanup
```bash
# Search archives
find academic/logs/archive/ -name "*robust*.log"
tar -xzf academic/logs/archive/robust_logs_2025-11.tar.gz
```

### Phase 4: Efficiency Optimization
```bash
# Run energy PSO (parallel, all 4 controllers)
parallel python simulate.py --ctrl {} --run-pso --fitness energy \
    --save experiments/{}/optimization/energy_optimized.json ::: \
    classical_smc sta_smc adaptive_smc hybrid_adaptive_sta_smc
```

### Phase 5: Multi-Objective Optimization
```bash
# Run MOPSO (parallel, all 4 controllers)
parallel python simulate.py --ctrl {} --run-mopso \
    --objectives chattering rmse \
    --save experiments/{}/optimization/pareto_front.json ::: \
    classical_smc sta_smc adaptive_smc hybrid_adaptive_sta_smc
```

---

## Appendix B: Validation Checklist

### After Each Phase

**Phase 1**:
- [ ] Convergence plots exist (3-4 files)
- [ ] Classical Phase 2 verified (found or intentional gap documented)
- [ ] Category 1 README updated
- [ ] FRAMEWORK_1_FILE_MAPPING.csv updated
- [ ] Changes committed and pushed

**Phase 2**:
- [ ] Chattering PSO completed for Classical, Adaptive, Hybrid
- [ ] 15 files created (5 per controller)
- [ ] Chattering reduced ≥3% per controller
- [ ] Comparative report created
- [ ] Category 2 README updated

**Phase 3**:
- [ ] Missing logs searched (archives, .logs/)
- [ ] Logs found or absence documented
- [ ] Category 3 README updated

**Phase 4**:
- [ ] Energy PSO completed for all 4 controllers
- [ ] 16 files created (4 per controller + 1 report)
- [ ] Energy reduced ≥20%, RMSE increase ≤10%
- [ ] Trade-off plots generated
- [ ] Category 4 README updated

**Phase 5**:
- [ ] MOPSO completed for all 4 controllers
- [ ] 24 files created (6 per controller + 2 reports)
- [ ] Pareto fronts contain ≥50 solutions
- [ ] Hypervolume computed
- [ ] Best solutions selected
- [ ] Category 5 README updated

---

## Contact & Approval

**Plan Author**: AI Workspace (Claude Code)
**Plan Date**: 2025-12-30
**Plan Version**: 1.0

**Approval Required From**:
- Project lead (for go/no-go decision)
- Computational resources manager (for parallel execution)

**Questions/Feedback**: See `.ai_workspace/pso/by_purpose/README.md`

---

**[Framework 1 Root](README.md)** | **[Gap Analysis](FRAMEWORK_1_GAP_ANALYSIS.md)** | **[File Mapping](FRAMEWORK_1_FILE_MAPPING.csv)** | **[Category 1](1_performance/README.md)**
