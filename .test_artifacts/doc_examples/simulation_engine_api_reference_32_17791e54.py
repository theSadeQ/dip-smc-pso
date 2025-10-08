# Example from: docs\api\simulation_engine_api_reference.md
# Index: 32
# Runnable: False
# Hash: 17791e54

# example-metadata:
# runnable: false

@abstractmethod
def compute_dynamics(
    self,
    state: np.ndarray,
    control_input: np.ndarray,
    time: float = 0.0,
    **kwargs: Any
) -> DynamicsResult:
    """Compute system dynamics (must be implemented by subclasses)."""
    pass

@abstractmethod
def get_physics_matrices(
    self,
    state: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Get physics matrices (must be implemented by subclasses)."""
    pass

@abstractmethod
def _setup_validation(self) -> None:
    """Setup state validation (must be implemented by subclasses)."""
    pass