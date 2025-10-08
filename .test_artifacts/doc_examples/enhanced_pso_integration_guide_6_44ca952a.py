# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 6
# Runnable: True
# Hash: 44ca952a

def parallel_fitness_evaluation(
    particles: np.ndarray,
    controller_factory: Callable,
    simulation_config: Any,
    n_threads: int = 4
) -> np.ndarray:
    """
    Parallel fitness evaluation using thread pool.

    Significantly improves PSO performance for expensive simulations.
    """

    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time

    def evaluate_single_particle(gains: np.ndarray) -> float:
        """Evaluate fitness for single particle."""
        try:
            controller = controller_factory(gains)
            result = run_simulation_with_controller(controller, simulation_config)
            return compute_fitness(result)
        except Exception:
            return 1000.0  # Penalty for failures

    # Parallel execution
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        future_to_idx = {
            executor.submit(evaluate_single_particle, particle): idx
            for idx, particle in enumerate(particles)
        }

        fitness_scores = np.zeros(len(particles))

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                fitness_scores[idx] = future.result()
            except Exception:
                fitness_scores[idx] = 1000.0

    return fitness_scores