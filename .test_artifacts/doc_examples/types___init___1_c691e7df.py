# Example from: docs\reference\utils\types___init__.md
# Index: 1
# Runnable: True
# Hash: c691e7df

from src.utils.types import ClassicalSMCOutput
import numpy as np

# Controller computation returns structured output
def compute_control(x):
    u = np.array([10.0])
    state_vars = {'sliding_surface': 0.5}
    history = np.array([[0.0]])

    # Type-safe return with named fields
    return ClassicalSMCOutput(u, state_vars, history)

# Client code uses descriptive names
output = compute_control(x)
control = output.u
surface = output.state_vars['sliding_surface']
past_controls = output.history