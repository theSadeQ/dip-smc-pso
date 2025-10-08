# Example from: docs\theory\pso_algorithm_foundations.md
# Index: 4
# Runnable: True
# Hash: 48750df7

import numpy as np

def analyze_conditioning_impact(
    condition_numbers: list,
    dimension: int = 10,
    n_trials: int = 5,
    n_iterations: int = 100
) -> dict:
    """
    Analyze PSO convergence on quadratic problems with varying condition numbers.

    Validates that ill-conditioned problems (high kappa) converge slower.

    Parameters
    ----------
    condition_numbers : list
        List of condition numbers to test (e.g., [1, 10, 100, 1000, 10000])
    dimension : int
        Problem dimensionality
    n_trials : int
        Trials per condition number
    n_iterations : int
        PSO iterations

    Returns
    -------
    dict
        Convergence rates vs condition number
    """
    results = []

    for kappa in condition_numbers:
        convergence_rates = []

        for trial in range(n_trials):
            # Create quadratic with specified condition number
            eigenvalues = np.logspace(0, np.log10(kappa), dimension)
            Q = np.diag(eigenvalues)  # Diagonal Hessian

            # Quadratic objective: f(x) = 0.5 * x^T Q x
            def objective(x):
                return 0.5 * x @ Q @ x

            # PSO optimization
            rng = np.random.default_rng(42 + trial)
            N = 20
            positions = rng.uniform(-10, 10, (N, dimension))
            velocities = rng.uniform(-1, 1, (N, dimension))

            p_best = positions.copy()
            p_best_costs = np.array([objective(x) for x in positions])
            g_best = p_best[np.argmin(p_best_costs)].copy()

            cost_history = [objective(g_best)]

            for t in range(n_iterations):
                for i in range(N):
                    r1 = rng.uniform(0, 1, dimension)
                    r2 = rng.uniform(0, 1, dimension)

                    velocities[i] = (0.7 * velocities[i] +
                                    2.0 * r1 * (p_best[i] - positions[i]) +
                                    2.0 * r2 * (g_best - positions[i]))

                    positions[i] = positions[i] + velocities[i]

                    cost = objective(positions[i])
                    if cost < p_best_costs[i]:
                        p_best[i] = positions[i].copy()
                        p_best_costs[i] = cost

                        if cost < objective(g_best):
                            g_best = positions[i].copy()

                cost_history.append(objective(g_best))

            # Estimate convergence rate from exponential fit
            log_costs = np.log(np.array(cost_history) + 1e-10)
            t_vals = np.arange(len(log_costs))

            valid = np.isfinite(log_costs)
            if np.sum(valid) > 10:
                coeffs = np.polyfit(t_vals[valid], log_costs[valid], 1)
                rate = -coeffs[0]  # Decay rate
            else:
                rate = 0.0

            convergence_rates.append(rate)

        results.append({
            "condition_number": float(kappa),
            "mean_convergence_rate": float(np.mean(convergence_rates)),
            "std_convergence_rate": float(np.std(convergence_rates)),
        })

    return {"conditioning_analysis": results}

# Expected output:
# - Convergence rate decreases as kappa increases
# - Well-conditioned (kappa=1): rate ~ 0.1-0.2
# - Ill-conditioned (kappa=10000): rate ~ 0.001-0.01