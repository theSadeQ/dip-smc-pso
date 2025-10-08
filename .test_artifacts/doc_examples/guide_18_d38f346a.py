# Example from: docs\optimization_simulation\guide.md
# Index: 18
# Runnable: True
# Hash: d38f346a

from benchmarks.integration import RK4Integrator
from src.plant.models.simplified import SimplifiedDIPDynamics

dynamics = SimplifiedDIPDynamics(config)
integrator = RK4Integrator(dynamics)

result = integrator.integrate(
    x0=initial_state,
    sim_time=5.0,
    dt=0.01,
    controller=controller
)