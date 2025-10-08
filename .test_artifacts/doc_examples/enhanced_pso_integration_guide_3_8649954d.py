# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 3
# Runnable: True
# Hash: 8649954d

def optimize_smc_controller_pso(
    controller_type: str,
    simulation_config: Any,
    pso_config: Dict[str, Any],
    optimization_objectives: List[str]
) -> Dict[str, Any]:
    """
    Complete PSO optimization workflow for SMC controllers.

    Args:
        controller_type: SMC controller type ('classical_smc', etc.)
        simulation_config: Plant and simulation parameters
        pso_config: PSO algorithm parameters
        optimization_objectives: List of objectives ['ise', 'overshoot', 'settling_time']

    Returns:
        Optimization results with best gains and performance metrics
    """

    # 1. Initialize PSO-Factory Interface
    pso_interface = PSOFactoryInterface(controller_type, simulation_config)

    # 2. Setup PSO Algorithm
    from pyswarms.single import GlobalBestPSO

    # PSO parameters with adaptive bounds
    bounds = (
        np.array(pso_interface.bounds_lower),
        np.array(pso_interface.bounds_upper)
    )

    optimizer = GlobalBestPSO(
        n_particles=pso_config.get('n_particles', 30),
        dimensions=pso_interface.n_gains,
        options={
            'c1': pso_config.get('c1', 2.0),  # Cognitive component
            'c2': pso_config.get('c2', 2.0),  # Social component
            'w': pso_config.get('w', 0.9)     # Inertia weight
        },
        bounds=bounds
    )

    # 3. Define Fitness Function
    def fitness_function(particles: np.ndarray) -> np.ndarray:
        """
        Vectorized fitness evaluation for PSO particles.

        Args:
            particles: Array of shape (n_particles, n_gains)

        Returns:
            Fitness scores for each particle
        """
        fitness_scores = []

        for gains in particles:
            try:
                # Create controller with current gains
                controller_factory = pso_interface.create_pso_controller_factory()
                controller = controller_factory(gains)

                # Validate gains
                if not controller.validate_gains(gains.reshape(1, -1))[0]:
                    fitness_scores.append(1000.0)  # Penalty for invalid gains
                    continue

                # Run simulation
                simulation_result = run_simulation_with_controller(
                    controller, simulation_config
                )

                # Compute multi-objective fitness
                fitness = compute_multi_objective_fitness(
                    simulation_result, optimization_objectives
                )

                fitness_scores.append(fitness)

            except Exception as e:
                # Penalty for simulation failures
                fitness_scores.append(1000.0)

        return np.array(fitness_scores)

    # 4. Run PSO Optimization
    best_cost, best_gains = optimizer.optimize(
        fitness_function,
        iters=pso_config.get('iters', 100),
        verbose=True
    )

    # 5. Validate and Return Results
    validation_result = validate_optimization_result(
        best_gains, best_cost, controller_type, simulation_config
    )

    return {
        'best_gains': best_gains.tolist(),
        'best_fitness': float(best_cost),
        'controller_type': controller_type,
        'optimization_history': optimizer.cost_history,
        'validation_result': validation_result,
        'pso_metrics': pso_interface.metrics
    }