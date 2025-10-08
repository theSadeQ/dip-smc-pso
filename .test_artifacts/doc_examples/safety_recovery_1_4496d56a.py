# Example from: docs\reference\simulation\safety_recovery.md
# Index: 1
# Runnable: True
# Hash: 4496d56a

from src.simulation.integrators import create_integrator

# Create integrator
integrator = create_integrator('rk4', dt=0.01)

# Integrate one step
x_next = integrator.integrate(dynamics_fn, x, u, dt)