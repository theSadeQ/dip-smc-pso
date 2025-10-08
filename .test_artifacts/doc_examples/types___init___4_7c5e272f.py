# Example from: docs\reference\utils\types___init__.md
# Index: 4
# Runnable: True
# Hash: 7c5e272f

from src.utils.types import HybridSTAOutput
from typing import Tuple
import numpy as np

def hybrid_controller(
    x: np.ndarray,
    state_vars: dict,
    history: np.ndarray
) -> HybridSTAOutput:
    \"\"\"Type-annotated controller with structured output.\"\"\"
    u = compute_hybrid_control(x)
    updated_vars = update_state_vars(state_vars, x)
    updated_history = np.vstack([history, u])

    return HybridSTAOutput(u, updated_vars, updated_history)

# Static type checker (mypy) validates this
output: HybridSTAOutput = hybrid_controller(x, state_vars, history)