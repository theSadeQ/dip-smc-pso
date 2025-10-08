# Example from: docs\api\optimization_module_api_reference.md
# Index: 9
# Runnable: False
# Hash: be72abdd

# example-metadata:
# runnable: false

def custom_fitness(particles: np.ndarray) -> np.ndarray:
    """
    Custom fitness function for specific control objectives.

    Parameters
    ----------
    particles : np.ndarray
        Gain vectors (shape: B × D)

    Returns
    -------
    np.ndarray
        Fitness values (shape: B,)
    """
    B = particles.shape[0]
    fitness = np.zeros(B)

    for i, gains in enumerate(particles):
        # Create controller
        controller = create_controller('classical_smc', config=config, gains=gains)

        # Simulate
        result = simulate(controller, duration=5.0, dt=0.01)

        # Custom cost: settle time + overshoot
        settle_time = compute_settle_time(result.states, threshold=0.02)
        overshoot = compute_overshoot(result.states)

        fitness[i] = 10.0 * settle_time + 50.0 * overshoot

    return fitness