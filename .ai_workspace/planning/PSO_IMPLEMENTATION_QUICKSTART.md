# PSO Framework Implementation - Quick Start Guide

**Created:** December 30, 2025
**Updated:** December 31, 2025 (added Regional Hybrid SMC)
**Purpose:** Fast implementation guide for PSO categorization frameworks
**Time to Complete:** 3-5 hours (Phase 1 only)

---

## Phase 1: Create Reference Structure (Immediate)

### Step 1: Create Directory Structure (15 minutes)

```bash
# Navigate to workspace
cd D:\Projects\main\.ai_workspace

# Create PSO workspace root
mkdir pso
cd pso

# Create 6 framework directories
mkdir by_purpose by_maturity by_task by_filetype by_controller by_strategy

# Create subdirectories for Framework 1 (Purpose)
mkdir by_purpose\performance
mkdir by_purpose\safety
mkdir by_purpose\robustness
mkdir by_purpose\efficiency
mkdir by_purpose\multi_objective

# Create subdirectories for Framework 2 (Maturity)
mkdir by_maturity\level_1_theoretical
mkdir by_maturity\level_2_simulation
mkdir by_maturity\level_3_statistical
mkdir by_maturity\level_4_robustness
mkdir by_maturity\level_5_hardware
mkdir by_maturity\level_6_production
mkdir by_maturity\level_7_archived

# Create subdirectories for Framework 3 (Task)
mkdir by_task\QW-3_visualization
mkdir by_task\MT-6_boundary_layer
mkdir by_task\MT-7_robustness
mkdir by_task\MT-8_disturbance
mkdir by_task\LT-6_uncertainty
mkdir by_task\phase_based

# Create subdirectories for Framework 4 (Filetype)
mkdir by_filetype\config
mkdir by_filetype\gains
mkdir by_filetype\data
mkdir by_filetype\reports
mkdir by_filetype\visualizations
mkdir by_filetype\logs
mkdir by_filetype\source

# Create subdirectories for Framework 5 (Controller)
mkdir by_controller\classical
mkdir by_controller\classical\classical_smc
mkdir by_controller\classical\sta_smc
mkdir by_controller\adaptive
mkdir by_controller\adaptive\adaptive_smc
mkdir by_controller\adaptive\hybrid_adaptive_sta
mkdir by_controller\adaptive\regional_hybrid_smc
mkdir by_controller\specialized
mkdir by_controller\specialized\swing_up_smc
mkdir by_controller\specialized\mcp

# Create subdirectories for Framework 6 (Strategy)
mkdir by_strategy\single_objective
mkdir by_strategy\robust_multiscenario
mkdir by_strategy\statistical_validation
mkdir by_strategy\multi_objective
mkdir by_strategy\adaptive_online

# Create tools directory
mkdir tools

# Create reports directory
mkdir reports
```

---

### Step 2: Create Master README (30 minutes)

Create `.ai_workspace\pso\README.md`:

```markdown
# PSO Optimization Workspace

**Purpose:** Comprehensive categorization system for PSO optimization work
**Total Files:** 153 PSO-related files
**Total Scenarios:** 60 optimization scenarios
**Controllers:** 8 (5 core + 3 experimental, including new Regional Hybrid SMC)

---

## Quick Navigation

### By Your Goal

**I want to...**
- Find production-ready gains → [by_maturity/level_6_production/](by_maturity/level_6_production/)
- Understand robustness optimization → [by_purpose/robustness/](by_purpose/robustness/)
- Debug MT-8 execution → [by_task/MT-8_disturbance/](by_task/MT-8_disturbance/)
- Compare controllers → [by_controller/](by_controller/)
- Learn about PSO algorithms → [by_strategy/](by_strategy/)

### By Framework

1. **[by_purpose/](by_purpose/)** - Categorized by optimization goal (performance, safety, robustness)
2. **[by_maturity/](by_maturity/)** - Categorized by validation level (TRL 1-7)
3. **[by_task/](by_task/)** - Categorized by research task (MT-6, MT-7, MT-8, etc.)
4. **[by_filetype/](by_filetype/)** - Categorized by artifact type (gains, data, reports, logs)
5. **[by_controller/](by_controller/)** - Categorized by controller architecture
6. **[by_strategy/](by_strategy/)** - Categorized by PSO algorithm variant

---

## Framework Coverage

| Framework | Coverage | Files Organized | Status |
|-----------|----------|-----------------|--------|
| Framework 1: Purpose | 65% | TBD | In Progress |
| Framework 2: Maturity | 85% | TBD | In Progress |
| Framework 3: Task | 100% | TBD | Complete |
| Framework 4: Filetype | 100% | TBD | Complete |
| Framework 5: Controller | 100% | TBD | Complete |
| Framework 6: Strategy | 60% | TBD | In Progress |

**Overall:** 78% complete

---

## Quick Reference

### File Counts by Type
- Configuration: 3 files
- Gains: 23 files (JSON)
- Data: 70 files (CSV/JSON/NPZ)
- Reports: 42 files (Markdown)
- Visualizations: 16 files (PNG, 3.6 MB)
- Logs: 6 files (978 KB)
- Source: 3 files (Python)

### Controllers
- Classical SMC: 80% coverage (8/10 scenarios)
- STA SMC: 90% coverage (9/10 scenarios)
- Adaptive SMC: 75% coverage (7.5/10 scenarios)
- Hybrid Adaptive STA: 85% coverage (8.5/10 scenarios)
- Regional Hybrid SMC: 0% coverage (NEW - Dec 31, 2025, PSO pending)
- Swing-Up SMC: 20% coverage (2/10 scenarios)
- MPC: 0% coverage (N/A)

---

## Documentation

- **Master Plan:** [../planning/PSO_CATEGORIZATION_MASTER_PLAN.md](../planning/PSO_CATEGORIZATION_MASTER_PLAN.md)
- **Quick Start:** [../planning/PSO_IMPLEMENTATION_QUICKSTART.md](../planning/PSO_IMPLEMENTATION_QUICKSTART.md)
- **Status Report:** [../planning/PSO_COMPREHENSIVE_STATUS_REPORT.md](../planning/PSO_COMPREHENSIVE_STATUS_REPORT.md)

---

## Usage Examples

### Example 1: Find MT-8 Disturbance Rejection Data
```bash
cd by_task/MT-8_disturbance/
# Or
cd by_purpose/robustness/MT-8/
```

### Example 2: Get Production Gains for Hybrid Controller
```bash
cd by_maturity/level_6_production/
# Look for hybrid_adaptive_sta gains
```

### Example 3: Compare PSO Algorithms
```bash
cd by_strategy/
cat README.md  # Algorithm comparison table
```

---

## Maintenance

**Weekly:** Run validation script (5 minutes)
```bash
python tools/validate_framework_links.py
```

**Monthly:** Update coverage dashboard (15 minutes)
```bash
python tools/generate_coverage_dashboard.py
```

---

## Contact

**Questions?** See [PSO_CATEGORIZATION_MASTER_PLAN.md](../planning/PSO_CATEGORIZATION_MASTER_PLAN.md) Section 6 (Usage Guidelines)

**Last Updated:** December 30, 2025
```

---

### Step 3: Create Framework READMEs (90 minutes)

#### Framework 1: by_purpose/README.md

```markdown
# Framework 1: By Optimization Purpose/Objective

**Audience:** Researchers, paper writers, application engineers
**Primary Use:** Research papers, publications, application selection

---

## Categories

### 1. Performance-Focused (performance/)
**Goal:** Minimize RMSE, settling time, overshoot

**Scenarios:**
- S1: Nominal PSO (single IC, RMSE objective)
- S10: Phase-based PSO (progressive refinement)

**Status:** ✅ 100% complete (4/4 controllers)
**Files:** 23 gain files across phases
**Priority:** HIGH (baseline requirement)

**Controllers:**
- Classical SMC: Phase 53 gains
- STA SMC: Phase 53 + Lyapunov-optimized
- Adaptive SMC: Phase 53 gains
- Hybrid Adaptive STA: Phase 53 gains
- Regional Hybrid SMC: PSO optimization pending (NEW - Dec 31, 2025)

**Use Cases:**
- Research benchmarks
- Initial controller tuning
- Performance comparison studies

---

### 2. Safety-Focused (safety/)
**Goal:** Minimize control chattering, ensure smooth operation

**Scenarios:**
- S9: Boundary layer optimization (MT-6)
- S4: Multi-objective PSO (chattering vs performance) - MISSING

**Status:** ⚠️ 50% complete
**Files:** 21 files (MT-6 boundary layer)
**Priority:** MEDIUM (safety-critical systems)

**Key Finding (MT-6):**
- Adaptive boundary layer: Only 3.7% chattering reduction
- Fixed ε=0.02 near-optimal for DIP system
- Negative result prevents future wasted effort

**Use Cases:**
- Medical robotics (patient safety)
- Precision manufacturing (surface quality)
- Actuator wear reduction

---

### 3. Robustness-Focused (robustness/)
**Goal:** Maintain performance under uncertainty/disturbances

**Scenarios:**
- S2: Robust PSO (MT-8 disturbance-aware)
- S3: Multi-seed PSO (MT-7 statistical validation)
- S7: Uncertainty-aware PSO (LT-6) - MISSING
- S8: Disturbance-aware PSO (MT-8)

**Status:** ⚠️ 75% complete (3/4 scenarios)
**Files:** 40 files in comparative/ (MT-7, MT-8, LT-6)
**Priority:** HIGH (real-world deployment)

**Key Findings:**
- MT-8: Hybrid controller +21.4% improvement (best)
- MT-7: 50.4x chattering degradation with narrow ICs (overfitting)
- LT-6: Controllers ranked by uncertainty robustness

**Use Cases:**
- Industrial deployment (variable conditions)
- Outdoor systems (environmental variations)
- High-reliability applications

---

### 4. Efficiency-Focused (efficiency/)
**Goal:** Minimize control effort, energy consumption

**Scenarios:**
- S4: Multi-objective PSO (energy vs performance) - MISSING
- S6: Long-duration stability PSO - MISSING

**Status:** ❌ 0% complete
**Priority:** LOW (future work)

**Use Cases:**
- Battery-powered systems
- Energy-constrained applications
- Sustainability optimization

---

### 5. Multi-Objective (multi_objective/)
**Goal:** Pareto-optimal solutions across multiple objectives

**Scenarios:**
- S4: Multi-objective PSO - MISSING

**Status:** ❌ 0% complete
**Priority:** HIGH (research contribution)

**Potential Algorithms:**
- NSGA-II
- MOPSO
- Pareto front analysis

**Use Cases:**
- Application-specific tuning
- Design space exploration
- Publication-quality research

---

## Quick Navigation

**Find data by goal:**
```bash
# Performance optimization
cd performance/

# Safety (chattering reduction)
cd safety/

# Robustness (disturbances/uncertainty)
cd robustness/

# Energy efficiency
cd efficiency/  # EMPTY - not implemented

# Multi-objective trade-offs
cd multi_objective/  # EMPTY - not implemented
```

---

## Related Frameworks

- **Maturity Level:** See [../by_maturity/](../by_maturity/) for TRL classification
- **Research Tasks:** See [../by_task/](../by_task/) for task-based organization
- **Controllers:** See [../by_controller/](../by_controller/) for controller-specific data
```

#### Similar READMEs for other frameworks (abbreviated for space)

For `by_maturity/README.md`, `by_task/README.md`, etc., follow same pattern:
1. Framework description
2. Category list with status
3. Quick navigation guide
4. Related frameworks

---

### Step 4: Create Symlinks (NOT RECOMMENDED on Windows)

**Alternative for Windows:** Create shortcut text files instead

Create `.ai_workspace\pso\tools\create_shortcuts.py`:

```python
"""
Create Windows shortcuts to actual data files instead of symlinks.
Symlinks require admin/developer mode on Windows.
"""

import os
from pathlib import Path

# Base paths
PSO_ROOT = Path("D:/Projects/main/.ai_workspace/pso")
EXPERIMENTS_ROOT = Path("D:/Projects/main/academic/paper/experiments")

# Framework 1: Purpose - Performance
performance_shortcuts = {
    "classical_smc_phase53": EXPERIMENTS_ROOT / "classical_smc/optimization/phases/phase53/optimized_gains_classical_smc_phase53.json",
    "sta_smc_phase53": EXPERIMENTS_ROOT / "sta_smc/optimization/phases/phase53/optimized_gains_sta_smc_phase53.json",
    "adaptive_smc_phase53": EXPERIMENTS_ROOT / "adaptive_smc/optimization/phases/phase53/optimized_gains_adaptive_smc_phase53.json",
    "hybrid_phase53": EXPERIMENTS_ROOT / "hybrid_adaptive_sta/optimization/phases/phase53/optimized_gains_hybrid_phase53.json",
}

def create_shortcut_file(shortcut_name: str, target_path: Path, output_dir: Path):
    """Create a text file with target path (Windows-friendly alternative to symlinks)"""
    output_dir.mkdir(parents=True, exist_ok=True)
    shortcut_file = output_dir / f"{shortcut_name}.txt"

    with open(shortcut_file, 'w') as f:
        f.write(f"# Shortcut to: {target_path}\n")
        f.write(f"# Framework: Performance-Focused PSO\n")
        f.write(f"# Controller: {shortcut_name}\n")
        f.write(f"\n")
        f.write(f"Target Path:\n")
        f.write(f"{target_path}\n")

    print(f"Created shortcut: {shortcut_file}")

# Create shortcuts for Framework 1 - Performance
performance_dir = PSO_ROOT / "by_purpose/performance/gains"
for name, path in performance_shortcuts.items():
    create_shortcut_file(name, path, performance_dir)

print("\nShortcuts created successfully!")
print("Note: These are text files with paths, not actual symlinks.")
print("Open the .txt file to see the actual file location.")
```

**Usage:**
```bash
python .ai_workspace\pso\tools\create_shortcuts.py
```

---

### Step 5: Validate Structure (15 minutes)

Create `.ai_workspace\pso\tools\validate_structure.py`:

```python
"""
Validate PSO framework directory structure.
"""

from pathlib import Path

PSO_ROOT = Path("D:/Projects/main/.ai_workspace/pso")

# Expected directories
EXPECTED_DIRS = [
    "by_purpose/performance",
    "by_purpose/safety",
    "by_purpose/robustness",
    "by_purpose/efficiency",
    "by_purpose/multi_objective",
    "by_maturity/level_1_theoretical",
    "by_maturity/level_2_simulation",
    "by_maturity/level_3_statistical",
    "by_maturity/level_4_robustness",
    "by_maturity/level_5_hardware",
    "by_maturity/level_6_production",
    "by_maturity/level_7_archived",
    "by_task/QW-3_visualization",
    "by_task/MT-6_boundary_layer",
    "by_task/MT-7_robustness",
    "by_task/MT-8_disturbance",
    "by_task/LT-6_uncertainty",
    "by_task/phase_based",
    "by_filetype/config",
    "by_filetype/gains",
    "by_filetype/data",
    "by_filetype/reports",
    "by_filetype/visualizations",
    "by_filetype/logs",
    "by_filetype/source",
    "by_controller/classical/classical_smc",
    "by_controller/classical/sta_smc",
    "by_controller/adaptive/adaptive_smc",
    "by_controller/adaptive/hybrid_adaptive_sta",
    "by_controller/adaptive/regional_hybrid_smc",
    "by_controller/specialized/swing_up_smc",
    "by_controller/specialized/mpc",
    "by_strategy/single_objective",
    "by_strategy/robust_multiscenario",
    "by_strategy/statistical_validation",
    "by_strategy/multi_objective",
    "by_strategy/adaptive_online",
    "tools",
    "reports",
]

def validate():
    """Validate directory structure."""
    print("Validating PSO framework structure...\n")

    missing = []
    existing = []

    for dir_path in EXPECTED_DIRS:
        full_path = PSO_ROOT / dir_path
        if full_path.exists():
            existing.append(dir_path)
            print(f"[OK] {dir_path}")
        else:
            missing.append(dir_path)
            print(f"[MISSING] {dir_path}")

    print(f"\n{'='*60}")
    print(f"Validation Summary:")
    print(f"{'='*60}")
    print(f"Total Expected: {len(EXPECTED_DIRS)}")
    print(f"Existing: {len(existing)} ({len(existing)/len(EXPECTED_DIRS)*100:.1f}%)")
    print(f"Missing: {len(missing)} ({len(missing)/len(EXPECTED_DIRS)*100:.1f}%)")

    if missing:
        print(f"\nMissing directories:")
        for d in missing:
            print(f"  - {d}")
    else:
        print(f"\n[SUCCESS] All directories exist!")

    return len(missing) == 0

if __name__ == "__main__":
    success = validate()
    exit(0 if success else 1)
```

**Usage:**
```bash
python .ai_workspace\pso\tools\validate_structure.py
```

---

## Summary

**What You've Created:**
- ✅ 6 framework directories with ~40 subdirectories
- ✅ Master README with quick navigation
- ✅ Framework-specific READMEs
- ✅ Validation tools
- ✅ Windows-friendly shortcuts (instead of symlinks)

**Time Spent:** ~3-5 hours

**Next Steps:**
- Phase 2: Create master index and cross-references (2-3 hours)
- Phase 3: Maturity-based config organization (5-8 hours)
- Phase 4: Automation and tooling (5-7 hours)

**Status:** Phase 1 COMPLETE ✅

---

## Troubleshooting

### Issue: Symlinks don't work on Windows
**Solution:** Use the shortcut script (`create_shortcuts.py`) to create text files with paths instead

### Issue: Too many directories, confusing navigation
**Solution:** Use master README navigation links, or create CLI navigator tool (Phase 4)

### Issue: Duplicate data concerns
**Solution:** Shortcuts/symlinks point to original files, no duplication

### Issue: Can't find specific file
**Solution:** Use Windows search in `.ai_workspace\pso\` or create file inventory (Phase 2)

---

## Quick Reference Commands

```bash
# Validate structure
python .ai_workspace\pso\tools\validate_structure.py

# Create shortcuts (Windows-friendly alternative to symlinks)
python .ai_workspace\pso\tools\create_shortcuts.py

# Navigate to framework
cd .ai_workspace\pso\by_purpose\robustness

# View master README
cat .ai_workspace\pso\README.md

# Check directory sizes
du -sh .ai_workspace\pso\*
```

---

**END OF QUICK START GUIDE**
