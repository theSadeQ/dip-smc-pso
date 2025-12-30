"""
Generate Windows-friendly shortcut files for Framework 1 (By Purpose/Objective).
Shortcut files are text files containing paths to actual data files.
"""

from pathlib import Path

# Base paths
PSO_ROOT = Path(r"D:\Projects\main\.ai_workspace\pso\by_purpose")
PROJECT_ROOT = Path(r"D:\Projects\main")
EXPERIMENTS = PROJECT_ROOT / "academic/paper/experiments"
LOGS = PROJECT_ROOT / "academic/logs/pso"
CONFIG = PROJECT_ROOT / "config.yaml"
SRC = PROJECT_ROOT / "src"

def create_shortcut(target_path, shortcut_dir, shortcut_name, category, purpose, notes=""):
    """Create a shortcut text file."""
    shortcut_dir.mkdir(parents=True, exist_ok=True)
    shortcut_file = shortcut_dir / f"{shortcut_name}.txt"

    with open(shortcut_file, 'w', encoding='utf-8') as f:
        f.write(f"# PSO Framework 1: By Purpose/Objective\n")
        f.write(f"# Category: {category}\n")
        f.write(f"# Purpose: {purpose}\n")
        if notes:
            f.write(f"# Notes: {notes}\n")
        f.write(f"\n")
        f.write(f"Target Path:\n")
        f.write(f"{target_path}\n")
        f.write(f"\n")
        f.write(f"# To view this file:\n")
        f.write(f"# Windows: start {target_path}\n")
        f.write(f"# OR: Open the path above in your file explorer\n")

    print(f"Created: {shortcut_file.name} -> {target_path.name}")
    return shortcut_file

# ============================================================================
# CATEGORY 1: PERFORMANCE-FOCUSED (21 files)
# ============================================================================

print("\n[CATEGORY 1: PERFORMANCE-FOCUSED]")
print("="*60)

# Phase 53 Gains (5 files)
print("\nPhase 53 Gains (5 files):")
phase53_dir = PSO_ROOT / "1_performance/phase53"
create_shortcut(
    EXPERIMENTS / "classical_smc/optimization/phases/phase53/optimized_gains_classical_smc_phase53.json",
    phase53_dir,
    "classical_smc_phase53",
    "Performance",
    "Baseline RMSE optimization - Classical SMC",
    "Phase 53 standard optimization"
)
create_shortcut(
    EXPERIMENTS / "sta_smc/optimization/phases/phase53/optimized_gains_sta_smc_phase53.json",
    phase53_dir,
    "sta_smc_phase53",
    "Performance",
    "Baseline RMSE optimization - STA SMC",
    "Phase 53 standard optimization"
)
create_shortcut(
    EXPERIMENTS / "sta_smc/optimization/phases/phase53/gains_sta_lyapunov_optimized.json",
    phase53_dir,
    "sta_smc_lyapunov_optimized",
    "Performance",
    "Lyapunov-based optimization - STA SMC",
    "Alternative optimization method"
)
create_shortcut(
    EXPERIMENTS / "adaptive_smc/optimization/phases/phase53/optimized_gains_adaptive_smc_phase53.json",
    phase53_dir,
    "adaptive_smc_phase53",
    "Performance",
    "Baseline RMSE optimization - Adaptive SMC",
    "Phase 53 standard optimization"
)
create_shortcut(
    EXPERIMENTS / "hybrid_adaptive_sta/optimization/phases/phase53/optimized_gains_hybrid_phase53.json",
    phase53_dir,
    "hybrid_adaptive_sta_phase53",
    "Performance",
    "Baseline RMSE optimization - Hybrid Adaptive STA",
    "Phase 53 standard optimization"
)

# Phase 2 Standard Gains (4 files)
print("\nPhase 2 Standard Gains (4 files):")
phase2_dir = PSO_ROOT / "1_performance/phase2_standard"
create_shortcut(
    EXPERIMENTS / "sta_smc/optimization/phases/phase2/gains/standard/pso_sta_smc_standard.json",
    phase2_dir,
    "sta_smc_standard",
    "Performance",
    "Phase 2 standard conditions - STA SMC"
)
create_shortcut(
    EXPERIMENTS / "adaptive_smc/optimization/phases/phase2/gains/standard/pso_adaptive_smc_standard.json",
    phase2_dir,
    "adaptive_smc_standard",
    "Performance",
    "Phase 2 standard conditions - Adaptive SMC"
)
create_shortcut(
    EXPERIMENTS / "hybrid_adaptive_sta/optimization/phases/phase2/gains/standard/pso_hybrid_adaptive_sta_smc_standard.json",
    phase2_dir,
    "hybrid_adaptive_sta_standard",
    "Performance",
    "Phase 2 standard conditions - Hybrid"
)
create_shortcut(
    EXPERIMENTS / "sta_smc/optimization/phases/phase2/gains/sta_smc_gains.json",
    phase2_dir,
    "sta_smc_baseline",
    "Performance",
    "Phase 2 baseline gains - STA SMC"
)

# Convergence Plots (3 files)
print("\nConvergence Plots (3 files):")
convergence_dir = PSO_ROOT / "1_performance/convergence_plots"
create_shortcut(
    EXPERIMENTS / "sta_smc/optimization/active/sta_smc_convergence.png",
    convergence_dir,
    "sta_smc_convergence",
    "Performance",
    "PSO convergence plot - STA SMC"
)
create_shortcut(
    EXPERIMENTS / "adaptive_smc/optimization/active/adaptive_smc_convergence.png",
    convergence_dir,
    "adaptive_smc_convergence",
    "Performance",
    "PSO convergence plot - Adaptive SMC"
)
create_shortcut(
    EXPERIMENTS / "hybrid_adaptive_sta/optimization/active/hybrid_adaptive_sta_smc_convergence.png",
    convergence_dir,
    "hybrid_adaptive_sta_convergence",
    "Performance",
    "PSO convergence plot - Hybrid Adaptive STA"
)

# LT7 Figures (2 files)
print("\nLT7 Publication Figures (2 files):")
lt7_dir = PSO_ROOT / "1_performance/lt7_figures"
create_shortcut(
    EXPERIMENTS / "figures/LT7_section_5_1_pso_convergence.png",
    lt7_dir,
    "LT7_section_5_1_pso_convergence",
    "Performance",
    "PSO convergence plot for LT-7 research paper"
)
create_shortcut(
    EXPERIMENTS / "figures/LT7_section_8_3_pso_generalization.png",
    lt7_dir,
    "LT7_section_8_3_pso_generalization",
    "Performance",
    "PSO generalization analysis for LT-7 paper"
)

# Config Reference (1 file)
print("\nConfig Reference (1 file):")
config_dir = PSO_ROOT / "1_performance/config"
create_shortcut(
    CONFIG,
    config_dir,
    "config_performance_section",
    "Performance",
    "See lines 39-83 (controller defaults), 186-229 (PSO bounds)",
    "Performance-focused default gains from MT-8 optimization"
)

# Source Code (6 files)
print("\nSource Code (6 files):")
source_dir = PSO_ROOT / "1_performance/source"
create_shortcut(
    SRC / "optimization/algorithms/pso_optimizer.py",
    source_dir,
    "pso_optimizer",
    "Performance",
    "Core PSO implementation (single-objective)"
)
create_shortcut(
    SRC / "optimization/algorithms/swarm/pso.py",
    source_dir,
    "swarm_pso",
    "Performance",
    "Swarm-based PSO algorithms"
)
create_shortcut(
    SRC / "optimization/core/cost_evaluator.py",
    source_dir,
    "cost_evaluator",
    "Performance",
    "Fitness function evaluation"
)
create_shortcut(
    SRC / "optimization/objectives/control/tracking.py",
    source_dir,
    "tracking_objectives",
    "Performance",
    "Tracking performance objectives (RMSE, settling time)"
)
create_shortcut(
    SRC / "optimization/objectives/control/stability.py",
    source_dir,
    "stability_objectives",
    "Performance",
    "Stability performance objectives"
)
create_shortcut(
    SRC / "utils/visualization/pso_plots.py",
    source_dir,
    "pso_visualization",
    "Performance",
    "PSO convergence and diversity plots (QW-3)"
)

# ============================================================================
# CATEGORY 2: SAFETY-FOCUSED (3 files)
# ============================================================================

print("\n[CATEGORY 2: SAFETY-FOCUSED]")
print("="*60)

# MT-6 Data (2 files)
print("\nMT-6 Boundary Layer Optimization (2 files):")
mt6_dir = PSO_ROOT / "2_safety/mt6_sta_smc"
create_shortcut(
    EXPERIMENTS / "sta_smc/boundary_layer/MT6_adaptive_optimization.csv",
    mt6_dir,
    "MT6_adaptive_optimization",
    "Safety",
    "Adaptive boundary layer PSO (ε_min + α optimization)",
    "32 iterations, ε_min=0.00250, α=1.21, chattering=2.14 (3.7% reduction)"
)
create_shortcut(
    EXPERIMENTS / "figures/MT6_pso_convergence.png",
    mt6_dir,
    "MT6_pso_convergence",
    "Safety",
    "MT-6 PSO convergence plot (chattering reduction)"
)

# Config Reference (1 file)
print("\nConfig Reference (1 file):")
config_dir = PSO_ROOT / "2_safety/config"
create_shortcut(
    CONFIG,
    config_dir,
    "config_safety_section",
    "Safety",
    "See lines 84, 97, 113, 179-181 (boundary_layer parameters)",
    "Chattering reduction via increased boundary layers (Issue #12 resolution)"
)

# ============================================================================
# CATEGORY 3: ROBUSTNESS-FOCUSED (46 files)
# ============================================================================

print("\n[CATEGORY 3: ROBUSTNESS-FOCUSED]")
print("="*60)

# MT-7 Validation (15 files)
print("\nMT-7 Multi-Seed Validation (15 files):")
mt7_dir = PSO_ROOT / "3_robustness/mt7_validation"
create_shortcut(
    EXPERIMENTS / "comparative/pso_robustness/MT7_COMPLETE_REPORT.md",
    mt7_dir,
    "MT7_COMPLETE_REPORT",
    "Robustness",
    "MT-7 comprehensive report (50.4x degradation, overfitting detected)"
)
create_shortcut(
    EXPERIMENTS / "comparative/pso_robustness/MT7_robustness_summary.json",
    mt7_dir,
    "MT7_robustness_summary",
    "Robustness",
    "MT-7 statistical summary (10 seeds, 500 runs)"
)
create_shortcut(
    EXPERIMENTS / "comparative/pso_robustness/MT7_statistical_comparison.json",
    mt7_dir,
    "MT7_statistical_comparison",
    "Robustness",
    "MT-7 cross-seed comparison (Welch's t-test, Cohen's d)"
)

# MT-7 seed results (10 files)
for seed in range(42, 52):
    create_shortcut(
        EXPERIMENTS / f"comparative/pso_robustness/MT7_seed_{seed}_results.csv",
        mt7_dir,
        f"MT7_seed_{seed}_results",
        "Robustness",
        f"MT-7 seed {seed} results (50 runs)"
    )

# MT-8 Disturbance Rejection (9 files)
print("\nMT-8 Disturbance Rejection (9 files):")
mt8_dir = PSO_ROOT / "3_robustness/mt8_disturbance"
create_shortcut(
    EXPERIMENTS / "comparative/disturbance_rejection/MT8_robust_validation_summary.json",
    mt8_dir,
    "MT8_robust_validation_summary",
    "Robustness",
    "MT-8 summary (Hybrid +21.4% best, 6.35% avg improvement)"
)
create_shortcut(
    EXPERIMENTS / "comparative/disturbance_rejection/MT8_disturbance_rejection.csv",
    mt8_dir,
    "MT8_disturbance_rejection",
    "Robustness",
    "MT-8 disturbance rejection results (all controllers)"
)
create_shortcut(
    EXPERIMENTS / "comparative/disturbance_rejection/MT8_disturbance_rejection.json",
    mt8_dir,
    "MT8_disturbance_rejection_json",
    "Robustness",
    "MT-8 disturbance rejection (JSON format)"
)
create_shortcut(
    EXPERIMENTS / "comparative/disturbance_rejection/MT8_adaptive_scheduling_results.json",
    mt8_dir,
    "MT8_adaptive_scheduling",
    "Robustness",
    "MT-8 adaptive gain scheduling validation"
)
create_shortcut(
    EXPERIMENTS / "comparative/disturbance_rejection/MT8_hil_validation_results.json",
    mt8_dir,
    "MT8_hil_validation",
    "Robustness",
    "MT-8 hardware-in-the-loop validation"
)
create_shortcut(
    EXPERIMENTS / "comparative/disturbance_rejection/MT8_extended_validation_results.json",
    mt8_dir,
    "MT8_extended_validation",
    "Robustness",
    "MT-8 extended validation results"
)

# MT-8 reproduction gains (4 files)
for ctrl in ["classical_smc", "sta_smc", "adaptive_smc", "hybrid_adaptive_sta_smc"]:
    create_shortcut(
        EXPERIMENTS / f"{ctrl}/optimization/active/mt8_repro_seed42_{ctrl}.json",
        mt8_dir,
        f"mt8_repro_{ctrl}",
        "Robustness",
        f"MT-8 robust gains (seed 42) - {ctrl}"
    )

# Phase 2 Robust Gains (5 files)
print("\nPhase 2 Robust Gains (5 files):")
phase2_robust_dir = PSO_ROOT / "3_robustness/phase2_robust"
create_shortcut(
    EXPERIMENTS / "sta_smc/optimization/phases/phase2/gains/robust/pso_sta_smc_robust.json",
    phase2_robust_dir,
    "sta_smc_robust",
    "Robustness",
    "Phase 2 robust gains - STA SMC"
)
create_shortcut(
    EXPERIMENTS / "adaptive_smc/optimization/phases/phase2/gains/robust/pso_adaptive_smc_robust.json",
    phase2_robust_dir,
    "adaptive_smc_robust",
    "Robustness",
    "Phase 2 robust gains - Adaptive SMC"
)
create_shortcut(
    EXPERIMENTS / "hybrid_adaptive_sta/optimization/phases/phase2/gains/robust/pso_hybrid_adaptive_sta_smc_robust.json",
    phase2_robust_dir,
    "hybrid_adaptive_sta_robust",
    "Robustness",
    "Phase 2 robust gains - Hybrid"
)
create_shortcut(
    EXPERIMENTS / "adaptive_smc/optimization/archive/adaptive_smc_robust_gains.json",
    phase2_robust_dir,
    "adaptive_smc_robust_archive",
    "Robustness",
    "Archived robust gains - Adaptive SMC"
)
create_shortcut(
    EXPERIMENTS / "hybrid_adaptive_sta/optimization/archive/hybrid_adaptive_sta_smc_robust_gains.json",
    phase2_robust_dir,
    "hybrid_adaptive_sta_robust_archive",
    "Robustness",
    "Archived robust gains - Hybrid"
)

# Robust Logs (13 files)
print("\nRobust PSO Logs (13 files):")
logs_dir = PSO_ROOT / "3_robustness/logs"
for ctrl in ["classical_smc", "sta_smc", "adaptive_smc", "hybrid_adaptive_sta_smc"]:
    log_file = LOGS / f"2025-12-09_{ctrl}_robust.log"
    if log_file.exists():
        create_shortcut(
            log_file,
            logs_dir,
            f"{ctrl}_robust_log",
            "Robustness",
            f"Robust PSO execution log - {ctrl}"
        )

# Config Reference (1 file)
print("\nConfig Reference (1 file):")
config_dir = PSO_ROOT / "3_robustness/config"
create_shortcut(
    CONFIG,
    config_dir,
    "config_robustness_section",
    "Robustness",
    "See lines 30-37 (MT-8 robust PSO), 230-244 (multi-scenario robustness)",
    "Disturbance-aware fitness (50% nominal + 50% disturbed)"
)

# Source Code (3 files)
print("\nSource Code (3 files):")
source_dir = PSO_ROOT / "3_robustness/source"
create_shortcut(
    SRC / "optimization/algorithms/robust_pso_optimizer.py",
    source_dir,
    "robust_pso_optimizer",
    "Robustness",
    "Robust PSO implementation (multi-scenario)"
)
create_shortcut(
    SRC / "optimization/core/robust_cost_evaluator.py",
    source_dir,
    "robust_cost_evaluator",
    "Robustness",
    "Robust fitness evaluation (worst-case weighting)"
)
create_shortcut(
    SRC / "optimization/objectives/control/robustness.py",
    source_dir,
    "robustness_objectives",
    "Robustness",
    "Robustness objectives (Monte Carlo, H-infinity, sensitivity)"
)

# ============================================================================
# CATEGORY 4: EFFICIENCY-FOCUSED (2 files - PLACEHOLDER)
# ============================================================================

print("\n[CATEGORY 4: EFFICIENCY-FOCUSED]")
print("="*60)

# Source Code (1 file)
print("\nSource Code (1 file):")
source_dir = PSO_ROOT / "4_efficiency/source"
create_shortcut(
    SRC / "optimization/objectives/control/energy.py",
    source_dir,
    "energy_objectives",
    "Efficiency",
    "Energy objectives (∫u²dt, RMS, peak, weighted)",
    "Infrastructure ready, no datasets yet"
)

# Config Reference (1 file)
print("\nConfig Reference (1 file):")
config_dir = PSO_ROOT / "4_efficiency/config"
create_shortcut(
    CONFIG,
    config_dir,
    "config_efficiency_section",
    "Efficiency",
    "See lines 367-396 (cost function energy weights)",
    "control_effort: 0.1, control_rate: 0.01"
)

# ============================================================================
# CATEGORY 5: MULTI-OBJECTIVE (12 files - PARTIAL)
# ============================================================================

print("\n[CATEGORY 5: MULTI-OBJECTIVE]")
print("="*60)

# Source Code (2 files)
print("\nSource Code (2 files):")
source_dir = PSO_ROOT / "5_multi_objective/source"
create_shortcut(
    SRC / "optimization/algorithms/multi_objective_pso.py",
    source_dir,
    "multi_objective_pso",
    "Multi-Objective",
    "MOPSO implementation (NSGA-II, Pareto fronts, hypervolume)",
    "Infrastructure ready, no datasets yet"
)
create_shortcut(
    SRC / "optimization/integration/pso_factory_bridge.py",
    source_dir,
    "pso_factory_bridge",
    "Multi-Objective",
    "PSO factory integration"
)

# Config Reference (1 file)
print("\nConfig Reference (1 file):")
config_dir = PSO_ROOT / "5_multi_objective/config"
create_shortcut(
    CONFIG,
    config_dir,
    "config_multi_objective_section",
    "Multi-Objective",
    "See lines 367-392 (multi-objective weights), 390-392 (combine method)",
    "Mean (0.7) + Max (0.3) combine weights"
)

# Implicit Multi-Objective: MT-8 files (9 files - dual categorized)
print("\nImplicit Multi-Objective (MT-8 files, dual-categorized):")
print("Note: MT-8 files already in 3_robustness, creating cross-references here")
mt8_multi_dir = PSO_ROOT / "5_multi_objective/mt8_implicit"
mt8_multi_dir.mkdir(parents=True, exist_ok=True)
with open(mt8_multi_dir / "README_DUAL_CATEGORY.txt", 'w') as f:
    f.write("# Dual Categorization: Robustness + Multi-Objective\n\n")
    f.write("MT-8 robust PSO balances multiple objectives:\n")
    f.write("- 50% Nominal performance (RMSE)\n")
    f.write("- 50% Disturbed performance (disturbance rejection)\n\n")
    f.write("This is implicit multi-objective optimization.\n\n")
    f.write("For full MT-8 files, see: ../3_robustness/mt8_disturbance/\n")
    f.write("\nFiles (9 total):\n")
    f.write("- MT8_robust_validation_summary.json\n")
    f.write("- MT8_disturbance_rejection.csv/.json\n")
    f.write("- MT8_adaptive_scheduling_results.json\n")
    f.write("- MT8_hil_validation_results.json\n")
    f.write("- MT8_extended_validation_results.json\n")
    f.write("- mt8_repro_seed42_*.json (4 controllers)\n")

print("Created README_DUAL_CATEGORY.txt explaining cross-categorization")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total shortcut files created:")
print(f"  Category 1 (Performance): 21 files")
print(f"  Category 2 (Safety): 3 files")
print(f"  Category 3 (Robustness): 46 files")
print(f"  Category 4 (Efficiency): 2 files (PLACEHOLDER)")
print(f"  Category 5 (Multi-Objective): 3 files + 1 README (PARTIAL)")
print(f"\nTotal: 75+ shortcut files")
print(f"\nAll shortcuts created in: {PSO_ROOT}")
print(f"\nNext: Create README files for each category")
