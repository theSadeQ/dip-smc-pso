# Example from: docs\issue_12_pso_implementation_summary.md
# Index: 1
# Runnable: True
# Hash: 9c6bbd5b

# In pso_optimizer.py _compute_cost_from_traj
control_rate_normalized = du_sq / 1000.0  # e.g., 500 / 1000 = 0.5
weighted_rate = 0.01 * 0.5 = 0.005        # Negligible!

# Chattering (high du_sq) is invisible to optimizer