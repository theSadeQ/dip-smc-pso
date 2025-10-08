# Example from: docs\technical\factory_usage_examples.md
# Index: 8
# Runnable: True
# Hash: 059bdefe

from src.optimization.integration.pso_factory_bridge import (
    EnhancedPSOFactory, PSOFactoryConfig, ControllerType
)

# Configure PSO optimization
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=20,
    max_iterations=50,
    convergence_threshold=1e-6
)

# Create and run PSO optimization
pso_factory = EnhancedPSOFactory(pso_config, "config.yaml")
optimization_result = pso_factory.optimize_controller()

if optimization_result['success']:
    optimized_controller = optimization_result['controller']
    best_gains = optimization_result['best_gains']
    best_cost = optimization_result['best_cost']

    print(f"Optimization successful!")
    print(f"Best gains: {best_gains}")
    print(f"Best cost: {best_cost:.6f}")
else:
    print(f"Optimization failed: {optimization_result['error']}")