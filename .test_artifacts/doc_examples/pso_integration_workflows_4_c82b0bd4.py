# Example from: docs\technical\pso_integration_workflows.md
# Index: 4
# Runnable: True
# Hash: c82b0bd4

from src.optimization.integration.pso_factory_bridge import (
    EnhancedPSOFactory, PSOFactoryConfig, ControllerType
)

# Configure PSO optimization
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=20,
    max_iterations=50
)

# Create PSO factory and optimize
pso_factory = EnhancedPSOFactory(pso_config, "config.yaml")
optimization_result = pso_factory.optimize_controller()

# Extract results
if optimization_result['success']:
    optimized_controller = optimization_result['controller']
    best_gains = optimization_result['best_gains']
    best_cost = optimization_result['best_cost']

    print(f"Optimization successful!")
    print(f"Best gains: {best_gains}")
    print(f"Best cost: {best_cost:.6f}")

    # Use optimized controller immediately
    test_state = [0.0, 0.1, 0.05, 0.0, 0.0, 0.0]
    control_output = optimized_controller.compute_control(test_state)
    print(f"Test control output: {control_output}")
else:
    print(f"Optimization failed: {optimization_result['error']}")