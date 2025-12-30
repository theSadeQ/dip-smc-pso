# Category 1: Performance-Focused PSO

**Framework 1: By Purpose/Objective**
**Category**: Performance Optimization (RMSE, settling time, tracking accuracy)
**Status**: 95% Complete (20/21 files) - [OPERATIONAL]
**Last Updated**: 2025-12-30 (Phase 1 gaps closed)

---

## Overview

This category contains all PSO optimization files focused on **performance objectives**: tracking accuracy (RMSE), settling time, overshoot reduction, and steady-state error minimization.

**Primary Objectives**:
- Minimize RMSE (Root Mean Square Error)
- Reduce settling time
- Improve tracking accuracy
- Minimize steady-state error

**Controllers Covered**: Classical SMC, STA SMC, Adaptive SMC, Hybrid Adaptive STA

---

## Quick Navigation

```
1_performance/
├─ phase53/              [5 files] Phase 53 optimization (baseline RMSE)
├─ phase2_standard/      [4 files] Phase 2 standard conditions
├─ convergence_plots/    [3 files] PSO convergence plots (STA, Adaptive, Hybrid)
├─ lt7_figures/          [2 files] LT-7 research paper figures
├─ config/               [1 file]  Config reference (lines 39-83, 186-229)
└─ source/               [6 files] Source code (algorithms, objectives, viz)
```

**Total**: 20 files (shortcuts to 21 actual files, Classical Phase 2 intentionally excluded)

---

## File Organization

### Phase 53 Gains (5 files) - [OK] COMPLETE

**Purpose**: Baseline RMSE optimization for all controllers (Phase 53 standard optimization)

| File | Controller | Optimization | RMSE | Notes |
|------|-----------|--------------|------|-------|
| `classical_smc_phase53.txt` | Classical SMC | Standard PSO | 0.0485 | Baseline performance |
| `sta_smc_phase53.txt` | STA SMC | Standard PSO | 0.0312 | 35.7% better than classical |
| `sta_smc_lyapunov_optimized.txt` | STA SMC | Lyapunov-based | 0.0328 | Alternative method (5.1% worse) |
| `adaptive_smc_phase53.txt` | Adaptive SMC | Standard PSO | 0.0289 | Best performance |
| `hybrid_adaptive_sta_phase53.txt` | Hybrid | Standard PSO | 0.0295 | 2nd best, robust |

**Research Provenance**: Phase 53 (baseline optimization), QW-1 (documentation), MT-5 (comprehensive benchmark)

**Usage**:
```python
# Load Phase 53 gains
import json
with open("experiments/sta_smc/optimization/phases/phase53/optimized_gains_sta_smc_phase53.json") as f:
    gains = json.load(f)
```

---

### Phase 2 Standard Gains (4 files) - [OK] COMPLETE

**Purpose**: Phase 2 standard conditions (nominal performance before robust optimization)

| File | Controller | RMSE | Chattering | Notes |
|------|-----------|------|-----------|-------|
| `sta_smc_standard.txt` | STA SMC | 0.0312 | 2.42 | Standard conditions |
| `adaptive_smc_standard.txt` | Adaptive SMC | 0.0289 | 1.87 | Best chattering-performance |
| `hybrid_adaptive_sta_standard.txt` | Hybrid | 0.0295 | 2.01 | Balanced |
| `sta_smc_baseline.txt` | STA SMC | 0.0328 | 2.56 | Early baseline |

**Research Provenance**: Phase 2 (initial optimization), MT-5 (validation)

**Note**: Classical SMC Phase 2 gains are missing from this category (see Gap Analysis).

---

### Convergence Plots (3 files) - [OK] COMPLETE

**Purpose**: PSO convergence visualization (fitness vs iteration, diversity metrics)

| File | Controller | Location | Status |
|------|-----------|----------|--------|
| `sta_smc_convergence.txt` | STA SMC | `sta_smc/optimization/active/` | [OK] Found |
| `adaptive_smc_convergence.txt` | Adaptive SMC | `adaptive_smc/optimization/active/` | [OK] Found |
| `hybrid_adaptive_sta_convergence.txt` | Hybrid | `hybrid_adaptive_sta/optimization/active/` | [OK] Found |

**Missing**:
- Classical SMC convergence plot (not generated - Classical has no active PSO convergence visualization)

**Research Provenance**: Phase 53 optimization, QW-3 (PSO visualization)

---

### LT7 Publication Figures (2 files) - [OK] COMPLETE

**Purpose**: Publication-ready PSO figures for LT-7 research paper

| File | Section | Description | Metrics |
|------|---------|-------------|---------|
| `LT7_section_5_1_pso_convergence.txt` | 5.1 | PSO convergence analysis | Fitness vs iteration, diversity |
| `LT7_section_8_3_pso_generalization.txt` | 8.3 | Generalization performance | Cross-seed validation, robustness |

**Research Provenance**: LT-7 (research paper), QW-3 (PSO visualization)

**Note**: These are high-quality publication figures with proper formatting, labels, and academic styling.

---

### Config Reference (1 file) - [OK] COMPLETE

**File**: `config_performance_section.txt` → `config.yaml`

**Relevant Sections**:
- **Lines 39-83**: Controller default gains (optimized by MT-8)
- **Lines 186-229**: PSO parameter bounds (λ, k, φ, boundary layer)

**Key Performance Parameters**:
```yaml
# config.yaml (lines 186-229)
pso:
  bounds:
    classical_smc:
      lambda1: [5.0, 50.0]   # Sliding surface gain (angle 1)
      lambda2: [5.0, 50.0]   # Sliding surface gain (angle 2)
      k1: [10.0, 100.0]      # Control gain (angle 1)
      k2: [10.0, 100.0]      # Control gain (angle 2)
    # ... (see config.yaml for full bounds)
```

---

### Source Code (6 files) - [OK] COMPLETE

**Purpose**: PSO implementation and performance objectives

| File | Module | Description | Lines |
|------|--------|-------------|-------|
| `pso_optimizer.txt` | `algorithms/pso_optimizer.py` | Core PSO algorithm (PySwarms wrapper) | 450 |
| `swarm_pso.txt` | `algorithms/swarm/pso.py` | Swarm-based PSO variants | 320 |
| `cost_evaluator.txt` | `core/cost_evaluator.py` | Fitness function evaluation | 280 |
| `tracking_objectives.txt` | `objectives/control/tracking.py` | RMSE, settling time, overshoot | 215 |
| `stability_objectives.txt` | `objectives/control/stability.py` | Lyapunov stability objectives | 180 |
| `pso_visualization.txt` | `utils/visualization/pso_plots.py` | Convergence/diversity plots (QW-3) | 340 |

**Key Functions**:
```python
# From tracking_objectives.py
def compute_rmse(state_history, target_angles):
    """Compute Root Mean Square Error for tracking."""
    # RMSE = sqrt(mean((θ_actual - θ_target)^2))

# From pso_optimizer.py
def optimize_gains(controller, dynamics, bounds, n_particles=30, n_iterations=100):
    """Run PSO optimization for controller gains."""
```

---

## Coverage Matrix

| Controller | Phase 53 | Phase 2 Std | Convergence | LT7 Figs | Config | Source |
|-----------|----------|-------------|-------------|----------|--------|--------|
| Classical SMC | [OK] | N/A (intentional) | [ERROR] Missing | N/A | [OK] | [OK] |
| STA SMC | [OK] x2 | [OK] x2 | [OK] | [OK] x2 | [OK] | [OK] |
| Adaptive SMC | [OK] | [OK] | [OK] | N/A | [OK] | [OK] |
| Hybrid | [OK] | [OK] | [OK] | N/A | [OK] | [OK] |

**Status**:
- [OK] Complete: 20/21 files (95.2%)
- [ERROR] Missing: 1/21 files (4.8%)
  - Classical SMC convergence plot (1 file - not generated)

**Note**: Classical SMC Phase 2 is NOT a gap - Classical controller only had Phase 53 optimization, not Phase 2

---

## Research Task Provenance

| Research Task | Description | Files in Category | Status |
|--------------|-------------|-------------------|--------|
| **QW-1** | Theory docs + baseline benchmarks | 0 (theory only) | [OK] |
| **QW-3** | PSO visualization system | 1 (pso_plots.py) | [OK] |
| **MT-5** | Comprehensive controller benchmark | 9 (Phase 53 + Phase 2) | [OK] |
| **LT-7** | Research paper (submission-ready) | 2 (LT7 figures) | [OK] |
| **Phase 53** | Baseline optimization run | 5 (all controllers) | [OK] |
| **Phase 2** | Standard conditions optimization | 4 (missing classical) | [PARTIAL] |

---

## Gap Analysis

### Phase 1 Results (2025-12-30)

**✅ RESOLVED: Convergence Plots**
- **Status**: 3/3 found (STA, Adaptive, Hybrid)
- **Location**: `academic/paper/experiments/*/optimization/active/*_convergence.png`
- **Shortcuts Created**: Yes

**✅ RESOLVED: Classical Phase 2**
- **Status**: NOT A GAP - Classical controller only has Phase 53 (by design)
- **Verification**: Only STA, Adaptive, Hybrid have Phase 2 directories
- **Documentation Updated**: Coverage matrix reflects intentional exclusion

### Priority 1: Remaining Critical Gap

**1. Classical SMC Convergence Plot (1 file missing)**
- **Impact**: Cannot visualize Classical SMC PSO optimization progress
- **Status**: Plot was not generated during Classical optimization
- **Effort**: 30 min - 1 hour (regenerate from logs if available)
- **Action**:
  ```bash
  # Check if logs exist
  find academic/logs/pso/ -name "*classical*phase53*.log"

  # Regenerate plot if logs exist
  python scripts/visualization/regenerate_pso_plots.py \
      --logs academic/logs/pso/classical_smc_phase53.log \
      --output academic/paper/experiments/classical_smc/optimization/active/
  ```

### Priority 2: Enhancement Gaps

**3. Additional Metrics (not tracked)**
- **Current**: Only RMSE tracked
- **Missing**: Settling time, overshoot, steady-state error (calculated but not saved)
- **Effort**: 2-3 hours (modify fitness logging)
- **Action**: Update `cost_evaluator.py` to save all metrics

**4. Cross-Controller Comparison Figures**
- **Current**: 2 LT7 figures
- **Missing**: Comparative bar charts, Pareto fronts
- **Effort**: 1-2 hours (use existing data)
- **Action**: Create comparative plots from Phase 53 results

---

## Usage Examples

### 1. Load Optimized Gains

```python
import json
from pathlib import Path

# Load best performance gains (Adaptive SMC Phase 53)
gains_path = Path("experiments/adaptive_smc/optimization/phases/phase53/optimized_gains_adaptive_smc_phase53.json")
with open(gains_path) as f:
    gains = json.load(f)

print(f"Lambda: {gains['lambda']}")
print(f"K: {gains['k']}")
print(f"RMSE: {gains['rmse']:.4f}")  # 0.0289
```

### 2. Compare Performance Across Controllers

```python
from pathlib import Path
import json

controllers = ["classical_smc", "sta_smc", "adaptive_smc", "hybrid_adaptive_sta"]
results = {}

for ctrl in controllers:
    gains_file = Path(f"experiments/{ctrl}/optimization/phases/phase53/optimized_gains_{ctrl}_phase53.json")
    if gains_file.exists():
        with open(gains_file) as f:
            data = json.load(f)
            results[ctrl] = data['rmse']

# Sort by performance
sorted_results = sorted(results.items(), key=lambda x: x[1])
print("Controller Performance Ranking (best to worst):")
for ctrl, rmse in sorted_results:
    print(f"{ctrl}: RMSE = {rmse:.4f}")
```

**Expected Output**:
```
Controller Performance Ranking (best to worst):
adaptive_smc: RMSE = 0.0289
hybrid_adaptive_sta: RMSE = 0.0295
sta_smc: RMSE = 0.0312
classical_smc: RMSE = 0.0485
```

### 3. Visualize PSO Convergence (when plots available)

```python
from PIL import Image
import matplotlib.pyplot as plt

# Load convergence plot
convergence_plot = Image.open("experiments/sta_smc/optimization/active/pso_convergence_sta_smc.png")
plt.imshow(convergence_plot)
plt.axis('off')
plt.title("STA SMC PSO Convergence")
plt.show()
```

---

## Related Categories

**Cross-References**:
- **Category 2 (Safety)**: MT-6 boundary layer optimization (trades performance for chattering reduction)
- **Category 3 (Robustness)**: MT-7/MT-8 robust PSO (trades nominal performance for disturbance rejection)
- **Category 5 (Multi-Objective)**: MOPSO for Pareto-optimal performance-chattering trade-offs

**Trade-offs**:
- Performance vs Safety: Increasing boundary layer (ε) reduces chattering but increases RMSE
- Performance vs Robustness: Robust PSO (MT-8) increases worst-case performance by 6.35% but reduces nominal performance by 2-3%

---

## Metrics Summary

| Metric | Classical | STA | Adaptive | Hybrid | Best |
|--------|-----------|-----|----------|--------|------|
| **RMSE** | 0.0485 | 0.0312 | **0.0289** | 0.0295 | Adaptive |
| **vs Classical** | - | -35.7% | **-40.4%** | -39.2% | Adaptive |
| **Chattering** (Phase 2) | N/A | 2.42 | **1.87** | 2.01 | Adaptive |
| **Optimization Time** | 12 min | 15 min | 18 min | 20 min | Classical |

**Source**: Phase 53 optimization results (Oct-Nov 2025), MT-5 comprehensive benchmark

---

## Next Steps

### Immediate (1-3 hours)
1. Locate/regenerate convergence plots (Priority 1, Gap #1)
2. Find Classical SMC Phase 2 standard gains (Priority 1, Gap #2)
3. Update coverage to 100% (21/21 files)

### Short-term (1-2 weeks)
4. Create cross-controller comparison figures (Priority 2, Gap #4)
5. Add settling time and overshoot metrics to logs (Priority 2, Gap #3)
6. Document trade-offs with other categories (safety, robustness)

### Long-term (1-2 months)
7. Run energy-focused PSO (Category 4 expansion)
8. Create Pareto fronts for performance vs chattering (Category 5)
9. Publish LT-7 paper with all performance figures

---

## Appendix: File Shortcut Format

All `.txt` files in this category are **shortcuts** pointing to actual data files. Format:

```
# PSO Framework 1: By Purpose/Objective
# Category: Performance
# Purpose: <optimization objective>
# Notes: <additional context>

Target Path:
<full path to actual file>

# To view this file:
# Windows: start <path>
# OR: Open the path above in your file explorer
```

**Example**:
```
# PSO Framework 1: By Purpose/Objective
# Category: Performance
# Purpose: Baseline RMSE optimization - STA SMC
# Notes: Phase 53 standard optimization

Target Path:
D:\Projects\main\experiments\sta_smc\optimization\phases\phase53\optimized_gains_sta_smc_phase53.json

# To view this file:
# Windows: start D:\Projects\main\experiments\sta_smc\optimization\phases\phase53\optimized_gains_sta_smc_phase53.json
# OR: Open the path above in your file explorer
```

---

## Contact & Contributions

**Maintainer**: AI Workspace (Claude Code)
**Last Review**: 2025-12-30
**Framework Version**: 1.0

**Report Issues**: `.ai_workspace/pso/FRAMEWORK_1_GAP_ANALYSIS.md`
**Suggest Additions**: `.ai_workspace/planning/BACKLOG.md`

---

**[Framework 1 Root](../README.md)** | **[All Categories](../README.md#categories)** | **[Next: Category 2 (Safety)](../2_safety/README.md)**
