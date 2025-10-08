# Example from: docs\api\optimization_module_api_reference.md
# Index: 35
# Runnable: False
# Hash: 973f49f2

#!/usr/bin/env python3
"""
Example 5: Complete Optimization Pipeline

Demonstrates:
- Full workflow: Config → Factory → PSO → Validation → Deployment
- Bounds validation and adjustment
- Convergence monitoring
- Performance benchmarking
- Controller deployment
"""

import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from pathlib import Path

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.optimization.validation.pso_bounds_validator import PSOBoundsValidator
from src.optimization.validation.enhanced_convergence_analyzer import (
    EnhancedConvergenceAnalyzer,
    ConvergenceCriteria
)
from src.controllers.factory import create_controller, SMCType
from src.config import load_config
from src.simulation.engines.simulation_runner import SimulationRunner

# ============================================================================
# Configuration
# ============================================================================

CONFIG_PATH = "config.yaml"
CONTROLLER_TYPE = 'classical_smc'
OUTPUT_DIR = Path("optimization_results")
SEED = 42

# ============================================================================
# Pipeline
# ============================================================================

def main():
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("="*80)
    print("COMPLETE PSO OPTIMIZATION PIPELINE")
    print("="*80)

    # -------------------------------------------------------------------------
    # Step 1: Load Configuration
    # -------------------------------------------------------------------------
    print("\n[1/7] Loading configuration...")
    config = load_config(CONFIG_PATH)
    print(f"  ✓ Configuration loaded from {CONFIG_PATH}")

    # -------------------------------------------------------------------------
    # Step 2: Validate and Adjust Bounds
    # -------------------------------------------------------------------------
    print("\n[2/7] Validating PSO bounds...")
    validator = PSOBoundsValidator(config)

    bounds_result = validator.validate_bounds(
        controller_type=CONTROLLER_TYPE,
        lower_bounds=list(config.pso.bounds.min),
        upper_bounds=list(config.pso.bounds.max)
    )

    if bounds_result.is_valid:
        print("  ✓ Bounds are valid")
    else:
        print("  ✗ Bounds validation failed, using adjusted bounds")
        config.pso.bounds.min = bounds_result.adjusted_bounds['lower']
        config.pso.bounds.max = bounds_result.adjusted_bounds['upper']

    # -------------------------------------------------------------------------
    # Step 3: Initialize Convergence Analyzer
    # -------------------------------------------------------------------------
    print("\n[3/7] Initializing convergence analyzer...")
    criteria = ConvergenceCriteria(
        fitness_tolerance=1e-6,
        max_stagnation_iterations=50
    )
    analyzer = EnhancedConvergenceAnalyzer(
        criteria=criteria,
        controller_type=SMCType.CLASSICAL
    )
    print("  ✓ Convergence analyzer ready")

    # -------------------------------------------------------------------------
    # Step 4: Create Controller Factory
    # -------------------------------------------------------------------------
    print("\n[4/7] Creating controller factory...")
    controller_factory = partial(
        create_controller,
        controller_type=CONTROLLER_TYPE,
        config=config
    )
    print("  ✓ Factory created")

    # -------------------------------------------------------------------------
    # Step 5: Run PSO Optimization
    # -------------------------------------------------------------------------
    print("\n[5/7] Running PSO optimization...")
    tuner = PSOTuner(
        controller_factory=controller_factory,
        config=config,
        seed=SEED,
        instability_penalty_factor=100.0
    )

    result = tuner.optimise()

    best_gains = result['best_pos']
    best_cost = result['best_cost']
    cost_history = result['cost_history']

    print(f"  ✓ Optimization complete")
    print(f"    Best cost: {best_cost:.6f}")
    print(f"    Convergence: {len(cost_history)} iterations")

    # Save results
    np.save(OUTPUT_DIR / "optimized_gains.npy", best_gains)
    np.save(OUTPUT_DIR / "cost_history.npy", cost_history)

    # -------------------------------------------------------------------------
    # Step 6: Validate Optimized Controller
    # -------------------------------------------------------------------------
    print("\n[6/7] Validating optimized controller...")

    # Create controller with optimized gains
    optimized_controller = create_controller(
        controller_type=CONTROLLER_TYPE,
        config=config,
        gains=best_gains
    )

    # Run validation simulations
    n_validation_trials = 10
    validation_costs = []

    for trial in range(n_validation_trials):
        sim_runner = SimulationRunner(
            controller=optimized_controller,
            config=config,
            seed=SEED + trial
        )
        result_trial = sim_runner.run()

        # Compute cost
        ise = np.sum(result_trial.states ** 2) * config.simulation.dt
        validation_costs.append(ise)

    mean_cost = np.mean(validation_costs)
    std_cost = np.std(validation_costs)

    print(f"  ✓ Validation complete ({n_validation_trials} trials)")
    print(f"    Mean cost: {mean_cost:.6f} ± {std_cost:.6f}")

    # -------------------------------------------------------------------------
    # Step 7: Generate Report and Visualizations
    # -------------------------------------------------------------------------
    print("\n[7/7] Generating reports and visualizations...")

    # Convergence plot
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    axes[0].plot(cost_history, linewidth=2, color='blue')
    axes[0].set_ylabel('Best Cost', fontsize=12)
    axes[0].set_title('PSO Convergence History', fontsize=14, fontweight='bold')
    axes[0].set_yscale('log')
    axes[0].grid(True, alpha=0.3)

    axes[1].bar(range(n_validation_trials), validation_costs, alpha=0.7, color='green')
    axes[1].axhline(y=mean_cost, color='red', linestyle='--', label=f'Mean: {mean_cost:.4f}')
    axes[1].set_xlabel('Validation Trial', fontsize=12)
    axes[1].set_ylabel('Cost (ISE)', fontsize=12)
    axes[1].set_title('Validation Performance', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "optimization_pipeline_summary.png", dpi=300)

    # Summary report
    report_path = OUTPUT_DIR / "optimization_report.txt"
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("PSO OPTIMIZATION PIPELINE - SUMMARY REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Controller Type: {CONTROLLER_TYPE}\n")
        f.write(f"Configuration: {CONFIG_PATH}\n")
        f.write(f"Random Seed: {SEED}\n\n")
        f.write("-"*80 + "\n")
        f.write("OPTIMIZATION RESULTS\n")
        f.write("-"*80 + "\n")
        f.write(f"Best Cost: {best_cost:.6f}\n")
        f.write(f"Convergence Iterations: {len(cost_history)}\n")
        f.write(f"Optimized Gains: {best_gains}\n\n")
        f.write("-"*80 + "\n")
        f.write("VALIDATION RESULTS\n")
        f.write("-"*80 + "\n")
        f.write(f"Number of Trials: {n_validation_trials}\n")
        f.write(f"Mean Cost: {mean_cost:.6f}\n")
        f.write(f"Std. Deviation: {std_cost:.6f}\n")
        f.write(f"Min Cost: {np.min(validation_costs):.6f}\n")
        f.write(f"Max Cost: {np.max(validation_costs):.6f}\n")
        f.write("="*80 + "\n")

    print(f"  ✓ Summary report: {report_path}")
    print(f"  ✓ Visualization: {OUTPUT_DIR / 'optimization_pipeline_summary.png'}")

    print("\n" + "="*80)
    print("PIPELINE COMPLETE")
    print("="*80)
    print(f"\nOptimized controller ready for deployment!")
    print(f"Gains: {best_gains}")

if __name__ == "__main__":
    main()