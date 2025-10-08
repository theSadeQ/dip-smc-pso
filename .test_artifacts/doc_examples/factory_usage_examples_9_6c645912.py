# Example from: docs\technical\factory_usage_examples.md
# Index: 9
# Runnable: False
# Hash: 6c645912

# example-metadata:
# runnable: false

# Enhanced PSO configuration with robust evaluation
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.STA_SMC,
    population_size=30,              # Larger population for better exploration
    max_iterations=100,              # More iterations for convergence
    convergence_threshold=1e-5,      # Stricter convergence criteria
    max_stagnation_iterations=15,    # Early stopping for stagnation
    enable_adaptive_bounds=True,     # Dynamic bound adjustment
    enable_gradient_guidance=False,  # Pure PSO without gradient hints
    fitness_timeout=15.0,           # 15-second timeout per evaluation
    use_robust_evaluation=True      # Enable error recovery
)

pso_factory = EnhancedPSOFactory(pso_config)
result = pso_factory.optimize_controller()

# Analyze optimization performance
if result['success']:
    performance = result['performance_analysis']
    validation = result['validation_results']

    print(f"Converged: {performance['converged']}")
    print(f"Improvement ratio: {performance['improvement_ratio']:.3f}")
    print(f"Gains valid: {validation['gains_valid']}")
    print(f"Controller stable: {validation['controller_stable']}")