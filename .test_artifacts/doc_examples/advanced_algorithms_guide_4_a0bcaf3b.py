# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 4
# Runnable: False
# Hash: a0bcaf3b

# example-metadata:
# runnable: false

# Vectorized evaluation (FAST)
t, x_b, u_b, sigma_b = simulate_system_batch(
    controller_factory=controller_factory,
    particles=particles,  # Shape: (N, D)
    sim_time=T,
    dt=dt,
    u_max=u_max
)
# Returns: x_b.shape = (N, timesteps, 6)

# Cost computation on entire batch
costs = self._compute_cost_from_traj(t, x_b, u_b, sigma_b)
# Returns: costs.shape = (N,)