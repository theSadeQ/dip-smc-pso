# Example from: docs\api\optimization_module_api_reference.md
# Index: 34
# Runnable: False
# Hash: 1c020e63

#!/usr/bin/env python3
"""
Example 4: PSO Hyperparameter Optimization

Demonstrates:
- PSOHyperparameterOptimizer usage
- Meta-optimization with differential evolution
- Multi-objective optimization
- Baseline comparison
"""

from src.optimization.tuning.pso_hyperparameter_optimizer import (
    PSOHyperparameterOptimizer,
    OptimizationObjective
)
from src.controllers.factory import SMCType
from src.config import load_config
import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# Configuration
# ============================================================================

CONFIG_PATH = "config.yaml"
CONTROLLER_TYPE = SMCType.CLASSICAL
MAX_META_EVALUATIONS = 50
N_TRIALS_PER_EVAL = 3

# ============================================================================
# Main
# ============================================================================

def main():
    # Load configuration
    config = load_config(CONFIG_PATH)

    # Initialize meta-optimizer
    print("Initializing PSO Hyperparameter Optimizer...")
    meta_optimizer = PSOHyperparameterOptimizer(config)

    # Run meta-optimization
    print(f"\nRunning meta-optimization for {CONTROLLER_TYPE.value}...")
    print(f"Max evaluations: {MAX_META_EVALUATIONS}")
    print(f"Trials per evaluation: {N_TRIALS_PER_EVAL}")
    print(f"Objective: {OptimizationObjective.MULTI_OBJECTIVE.value}")
    print("="*80)

    result = meta_optimizer.optimize_hyperparameters(
        controller_type=CONTROLLER_TYPE,
        objective=OptimizationObjective.MULTI_OBJECTIVE,
        max_evaluations=MAX_META_EVALUATIONS,
        n_trials_per_evaluation=N_TRIALS_PER_EVAL
    )

    # Display results
    print("\n" + "="*80)
    print("HYPERPARAMETER OPTIMIZATION RESULTS")
    print("="*80)
    print(f"\nOptimized Hyperparameters:")
    print(f"  Inertia weight (w):   {result.hyperparameters.w:.6f}")
    print(f"  Cognitive (c1):       {result.hyperparameters.c1:.6f}")
    print(f"  Social (c2):          {result.hyperparameters.c2:.6f}")
    print(f"  Swarm size:           {result.hyperparameters.n_particles}")

    print(f"\nBaseline Hyperparameters:")
    print(f"  Inertia weight (w):   {result.baseline_hyperparameters.w:.6f}")
    print(f"  Cognitive (c1):       {result.baseline_hyperparameters.c1:.6f}")
    print(f"  Social (c2):          {result.baseline_hyperparameters.c2:.6f}")
    print(f"  Swarm size:           {result.baseline_hyperparameters.n_particles}")

    print(f"\nPerformance Improvements vs. Baseline:")
    print(f"  Convergence speedup:  {result.convergence_improvement:.2f}x")
    print(f"  Quality improvement:  {result.quality_improvement*100:.2f}%")
    print(f"  Robustness improvement: {result.robustness_improvement*100:.2f}%")
    print(f"  Efficiency score:     {result.efficiency_score:.4f}")
    print("="*80)

    # Visualize comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    categories = ['w', 'c1', 'c2', 'N']
    baseline_values = [
        result.baseline_hyperparameters.w,
        result.baseline_hyperparameters.c1,
        result.baseline_hyperparameters.c2,
        result.baseline_hyperparameters.n_particles
    ]
    optimized_values = [
        result.hyperparameters.w,
        result.hyperparameters.c1,
        result.hyperparameters.c2,
        result.hyperparameters.n_particles
    ]

    x = np.arange(len(categories))
    width = 0.35

    axes[0, 0].bar(x - width/2, baseline_values, width, label='Baseline', alpha=0.7)
    axes[0, 0].bar(x + width/2, optimized_values, width, label='Optimized', alpha=0.7)
    axes[0, 0].set_ylabel('Value')
    axes[0, 0].set_title('Hyperparameter Comparison')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(categories)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Performance metrics
    metrics = ['Convergence\nSpeed', 'Solution\nQuality', 'Robustness']
    improvements = [
        result.convergence_improvement,
        1 + result.quality_improvement,
        1 + result.robustness_improvement
    ]

    axes[0, 1].bar(metrics, improvements, color=['blue', 'green', 'orange'], alpha=0.7)
    axes[0, 1].axhline(y=1.0, color='red', linestyle='--', label='Baseline')
    axes[0, 1].set_ylabel('Improvement Factor')
    axes[0, 1].set_title('Performance Improvements')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Convergence history (if available)
    if hasattr(result, 'optimization_history'):
        axes[1, 0].plot(result.optimization_history['best_objective'], linewidth=2)
        axes[1, 0].set_xlabel('Meta-Optimization Iteration')
        axes[1, 0].set_ylabel('Objective Value')
        axes[1, 0].set_title('Meta-Optimization Convergence')
        axes[1, 0].grid(True, alpha=0.3)

    # Hide unused subplot
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig('pso_hyperparameter_optimization.png', dpi=300)
    print("\nVisualization saved: pso_hyperparameter_optimization.png")

if __name__ == "__main__":
    main()