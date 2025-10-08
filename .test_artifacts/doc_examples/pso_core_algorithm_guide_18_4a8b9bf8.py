# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 18
# Runnable: True
# Hash: 4a8b9bf8

from multiprocessing import Pool

def parallel_fitness_evaluation(positions: np.ndarray,
                                objective_func: Callable) -> np.ndarray:
    """Evaluate fitness in parallel.

    Args:
        positions: Particle positions (N × n)
        objective_func: Fitness function

    Returns:
        Fitness values (N,)
    """
    with Pool(processes=8) as pool:
        fitness = pool.map(objective_func, positions)

    return np.array(fitness)