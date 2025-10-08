# Example from: docs\api\optimization_module_api_reference.md
# Index: 23
# Runnable: True
# Hash: c820284b

from src.optimization.validation.pso_bounds_optimizer import (
    PSOBoundsOptimizer,
    BoundsOptimizationStrategy
)
from src.controllers.factory import SMCType
from src.config import load_config

config = load_config("config.yaml")
optimizer = PSOBoundsOptimizer(config)

# Optimize bounds for Classical SMC
result = optimizer.optimize_bounds_for_controller(
    controller_type=SMCType.CLASSICAL,
    strategy=BoundsOptimizationStrategy.HYBRID,
    max_optimization_time=600.0,
    n_trials=20
)

print(f"Optimized Bounds:")
print(f"  Lower: {result.adjusted_bounds['lower']}")
print(f"  Upper: {result.adjusted_bounds['upper']}")
print(f"\nPerformance Improvements:")
print(f"  Convergence: {result.convergence_estimate:.2%}")
print(f"  Quality: {result.stability_analysis['quality_improvement']:.2%}")
print(f"  Success Rate: {result.stability_analysis['success_rate']:.2%}")