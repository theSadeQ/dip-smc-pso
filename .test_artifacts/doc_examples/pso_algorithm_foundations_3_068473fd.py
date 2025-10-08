# Example from: docs\theory\pso_algorithm_foundations.md
# Index: 3
# Runnable: True
# Hash: 068473fd

import numpy as np
from scipy.optimize import rosen  # Rosenbrock function for testing

def parameter_sensitivity_analysis(
    test_function,
    bounds: tuple,
    dimension: int,
    parameter_ranges: dict,
    n_trials: int = 10,
    n_iterations: int = 50,
    seed: int = 42
) -> dict:
    """
    Systematic parameter sensitivity analysis for PSO.

    Tests the impact of w, c1, c2, and swarm size on convergence
    performance using a standard test function.

    Parameters
    ----------
    test_function : callable
        Objective function to minimize (e.g., Rosenbrock)
    bounds : tuple
        (min, max) bounds for each dimension
    dimension : int
        Problem dimensionality
    parameter_ranges : dict
        Ranges for w, c1, c2, N to test
    n_trials : int
        Number of independent runs per parameter combination
    n_iterations : int
        PSO iterations per trial
    seed : int
        Random seed base

    Returns
    -------
    dict
        Sensitivity results with convergence statistics
    """
    results = {
        "inertia_weight": [],
        "cognitive_coeff": [],
        "social_coeff": [],
        "swarm_size": [],
    }

    # Test inertia weight sensitivity
    for w in parameter_ranges.get("w", [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]):
        costs = []
        for trial in range(n_trials):
            rng = np.random.default_rng(seed + trial)

            # Initialize swarm
            N = 20
            positions = rng.uniform(bounds[0], bounds[1], (N, dimension))
            velocities = rng.uniform(-1, 1, (N, dimension))

            # Personal and global bests
            p_best = positions.copy()
            p_best_costs = np.array([test_function(x) for x in positions])
            g_best = p_best[np.argmin(p_best_costs)].copy()

            # PSO iterations
            for t in range(n_iterations):
                for i in range(N):
                    r1 = rng.uniform(0, 1, dimension)
                    r2 = rng.uniform(0, 1, dimension)

                    velocities[i] = (w * velocities[i] +
                                    2.0 * r1 * (p_best[i] - positions[i]) +
                                    2.0 * r2 * (g_best - positions[i]))

                    positions[i] = positions[i] + velocities[i]
                    positions[i] = np.clip(positions[i], bounds[0], bounds[1])

                    cost = test_function(positions[i])
                    if cost < p_best_costs[i]:
                        p_best[i] = positions[i].copy()
                        p_best_costs[i] = cost

                        if cost < test_function(g_best):
                            g_best = positions[i].copy()

            final_cost = test_function(g_best)
            costs.append(final_cost)

        results["inertia_weight"].append({
            "w": float(w),
            "mean_cost": float(np.mean(costs)),
            "std_cost": float(np.std(costs)),
            "min_cost": float(np.min(costs)),
        })

    # Similar analysis for c1, c2, and N (abbreviated for brevity)
    # Full implementation in validation script

    return results

# Expected output:
# - Optimal w around 0.6-0.7 for Rosenbrock
# - Performance degrades for w < 0.4 or w > 0.9
# - Balanced c1=c2=2.0 outperforms imbalanced coefficients