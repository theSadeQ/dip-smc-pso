# Example from: docs\technical\pso_integration_workflows.md
# Index: 7
# Runnable: False
# Hash: 23192730

# example-metadata:
# runnable: false

# Advanced PSO configuration example
custom_pso_config = PSOFactoryConfig(
    controller_type=ControllerType.ADAPTIVE_SMC,
    population_size=30,              # Larger swarm for exploration
    max_iterations=100,              # Extended optimization
    convergence_threshold=1e-5,      # Strict convergence
    max_stagnation_iterations=15,    # Patience for stagnation
    enable_adaptive_bounds=True,     # Dynamic parameter bounds
    fitness_timeout=15.0,           # Longer evaluation timeout
    use_robust_evaluation=True      # Enhanced error handling
)

pso_factory = EnhancedPSOFactory(custom_pso_config)
result = pso_factory.optimize_controller()

# Detailed result analysis
if result['success']:
    print("=== Optimization Analysis ===")

    # Performance metrics
    perf = result['performance_analysis']
    print(f"Converged: {perf['converged']}")
    print(f"Final cost: {perf['final_cost']:.6f}")
    print(f"Initial cost: {perf['initial_cost']:.6f}")
    print(f"Improvement: {perf['improvement_ratio']:.1%}")
    print(f"Iterations: {perf['iterations_completed']}")

    # Validation results
    validation = result['validation_results']
    print(f"\nValidation Status:")
    print(f"  Gains valid: {validation['gains_valid']}")
    print(f"  Controller stable: {validation['controller_stable']}")
    print(f"  Performance acceptable: {validation['performance_acceptable']}")

    if validation['validation_errors']:
        print(f"  Warnings: {validation['validation_errors']}")