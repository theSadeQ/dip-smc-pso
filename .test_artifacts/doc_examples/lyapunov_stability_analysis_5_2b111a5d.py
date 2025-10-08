# Example from: docs\theory\lyapunov_stability_analysis.md
# Index: 5
# Runnable: True
# Hash: 2b111a5d

import numpy as np

def simulate_adaptive_gain_evolution(s_trajectory, gamma, alpha, K_init, K_min, K_max, dt, dead_zone):
    """
    Simulate adaptive gain evolution and validate boundedness.

    Args:
        s_trajectory: Time series of sliding surface values
        gamma: Adaptation rate
        alpha: Leak rate
        K_init: Initial gain
        K_min, K_max: Gain bounds
        dt: Time step
        dead_zone: Dead zone width (no adaptation if |s| < dead_zone)

    Returns:
        dict: Gain evolution and stability metrics
    """
    n_steps = len(s_trajectory)
    K_history = np.zeros(n_steps)
    K_history[0] = K_init

    for i in range(1, n_steps):
        s = s_trajectory[i-1]
        K = K_history[i-1]

        # Adaptation law with dead zone
        if abs(s) > dead_zone:
            dK = gamma * abs(s) - alpha * (K - K_init)
        else:
            dK = 0.0  # No adaptation in dead zone

        # Update gain
        K_new = K + dK * dt

        # Saturate to bounds
        K_new = np.clip(K_new, K_min, K_max)

        K_history[i] = K_new

    # Analyze boundedness
    K_mean = np.mean(K_history)
    K_std = np.std(K_history)
    K_final = K_history[-1]

    bounded = (np.min(K_history) >= K_min - 1e-6) and (np.max(K_history) <= K_max + 1e-6)

    return {
        "K_history": K_history.tolist(),
        "K_mean": float(K_mean),
        "K_std": float(K_std),
        "K_final": float(K_final),
        "K_min_observed": float(np.min(K_history)),
        "K_max_observed": float(np.max(K_history)),
        "gain_bounded": bool(bounded),
        "adaptation_active_fraction": float(np.sum(np.abs(s_trajectory) > dead_zone) / n_steps),
    }

# Example usage:
# t = np.linspace(0, 10, 1000)
# s_traj = 0.5 * np.exp(-t) * np.sin(5*t)  # Decaying oscillation
# result = simulate_adaptive_gain_evolution(
#     s_traj, gamma=10, alpha=0.1, K_init=20, K_min=10, K_max=100, dt=0.01, dead_zone=0.05
# )
# Expected: gain_bounded=True, K_final near K_init (convergence to nominal)