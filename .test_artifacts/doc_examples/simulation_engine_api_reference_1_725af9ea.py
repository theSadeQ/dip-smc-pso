# Example from: docs\api\simulation_engine_api_reference.md
# Index: 1
# Runnable: False
# Hash: 725af9ea

# example-metadata:
# runnable: false

from typing import Protocol

class DynamicsModel(Protocol):
    """Protocol for plant dynamics models."""
    def compute_dynamics(self, state, control_input, time=0.0, **kwargs) -> DynamicsResult: ...
    def get_physics_matrices(self, state) -> Tuple[np.ndarray, np.ndarray, np.ndarray]: ...
    def validate_state(self, state) -> bool: ...