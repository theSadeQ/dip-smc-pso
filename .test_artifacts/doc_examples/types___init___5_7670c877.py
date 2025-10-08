# Example from: docs\reference\utils\types___init__.md
# Index: 5
# Runnable: True
# Hash: 7670c877

from src.utils.types import ClassicalSMCOutput
import numpy as np
from typing import List

def batch_control(states: List[np.ndarray]) -> List[ClassicalSMCOutput]:
    \"\"\"Process multiple states with type-safe outputs.\"\"\"
    outputs = []

    for x in states:
        u = controller.compute_control(x, state_vars, history)
        # u is already ClassicalSMCOutput
        outputs.append(u)

    return outputs

# Type-safe batch processing
states = [x1, x2, x3]
outputs = batch_control(states)

# Extract all controls (type-safe field access)
controls = np.array([out.u for out in outputs])
surfaces = [out.state_vars['sliding_surface'] for out in outputs]