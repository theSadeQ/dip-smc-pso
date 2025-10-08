# Example from: docs\guides\api\simulation.md
# Index: 7
# Runnable: True
# Hash: 61750975

from src.core.exceptions import NumericalInstabilityError, ControlSaturationError

try:
    result = runner.run(controller)
except NumericalInstabilityError as e:
    print(f"Simulation became unstable: {e}")
    # Try smaller timestep
    runner.dt = 0.005
    result = runner.run(controller)
except ControlSaturationError as e:
    print(f"Control saturated: {e}")
    # Reduce gains or increase max_force