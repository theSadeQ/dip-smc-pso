# Example from: docs\guides\api\simulation.md
# Index: 18
# Runnable: False
# Hash: ea22b164

# Monte Carlo simulation for statistical analysis
n_samples = 1000

# Sample initial conditions from distribution
ic_mean = np.array([0, 0, 0.1, 0, 0.15, 0])
ic_std = np.array([0.05, 0, 0.05, 0, 0.05, 0])
initial_conditions = np.random.normal(ic_mean, ic_std, size=(n_samples, 6))

# Run batch
batch_results = run_batch_simulation(controller, dynamics, initial_conditions, sim_params)

# Compute statistics
ise_values = np.sum(batch_results[:, :, 2:4]**2, axis=(1, 2))  # ISE for θ₁, θ₂
mean_ise = np.mean(ise_values)
std_ise = np.std(ise_values)
percentile_95 = np.percentile(ise_values, 95)

print(f"ISE: {mean_ise:.4f} ± {std_ise:.4f}")
print(f"95th percentile: {percentile_95:.4f}")