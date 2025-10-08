# Example from: docs\guides\api\simulation.md
# Index: 4
# Runnable: True
# Hash: 84faf8cc

import numpy as np

# Override initial conditions
custom_ic = np.array([
    0.0,    # x (cart position)
    0.0,    # dx (cart velocity)
    0.2,    # θ₁ (first pendulum angle, rad)
    0.0,    # dθ₁ (first pendulum angular velocity)
    0.25,   # θ₂ (second pendulum angle, rad)
    0.0     # dθ₂ (second pendulum angular velocity)
])

result = runner.run(controller, initial_state=custom_ic)