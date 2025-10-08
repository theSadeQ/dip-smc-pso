# Example from: docs\api\simulation_engine_api_reference.md
# Index: 2
# Runnable: True
# Hash: 9bdfb13f

from src.simulation.integrators import IntegratorFactory

integrator = IntegratorFactory.create_integrator('rk4', dt=0.01)