# Example from: docs\optimization_simulation\guide.md
# Index: 10
# Runnable: True
# Hash: 2c4f9d72

t, x_batch, u_batch, sigma_batch = simulate_system_batch(
    controller_factory=factory,
    particles=particles,
    sim_time=10.0,
    dt=0.01,
    convergence_tol=0.001,  # Stop when max(|σ|) < 0.001
    grace_period=1.0        # Wait 1 second before checking
)

print(f"Converged early: {len(t)} steps < {int(10.0/0.01)} max steps")