# Example from: docs\api\optimization_module_api_reference.md
# Index: 27
# Runnable: True
# Hash: c9c8905a

from src.optimization.tuning.pso_hyperparameter_optimizer import (
    PSOHyperparameterOptimizer,
    OptimizationObjective
)
from src.controllers.factory import SMCType
from src.config import load_config

config = load_config("config.yaml")
meta_optimizer = PSOHyperparameterOptimizer(config)

# Optimize PSO hyperparameters for Classical SMC
result = meta_optimizer.optimize_hyperparameters(
    controller_type=SMCType.CLASSICAL,
    objective=OptimizationObjective.MULTI_OBJECTIVE,
    max_evaluations=100,
    n_trials_per_evaluation=5
)

print(f"Optimized PSO Hyperparameters:")
print(f"  Inertia weight (w): {result.hyperparameters.w:.4f}")
print(f"  Cognitive (c1): {result.hyperparameters.c1:.4f}")
print(f"  Social (c2): {result.hyperparameters.c2:.4f}")
print(f"  Swarm size: {result.hyperparameters.n_particles}")
print(f"\nPerformance vs. Baseline:")
print(f"  Convergence speedup: {result.convergence_improvement:.2f}x")
print(f"  Quality improvement: {result.quality_improvement:.2%}")
print(f"  Robustness improvement: {result.robustness_improvement:.2%}")

# Update configuration with optimized hyperparameters
config.pso.w = result.hyperparameters.w
config.pso.c1 = result.hyperparameters.c1
config.pso.c2 = result.hyperparameters.c2
config.pso.n_particles = result.hyperparameters.n_particles