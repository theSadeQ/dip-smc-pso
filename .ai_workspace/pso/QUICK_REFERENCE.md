# PSO Categorization System - Quick Reference

**Last Updated:** January 5, 2026
**Framework Status:** Framework 1 OPERATIONAL (73% complete)
**Navigation Time:** 2-3 minutes to find any PSO artifact

---

## Quick Navigation by Goal

### "I need production-ready gains for [controller]"

```bash
# Navigate to Performance category
cd .ai_workspace/pso/by_purpose/1_performance/phase53/

# Available controllers:
# - classical_smc_phase53.txt
# - sta_smc_phase53.txt
# - adaptive_smc_phase53.txt
# - hybrid_adaptive_sta_phase53.txt
```

**Best Performance:** Adaptive SMC (RMSE: 0.0289, 40.4% better than Classical)

---

### "I need robust gains for disturbance rejection"

```bash
# Navigate to Robustness category
cd .ai_workspace/pso/by_purpose/3_robustness/mt8_disturbance/

# Best performer: Hybrid Adaptive STA SMC (+21.4% improvement)
cat mt8_repro_hybrid.txt
```

**MT-8 Results:** Hybrid best (+21.4%), average improvement 6.35% across all controllers

---

### "I need low-chattering gains"

```bash
# Navigate to Safety category
cd .ai_workspace/pso/by_purpose/2_safety/

# Classical SMC (boundary layer optimization)
cd classical_phase2_boundary/

# STA SMC (MT-6 adaptive boundary layer)
cd sta_mt6_boundary/
```

**Finding:** Adaptive boundary layers provide marginal improvement (3.7%), fixed ε=0.02 near-optimal

---

### "I want to see PSO convergence plots"

```bash
# Navigate to Performance visualization
cd .ai_workspace/pso/by_purpose/1_performance/convergence_plots/

# Available:
# - sta_smc_convergence.txt
# - adaptive_smc_convergence.txt
# - hybrid_adaptive_sta_convergence.txt
```

---

### "I need statistical validation data (MT-7)"

```bash
# Navigate to Robustness validation
cd .ai_workspace/pso/by_purpose/3_robustness/mt7_validation/

# 15 files: multi-seed validation results (10 seeds × 50 runs)
```

**MT-7 Finding:** 50.4x performance degradation across seeds (overfitting detected in narrow IC range)

---

## Quick Navigation by Controller

### Classical SMC

```bash
# Performance
.ai_workspace/pso/by_purpose/1_performance/phase53/classical_smc_phase53.txt

# Robustness
.ai_workspace/pso/by_purpose/3_robustness/phase2_robust/pso_classical_smc_robust.txt

# Safety (boundary layer)
.ai_workspace/pso/by_purpose/2_safety/classical_phase2_boundary/
```

### STA SMC

```bash
# Performance
.ai_workspace/pso/by_purpose/1_performance/phase53/sta_smc_phase53.txt

# Robustness
.ai_workspace/pso/by_purpose/3_robustness/mt8_disturbance/mt8_repro_sta_smc.txt

# Safety (MT-6 boundary layer)
.ai_workspace/pso/by_purpose/2_safety/sta_mt6_boundary/
```

### Adaptive SMC

```bash
# Performance (BEST - RMSE: 0.0289)
.ai_workspace/pso/by_purpose/1_performance/phase53/adaptive_smc_phase53.txt

# Robustness
.ai_workspace/pso/by_purpose/3_robustness/mt8_disturbance/mt8_repro_adaptive_smc.txt

# Safety: N/A (no boundary layer support)
```

### Hybrid Adaptive STA SMC

```bash
# Performance
.ai_workspace/pso/by_purpose/1_performance/phase53/hybrid_adaptive_sta_phase53.txt

# Robustness (BEST for MT-8 +21.4%)
.ai_workspace/pso/by_purpose/3_robustness/mt8_disturbance/mt8_repro_hybrid.txt

# Safety: N/A (no boundary layer support)
```

---

## Quick Navigation by Research Task

### QW-3: PSO Visualization
```bash
cd .ai_workspace/pso/by_purpose/1_performance/source/
# File: pso_plots_source.txt
```

### MT-5: Comprehensive Benchmarking
```bash
cd .ai_workspace/pso/by_purpose/1_performance/phase53/
# All 4 controllers available
```

### MT-6: Boundary Layer Optimization
```bash
cd .ai_workspace/pso/by_purpose/2_safety/sta_mt6_boundary/
# 2 files (STA SMC only, Classical in classical_phase2_boundary/)
```

### MT-7: Multi-Seed Statistical Validation
```bash
cd .ai_workspace/pso/by_purpose/3_robustness/mt7_validation/
# 15 files (10 seeds × 50 runs)
```

### MT-8: Disturbance Rejection
```bash
cd .ai_workspace/pso/by_purpose/3_robustness/mt8_disturbance/
# 9 files (4 controllers + analysis)
```

### LT-7: Research Paper Figures
```bash
cd .ai_workspace/pso/by_purpose/1_performance/lt7_figures/
# 2 files (publication-ready)
```

### Phase 2: Standard PSO
```bash
# Performance
cd .ai_workspace/pso/by_purpose/1_performance/phase2/

# Robustness
cd .ai_workspace/pso/by_purpose/3_robustness/phase2_robust/
```

### Phase 53: Progressive Refinement
```bash
cd .ai_workspace/pso/by_purpose/1_performance/phase53/
# All 4 controllers available
```

---

## File Types Quick Reference

### Gain Files (.json)
**Location:** `**/gains/` or `**/phase53/` or `**/phase2/`
**Format:** `{"controller_name": [gain1, gain2, ..., gainN]}`
**Count:** 23 files total

### Data Files (.csv, .json, .npz)
**Location:** `**/mt7_validation/`, `**/mt8_disturbance/`, `**/data/`
**Format:** Tabular (CSV), summaries (JSON), time-series (NPZ)
**Count:** 70+ files

### Log Files (.log shortcuts as .txt)
**Location:** `**/logs/`
**Format:** Shortcut text files pointing to `academic/logs/pso/*.log`
**Count:** 13+ files (7 in robustness category)

### Source Code (.py shortcuts as .txt)
**Location:** `**/source/`
**Count:** 6 files

### Reports (.md)
**Location:** Documented in parent category READMEs
**Count:** 42+ files (referenced)

### Visualizations (.png)
**Location:** `**/convergence_plots/`, `**/lt7_figures/`
**Count:** 5 shortcuts (actual: 16 files in experiments/)

---

## Common Tasks

### Compare Performance vs Robustness for Same Controller

```bash
# Example: STA SMC

# Performance-optimized (Phase 53)
cat .ai_workspace/pso/by_purpose/1_performance/phase53/sta_smc_phase53.txt

# Robustness-optimized (Phase 2 Robust)
cat .ai_workspace/pso/by_purpose/3_robustness/phase2_robust/pso_sta_smc_robust.txt

# Trade-off: Robust gains sacrifice ~5-10% nominal performance for +15-20% disturbance rejection
```

### Find Best Controller for Application

| Application | Recommended Controller | Gains Location |
|-------------|----------------------|----------------|
| **Maximum Accuracy** | Adaptive SMC | `1_performance/phase53/adaptive_smc_phase53.txt` |
| **Best Robustness** | Hybrid Adaptive STA | `3_robustness/mt8_disturbance/mt8_repro_hybrid.txt` |
| **Low Chattering** | STA SMC (MT-6) | `2_safety/sta_mt6_boundary/` |
| **Balanced (Production)** | Hybrid Adaptive STA | `1_performance/phase53/hybrid_adaptive_sta_phase53.txt` |
| **Simplest** | Classical SMC | `1_performance/phase53/classical_smc_phase53.txt` |

### Reproduce Research Task Results

```bash
# Step 1: Find task directory
cd .ai_workspace/pso/by_purpose/[category]/[task_name]/

# Step 2: Read shortcut to get actual file path
cat [shortcut_file].txt

# Step 3: Load gains or data from actual path
# (Shortcut file's last line contains the full path)
```

### Load Gains in Python

```python
import json
from pathlib import Path

# Read shortcut
shortcut = Path(".ai_workspace/pso/by_purpose/1_performance/phase53/adaptive_smc_phase53.txt")
with open(shortcut) as f:
    lines = f.readlines()
    actual_path = Path(lines[-1].strip())  # Last line has path

# Load gains
with open(actual_path) as f:
    gains_data = json.load(f)
    gains = gains_data["adaptive_smc"]  # Adjust key to controller name

print(f"Loaded {len(gains)} gains for Adaptive SMC")
```

---

## Category Status

| Category | Files | Coverage | Status | Use When |
|----------|-------|----------|--------|----------|
| **1. Performance** | 20/21 | 95% | ✅ OPERATIONAL | Maximizing accuracy, minimizing RMSE |
| **2. Safety** | 6/18 | 53% | ⚠️ PARTIAL | Reducing chattering, boundary layer tuning |
| **3. Robustness** | 49/48 | 98% | ✅ OPERATIONAL | Disturbance rejection, uncertainty handling |
| **4. Efficiency** | 2/17 | 15% | ⚠️ INFRASTRUCTURE | Energy minimization (not yet run) |
| **5. Multi-Objective** | 13/25 | 25% | ⚠️ PARTIAL | Pareto trade-offs (implicit MT-8 only) |

**Overall:** 78/133 files organized (59% actual data + 19% infrastructure)

---

## Directory Structure

```
.ai_workspace/pso/by_purpose/
├── README.md (master overview, 6,200 lines)
├── IMPLEMENTATION_STATUS.md
├── FRAMEWORK_1_FILE_MAPPING.csv (90 entries)
├── create_shortcuts.py (automation)
│
├── 1_performance/ (20 files, 95% complete)
│   ├── phase53/ (5 gain files)
│   ├── phase2/ (4 gain files)
│   ├── convergence_plots/ (3 plots)
│   ├── lt7_figures/ (2 publication figs)
│   ├── config/ (1 file)
│   └── source/ (6 files)
│
├── 2_safety/ (6 files, 53% partial)
│   ├── classical_phase2_boundary/ (3 files)
│   ├── sta_mt6_boundary/ (2 files)
│   └── config/ (1 file)
│
├── 3_robustness/ (49 files, 98% complete)
│   ├── mt7_validation/ (15 files)
│   ├── mt8_disturbance/ (9 files)
│   ├── phase2_robust/ (5 files)
│   ├── logs/ (7 files) [UPDATED: +3 phase2 logs]
│   ├── config/ (1 file)
│   └── source/ (3 files)
│
├── 4_efficiency/ (2 files, 15% infrastructure)
│   ├── source/ (1 file)
│   └── config/ (1 file)
│
└── 5_multi_objective/ (13 files, 25% partial)
    ├── source/ (3 files)
    ├── config/ (1 file)
    └── mt8_implicit/ (9 files, dual-categorized)
```

---

## Performance Benchmarks

### RMSE (Lower = Better)

| Controller | Phase 53 | Phase 2 | MT-8 Robust | Improvement vs Classical |
|------------|----------|---------|-------------|--------------------------|
| Adaptive SMC | **0.0289** | 0.0312 | 0.0335 | **+40.4%** (best) |
| Hybrid Adaptive STA | 0.0315 | 0.0340 | 0.0298 | +35.1% |
| STA SMC | 0.0398 | 0.0425 | 0.0380 | +17.9% |
| Classical SMC | 0.0485 | 0.0510 | 0.0465 | baseline |

### Disturbance Rejection (MT-8, Higher = Better)

| Controller | Improvement vs Baseline | Rank |
|------------|------------------------|------|
| Hybrid Adaptive STA | **+21.4%** | 1st |
| Adaptive SMC | +8.2% | 2nd |
| STA SMC | +6.1% | 3rd |
| Classical SMC | +3.5% | 4th |

### Chattering Reduction (Lower = Better)

| Controller | Approach | Chattering Reduction | Finding |
|------------|----------|---------------------|---------|
| STA SMC | MT-6 adaptive ε | **3.7%** | Marginal, fixed ε=0.02 better |
| Classical SMC | Phase 2 boundary layer | ~5-10% | Effective for Classical |
| Adaptive SMC | N/A | N/A | No boundary layer |
| Hybrid | N/A | N/A | No boundary layer |

---

## Tips & Tricks

### Fast Search

```bash
# Search all categories for specific controller
find .ai_workspace/pso/by_purpose -name "*adaptive_smc*" -type f

# Search by task
find .ai_workspace/pso/by_purpose -name "*mt8*" -type f

# Count shortcuts per category
for dir in .ai_workspace/pso/by_purpose/*/; do
  echo "$dir: $(find $dir -name "*.txt" | wc -l) files"
done
```

### Batch Load All Gains

```python
from pathlib import Path
import json

def load_all_phase53_gains():
    phase53_dir = Path(".ai_workspace/pso/by_purpose/1_performance/phase53")
    gains = {}

    for shortcut in phase53_dir.glob("*.txt"):
        with open(shortcut) as f:
            lines = f.readlines()
            actual_path = Path(lines[-1].strip())

        with open(actual_path) as f:
            data = json.load(f)
            controller = shortcut.stem.replace("_phase53", "")
            gains[controller] = data.get(controller.replace("_", " ").title())

    return gains

# Usage
all_gains = load_all_phase53_gains()
print(f"Loaded gains for {len(all_gains)} controllers")
```

### Regenerate All Shortcuts

```bash
cd .ai_workspace/pso/by_purpose
python create_shortcuts.py
# Regenerates all 67 shortcuts in seconds
```

---

## Troubleshooting

### "Shortcut file not found"

Check category completeness in main README.md - some categories only 15-53% complete.

### "Actual file doesn't exist"

Verify path in last line of shortcut file. File may have been moved/archived.

### "Want framework by maturity/task/filetype/strategy"

Only Framework 1 (By Purpose) is implemented. See planning docs for Frameworks 2-6.

### "Can't find specific controller"

Some controllers have limited PSO coverage:
- Swing-Up SMC: 20% coverage (2/10 scenarios)
- MPC: 0% coverage (N/A)
- Conditional Hybrid SMC: 0% coverage (NEW, not yet optimized)

---

## Maintenance

**Weekly:**
```bash
python .ai_workspace/pso/by_purpose/create_shortcuts.py
# Regenerates shortcuts, validates links
```

**Monthly:**
- Review category completion percentages
- Update this quick reference with new research tasks
- Archive superseded gains

**As Needed:**
- Add new shortcuts when new PSO runs complete
- Update performance benchmarks
- Document new findings

---

## Additional Resources

- **Master Plan:** `.ai_workspace/planning/PSO_CATEGORIZATION_MASTER_PLAN.md` (38 pages)
- **Status Report:** `.ai_workspace/planning/PSO_COMPREHENSIVE_STATUS_REPORT.md` (complete analysis)
- **Implementation Guide:** `.ai_workspace/planning/PSO_IMPLEMENTATION_QUICKSTART.md`
- **Framework README:** `.ai_workspace/pso/by_purpose/README.md` (6,200 lines)
- **File Mapping:** `.ai_workspace/pso/by_purpose/FRAMEWORK_1_FILE_MAPPING.csv` (90 entries)

---

**Version:** 1.0
**Last Updated:** January 5, 2026
**Maintained By:** AI Workspace (Claude Code)
**Status:** Framework 1 operational, 2-3 min navigation achieved
