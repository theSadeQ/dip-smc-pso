# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 17
# Runnable: False
# Hash: efdd0966

def optimize_controller_comprehensive():
    """Complete PSO optimization workflow example."""

    # Step 1: Configuration
    pso_config = PSOFactoryConfig(
        controller_type=ControllerType.STA_SMC,
        population_size=25,
        max_iterations=100,
        convergence_threshold=1e-5,
        fitness_timeout=15.0
    )

    # Step 2: Create PSO factory
    pso_factory = EnhancedPSOFactory(pso_config)

    # Step 3: Run optimization
    optimization_result = pso_factory.optimize_controller()

    if optimization_result['success']:
        # Step 4: Extract results
        best_gains = optimization_result['best_gains']
        best_cost = optimization_result['best_cost']
        optimized_controller = optimization_result['controller']

        # Step 5: Performance analysis
        perf_analysis = optimization_result['performance_analysis']
        validation_results = optimization_result['validation_results']

        print(f"Optimization successful!")
        print(f"Best gains: {best_gains}")
        print(f"Best cost: {best_cost:.6f}")
        print(f"Converged: {perf_analysis['converged']}")

        return optimized_controller, optimization_result
    else:
        print(f"Optimization failed: {optimization_result['error']}")
        return None, optimization_result