# Example from: docs\api\simulation_engine_api_reference.md
# Index: 54
# Runnable: False
# Hash: c96be8bd

# example-metadata:
# runnable: false

from src.simulation.integrators.base import BaseIntegrator

class MyCustomIntegrator(BaseIntegrator):
    """Custom integration method."""
    ORDER = 3
    ADAPTIVE = False
    # ... implement integrate() method ...

# Register custom integrator
IntegratorFactory.register_integrator('my_custom', MyCustomIntegrator)