# Example from: docs\api\optimization_module_api_reference.md
# Index: 14
# Runnable: False
# Hash: 1223cd70

# example-metadata:
# runnable: false

def check_convergence(
    self,
    iteration: int,
    best_fitness: float,
    mean_fitness: float,
    fitness_std: float,
    swarm_positions: np.ndarray
) -> Tuple[ConvergenceStatus, ConvergenceMetrics]:
    """
    Analyze current optimization state and determine convergence status.

    Returns
    -------
    status : ConvergenceStatus
        Current convergence status (EXPLORING, CONVERGING, CONVERGED, etc.)
    metrics : ConvergenceMetrics
        Comprehensive metrics for current iteration
    """