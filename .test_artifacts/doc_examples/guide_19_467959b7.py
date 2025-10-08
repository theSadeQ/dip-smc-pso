# Example from: docs\optimization_simulation\guide.md
# Index: 19
# Runnable: True
# Hash: 467959b7

from benchmarks.integration import AdaptiveRK45Integrator

integrator = AdaptiveRK45Integrator(dynamics)
result = integrator.integrate(
    x0=initial_state,
    sim_time=5.0,
    rtol=1e-8,  # Relative tolerance
    atol=1e-10, # Absolute tolerance
    controller=controller
)