# Example from: docs\reference\simulation\integrators_fixed_step_runge_kutta.md
# Index: 1
# Runnable: True
# Hash: cfd65544

from src.simulation.integrators import IntegratorsFixedStepRungeKutta

# Initialize
instance = IntegratorsFixedStepRungeKutta()

# Execute
result = instance.process(data)