# Example from: docs\theory\pso_algorithm_foundations.md
# Index: 1
# Runnable: True
# Hash: f4444593

import numpy as np

def simulate_pso_particle_trajectory(
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    personal_best: np.ndarray,
    global_best: np.ndarray,
    w: float,
    c1: float,
    c2: float,
    n_iterations: int,
    seed: int = 42
) -> dict:
    """
    Simulate PSO particle trajectory for a simple test function.

    This validates the position/velocity update equations by tracking
    a single particle's motion through the search space.

    Parameters
    ----------
    initial_position : np.ndarray, shape (D,)
        Starting position of particle
    initial_velocity : np.ndarray, shape (D,)
        Initial velocity vector
    personal_best : np.ndarray, shape (D,)
        Particle's personal best position (fixed for this demo)
    global_best : np.ndarray, shape (D,)
        Swarm's global best position (fixed for this demo)
    w : float
        Inertia weight
    c1 : float
        Cognitive coefficient
    c2 : float
        Social coefficient
    n_iterations : int
        Number of PSO iterations to simulate
    seed : int
        Random seed for reproducibility

    Returns
    -------
    dict
        Trajectory data with positions, velocities, and convergence metrics
    """
    rng = np.random.default_rng(seed)
    D = len(initial_position)

    # Initialize storage
    positions = np.zeros((n_iterations + 1, D))
    velocities = np.zeros((n_iterations + 1, D))

    positions[0] = initial_position.copy()
    velocities[0] = initial_velocity.copy()

    # PSO main loop
    for t in range(n_iterations):
        # Random coefficients
        r1 = rng.uniform(0, 1, D)
        r2 = rng.uniform(0, 1, D)

        # Velocity update equation
        v_inertia = w * velocities[t]
        v_cognitive = c1 * r1 * (personal_best - positions[t])
        v_social = c2 * r2 * (global_best - positions[t])

        velocities[t+1] = v_inertia + v_cognitive + v_social

        # Position update equation
        positions[t+1] = positions[t] + velocities[t+1]

    # Convergence metrics
    distances_to_gbest = np.linalg.norm(positions - global_best, axis=1)
    velocity_magnitudes = np.linalg.norm(velocities, axis=1)

    # Exponential convergence check
    # Expect: distance ~ exp(-alpha * t) for stable parameters
    if n_iterations > 10:
        # Fit exponential decay to distance
        t_vals = np.arange(n_iterations + 1)
        log_dist = np.log(distances_to_gbest + 1e-10)

        # Linear regression on log scale
        valid_idx = np.isfinite(log_dist)
        if np.sum(valid_idx) > 5:
            coeffs = np.polyfit(t_vals[valid_idx], log_dist[valid_idx], 1)
            convergence_rate = -coeffs[0]  # Negative slope = decay rate
        else:
            convergence_rate = 0.0
    else:
        convergence_rate = 0.0

    return {
        "positions": positions,
        "velocities": velocities,
        "distances_to_gbest": distances_to_gbest,
        "velocity_magnitudes": velocity_magnitudes,
        "final_position": positions[-1],
        "final_distance": distances_to_gbest[-1],
        "convergence_rate": convergence_rate,
        "converged": distances_to_gbest[-1] < 1e-3,
    }

# Expected output (example):
# result = simulate_pso_particle_trajectory(
#     initial_position=np.array([5.0, 5.0]),
#     initial_velocity=np.array([0.0, 0.0]),
#     personal_best=np.array([3.0, 3.0]),
#     global_best=np.array([0.0, 0.0]),
#     w=0.7, c1=2.0, c2=2.0, n_iterations=50
# )
# Expected: converged=True, convergence_rate > 0, final_distance < 1e-3