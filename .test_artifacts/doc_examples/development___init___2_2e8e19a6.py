# Example from: docs\reference\utils\development___init__.md
# Index: 2
# Runnable: True
# Hash: 2e8e19a6

from src.utils.development import DebugTools
import numpy as np

# Enable interactive debugging
debug = DebugTools()

def problematic_function(x):
    # Set breakpoint
    debug.set_breakpoint()

    # Inspect variables
    debug.inspect_state(x)

    # Step through computation
    result = compute_control(x)

    return result

# Debug in Jupyter
x = np.random.randn(6)
result = problematic_function(x)  # Stops at breakpoint