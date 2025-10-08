# Example from: docs\plant\models_guide.md
# Index: 2
# Runnable: True
# Hash: 27042f23

from typing import NamedTuple, Dict, Any

class DynamicsResult(NamedTuple):
    """Result of dynamics computation."""
    state_derivative: np.ndarray    # dx/dt vector
    success: bool                   # Computation succeeded
    info: Dict[str, Any]           # Diagnostics and metadata