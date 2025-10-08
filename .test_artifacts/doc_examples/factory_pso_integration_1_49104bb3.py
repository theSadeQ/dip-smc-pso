# Example from: docs\reference\controllers\factory_pso_integration.md
# Index: 1
# Runnable: False
# Hash: 49104bb3

def create_fitness_function(
    ctrl_type: SMCType,
    config: Config
) -> Callable[[np.ndarray], float]:
    """Returns fitness function for PSO."""

    def fitness(gains: np.ndarray) -> float:
        # Create controller with candidate gains
        controller = create_smc_for_pso(ctrl_type, gains)

        # Simulate
        result = simulate(controller, config)

        # Compute cost
        return compute_cost(result)

    return fitness