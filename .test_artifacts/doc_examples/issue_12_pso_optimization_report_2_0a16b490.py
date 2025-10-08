# Example from: docs\issue_12_pso_optimization_report.md
# Index: 2
# Runnable: True
# Hash: 0a16b490

# In _compute_cost_from_traj:
ise_normalized = ise / 10.0       # e.g., 5.0 / 10.0 = 0.5
weighted_cost = 1.0 * 0.5 = 0.5

control_effort_norm = u_sq / 100.0  # e.g., 1000 / 100 = 10.0
weighted_ctrl = 0.1 * 10.0 = 1.0

control_rate_norm = du_sq / 1000.0  # e.g., 500 / 1000 = 0.5
weighted_rate = 0.01 * 0.5 = 0.005  # Negligible!

# Total cost is dominated by tracking, control derivative term vanishes
# PSO sees all particles as nearly equivalent (cost ≈ 0.0)