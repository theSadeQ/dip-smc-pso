# Example from: docs\optimization_simulation\guide.md
# Index: 27
# Runnable: True
# Hash: 8a8d623e

t, x_batch, u_batch, sigma_batch = simulate_system_batch(
    controller_factory=factory,
    particles=particles,
    sim_time=10.0,
    dt=0.01,
    convergence_tol=0.001,  # Stop when converged
    grace_period=1.0        # Minimum settling time
)