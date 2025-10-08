# Example from: docs\reports\PSO_OPTIMIZATION_ENGINEER_COMPREHENSIVE_ANALYSIS_REPORT.md
# Index: 2
# Runnable: False
# Hash: 6c945226

# example-metadata:
# runnable: false

def _compute_cost_from_traj(self, t, x_b, u_b, sigma_b):
    """Advanced multi-component fitness function"""

    # 1. State Error Integration (ISE)
    ise = np.sum((x_b[:, :-1, :] ** 2 * dt_b) * time_mask, axis=(1, 2))

    # 2. Control Effort Minimization
    u_sq = np.sum((u_b ** 2 * dt_b) * time_mask, axis=1)

    # 3. Control Rate Smoothness
    du_sq = np.sum((du ** 2 * dt_b) * time_mask, axis=1)

    # 4. Sliding Variable Stability
    sigma_sq = np.sum((sigma_b ** 2 * dt_b) * time_mask, axis=1)

    # 5. Instability Penalty (Graded)
    penalty = stability_weight * failure_penalty

    return weighted_combination + penalty