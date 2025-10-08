# Example from: docs\issue_12_pso_optimization_report.md
# Index: 3
# Runnable: False
# Hash: 554c41df

# optimize_chattering_direct.py

def simulate_and_evaluate(gains, controller_type, config, dynamics):
    """Direct simulation with chattering metrics."""

    # Compute chattering without excessive normalization
    control_derivative = np.gradient(control_hist, dt)
    time_domain_index = np.sqrt(np.mean(control_derivative**2))

    spectrum = np.abs(fft(control_hist))
    hf_power_ratio = high_freq_power / total_power

    chattering_index = 0.7 * time_domain_index + 0.3 * hf_power_ratio

    # Explicit multi-objective fitness
    chattering_penalty = max(0.0, chattering_index - 2.0) * 10.0
    tracking_penalty = max(0.0, tracking_error - 0.1) * 100.0

    fitness = tracking_error_rms + chattering_penalty + tracking_penalty
    return fitness

# Use PySwarms GlobalBestPSO directly
optimizer = GlobalBestPSO(n_particles=50, dimensions=n_dims, options=pso_options, bounds=bounds)
best_cost, best_gains = optimizer.optimize(objective_function, iters=300)