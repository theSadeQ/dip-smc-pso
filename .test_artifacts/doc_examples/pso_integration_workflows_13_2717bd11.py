# Example from: docs\technical\pso_integration_workflows.md
# Index: 13
# Runnable: False
# Hash: 2717bd11

# Configure PSO for robustness optimization
robust_config = PSOFactoryConfig(
    controller_type=ControllerType.ADAPTIVE_SMC,
    population_size=35,
    max_iterations=120,
    fitness_timeout=25.0,    # Longer timeout for robust evaluation
    use_robust_evaluation=True
)

pso_factory = EnhancedPSOFactory(robust_config)

# Robust evaluation automatically includes:
# - Multiple initial conditions
# - Different simulation durations
# - Varying disturbance levels
# - Parameter uncertainty scenarios

result = pso_factory.optimize_controller()

if result['success']:
    # Analyze robustness metrics
    validation = result['validation_results']
    print(f"Robustness Analysis:")
    print(f"  All scenarios passed: {validation['performance_acceptable']}")
    print(f"  Controller stability: {validation['controller_stable']}")