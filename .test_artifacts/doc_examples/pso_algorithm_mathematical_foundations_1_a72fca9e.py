# Example from: docs\pso_algorithm_mathematical_foundations.md
# Index: 1
# Runnable: False
# Hash: a72fca9e

# Mathematical implementation in PSO cost function
def _combine_costs(self, costs: np.ndarray) -> np.ndarray:
    """
    Combine costs across uncertainty draws.

    costs: Array of shape (n_draws, n_particles)
    Returns: Array of shape (n_particles,)
    """
    mean_cost = np.mean(costs, axis=0)
    max_cost = np.max(costs, axis=0)
    return self.combine_weights[0] * mean_cost + self.combine_weights[1] * max_cost