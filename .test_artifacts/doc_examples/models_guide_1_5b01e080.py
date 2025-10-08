# Example from: docs\plant\models_guide.md
# Index: 1
# Runnable: False
# Hash: 5b01e080

# example-metadata:
# runnable: false

from typing import Protocol, Tuple
import numpy as np

class DynamicsModel(Protocol):
    """Protocol for plant dynamics models."""

    def compute_dynamics(
        self,
        state: np.ndarray,
        control_input: np.ndarray,
        time: float = 0.0,
        **kwargs
    ) -> DynamicsResult:
        """Compute system dynamics at given state and input."""
        ...

    def get_physics_matrices(
        self,
        state: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get M, C, G matrices at current state."""
        ...

    def validate_state(self, state: np.ndarray) -> bool:
        """Validate state vector format and bounds."""
        ...