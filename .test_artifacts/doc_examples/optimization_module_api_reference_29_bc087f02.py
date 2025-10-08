# Example from: docs\api\optimization_module_api_reference.md
# Index: 29
# Runnable: True
# Hash: bc087f02

from src.optimization.integration.pso_factory_bridge import EnhancedPSOFactory
from src.config import load_config

# 1. Load configuration
config = load_config("config.yaml")

# 2. Create enhanced PSO factory
factory = EnhancedPSOFactory(
    controller_type='classical_smc',
    config=config,
    enable_convergence_monitoring=True,
    enable_bounds_validation=True
)

# 3. Run optimization
result = factory.optimize(
    max_iterations=100,
    convergence_tolerance=1e-6
)

# 4. Extract optimized controller
optimized_controller = factory.create_controller(result['best_pos'])

# 5. Validate performance
validation_result = factory.validate_controller(
    controller=optimized_controller,
    n_trials=10
)

print(f"Optimization Summary:")
print(f"  Best Cost: {result['best_cost']:.6f}")
print(f"  Convergence Iteration: {result['convergence_iteration']}")
print(f"  Validation Success Rate: {validation_result['success_rate']:.2%}")
print(f"  Mean Performance: {validation_result['mean_cost']:.6f} ± {validation_result['std_cost']:.6f}")