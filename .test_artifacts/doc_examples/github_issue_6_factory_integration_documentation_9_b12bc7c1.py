# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 9
# Runnable: True
# Hash: b12bc7c1

def optimize_smc_with_factory(controller_type: str,
                             simulation_config: Dict[str, Any],
                             pso_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Complete PSO optimization workflow using factory pattern.

    This function demonstrates the full integration between:
    - Factory pattern for controller creation
    - PSO optimization algorithm
    - Simulation framework for evaluation
    - Performance metrics computation

    Workflow:
    1. Create PSO-optimized factory function
    2. Setup PSO algorithm with factory-derived bounds
    3. Define fitness function using factory controller creation
    4. Execute PSO optimization with parallel evaluation
    5. Validate and return optimized controller parameters

    Args:
        controller_type: SMC type ('classical_smc', 'sta_smc', etc.)
        simulation_config: Simulation parameters and test scenarios
        pso_config: PSO algorithm configuration

    Returns:
        Optimization results with best gains and validation metrics
    """

    # Convert string to SMCType enum
    smc_type = SMCType(controller_type)

    # Get factory-derived PSO bounds
    bounds = get_gain_bounds_for_pso(smc_type)
    bounds_array = np.array(bounds)

    # Create PSO algorithm with factory bounds
    from pyswarms.single import GlobalBestPSO

    optimizer = GlobalBestPSO(
        n_particles=pso_config.get('n_particles', 30),
        dimensions=len(bounds),
        options={
            'c1': pso_config.get('c1', 2.0),  # Cognitive component
            'c2': pso_config.get('c2', 2.0),  # Social component
            'w': pso_config.get('w', 0.9)     # Inertia weight
        },
        bounds=(bounds_array[:, 0], bounds_array[:, 1])
    )

    # Define fitness function using factory
    def fitness_function(particles: np.ndarray) -> np.ndarray:
        """
        PSO fitness function using factory pattern.

        For each particle (gain set):
        1. Create controller using factory
        2. Run simulation with controller
        3. Compute performance metrics
        4. Return fitness score (lower is better)
        """
        fitness_scores = []

        for gains in particles:
            try:
                # Create controller using factory with validation
                controller = create_smc_for_pso(
                    smc_type=smc_type,
                    gains=gains.tolist(),
                    max_force=simulation_config.get('max_force', 100.0)
                )

                # Run simulation
                simulation_result = run_simulation_with_controller(
                    controller, simulation_config
                )

                # Compute multi-objective fitness
                fitness = compute_control_performance_metrics(
                    simulation_result,
                    objectives=['ise', 'overshoot', 'control_effort']
                )

                fitness_scores.append(fitness)

            except Exception as e:
                # Invalid gains get penalty fitness
                fitness_scores.append(1000.0)

        return np.array(fitness_scores)

    # Execute PSO optimization
    best_cost, best_gains = optimizer.optimize(
        fitness_function,
        iters=pso_config.get('iters', 100),
        verbose=True
    )

    # Validate optimization result
    final_controller = create_smc_for_pso(smc_type, best_gains.tolist())
    validation_result = validate_optimized_controller(
        final_controller, simulation_config
    )

    return {
        'best_gains': best_gains.tolist(),
        'best_fitness': float(best_cost),
        'controller_type': controller_type,
        'smc_type': smc_type.value,
        'optimization_history': optimizer.cost_history,
        'validation_result': validation_result,
        'bounds_used': bounds,
        'pso_config': pso_config
    }