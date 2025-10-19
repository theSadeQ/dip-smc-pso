# LT-7 Research Paper - Data Inventory

**Purpose**: Validate all data sources exist for figures and tables

**Status**: ✅ All critical data files found

---

## Data Sources by Research Task

### MT-5: Baseline Controller Comparison

**Data Files**:
- `benchmarks/comprehensive_benchmark.csv` ✅
- `benchmarks/comprehensive_benchmark.json` ✅

**Figures to Generate**:
- **Figure 3**: Baseline controller comparison (radar plot)
  - Metrics: Energy efficiency, overshoot, chattering, settling time
  - Controllers: Classical SMC, STA-SMC, Adaptive SMC, Hybrid SMC

**Tables to Generate**:
- **Table 1**: Controller Baseline Comparison
  - Columns: Controller, Energy [N²·s], Overshoot [%], Chattering, Settling [s]
  - Format: Mean ± Std for each metric

---

### MT-6: Adaptive Boundary Layer PSO Optimization

**Data Files**:
- `benchmarks/MT6_adaptive_optimization.csv` ✅ (PSO convergence)
- `benchmarks/MT6_adaptive_validation.csv` ✅ (validation results)
- `benchmarks/MT6_fixed_baseline.csv` ✅ (baseline for comparison)
- `benchmarks/MT6_fixed_baseline_summary.json` ✅
- `benchmarks/MT6_adaptive_summary.json` ✅
- `benchmarks/MT6_statistical_comparison.json` ✅

**Figures to Generate**:
- **Figure 2**: Adaptive boundary layer concept
  - Plot: ε_eff = ε_min + α|ṡ| vs sliding surface derivative
  - Source: Generate from formula (not data-driven)

- **Figure 4**: PSO convergence curve
  - X-axis: Iteration
  - Y-axis: Best fitness value
  - Source: `MT6_adaptive_optimization.csv`

- **Figure 5**: Chattering reduction results (box plot, 2-column span)
  - Comparison: Fixed boundary layer vs Adaptive boundary layer
  - Source: `MT6_fixed_baseline.csv` + `MT6_adaptive_validation.csv`

**Tables to Generate**:
- **Table 2**: Adaptive Boundary Layer Results
  - Columns: Metric, Fixed (ε=0.02), Adaptive (ε_min=0.0025, α=1.21), Improvement, p-value
  - Rows: Chattering, Overshoot, Energy, Settling Time
  - Source: `MT6_statistical_comparison.json`

---

### MT-7: Robustness Validation (Generalization Failure)

**Data Files**:
- `benchmarks/MT7_seed_42_results.csv` ✅
- `benchmarks/MT7_seed_43_results.csv` ✅
- `benchmarks/MT7_seed_44_results.csv` ✅
- `benchmarks/MT7_seed_45_results.csv` ✅
- `benchmarks/MT7_seed_46_results.csv` ✅
- `benchmarks/MT7_seed_47_results.csv` ✅
- `benchmarks/MT7_seed_48_results.csv` ✅
- `benchmarks/MT7_seed_49_results.csv` ✅
- `benchmarks/MT7_seed_50_results.csv` ✅
- `benchmarks/MT7_seed_51_results.csv` ✅
- `benchmarks/MT7_robustness_summary.json` ✅
- `benchmarks/MT7_statistical_comparison.json` ✅

**Figures to Generate**:
- **Figure 6**: Robustness degradation analysis (2-column span)
  - Subplot A: Chattering distribution comparison (MT-6 vs MT-7)
  - Subplot B: Success rate breakdown
  - Source: `MT7_robustness_summary.json` + `MT7_seed_*_results.csv`

**Tables to Generate**:
- **Table 5**: Generalization Analysis
  - Columns: Metric, MT-6 (±0.05 rad), MT-7 (±0.3 rad), Degradation
  - Rows: Chattering, Success Rate, P95 Worst-Case
  - Source: `MT7_statistical_comparison.json`

---

### MT-8: Disturbance Rejection Analysis

**Data Files**:
- `benchmarks/MT8_disturbance_rejection.csv` ✅
- `benchmarks/MT8_disturbance_rejection.json` ✅

**Figures to Generate**:
- **Figure 7**: Disturbance rejection failure
  - Time series plot: θ₁, θ₂ under step disturbance
  - Source: `MT8_disturbance_rejection.csv`

**Tables to Generate**:
- **Table 4**: Disturbance Rejection Performance
  - Columns: Scenario, Classical SMC, STA-SMC, Adaptive SMC
  - Rows: Step (10N), Impulse (30N), Sinusoidal (8N)
  - Format: Max overshoot [°] / Convergence rate [%]
  - Source: `MT8_disturbance_rejection.json`

---

### LT-4: Lyapunov Stability Analysis

**Data Files**:
- `.artifacts/lt4_validation_report.md` ✅
- `.artifacts/lt4_validation_report_FINAL.md` ✅

**Content to Extract**:
- Lyapunov functions for each controller
- Stability theorems and proofs
- ISS framework for hybrid controller

**Target Section**:
- **Section IV-B**: Lyapunov Stability Analysis
  - Theorem 1: Classical SMC finite-time stability
  - Remark 1: Boundary layer compatibility with stability
  - (Full proofs may go in online appendix if space limited)

---

### LT-6: Model Uncertainty Analysis

**Status**: ❌ No data files found / ⚠️ SKIPPED BY DESIGN

**Rationale**:
- Plan recommended skipping LT-6 (uninformative results)
- Default gains failed even under nominal conditions
- MT-7 provides superior robustness analysis
- Decision: Do not include in paper

---

## Additional Figures Needed

### Figure 1: DIP System Schematic

**Type**: Diagram (not data-driven)
**Tool**: TikZ, Inkscape, or PowerPoint
**Content**:
- Double inverted pendulum on cart
- Coordinate frame (x, θ₁, θ₂)
- System parameters (masses, lengths)
- Control input (force F)

**Source**:
- Extract physical parameters from `config.yaml`
- Reference similar diagrams in literature
- Create original schematic

**Estimated Time**: 1-2 hours

---

## Data Extraction Scripts Needed

### Script 1: `extract_mt5_baseline.py`
**Purpose**: Generate Figure 3 and Table 1
**Input**: `benchmarks/comprehensive_benchmark.csv`
**Output**:
- `figures/fig3_baseline_radar.pdf`
- `tables/table1_baseline.tex`

### Script 2: `extract_mt6_optimization.py`
**Purpose**: Generate Figures 2, 4, 5 and Table 2
**Input**: `benchmarks/MT6_*.csv`, `benchmarks/MT6_*.json`
**Output**:
- `figures/fig2_adaptive_boundary.pdf` (formula-based)
- `figures/fig4_pso_convergence.pdf`
- `figures/fig5_chattering_boxplot.pdf`
- `tables/table2_adaptive_results.tex`

### Script 3: `extract_mt7_robustness.py`
**Purpose**: Generate Figure 6 and Table 5
**Input**: `benchmarks/MT7_*.csv`, `benchmarks/MT7_*.json`
**Output**:
- `figures/fig6_robustness_degradation.pdf`
- `tables/table5_generalization.tex`

### Script 4: `extract_mt8_disturbance.py`
**Purpose**: Generate Figure 7 and Table 4
**Input**: `benchmarks/MT8_disturbance_rejection.csv`
**Output**:
- `figures/fig7_disturbance_rejection.pdf`
- `tables/table4_disturbance.tex`

---

## Physical System Parameters

**Source**: `config.yaml` (lines 248-260, per LT-4 context)

**Parameters Needed for Figure 1 Caption**:
- Cart mass (M)
- Pendulum 1 mass (m₁), length (l₁), inertia (I₁)
- Pendulum 2 mass (m₂), length (l₂), inertia (I₂)
- Gravity (g)

**Action**: Extract these values for Section VI-A (Experimental Setup)

---

## Validation Checklist

**Data Files**:
- [✅] MT-5 baseline data available
- [✅] MT-6 optimization data available
- [✅] MT-7 robustness data available
- [✅] MT-8 disturbance data available
- [✅] LT-4 stability proofs available
- [⚠️] LT-6 data skipped (by design)

**Figures** (7 total):
- [Pending] Figure 1: DIP schematic (manual creation)
- [Pending] Figure 2: Adaptive boundary concept (formula-based)
- [✅] Figure 3: Baseline radar plot (data ready)
- [✅] Figure 4: PSO convergence (data ready)
- [✅] Figure 5: Chattering box plot (data ready)
- [✅] Figure 6: Robustness degradation (data ready)
- [✅] Figure 7: Disturbance time series (data ready)

**Tables** (5 total):
- [✅] Table 1: Baseline comparison (data ready)
- [✅] Table 2: Adaptive results (data ready)
- [✅] Table 4: Disturbance rejection (data ready)
- [✅] Table 5: Generalization analysis (data ready)
- [Pending] Table 0: Related work comparison (literature review needed)

**Sections**:
- [Pending] Section I: Introduction (write after results)
- [Pending] Section II: Related Work (literature review first)
- [Pending] Section III: System Modeling (extract from code)
- [Pending] Section IV: SMC Design (adapt LT-4)
- [Pending] Section V: PSO Optimization (straightforward)
- [Pending] Section VI: Experimental Setup (config.yaml params)
- [Pending] Section VII: Results (data extraction priority)
- [Pending] Section VIII: Discussion (write after results)
- [Pending] Section IX: Conclusions (write last)

---

## Next Steps

1. **Create data extraction scripts** (4 scripts above)
2. **Extract physical parameters** from `config.yaml`
3. **Read LT-4 final report** to extract Lyapunov proofs
4. **Generate all 7 figures** (target: 300 DPI, IEEE format)
5. **Generate all 5 tables** (LaTeX format)
6. **Begin writing Section VII** (Results) - easiest with data in hand

**Estimated Time for Data Prep**: 4-6 hours
**Status**: Ready to proceed with figure/table generation

---

## Notes

- All critical data files confirmed to exist
- No gaps in data (except intentional LT-6 skip)
- Figure 1 (DIP schematic) requires manual creation
- Ready to proceed to Phase 2: Figure Generation
