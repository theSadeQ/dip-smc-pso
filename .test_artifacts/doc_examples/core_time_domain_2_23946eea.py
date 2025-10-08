# Example from: docs\reference\simulation\core_time_domain.md
# Index: 2
# Runnable: True
# Hash: 23946eea

from src.simulation.integrators.adaptive import AdaptiveRK45Integrator

# Create adaptive integrator
integrator = AdaptiveRK45Integrator(
    rtol=1e-6,
    atol=1e-8,
    max_step=0.1,
    min_step=1e-6
)

# Simulate with automatic step size control
results = runner.simulate(
    x0=initial_state,
    duration=5.0,
    integrator=integrator
)

# Check step size history
print(f"Steps taken: {len(results.time)}")
print(f"Average dt: {np.mean(np.diff(results.time)):.6f}")