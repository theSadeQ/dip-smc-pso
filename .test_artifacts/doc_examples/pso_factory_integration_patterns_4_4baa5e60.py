# Example from: docs\pso_factory_integration_patterns.md
# Index: 4
# Runnable: False
# Hash: 4baa5e60

def basic_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Standard PSO optimization workflow for SMC controllers."""

    # Step 1: Get gain bounds based on control theory
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(controller_type)

    # Step 2: Create optimized factory function
    controller_factory = create_pso_controller_factory(
        controller_type,
        plant_config=load_config("config.yaml").physics
    )

    # Step 3: Define fitness function with validation
    def fitness_function(gains: np.ndarray) -> float:
        """PSO fitness function with robust error handling."""

        # Pre-validate gains
        if not validate_smc_gains(controller_type, gains):
            return float('inf')  # Invalid gains get worst fitness

        try:
            # Create controller
            controller = controller_factory(gains)

            # Evaluate performance
            metrics = evaluate_controller_performance(controller)

            # Combine multiple objectives
            fitness = (
                0.4 * metrics['control_effort'] +
                0.3 * metrics['tracking_error'] +
                0.2 * metrics['settling_time'] +
                0.1 * metrics['overshoot_penalty']
            )

            return fitness

        except Exception as e:
            logger.warning(f"Controller evaluation failed: {e}")
            return float('inf')

    # Step 4: Configure and run PSO
    pso_config = {
        'n_particles': 30,
        'max_iter': 100,
        'bounds': (lower_bounds, upper_bounds),
        'w': 0.9,       # Inertia weight
        'c1': 2.0,      # Cognitive coefficient
        'c2': 2.0       # Social coefficient
    }

    tuner = PSOTuner(
        controller_factory=fitness_function,
        config=config,
        **pso_config
    )

    # Step 5: Run optimization
    best_gains, best_fitness = tuner.optimize()

    # Step 6: Validate results
    final_controller = controller_factory(best_gains)
    final_metrics = evaluate_controller_performance(final_controller)

    logger.info(f"Optimization complete:")
    logger.info(f"Best gains: {best_gains}")
    logger.info(f"Best fitness: {best_fitness}")
    logger.info(f"Final metrics: {final_metrics}")

    return best_gains, best_fitness