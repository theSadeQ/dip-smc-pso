# Example from: docs\testing\reports\2025-09-30\pso_fitness_investigation.md
# Index: 1
# Runnable: False
# Hash: 426d5279

# Automatic baseline normalization
baseline_particles = np.asarray(gains_list, dtype=float).reshape(1, -1)
res = simulate_system_batch(
    controller_factory=controller_factory,
    particles=baseline_particles,
    sim_time=self.sim_cfg.duration,
    dt=self.sim_cfg.dt,
    u_max=u_max_val,
)

# Extract baseline costs
ise_base = float(np.sum((x_b[:, :-1, :3] ** 2 * dt_arr) * time_mask, axis=(1, 2))[0])
u_sq_base = float(np.sum((u_b ** 2 * dt_arr) * time_mask, axis=1)[0])
du_sq_base = float(np.sum((du ** 2 * dt_arr) * time_mask, axis=1)[0])
sigma_sq_base = float(np.sum((sigma_b ** 2 * dt_arr) * time_mask, axis=1)[0])

# Set normalization denominators
self.norm_ise = max(ise_base, 1e-12)
self.norm_u = max(u_sq_base, 1e-12)
self.norm_du = max(du_sq_base, 1e-12)
self.norm_sigma = max(sigma_sq_base, 1e-12)