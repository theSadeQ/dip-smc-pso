# Example from: docs\issue_12_pso_optimization_report.md
# Index: 6
# Runnable: False
# Hash: 1b859e07

# In pso_optimizer.py _compute_cost_from_traj

   # Add chattering index calculation
   control_derivative = np.gradient(u_b, dt_const, axis=1)
   chattering_time = np.sqrt(np.mean(control_derivative**2, axis=1))

   # Add FFT spectral analysis
   # ... (similar to optimize_chattering_direct.py)

   # Add to fitness
   chattering_index = 0.7 * chattering_time + 0.3 * freq_index
   chattering_penalty = max(0, chattering_index - 2.0) * penalty_weight
   J += chattering_penalty