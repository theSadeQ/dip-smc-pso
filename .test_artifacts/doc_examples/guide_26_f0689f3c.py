# Example from: docs\optimization_simulation\guide.md
# Index: 26
# Runnable: False
# Hash: f0689f3c

# example-metadata:
# runnable: false

# FAST: Vectorized batch evaluation
t, x_batch, u_batch, sigma_batch = simulate_system_batch(
    controller_factory=factory,
    particles=gain_array,
    sim_time=5.0,
    dt=0.01
)

# SLOW: Sequential loop (10-100× slower)
for i, gains in enumerate(gain_array):
    controller = factory(gains)
    t, x, u = run_simulation(controller, dynamics, 5.0, 0.01, x0)