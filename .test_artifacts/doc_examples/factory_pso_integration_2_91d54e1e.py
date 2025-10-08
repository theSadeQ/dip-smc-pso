# Example from: docs\reference\controllers\factory_pso_integration.md
# Index: 2
# Runnable: True
# Hash: 91d54e1e

def batch_fitness(
    gains_population: np.ndarray,  # Shape: (n_particles, n_gains)
    ctrl_type: SMCType
) -> np.ndarray:  # Shape: (n_particles,)
    """Evaluate all particles in parallel."""
    controllers = [create_smc_for_pso(ctrl_type, g) for g in gains_population]
    results = batch_simulate(controllers, config)
    return np.array([compute_cost(r) for r in results])