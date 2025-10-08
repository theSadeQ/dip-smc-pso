# Example from: docs\api\simulation_engine_api_reference.md
# Index: 28
# Runnable: False
# Hash: 23b597b1

class DynamicsModel(Protocol):
    """Protocol for plant dynamics models."""

    def compute_dynamics(
        self,
        state: np.ndarray,
        control_input: np.ndarray,
        time: float = 0.0,
        **kwargs: Any
    ) -> DynamicsResult:
        """Compute system dynamics at given state and input."""
        ...

    def get_physics_matrices(
        self,
        state: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get physics matrices M, C, G at current state."""
        ...

    def validate_state(self, state: np.ndarray) -> bool:
        """Validate state vector format and bounds."""
        ...

    def get_state_dimension(self) -> int:
        """Get dimension of state vector."""
        ...

    def get_control_dimension(self) -> int:
        """Get dimension of control input vector."""
        ...